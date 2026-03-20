from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from src.storage.database.mysql_db import Base

class LearningStat(Base):
    __tablename__ = "learning_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    study_date = Column(Date, nullable=False, index=True)
    study_minutes = Column(Integer, default=0, nullable=False)
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_correct = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="learning_stats")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "study_date": self.study_date.isoformat() if self.study_date else None,
            "study_minutes": self.study_minutes,
            "questions_attempted": self.questions_attempted,
            "questions_correct": self.questions_correct,
            "accuracy": round(self.questions_correct / self.questions_attempted * 100, 1) if self.questions_attempted > 0 else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="learning_goals")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "is_completed": self.is_completed,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
