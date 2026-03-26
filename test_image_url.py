#!/usr/bin/env python3
"""
测试图片URL功能的脚本
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
CHAT_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_freezer_inspection_without_image():
    """测试不带图片的冰柜检查请求"""
    print("🧪 测试不带图片的冰柜检查请求")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        request_data = {
            "message": "我要检查冰柜陈列"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 响应成功: {result['message']}")
                print(f"📋 需要图片: {data.get('requires_image', False)}")
                print(f"📋 任务类型: {data.get('task_type', '')}")
                print(f"📋 操作指引: {data.get('instructions', [])}")
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_freezer_inspection_with_image():
    """测试带图片URL的冰柜检查请求"""
    print("\n🧪 测试带图片URL的冰柜检查请求")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        request_data = {
            "message": "我要检查冰柜陈列",
            "image_url": "https://example.com/freezer_photo.jpg"
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 响应成功: {result['message'][:100]}...")
                print(f"📋 检查结果: {data.get('inspection_result', '')}")
                print(f"📊 评分: {data.get('score', 0)}")
                print(f"🎁 奖励: {data.get('reward', 0)}元")
                print(f"🔗 图片URL: {data.get('image_url', '')}")
                if data.get('suggestions'):
                    print(f"💡 建议: {data['suggestions']}")
            else:
                print(f"❌ 响应失败: {result['message']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")


async def test_other_tasks():
    """测试其他任务类型"""
    print("\n🧪 测试其他任务类型")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        
        # 测试采购任务
        print("\n📦 测试采购任务:")
        request_data = {
            "message": "我要采购商品",
            "image_url": "https://example.com/products.jpg"  # 采购任务也会传递图片URL但不会使用
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 采购任务成功: {result['message'][:50]}...")
            else:
                print(f"❌ 采购任务失败: {result['message']}")
        
        # 测试搜索任务
        print("\n🔍 测试搜索任务:")
        request_data = {
            "message": "搜索市场信息",
            "image_url": None  # 搜索任务不需要图片
        }
        
        response = await client.post(CHAT_URL, json=request_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 搜索任务成功: {result['message'][:50]}...")
            else:
                print(f"❌ 搜索任务失败: {result['message']}")


def show_curl_examples():
    """显示curl命令示例"""
    print("\n" + "=" * 60)
    print("🔧 图片URL功能使用示例")
    print("=" * 60)
    
    print("\n1️⃣ 不带图片的冰柜检查请求:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "我要检查冰柜陈列"}' ''')
    
    print("\n2️⃣ 带图片URL的冰柜检查请求:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "我要检查冰柜陈列",
    "image_url": "https://example.com/freezer_photo.jpg"
  }' ''')
    
    print("\n3️⃣ 其他任务（图片URL会被忽略）:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "我要采购商品",
    "image_url": "https://example.com/products.jpg"
  }' ''')


async def main():
    """主测试函数"""
    print("🚀 图片URL功能测试")
    print("=" * 50)
    
    try:
        # 测试不带图片的请求
        await test_freezer_inspection_without_image()
        
        # 测试带图片的请求
        await test_freezer_inspection_with_image()
        
        # 测试其他任务类型
        await test_other_tasks()
        
        # 显示使用示例
        show_curl_examples()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 功能说明:")
        print("1. 冰柜检查任务会检查是否提供了image_url参数")
        print("2. 如果没有提供图片URL，会提示用户需要提供图片")
        print("3. 如果提供了图片URL，会基于图片进行陈列评估")
        print("4. 其他任务类型会忽略image_url参数")
        print("5. 图片URL可以是任何有效的图片地址")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
