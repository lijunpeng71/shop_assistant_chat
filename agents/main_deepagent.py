"""
主智能体 - 基于LangChain DeepAgents
"""

from typing import Dict, Any, Optional
import time
from deepagents import create_deep_agent
from agents.task_deepagent import task_subagent
from agents.purchase_deepagent import purchase_subagent
from agents.search_deepagent import search_subagent

from llm.client import llm_client
from core.logger import get_logger

log = get_logger(__name__)


class MainDeepAgent:
    """主智能体 - 负责协调各个子智能体"""
    
    def __init__(self):
        """初始化主智能体"""
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """创建主智能体"""
        
        # 主智能体系统提示
        main_system_prompt = """你是一个智能助手协调器，负责管理多个专业子智能体。你的工作流程：

1. **理解用户需求** - 分析用户的问题和意图
2. **选择合适的子智能体** - 根据需求选择task-agent、purchase-agent或search-agent
3. **协调任务执行** - 将任务委托给合适的子智能体
4. **整合结果** - 汇总子智能体的结果并提供完整的回答

子智能体分工：
- **task-agent**: 任务执行、冰柜陈列、库存管理
- **purchase-agent**: 商品采购、供应商管理、采购策略
- **search-agent**: 信息搜索、市场调研、数据分析

请根据用户的具体需求，选择最合适的子智能体来处理任务。如果是一般性对话，可以直接回答。"""
        
        # 子智能体列表
        subagents = [
            task_subagent,
            purchase_subagent,
            search_subagent
        ]
        
        try:
            # 创建DeepAgents主智能体
            agent = create_deep_agent(
                model=llm_client.model,
                system_prompt=main_system_prompt,
                subagents=subagents,
                tools=[],  # 主智能体不需要特殊工具
            )
            
            log.info("✅ 主智能体初始化成功")
            log.info(f"📋 已注册子智能体: {[s['name'] for s in subagents]}")
            
            return agent
            
        except Exception as e:
            log.error(f"❌ 主智能体初始化失败: {e}")
            # 如果DeepAgents初始化失败，返回模拟模式
            return self._create_mock_agent()
    
    def _create_mock_agent(self):
        """创建模拟智能体（当LLM未配置时）"""
        log.warning("⚠️ 使用模拟智能体模式")
        
        class MockAgent:
            async def __call__(self, message: str, **kwargs) -> Dict[str, Any]:
                """模拟智能体响应 - 所有模拟逻辑都在工具中执行"""
                from tools.simulation_tool import simulate_response
                
                user_id = kwargs.get('user_id')  # 不再提供默认值，必须从header获取
                session_id = kwargs.get('session_id')  # 不再提供默认值，必须从header获取
                
                if not user_id:
                    log.warning("⚠️ 缺少user_id，无法进行模拟")
                    return {
                        "type": "error",
                        "message": "缺少用户ID，无法处理请求",
                        "data": {"error": "Missing user_id"}
                    }
                
                return await simulate_response(message, user_id, "auto")
        
        return MockAgent()
    
    def _build_context_from_history(self, history: list, current_message: str, user_id: str = None, session_id: str = None) -> str:
        """
        从历史对话构建上下文
        
        Args:
            history: 对话历史列表
            current_message: 当前用户消息
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            构建的上下文消息
        """
        try:
            # 构建用户信息上下文
            user_info = f"""当前用户信息：
- 用户ID: {user_id or '未知'}
- 会话ID: {session_id or '未知'}
- 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # 构建对话历史上下文
            context_parts = []
            
            # 添加历史对话（限制最近10轮对话以避免上下文过长）
            recent_history = history[-10:] if len(history) > 10 else history
            
            for msg in recent_history:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                
                if role == 'user':
                    context_parts.append(f"用户: {content}")
                elif role == 'assistant':
                    context_parts.append(f"助手: {content}")
            
            # 添加当前消息
            context_parts.append(f"用户: {current_message}")
            
            # 构建完整的上下文
            full_context = "\n".join(context_parts)
            
            # 添加上下文提示
            context_prompt = f"""{user_info}以下是我们的对话历史，请基于上下文理解我的当前需求并给出回应：

{full_context}

请基于以上对话历史和当前用户信息，理解我的当前需求并提供合适的回应。"""
            
            log.info(f"📝 构建历史上下文: {len(recent_history)}条历史消息, 用户: {user_id}")
            
            return context_prompt
            
        except Exception as e:
            log.error(f"❌ 构建历史上下文失败: {e}")
            # 如果构建失败，返回带用户信息的原始消息
            return f"""当前用户信息：
- 用户ID: {user_id or '未知'}
- 会话ID: {session_id or '未知'}
- 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

