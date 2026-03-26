from typing import List, Optional
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Settings
    app_name: str = Field(default="shop assistant chatbot", description="Application name")
    app_version: str = Field(default="v1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="production", description="Environment name")
    
    # Server Settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8800, description="Server port")
    api_prefix: str = Field(default="/api", description="API prefix")
    
    # CORS Settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed CORS methods"
    )
    allowed_headers: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )
    
    # AI Model Settings
    base_url: str = Field(default="http://183.222.230.18:8000/v1", description="AI model base URL")
    api_key: str = Field(default="", description="AI model API key")
    model_id: str = Field(default="Qwen/Qwen3.5-35B-A3B", description="AI model ID")
    model_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Model temperature")
    model_max_tokens: int = Field(default=2048, ge=1, description="Model max tokens")
    model_timeout: int = Field(default=30, ge=1, description="Model timeout in seconds")
    
    # Logging Settings
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")
    log_file_path: str = Field(default="logs/app.log", description="Log file path")
    log_max_size: str = Field(default="10MB", description="Log max size")
    log_backup_count: int = Field(default=5, description="Log backup count")
    
    # External Services
    bing_search_api_key: Optional[str] = Field(default=None, description="Bing search API key")
    bing_search_endpoint: str = Field(
        default="https://api.bing.microsoft.com/v7.0/search",
        description="Bing search endpoint"
    )

    model_config = ConfigDict(
        env_file=[".env", ".env.local"],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
        
    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    @field_validator("environment", mode="before")
    @classmethod
    def validate_environment(cls, v):
        valid_envs = ["development", "testing", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v.lower()
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.environment == "testing"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
