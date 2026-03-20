from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.storage.database.mysql_db import get_session
from src.models.question import LearningResource

router = APIRouter()

class LearningResourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    resource_type: str
    content_url: Optional[str] = None
    content: Optional[str] = None
    knowledge_points: Optional[List[str]] = None
    subject: Optional[str] = None
    difficulty: str = "medium"
    tags: Optional[List[str]] = None

@router.get("/")
async def get_resources(
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

@router.get("/{resource_id}")
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_session)
):
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.view_count += 1
    db.commit()
    db.refresh(resource)
    
    return {"success": True, "data": resource.to_dict()}

@router.post("/")
async def create_resource(
    resource: LearningResourceCreate,
    db: Session = Depends(get_session)
):
    new_resource = LearningResource(
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        content_url=resource.content_url,
        content=resource.content,
        knowledge_points=resource.knowledge_points,
        subject=resource.subject,
        difficulty=resource.difficulty,
        tags=resource.tags
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return {"success": True, "data": new_resource.to_dict()}
