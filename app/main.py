from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.global_config import Config
from app.core.lifespan import lifespan
from app.api import chat_router

# 创建 FastAPI 应用实例
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version=Config.APP_VERSION,
    lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)
