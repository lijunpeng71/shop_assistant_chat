"""
意图识别智能体 - 基于LangChain DeepAgents
"""

from typing import Any, Dict, List, Optional

from core.logger import get_logger
from deepagents import create_deep_agent

from llm import chat_base_model

log = get_logger(__name__)


class IntentRecognitionAgent:
    """意图识别智能体 - 负责识别用户意图并选择合适的处理方案"""

    def __init__(self):
        """初始化意图识别智能体"""
        self.intent_mappings = self._init_intent_mappings()
        self.agent = self._create_agent()

    def _create_agent(self):
        """创建意图识别智能体"""

        # 意图识别系统提示
        intent_system_prompt = (
            "你是一个专业的意图识别助手。你的职责是：\n\n"
            "1. **分析用户输入** - 理解用户的具体需求和意图\n"
            "2. **匹配预定义结果集** - 从给定的候选结果集中选择最合适的答案\n"
            "3. **返回最佳匹配** - 返回选择的结果和置信度\n\n"
            "工作流程：\n"
            "- 接收用户输入和预定义的结果集\n"
            "- 分析用户意图和语义\n"
            "- 从结果集中选择最匹配的选项\n"
            "- 返回选择结果和置信度评分\n\n"
            "重要原则：\n"
            "- 必须从给定的结果集中选择答案\n"
            "- 基于语义相似度和用户需求进行匹配\n"
            "- 提供置信度评分帮助决策\n"
            "- 如果没有合适的匹配，选择最接近的选项\n\n"
            "请始终以客观、准确的方式进行意图识别和匹配。"
        )

        try:
            # 创建DeepAgents意图识别智能体
            agent = create_deep_agent(
                model=chat_base_model,
                system_prompt=intent_system_prompt,
                subagents=[],  # 意图识别不需要子智能体
                tools=[],  # 意图识别不需要特殊工具
            )

            log.info("✅ 意图识别智能体初始化成功")
            return agent

        except Exception as e:
            log.error(f"❌ 意图识别智能体初始化失败: {e}")
            raise RuntimeError(f"意图识别智能体初始化失败: {e}")

    def _init_intent_mappings(self) -> Dict[str, Dict[str, Any]]:
        """初始化意图映射配置"""
        return {
            "task": {
                "keywords": ["任务", "执行", "检查", "陈列", "库存", "盘点"],
                "description": "任务执行相关",
                "default_result": {
                    "type": "task",
                    "title": "任务执行",
                    "description": "执行冰柜陈列检查、库存管理等任务",
                    "agent": "task-agent"
                }
            },
            "purchase": {
                "keywords": ["采购", "购买", "进货", "供应商"],
                "description": "采购管理相关",
                "default_result": {
                    "type": "purchase",
                    "title": "商品采购",
                    "description": "商品采购、供应商管理、采购策略制定",
                    "agent": "purchase-agent"
                }
            },
            "search": {
                "keywords": ["搜索", "查询", "信息"],
                "description": "信息搜索相关",
                "default_result": {
                    "type": "search",
                    "title": "信息搜索",
                    "description": "信息搜索、市场调研、数据分析",
                    "agent": "search-agent"
                }
            },
            "general": {
                "keywords": ["对话", "聊天", "帮助", "其他"],
                "description": "通用对话相关",
                "default_result": {
                    "type": "general",
                    "title": "通用对话",
                    "description": "通用对话和问答",
                    "agent": "main-agent"
                }
            }
        }

    async def recognize_intent(
            self,
            user_input: str,
            result_set: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        识别用户意图并从结果集中选择最佳匹配
        """
        try:
            log.info(f"🎯 开始意图识别: user_input={user_input[:50]}...")

            # 如果没有提供结果集，使用默认结果集
            if result_set is None:
                result_set = self._get_default_result_set()

            # 构建意图识别提示
            intent_prompt = self._build_intent_prompt(user_input, result_set)

            # 调用大模型进行意图识别
            result = await self.agent(intent_prompt, result_set=result_set, user_input=user_input)

            # 解析大模型结果
            if hasattr(result, 'content'):
                response_text = result.content
            elif isinstance(result, dict) and 'content' in result:
                response_text = result['content']
            else:
                response_text = str(result)

            # 提取选择的结果
            selected_result = self._extract_selected_result(response_text, result_set)
            confidence = self._extract_confidence(response_text)

            # 确保返回有效结果
            if not selected_result and result_set:
                selected_result = result_set[0]
                confidence = 0.3
                log.warning("⚠️ 大模型未返回有效结果，使用默认选项")

            log.info(f"✅ 大模型意图识别完成: selected={selected_result.get('title') if selected_result else 'None'}, confidence={confidence:.2f}")

            return {
                "intent": "recognized",
                "selected_result": selected_result,
                "confidence": confidence,
                "message": f"大模型意图识别完成，置信度: {confidence:.2f}",
                "result_set_size": len(result_set),
                "user_input": user_input,
                "matching_method": "llm_reasoning",
                "llm_response": response_text
            }

        except Exception as e:
            log.error(f"❌ 意图识别失败: {e}")
            return {
                "intent": "error",
                "selected_result": None,
                "confidence": 0.0,
                "message": f"意图识别失败: {str(e)}",
                "error": str(e)
            }

    def _get_default_result_set(self) -> List[Dict[str, Any]]:
        """获取默认结果集"""
        return [mapping["default_result"] for mapping in self.intent_mappings.values()]

    def _build_intent_prompt(self, user_input: str, result_set: List[Dict[str, Any]]) -> str:
        """构建意图识别提示"""
        result_descriptions = []
        for i, result in enumerate(result_set, 1):
            result_descriptions.append(
                f"{i}. **{result.get('title', '未知')}** (类型: {result.get('type', 'unknown')})\n"
                f"   描述: {result.get('description', '无描述')}"
            )

        prompt = f"""你是一个专业的意图识别助手。请仔细分析用户输入，并从给定的结果集中选择最匹配的选项。

**用户输入：**
{user_input}

**可选结果：**
{chr(10).join(result_descriptions)}

**请按照以下格式回复：**
选择结果：[数字]
选择理由：[具体说明为什么选择这个选项]
置信度：[0.1-1.0之间的数值]"""

        return prompt

    def _extract_selected_result(self, response_text: str, result_set: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """从大模型响应中提取选择的结果"""
        try:
            import re

            # 查找选择结果
            patterns = [
                r'选择结果[：:]\s*(\d+)',
                r'选择[：:]\s*(\d+)',
                r'(\d+)\.**',
                r'选项\s*(\d+)',
            ]

            selected_value = None
            for pattern in patterns:
                match = re.search(pattern, response_text)
                if match:
                    selected_value = match.group(1)
                    break

            if selected_value and selected_value.isdigit():
                index = int(selected_value) - 1
                if 0 <= index < len(result_set):
                    return result_set[index]

            # 如果都失败了，返回第一个结果
            return result_set[0] if result_set else None

        except Exception as e:
            log.error(f"提取选择结果失败: {e}")
            return result_set[0] if result_set else None

    def _extract_confidence(self, response_text: str) -> float:
        """从大模型响应中提取置信度"""
        try:
            import re

            # 查找置信度
            confidence_match = re.search(r'置信度[：:]\s*([\d.]+)', response_text)
            if confidence_match:
                confidence = float(confidence_match.group(1))
                return min(max(confidence, 0.0), 1.0)

            # 默认置信度
            return 0.7

        except Exception as e:
            log.error(f"提取置信度失败: {e}")
            return 0.5


# 创建全局实例
intent_recognition_agent = IntentRecognitionAgent()
