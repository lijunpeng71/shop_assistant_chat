"""
路由模块 - API路由定义
"""

from app.api.chat_router import router as chat_router

# 模块化路由

__all__ = [
    "chat_router",
]

