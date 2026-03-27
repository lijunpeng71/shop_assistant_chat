"""LLM (Large Language Model) module for AI model integration"""

from .model import chat_base_model

__all__ = [
    "chat_base_model",
]


def client():
    return None