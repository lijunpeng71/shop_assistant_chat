"""
红包工具 - 用于发送红包奖励
"""

from typing import Dict, Any, Optional
from core.logger import get_logger

log = get_logger(__name__)


class RedPacketTool:
    """红包工具类"""
    
    def __init__(self):
        """初始化红包工具"""
        self.redpacket_api_url = "https://api.redpacket.example.com/send"  # 模拟API地址
        self.api_key = "redpacket_api_key_12345"  # 模拟API密钥
    
    async def send_redpacket(self, user_id: str, amount: float, reason: str, task_type: str = "general") -> Dict[str, Any]:
        """
        发送红包
        
        Args:
            user_id: 用户ID
            amount: 红包金额
            reason: 发送原因
            task_type: 任务类型
            
        Returns:
            发送结果
        """
        try:
            log.info(f"🧧 准备发送红包: user_id={user_id}, amount={amount}, reason={reason}")
            
            # 构建红包数据
            redpacket_data = {
                "user_id": user_id,
                "amount": amount,
                "reason": reason,
                "task_type": task_type,
                "timestamp": self._get_timestamp(),
                "signature": self._generate_signature(user_id, amount, reason)
            }
            
            # 调用红包API（模拟）
            result = await self._call_redpacket_api(redpacket_data)
            
            if result.get("success"):
                log.info(f"✅ 红包发送成功: {result.get('redpacket_id')}")
                return {
                    "success": True,
                    "redpacket_id": result.get("redpacket_id"),
                    "amount": amount,
                    "user_id": user_id,
                    "reason": reason,
                    "status": "sent",
                    "message": f"成功发送{amount}元红包给用户{user_id}"
                }
            else:
                log.error(f"❌ 红包发送失败: {result.get('error')}")
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "amount": amount,
                    "user_id": user_id,
                    "reason": reason,
                    "status": "failed",
                    "message": f"红包发送失败: {result.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            log.error(f"❌ 红包发送异常: {e}")
            return {
                "success": False,
                "error": str(e),
                "amount": amount,
                "user_id": user_id,
                "reason": reason,
                "status": "error",
                "message": f"红包发送异常: {str(e)}"
            }
    
    async def _call_redpacket_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用红包API（模拟）
        
        Args:
            data: 请求数据
            
        Returns:
            API响应结果
        """
        # 模拟API调用
        import asyncio
        await asyncio.sleep(0.1)  # 模拟网络延迟
        
        # 模拟成功响应
        import uuid
        redpacket_id = f"RP_{uuid.uuid4().hex[:8]}"
        
        return {
            "success": True,
            "redpacket_id": redpacket_id,
            "amount": data["amount"],
            "user_id": data["user_id"],
            "message": "红包发送成功"
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        import time
        return str(int(time.time()))
    
    def _generate_signature(self, user_id: str, amount: float, reason: str) -> str:
        """
        生成签名（模拟）
        
        Args:
            user_id: 用户ID
            amount: 金额
            reason: 原因
            
        Returns:
            签名字符串
        """
        import hashlib
        import hmac
        
        # 模拟签名生成
        sign_string = f"{user_id}_{amount}_{reason}_{self._get_timestamp()}"
        signature = hmac.new(
            self.api_key.encode(),
            sign_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def calculate_reward(self, task_type: str, performance_score: float, base_amount: float = 8.8) -> float:
        """
        计算奖励金额
        
        Args:
            task_type: 任务类型
            performance_score: 绩效评分 (0-100)
            base_amount: 基础金额
            
        Returns:
            计算后的奖励金额
        """
        # 根据任务类型调整系数
        task_multipliers = {
            "inventory_check": 1.2,      # 库存盘点
            "freezer_inspection": 1.0,   # 冰柜检查
            "sales_analysis": 1.1,        # 销售分析
            "general_task": 0.9,          # 一般任务
            "purchase_task": 1.3         # 采购任务
        }
        
        multiplier = task_multipliers.get(task_type, 1.0)
        
        # 根据绩效评分调整金额
        if performance_score >= 90:
            performance_bonus = 1.5  # 优秀表现
        elif performance_score >= 80:
            performance_bonus = 1.2  # 良好表现
        elif performance_score >= 70:
            performance_bonus = 1.0  # 标准表现
        else:
            performance_bonus = 0.8  # 需要改进
        
        final_amount = base_amount * multiplier * performance_bonus
        
        # 确保金额在合理范围内
        final_amount = max(1.0, min(final_amount, 50.0))
        
        # 保留一位小数
        return round(final_amount, 1)
    
    def analyze_task(self, message: str, task_type: str = "general") -> Dict[str, Any]:
        """
        分析任务并生成模拟结果
        
        Args:
            message: 用户消息
            task_type: 任务类型
            
        Returns:
            任务分析结果
        """
        message_lower = message.lower()
        
        # 分析任务类型
        if any(keyword in message_lower for keyword in ["库存", "盘点"]):
            analyzed_task_type = "inventory_check"
            performance_score = 88
            result_description = "经检查，库存管理良好，商品摆放有序，建议发放奖励。"
            execution_details = {
                "total_items": 156,
                "expiring_items": 3,
                "display_compliance": "95%"
            }
        elif any(keyword in message_lower for keyword in ["冰柜", "陈列", "检查"]):
            analyzed_task_type = "freezer_inspection"
            performance_score = 85
            result_description = "经检查，冰柜陈列符合标准，商品可见性良好，建议发放奖励。"
            execution_details = {
                "layout_score": 85,
                "visibility_score": 90,
                "brand_distribution": "良好"
            }
        elif any(keyword in message_lower for keyword in ["销售", "数据", "分析"]):
            analyzed_task_type = "sales_analysis"
            performance_score = 82
            result_description = "经分析，销售数据呈现良好趋势，增长稳定，建议发放奖励。"
            execution_details = {
                "sales_growth": "15%",
                "top_products": ["可乐", "雪碧"],
                "trend_analysis": "上升"
            }
        elif any(keyword in message_lower for keyword in ["采购", "购买", "进货"]):
            analyzed_task_type = "purchase_task"
            performance_score = 90
            result_description = "经分析，采购策略合理，成本控制有效，建议发放奖励。"
            execution_details = {
                "cost_savings": "8%",
                "supplier_performance": "优秀",
                "inventory_optimization": "良好"
            }
        else:
            analyzed_task_type = task_type
            performance_score = 80
            result_description = "任务执行完成，表现良好，建议发放奖励。"
            execution_details = {
                "completion_rate": "100%",
                "quality_score": "良好",
                "efficiency": "高"
            }
        
        # 计算建议奖励金额
        suggested_reward = self.calculate_reward(analyzed_task_type, performance_score)
        
        return {
            "task_type": analyzed_task_type,
            "performance_score": performance_score,
            "result_description": result_description,
            "execution_details": execution_details,
            "suggested_reward": suggested_reward
        }


# 创建红包工具实例
redpacket_tool = RedPacketTool()


# 定义红包工具函数（供DeepAgents使用）
async def send_redpacket(user_id: str, amount: float, reason: str, task_type: str = "general") -> Dict[str, Any]:
    """
    发送红包工具函数
    
    Args:
        user_id: 用户ID
        amount: 红包金额
        reason: 发送原因
        task_type: 任务类型
        
    Returns:
        发送结果
    """
    return await redpacket_tool.send_redpacket(user_id, amount, reason, task_type)


async def calculate_and_send_reward(user_id: str, task_type: str, performance_score: float, task_description: str) -> Dict[str, Any]:
    """
    计算并发送奖励
    
    Args:
        user_id: 用户ID
        task_type: 任务类型
        performance_score: 绩效评分
        task_description: 任务描述
        
    Returns:
        发送结果
    """
    # 计算奖励金额
    amount = redpacket_tool.calculate_reward(task_type, performance_score)
    
    # 构建发送原因
    reason = f"{task_description} - 绩效评分: {performance_score}分"
    
    # 发送红包
    return await send_redpacket(user_id, amount, reason, task_type)


async def simulate_task_execution(user_id: str, message: str, task_type: str = "general") -> Dict[str, Any]:
    """
    模拟任务执行（包含红包发放）
    
    Args:
        user_id: 用户ID（必须提供，不从header获取）
        message: 用户消息
        task_type: 任务类型
        
    Returns:
        任务执行结果
    """
    if not user_id:
        return {
            "type": "error",
            "message": "缺少用户ID，无法进行模拟",
            "data": {"error": "Missing user_id"}
        }
    
    try:
        # 分析任务类型和绩效评分
        task_analysis = redpacket_tool.analyze_task(message, task_type)
        
        # 构建任务执行结果
        task_result = {
            "type": "task",
            "message": f"模拟任务执行：关于'{message}'的任务已经完成。{task_analysis['result_description']}",
            "data": {
                "task_completed": True,
                "performance_score": task_analysis["performance_score"],
                "task_type": task_analysis["task_type"],
                "execution_details": task_analysis["execution_details"],
                "reward": task_analysis["suggested_reward"]
            }
        }
        
        # 发送红包
        redpacket_result = await calculate_and_send_reward(
            user_id=user_id,
            task_type=task_analysis["task_type"],
            performance_score=task_analysis["performance_score"],
            task_description=f"模拟任务执行：{message}"
        )
        
        if redpacket_result.get("success"):
            task_result["data"]["redpacket_sent"] = True
            task_result["data"]["redpacket_id"] = redpacket_result.get("redpacket_id")
            task_result["data"]["actual_reward"] = redpacket_result.get("amount")
            task_result["message"] += f"\n\n🎁 **奖励发放**：已成功发放{redpacket_result.get('amount')}元红包（红包ID: {redpacket_result.get('redpacket_id')}）"
        else:
            task_result["data"]["redpacket_sent"] = False
            task_result["data"]["redpacket_error"] = redpacket_result.get("error")
            task_result["message"] += f"\n\n⚠️ **奖励发放失败**：{redpacket_result.get('error')}"
        
        return task_result
        
    except Exception as e:
        return {
            "type": "task",
            "message": f"模拟任务执行失败：{str(e)}",
            "data": {
                "task_completed": False,
                "error": str(e),
                "redpacket_sent": False,
                "redpacket_error": str(e)
            }
        }


# 工具定义（供DeepAgents使用）
redpacket_tools = [
    {
        "name": "send_redpacket",
        "description": "发送红包奖励给用户",
        "function": send_redpacket,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "amount": {"type": "number", "description": "红包金额"},
            "reason": {"type": "string", "description": "发送原因"},
            "task_type": {"type": "string", "description": "任务类型"}
        }
    },
    {
        "name": "calculate_and_send_reward",
        "description": "计算并发送任务奖励",
        "function": calculate_and_send_reward,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "task_type": {"type": "string", "description": "任务类型"},
            "performance_score": {"type": "number", "description": "绩效评分 (0-100)"},
            "task_description": {"type": "string", "description": "任务描述"}
        }
    },
    {
        "name": "simulate_task_execution",
        "description": "模拟任务执行（包含红包发放）",
        "function": simulate_task_execution,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "message": {"type": "string", "description": "用户消息"},
            "task_type": {"type": "string", "description": "任务类型"}
        }
    }
]
