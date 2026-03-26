#!/usr/bin/env python3
"""
测试LangChain DeepAgents原生Human-in-the-Loop中断功能
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_deepagents_task_confirmation():
    """测试DeepAgents任务确认中断"""
    print("🧪 测试DeepAgents任务确认中断")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 用户发起库存盘点任务
        print("\n📝 步骤1: 用户发起库存盘点任务")
        request_data = {
            "message": "我要执行库存盘点"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ DeepAgents中断成功: {result['message'][:100]}...")
                print(f"🔄 中断状态: {data.get('interrupted', False)}")
                print(f"📋 中断原因: {data.get('interrupt_reason', '')}")
                if data.get('task_info'):
                    task_info = data.get('task_info', {})
                    print(f"📋 任务名称: {task_info.get('task_name', '')}")
                    print(f"📋 任务描述: {task_info.get('description', '')}")
                
                # 步骤2: 用户确认执行
                await test_task_execution_after_confirm(client, headers)
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_task_execution_after_confirm(client, headers):
    """测试确认后的任务执行"""
    print("\n📝 步骤2: 用户确认执行任务")
    
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


async def test_deepagents_image_required():
    """测试DeepAgents图片需求中断"""
    print("\n🧪 测试DeepAgents图片需求中断")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 用户发起冰柜检查（不带图片）
        print("\n📝 步骤1: 用户发起冰柜检查（不带图片）")
        request_data = {
            "message": "我要检查冰柜陈列"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ DeepAgents图片中断成功: {result['message'][:100]}...")
                print(f"🔄 中断状态: {data.get('interrupted', False)}")
                print(f"📋 中断原因: {data.get('interrupt_reason', '')}")
                print(f"📸 需要图片: {data.get('requires_image', False)}")
                print(f"📋 图片类型: {data.get('image_type', '')}")
                
                # 步骤2: 提供图片URL后继续
                await test_image_provision(client, headers)
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_image_provision(client, headers):
    """测试提供图片后的处理"""
    print("\n📝 步骤2: 提供图片URL后继续")
    
    request_data = {
        "message": "我要检查冰柜陈列",
        "image_url": "https://example.com/freezer_photo.jpg"
    }
    
    response = await client.post(CHAT_URL, json=request_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            data = result.get('data', {})
            print(f"✅ 图片分析成功: {result['message'][:100]}...")
            print(f"📋 检查结果: {data.get('inspection_result', '')}")
            print(f"📊 评分: {data.get('score', 0)}")
            if data.get('reward'):
                print(f"🎁 奖励: {data.get('reward')}元")
        else:
            print(f"❌ 图片分析失败: {result['message']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")


async def test_deepagents_user_approval():
    """测试DeepAgents用户批准中断"""
    print("\n🧪 测试DeepAgents用户批准中断")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 步骤1: 触发需要批准的操作
        print("\n📝 步骤1: 触发需要批准的操作")
        request_data = {
            "message": "我要执行高风险操作"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ DeepAgents批准中断成功: {result['message'][:100]}...")
                print(f"🔄 中断状态: {data.get('interrupted', False)}")
                print(f"📋 中断原因: {data.get('interrupt_reason', '')}")
                print(f"⚠️ 需要批准: {data.get('requires_approval', False)}")
                
                # 步骤2: 用户批准操作
                await test_user_approval_response(client, headers)
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_user_approval_response(client, headers):
    """测试用户批准响应"""
    print("\n📝 步骤2: 用户批准操作")
    
    request_data = {
        "message": "批准"
    }
    
    response = await client.post(CHAT_URL, json=request_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            print(f"✅ 操作批准成功: {result['message'][:100]}...")
        else:
            print(f"❌ 操作批准失败: {result['message']}")
    else:
        print(f"❌ 请求失败: {response.status_code}")


async def test_interrupt_error_handling():
    """测试中断错误处理"""
    print("\n🧪 测试中断错误处理")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 测试可能导致中断错误的场景
        print("\n📝 测试中断错误处理:")
        request_data = {
            "message": "执行可能导致中断的任务"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                if data.get('interrupted'):
                    print(f"✅ 中断处理正常: {result['message'][:50]}...")
                else:
                    print(f"✅ 正常执行: {result['message'][:50]}...")
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


def show_curl_examples():
    """显示curl命令示例"""
    print("\n" + "=" * 60)
    print("🔧 DeepAgents原生中断功能使用示例")
    print("=" * 60)
    
    print("\n1️⃣ 触发任务确认中断:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要执行库存盘点"}' ''')
    
    print("\n2️⃣ 确认执行任务:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "确认执行"}' ''')
    
    print("\n3️⃣ 触发图片需求中断:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要检查冰柜陈列"}' ''')
    
    print("\n4️⃣ 提供图片URL:")
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
    print("🚀 DeepAgents原生Human-in-the-Loop中断功能测试")
    print("=" * 60)
    
    try:
        # 测试任务确认中断
        await test_deepagents_task_confirmation()
        
        # 测试图片需求中断
        await test_deepagents_image_required()
        
        # 测试用户批准中断
        await test_deepagents_user_approval()
        
        # 测试中断错误处理
        await test_interrupt_error_handling()
        
        # 显示使用示例
        show_curl_examples()
        
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print("\n📝 DeepAgents原生中断功能说明:")
        print("1. 使用LangChain DeepAgents的interrupt_on机制")
        print("2. 支持task_confirmation、image_required、user_approval等中断类型")
        print("3. 中断状态由DeepAgents框架自动管理")
        print("4. 主智能体负责处理中断状态并转换为用户友好的响应")
        print("5. 支持中断错误的优雅处理和回退机制")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
