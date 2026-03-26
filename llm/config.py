"""LLM configuration and settings"""

from typing import Optional, Dict, Any
from pydantic import Field

from core.config import settings


class LLMConfig:
    """LLM configuration class"""
    
    def __init__(self):
        self.base_url = settings.base_url
        self.api_key = settings.api_key
        self.model_id = settings.model_id
        self.temperature = settings.model_temperature
        self.max_tokens = settings.model_max_tokens
        self.timeout = settings.model_timeout
    
    @property
    def is_configured(self) -> bool:
        """Check if LLM is properly configured"""
        return bool(self.api_key and self.base_url)
    
    @property
    def model_params(self) -> Dict[str, Any]:
        """Get model parameters as dictionary"""
        return {
            "base_url": self.base_url,
            "model": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }
    
    def update_config(self, **kwargs):
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# Global LLM configuration instance
llm_config = LLMConfig()
