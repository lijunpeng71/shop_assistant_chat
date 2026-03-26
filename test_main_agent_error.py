#!/usr/bin/env python3
"""
测试主智能体错误处理
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.main_deepagent import MainDeepAgent
from core.logger import get_logger

log = get_logger(__name__)


async def test_main_agent_error_handling():
    """测试主智能体错误处理"""
    print("🧪 测试主智能体错误处理")
    print("=" * 50)
    
    try:
        # 尝试创建主智能体
        print("正在创建主智能体...")
        main_agent = MainDeepAgent()
        print("✅ 主智能体创建成功")
        
        # 测试基本功能
        print("\n测试基本功能...")
        result = await main_agent.process_message(
            message="你好",
            user_id="test_user",
            session_id="test_session"
        )
        
        print(f"响应类型: {result.get('type')}")
        print(f"响应消息: {result.get('message', 'No message')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_main_agent_error_handling())
    sys.exit(0 if success else 1)
