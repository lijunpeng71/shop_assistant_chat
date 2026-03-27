"""
主智能体 - 基于LangChain DeepAgents
"""

import time
from typing import Any, Dict, Optional

from agents.intent_recognition_agent import intent_recognition_agent
from agents.purchase_deepagent import purchase_subagent
from agents.search_deepagent import search_subagent
from agents.task_deepagent import task_subagent
from core.logger import get_logger
from deepagents import create_deep_agent

from llm import chat_base_model
from tools.deepagents_tools import DEEPAGENTS_TOOLS

log = get_logger(__name__)


class MainDeepAgent:
    """主智能体 - 负责协调各个子智能体"""

    def __init__(self):
        """初始化主智能体"""
        self.agent = self._create_agent()
        self.intent_agent = intent_recognition_agent

    def _create_agent(self):
        """创建主智能体"""

        # 主智能体系统提示
        main_system_prompt = (
            "你是一个智能助手协调器，负责管理多个专业子智能体。你的工作流程：\n\n"
            "1. **理解用户需求** - 分析用户的问题和意图\n"
            "2. **选择合适的子智能体** - 根据需求选择task-agent、purchase-agent或search-agent\n"
            "3. **协调任务执行** - 将任务委托给合适的子智能体\n"
            "4. **整合结果** - 汇总子智能体的结果并提供完整的回答\n\n"
            "子智能体分工：\n"
            "- **task-agent**: 任务执行、冰柜陈列、库存管理\n"
            "- **purchase-agent**: 商品采购、供应商管理、采购策略\n"
            "- **search-agent**: 信息搜索、市场调研、数据分析\n\n"
            "## 可用工具\n"
            "你可以使用以下工具来获取任务信息：\n"
            "- **get_available_tasks()**: 获取所有可用任务列表\n"
            "- **search_tasks(keyword)**: 根据关键词搜索相关任务\n"
            "- **get_task_details(task_id)**: 获取特定任务的详细信息\n"
            "- **get_tasks_by_category(category)**: 根据分类获取任务 (task/purchase/search)\n\n"
            "## 工具使用指南\n"
            "1. 当用户询问'有哪些任务'、'能做什么'时，使用get_available_tasks()\n"
            "2. 当用户提到具体需求时，使用search_tasks()搜索相关任务\n"
            "3. 当用户询问特定任务详情时，使用get_task_details()\n"
            "4. 当用户需要特定类型的任务时，使用get_tasks_by_category()\n\n"
            "## 拍照需求处理\n"
            "当任务需要拍照时（如冰柜陈列检查），你必须在返回的消息中包含'需要拍照'标识。\n"
            "格式：在消息中明确加入'需要拍照'字样，例如：\n"
            "'此任务需要拍照来完成，请准备好相机。需要拍照'\n"
            "或者：'为了完成冰柜陈列检查，需要拍照。需要拍照'\n\n"
            "请根据用户的具体需求，选择最合适的子智能体来处理任务。如果是一般性对话，可以直接回答。"
        )

        # 子智能体列表
        subagents = [
            task_subagent,
            purchase_subagent,
            search_subagent
        ]

        try:
            # 创建带有工具的DeepAgents
            agent = create_deep_agent(
                model=chat_base_model,
                system_prompt=main_system_prompt,
                subagents=subagents,
                tools=DEEPAGENTS_TOOLS,  # 集成工具
            )

            log.info("✅ 主智能体初始化成功")
            log.info(f"📋 已注册子智能体: {[s['name'] for s in subagents]}")

            return agent

        except Exception as e:
            log.error(f"❌ 主智能体初始化失败: {e}")
            # 直接抛出异常，不使用模拟智能体
            raise RuntimeError(f"主智能体创建失败: {e}")

    def _build_context_from_history(self, history: list, current_message: str, user_id: str = None,
                                    session_id: str = None) -> str:
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

    async def process_message(self, message: str, user_id: str = None, session_id: str = None, image_url: str = None,
                              history: list = None) -> Dict[str, Any]:
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

            # 直接使用主智能体处理消息，不进行意图识别
            return await self._process_with_main_agent(message, user_id, session_id, image_url, history)

        except Exception as e:
            log.error(f"❌ 主智能体处理失败: {e}")
            return f"抱歉，处理您的请求时遇到了问题，请稍后重试。错误详情：{str(e)}"

    async def _process_with_main_agent(self, message: str, user_id: str = None, session_id: str = None,
                                       image_url: str = None, history: list = None) -> Dict[str, Any]:
        """使用传统的主智能体处理消息"""
        try:
            # 构建完整的消息上下文
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

            # 调用DeepAgents
            try:
                # DeepAgents需要正确的消息格式
                result = await self.agent.ainvoke({
                    "messages": [
                        {"role": "user", "content": full_message}
                    ]
                })

                # 检查是否是中断状态
                if hasattr(result, 'interrupted') and result.interrupted:
                    return self._handle_deepagents_interrupt(result, user_id, session_id, image_url)

                # 解析正常结果 - 提取AIMessage的content
                # result是一个字典，不是对象
                if isinstance(result, dict) and 'messages' in result and result['messages']:
                    messages = result['messages']
                    
                    # 从messages中找到AIMessage（通常是最后一条消息）
                    ai_message = None
                    for msg in reversed(messages):
                        # 检查消息类型，更准确地识别AIMessage
                        msg_type = str(type(msg).__name__)
                        if hasattr(msg, 'content') and ('AIMessage' in msg_type or 'AI' in msg_type):
                            ai_message = msg
                            break
                    
                    if ai_message and hasattr(ai_message, 'content'):
                        response_text = ai_message.content
                    else:
                        # 如果没有找到AIMessage，使用最后一条消息
                        last_message = messages[-1]
                        response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
                elif hasattr(result, 'content'):
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

                # 只返回大模型的回答内容
                return response_text

            except Exception as deepagents_error:
                log.error(f"❌ DeepAgents处理失败: {deepagents_error}")
                # 如果DeepAgents失败，检查是否是中断相关的错误
                if "interrupt" in str(deepagents_error).lower():
                    return self._handle_interrupt_error(deepagents_error, user_id, session_id, image_url)
                else:
                    # 其他错误，直接返回错误信息
                    return f"智能体处理失败，请稍后重试。错误详情：{str(deepagents_error)}"

        except Exception as e:
            log.error(f"❌ 传统主智能体处理失败: {e}")
            return f"抱歉，处理您的请求时遇到了问题，请稍后重试。错误详情：{str(e)}"

    async def _call_task_agent(self, message: str, user_id: str = None, session_id: str = None,
                               image_url: str = None) -> str:
        """调用任务智能体"""
        # 注意：现在工具由DeepAgents智能体自主调用，这个方法可能不会被调用
        # 保留作为回退机制
        return "📋 **任务执行模式**\n\n我将协助您完成各种任务执行工作。请告诉我您具体需要什么帮助，我会使用合适的工具来为您服务。"

    async def _call_purchase_agent(self, message: str, user_id: str = None, session_id: str = None) -> str:
        """调用采购智能体"""
        # 注意：现在工具由DeepAgents智能体自主调用，这个方法可能不会被调用
        # 保留作为回退机制
        return "🛒 **采购管理模式**\n\n我将协助您完成各种采购管理工作。请告诉我您具体需要什么帮助，我会使用合适的工具来为您服务。"

    async def _call_search_agent(self, message: str, user_id: str = None, session_id: str = None) -> str:
        """调用搜索智能体"""
        # 注意：现在工具由DeepAgents智能体自主调用，这个方法可能不会被调用
        # 保留作为回退机制
        return "🔍 **信息搜索模式**\n\n我将协助您完成各种信息搜索工作。请告诉我您具体需要什么帮助，我会使用合适的工具来为您服务。"

    def _handle_deepagents_interrupt(self, result, user_id: str, session_id: str, image_url: str = None) -> Dict[
        str, Any]:
        """处理DeepAgents的中断状态"""
        try:
            # 获取中断信息
            interrupt_info = getattr(result, 'interrupt_info', {})
            interrupt_reason = interrupt_info.get('reason', 'unknown')
            interrupt_message = interrupt_info.get('message', '任务需要用户确认')

            log.info(f"🔄 DeepAgents中断: reason={interrupt_reason}")

            # 在中断时进行意图识别，帮助确定下一步操作
            if interrupt_reason in ["task_confirmation", "user_approval"]:
                # 需要用户确认的中断，使用意图识别帮助用户决策
                return self._handle_interrupt_with_intent_recognition(interrupt_info, user_id, session_id, image_url)
            else:
                # 其他类型的中断，直接处理
                if interrupt_reason == "image_required":
                    return self._handle_image_required_interrupt(interrupt_info, user_id, session_id)
                elif interrupt_reason == "task_confirmation":
                    return self._handle_task_confirmation_interrupt(interrupt_info, user_id, session_id, image_url)
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

    async def _handle_interrupt_with_intent_recognition(self, interrupt_info: dict, user_id: str, session_id: str, 
                                                   image_url: str = None) -> Dict[str, Any]:
        """在中断时使用意图识别帮助用户决策"""
        try:
            # 构建中断场景的意图识别提示
            interrupt_context = f"""
当前场景：智能体执行任务时被中断

中断信息：
- 中断原因：{interrupt_info.get('reason', 'unknown')}
- 中断消息：{interrupt_info.get('message', '需要用户决策')}
- 任务类型：{interrupt_info.get('task_info', {}).get('task_name', '未知任务')}

请分析用户可能的意图并选择合适的处理方式。
"""
            
            # 调用意图识别
            intent_result = await self.intent_agent.recognize_intent(interrupt_context, [
                {
                    "type": "confirm",
                    "title": "确认执行",
                    "description": "用户确认继续执行被中断的任务",
                    "agent": "main-agent"
                },
                {
                    "type": "cancel", 
                    "title": "取消任务",
                    "description": "用户取消当前任务",
                    "agent": "main-agent"
                },
                {
                    "type": "modify",
                    "title": "修改任务",
                    "description": "用户修改任务参数或要求",
                    "agent": "main-agent"
                },
                {
                    "type": "help",
                    "title": "需要帮助",
                    "description": "用户需要更多帮助信息",
                    "agent": "main-agent"
                }
            ])
            
            selected_result = intent_result.get('selected_result', {})
            confidence = intent_result.get('confidence', 0.0)
            
            log.info(f"🎯 中断场景意图识别: 选择={selected_result.get('title')}, 置信度={confidence}")
            
            # 根据意图识别结果构建响应
            if selected_result.get('type') == 'confirm':
                return self._build_confirm_response(interrupt_info)
            elif selected_result.get('type') == 'cancel':
                return self._build_cancel_response()
            elif selected_result.get('type') == 'modify':
                return self._build_modify_response(interrupt_info)
            else:
                return self._build_help_response(interrupt_info)
                
        except Exception as e:
            log.error(f"❌ 中断场景意图识别失败: {e}")
            # 回退到通用中断处理
            return self._handle_generic_interrupt(interrupt_info, user_id, session_id)

    def _build_confirm_response(self, interrupt_info: dict) -> str:
        """构建确认响应"""
        task_info = interrupt_info.get('task_info', {})
        return f"🔄 **任务确认**\n\n{interrupt_info.get('message', '请确认是否执行此任务')}\n\n**任务详情**：\n- 任务类型：{task_info.get('task_name', '未知任务')}\n- 任务描述：{task_info.get('description', '无描述')}\n\n💡 基于意图识别，建议您确认执行此任务。\n\n⚠️ 请回复\"确认执行\"或\"同意执行\"来继续，或回复\"取消\"来放弃任务。"

    def _build_cancel_response(self) -> str:
        """构建取消响应"""
        return "🚫 **任务取消**\n\n基于意图识别，您可能想要取消当前任务。\n\n任务已取消，您可以开始新的任务或寻求其他帮助。"

    def _build_modify_response(self, interrupt_info: dict) -> str:
        """构建修改响应"""
        return "🔧 **任务修改**\n\n基于意图识别，您可能想要修改当前任务。\n\n请告诉我您希望如何修改任务参数或要求。"

    def _build_help_response(self, interrupt_info: dict) -> str:
        """构建帮助响应"""
        return f"❓ **需要帮助**\n\n基于意图识别，您可能需要更多帮助信息。\n\n当前任务状态：{interrupt_info.get('message', '任务已暂停')}\n\n请告诉我您需要什么具体帮助。"

    def _handle_task_confirmation_interrupt(self, interrupt_info: dict, user_id: str, session_id: str,
                                            image_url: str = None) -> str:
        """处理任务确认中断"""
        task_info = interrupt_info.get('task_info', {})
        return f"📋 **任务确认**\n\n{interrupt_info.get('message', '请确认是否执行此任务')}\n\n**任务详情**：\n- 任务类型：{task_info.get('task_name', '未知任务')}\n- 任务描述：{task_info.get('description', '无描述')}\n- 预计耗时：{task_info.get('estimated_time', '未知')}\n\n⚠️ 请回复\"确认执行\"或\"同意执行\"来继续，或回复\"取消\"来放弃任务。"

    def _handle_image_required_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> str:
        """处理图片需求中断"""
        return f"📸 **需要图片**\n\n{interrupt_info.get('message', '此任务需要提供图片')}\n\n请提供图片URL，我将基于图片进行专业分析。"

    def _handle_user_approval_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> str:
        """处理用户批准中断"""
        return f"⚠️ **需要批准**\n\n{interrupt_info.get('message', '此操作需要您的批准')}\n\n请确认是否继续执行此操作。"

    def _handle_generic_interrupt(self, interrupt_info: dict, user_id: str, session_id: str) -> str:
        """处理通用中断"""
        return f"⏸️ **任务暂停**\n\n{interrupt_info.get('message', '任务已暂停，需要用户干预')}"

    def _handle_interrupt_error(self, error: Exception, user_id: str, session_id: str, image_url: str = None) -> str:
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
            return f"处理中断时发生错误：{error_message}"

    # 创建全局实例
main_deep_agent = MainDeepAgent()
