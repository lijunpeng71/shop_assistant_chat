#!/usr/bin/env python3
"""
测试任务确认功能的脚本
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_task_confirmation_workflow():
    """测试任务确认工作流程"""
    print("🧪 测试任务确认工作流程")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 用户发起任务请求
        print("\n📝 步骤1: 用户发起任务请求")
        request_data = {
            "message": "我要执行库存盘点"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 响应成功: {result['message'][:100]}...")
                print(f"📋 需要确认: {data.get('requires_confirmation', False)}")
                if data.get('task_info'):
                    task_info = data.get('task_info', {})
                    print(f"📋 任务名称: {task_info.get('task_name', '')}")
                    print(f"📋 任务描述: {task_info.get('description', '')}")
                    print(f"⏱️ 预计耗时: {task_info.get('estimated_time', '')}")
                    print(f"📋 确认选项: {data.get('confirmation_options', [])}")
                
                # 步骤2: 用户确认执行任务
                await test_task_execution(client, headers)
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_task_execution(client, headers):
    """测试任务执行"""
    print("\n📝 步骤2: 用户确认执行任务")
    
    # 用户确认执行
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
            if data.get('reward'):
                print(f"🎁 奖励: {data.get('reward')}元")
        else:
            print(f"❌ 任务执行失败: {result['message']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")


async def test_different_task_types():
    """测试不同类型的任务确认"""
    print("\n🧪 测试不同类型的任务确认")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 测试销售数据分析
        print("\n📊 测试销售数据分析:")
        request_data = {
            "message": "我要分析销售数据"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 销售分析确认: {result['message'][:50]}...")
                if data.get('task_info'):
                    task_info = data.get('task_info', {})
                    print(f"📋 任务类型: {task_info.get('task_type', '')}")
        
        # 测试一般任务
        print("\n🔧 测试一般任务:")
        request_data = {
            "message": "我要执行任务"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 一般任务确认: {result['message'][:50]}...")
                if data.get('task_info'):
                    task_info = data.get('task_info', {})
                    print(f"📋 任务类型: {task_info.get('task_type', '')}")


async def test_user_cancellation():
    """测试用户取消任务"""
    print("\n🧪 测试用户取消任务")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 用户发起任务
        print("\n📝 用户发起任务:")
        request_data = {
            "message": "我要执行库存盘点"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 任务确认请求: {result['message'][:50]}...")
                
                # 用户取消任务
                print("\n📝 用户取消任务:")
                request_data = {
                    "message": "取消"
                }
                
                response = await client.post(CHAT_URL, json=request_data, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 任务取消成功: {result['message']}")
                else:
                    print(f"❌ 任务取消失败: {response.status_code}")


def show_curl_examples():
    """显示curl命令示例"""
    print("\n" + "=" * 60)
    print("🔧 任务确认功能使用示例")
    print("=" * 60)
    
    print("\n1️⃣ 发起任务请求（需要确认）:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要执行库存盘点"}' ''')
    
    print("\n2️⃣ 用户确认执行任务:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "确认执行"}' ''')
    
    print("\n3️⃣ 用户取消任务:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "取消"}' ''')
    
    print("\n4️⃣ 其他任务类型:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要分析销售数据"}" ''')


async def main():
    """主测试函数"""
    print("🚀 任务确认功能测试")
    print("=" * 50)
    
    try:
        # 测试完整的任务确认工作流程
        await test_task_confirmation_workflow()
        
        # 测试不同类型的任务
        await test_different_task_types()
        
        # 测试用户取消任务
        await test_user_cancellation()
        
        # 显示使用示例
        show_curl_examples()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 功能说明:")
        print("1. 任务智能体会先识别任务类型和内容")
        print("2. 向用户详细说明将要执行的任务")
        print("3. 询问用户是否确认执行任务")
        print("4. 只有在用户明确同意后才执行任务")
        print("5. 支持用户取消任务")
        print("6. 提供详细的任务信息和执行要求")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
