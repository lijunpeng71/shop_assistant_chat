#!/usr/bin/env python3
"""
聊天服务层
处理所有与聊天相关的业务逻辑
"""

from typing import Dict, Optional, Any, List

# 优先使用带插件支持的引擎
try:
    from backend.modules.llm.core.llm_with_plugins import EmotionalChatEngineWithPlugins

    PLUGIN_ENGINE_AVAILABLE = True
except ImportError:
    PLUGIN_ENGINE_AVAILABLE = False
    EmotionalChatEngineWithPlugins = None
from app.common.global_models import ChatRequest, ChatResponse
import uuid
from datetime import datetime

# 尝试导入RAG服务（可选功能）
try:
    from backend.modules.rag.services.rag_service import RAGIntegrationService

    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    RAGIntegrationService = None

# 尝试导入意图识别服务（可选功能）
try:
    from backend.modules.intent.services import IntentService

    INTENT_AVAILABLE = True
except ImportError:
    INTENT_AVAILABLE = False
    IntentService = None

# 导入增强版输入处理器
try:
    from backend.modules.intent.core.enhanced_input_processor import EnhancedInputProcessor

    ENHANCED_PROCESSOR_AVAILABLE = True
except ImportError:
    ENHANCED_PROCESSOR_AVAILABLE = False
    EnhancedInputProcessor = None


