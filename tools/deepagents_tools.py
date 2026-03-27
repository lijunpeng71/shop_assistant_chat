"""
DeepAgents工具集成 - 为DeepAgents提供工具调用能力
"""

from typing import List, Dict, Any
from tools.task_tools import task_tools
from core.logger import get_logger

log = get_logger(__name__)


class DeepAgentsTools:
    """DeepAgents工具集成类"""
    
    @staticmethod
    def get_available_tasks() -> Dict[str, Any]:
        """
        获取当前可用任务列表 - 工具函数
        
        Returns:
            包含任务列表的字典，供DeepAgents调用
        """
        try:
            tasks = task_tools.get_available_tasks()
            log.info("🔧 DeepAgents调用get_available_tasks工具")
            return {
                "success": True,
                "tasks": tasks,
                "total": len(tasks)
            }
        except Exception as e:
            log.error(f"❌ get_available_tasks工具调用失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "tasks": []
            }
    
    @staticmethod
    def search_tasks(keyword: str) -> Dict[str, Any]:
        """
        根据关键词搜索任务 - 工具函数
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            包含搜索结果的字典，供DeepAgents调用
        """
        try:
            tasks = task_tools.search_tasks(keyword)
            log.info(f"🔧 DeepAgents调用search_tasks工具，关键词: {keyword}")
            return {
                "success": True,
                "keyword": keyword,
                "tasks": tasks,
                "total": len(tasks)
            }
        except Exception as e:
            log.error(f"❌ search_tasks工具调用失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "keyword": keyword,
                "tasks": []
            }
    
    @staticmethod
    def get_task_details(task_id: str) -> Dict[str, Any]:
        """
        获取任务详情 - 工具函数
        
        Args:
            task_id: 任务ID
            
        Returns:
            包含任务详情的字典，供DeepAgents调用
        """
        try:
            task = task_tools.get_task_by_id(task_id)
            log.info(f"🔧 DeepAgents调用get_task_details工具，任务ID: {task_id}")
            if task:
                # 如果任务需要拍照，在描述中加入提示
                if task.get("requires_image"):
                    task["camera_needed"] = True
                    log.info(f"📸 任务{task_id}需要拍照")
                
                return {
                    "success": True,
                    "task": task
                }
            else:
                return {
                    "success": False,
                    "error": f"未找到任务ID: {task_id}",
                    "task": None
                }
        except Exception as e:
            log.error(f"❌ get_task_details工具调用失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "task": None
            }
    
    @staticmethod
    def get_tasks_by_category(category: str) -> Dict[str, Any]:
        """
        根据分类获取任务 - 工具函数
        
        Args:
            category: 任务分类 (task, purchase, search)
            
        Returns:
            包含分类任务的字典，供DeepAgents调用
        """
        try:
            tasks = task_tools.get_tasks_by_category(category)
            log.info(f"🔧 DeepAgents调用get_tasks_by_category工具，分类: {category}")
            return {
                "success": True,
                "category": category,
                "tasks": tasks,
                "total": len(tasks)
            }
        except Exception as e:
            log.error(f"❌ get_tasks_by_category工具调用失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "category": category,
                "tasks": []
            }


# 创建工具实例
deepagents_tools = DeepAgentsTools()

# 定义DeepAgents可用的工具函数
DEEPAGENTS_TOOLS = [
    {
        "name": "get_available_tasks",
        "description": "获取当前可用的任务列表，包括任务名称、描述、分类等信息",
        "function": deepagents_tools.get_available_tasks,
        "parameters": {}
    },
    {
        "name": "search_tasks", 
        "description": "根据关键词搜索相关任务",
        "function": deepagents_tools.search_tasks,
        "parameters": {
            "keyword": {
                "type": "string",
                "description": "搜索关键词，如'冰柜'、'采购'、'市场调研'等"
            }
        }
    },
    {
        "name": "get_task_details",
        "description": "根据任务ID获取特定任务的详细信息",
        "function": deepagents_tools.get_task_details,
        "parameters": {
            "task_id": {
                "type": "string", 
                "description": "任务ID，如'freezer_check'、'inventory_management'等"
            }
        }
    },
    {
        "name": "get_tasks_by_category",
        "description": "根据分类获取任务列表",
        "function": deepagents_tools.get_tasks_by_category,
        "parameters": {
            "category": {
                "type": "string",
                "description": "任务分类，可选值: 'task'(执行任务), 'purchase'(采购管理), 'search'(信息搜索)"
            }
        }
    }
]
