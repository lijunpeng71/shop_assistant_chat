import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Dict, Any

from core.config import settings


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in {
                'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                'filename', 'module', 'lineno', 'funcName', 'created',
                'msecs', 'relativeCreated', 'thread', 'threadName',
                'processName', 'process', 'getMessage', 'exc_info',
                'exc_text', 'stack_info', 'message'
            }:
                log_entry[key] = value
        
        return json.dumps(log_entry, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color
        return f"{log_color}{formatted}{reset}"


class LoggerManager:
    """Enterprise-level logger manager"""
    
    def __init__(self):
        self.loggers: Dict[str, logging.Logger] = {}
        self._setup_root_logger()
    
    def _setup_root_logger(self):
        """Setup root logger configuration"""
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, settings.log_level))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Add console handler
        console_handler = self._create_console_handler()
        root_logger.addHandler(console_handler)
        
        # Add file handler if not in testing
        if not settings.is_testing:
            file_handler = self._create_file_handler()
            if file_handler:
                root_logger.addHandler(file_handler)
    
    def _create_console_handler(self) -> logging.StreamHandler:
        """Create console handler with appropriate formatter"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.log_level))
        
        if settings.is_development and settings.log_format != "json":
            formatter = ColoredFormatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        else:
            formatter = JSONFormatter() if settings.log_format == "json" else logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        
        console_handler.setFormatter(formatter)
        return console_handler
    
    def _create_file_handler(self) -> logging.Handler:
        """Create file handler with rotation"""
        try:
            # Ensure log directory exists
            log_path = Path(settings.log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Parse log size
            max_bytes = self._parse_size(settings.log_max_size)
            
            if settings.log_format == "json":
                handler = RotatingFileHandler(
                    settings.log_file_path,
                    maxBytes=max_bytes,
                    backupCount=settings.log_backup_count,
                    encoding="utf-8"
                )
                handler.setFormatter(JSONFormatter())
            else:
                handler = TimedRotatingFileHandler(
                    settings.log_file_path,
                    when="midnight",
                    backupCount=settings.log_backup_count,
                    encoding="utf-8"
                )
                handler.setFormatter(logging.Formatter(
                    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                ))
            
            handler.setLevel(getattr(logging, settings.log_level))
            return handler
            
        except Exception as e:
            # Fallback to console if file handler fails
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setFormatter(logging.Formatter(
                f"ERROR: Could not create file handler: {e}"
            ))
            return console_handler
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string to bytes"""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get or create a logger with the given name"""
        if name not in self.loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, settings.log_level))
            self.loggers[name] = logger
        return self.loggers[name]


# Initialize logger manager
logger_manager = LoggerManager()

# Convenience function
def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance"""
    if name is None:
        name = "app"
    return logger_manager.get_logger(name)

# Default logger for the application
log = get_logger("shop_assistant")

# Configure third-party loggers
def configure_third_party_loggers():
    """Configure log levels for third-party libraries"""
    third_party_loggers = {
        "uvicorn": "INFO",
        "uvicorn.access": "WARNING",
        "fastapi": "INFO",
        "langchain": "WARNING",
        "httpx": "WARNING",
        "modelscope": settings.log_level if settings.debug else "WARNING",
        "watchfiles": "WARNING",  # 禁用watchfiles日志
        "watchfiles.main": "WARNING",  # 禁用watchfiles主日志
    }
    
    for logger_name, level in third_party_loggers.items():
        logging.getLogger(logger_name).setLevel(getattr(logging, level))

# Initialize third-party logger configuration
configure_third_party_loggers()