import os
import io
import base64
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
from urllib.request import urlopen

from alibabacloud_facebody20191230.client import Client
from alibabacloud_facebody20191230.models import (
    RecognizeActionAdvanceRequestURLList,
    RecognizeActionAdvanceRequest
)
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions

load_dotenv()


class PostureDetectionResult:
    def __init__(
        self,
        status: str,
        score: float,
        head_angle: float,
        shoulder_balance: str,
        back_curve: str,
        eye_distance: float,
        details: Dict[str, Any] = None
    ):
        self.status = status
        self.score = score
        self.head_angle = head_angle
        self.shoulder_balance = shoulder_balance
        self.back_curve = back_curve
        self.eye_distance = eye_distance
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "score": self.score,
            "head_angle": self.head_angle,
            "shoulder_balance": self.shoulder_balance,
            "back_curve": self.back_curve,
            "eye_distance": self.eye_distance,
            "details": self.details
        }


class PostureQuantification:
    def __init__(self):
        self.good_posture_threshold = 70.0
        self.warning_threshold = 50.0
        self.head_angle_good = 10.0
        self.head_angle_warning = 20.0
        self.eye_distance_good_min = 35.0
        self.eye_distance_good_max = 50.0
        self.eye_distance_warning_min = 25.0
        self.eye_distance_warning_max = 60.0
    
    def calculate_posture_score(
        self,
        head_angle: float,
        shoulder_balance_score: float,
        back_curve_score: float,
        eye_distance: float
    ) -> float:
        head_score = 100.0
        if head_angle > self.head_angle_good:
            if head_angle > self.head_angle_warning:
                head_score = max(0, 100 - (head_angle - self.head_angle_warning) * 3)
            else:
                head_score = max(50, 100 - (head_angle - self.head_angle_good) * 5)
        
        eye_score = 100.0
        if self.eye_distance_good_min <= eye_distance <= self.eye_distance_good_max:
            eye_score = 100.0
        elif self.eye_distance_warning_min <= eye_distance <= self.eye_distance_warning_max:
            if eye_distance < self.eye_distance_good_min:
                eye_score = 100 - (self.eye_distance_good_min - eye_distance) * 3
            else:
                eye_score = 100 - (eye_distance - self.eye_distance_good_max) * 3
        else:
            eye_score = max(0, 50 - abs(eye_distance - 45) * 2)
        
        weights = {
            "head": 0.35,
            "shoulder": 0.25,
            "back": 0.25,
            "eye": 0.15
        }
        
        total_score = (
            head_score * weights["head"] +
            shoulder_balance_score * weights["shoulder"] +
            back_curve_score * weights["back"] +
            eye_score * weights["eye"]
        )
        
        return round(total_score, 1)
    
    def determine_status(self, score: float) -> str:
        if score >= self.good_posture_threshold:
            return "good"
        elif score >= self.warning_threshold:
            return "warning"
        else:
            return "danger"
    
    def get_recommendation(self, status: str, details: Dict[str, Any]) -> str:
        recommendations = []
        
        if details.get("head_angle", 0) > self.head_angle_warning:
            recommendations.append("头部前倾严重，请抬起头部，保持颈椎自然")
        elif details.get("head_angle", 0) > self.head_angle_good:
            recommendations.append("头部轻微前倾，请注意调整")
        
        if details.get("shoulder_balance") == "不平衡":
            recommendations.append("肩膀不平衡，请调整坐姿，保持双肩水平")
        elif details.get("shoulder_balance") == "需注意":
            recommendations.append("肩膀轻微倾斜，请注意保持平衡")
        
        if details.get("back_curve") == "过度弯曲":
            recommendations.append("背部过度弯曲，请挺直腰背，保持脊柱自然曲线")
        elif details.get("back_curve") == "轻微弯曲":
            recommendations.append("背部轻微弯曲，请注意挺直")
        
        eye_dist = details.get("eye_distance", 45)
        if eye_dist < self.eye_distance_warning_min:
            recommendations.append("眼睛距离屏幕太近，请保持35-50cm的距离")
        elif eye_dist > self.eye_distance_warning_max:
            recommendations.append("眼睛距离屏幕太远，请适当调整距离")
        
        if not recommendations:
            if status == "good":
                recommendations.append("坐姿良好，请继续保持")
            else:
                recommendations.append("请调整坐姿，保持正确姿势")
        
        return "；".join(recommendations)


