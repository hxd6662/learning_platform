#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI智能学习助手 - Web后端服务

提供REST API接口，供Web前端调用Agent
"""

import os
import sys
import json
import asyncio
from typing import AsyncGenerator, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# 获取项目根目录并添加到Python路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 添加src目录到Python路径
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from agents.agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, "assets", "static")

# 创建FastAPI应用
app = FastAPI(
    title="AI智能学习助手API",
    description="青少年智能学习平台 - 后端服务",
    version="1.0.0"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局Agent实例
_agent = None
_agent_lock = asyncio.Lock()

# 请求模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    """聊天响应模型"""
    message: str
    conversation_id: str
    timestamp: str

async def get_agent():
    """获取Agent实例（单例模式）"""
    global _agent
    async with _agent_lock:
        if _agent is None:
            _agent = build_agent()
    return _agent

@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "AI智能学习助手API",
        "version": "1.0.0",
        "status": "running",
        "message": "请访问 /static/index.html 查看前端页面",
        "endpoints": {
            "chat": "/api/chat",
            "chat_stream": "/api/chat/stream",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    非流式聊天接口

    一次性返回完整的AI回复
    """
    try:
        agent = await get_agent()

        # 准备消息
        messages = [HumanMessage(content=request.message)]

        # 调用Agent
        response = await agent.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": request.conversation_id or "default"}}
        )

        # 提取回复内容
        ai_message = response["messages"][-1]
        if isinstance(ai_message.content, str):
            reply_text = ai_message.content
        elif isinstance(ai_message.content, list):
            # 处理多模态响应
            text_parts = []
            for item in ai_message.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            reply_text = " ".join(text_parts)
        else:
            reply_text = str(ai_message.content)

        return ChatResponse(
            message=reply_text,
            conversation_id=request.conversation_id or "default",
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求失败: {str(e)}")

async def generate_chat_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    流式聊天生成器

    为了可靠性，实际使用非流式invoke，然后在生成器中逐字返回
    这样既保持了接口的流式特性，又确保了稳定性
    """
    try:
        agent = await get_agent()

        # 准备消息
        messages = [HumanMessage(content=request.message)]

        # 调用Agent获取完整响应
        response = await agent.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": request.conversation_id or "default"}}
        )

        # 提取回复内容
        ai_message = response["messages"][-1]
        if isinstance(ai_message.content, str):
            reply_text = ai_message.content
        elif isinstance(ai_message.content, list):
            # 处理多模态响应
            text_parts = []
            for item in ai_message.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            reply_text = " ".join(text_parts)
        else:
            reply_text = str(ai_message.content)

        # 逐字发送（模拟流式效果）
        for char in reply_text:
            yield json.dumps({
                "type": "content",
                "content": char
            }, ensure_ascii=False) + "\n"
            # 添加小延迟模拟流式效果
            await asyncio.sleep(0.01)

        # 发送结束标记
        yield json.dumps({
            "type": "done",
            "conversation_id": request.conversation_id or "default"
        }, ensure_ascii=False) + "\n"

    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e)
        }, ensure_ascii=False) + "\n"

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    流式聊天接口

    逐块返回AI回复内容，提供更好的用户体验
    """
    return StreamingResponse(
        generate_chat_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    # 启动FastAPI服务器
    uvicorn.run(
        "web_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
