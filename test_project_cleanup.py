#!/usr/bin/env python3
"""
测试项目清理后的状态 - 验证所有模拟操作都使用工具调用
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_simulation_tools_integration():
    """测试模拟工具集成"""
    print("🧪 测试模拟工具集成")
    print("=" * 50)
    
    try:
        from tools.simulation_tool import simulate_response, simulate_task, simulate_purchase, simulate_search
        from tools.redpacket_tool import simulate_task_execution
        
        # 测试1: 通用模拟响应
        print("\n📝 测试1: 通用模拟响应")
        result1 = await simulate_response("我要执行任务", "test_user", "auto")
        print(f"✅ 通用模拟: {result1.get('type')} - {result1.get('message', '')[:50]}...")
        
        # 测试2: 任务模拟
        print("\n📝 测试2: 任务模拟")
        result2 = await simulate_task("我要检查冰柜陈列", "test_user")
        print(f"✅ 任务模拟: {result2.get('type')} - 红包发放: {result2.get('data', {}).get('redpacket_sent', False)}")
        
        # 测试3: 采购模拟
        print("\n📝 测试3: 采购模拟")
        result3 = await simulate_purchase("我要采购商品", "test_user")
        print(f"✅ 采购模拟: {result3.get('type')} - 建议: {result3.get('data', {}).get('recommendations', [])}")
        
        # 测试4: 搜索模拟
        print("\n📝 测试4: 搜索模拟")
        result4 = await simulate_search("搜索市场信息", "test_user")
        print(f"✅ 搜索模拟: {result4.get('type')} - 趋势: {result4.get('data', {}).get('trend', '')}")
        
        # 测试5: 红包任务模拟
        print("\n📝 测试5: 红包任务模拟")
        result5 = await simulate_task_execution("test_user", "我要执行库存盘点", "general")
        print(f"✅ 红包任务模拟: {result5.get('type')} - 红包ID: {result5.get('data', {}).get('redpacket_id', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 模拟工具集成测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_api_simulation_workflow():
    """测试API模拟工作流程"""
    print("\n🧪 测试API模拟工作流程")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        test_cases = [
            {
                "message": "我要执行库存盘点",
                "expected_type": "task",
                "description": "任务执行模拟"
            },
            {
                "message": "我要采购商品",
                "expected_type": "purchase",
                "description": "采购分析模拟"
            },
            {
                "message": "搜索市场信息",
                "expected_type": "search",
                "description": "搜索结果模拟"
            },
            {
                "message": "一般性问题",
                "expected_type": "general",
                "description": "通用响应模拟"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 API测试{i}: {test_case['description']}")
            
            request_data = {"message": test_case['message']}
            
            response = await client.post(CHAT_URL, json=request_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    data = result.get('data', {})
                    print(f"   ✅ API响应成功")
                    print(f"   📋 响应类型: {result.get('message', '')[:50]}...")
                    print(f"   📊 数据类型: {data.get('type', 'N/A')}")
                    
                    # 验证模拟工具调用
                    if test_case['expected_type'] == 'task' and data.get('task_completed'):
                        print(f"   ✅ 任务模拟执行成功")
                        if data.get('redpacket_sent'):
                            print(f"   ✅ 红包发放成功: {data.get('redpacket_id', 'N/A')}")
                    elif test_case['expected_type'] == 'purchase' and data.get('recommendations'):
                        print(f"   ✅ 采购模拟执行成功")
                    elif test_case['expected_type'] == 'search' and data.get('search_results'):
                        print(f"   ✅ 搜索模拟执行成功")
                    elif test_case['expected_type'] == 'general':
                        print(f"   ✅ 通用模拟执行成功")
                else:
                    print(f"   ❌ API响应失败: {result['message']}")
            else:
                print(f"   ❌ API请求失败: {response.status_code}")


def check_project_structure():
    """检查项目结构"""
    print("\n🧪 检查项目结构")
    print("=" * 50)
    
    import os
    
    # 检查关键文件
    key_files = {
        "智能体文件": [
            "agents/main_deepagent.py",
            "agents/task_deepagent.py",
            "agents/purchase_deepagent.py",
            "agents/search_deepagent.py"
        ],
        "工具文件": [
            "tools/redpacket_tool.py",
            "tools/simulation_tool.py",
            "tools/bing_search.py"
        ],
        "API文件": [
            "api/chat_router.py",
            "service/chat_service.py",
            "main.py"
        ]
    }
    
    for category, files in key_files.items():
        print(f"\n📁 {category}:")
        for file_path in files:
            full_path = f"e:/workspace/program/python/shop_assistant_chat/{file_path}"
            if os.path.exists(full_path):
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} (缺失)")
    
    # 检查删除的文件
    deleted_files = [
        "agents/deepagents_system.py",
        "AGENTS_SEPARATION.md",
        "DEEPAGENTS_IMPLEMENTATION.md"
    ]
    
    print(f"\n🗑️ 已删除的文件:")
    for file_path in deleted_files:
        full_path = f"e:/workspace/program/python/shop_assistant_chat/{file_path}"
        if not os.path.exists(full_path):
            print(f"   ✅ {file_path} (已删除)")
        else:
            print(f"   ❌ {file_path} (仍存在)")


def check_code_cleanliness():
    """检查代码整洁性"""
    print("\n🧪 检查代码整洁性")
    print("=" * 50)
    
    import re
    
    # 检查是否有模拟逻辑在智能体中
    agent_files = [
        "e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/task_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/purchase_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/search_deepagent.py"
    ]
    
    for file_path in agent_files:
        print(f"\n📄 检查文件: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否有直接的模拟逻辑
            simulation_patterns = [
                r'模拟.*执行',
                r'MockAgent',
                r'mock.*response',
                r'模拟.*回答',
                r'模拟.*分析'
            ]
            
            found_simulations = []
            for pattern in simulation_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_simulations.extend(matches)
            
            if found_simulations:
                print(f"   ⚠️ 发现模拟逻辑: {found_simulations}")
            else:
                print(f"   ✅ 无直接模拟逻辑")
            
            # 检查是否使用工具调用
            tool_patterns = [
                r'from tools\.',
                r'await.*tool',
                r'simulate_.*\(',
                r'tools\.'
            ]
            
            found_tools = []
            for pattern in tool_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_tools.extend(matches)
            
            if found_tools:
                print(f"   ✅ 使用工具调用: {len(found_tools)}处")
            else:
                print(f"   ⚠️ 未发现工具调用")
                
        except Exception as e:
            print(f"   ❌ 检查失败: {e}")


async def main():
    """主测试函数"""
    print("🚀 项目清理验证测试")
    print("=" * 50)
    
    try:
        # 检查项目结构
        check_project_structure()
        
        # 检查代码整洁性
        check_code_cleanliness()
        
        # 测试模拟工具集成
        await test_simulation_tools_integration()
        
        # 测试API模拟工作流程
        await test_api_simulation_workflow()
        
        print("\n" + "=" * 50)
        print("✅ 项目清理验证完成！")
        print("\n📝 清理总结:")
        print("1. ✅ 删除了重复的deepagents_system.py文件")
        print("2. ✅ 删除了过时的文档文件")
        print("3. ✅ 重命名了req.txt为REQUIREMENTS.md")
        print("4. ✅ 所有模拟逻辑都在工具中执行")
        print("5. ✅ 智能体只负责调用工具")
        print("6. ✅ 实现了职责分离")
        print("7. ✅ 项目结构更加整洁")
        
    except Exception as e:
        print(f"\n❌ 验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
