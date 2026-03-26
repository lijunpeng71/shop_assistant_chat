"""
意图识别智能体 - 基于LangChain DeepAgents
"""

from typing import Dict, Any, List, Optional
from deepagents import create_deep_agent
from llm.client import llm_client
from core.logger import get_logger

log = get_logger(__name__)


class IntentRecognitionAgent:
    """意图识别智能体 - 负责识别用户意图并选择合适的处理方案"""
    
    def __init__(self):
        """初始化意图识别智能体"""
        self.agent = self._create_agent()
        self.intent_mappings = self._init_intent_mappings()
    
    def _create_agent(self):
        """创建意图识别智能体"""
        
        # 意图识别系统提示
        intent_system_prompt = """你是一个专业的意图识别助手。你的职责是：

1. **分析用户输入** - 理解用户的具体需求和意图
2. **匹配预定义结果集** - 从给定的候选结果集中选择最合适的答案
3. **返回最佳匹配** - 返回选择的结果和置信度

工作流程：
- 接收用户输入和预定义的结果集
- 分析用户意图和语义
- 从结果集中选择最匹配的选项
- 返回选择结果和置信度评分

重要原则：
- 必须从给定的结果集中选择答案
- 基于语义相似度和用户需求进行匹配
- 提供置信度评分帮助决策
- 如果没有合适的匹配，选择最接近的选项

请始终以客观、准确的方式进行意图识别和匹配。"""
        
        try:
            # 获取模型信息
            model_info = llm_client.get_model_info()
            model_id = model_info.get('model_id', 'gpt-3.5-turbo')
            
            # 如果是复杂的模型名称，使用简单的默认名称
            if '/' in model_id:
                model_id = 'gpt-3.5-turbo'
            
            # 创建DeepAgents意图识别智能体
            agent = create_deep_agent(
                model=model_id,
                system_prompt=intent_system_prompt,
                subagents=[],  # 意图识别不需要子智能体
                tools=[],      # 意图识别不需要特殊工具
            )
            
            log.info("✅ 意图识别智能体初始化成功")
            return agent
            
        except Exception as e:
            log.error(f"❌ 意图识别智能体初始化失败: {e}")
            # 如果DeepAgents初始化失败，抛出异常而不是使用mock
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
                "keywords": ["搜索", "查询", "信息", "市场", "数据"],
                "description": "信息搜索相关",
                "default_result": {
                    "type": "search",
                    "title": "信息搜索", 
                    "description": "信息搜索、市场调研、数据分析",
                    "agent": "search-agent"
                }
            },
            "general": {
                "keywords": ["帮助", "你好", "介绍"],
                "description": "一般对话",
                "default_result": {
                    "type": "general",
                    "title": "一般对话",
                    "description": "一般性对话和帮助",
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
        
        Args:
            user_input: 用户输入文本
            result_set: 预定义的结果集，如果为None则使用默认结果集
            
        Returns:
            意图识别结果，包含选择的答案和置信度
        """
        try:
            log.info(f"🎯 开始意图识别: user_input={user_input[:50]}...")
            
            # 如果没有提供结果集，使用默认结果集
            if result_set is None:
                result_set = self._get_default_result_set()
            
            # 构建意图识别提示
            intent_prompt = self._build_intent_prompt(user_input, result_set)
            
            # 调用大模型进行意图识别
            try:
                # DeepAgents返回的是一个图对象，需要使用正确的调用方式
                if hasattr(self.agent, 'ainvoke'):
                    result = await self.agent.ainvoke({"messages": [{"role": "user", "content": intent_prompt}]})
                elif hasattr(self.agent, 'invoke'):
                    result = self.agent.invoke({"messages": [{"role": "user", "content": intent_prompt}]})
                else:
                    # 尝试直接调用
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
                
            except Exception as llm_error:
                log.error(f"❌ 大模型意图识别失败: {llm_error}")
                # 如果大模型失败，抛出异常
                raise RuntimeError(f"大模型意图识别失败: {llm_error}")
            
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
            keywords_str = ", ".join(result.get('keywords', []))
            result_descriptions.append(
                f"{i}. **{result.get('title', '未知')}** (类型: {result.get('type', 'unknown')})\n"
                f"   描述: {result.get('description', '无描述')}\n"
                f"   关键词: {keywords_str}"
            )
        
        prompt = f"""你是一个专业的意图识别助手。请仔细分析用户输入，并从给定的结果集中选择最匹配的选项。

**用户输入：**
"{user_input}"

**候选结果集：**
{chr(10).join(result_descriptions)}

**分析步骤：**
1. 理解用户的主要意图和需求
2. 识别用户输入中的关键词
3. 对比每个选项的关键词和描述
4. 选择最匹配的选项

**重要提醒：**
- 必须从上述1-{len(result_set)}个选项中选择一个
- 不要选择默认选项，要根据用户实际需求选择
- 如果用户提到"采购"、"购买"、"进货"等，选择采购相关选项
- 如果用户提到"搜索"、"查询"、"信息"等，选择搜索相关选项
- 如果用户提到"任务"、"执行"、"检查"等，选择任务相关选项
- 如果用户只是打招呼或询问功能，选择一般对话选项

**请严格按照以下格式回答：**
选择结果：[数字]
选择理由：[具体说明为什么选择这个选项]
置信度：[0.1-1.0之间的数值]"""
        
        return prompt
    
    def _extract_selected_result(self, response_text: str, result_set: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """从大模型响应中提取选择的结果"""
        try:
            import re
            
            # 查找选择结果 - 支持多种格式
            patterns = [
                r'选择结果[：:]\s*(\d+)',  # 选择结果：2
                r'选择结果[：:]\s*(\d+)\.',  # 选择结果：2.
                r'选择结果[：:]\s*选项(\d+)',  # 选择结果：选项2
                r'选择结果[：:]\s*(\d+)[^\d]',  # 选择结果：2后面跟非数字
                r'(\d+)\.**',  # 2.**
                r'选项\s*(\d+)',  # 选项2
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
                    log.info(f"成功提取选择结果: 选项{selected_value} -> 索引{index}")
                    return result_set[index]
            
            # 如果数字提取失败，尝试关键词匹配
            keywords_map = {
                '任务': 'task',
                '采购': 'purchase', 
                '搜索': 'search',
                '一般': 'general',
                '对话': 'general'
            }
            
            for keyword, intent_type in keywords_map.items():
                if keyword in response_text:
                    for result in result_set:
                        if result.get('type') == intent_type:
                            log.info(f"通过关键词匹配选择结果: {keyword} -> {intent_type}")
                            return result
            
            # 如果都失败了，返回第一个结果
            log.warning("无法提取选择结果，返回默认选项")
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
                return min(max(confidence, 0.0), 1.0)  # 确保在0-1范围内
            
            # 默认置信度
            return 0.7
            
        except Exception as e:
            log.error(f"提取置信度失败: {e}")
            return 0.5
    
    def _fallback_to_keyword_matching(self, user_input: str, result_set: List[Dict[str, Any]]) -> Dict[str, Any]:
        """回退到关键词匹配"""
        log.warning("⚠️ 回退到关键词匹配模式")
        
        user_lower = user_input.lower()
        best_match = None
        best_score = 0
        
        for result in result_set:
            score = 0
            title = result.get('title', '').lower()
            description = result.get('description', '').lower()
            
            # 计算关键词匹配分数
            for intent_name, intent_config in self.intent_mappings.items():
                if intent_config["default_result"].get('type') == result.get('type'):
                    for keyword in intent_config["keywords"]:
                        if keyword in user_lower:
                            score += 1
                            break
            
            if score > best_score:
                best_score = score
                best_match = result
        
        confidence = min(best_score / 3.0, 0.8)  # 标准化置信度
        
        return {
            "intent": "keyword_matched",
            "selected_result": best_match,
            "confidence": confidence,
            "message": f"基于关键词匹配选择结果，置信度: {confidence}",
            "result_set_size": len(result_set),
            "user_input": user_input
        }


# 创建全局实例
intent_recognition_agent = IntentRecognitionAgent()