class AliyunPostureService:
    def __init__(self):
        self.access_key_id = os.getenv("ALIYUN_OCR_ACCESS_KEY_ID")
        self.access_key_secret = os.getenv("ALIYUN_OCR_ACCESS_KEY_SECRET")
        self.endpoint = "facebody.cn-shanghai.aliyuncs.com"
        self.region_id = "cn-shanghai"
        self.is_available = self.access_key_id and self.access_key_secret and \
                         self.access_key_id != "your-aliyun-access-key-id"
        
        self.quantification = PostureQuantification()
        self._client = None
    
    def _get_client(self) -> Client:
        if self._client is None:
            config = Config(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
                endpoint=self.endpoint,
                region_id=self.region_id
            )
            self._client = Client(config)
        return self._client
    
    def _parse_action_result(self, action_result: Dict[str, Any]) -> Dict[str, Any]:
        parsed = {
            "action_type": None,
            "confidence": 0.0,
            "keypoints": [],
            "skeleton_data": {}
        }
        
        if not action_result:
            return parsed
        
        if "Data" in action_result:
            data = action_result["Data"]
            if "ActionList" in data and data["ActionList"]:
                action = data["ActionList"][0]
                parsed["action_type"] = action.get("ActionName", "unknown")
                parsed["confidence"] = action.get("Score", 0.0)
            
            if "SkeletonList" in data:
                parsed["skeleton_data"] = data["SkeletonList"]
        
        return parsed
    
    def _calculate_metrics_from_skeleton(self, skeleton_data: List[Dict]) -> Dict[str, Any]:
        metrics = {
            "head_angle": 0.0,
            "shoulder_balance": "良好",
            "back_curve": "正常",
            "eye_distance": 45.0,
            "shoulder_score": 100.0,
            "back_score": 100.0
        }
        
        if not skeleton_data:
            return metrics
        
        try:
            skeleton = skeleton_data[0] if isinstance(skeleton_data, list) else skeleton_data
            keypoints = skeleton.get("Keypoints", [])
            
            if not keypoints:
                return metrics
            
            keypoint_dict = {}
            for kp in keypoints:
                keypoint_dict[kp.get("Name", "")] = {
                    "x": kp.get("X", 0),
                    "y": kp.get("Y", 0),
                    "confidence": kp.get("Confidence", 0)
                }
            
            if "nose" in keypoint_dict and "neck" in keypoint_dict:
                nose = keypoint_dict["nose"]
                neck = keypoint_dict["neck"]
                dx = nose["x"] - neck["x"]
                dy = nose["y"] - neck["y"]
                import math
                angle = math.degrees(math.atan2(abs(dx), abs(dy)))
                metrics["head_angle"] = round(angle, 1)
            
            if "left_shoulder" in keypoint_dict and "right_shoulder" in keypoint_dict:
                left_shoulder = keypoint_dict["left_shoulder"]
                right_shoulder = keypoint_dict["right_shoulder"]
                y_diff = abs(left_shoulder["y"] - right_shoulder["y"])
                x_diff = abs(left_shoulder["x"] - right_shoulder["x"])
                
                if y_diff > 20:
                    metrics["shoulder_balance"] = "不平衡"
                    metrics["shoulder_score"] = max(0, 100 - y_diff * 2)
                elif y_diff > 10:
                    metrics["shoulder_balance"] = "需注意"
                    metrics["shoulder_score"] = max(50, 100 - y_diff)
                else:
                    metrics["shoulder_balance"] = "良好"
                    metrics["shoulder_score"] = 100.0
            
            if "neck" in keypoint_dict and "mid_hip" in keypoint_dict:
                neck = keypoint_dict["neck"]
                mid_hip = keypoint_dict["mid_hip"]
                dx = neck["x"] - mid_hip["x"]
                dy = neck["y"] - mid_hip["y"]
                
                import math
                back_angle = math.degrees(math.atan2(abs(dx), abs(dy)))
                
                if back_angle > 15:
                    metrics["back_curve"] = "过度弯曲"
                    metrics["back_score"] = max(0, 100 - back_angle * 3)
                elif back_angle > 8:
                    metrics["back_curve"] = "轻微弯曲"
                    metrics["back_score"] = max(50, 100 - back_angle * 2)
                else:
                    metrics["back_curve"] = "正常"
                    metrics["back_score"] = 100.0
            
            if "nose" in keypoint_dict:
                nose = keypoint_dict["nose"]
                frame_height = skeleton.get("Height", 480)
                relative_y = nose["y"] / frame_height if frame_height else 0.5
                
                if relative_y > 0.7:
                    metrics["eye_distance"] = 25.0
                elif relative_y > 0.5:
                    metrics["eye_distance"] = 35.0 + (0.7 - relative_y) * 50
                else:
                    metrics["eye_distance"] = 45.0
        
        except Exception as e:
            print(f"计算骨架指标错误: {e}")
        
        return metrics
    
    async def detect_posture_from_images(
        self,
        images: List[bytes]
    ) -> PostureDetectionResult:
        if not self.is_available:
            return self._get_mock_result()
        
        if len(images) < 2:
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="未知",
                back_curve="未知",
                eye_distance=0,
                details={"error": "需要至少2张图片进行动作识别"}
            )
        
        try:
            client = self._get_client()
            runtime_option = RuntimeOptions()
            
            urllist = []
            for img_data in images[:4]:
                url_item = RecognizeActionAdvanceRequestURLList()
                url_item.urlobject = io.BytesIO(img_data)
                urllist.append(url_item)
            
            request = RecognizeActionAdvanceRequest(
                type=1,
                urllist=urllist
            )
            
            response = client.recognize_action_advance(request, runtime_option)
            
            if response.body:
                result_data = json.loads(str(response.body))
                parsed = self._parse_action_result(result_data)
                
                metrics = self._calculate_metrics_from_skeleton(
                    parsed.get("skeleton_data", [])
                )
                
                score = self.quantification.calculate_posture_score(
                    metrics["head_angle"],
                    metrics["shoulder_score"],
                    metrics["back_score"],
                    metrics["eye_distance"]
                )
                
                status = self.quantification.determine_status(score)
                
                recommendation = self.quantification.get_recommendation(
                    status,
                    {
                        "head_angle": metrics["head_angle"],
                        "shoulder_balance": metrics["shoulder_balance"],
                        "back_curve": metrics["back_curve"],
                        "eye_distance": metrics["eye_distance"]
                    }
                )
                
                return PostureDetectionResult(
                    status=status,
                    score=score,
                    head_angle=metrics["head_angle"],
                    shoulder_balance=metrics["shoulder_balance"],
                    back_curve=metrics["back_curve"],
                    eye_distance=metrics["eye_distance"],
                    details={
                        "action_type": parsed.get("action_type"),
                        "confidence": parsed.get("confidence"),
                        "recommendation": recommendation,
                        "raw_result": result_data
                    }
                )
            else:
                return self._get_mock_result()
                
        except Exception as e:
            print(f"坐姿检测错误: {e}")
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="错误",
                back_curve="错误",
                eye_distance=0,
                details={"error": str(e)}
            )
    
    async def detect_posture_from_urls(
        self,
        image_urls: List[str]
    ) -> PostureDetectionResult:
        if not self.is_available:
            return self._get_mock_result()
        
        if len(image_urls) < 2:
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="未知",
                back_curve="未知",
                eye_distance=0,
                details={"error": "需要至少2张图片URL进行动作识别"}
            )
        
        try:
            images = []
            for url in image_urls[:4]:
                img_data = urlopen(url).read()
                images.append(img_data)
            
            return await self.detect_posture_from_images(images)
            
        except Exception as e:
            print(f"从URL检测坐姿错误: {e}")
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="错误",
                back_curve="错误",
                eye_distance=0,
                details={"error": str(e)}
            )
    
    async def detect_posture_from_base64(
        self,
        base64_images: List[str]
    ) -> PostureDetectionResult:
        if not self.is_available:
            return self._get_mock_result()
        
        if len(base64_images) < 2:
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="未知",
                back_curve="未知",
                eye_distance=0,
                details={"error": "需要至少2张Base64图片进行动作识别"}
            )
        
        try:
            images = []
            for b64_img in base64_images[:4]:
                if "," in b64_img:
                    b64_img = b64_img.split(",")[1]
                img_data = base64.b64decode(b64_img)
                images.append(img_data)
            
            return await self.detect_posture_from_images(images)
            
        except Exception as e:
            print(f"从Base64检测坐姿错误: {e}")
            return PostureDetectionResult(
                status="error",
                score=0,
                head_angle=0,
                shoulder_balance="错误",
                back_curve="错误",
                eye_distance=0,
                details={"error": str(e)}
            )
    
    def _get_mock_result(self) -> PostureDetectionResult:
        import random
        
        status = "good"
        head_angle = random.uniform(0, 8)
        shoulder_score = random.uniform(90, 100)
        back_score = random.uniform(90, 100)
        eye_distance = random.uniform(40, 50)
        
        rand = random.random()
        if rand > 0.9:
            status = "danger"
            head_angle = random.uniform(25, 40)
            shoulder_score = random.uniform(30, 50)
            back_score = random.uniform(30, 50)
            eye_distance = random.uniform(20, 30)
        elif rand > 0.7:
            status = "warning"
            head_angle = random.uniform(10, 20)
            shoulder_score = random.uniform(60, 80)
            back_score = random.uniform(60, 80)
            eye_distance = random.uniform(30, 40)
        
        score = self.quantification.calculate_posture_score(
            head_angle, shoulder_score, back_score, eye_distance
        )
        
        shoulder_balance = "良好" if shoulder_score >= 90 else ("需注意" if shoulder_score >= 70 else "不平衡")
        back_curve = "正常" if back_score >= 90 else ("轻微弯曲" if back_score >= 70 else "过度弯曲")
        
        recommendation = self.quantification.get_recommendation(
            status,
            {
                "head_angle": head_angle,
                "shoulder_balance": shoulder_balance,
                "back_curve": back_curve,
                "eye_distance": eye_distance
            }
        )
        
        return PostureDetectionResult(
            status=status,
            score=score,
            head_angle=round(head_angle, 1),
            shoulder_balance=shoulder_balance,
            back_curve=back_curve,
            eye_distance=round(eye_distance, 1),
            details={
                "recommendation": recommendation,
                "is_mock": True,
                "message": "阿里云服务未配置或不可用，使用模拟数据"
            }
        )


_aliyun_posture_service = None


def get_aliyun_posture_service() -> AliyunPostureService:
    global _aliyun_posture_service
    if _aliyun_posture_service is None:
        _aliyun_posture_service = AliyunPostureService()
    return _aliyun_posture_service
