from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from core.logger import get_logger

log = get_logger(__name__)


class BaseCustomException(Exception):
    """Base exception for custom application exceptions"""
    
    def __init__(
        self,
        message: str,
        error_code: str = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AIModelError(BaseCustomException):
    """Raised when AI model operation fails"""
    
    def __init__(self, message: str = "AI model operation failed"):
        super().__init__(
            message=message,
            error_code="AI_MODEL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Simple exception handler"""
    log.error(f"Exception occurred: {type(exc).__name__}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )


def setup_exception_handlers(app):
    """Setup exception handlers for FastAPI app"""
    app.add_exception_handler(Exception, exception_handler)
