from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
import base64

from src.storage.database.mysql_db import get_session
from src.models.user import User
from src.api.auth import get_current_user
from src.services import get_deepseek_service, get_photo_search_service, get_aliyun_ocr_service

router = APIRouter()

class OCRAnalyzeRequest(BaseModel):
    question_text: str
    subject: Optional[str] = None
    image_data: Optional[str] = None

@router.post("/recognize")
async def ocr_recognize(
    file: UploadFile = File(None),
    image_data: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    if not file and not image_data and not image_url:
        raise HTTPException(status_code=400, detail="Either file, image_data or image_url is required")
    
    ocr_service = get_aliyun_ocr_service()
    
    image_bytes = None
    if file:
        image_bytes = await file.read()
    elif image_data:
        try:
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image_data: {str(e)}")
    
    ocr_result = ocr_service.recognize_text(image_data=image_bytes, image_url=image_url)
    
    if "error" in ocr_result:
        return {
            "success": False,
            "error": ocr_result["error"],
            "data": ocr_result
        }
    
    return {
        "success": True,
        "data": ocr_result
    }

@router.post("/analyze")
async def analyze_question(
    request: OCRAnalyzeRequest,
    current_user: User = Depends(get_current_user)
):
    ai_service = get_deepseek_service()
    
    analysis_result = ai_service.analyze_question(request.question_text, request.subject)
    
    return {
        "success": True,
        "data": analysis_result
    }

@router.post("/photo-search")
async def photo_search(
    file: UploadFile = File(None),
    image_data: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    if not file and not image_data and not image_url:
        raise HTTPException(status_code=400, detail="Either file, image_data or image_url is required")
    
    ocr_service = get_aliyun_ocr_service()
    ai_service = get_photo_search_service()
    
    image_bytes = None
    if file:
        image_bytes = await file.read()
    elif image_data:
        try:
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image_data: {str(e)}")
    
    ocr_result = ocr_service.recognize_text(image_data=image_bytes, image_url=image_url)
    
    if "error" in ocr_result:
        return {
            "success": False,
            "error": ocr_result["error"],
            "data": ocr_result
        }
    
    ocr_text = ocr_result.get("text", "") or ocr_result.get("content", "") or str(ocr_result)
    
    analysis_prompt = f"""请分析以下题目，给出详细的讲解和思路引导：

{ocr_text}

请按照以下格式回答：
1. 【题目分析】简要说明题目考察的知识点
2. 【解题思路】分步骤引导学生思考，不要直接给出答案
3. 【知识点讲解】解释相关的知识点和概念
4. 【鼓励提示】给出鼓励性的话语"""
    
    ai_response = ai_service.chat(analysis_prompt, [])
    
    return {
        "success": True,
        "data": {
            "ocr_result": ocr_result,
            "ocr_text": ocr_text,
            "ai_analysis": ai_response
        }
    }
