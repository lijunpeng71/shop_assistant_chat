#!/usr/bin/env python3
"""
简化的测试脚本 - 只测试 chat/complete 接口
"""

import asyncio
import httpx

# API配置
BASE_URL = "http://localhost:8800"
API_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_chat_complete():
    """测试聊天完成接口"""
    print("🧪 测试聊天完成接口...")
    
    async with httpx.AsyncClient() as client:
        # 测试首次进入用户
        print("\n1. 测试首次进入用户:")
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001"
        }
        data = {
            "message": "你好"
        }
        
        response = await client.post(
            API_URL,
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 首次进入成功: {result['message']}")
                data = result.get('data', {})
                print(f"   类型: {data.get('type', 'unknown')}")
                if data.get('suggestions'):
                    print(f"   建议: {data['suggestions']}")
            else:
                print(f"❌ 首次进入失败: {result['message']}")
        else:
            print(f"❌ 首次进入失败: {response.status_code}")
            print(f"   响应: {response.text}")
        
        # 测试任务执行
        print("\n2. 测试任务执行:")
        data = {
            "message": "我要执行任务，检查冰柜陈列"
        }
        
        response = await client.post(
            API_URL,
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 任务执行成功: {result['message']}")
                data = result.get('data', {})
                print(f"   结果: {data.get('message', 'N/A')}")
            else:
                print(f"❌ 任务执行失败: {result['message']}")
        else:
            print(f"❌ 任务执行失败: {response.status_code}")
        
        # 测试采购需求
        print("\n3. 测试采购需求:")
        data = {
            "message": "我要采购商品"
        }
        
        response = await client.post(
            API_URL,
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 采购分析成功: {result['message']}")
                data = result.get('data', {})
                print(f"   建议: {data.get('message', 'N/A')}")
            else:
                print(f"❌ 采购分析失败: {result['message']}")
        else:
            print(f"❌ 采购分析失败: {response.status_code}")
        
        # 测试日常对话
        print("\n4. 测试日常对话:")
        data = {
            "message": "今天天气怎么样？"
        }
        
        response = await client.post(
            API_URL,
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"✅ 日常对话成功: {result['message']}")
                data = result.get('data', {})
                print(f"   回答: {data.get('message', 'N/A')}")
            else:
                print(f"❌ 日常对话失败: {result['message']}")
        else:
            print(f"❌ 日常对话失败: {response.status_code}")


async def test_health_check():
    """测试健康检查接口"""
    print("\n🏥 测试健康检查接口:")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                data = result.get('data', {})
                print(f"✅ 服务健康: {data.get('status', 'unknown')}")
            else:
                print(f"❌ 服务异常: {result['message']}")
        else:
            print(f"❌ 服务异常: {response.status_code}")


async def main():
    """主测试函数"""
    print("🚀 开始简化版多智能体系统测试")
    print("=" * 50)
    
    try:
        # 测试健康检查
        await test_health_check()
        
        # 测试聊天功能
        await test_chat_complete()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 测试说明:")
        print("1. 首次进入会显示欢迎信息和操作建议")
        print("2. 任务智能体可以处理冰柜陈列检查等任务")
        print("3. 采购智能体可以分析采购需求和执行采购")
        print("4. 主智能体负责统筹调度各个子智能体")
        print("5. 所有对话记录只保存在短期记忆中")
        print("6. 系统只提供一个对外接口: /api/v1/chat/complete")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
