"""
主应用入口 - FastAPI应用初始化和配置
"""

import time
from contextlib import asynccontextmanager

from api.chat_router import chat_router
from common.result import ApiResult
from core.config import settings
from core.exceptions import setup_exception_handlers
from core.logger import get_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    log.info(
        "✅ 服务启动",
        extra={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "host": settings.host,
            "port": settings.port,
        },
    )

    # 打印注册的API接口
    print_api_routes(app)

    yield

    log.info("🛑 服务关闭")


def print_api_routes(app: FastAPI):
    """打印注册的API接口"""
    print("\n📡 注册的API接口:")
    print("=" * 60)

    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            methods = list(route.methods)
            # 过滤掉OPTIONS和HEAD方法
            methods = [m for m in methods if m not in ["OPTIONS", "HEAD"]]

            if methods:  # 只显示有HTTP方法的路由
                method_str = ", ".join(methods)
                print(f"  {method_str:<8} {route.path}")

                # 如果路由有描述，显示描述
                if hasattr(route, 'summary') and route.summary:
                    print(f"         📝 {route.summary}")
                elif hasattr(route, 'description') and route.description:
                    print(f"         📝 {route.description}")

    print("=" * 60)
    print(f"🌐 服务地址: http://{settings.host}:{settings.port}")
    print(f"📚 API文档: http://{settings.host}:{settings.port}/docs")
    print()


# ==================== APP 初始化 ====================
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise-level shop assistant chatbot with AI integration",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None,
    lifespan=lifespan
)

# ==================== 中间件配置 ====================
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 异常处理 ====================
setup_exception_handlers(app)

# ==================== 路由注册 ====================
app.include_router(chat_router, prefix=settings.api_prefix)


# ==================== 健康检查 ====================
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return ApiResult.success(
        data={
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.app_version,
            "environment": settings.environment
        },
        message="服务正常"
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.is_development else None
    }


# ==================== 启动配置 ====================
if __name__ == "__main__":
    import uvicorn

    log.info("🚀 启动服务器", extra={
        "host": settings.host,
        "port": settings.port,
        "debug": settings.debug,
        "environment": settings.environment
    })

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        access_log=True,
        reload=False,
        use_colors=True
    )
