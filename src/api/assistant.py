from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from src.storage.database.mysql_db import get_session
from src.models.health import AIConversation
from src.models.user import User
from src.api.auth import get_current_user
from src.services import get_deepseek_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

@router.get("/history")
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    query = db.query(AIConversation).filter(AIConversation.user_id == current_user.id)
    if session_id:
        query = query.filter(AIConversation.session_id == session_id)
    
    conversations = query.order_by(AIConversation.created_at.desc()).limit(limit).all()
    return {"success": True, "data": [c.to_dict() for c in reversed(conversations)]}

@router.post("/chat")
async def chat_with_assistant(
    chat: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    session_id = chat.session_id or str(uuid.uuid4())
    
    ai_service = get_deepseek_service()
    
    conversation_history = []
    if session_id:
        previous_conversations = db.query(AIConversation).filter(
            AIConversation.user_id == current_user.id,
            AIConversation.session_id == session_id
        ).order_by(AIConversation.created_at).all()
        
        for conv in previous_conversations:
            conversation_history.append({"role": "user", "content": conv.message})
            conversation_history.append({"role": "assistant", "content": conv.response})
    
    ai_response = ai_service.chat(chat.message, conversation_history)
    
    new_conversation = AIConversation(
        user_id=current_user.id,
        session_id=session_id,
        message=chat.message,
        response=ai_response,
        message_type="text"
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    
    return {
        "success": True,
        "data": {
            "message": ai_response,
            "session_id": session_id,
            "conversation_id": new_conversation.id
        }
    }

@router.get("/sessions")
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    sessions = db.query(
        AIConversation.session_id,
        db.func.max(AIConversation.created_at).label('last_message_time'),
        db.func.count(AIConversation.id).label('message_count')
    ).filter(
        AIConversation.user_id == current_user.id,
        AIConversation.session_id.isnot(None)
    ).group_by(
        AIConversation.session_id
    ).order_by(
        db.func.max(AIConversation.created_at).desc()
    ).all()
    
    session_list = []
    for session in sessions:
        session_list.append({
            "session_id": session.session_id,
            "last_message_time": session.last_message_time.isoformat() if session.last_message_time else None,
            "message_count": session.message_count
        })
    
    return {"success": True, "data": session_list}
