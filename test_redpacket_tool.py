#!/usr/bin/env python3
"""
测试红包工具功能
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_task_with_redpacket():
    """测试任务执行后的红包发放"""
    print("🧪 测试任务执行后的红包发放")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 用户发起任务
        print("\n📝 步骤1: 用户发起任务")
        request_data = {
            "message": "我要执行库存盘点"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 任务确认成功: {result['message'][:100]}...")
                print(f"🔄 中断状态: {data.get('interrupted', False)}")
                
                # 步骤2: 用户确认执行
                await test_task_execution_with_redpacket(client, headers)
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_task_execution_with_redpacket(client, headers):
    """测试任务执行和红包发放"""
    print("\n📝 步骤2: 用户确认执行任务（包含红包发放）")
    
    request_data = {
        "message": "确认执行"
    }
    
    response = await client.post(CHAT_URL, json=request_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            data = result.get('data', {})
            print(f"✅ 任务执行成功: {result['message'][:100]}...")
            print(f"📋 执行结果: {data.get('task_result', 'N/A')}")
            
            # 检查红包发放情况
            if data.get('redpacket_sent'):
                print(f"🧧 红包发放成功: {data.get('redpacket_id')}")
                print(f"💰 实际奖励金额: {data.get('actual_reward', 0)}元")
            else:
                print(f"⚠️ 红包发放失败: {data.get('redpacket_error', 'Unknown error')}")
                
            if data.get('reward'):
                print(f"🎁 建议奖励: {data.get('reward')}元")
        else:
            print(f"❌ 任务执行失败: {result['message']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")


async def test_freezer_inspection_with_redpacket():
    """测试冰柜检查和红包发放"""
    print("\n🧪 测试冰柜检查和红包发放")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 带图片的冰柜检查
        print("\n📝 步骤1: 带图片的冰柜检查")
        request_data = {
            "message": "我要检查冰柜陈列",
            "image_url": "https://example.com/freezer_photo.jpg"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 冰柜检查成功: {result['message'][:100]}...")
                print(f"📋 检查结果: {data.get('inspection_result', '')}")
                print(f"📊 评分: {data.get('score', 0)}")
                
                # 检查红包发放情况
                if data.get('redpacket_sent'):
                    print(f"🧧 红包发放成功: {data.get('redpacket_id')}")
                    print(f"💰 实际奖励金额: {data.get('actual_reward', 0)}元")
                else:
                    print(f"⚠️ 红包发放失败: {data.get('redpacket_error', 'Unknown error')}")
                
                if data.get('reward'):
                    print(f"🎁 建议奖励: {data.get('reward')}元")
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_redpacket_tool_directly():
    """直接测试红包工具"""
    print("\n🧪 直接测试红包工具")
    print("=" * 50)
    
    try:
        from tools.redpacket_tool import send_redpacket, calculate_and_send_reward, redpacket_tool, simulate_task_execution
        
        # 测试1: 直接发送红包
        print("\n📝 测试1: 直接发送红包")
        result1 = await send_redpacket(
            user_id="test_user_123",
            amount=8.8,
            reason="库存盘点任务完成",
            task_type="inventory_check"
        )
        print(f"✅ 直接发送红包结果: {result1}")
        
        # 测试2: 计算并发送奖励
        print("\n📝 测试2: 计算并发送奖励")
        result2 = await calculate_and_send_reward(
            user_id="test_user_123",
            task_type="freezer_inspection",
            performance_score=85,
            task_description="冰柜陈列检查任务"
        )
        print(f"✅ 计算并发送奖励结果: {result2}")
        
        # 测试3: 模拟任务执行（新功能）
        print("\n📝 测试3: 模拟任务执行")
        result3 = await simulate_task_execution(
            user_id="test_user_123",
            message="我要执行库存盘点",
            task_type="general"
        )
        print(f"✅ 模拟任务执行结果: {result3}")
        
        # 测试4: 任务分析
        print("\n📝 测试4: 任务分析")
        analysis1 = redpacket_tool.analyze_task("我要检查冰柜陈列", "general")
        analysis2 = redpacket_tool.analyze_task("我要执行库存盘点", "general")
        analysis3 = redpacket_tool.analyze_task("我要分析销售数据", "general")
        
        print(f"📊 冰柜检查分析: {analysis1}")
        print(f"📊 库存盘点分析: {analysis2}")
        print(f"📊 销售分析分析: {analysis3}")
        
        # 测试5: 奖励金额计算
        print("\n📝 测试5: 奖励金额计算")
        amount1 = redpacket_tool.calculate_reward("inventory_check", 90)
        amount2 = redpacket_tool.calculate_reward("freezer_inspection", 85)
        amount3 = redpacket_tool.calculate_reward("sales_analysis", 75)
        
        print(f"💰 库存盘点奖励(90分): {amount1}元")
        print(f"💰 冰柜检查奖励(85分): {amount2}元")
        print(f"💰 销售分析奖励(75分): {amount3}元")
        
    except Exception as e:
        print(f"❌ 红包工具测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_mock_agent_with_redpacket():
    """测试模拟智能体的红包功能"""
    print("\n🧪 测试模拟智能体的红包功能")
    print("=" * 50)
    
    # 模拟DeepAgents不可用的情况
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 发送任务请求（应该触发模拟智能体）
        print("\n📝 测试模拟智能体任务执行")
        request_data = {
            "message": "我要执行任务"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 模拟智能体响应: {result['message'][:100]}...")
                
                # 检查红包发放情况
                if data.get('redpacket_sent'):
                    print(f"🧧 模拟红包发放成功: {data.get('redpacket_id')}")
                    print(f"💰 实际奖励金额: {data.get('actual_reward', 0)}元")
                else:
                    print(f"⚠️ 模拟红包发放失败: {data.get('redpacket_error', 'Unknown error')}")
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


def show_curl_examples():
    """显示curl命令示例"""
    print("\n" + "=" * 60)
    print("🔧 红包工具功能使用示例")
    print("=" * 60)
    
    print("\n1️⃣ 执行任务（包含红包发放）:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要执行库存盘点"}' ''')
    
    print("\n2️⃣ 确认执行（自动发放红包）:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "确认执行"}' ''')
    
    print("\n3️⃣ 冰柜检查（包含红包发放）:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "我要检查冰柜陈列",
    "image_url": "https://example.com/freezer_photo.jpg"
  }' ''')


async def main():
    """主测试函数"""
    print("🚀 红包工具功能测试")
    print("=" * 50)
    
    try:
        # 测试任务执行和红包发放
        await test_task_with_redpacket()
        
        # 测试冰柜检查和红包发放
        await test_freezer_inspection_with_redpacket()
        
        # 直接测试红包工具
        await test_redpacket_tool_directly()
        
        # 测试模拟智能体的红包功能
        await test_mock_agent_with_redpacket()
        
        # 显示使用示例
        show_curl_examples()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 红包工具功能说明:")
        print("1. 任务执行完成后，智能体自动计算奖励金额")
        print("2. 使用红包工具API发送红包给用户")
        print("3. 奖励金额基于任务类型和绩效评分动态计算")
        print("4. 支持模拟智能体的红包发放功能")
        print("5. 完善的错误处理和状态反馈")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
