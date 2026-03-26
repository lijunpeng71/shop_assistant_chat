"""
所有可用工具的集合 - 供智能体自主选择使用
"""

from tools.bing_search import bing_search_tool
from tools.redpacket_tool import redpacket_tools
from tools.simulation_tool import simulation_tools

# 所有可用工具的完整列表
all_available_tools = {
    # 搜索工具
    "bing_search": bing_search_tool,
    
    # 红包工具
    "send_redpacket": redpacket_tools[0] if len(redpacket_tools) > 0 else None,
    "calculate_and_send_reward": redpacket_tools[1] if len(redpacket_tools) > 1 else None,
    "simulate_task_execution": redpacket_tools[2] if len(redpacket_tools) > 2 else None,
    
    # 模拟工具
    "simulate_response": simulation_tools[0] if len(simulation_tools) > 0 else None,
    "simulate_task": simulation_tools[1] if len(simulation_tools) > 1 else None,
    "simulate_purchase": simulation_tools[2] if len(simulation_tools) > 2 else None,
    "simulate_search": simulation_tools[3] if len(simulation_tools) > 3 else None,
}

# 工具描述映射
tool_descriptions = {
    "bing_search": "用于搜索网络信息、市场数据、价格趋势等",
    "send_redpacket": "用于发送红包奖励给用户",
    "calculate_and_send_reward": "用于计算并发送任务奖励",
    "simulate_task_execution": "用于模拟任务执行（包含红包发放）",
    "simulate_response": "用于模拟智能体响应",
    "simulate_task": "用于模拟任务执行",
    "simulate_purchase": "用于模拟采购分析",
    "simulate_search": "用于模拟搜索结果",
}

# 获取所有可用工具的函数
def get_all_tools():
    """获取所有可用工具列表"""
    tools = []
    for name, tool in all_available_tools.items():
        if tool is not None:
            tools.append(tool)
    return tools

# 获取工具描述的函数
def get_tool_descriptions():
    """获取工具描述映射"""
    return tool_descriptions

# 根据名称获取工具的函数
def get_tool_by_name(name):
    """根据工具名称获取工具"""
    return all_available_tools.get(name)

# 根据用途获取推荐工具的函数
def get_recommended_tools_for_task(task_type):
    """根据任务类型获取推荐工具"""
    recommendations = {
        "task": ["simulate_task_execution", "calculate_and_send_reward", "simulate_task"],
        "purchase": ["bing_search", "simulate_purchase"],
        "search": ["bing_search", "simulate_search"],
        "general": ["simulate_response"],
        "reward": ["send_redpacket", "calculate_and_send_reward"],
        "simulation": ["simulate_response", "simulate_task", "simulate_purchase", "simulate_search"]
    }
    
    return recommendations.get(task_type, [])

# 工具使用指导
tool_usage_guidance = """
工具使用指导：

1. **搜索工具 (bing_search)**
   - 用途：获取实时网络信息、市场数据、价格趋势
   - 使用时机：当需要外部信息支持分析时

2. **红包工具 (send_redpacket, calculate_and_send_reward)**
   - 用途：发送红包奖励给用户
   - 使用时机：任务完成后需要发放奖励时

3. **模拟工具 (simulate_*)**
   - 用途：当LLM未配置或需要模拟时使用
   - 使用时机：无法正常调用LLM或需要模拟响应时

重要原则：
- 根据实际需要选择工具，不要主动使用
- 优先使用LLM直接回答，必要时才使用工具
- 工具是用来增强能力，不是替代思考
"""
