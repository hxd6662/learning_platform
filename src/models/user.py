from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from src.storage.database.mysql_db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    nickname = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    learning_stats = relationship("LearningStat", back_populates="user", cascade="all, delete-orphan")
    wrong_questions = relationship("WrongQuestion", back_populates="user", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="user", cascade="all, delete-orphan")
    ai_conversations = relationship("AIConversation", back_populates="user", cascade="all, delete-orphan")
    learning_goals = relationship("LearningGoal", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
