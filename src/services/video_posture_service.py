import os
import io
import base64
import json
import time
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from urllib.request import urlopen
import threading
from collections import deque
import statistics

from alibabacloud_facebody20191230.client import Client
from alibabacloud_facebody20191230.models import (
    RecognizeActionAdvanceRequestURLList,
    RecognizeActionAdvanceRequest
)
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions

load_dotenv()


class RealTimePostureSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.is_active = False
        self.start_time = None
        self.end_time = None
        self.frames_buffer = deque(maxlen=30)
        self.detection_results = deque(maxlen=100)
        self.total_frames = 0
        self.good_posture_frames = 0
        self.bad_posture_frames = 0
        self.warning_count = 0
        self.head_shake_count = 0
        self.distance_warning_count = 0
        self.fatigue_reminder_count = 0
        self.last_detection_time = 0
        self.detection_interval = 2.0
        
    def add_detection_result(self, result: Dict[str, Any]):
        self.detection_results.append({
            "time": datetime.utcnow().isoformat(),
            "score": result.get("score", 0),
            "status": result.get("status", "unknown"),
            "head_angle": result.get("head_angle", 0),
            "eye_distance": result.get("eye_distance", 45)
        })
        
        self.total_frames += 1
        if result.get("status") == "good":
            self.good_posture_frames += 1
        elif result.get("status") in ["warning", "danger"]:
            self.bad_posture_frames += 1
            self.warning_count += 1
        
        if result.get("head_angle", 0) > 20:
            self.head_shake_count += 1
        
        if result.get("eye_distance", 45) < 30:
            self.distance_warning_count += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        if not self.detection_results:
            return {
                "detection_count": 0,
                "good_posture_rate": 0,
                "bad_posture_count": 0,
                "warning_count": 0,
                "head_shake_count": 0,
                "distance_warning_count": 0,
                "fatigue_reminder_count": 0,
                "average_score": 0,
                "session_duration": 0
            }
        
        scores = [r["score"] for r in self.detection_results]
        avg_score = statistics.mean(scores) if scores else 0
        
        good_rate = (self.good_posture_frames / self.total_frames * 100) if self.total_frames > 0 else 0
        
        duration = 0
        if self.start_time:
            end = self.end_time or datetime.utcnow()
            duration = (end - self.start_time).total_seconds()
        
        return {
            "detection_count": self.total_frames,
            "good_posture_rate": round(good_rate, 1),
            "bad_posture_count": self.bad_posture_frames,
            "warning_count": self.warning_count,
            "head_shake_count": self.head_shake_count,
            "distance_warning_count": self.distance_warning_count,
            "fatigue_reminder_count": self.fatigue_reminder_count,
            "average_score": round(avg_score, 1),
            "session_duration": int(duration)
        }


