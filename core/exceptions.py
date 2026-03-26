from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

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


class ValidationErrorException(BaseCustomException):
    """Raised when validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class NotFoundError(BaseCustomException):
    """Raised when a resource is not found"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            error_code="NOT_FOUND_ERROR",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ConflictError(BaseCustomException):
    """Raised when a conflict occurs"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            error_code="CONFLICT_ERROR",
            status_code=status.HTTP_409_CONFLICT
        )


class RateLimitError(BaseCustomException):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_ERROR",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )


class ExternalServiceError(BaseCustomException):
    """Raised when an external service fails"""
    
    def __init__(self, message: str, service_name: str = None):
        details = {"service_name": service_name} if service_name else {}
        super().__init__(
            message=message,
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class DatabaseError(BaseCustomException):
    """Raised when database operation fails"""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AIModelError(BaseCustomException):
    """Raised when AI model operation fails"""
    
    def __init__(self, message: str = "AI model operation failed"):
        super().__init__(
            message=message,
            error_code="AI_MODEL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class BusinessLogicError(BaseCustomException):
    """Raised when business logic validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="BUSINESS_LOGIC_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


async def custom_exception_handler(request: Request, exc: BaseCustomException) -> JSONResponse:
    """Handler for custom exceptions"""
    log.error(
        f"Custom exception occurred: {exc.error_code}",
        extra={
            "error_code": exc.error_code,
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    response_data = {
        "success": False,
        "error": {
            "code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        },
        "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]) -> JSONResponse:
    """Handler for HTTP exceptions"""
    log.warning(
        f"HTTP exception occurred: {exc.status_code}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    response_data = {
        "success": False,
        "error": {
            "code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "details": {}
        },
        "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for request validation exceptions"""
    log.warning(
        f"Validation exception occurred: {exc.errors()}",
        extra={
            "validation_errors": exc.errors(),
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    # Format validation errors
    formatted_errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"]
        })
    
    response_data = {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": {
                "validation_errors": formatted_errors
            }
        },
        "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_data
    )


async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handler for Pydantic validation exceptions"""
    log.warning(
        f"Pydantic validation exception occurred: {exc.errors()}",
        extra={
            "validation_errors": exc.errors(),
            "path": str(request.url.path),
            "method": request.method
        }
    )
    
    # Format validation errors
    formatted_errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"]
        })
    
    response_data = {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Data validation failed",
            "details": {
                "validation_errors": formatted_errors
            }
        },
        "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_data
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for general exceptions"""
    log.error(
        f"Unhandled exception occurred: {type(exc).__name__}: {str(exc)}",
        extra={
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "path": str(request.url.path),
            "method": request.method
        },
        exc_info=True
    )
    
    response_data = {
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "details": {}
        },
        "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
    }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )


def setup_exception_handlers(app):
    """Setup exception handlers for the FastAPI app"""
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
