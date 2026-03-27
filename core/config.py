"""
应用配置 - 简化配置管理
"""

import os
from typing import Optional


class Settings:
    """应用配置类 - 简化版本"""
    
    def __init__(self):
        # Application Settings
        self.app_name = os.getenv("APP_NAME", "shop assistant chatbot")
        self.app_version = os.getenv("APP_VERSION", "v1.0.0")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.environment = os.getenv("ENVIRONMENT", "development")

        # Server Settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8800"))
        self.api_prefix = os.getenv("API_PREFIX", "/api")

        # AI Model Settings
        self.base_url = os.getenv("BASE_URL", "http://183.222.230.18:8000/v1")
        self.api_key = os.getenv("API_KEY", "")
        self.model_id = os.getenv("MODEL_ID", "Qwen/Qwen3.5-35B-A3B")
        self.model_temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.model_max_tokens = int(os.getenv("MODEL_MAX_TOKENS", "2048"))
        self.model_timeout = int(os.getenv("MODEL_TIMEOUT", "30"))
        
        # Logging Settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = os.getenv("LOG_FORMAT", "json")
        self.log_file_path = os.getenv("LOG_FILE_PATH", "logs/app.log")
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"


# 全局配置实例
settings = Settings()
