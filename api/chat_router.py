"""
聊天API路由 - 处理聊天相关的HTTP请求
"""

import asyncio
import json

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
    image_url: str = Field(None, description="图片地址URL，用于冰柜检查等任务")


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

        # 智能体现在只返回字符串消息，直接使用
        response_message = result if isinstance(result, str) else str(result)

        # 检查智能体返回的消息中是否包含"需要拍照"标识
        front_calls = []

        # 检查消息中的拍照标识
        if "需要拍照" in response_message or "[需要拍照]" in response_message:
            front_calls.append("camera_call")
            log.info(f"检测到智能体返回的'需要拍照'标识")

        # 检查用户原始消息中是否明确提到拍照需求（作为备用检测）
        elif any(keyword in request.message for keyword in ["拍照", "图片", "照片", "上传图片"]):
            front_calls.append("camera_call")
            log.info(f"用户明确提到拍照需求")

        log.info(f"聊天请求处理成功，front_calls: {front_calls}")

        return ApiResult.success(
            data={
                "message": response_message,
                "front_calls": front_calls
            },
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
                iter(["缺少用户ID，请在请求头中提供user_id"]),
                media_type="text/event-stream"
            )

        if not session_id:
            error_data = ApiResult.bad_request(
                message="缺少会话ID，请在请求头中提供session_id",
                data={"error": "Missing session_id header"}
            )
            error_data["finished"] = True
            return StreamingResponse(
                iter(["缺少会话ID，请在请求头中提供session_id"]),
                media_type="text/event-stream"
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
    流式聊天响应生成器 - 标准SSE格式
    
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

        # 智能体现在只返回字符串消息，直接使用
        response_message = result if isinstance(result, str) else str(result)

        # 检查智能体返回的消息中是否包含"需要拍照"标识
        front_calls = []

        # 检查消息中的拍照标识
        if "需要拍照" in response_message or "[需要拍照]" in response_message:
            front_calls.append("camera_call")
            log.info(f"流式响应检测到智能体返回的'需要拍照'标识")

        # 检查用户原始消息中是否明确提到拍照需求（作为备用检测）
        elif any(keyword in request.message for keyword in ["拍照", "图片", "照片", "上传图片"]):
            front_calls.append("camera_call")
            log.info(f"流式响应检测到用户明确提到拍照需求")

        # 构建最终响应数据
        final_data = {
            "message": response_message,
            "front_calls": front_calls
        }

        # 标准SSE格式流式输出，保持与complete接口格式一致
        # 1. 发送开始事件 - 使用ApiResult格式
        start_data = ApiResult.success(
            data={"status": "started", "message": "开始处理请求"},
            message="处理开始"
        )
        yield f"event: start\n"
        yield f"data: {json.dumps(start_data, ensure_ascii=False)}\n\n"

        # 2. 逐字符流式输出消息内容
        for i, char in enumerate(response_message):
            # 发送字符片段 - 使用ApiResult格式
            chunk_data = ApiResult.success(
                data={
                    "type": "chunk",
                    "content": char,
                    "index": i,
                    "finished": False
                },
                message="正在处理"
            )
            yield f"event: chunk\n"
            yield f"data: {json.dumps(chunk_data, ensure_ascii=False)}\n\n"

            # 控制打字速度
            if i % 3 == 0:
                await asyncio.sleep(0.05)

        # 3. 发送完成事件，包含完整数据和front_calls - 使用ApiResult格式
        complete_data = ApiResult.success(
            data=final_data,
            message="处理成功"
        )
        yield f"event: complete\n"
        yield f"data: {json.dumps(complete_data, ensure_ascii=False)}\n\n"

        # 4. 发送结束事件 - 使用ApiResult格式
        end_data = ApiResult.success(
            data={"status": "finished", "message": "流式响应完成", "front_calls": front_calls},
            message="响应完成"
        )
        yield f"event: end\n"
        yield f"data: {json.dumps(end_data, ensure_ascii=False)}\n\n"

        log.info(f"流式聊天请求处理成功，front_calls: {front_calls}")

    except Exception as e:
        log.error(f"流式响应生成失败: {e}")
        # 发送错误事件 - 使用ApiResult格式
        error_data = ApiResult.server_error(
            message="流式响应失败，请稍后重试",
            data={"error": str(e)}
        )
        yield f"event: error\n"
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
