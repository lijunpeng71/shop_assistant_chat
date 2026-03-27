"""
聊天API路由 - 处理聊天相关的HTTP请求
"""

import asyncio
import json
from typing import Optional

from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from common.result import ApiResult
from core.logger import get_logger
from service.chat_service import ChatService

# 创建单例实例
chat_service = ChatService()
log = get_logger(__name__)

chat_router = APIRouter(prefix="/v1/chat")


class ChatRequest(BaseModel):
    """聊天请求模型"""

    message: str = Field(..., description="用户输入的消息", min_length=1, max_length=10000)
    image_url: Optional[str] = Field(None, description="图片地址URL，用于冰柜检查等任务")


@chat_router.post("/complete")
async def complete(
    request: ChatRequest,
    user_id: str = Header(None, description="用户ID"),
    session_id: str = Header(None, description="会话ID"),
):
    """
    聊天完成接口
    
    Args:
        request: 聊天请求
        user_id: 从header获取的用户ID
        session_id: 从header获取的会话ID
        
    Returns:
        统一格式的聊天响应
    """
    try:
        log.info(f"收到聊天请求: message={request.message[:50]}...")

        # 打印请求头信息用于调试
        log.info(f"请求头信息: user_id={user_id}, session_id={session_id}")
        
        # 验证必需的header参数
        if not user_id:
            return ApiResult.bad_request(
                message="缺少用户ID，请在请求头中提供user_id",
                data={"error": "Missing user_id header"}
            )
        
        if not session_id:
            return ApiResult.bad_request(
                message="缺少会话ID，请在请求头中提供session_id",
                data={"error": "Missing session_id header"}
            )
        
        # 调用聊天服务（使用单例实例）
        result = await chat_service.chat(
            message=request.message,
            user_id=user_id,
            session_id=session_id,
            image_url=request.image_url
        )

        # 构建响应数据
        response_data = {
            "type": result.get("type", "general"),
            "message": result.get("message", str(result.get("result", ""))),
            "data": result.get("data"),
            "suggestions": result.get("suggestions")
        }

        log.info(f"聊天请求处理成功: type={response_data['type']}")

        return ApiResult.success(
            data=response_data,
            message="处理成功"
        )

    except ValueError as e:
        log.error(f"请求参数错误: {e}")
        return ApiResult.bad_request(
            message=f"请求参数错误: {str(e)}",
            data={"error": str(e)}
        )
    except PermissionError as e:
        log.error(f"权限错误: {e}")
        return ApiResult.forbidden(
            message=f"权限不足: {str(e)}",
            data={"error": str(e)}
        )
    except Exception as e:
        log.error(f"聊天请求处理失败: {e}")
        return ApiResult.server_error(
            message="聊天处理失败，请稍后重试",
            data={"error": str(e)}
        )


@chat_router.post("/stream")
async def stream_complete(
        request: ChatRequest,
        user_id: str = Header(None, description="用户ID"),
        session_id: str = Header(None, description="会话ID")
):
    """
    流式聊天完成接口 - 实现打字机效果
    
    Args:
        request: 聊天请求
        user_id: 从header获取的用户ID
        session_id: 从header获取的会话ID
        
    Returns:
        流式响应，逐字符返回结果
    """
    try:
        log.info(f"收到流式聊天请求: message={request.message[:50]}...")

        # 打印请求头信息用于调试
        log.info(f"流式请求头信息: user_id={user_id}, session_id={session_id}")
        
        # 验证必需的header参数
        if not user_id:
            error_data = ApiResult.bad_request(
                message="缺少用户ID，请在请求头中提供user_id",
                data={"error": "Missing user_id header"}
            )
            error_data["finished"] = True
            return StreamingResponse(
                iter([f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"]),
                media_type="text/plain"
            )
        
        if not session_id:
            error_data = ApiResult.bad_request(
                message="缺少会话ID，请在请求头中提供session_id",
                data={"error": "Missing session_id header"}
            )
            error_data["finished"] = True
            return StreamingResponse(
                iter([f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"]),
                media_type="text/plain"
            )
        
        # 返回流式响应
        return StreamingResponse(
            stream_chat_response(request, user_id, session_id),
            media_type="text/event-stream"
        )

    except Exception as e:
        log.error(f"流式聊天请求处理失败: {e}")
        error_data = ApiResult.server_error(
            message="聊天处理失败，请稍后重试",
            data={"error": str(e)}
        )
        error_data["finished"] = True
        return StreamingResponse(
            iter([f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"]),
            media_type="text/event-stream"
        )


async def stream_chat_response(request: ChatRequest, user_id: str, session_id: str):
    """
    流式聊天响应生成器
    
    Args:
        request: 聊天请求
        user_id: 用户ID
        session_id: 会话ID
    """
    try:
        # 调用聊天服务获取完整响应
        result = await chat_service.chat(
            message=request.message,
            user_id=user_id,
            session_id=session_id,
            image_url=request.image_url
        )

        # 构建响应数据
        response_data = {
            "type": result.get("type", "general"),
            "message": result.get("message", str(result.get("result", ""))),
            "data": result.get("data"),
            "suggestions": result.get("suggestions")
        }

        # 使用ApiResult统一封装
        success_response = ApiResult.success(
            data=response_data,
            message="处理成功"
        )

        # 转换为JSON字符串
        response_json = json.dumps(success_response, ensure_ascii=False)
        
        # 逐字符流式输出（打字机效果）
        for i, char in enumerate(response_json):
            # 构建部分响应 - 避免嵌套data字段
            partial_content = response_json[:i+1]
            
            # 尝试解析部分JSON，如果失败则返回原始内容
            try:
                if i == len(response_json) - 1:
                    # 最后一个字符，完整解析
                    parsed_data = json.loads(partial_content)
                    partial_data = {
                        "code": parsed_data.get("code", 0),
                        "message": parsed_data.get("message", "处理成功"),
                        "response": parsed_data.get("data"),  # 使用response字段避免嵌套
                        "partial": False,
                        "finished": True
                    }
                else:
                    # 部分内容，返回原始字符串
                    partial_data = {
                        "code": 0,
                        "message": "正在处理...",
                        "partial_content": partial_content,
                        "partial": True,
                        "finished": False
                    }
            except json.JSONDecodeError:
                # JSON解析失败，返回原始内容
                partial_data = {
                    "code": 0,
                    "message": "正在处理...",
                    "partial_content": partial_content,
                    "partial": True,
                    "finished": False
                }
            
            # 发送部分数据
            yield f"data: {json.dumps(partial_data, ensure_ascii=False)}\n\n"
            
            # 控制打字速度（每2-3个字符暂停一下）
            if i % 3 == 0:
                await asyncio.sleep(0.05)  # 50ms延迟，模拟打字效果

        # 发送完成信号 - 使用ApiResult格式
        complete_data = ApiResult.success(
            data={"streaming_completed": True},
            message="流式响应完成"
        )
        complete_data["finished"] = True
        yield f"data: {json.dumps(complete_data, ensure_ascii=False)}\n\n"

        log.info(f"流式聊天请求处理成功: type={response_data['type']}")

    except Exception as e:
        log.error(f"流式响应生成失败: {e}")
        # 使用ApiResult统一错误格式
        error_data = ApiResult.server_error(
            message="流式响应失败，请稍后重试",
            data={"error": str(e)}
        )
        error_data["finished"] = True
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
