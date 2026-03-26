"""LLM model configuration and initialization"""

from langchain_openai import ChatOpenAI

from core.config import settings

# Initialize the base chat model with configuration
chat_base_model = ChatOpenAI(
    base_url=settings.base_url,
    api_key=settings.api_key,
    model=settings.model_id,
    temperature=settings.model_temperature,
    max_tokens=settings.model_max_tokens,
    timeout=settings.model_timeout,
)
