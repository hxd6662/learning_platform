from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from src.storage.database.mysql_db import get_session
from src.models.learning import LearningStat, LearningGoal
from src.models.user import User
from src.api.auth import get_current_user

router = APIRouter()

class LearningStatCreate(BaseModel):
    study_minutes: int
    questions_attempted: int = 0
    questions_correct: int = 0

class LearningGoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None

class LearningGoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    is_completed: Optional[bool] = None
    progress: Optional[int] = None

@router.get("/stats/{user_id}")
async def get_learning_stats(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    query = db.query(LearningStat).filter(LearningStat.user_id == user_id)
    if start_date:
        query = query.filter(LearningStat.study_date >= start_date)
    if end_date:
        query = query.filter(LearningStat.study_date <= end_date)
    
    stats = query.order_by(LearningStat.study_date.desc()).all()
    
    total_minutes = sum(s.study_minutes for s in stats)
    total_questions = sum(s.questions_attempted for s in stats)
    total_correct = sum(s.questions_correct for s in stats)
    
    first_date = db.query(func.min(LearningStat.study_date)).filter(
        LearningStat.user_id == user_id
    ).scalar()
    
    consecutive_days = 0
    if first_date:
        today = date.today()
        current_date = today
        while True:
            stat = db.query(LearningStat).filter(
                and_(
                    LearningStat.user_id == user_id,
                    LearningStat.study_date == current_date
                )
            ).first()
            if stat:
                consecutive_days += 1
                current_date = current_date.replace(day=current_date.day - 1)
            else:
                break
    
    return {
        "success": True,
        "data": {
            "stats": [s.to_dict() for s in stats],
            "totalStudyMinutes": total_minutes,
            "totalQuestions": total_questions,
            "consecutiveDays": consecutive_days,
            "accuracy": round(total_correct / total_questions * 100, 1) if total_questions > 0 else 0
        }
    }

@router.post("/stats")
async def create_learning_stat(
    stat: LearningStatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    today = date.today()
    existing_stat = db.query(LearningStat).filter(
        and_(
            LearningStat.user_id == current_user.id,
            LearningStat.study_date == today
        )
    ).first()
    
    if existing_stat:
        existing_stat.study_minutes += stat.study_minutes
        existing_stat.questions_attempted += stat.questions_attempted
        existing_stat.questions_correct += stat.questions_correct
    else:
        new_stat = LearningStat(
            user_id=current_user.id,
            study_date=today,
            study_minutes=stat.study_minutes,
            questions_attempted=stat.questions_attempted,
            questions_correct=stat.questions_correct
        )
        db.add(new_stat)
    
    db.commit()
    return {"success": True, "message": "Learning stat recorded"}

@router.get("/goals")
async def get_learning_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id
    ).order_by(LearningGoal.created_at.desc()).all()
    return {"success": True, "data": [g.to_dict() for g in goals]}

@router.post("/goals")
async def create_learning_goal(
    goal: LearningGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    new_goal = LearningGoal(
        user_id=current_user.id,
        title=goal.title,
        description=goal.description,
        target_date=goal.target_date
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return {"success": True, "data": new_goal.to_dict()}

@router.put("/goals/{goal_id}")
async def update_learning_goal(
    goal_id: int,
    goal_update: LearningGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    goal = db.query(LearningGoal).filter(
        and_(LearningGoal.id == goal_id, LearningGoal.user_id == current_user.id)
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    update_data = goal_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    return {"success": True, "data": goal.to_dict()}

@router.delete("/goals/{goal_id}")
async def delete_learning_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    goal = db.query(LearningGoal).filter(
        and_(LearningGoal.id == goal_id, LearningGoal.user_id == current_user.id)
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    return {"success": True, "message": "Goal deleted"}

@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_session)
):
    current_user_id = 1
    today = date.today()
    
    today_stat = db.query(LearningStat).filter(
        and_(
            LearningStat.user_id == current_user_id,
            LearningStat.study_date == today
        )
    ).first()
    
    study_time = today_stat.study_minutes if today_stat else 0
    completed_questions = today_stat.questions_correct if today_stat else 0
    
    first_date = db.query(func.min(LearningStat.study_date)).filter(
        LearningStat.user_id == current_user_id
    ).scalar()
    
    streak_days = 0
    if first_date:
        current_date = today
        while True:
            stat = db.query(LearningStat).filter(
                and_(
                    LearningStat.user_id == current_user_id,
                    LearningStat.study_date == current_date
                )
            ).first()
            if stat:
                streak_days += 1
                current_date = current_date.replace(day=current_date.day - 1)
            else:
                break
    
    from src.models.question import WrongQuestion
    wrong_count = db.query(func.count(WrongQuestion.id)).filter(
        WrongQuestion.user_id == current_user_id
    ).scalar() or 0
    
    goal_count = db.query(func.count(LearningGoal.id)).filter(
        LearningGoal.user_id == current_user_id
    ).scalar() or 0
    
    return {
        "success": True,
        "study_time": study_time,
        "completed_questions": completed_questions,
        "streak_days": streak_days,
        "wrong_questions": wrong_count,
        "goals": goal_count
    }