用户消息: {current_message}"""
    
    async def process_message(self, message: str, user_id: str = None, session_id: str = None, image_url: str = None, history: list = None) -> Dict[str, Any]:
        """
        处理用户消息
        
        Args:
            message: 用户消息
            user_id: 用户ID
            session_id: 会话ID
            image_url: 图片地址URL（可选）
            history: 对话历史（可选）
            
        Returns:
            智能体响应结果
        """
        try:
            log.info(f"🤖 主智能体处理消息: user_id={user_id}, session_id={session_id}")
            
            # 构建完整的消息上下文，包含用户信息、历史对话和图片URL信息
            full_message = message
            
            # 添加用户上下文信息
            user_context = f"""当前用户信息：
- 用户ID: {user_id}
- 会话ID: {session_id}
- 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # 构建完整消息
            if image_url:
                full_message = f"{user_context}用户消息（包含图片）: {message}\n\n[图片URL: {image_url}]"
            else:
                full_message = f"{user_context}用户消息: {message}"
            
            # 如果有历史对话，构建上下文
            if history and len(history) > 0:
                context_message = self._build_context_from_history(history, message, user_id, session_id)
                full_message = context_message
            
            # 调用DeepAgents，让其处理human-in-the-loop中断
            try:
                result = await self.agent(full_message)
                
                # 检查是否是中断状态
                if hasattr(result, 'interrupted') and result.interrupted:
                    return self._handle_deepagents_interrupt(result, user_id, session_id, image_url)
                
                # 解析正常结果
                if hasattr(result, 'content'):
                    response_text = result.content
                else:
                    response_text = str(result)
                
                # 根据响应内容确定类型
                message_lower = message.lower()
                if any(keyword in message_lower for keyword in ["任务", "执行", "检查", "陈列"]):
                    response_type = "task"
                elif any(keyword in message_lower for keyword in ["采购", "购买", "进货"]):
                    response_type = "purchase"
                elif any(keyword in message_lower for keyword in ["搜索", "查询", "信息"]):
                    response_type = "search"
                else:
                    response_type = "general"
                
                log.info(f"✅ 主智能体处理完成: type={response_type}")
                
                return {
                    "type": response_type,
                    "message": response_text,
                    "data": None,
                    "suggestions": self._get_suggestions(response_type)
                }
                
            except Exception as deepagents_error:
                log.error(f"❌ DeepAgents处理失败: {deepagents_error}")
                # 如果DeepAgents失败，检查是否是中断相关的错误
                if "interrupt" in str(deepagents_error).lower():
                    return self._handle_interrupt_error(deepagents_error, user_id, session_id, image_url)
                else:
                    # 其他错误，使用模拟智能体
                    return await self._fallback_to_mock_agent(message, user_id, session_id)
            
        except Exception as e:
            log.error(f"❌ 主智能体处理失败: {e}")
            return {
                "type": "error",
                "message": "抱歉，处理您的请求时遇到了问题，请稍后重试。",
                "data": {"error": str(e)},
                "suggestions": ["请重新描述您的问题", "尝试简化您的需求"]
            }
    
    def _handle_deepagents_interrupt(self, result, user_id: str, session_id: str, image_url: str = None) -> Dict[str, Any]:
        """处理DeepAgents的中断状态"""
        try:
            # 获取中断信息
            interrupt_info = getattr(result, 'interrupt_info', {})
            interrupt_reason = interrupt_info.get('reason', 'unknown')
            interrupt_message = interrupt_info.get('message', '任务需要用户确认')
            
            log.info(f"🔄 DeepAgents中断: reason={interrupt_reason}")
            
            # 根据中断原因处理
            if interrupt_reason == "task_confirmation":
                return self._handle_task_confirmation_interrupt(interrupt_info, user_id, session_id, image_url)
            elif interrupt_reason == "image_required":
                return self._handle_image_required_interrupt(interrupt_info, user_id, session_id)
            elif interrupt_reason == "user_approval":
                return self._handle_user_approval_interrupt(interrupt_info, user_id, session_id)
            else:
                return self._handle_generic_interrupt(interrupt_info, user_id, session_id)
                
        except Exception as e:
            log.error(f"❌ 处理DeepAgents中断失败: {e}")
            return {
                "type": "interrupt",
                "message": "任务需要用户确认，但处理中断时发生错误。",
                "data": {
                    "interrupted": True,
                    "interrupt_reason": "error",
                    "error": str(e)
                },
                "suggestions": ["重新尝试", "联系客服"]
            }
    
    def _handle_task_confirmation_interrupt(self, interrupt_info: dict, user_id: str, session_id: str, image_url: str = None) -> Dict[str, Any]:
        """处理任务确认中断"""
        task_info = interrupt_info.get('task_info', {})
        
        return {
            "type": "task",
            "message": f"📋 **任务确认**\n\n{interrupt_info.get('message', '请确认是否执行此任务')}\n\n**任务详情**：\n- 任务类型：{task_info.get('task_name', '未知任务')}\n- 任务描述：{task_info.get('description', '无描述')}\n- 预计耗时：{task_info.get('estimated_time', '未知')}\n\n⚠️ 请回复\"确认执行\"或\"同意执行\"来继续，或回复\"取消\"来放弃任务。",
            "data": {
                "interrupted": True,
                "interrupt_reason": "task_confirmation",
                "task_info": task_info,
                "requires_confirmation": True,
                "confirmation_options": ["确认执行", "同意执行", "取消"],
                "waiting_for_user_response": True
            },
            "suggestions": ["确认执行", "取消任务", "了解更多"]
        }
    
    def _handle_image_required_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> Dict[str, Any]:
        """处理图片需求中断"""
        return {
            "type": "task",
            "message": f"📸 **需要图片**\n\n{interrupt_info.get('message', '此任务需要提供图片')}\n\n请提供图片URL，我将基于图片进行专业分析。",
            "data": {
                "interrupted": True,
                "interrupt_reason": "image_required",
                "requires_image": True,
                "image_type": interrupt_info.get('image_type', 'general'),
                "task_type": interrupt_info.get('task_type', 'unknown'),
                "instructions": interrupt_info.get('instructions', ['请提供图片URL'])
            },
            "suggestions": ["提供图片URL", "取消任务", "了解更多"]
        }
    
    def _handle_user_approval_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> Dict[str, Any]:
        """处理用户批准中断"""
        return {
            "type": "task",
            "message": f"⚠️ **需要批准**\n\n{interrupt_info.get('message', '此操作需要您的批准')}\n\n请确认是否继续执行此操作。",
            "data": {
                "interrupted": True,
                "interrupt_reason": "user_approval",
                "requires_approval": True,
                "operation_info": interrupt_info.get('operation_info', {}),
                "approval_options": ["批准", "拒绝", "取消"]
            },
            "suggestions": ["批准", "拒绝", "了解更多"]
        }
    
    def _handle_generic_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> Dict[str, Any]:
        """处理通用中断"""
        return {
            "type": "interrupt",
            "message": f"⏸️ **任务暂停**\n\n{interrupt_info.get('message', '任务已暂停，需要用户干预')}",
            "data": {
                "interrupted": True,
                "interrupt_reason": interrupt_info.get('reason', 'generic'),
                "interrupt_info": interrupt_info
            },
            "suggestions": ["继续", "取消", "了解更多"]
        }
    
    def _handle_interrupt_error(self, error: Exception, user_id: str, session_id: str, image_url: str = None) -> Dict[str, Any]:
        """处理中断错误"""
        error_message = str(error)
        
        # 分析错误类型
        if "image" in error_message.lower():
            return self._handle_image_required_interrupt(
                {"message": "执行任务时发现需要图片", "image_type": "freezer_photo"},
                user_id, session_id
            )
        elif "confirmation" in error_message.lower():
            return self._handle_task_confirmation_interrupt(
                {"message": "任务需要确认", "task_info": {"task_name": "待确认任务"}},
                user_id, session_id, image_url
            )
        else:
            return {
                "type": "error",
                "message": f"处理中断时发生错误：{error_message}",
                "data": {
                    "interrupted": True,
                    "interrupt_reason": "error",
                    "error": error_message
                },
                "suggestions": ["重新尝试", "简化请求", "联系客服"]
            }
    
    async def _fallback_to_mock_agent(self, message: str, user_id: str, session_id: str) -> Dict[str, Any]:
        """回退到模拟智能体 - 所有模拟逻辑都在工具中执行"""
        log.warning("⚠️ 回退到模拟智能体模式")
        
        from tools.simulation_tool import simulate_response
        
        if not user_id:
            log.warning("⚠️ 缺少user_id，无法进行模拟")
            return {
                "type": "error",
                "message": "缺少用户ID，无法处理请求",
                "data": {"error": "Missing user_id"}
            }
        
        return await simulate_response(message, user_id, "auto")
    
    def _get_suggestions(self, response_type: str) -> list:
        """根据响应类型获取建议"""
        suggestions_map = {
            "task": ["我要执行任务", "检查冰柜陈列", "查看库存状态"],
            "purchase": ["我要采购商品", "分析采购需求", "查看供应商信息"],
            "search": ["搜索市场信息", "查询商品价格", "分析销售数据"],
            "general": ["我要执行任务", "我要采购商品", "搜索信息"],
            "welcome": ["我要执行任务", "我要采购商品", "搜索信息"],
            "error": ["重新描述问题", "联系客服", "查看帮助文档"]
        }
        
        return suggestions_map.get(response_type, ["我要执行任务", "我要采购商品", "搜索信息"])


# 创建全局实例
main_deep_agent = MainDeepAgent()
