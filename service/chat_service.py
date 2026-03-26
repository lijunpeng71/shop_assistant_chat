import time
import sys
from typing import Dict, Any, Optional

from agents.main_deepagent import main_deep_agent
from core.logger import get_logger

log = get_logger(__name__)


class ChatService:
    """增强的聊天服务，支持多智能体，使用短期记忆（单例模式）"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # 使用主智能体
            self.main_agent = main_deep_agent
            self.session_memory = {}  # 短期记忆存储
            ChatService._initialized = True
    
    async def chat(self, message: str, user_id: str = None, session_id: str = None, image_url: str = None) -> Dict[str, Any]:
        """
        处理聊天消息
        
        Args:
            message: 用户消息
            user_id: 用户ID
            session_id: 会话ID
            image_url: 图片地址URL（可选）
            
        Returns:
            聊天响应结果
        """
        try:
            log.info(f"ChatService处理消息: user_id={user_id}, session_id={session_id}")
            
            # 检查是否是首次进入用户
            is_first_time = self._is_first_time_user(user_id, session_id)
            
            if is_first_time:
                # 首次进入，返回欢迎信息
                welcome_result = {
                    "type": "welcome",
                    "message": "欢迎使用智能助手！我可以帮您执行任务、管理采购、搜索信息等。请告诉我您需要什么帮助？",
                    "data": None,
                    "suggestions": ["我要执行任务", "我要采购商品", "搜索信息"]
                }
                
                # 保存首次进入的记录
                self._save_to_memory(user_id, session_id, message, welcome_result)
                
                log.info(f"首次进入用户处理完成: user_id={user_id}, session_id={session_id}")
                return welcome_result
            
            # 使用主智能体处理消息
            # 获取对话历史
            history = self._get_conversation_history(user_id, session_id)
            
            # 处理消息，传递历史上下文
            result = await self.main_agent.process_message(message, user_id, session_id, image_url, history)
            
            # 保存对话记录到短期记忆
            self._save_to_memory(user_id, session_id, message, result)
            
            log.info(f"聊天请求处理成功: type={result.get('type')}")
            return result
            
        except Exception as e:
            log.error(f"聊天处理失败: {e}")
            return {
                "type": "error",
                "message": "抱歉，处理您的请求时遇到了问题，请稍后重试。",
                "data": {"error": str(e)},
                "suggestions": ["请重新描述您的问题", "尝试简化您的需求"]
            }
    
    def _is_first_time_user(self, user_id: str, session_id: str) -> bool:
        """判断是否为首次进入用户（基于短期记忆）"""
        if not user_id or not session_id:
            return True
        
        # 检查短期记忆
        memory_key = f"{user_id}_{session_id}"
        if memory_key in self.session_memory:
            return False
        
        # 首次进入，初始化记忆
        self.session_memory[memory_key] = {
            "user_id": user_id,
            "session_id": session_id,
            "messages": [],
            "created_at": time.time(),
            "last_activity": time.time()
        }
        
        return True
    
    def _get_conversation_history(self, user_id: str, session_id: str) -> list:
        """
        获取对话历史
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            对话历史列表
        """
        try:
            memory_key = f"{user_id}_{session_id}"
            
            if memory_key in self.session_memory:
                messages = self.session_memory[memory_key]["messages"]
                
                # 返回最近的20条消息作为上下文
                recent_messages = messages[-20:] if len(messages) > 20 else messages
                
                log.info(f"📚 获取对话历史: session_id={session_id}, 历史消息数={len(recent_messages)}")
                
                return recent_messages
            
            log.info(f"📚 无对话历史: session_id={session_id}")
            return []
            
        except Exception as e:
            log.error(f"❌ 获取对话历史失败: {e}")
            return []
    
    async def _save_to_memory(
        self, 
        message: str, 
        response: Dict[str, Any], 
        user_id: str, 
        session_id: str
    ):
        """保存到短期记忆"""
        try:
            memory_key = f"{user_id}_{session_id}"
            
            if memory_key in self.session_memory:
                # 添加用户消息
                user_message = {
                    "role": "user",
                    "content": message,
                    "timestamp": time.time(),
                    "metadata": {"user_id": user_id}
                }
                
                # 添加助手回复
                response_content = str(response.get("result", response.get("message", "")))
                assistant_message = {
                    "role": "assistant",
                    "content": response_content,
                    "timestamp": time.time(),
                    "metadata": {
                        "type": response.get("type", "general"),
                        "user_id": user_id
                    }
                }
                
                # 保存到记忆中
                self.session_memory[memory_key]["messages"].extend([user_message, assistant_message])
                self.session_memory[memory_key]["last_activity"] = time.time()
                
                # 限制记忆长度（保留最近100条消息）
                if len(self.session_memory[memory_key]["messages"]) > 100:
                    self.session_memory[memory_key]["messages"] = self.session_memory[memory_key]["messages"][-100:]
                
                log.info(f"消息已保存到短期记忆: session_id={session_id}")
                
        except Exception as e:
            log.error(f"保存到短期记忆失败: {e}")
    
    async def get_conversation_history(self, session_id: str, limit: int = 50) -> Dict[str, Any]:
        """获取聊天历史（从短期记忆）"""
        try:
            # 查找对应的记忆
            memory_data = None
            for memory_key, memory in self.session_memory.items():
                if memory["session_id"] == session_id:
                    memory_data = memory
                    break
            
            if memory_data and memory_data["messages"]:
                messages = memory_data["messages"][-limit:]  # 获取最新的消息
                
                return {
                    "session_id": session_id,
                    "messages": messages,
                    "total": len(memory_data["messages"]),
                    "source": "short_term_memory"
                }
            
            return {
                "session_id": session_id,
                "messages": [],
                "total": 0,
                "source": "short_term_memory"
            }
                
        except Exception as e:
            log.error(f"获取聊天历史失败: {e}")
            return {
                "session_id": session_id,
                "error": str(e),
                "messages": [],
                "total": 0,
                "source": "short_term_memory"
            }
    
    async def cleanup_old_memory(self, max_age_hours: int = 24):
        """清理过期的短期记忆"""
        try:
            current_time = time.time()
            expired_keys = []
            
            for memory_key, memory in self.session_memory.items():
                age_hours = (current_time - memory["last_activity"]) / 3600
                if age_hours > max_age_hours:
                    expired_keys.append(memory_key)
            
            for key in expired_keys:
                del self.session_memory[key]
                log.info(f"清理过期记忆: {key}")
            
            if expired_keys:
                log.info(f"清理了 {len(expired_keys)} 个过期记忆")
                
        except Exception as e:
            log.error(f"清理记忆失败: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        total_sessions = len(self.session_memory)
        total_messages = sum(len(memory["messages"]) for memory in self.session_memory.values())
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "average_messages_per_session": total_messages / total_sessions if total_sessions > 0 else 0,
            "memory_usage_mb": sys.getsizeof(self.session_memory) / (1024 * 1024)
        }
