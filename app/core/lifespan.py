"""
应用生命周期管理
优雅地处理数据库、Redis连接池等资源的初始化与释放
"""
import json
# 导入引发的报错在创建项目之后会自动消失
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from requests import Request
from starlette.routing import Route


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        """
        应用生命周期管理器
        处理资源的初始化和清理
        """
        # 启动时初始化
        logger.info("应用启动中...")

        # 启动时打印路由
        print("=" * 50)
        print("✅ FastAPI 启动成功，注册路由：")
        for route in app.routes:
            if isinstance(route, Route):
                if route.path in ["/docs", "/openapi.json", "/redoc"]:
                    continue
                print(f"[{','.join(route.methods)}] {route.path}")
        print("=" * 50)
        yield
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise
    finally:
        try:
            # 关闭时清理
            logger.info("应用关闭中...")
            logger.info("应用关闭完成")
        except Exception as e:
            logger.error(f"应用关闭时出错: {e}")




# ================ 请求日志中间件（打印地址+参数） ================
async def log_request_middleware(request: Request, call_next):
    """
    打印每次请求：地址、方法、参数
    """
    # 1. 请求基础信息
    method = request.method
    url = str(request.url)
    client_ip = request.client.host

    # 2. 查询参数 ?a=1&b=2
    query_params = dict(request.query_params)

    # 3. 路径参数 /user/{id}
    path_params = request.path_params

    # 4. Body 参数（JSON）
    body_params = {}
    if request.headers.get("content-type") == "application/json":
        try:
            body = await request.json()
            body_params = body if isinstance(body, dict) else str(body)
        except:
            body_params = "非JSON格式"

    # ———— 打印 ————
    print(f"\n📩 新请求 [{method}] {url}")
    print(f"    客户端IP: {client_ip}")
    if path_params:
        print(f"    路径参数: {path_params}")
    if query_params:
        print(f"    查询参数: {query_params}")
    if body_params:
        print(f"    请求体: {json.dumps(body_params, ensure_ascii=False, indent=2)}")

    # 执行请求
    response = await call_next(request)
    return response

# 后台定时任务示例
async def periodic_task() -> None:
    """后台定时任务示例"""
    import asyncio
    while True:
        try:
            # 执行定时任务
            logger.debug("执行后台定时任务...")
            await asyncio.sleep(60)  # 每60秒执行一次
        except asyncio.CancelledError:
            logger.info("后台任务已取消")
            break
        except Exception as e:
            logger.error(f"后台任务执行失败: {e}")
            await asyncio.sleep(60)
