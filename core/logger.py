import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import settings


def setup_logging():
    """设置简单的日志配置"""
    # 创建日志目录
    log_path = Path(settings.log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 配置日志级别
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # 配置根日志记录器
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),  # 控制台输出
            RotatingFileHandler(
                settings.log_file_path,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )  # 文件输出
        ]
    )


def get_logger(name: str = None) -> logging.Logger:
    """获取日志记录器"""
    if name is None:
        name = "app"
    return logging.getLogger(name)


# 初始化日志配置
setup_logging()

# 默认日志记录器
log = get_logger("shop_assistant")