class VideoStreamPostureService:
    def __init__(self):
        self.access_key_id = os.getenv("ALIYUN_OCR_ACCESS_KEY_ID")
        self.access_key_secret = os.getenv("ALIYUN_OCR_ACCESS_KEY_SECRET")
        self.endpoint = "facebody.cn-shanghai.aliyuncs.com"
        self.region_id = "cn-shanghai"
        self.is_available = self.access_key_id and self.access_key_secret and \
                         self.access_key_id != "your-aliyun-access-key-id"
        
        self._client = None
        self.sessions: Dict[int, RealTimePostureSession] = {}
    
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
    
    def get_or_create_session(self, user_id: int) -> RealTimePostureSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = RealTimePostureSession(user_id)
        return self.sessions[user_id]
    
    def start_session(self, user_id: int):
        session = self.get_or_create_session(user_id)
        session.is_active = True
        session.start_time = datetime.utcnow()
        session.end_time = None
    
    def stop_session(self, user_id: int):
        if user_id in self.sessions:
            session = self.sessions[user_id]
            session.is_active = False
            session.end_time = datetime.utcnow()
    
    def get_session_stats(self, user_id: int) -> Dict[str, Any]:
        if user_id not in self.sessions:
            return {
                "is_active": False,
                "statistics": {
                    "detection_count": 0,
                    "good_posture_rate": 0,
                    "bad_posture_count": 0,
                    "warning_count": 0,
                    "head_shake_count": 0,
                    "distance_warning_count": 0,
                    "fatigue_reminder_count": 0,
                    "average_score": 0,
                    "session_duration": 0
                }
            }
        
        session = self.sessions[user_id]
        stats = session.get_statistics()
        stats["is_active"] = session.is_active
        
        return stats
    
    def _calculate_metrics_from_skeleton(self, skeleton_data: List[Dict]) -> Dict[str, Any]:
        metrics = {
            "head_angle": 0.0,
            "shoulder_balance": "良好",
            "back_curve": "正常",
            "eye_distance": 45.0,
            "shoulder_score": 100.0,
            "back_score": 100.0,
            "fatigue_level": 0
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
            
            if metrics["head_angle"] > 15 or metrics["shoulder_score"] < 70:
                metrics["fatigue_level"] = 2
            elif metrics["head_angle"] > 8 or metrics["shoulder_score"] < 85:
                metrics["fatigue_level"] = 1
            else:
                metrics["fatigue_level"] = 0
        
        except Exception as e:
            print(f"计算骨架指标错误：{e}")
        
        return metrics
    
    def _calculate_posture_score(
        self,
        head_angle: float,
        shoulder_balance_score: float,
        back_curve_score: float,
        eye_distance: float
    ) -> float:
        head_score = 100.0
        if head_angle > 10:
            if head_angle > 20:
                head_score = max(0, 100 - (head_angle - 20) * 3)
            else:
                head_score = max(50, 100 - (head_angle - 10) * 5)
        
        eye_score = 100.0
        if 35 <= eye_distance <= 50:
            eye_score = 100.0
        elif 25 <= eye_distance < 35 or 50 < eye_distance <= 60:
            if eye_distance < 35:
                eye_score = 100 - (35 - eye_distance) * 3
            else:
                eye_score = 100 - (eye_distance - 50) * 3
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
    
    def _determine_status(self, score: float) -> str:
        if score >= 70:
            return "good"
        elif score >= 50:
            return "warning"
        else:
            return "danger"
    
    def _get_recommendation(self, status: str, details: Dict[str, Any]) -> str:
        recommendations = []
        
        if details.get("head_angle", 0) > 20:
            recommendations.append("头部前倾严重，请抬起头部")
        elif details.get("head_angle", 0) > 10:
            recommendations.append("头部轻微前倾，请注意调整")
        
        if details.get("shoulder_balance") == "不平衡":
            recommendations.append("肩膀不平衡，请保持双肩水平")
        elif details.get("shoulder_balance") == "需注意":
            recommendations.append("肩膀轻微倾斜，请注意保持平衡")
        
        if details.get("back_curve") == "过度弯曲":
            recommendations.append("背部过度弯曲，请挺直腰背")
        elif details.get("back_curve") == "轻微弯曲":
            recommendations.append("背部轻微弯曲，请注意挺直")
        
        eye_dist = details.get("eye_distance", 45)
        if eye_dist < 30:
            recommendations.append("眼睛距离屏幕太近，请保持距离")
        elif eye_dist > 60:
            recommendations.append("眼睛距离屏幕太远，请适当调整")
        
        if details.get("fatigue_level", 0) >= 2:
            recommendations.append("疲劳程度较高，建议休息一下")
            return "；".join(recommendations)
        
        if not recommendations:
            if status == "good":
                recommendations.append("坐姿良好，请继续保持")
            else:
                recommendations.append("请调整坐姿，保持正确姿势")
        
        return "；".join(recommendations)
    
    async def process_video_frame(
        self,
        user_id: int,
        frame_data: bytes
    ) -> Dict[str, Any]:
        session = self.get_or_create_session(user_id)
        
        current_time = time.time()
        if current_time - session.last_detection_time < session.detection_interval:
            return {
                "success": True,
                "skipped": True,
                "message": "检测间隔太短，已跳过"
            }
        
        session.last_detection_time = current_time
        
        if not self.is_available:
            mock_result = self._generate_mock_result()
            session.add_detection_result(mock_result)
            return {
                "success": True,
                "data": mock_result,
                "is_mock": True
            }
        
        try:
            client = self._get_client()
            runtime_option = RuntimeOptions()
            
            url_item = RecognizeActionAdvanceRequestURLList()
            url_item.urlobject = io.BytesIO(frame_data)
            
            request = RecognizeActionAdvanceRequest(
                type=1,
                urllist=[url_item]
            )
            
            response = client.recognize_action_advance(request, runtime_option)
            
            if response.body:
                result_data = json.loads(str(response.body))
                
                skeleton_data = []
                if "Data" in result_data and "SkeletonList" in result_data["Data"]:
                    skeleton_data = result_data["Data"]["SkeletonList"]
                
                metrics = self._calculate_metrics_from_skeleton(skeleton_data)
                
                score = self._calculate_posture_score(
                    metrics["head_angle"],
                    metrics["shoulder_score"],
                    metrics["back_score"],
                    metrics["eye_distance"]
                )
                
                status = self._determine_status(score)
                
                recommendation = self._get_recommendation(
                    status,
                    {
                        "head_angle": metrics["head_angle"],
                        "shoulder_balance": metrics["shoulder_balance"],
                        "back_curve": metrics["back_curve"],
                        "eye_distance": metrics["eye_distance"],
                        "fatigue_level": metrics["fatigue_level"]
                    }
                )
                
                result = {
                    "status": status,
                    "score": score,
                    "head_angle": metrics["head_angle"],
                    "shoulder_balance": metrics["shoulder_balance"],
                    "back_curve": metrics["back_curve"],
                    "eye_distance": metrics["eye_distance"],
                    "fatigue_level": metrics["fatigue_level"],
                    "recommendation": recommendation
                }
                
                session.add_detection_result(result)
                
                return {
                    "success": True,
                    "data": result,
                    "is_mock": False
                }
            else:
                mock_result = self._generate_mock_result()
                session.add_detection_result(mock_result)
                return {
                    "success": True,
                    "data": mock_result,
                    "is_mock": True
                }
                
        except Exception as e:
            print(f"视频帧处理错误：{e}")
            mock_result = self._generate_mock_result()
            session.add_detection_result(mock_result)
            return {
                "success": True,
                "data": mock_result,
                "is_mock": True,
                "error": str(e)
            }
    
    def _generate_mock_result(self) -> Dict[str, Any]:
        import random
        
        status = "good"
        head_angle = random.uniform(0, 8)
        shoulder_score = random.uniform(90, 100)
        back_score = random.uniform(90, 100)
        eye_distance = random.uniform(40, 50)
        fatigue_level = 0
        
        rand = random.random()
        if rand > 0.9:
            status = "danger"
            head_angle = random.uniform(25, 40)
            shoulder_score = random.uniform(30, 50)
            back_score = random.uniform(30, 50)
            eye_distance = random.uniform(20, 30)
            fatigue_level = random.randint(1, 3)
        elif rand > 0.7:
            status = "warning"
            head_angle = random.uniform(10, 20)
            shoulder_score = random.uniform(60, 80)
            back_score = random.uniform(60, 80)
            eye_distance = random.uniform(30, 40)
            fatigue_level = random.randint(0, 2)
        
        score = self._calculate_posture_score(
            head_angle, shoulder_score, back_score, eye_distance
        )
        
        shoulder_balance = "良好" if shoulder_score >= 90 else ("需注意" if shoulder_score >= 70 else "不平衡")
        back_curve = "正常" if back_score >= 90 else ("轻微弯曲" if back_score >= 70 else "过度弯曲")
        
        recommendation = self._get_recommendation(
            status,
            {
                "head_angle": head_angle,
                "shoulder_balance": shoulder_balance,
                "back_curve": back_curve,
                "eye_distance": eye_distance,
                "fatigue_level": fatigue_level
            }
        )
        
        return {
            "status": status,
            "score": score,
            "head_angle": round(head_angle, 1),
            "shoulder_balance": shoulder_balance,
            "back_curve": back_curve,
            "eye_distance": round(eye_distance, 1),
            "fatigue_level": fatigue_level,
            "recommendation": recommendation
        }


_video_stream_service = None


def get_video_stream_service() -> VideoStreamPostureService:
    global _video_stream_service
    if _video_stream_service is None:
        _video_stream_service = VideoStreamPostureService()
    return _video_stream_service
