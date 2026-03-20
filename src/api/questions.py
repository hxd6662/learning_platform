from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.storage.database.mysql_db import get_session
from src.models.question import WrongQuestion, LearningResource
from src.models.user import User
from src.api.auth import get_current_user

router = APIRouter()

class WrongQuestionCreate(BaseModel):
    question_text: str
    question_image: Optional[str] = None
    correct_answer: Optional[str] = None
    user_answer: Optional[str] = None
    knowledge_point: Optional[str] = None
    subject: Optional[str] = None
    difficulty: str = "medium"
    analysis: Optional[str] = None
    tags: Optional[List[str]] = None

class WrongQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    correct_answer: Optional[str] = None
    user_answer: Optional[str] = None
    knowledge_point: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    analysis: Optional[str] = None
    tags: Optional[List[str]] = None
    is_mastered: Optional[bool] = None

@router.get("/wrong")
async def get_wrong_questions(
    subject: Optional[str] = None,
    knowledge_point: Optional[str] = None,
    is_mastered: Optional[bool] = None,
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    query = db.query(WrongQuestion).filter(WrongQuestion.user_id == current_user.id)
    
    if subject:
        query = query.filter(WrongQuestion.subject == subject)
    if knowledge_point:
        query = query.filter(WrongQuestion.knowledge_point == knowledge_point)
    if is_mastered is not None:
        query = query.filter(WrongQuestion.is_mastered == (1 if is_mastered else 0))
    
    total = query.count()
    questions = query.order_by(WrongQuestion.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "success": True,
        "data": {
            "questions": [q.to_dict() for q in questions],
            "total": total,
            "page": page,
            "limit": limit
        }
    }

@router.get("/wrong/{question_id}")
async def get_wrong_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    question = db.query(WrongQuestion).filter(
        and_(WrongQuestion.id == question_id, WrongQuestion.user_id == current_user.id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"success": True, "data": question.to_dict()}

@router.post("/wrong")
async def create_wrong_question(
    question: WrongQuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    new_question = WrongQuestion(
        user_id=current_user.id,
        question_text=question.question_text,
        question_image=question.question_image,
        correct_answer=question.correct_answer,
        user_answer=question.user_answer,
        knowledge_point=question.knowledge_point,
        subject=question.subject,
        difficulty=question.difficulty,
        analysis=question.analysis,
        tags=question.tags
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return {"success": True, "data": new_question.to_dict()}

@router.put("/wrong/{question_id}")
async def update_wrong_question(
    question_id: int,
    question_update: WrongQuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    question = db.query(WrongQuestion).filter(
        and_(WrongQuestion.id == question_id, WrongQuestion.user_id == current_user.id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "is_mastered":
            setattr(question, field, 1 if value else 0)
        else:
            setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    return {"success": True, "data": question.to_dict()}

@router.post("/wrong/{question_id}/review")
async def review_wrong_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    question = db.query(WrongQuestion).filter(
        and_(WrongQuestion.id == question_id, WrongQuestion.user_id == current_user.id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.review_count += 1
    question.reviewed_at = datetime.utcnow()
    db.commit()
    db.refresh(question)
    return {"success": True, "data": question.to_dict()}

@router.delete("/wrong/{question_id}")
async def delete_wrong_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    question = db.query(WrongQuestion).filter(
        and_(WrongQuestion.id == question_id, WrongQuestion.user_id == current_user.id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()
    return {"success": True, "message": "Question deleted"}

@router.get("/resources")
async def get_learning_resources(
    subject: Optional[str] = None,
    resource_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_session)
):
    query = db.query(LearningResource)
    
    if subject:
        query = query.filter(LearningResource.subject == subject)
    if resource_type:
        query = query.filter(LearningResource.resource_type == resource_type)
    if difficulty:
        query = query.filter(LearningResource.difficulty == difficulty)
    if search:
        query = query.filter(
            or_(
                LearningResource.title.contains(search),
                LearningResource.description.contains(search)
            )
        )
    
    total = query.count()
    resources = query.order_by(LearningResource.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "success": True,
        "data": {
            "resources": [r.to_dict() for r in resources],
            "total": total,
            "page": page,
            "limit": limit
        }
    }
