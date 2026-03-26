"""LLM client wrapper for better error handling and retry logic"""

import asyncio
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from core.logger import get_logger
from core.exceptions import AIModelError, ExternalServiceError
from .config import llm_config

log = get_logger(__name__)


class LLMClient:
    """Enhanced LLM client with error handling and retry logic"""
    
    def __init__(self):
        self.client = None
        self._initialized = False
    
    def _ensure_initialized(self):
        """延迟初始化客户端"""
        if not self._initialized:
            if not llm_config.is_configured:
                raise AIModelError("LLM is not properly configured")
            
            self.client = ChatOpenAI(
                base_url=llm_config.base_url,
                api_key=llm_config.api_key,
                model=llm_config.model_id,
                temperature=llm_config.temperature,
                max_tokens=llm_config.max_tokens,
                timeout=llm_config.timeout,
            )
            self._initialized = True
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> str:
        """
        Generate response from LLM with retry logic
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        
        Returns:
            Generated response text
        
        Raises:
            AIModelError: If all retry attempts fail
        """
        self._ensure_initialized()
        
        for attempt in range(max_retries):
            try:
                # Convert message dicts to langchain message objects
                langchain_messages = []
                for msg in messages:
                    if msg["role"] == "system":
                        langchain_messages.append(SystemMessage(content=msg["content"]))
                    elif msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        langchain_messages.append(AIMessage(content=msg["content"]))
                
                response = await self.client.ainvoke(langchain_messages)
                return response.content
                
            except Exception as e:
                log.warning(
                    f"LLM request failed (attempt {attempt + 1}/{max_retries}): {e}",
                    extra={
                        "attempt": attempt + 1,
                        "max_retries": max_retries,
                        "error": str(e)
                    }
                )
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise AIModelError(f"Failed to generate response after {max_retries} attempts: {e}")
    
    async def health_check(self) -> bool:
        """Check if LLM service is healthy"""
        try:
            self._ensure_initialized()
            test_messages = [{"role": "user", "content": "Hello"}]
            await self.generate_response(test_messages, max_retries=1)
            return True
        except Exception as e:
            log.error(f"LLM health check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_id": llm_config.model_id,
            "base_url": llm_config.base_url,
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "timeout": llm_config.timeout,
            "configured": llm_config.is_configured
        }


# Global LLM client instance (延迟初始化)
llm_client = LLMClient()
