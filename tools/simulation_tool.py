"""
通用模拟工具 - 处理所有模拟操作
"""

from typing import Dict, Any
from core.logger import get_logger

log = get_logger(__name__)


class SimulationTool:
    """通用模拟工具类"""
    
    def __init__(self):
        """初始化模拟工具"""
        pass
    
    async def simulate_task_response(self, message: str, user_id: str = None, response_type: str = "auto") -> Dict[str, Any]:
        """
        模拟任务响应
        
        Args:
            message: 用户消息
            user_id: 用户ID
            response_type: 响应类型（auto/task/purchase/search/general）
            
        Returns:
            模拟响应结果
        """
        try:
            message_lower = message.lower()
            
            if response_type == "auto":
                # 自动识别响应类型
                if any(keyword in message_lower for keyword in ["任务", "执行", "检查", "陈列"]):
                    response_type = "task"
                elif any(keyword in message_lower for keyword in ["采购", "购买", "进货"]):
                    response_type = "purchase"
                elif any(keyword in message_lower for keyword in ["搜索", "查询", "信息"]):
                    response_type = "search"
                else:
                    response_type = "general"
            
            # 根据响应类型生成模拟结果
            if response_type == "task":
                return await self._simulate_task_execution(message, user_id)
            elif response_type == "purchase":
                return await self._simulate_purchase_analysis(message, user_id)
            elif response_type == "search":
                return await self._simulate_search_result(message, user_id)
            else:
                return await self._simulate_general_response(message, user_id)
                
        except Exception as e:
            log.error(f"❌ 模拟响应失败: {e}")
            return {
                "type": "error",
                "message": f"模拟响应失败: {str(e)}",
                "data": {"error": str(e)}
            }
    
    async def _simulate_task_execution(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """模拟任务执行"""
        # 使用红包工具进行任务模拟
        from tools.redpacket_tool import simulate_task_execution
        
        return await simulate_task_execution(user_id or "sim_user", message, "general")
    
    async def _simulate_purchase_analysis(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """模拟采购分析"""
        message_lower = message.lower()
        
        # 分析采购需求
        if any(keyword in message_lower for keyword in ["饮料", "可乐", "雪碧"]):
            recommendations = ["可乐", "雪碧", "果汁"]
            increase = "20%"
            analysis = "饮料类商品需求旺盛，建议增加采购量"
        elif any(keyword in message_lower for keyword in ["零食", "薯片", "饼干"]):
            recommendations = ["薯片", "饼干", "坚果"]
            increase = "15%"
            analysis = "零食类商品销售稳定，建议保持现有采购水平"
        else:
            recommendations = ["可乐", "雪碧", "薯片", "饼干"]
            increase = "15%"
            analysis = "根据销售数据分析，建议增加热销商品采购量"
        
        return {
            "type": "purchase",
            "message": f"模拟采购分析：关于'{message}'的采购需求已分析。{analysis}。建议增加{recommendations}等商品的采购量，预计可提升销售额{increase}。",
            "data": {
                "recommendations": recommendations,
                "estimated_increase": increase,
                "analysis": analysis,
                "user_id": user_id
            }
        }
    
    async def _simulate_search_result(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """模拟搜索结果"""
        message_lower = message.lower()
        
        # 分析搜索需求
        if any(keyword in message_lower for keyword in ["市场", "趋势"]):
            search_results = "市场调研显示，当前饮料市场增长稳定，消费者对健康饮品需求增加"
            trend = "上升"
        elif any(keyword in message_lower for keyword in ["价格", "成本"]):
            search_results = "价格分析显示，原材料成本略有上涨，建议优化采购策略以控制成本"
            trend = "稳定"
        else:
            search_results = "根据最新数据，市场趋势向好，建议抓住机会扩大业务"
            trend = "向好"
        
        return {
            "type": "search",
            "message": f"模拟搜索结果：关于'{message}'的相关信息已获取。{search_results}。",
            "data": {
                "search_results": search_results,
                "trend": trend,
                "user_id": user_id
            }
        }
    
    async def _simulate_general_response(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """模拟一般响应"""
        return {
            "type": "general",
            "message": f"模拟回答：关于'{message}'的问题，我理解您的需求。由于LLM未配置，当前使用模拟模式，建议配置LLM以获得更好的体验。",
            "data": {
                "user_id": user_id,
                "simulation_mode": True
            }
        }
    
    def get_suggestions(self, response_type: str) -> list:
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


# 创建模拟工具实例
simulation_tool = SimulationTool()


# 定义模拟工具函数（供DeepAgents使用）
async def simulate_response(message: str, user_id: str = None, response_type: str = "auto") -> Dict[str, Any]:
    """
    模拟响应工具函数
    
    Args:
        message: 用户消息
        user_id: 用户ID（必须提供，不从header获取）
        response_type: 响应类型
        
    Returns:
        模拟响应结果
    """
    if not user_id:
        return {
            "type": "error",
            "message": "缺少用户ID，无法进行模拟",
            "data": {"error": "Missing user_id"}
        }
    
    return await simulation_tool.simulate_task_response(message, user_id, response_type)


async def simulate_task(message: str, user_id: str = None) -> Dict[str, Any]:
    """
    模拟任务执行
    
    Args:
        message: 用户消息
        user_id: 用户ID（必须提供，不从header获取）
        
    Returns:
        任务执行结果
    """
    if not user_id:
        return {
            "type": "error",
            "message": "缺少用户ID，无法进行模拟",
            "data": {"error": "Missing user_id"}
        }
    
    return await simulation_tool._simulate_task_execution(message, user_id)


async def simulate_purchase(message: str, user_id: str = None) -> Dict[str, Any]:
    """
    模拟采购分析
    
    Args:
        message: 用户消息
        user_id: 用户ID（必须提供，不从header获取）
        
    Returns:
        采购分析结果
    """
    if not user_id:
        return {
            "type": "error",
            "message": "缺少用户ID，无法进行模拟",
            "data": {"error": "Missing user_id"}
        }
    
    return await simulation_tool._simulate_purchase_analysis(message, user_id)


async def simulate_search(message: str, user_id: str = None) -> Dict[str, Any]:
    """
    模拟搜索结果
    
    Args:
        message: 用户消息
        user_id: 用户ID（必须提供，不从header获取）
        
    Returns:
        搜索结果
    """
    if not user_id:
        return {
            "type": "error",
            "message": "缺少用户ID，无法进行模拟",
            "data": {"error": "Missing user_id"}
        }
    
    return await simulation_tool._simulate_search_result(message, user_id)


# 工具定义（供DeepAgents使用）
simulation_tools = [
    {
        "name": "simulate_response",
        "description": "模拟智能体响应",
        "function": simulate_response,
        "parameters": {
            "message": {"type": "string", "description": "用户消息"},
            "user_id": {"type": "string", "description": "用户ID"},
            "response_type": {"type": "string", "description": "响应类型"}
        }
    },
    {
        "name": "simulate_task",
        "description": "模拟任务执行",
        "function": simulate_task,
        "parameters": {
            "message": {"type": "string", "description": "用户消息"},
            "user_id": {"type": "string", "description": "用户ID"}
        }
    },
    {
        "name": "simulate_purchase",
        "description": "模拟采购分析",
        "function": simulate_purchase,
        "parameters": {
            "message": {"type": "string", "description": "用户消息"},
            "user_id": {"type": "string", "description": "用户ID"}
        }
    },
    {
        "name": "simulate_search",
        "description": "模拟搜索结果",
        "function": simulate_search,
        "parameters": {
            "message": {"type": "string", "description": "用户消息"},
            "user_id": {"type": "string", "description": "用户ID"}
        }
    }
]