class ChatService:
    """聊天服务 - 统一的聊天接口"""

    def __init__(self):
        """
        初始化聊天服务
        """

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        处理聊天请求（支持记忆系统）

        Args:
            request: 聊天请求
            use_memory_system: 是否启用记忆系统

        Returns:
            聊天响应
        """
        # 生成会话ID（如果没有）
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        else:
            # 使用原有引擎（无记忆）
            return self.chat_engine.chat(request)

    async def _chat_with_memory(self, request: ChatRequest) -> ChatResponse:
        """使用记忆系统的聊天"""
        user_id = request.user_id or "anonymous"
        session_id = request.session_id
        message = request.message

        # 0. 增强版输入预处理（第一步）
        preprocessed = None
        if self.enhanced_processor_enabled and self.enhanced_processor:
            try:
                preprocessed = self.enhanced_processor.preprocess(message, user_id)

                # 检查是否被阻止
                if preprocessed["blocked"]:
                    return ChatResponse(
                        response=preprocessed.get("friendly_message", "输入无效，请重新输入"),
                        emotion="neutral",
                        session_id=session_id,
                        timestamp=datetime.now(),
                        context={
                            "blocked": True,
                            "reason": preprocessed["warnings"],
                            "input_validation": "failed"
                        }
                    )

                # 使用清洗后的文本
                message = preprocessed["cleaned"]

                # 如果检测到重复且频率过高，可以提供特殊提示
                if preprocessed["metadata"].get("high_frequency_repeat"):
                    print(f"⚠️ 用户 {user_id} 高频重复输入: {message[:30]}...")

            except Exception as e:
                print(f"输入预处理失败，使用原始消息: {e}")
                preprocessed = None

        # 1. 分析情绪（使用清洗后的消息）
        emotion_result = self.chat_engine.analyze_emotion(message)
        emotion = emotion_result.get("emotion", "neutral")
        emotion_intensity = emotion_result.get("intensity", 5.0)

        # 2. 意图识别（如果启用）
        intent_result = None
        if self.intent_enabled and self.intent_service:
            try:
                intent_analysis = self.intent_service.analyze(message, user_id)
                intent_result = intent_analysis.get('intent', {})

                # 检查是否需要特殊处理（危机情况）
                if intent_analysis.get('action_required', False):
                    print(f"⚠️ 检测到用户 {user_id} 的危机情况，意图: {intent_result.get('intent')}")
                    # 这里可以触发特殊的危机响应流程

            except Exception as e:
                print(f"意图识别失败: {e}")
                intent_result = None

        # 3. 构建上下文（包含记忆）
        context = await self.context_service.build_context(
            user_id=user_id,
            session_id=session_id,
            current_message=message,
            emotion=emotion,
            emotion_intensity=emotion_intensity
        )

        # 将意图信息添加到上下文中
        if intent_result:
            context['intent'] = intent_result

        # 4. 尝试使用RAG增强回复
        rag_result = None
        print(f"ChatService RAG检查: rag_enabled={self.rag_enabled}, rag_service={self.rag_service is not None}")
        if self.rag_enabled and self.rag_service:
            try:
                print("ChatService尝试使用RAG增强")
                # 获取对话历史
                conversation_history = await self._get_conversation_history(session_id)

                # 尝试RAG增强
                rag_result = self.rag_service.enhance_response(
                    message=message,
                    emotion=emotion,
                    conversation_history=conversation_history
                )
                print(f"ChatService RAG结果: {rag_result}")

            except Exception as e:
                print(f"RAG增强失败，使用常规回复: {e}")
        else:
            print("ChatService RAG未启用，使用常规引擎")

        # 5. 生成回复
        if rag_result and rag_result.get("use_rag"):
            # 使用RAG增强的回复
            response = ChatResponse(
                response=rag_result["answer"],
                emotion=emotion,
                emotion_intensity=emotion_intensity,
                session_id=session_id,
                timestamp=datetime.now()
            )
            # 添加RAG来源信息和预处理信息
            response.context = {
                "memories_count": len(context.get("memories", {}).get("all", [])),
                "emotion_trend": context.get("emotion_context", {}).get("trend", {}).get("trend"),
                "has_profile": bool(context.get("user_profile", {}).get("summary")),
                "used_rag": True,
                "knowledge_sources": len(rag_result.get("sources", [])),
                "intent": intent_result.get('intent') if intent_result else None,
                "intent_confidence": intent_result.get('confidence') if intent_result else None,
                "input_preprocessed": preprocessed is not None,
                "input_metadata": preprocessed.get("metadata") if preprocessed else None
            }
        else:
            # 使用常规引擎回复
            print(f"ChatService使用常规引擎: session_id={session_id}, user_id={user_id}")
            try:
                response = self.chat_engine.chat(request)
                print(f"ChatService常规引擎回复完成: {response.session_id}")
            except Exception as e:
                print(f"ChatService常规引擎调用失败: {e}")
                import traceback
                traceback.print_exc()
                # 创建简单的回复
                response = ChatResponse(
                    response="抱歉，我遇到了一些技术问题，请稍后再试。",
                    session_id=session_id,
                    emotion="neutral",
                    timestamp=datetime.now()
                )
            response.context = {
                "memories_count": len(context.get("memories", {}).get("all", [])),
                "emotion_trend": context.get("emotion_context", {}).get("trend", {}).get("trend"),
                "has_profile": bool(context.get("user_profile", {}).get("summary")),
                "used_rag": False,
                "intent": intent_result.get('intent') if intent_result else None,
                "intent_confidence": intent_result.get('confidence') if intent_result else None,
                "input_preprocessed": preprocessed is not None,
                "input_metadata": preprocessed.get("metadata") if preprocessed else None
            }
        return response

    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        获取会话摘要

        Args:
            session_id: 会话ID

        Returns:
            会话摘要
        """
        return self.chat_engine.get_session_summary(session_id)

    async def delete_sessions_batch(self, session_ids: List[str]) -> Dict[str, Any]:
        """
        批量删除会话

        Args:
            session_ids: 会话ID列表

        Returns:
            删除结果
        """
        try:
            success_count = 0
            failed_count = 0
            failed_sessions = []

            for session_id in session_ids:
                try:
                    success = await self.delete_session(session_id)
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_sessions.append(session_id)
                except Exception as e:
                    failed_count += 1
                    failed_sessions.append(session_id)
                    print(f"删除会话 {session_id} 失败: {e}")

            return {
                "success_count": success_count,
                "failed_count": failed_count,
                "failed_sessions": failed_sessions,
                "total": len(session_ids)
            }
        except Exception as e:
            print(f"批量删除会话失败: {e}")
            return {
                "success_count": 0,
                "failed_count": len(session_ids),
                "failed_sessions": session_ids,
                "total": len(session_ids),
                "error": str(e)
            }

    async def get_user_emotion_trends(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        获取用户情绪趋势

        Args:
            user_id: 用户ID
            days: 天数

        Returns:
            情绪趋势
        """
        return self.chat_engine.get_user_emotion_trends(user_id)
