#!/usr/bin/env python3
"""
聊天相关路由
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from app.common.global_models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.config.logging_config import get_logger
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

router = APIRouter(prefix="/chat", tags=["聊天"])
logger = get_logger(__name__)

# 初始化服务
chat_service = ChatService()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口（启用记忆系统）
    """
    try:
        response = await chat_service.chat(request)
        return response
    except Exception as e:
        logger.error(f"聊天接口错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))