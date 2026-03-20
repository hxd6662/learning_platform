from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
import random
import base64

from src.storage.database.mysql_db import get_session
from src.models.health import HealthRecord
from src.models.user import User
from src.api.auth import get_current_user
from src.services.posture_service import get_aliyun_posture_service
from src.services.video_posture_service import get_video_stream_service

router = APIRouter()

monitoring_sessions: Dict[int, Dict[str, Any]] = {}
posture_history: Dict[int, List[Dict[str, Any]]] = {}

class HealthRecordCreate(BaseModel):
    record_time: Optional[datetime] = None
    posture_score: Optional[float] = None
    fatigue_level: Optional[int] = None
    eye_strain: Optional[int] = None
    head_pose: Optional[str] = None
    notes: Optional[str] = None

@router.get("/records")
async def get_health_records(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    query = db.query(HealthRecord).filter(HealthRecord.user_id == current_user.id)
    
    if start_date:
        query = query.filter(HealthRecord.record_time >= start_date)
    if end_date:
        query = query.filter(HealthRecord.record_time <= end_date)
    
    records = query.order_by(HealthRecord.record_time.desc()).limit(limit).all()
    return {"success": True, "data": [r.to_dict() for r in records]}

@router.post("/records")
async def create_health_record(
    record: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    new_record = HealthRecord(
        user_id=current_user.id,
        record_time=record.record_time or datetime.utcnow(),
        posture_score=record.posture_score,
        fatigue_level=record.fatigue_level,
        eye_strain=record.eye_strain,
        head_pose=record.head_pose,
        notes=record.notes
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"success": True, "data": new_record.to_dict()}

@router.get("/report")
async def get_health_report(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    records = db.query(HealthRecord).filter(
        and_(
            HealthRecord.user_id == current_user.id,
            HealthRecord.record_time >= start_date,
            HealthRecord.record_time <= end_date
        )
    ).all()
    
    avg_posture = None
    avg_fatigue = None
    avg_eye_strain = None
    bad_posture_count = 0
    high_fatigue_count = 0
    
    if records:
        posture_scores = [r.posture_score for r in records if r.posture_score is not None]
        fatigue_levels = [r.fatigue_level for r in records if r.fatigue_level is not None]
        eye_strains = [r.eye_strain for r in records if r.eye_strain is not None]
        
        if posture_scores:
            avg_posture = sum(posture_scores) / len(posture_scores)
            bad_posture_count = len([s for s in posture_scores if s < 60])
        
        if fatigue_levels:
            avg_fatigue = sum(fatigue_levels) / len(fatigue_levels)
            high_fatigue_count = len([f for f in fatigue_levels if f >= 3])
        
        if eye_strains:
            avg_eye_strain = sum(eye_strains) / len(eye_strains)
    
    recommendations = []
    if avg_posture and avg_posture < 70:
        recommendations.append("建议注意坐姿，每30分钟休息一下")
    if avg_fatigue and avg_fatigue >= 3:
        recommendations.append("疲劳程度较高，建议增加休息时间")
    if high_fatigue_count > len(records) * 0.3:
        recommendations.append("高频疲劳状态，建议调整学习节奏")
    
    return {
        "success": True,
        "data": {
            "period_days": days,
            "total_records": len(records),
            "average_posture_score": round(avg_posture, 1) if avg_posture else None,
            "average_fatigue_level": round(avg_fatigue, 1) if avg_fatigue else None,
            "average_eye_strain": round(avg_eye_strain, 1) if avg_eye_strain else None,
            "bad_posture_count": bad_posture_count,
            "high_fatigue_count": high_fatigue_count,
            "recommendations": recommendations
        }
    }

@router.get("/stats")
async def get_health_stats(
    db: Session = Depends(get_session)
):
    current_user_id = 1
    today = datetime.utcnow().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    records = db.query(HealthRecord).filter(
        and_(
            HealthRecord.user_id == current_user_id,
            HealthRecord.record_time >= start_of_day,
            HealthRecord.record_time <= end_of_day
        )
    ).all()
    
    good_posture_time = 0
    bad_posture_count = 0
    history = []
    
    for record in records:
        if record.posture_score:
            if record.posture_score >= 70:
                good_posture_time += 5
            else:
                bad_posture_count += 1
        
        status = "good"
        desc = "坐姿良好"
        if record.posture_score and record.posture_score < 60:
            status = "danger"
            desc = "需纠正"
        elif record.posture_score and record.posture_score < 70:
            status = "warning"
            desc = "需注意"
        
        history.append({
            "time": record.record_time.strftime("%H:%M"),
            "status": status,
            "desc": desc
        })
    
    history = history[-10:]
    history.reverse()
    
    return {
        "success": True,
        "good_posture_time": good_posture_time,
        "bad_posture_count": bad_posture_count,
        "history": history
    }

@router.get("/realtime")
async def get_realtime_data():
    current_user_id = 1
    session = monitoring_sessions.get(current_user_id)
    
    if not session or not session.get("is_monitoring"):
        return {
            "success": True,
            "head_angle": 0,
            "shoulder_balance": "良好",
            "back_curve": "正常",
            "eye_distance": 45,
            "status": "good"
        }
    
    random_val = random.random()
    status = "good"
    head_angle = random.randint(0, 8)
    shoulder_balance = "良好"
    back_curve = "正常"
    eye_distance = random.randint(40, 50)
    
    if random_val > 0.9:
        status = "danger"
        head_angle = random.randint(25, 40)
        shoulder_balance = "不平衡"
        back_curve = "过度弯曲"
        eye_distance = random.randint(20, 30)
    elif random_val > 0.7:
        status = "warning"
        head_angle = random.randint(10, 20)
        shoulder_balance = "需注意"
        back_curve = "轻微弯曲"
        eye_distance = random.randint(30, 40)
    
    return {
        "success": True,
        "head_angle": head_angle,
        "shoulder_balance": shoulder_balance,
        "back_curve": back_curve,
        "eye_distance": eye_distance,
        "status": status
    }

@router.post("/monitor/start")
async def start_monitoring(
    db: Session = Depends(get_session)
):
    current_user_id = 1
    monitoring_sessions[current_user_id] = {
        "is_monitoring": True,
        "start_time": datetime.utcnow()
    }
    
    return {
        "success": True,
        "message": "监测已开始"
    }

@router.post("/monitor/stop")
async def stop_monitoring(
    db: Session = Depends(get_session)
):
    current_user_id = 1
    session = monitoring_sessions.get(current_user_id)
    if session:
        session["is_monitoring"] = False
        session["end_time"] = datetime.utcnow()
    
    return {
        "success": True,
        "message": "监测已停止"
    }


class PostureDetectRequest(BaseModel):
    images: List[str]
    image_type: str = "base64"


class PostureDetectURLsRequest(BaseModel):
    image_urls: List[str]


@router.post("/posture/detect")
async def detect_posture(
    request: PostureDetectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    posture_service = get_aliyun_posture_service()
    
    result = await posture_service.detect_posture_from_base64(request.images)
    
    user_id = current_user.id
    if user_id not in posture_history:
        posture_history[user_id] = []
    
    history_entry = {
        "time": datetime.utcnow().strftime("%H:%M"),
        "status": result.status,
        "desc": "坐姿良好" if result.status == "good" else ("需注意" if result.status == "warning" else "需纠正"),
        "score": result.score,
        "head_angle": result.head_angle,
        "shoulder_balance": result.shoulder_balance,
        "back_curve": result.back_curve,
        "eye_distance": result.eye_distance
    }
    posture_history[user_id].append(history_entry)
    posture_history[user_id] = posture_history[user_id][-20:]
    
    new_record = HealthRecord(
        user_id=user_id,
        record_time=datetime.utcnow(),
        posture_score=result.score,
        head_pose=f"head_angle:{result.head_angle}",
        notes=result.details.get("recommendation", "")
    )
    db.add(new_record)
    db.commit()
    
    return {
        "success": True,
        "data": result.to_dict()
    }


@router.post("/posture/detect/urls")
async def detect_posture_from_urls(
    request: PostureDetectURLsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    posture_service = get_aliyun_posture_service()
    
    result = await posture_service.detect_posture_from_urls(request.image_urls)
    
    user_id = current_user.id
    if user_id not in posture_history:
        posture_history[user_id] = []
    
    history_entry = {
        "time": datetime.utcnow().strftime("%H:%M"),
        "status": result.status,
        "desc": "坐姿良好" if result.status == "good" else ("需注意" if result.status == "warning" else "需纠正"),
        "score": result.score,
        "head_angle": result.head_angle,
        "shoulder_balance": result.shoulder_balance,
        "back_curve": result.back_curve,
        "eye_distance": result.eye_distance
    }
    posture_history[user_id].append(history_entry)
    posture_history[user_id] = posture_history[user_id][-20:]
    
    new_record = HealthRecord(
        user_id=user_id,
        record_time=datetime.utcnow(),
        posture_score=result.score,
        head_pose=f"head_angle:{result.head_angle}",
        notes=result.details.get("recommendation", "")
    )
    db.add(new_record)
    db.commit()
    
    return {
        "success": True,
        "data": result.to_dict()
    }


@router.post("/posture/detect/upload")
async def detect_posture_upload(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="需要至少上传2张图片进行坐姿检测")
    
    images = []
    for file in files[:4]:
        content = await file.read()
        images.append(content)
    
    posture_service = get_aliyun_posture_service()
    result = await posture_service.detect_posture_from_images(images)
    
    user_id = current_user.id
    if user_id not in posture_history:
        posture_history[user_id] = []
    
    history_entry = {
        "time": datetime.utcnow().strftime("%H:%M"),
        "status": result.status,
        "desc": "坐姿良好" if result.status == "good" else ("需注意" if result.status == "warning" else "需纠正"),
        "score": result.score,
        "head_angle": result.head_angle,
        "shoulder_balance": result.shoulder_balance,
        "back_curve": result.back_curve,
        "eye_distance": result.eye_distance
    }
    posture_history[user_id].append(history_entry)
    posture_history[user_id] = posture_history[user_id][-20:]
    
    new_record = HealthRecord(
        user_id=user_id,
        record_time=datetime.utcnow(),
        posture_score=result.score,
        head_pose=f"head_angle:{result.head_angle}",
        notes=result.details.get("recommendation", "")
    )
    db.add(new_record)
    db.commit()
    
    return {
        "success": True,
        "data": result.to_dict()
    }


@router.get("/posture/history")
async def get_posture_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    history = posture_history.get(user_id, [])
    
    return {
        "success": True,
        "data": history[-limit:]
    }


@router.get("/posture/stats")
async def get_posture_stats(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    records = db.query(HealthRecord).filter(
        and_(
            HealthRecord.user_id == current_user.id,
            HealthRecord.record_time >= start_date,
            HealthRecord.record_time <= end_date,
            HealthRecord.posture_score.isnot(None)
        )
    ).all()
    
    if not records:
        return {
            "success": True,
            "data": {
                "total_detections": 0,
                "average_score": None,
                "good_posture_count": 0,
                "warning_posture_count": 0,
                "bad_posture_count": 0,
                "improvement_trend": "stable"
            }
        }
    
    scores = [r.posture_score for r in records if r.posture_score is not None]
    
    good_count = len([s for s in scores if s >= 70])
    warning_count = len([s for s in scores if 50 <= s < 70])
    bad_count = len([s for s in scores if s < 50])
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    if len(scores) >= 2:
        recent_avg = sum(scores[-5:]) / len(scores[-5:]) if len(scores) >= 5 else sum(scores[-2:]) / 2
        older_avg = sum(scores[:5]) / len(scores[:5]) if len(scores) > 5 else scores[0]
        
        if recent_avg > older_avg + 5:
            trend = "improving"
        elif recent_avg < older_avg - 5:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    return {
        "success": True,
        "data": {
            "total_detections": len(records),
            "average_score": round(avg_score, 1),
            "good_posture_count": good_count,
            "warning_posture_count": warning_count,
            "bad_posture_count": bad_count,
            "improvement_trend": trend,
            "period_days": days
        }
    }


@router.get("/realtime/detect")
async def get_realtime_detection(
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    session = monitoring_sessions.get(user_id)
    
    if not session or not session.get("is_monitoring"):
        return {
            "success": True,
            "head_angle": 0,
            "shoulder_balance": "良好",
            "back_curve": "正常",
            "eye_distance": 45,
            "status": "good",
            "score": 100,
            "recommendation": "请开始监测以获取实时坐姿数据"
        }
    
    posture_service = get_aliyun_posture_service()
    mock_result = posture_service._get_mock_result()
    
    return {
        "success": True,
        "head_angle": mock_result.head_angle,
        "shoulder_balance": mock_result.shoulder_balance,
        "back_curve": mock_result.back_curve,
        "eye_distance": mock_result.eye_distance,
        "status": mock_result.status,
        "score": mock_result.score,
        "recommendation": mock_result.details.get("recommendation", "")
    }


@router.post("/video/start")
async def start_video_monitoring(
    current_user: User = Depends(get_current_user)
):
    video_service = get_video_stream_service()
    video_service.start_session(current_user.id)
    
    return {
        "success": True,
        "message": "视频流监测已启动"
    }


@router.post("/video/stop")
async def stop_video_monitoring(
    current_user: User = Depends(get_current_user)
):
    video_service = get_video_stream_service()
    video_service.stop_session(current_user.id)
    
    stats = video_service.get_session_stats(current_user.id)
    
    return {
        "success": True,
        "message": "视频流监测已停止",
        "statistics": stats.get("statistics", {})
    }


@router.post("/video/frame")
async def process_video_frame(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    video_service = get_video_stream_service()
    
    frame_data = await file.read()
    
    result = await video_service.process_video_frame(current_user.id, frame_data)
    
    return result


@router.get("/video/stats")
async def get_video_monitoring_stats(
    current_user: User = Depends(get_current_user)
):
    video_service = get_video_stream_service()
    stats = video_service.get_session_stats(current_user.id)
    
    return {
        "success": True,
        "data": stats
    }


@router.get("/video/history")
async def get_video_monitoring_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    video_service = get_video_stream_service()
    session = video_service.get_or_create_session(current_user.id)
    
    history = list(session.detection_results)[-limit:]
    
    return {
        "success": True,
        "data": history
    }
