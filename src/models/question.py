from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.storage.database.mysql_db import Base

class WrongQuestion(Base):
    __tablename__ = "wrong_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_image = Column(String(500), nullable=True)
    correct_answer = Column(Text, nullable=True)
    user_answer = Column(Text, nullable=True)
    knowledge_point = Column(String(200), nullable=True)
    subject = Column(String(50), nullable=True, index=True)
    difficulty = Column(String(20), default="medium", nullable=False)
    analysis = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    review_count = Column(Integer, default=0, nullable=False)
    is_mastered = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="wrong_questions")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question_text": self.question_text,
            "question_image": self.question_image,
            "correct_answer": self.correct_answer,
            "user_answer": self.user_answer,
            "knowledge_point": self.knowledge_point,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "analysis": self.analysis,
            "tags": self.tags,
            "review_count": self.review_count,
            "is_mastered": bool(self.is_mastered),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False, index=True)
    content_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    knowledge_points = Column(JSON, nullable=True)
    subject = Column(String(50), nullable=True, index=True)
    difficulty = Column(String(20), default="medium", nullable=False)
    tags = Column(JSON, nullable=True)
    view_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "resource_type": self.resource_type,
            "content_url": self.content_url,
            "content": self.content,
            "knowledge_points": self.knowledge_points,
            "subject": self.subject,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
