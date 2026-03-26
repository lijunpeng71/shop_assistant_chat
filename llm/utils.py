"""LLM utility functions"""

from typing import List, Dict, Any, Optional
import tiktoken

from core.logger import get_logger
from .config import llm_config

log = get_logger(__name__)


def count_tokens(text: str, model: Optional[str] = None) -> int:
    """
    Count tokens in text using tiktoken
    
    Args:
        text: Text to count tokens for
        model: Model name for tokenization (defaults to configured model)
    
    Returns:
        Number of tokens
    """
    try:
        model_name = model or llm_config.model_id
        
        # Use a default encoding if model is not recognized
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(text))
    except Exception as e:
        log.warning(f"Token counting failed: {e}")
        # Fallback to rough estimation (1 token ≈ 4 characters for English)
        return len(text) // 4


def truncate_text(text: str, max_tokens: int, model: Optional[str] = None) -> str:
    """
    Truncate text to fit within token limit
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens
        model: Model name for tokenization
    
    Returns:
        Truncated text
    """
    try:
        model_name = model or llm_config.model_id
        
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        tokens = encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        
        # Truncate tokens and decode back to text
        truncated_tokens = tokens[:max_tokens]
        return encoding.decode(truncated_tokens)
    except Exception as e:
        log.warning(f"Text truncation failed: {e}")
        # Fallback to character-based truncation
        max_chars = max_tokens * 4  # Rough estimation
        return text[:max_chars]


def format_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Format and validate messages for LLM
    
    Args:
        messages: List of message dictionaries
    
    Returns:
        Formatted and validated messages
    """
    formatted_messages = []
    
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValueError(f"Message {i} must be a dictionary")
        
        if "role" not in message or "content" not in message:
            raise ValueError(f"Message {i} must have 'role' and 'content' fields")
        
        role = message["role"]
        content = message["content"]
        
        if role not in ["system", "user", "assistant"]:
            raise ValueError(f"Message {i} has invalid role: {role}")
        
        if not isinstance(content, str):
            raise ValueError(f"Message {i} content must be a string")
        
        formatted_messages.append({
            "role": role,
            "content": content.strip()
        })
    
    return formatted_messages


def estimate_cost(tokens: int, model: Optional[str] = None) -> Dict[str, float]:
    """
    Estimate cost for token usage
    
    Args:
        tokens: Number of tokens used
        model: Model name for pricing
    
    Returns:
        Dictionary with cost estimates
    """
    # This is a simplified cost estimation
    # In practice, you'd want to use actual pricing from the model provider
    model_costs = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},  # per 1K tokens
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        # Add more models as needed
    }
    
    model_name = model or llm_config.model_id
    costs = model_costs.get(model_name, {"input": 0.01, "output": 0.02})  # Default pricing
    
    # Assume 50/50 split between input and output for estimation
    input_tokens = tokens * 0.5
    output_tokens = tokens * 0.5
    
    input_cost = (input_tokens / 1000) * costs["input"]
    output_cost = (output_tokens / 1000) * costs["output"]
    
    return {
        "input_tokens": int(input_tokens),
        "output_tokens": int(output_tokens),
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6)
    }


def validate_message_length(messages: List[Dict[str, str]], max_tokens: Optional[int] = None) -> Dict[str, Any]:
    """
    Validate message length against token limits
    
    Args:
        messages: List of messages
        max_tokens: Maximum allowed tokens (defaults to configured max)
    
    Returns:
        Validation result with token counts
    """
    max_allowed = max_tokens or llm_config.max_tokens
    total_tokens = 0
    
    message_tokens = []
    for i, message in enumerate(messages):
        content = message.get("content", "")
        tokens = count_tokens(content)
        total_tokens += tokens
        
        message_tokens.append({
            "index": i,
            "role": message.get("role", "unknown"),
            "content_length": len(content),
            "tokens": tokens
        })
    
    return {
        "total_tokens": total_tokens,
        "max_allowed": max_allowed,
        "within_limit": total_tokens <= max_allowed,
        "message_tokens": message_tokens
    }
