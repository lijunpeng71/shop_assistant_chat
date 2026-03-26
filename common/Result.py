"""统一的API响应结果"""

from typing import Any, Optional


class ApiResult:
    """统一的API响应结果类"""
    
    @staticmethod
    def success(data: Any = None, message: str = "请求成功") -> dict:
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 响应消息
            
        Returns:
            标准化的成功响应
        """
        return {
            "code": 0,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str = "请求失败", code: int = 1, data: Any = None) -> dict:
        """
        错误响应
        
        Args:
            message: 错误消息
            code: 错误码
            data: 错误数据
            
        Returns:
            标准化的错误响应
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def server_error(message: str = "服务器内部错误", data: Any = None) -> dict:
        """
        服务器错误响应
        
        Args:
            message: 错误消息
            data: 错误数据
            
        Returns:
            服务器错误响应
        """
        return {
            "code": 500,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def not_found(message: str = "资源不存在", data: Any = None) -> dict:
        """
        资源不存在响应
        
        Args:
            message: 错误消息
            data: 错误数据
            
        Returns:
            资源不存在响应
        """
        return {
            "code": 404,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def bad_request(message: str = "请求参数错误", data: Any = None) -> dict:
        """
        请求参数错误响应
        
        Args:
            message: 错误消息
            data: 错误数据
            
        Returns:
            请求参数错误响应
        """
        return {
            "code": 400,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def unauthorized(message: str = "未授权访问", data: Any = None) -> dict:
        """
        未授权响应
        
        Args:
            message: 错误消息
            data: 错误数据
            
        Returns:
            未授权响应
        """
        return {
            "code": 401,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def forbidden(message: str = "禁止访问", data: Any = None) -> dict:
        """
        禁止访问响应
        
        Args:
            message: 错误消息
            data: 错误数据
            
        Returns:
            禁止访问响应
        """
        return {
            "code": 403,
            "message": message,
            "data": data
        }
