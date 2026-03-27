"""
任务相关工具
"""

from typing import List, Dict, Any
from core.logger import get_logger

log = get_logger(__name__)


class TaskTools:
    """任务工具类"""
    
    @staticmethod
    def get_available_tasks() -> List[Dict[str, Any]]:
        """
        获取当前可用的任务列表
        
        Returns:
            任务列表，包含任务名称、描述、类型等信息
        """
        tasks = [
            {
                "id": "freezer_check",
                "name": "冰柜陈列检查",
                "description": "检查冰柜商品陈列情况，确保商品摆放规范、价格标签正确、库存充足",
                "category": "task",
                "keywords": ["冰柜", "陈列", "检查", "摆放", "价格标签"],
                "requires_image": True,
                "estimated_time": "15-30分钟",
                "priority": "high"
            },
            {
                "id": "inventory_management",
                "name": "库存管理",
                "description": "管理商品库存，包括库存盘点、库存预警、补货建议等",
                "category": "task",
                "keywords": ["库存", "盘点", "补货", "库存预警", "库存管理"],
                "requires_image": False,
                "estimated_time": "10-20分钟",
                "priority": "medium"
            },
            {
                "id": "product_purchase",
                "name": "商品采购",
                "description": "进行商品采购，包括供应商选择、价格谈判、订单管理等",
                "category": "purchase",
                "keywords": ["采购", "购买", "进货", "供应商", "订单"],
                "requires_image": False,
                "estimated_time": "20-40分钟",
                "priority": "high"
            },
            {
                "id": "supplier_management",
                "name": "供应商管理",
                "description": "管理供应商信息，包括供应商评估、合同管理、绩效跟踪等",
                "category": "purchase",
                "keywords": ["供应商", "供货商", "合同", "评估", "绩效"],
                "requires_image": False,
                "estimated_time": "15-30分钟",
                "priority": "medium"
            },
            {
                "id": "market_research",
                "name": "市场调研",
                "description": "进行市场信息搜索和数据分析，包括竞品分析、价格调研、趋势分析等",
                "category": "search",
                "keywords": ["市场", "调研", "搜索", "数据分析", "竞品", "趋势"],
                "requires_image": False,
                "estimated_time": "30-60分钟",
                "priority": "medium"
            },
            {
                "id": "price_analysis",
                "name": "价格分析",
                "description": "分析商品价格信息，包括价格对比、价格趋势、定价建议等",
                "category": "search",
                "keywords": ["价格", "分析", "对比", "定价", "趋势"],
                "requires_image": False,
                "estimated_time": "20-30分钟",
                "priority": "medium"
            },
            {
                "id": "sales_data_analysis",
                "name": "销售数据分析",
                "description": "分析销售数据，包括销售趋势、热销商品、客户偏好等",
                "category": "search",
                "keywords": ["销售", "数据", "分析", "趋势", "热销", "客户"],
                "requires_image": False,
                "estimated_time": "25-45分钟",
                "priority": "medium"
            }
        ]
        
        log.info(f"📋 获取可用任务列表: 共{len(tasks)}个任务")
        return tasks
    
    @staticmethod
    def get_task_by_id(task_id: str) -> Dict[str, Any]:
        """
        根据任务ID获取任务详情
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务详情，如果未找到返回None
        """
        tasks = TaskTools.get_available_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                log.info(f"📋 根据ID找到任务: {task.get('name')}")
                return task
        
        log.warning(f"⚠️ 未找到任务ID: {task_id}")
        return None
    
    @staticmethod
    def search_tasks(keyword: str) -> List[Dict[str, Any]]:
        """
        根据关键词搜索任务
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的任务列表
        """
        tasks = TaskTools.get_available_tasks()
        keyword_lower = keyword.lower()
        
        matched_tasks = []
        for task in tasks:
            # 在任务名称、描述和关键词中搜索
            if (keyword_lower in task.get("name", "").lower() or 
                keyword_lower in task.get("description", "").lower() or
                any(keyword_lower in kw.lower() for kw in task.get("keywords", []))):
                matched_tasks.append(task)
        
        log.info(f"🔍 关键词'{keyword}'搜索到{len(matched_tasks)}个任务")
        return matched_tasks
    
    @staticmethod
    def get_tasks_by_category(category: str) -> List[Dict[str, Any]]:
        """
        根据分类获取任务
        
        Args:
            category: 任务分类 (task, purchase, search)
            
        Returns:
            指定分类的任务列表
        """
        tasks = TaskTools.get_available_tasks()
        category_tasks = [task for task in tasks if task.get("category") == category]
        
        log.info(f"📂 分类'{category}'包含{len(category_tasks)}个任务")
        return category_tasks
    
    @staticmethod
    def format_tasks_for_display(tasks: List[Dict[str, Any]]) -> str:
        """
        格式化任务列表用于显示
        
        Args:
            tasks: 任务列表
            
        Returns:
            格式化的任务描述字符串
        """
        if not tasks:
            return "未找到相关任务。"
        
        formatted_text = "📋 **可用任务列表**\n\n"
        
        for i, task in enumerate(tasks, 1):
            formatted_text += f"**{i}. {task.get('name')}**\n"
            formatted_text += f"   📝 {task.get('description')}\n"
            formatted_text += f"   ⏱️ 预计耗时: {task.get('estimated_time')}\n"
            formatted_text += f"   🏷️ 分类: {task.get('category')}\n"
            formatted_text += f"   📸 需要图片: {'是' if task.get('requires_image') else '否'}\n"
            formatted_text += f"   🔑 关键词: {', '.join(task.get('keywords', []))}\n\n"
        
        return formatted_text


# 创建工具实例
task_tools = TaskTools()
