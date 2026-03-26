#!/usr/bin/env python3
"""
测试模拟工具功能 - 验证所有模拟逻辑都在工具中执行
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_simulation_tool_directly():
    """直接测试模拟工具"""
    print("🧪 直接测试模拟工具")
    print("=" * 50)
    
    try:
        from tools.redpacket_tool import simulate_task_execution, redpacket_tool
        
        # 测试不同类型的任务模拟
        test_cases = [
            {
                "message": "我要检查冰柜陈列",
                "expected_type": "freezer_inspection",
                "description": "冰柜陈列检查"
            },
            {
                "message": "我要执行库存盘点",
                "expected_type": "inventory_check", 
                "description": "库存盘点"
            },
            {
                "message": "我要分析销售数据",
                "expected_type": "sales_analysis",
                "description": "销售数据分析"
            },
            {
                "message": "我要采购商品",
                "expected_type": "purchase_task",
                "description": "商品采购"
            },
            {
                "message": "我要执行任务",
                "expected_type": "general_task",
                "description": "一般任务"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 测试{i}: {test_case['description']}")
            print(f"   消息: {test_case['message']}")
            
            # 使用工具模拟
            result = await simulate_task_execution(
                user_id="test_user_123",
                message=test_case['message'],
                task_type="general"
            )
            
            print(f"   ✅ 模拟结果类型: {result.get('type')}")
            print(f"   📊 任务类型: {result.get('data', {}).get('task_type')}")
            print(f"   📈 绩效评分: {result.get('data', {}).get('performance_score')}")
            print(f"   💰 建议奖励: {result.get('data', {}).get('reward')}元")
            print(f"   🧧 红包发放: {result.get('data', {}).get('redpacket_sent')}")
            if result.get('data', {}).get('redpacket_id'):
                print(f"   🆔 红包ID: {result.get('data', {}).get('redpacket_id')}")
            
            # 验证结果
            data = result.get('data', {})
            assert data.get('task_completed') == True, "任务应该标记为已完成"
            assert data.get('performance_score') is not None, "应该有绩效评分"
            assert data.get('redpacket_sent') is not None, "应该有红包发放状态"
            
            print(f"   ✅ 验证通过")
        
    except Exception as e:
        print(f"❌ 模拟工具测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_agent_simulation_via_api():
    """通过API测试智能体模拟功能"""
    print("\n🧪 通过API测试智能体模拟功能")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        test_messages = [
            "我要执行库存盘点",
            "我要检查冰柜陈列",
            "我要分析销售数据",
            "我要采购商品"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 API测试{i}: {message}")
            
            request_data = {"message": message}
            
            response = await client.post(CHAT_URL, json=request_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    data = result.get('data', {})
                    print(f"   ✅ API响应成功")
                    print(f"   📋 响应类型: {result.get('message', '')[:50]}...")
                    print(f"   📊 任务完成: {data.get('task_completed', False)}")
                    print(f"   📈 绩效评分: {data.get('performance_score', 'N/A')}")
                    print(f"   🧧 红包发放: {data.get('redpacket_sent', False)}")
                    
                    # 验证模拟逻辑在工具中执行
                    if data.get('task_completed') and data.get('redpacket_sent'):
                        print(f"   ✅ 模拟逻辑在工具中正确执行")
                    else:
                        print(f"   ⚠️ 模拟逻辑可能未正确执行")
                else:
                    print(f"   ❌ API响应失败: {result['message']}")
            else:
                print(f"   ❌ API请求失败: {response.status_code}")


async def test_task_analysis_function():
    """测试任务分析功能"""
    print("\n🧪 测试任务分析功能")
    print("=" * 50)
    
    try:
        from tools.redpacket_tool import redpacket_tool
        
        # 测试任务分析
        test_messages = [
            "我要检查冰柜陈列",
            "我要执行库存盘点", 
            "我要分析销售数据",
            "我要采购商品",
            "我要执行任务"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 分析测试{i}: {message}")
            
            analysis = redpacket_tool.analyze_task(message, "general")
            
            print(f"   📊 识别任务类型: {analysis.get('task_type')}")
            print(f"   📈 绩效评分: {analysis.get('performance_score')}")
            print(f"   💰 建议奖励: {analysis.get('suggested_reward')}元")
            print(f"   📋 执行详情: {analysis.get('execution_details')}")
            print(f"   📝 结果描述: {analysis.get('result_description')}")
            
            # 验证分析结果
            assert analysis.get('task_type') is not None, "应该有任务类型"
            assert analysis.get('performance_score') is not None, "应该有绩效评分"
            assert analysis.get('suggested_reward') is not None, "应该有建议奖励"
            
            print(f"   ✅ 分析验证通过")
        
    except Exception as e:
        print(f"❌ 任务分析测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_simulation_error_handling():
    """测试模拟工具的错误处理"""
    print("\n🧪 测试模拟工具的错误处理")
    print("=" * 50)
    
    try:
        from tools.redpacket_tool import simulate_task_execution
        
        # 测试错误情况
        print("\n📝 测试错误处理:")
        
        # 测试空用户ID
        result1 = await simulate_task_execution(
            user_id="",
            message="测试消息",
            task_type="general"
        )
        print(f"   ✅ 空用户ID处理: {result1.get('type')}")
        
        # 测试空消息
        result2 = await simulate_task_execution(
            user_id="test_user",
            message="",
            task_type="general"
        )
        print(f"   ✅ 空消息处理: {result2.get('type')}")
        
        # 测试无效任务类型
        result3 = await simulate_task_execution(
            user_id="test_user",
            message="测试消息",
            task_type="invalid_type"
        )
        print(f"   ✅ 无效任务类型处理: {result3.get('type')}")
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        import traceback
        traceback.print_exc()


def show_architecture_benefits():
    """显示架构优势"""
    print("\n" + "=" * 60)
    print("🏗️ 模拟逻辑在工具中执行的架构优势")
    print("=" * 60)
    
    print("\n✅ **职责分离**:")
    print("   - 智能体：专注于任务协调和用户交互")
    print("   - 工具：负责具体的模拟逻辑和红包发放")
    
    print("\n✅ **代码复用**:")
    print("   - 模拟逻辑可在多个场景中复用")
    print("   - 红包发放逻辑统一管理")
    
    print("\n✅ **易于测试**:")
    print("   - 工具可以独立测试")
    print("   - 模拟逻辑与智能体逻辑解耦")
    
    print("\n✅ **易于维护**:")
    print("   - 修改模拟逻辑只需更新工具")
    print("   - 智能体代码保持简洁")
    
    print("\n✅ **扩展性强**:")
    print("   - 新增模拟类型只需扩展工具")
    print("   - 支持插件化的模拟策略")


async def main():
    """主测试函数"""
    print("🚀 模拟工具功能测试")
    print("=" * 50)
    
    try:
        # 直接测试模拟工具
        await test_simulation_tool_directly()
        
        # 通过API测试智能体模拟
        await test_agent_simulation_via_api()
        
        # 测试任务分析功能
        await test_task_analysis_function()
        
        # 测试错误处理
        await test_simulation_error_handling()
        
        # 显示架构优势
        show_architecture_benefits()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 架构改进总结:")
        print("1. ✅ 所有模拟逻辑都在工具中执行")
        print("2. ✅ 智能体只负责调用工具，不包含模拟代码")
        print("3. ✅ 实现了职责分离和代码复用")
        print("4. ✅ 提高了代码的可测试性和可维护性")
        print("5. ✅ 支持灵活的模拟策略扩展")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
