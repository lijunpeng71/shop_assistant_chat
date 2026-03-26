#!/usr/bin/env python3
"""
测试Header参数获取的脚本
"""

import asyncio
import httpx
import json

# API配置
BASE_URL = "http://localhost:8800"
API_URL = f"{BASE_URL}/api/v1/chat/complete"


async def test_headers():
    """测试不同的Header参数传递方式"""
    print("🧪 测试Header参数获取...")
    
    async with httpx.AsyncClient() as client:
        # 测试1: 标准Header传递
        print("\n1. 测试标准Header传递:")
        headers = {
            "user_id": "test_user_123",
            "session_id": "session_001",
            "Content-Type": "application/json"
        }
        data = {
            "message": "你好，测试Header传递"
        }
        
        response = await client.post(
            API_URL,
            json=data,
            headers=headers
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"错误响应: {response.text}")
        
        # 测试2: 小写Header
        print("\n2. 测试小写Header:")
        headers_lower = {
            "user-id": "test_user_456",
            "session-id": "session_002",
            "Content-Type": "application/json"
        }
        
        response = await client.post(
            API_URL,
            json={"message": "测试小写Header"},
            headers=headers_lower
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"错误响应: {response.text}")
        
        # 测试3: 无Header
        print("\n3. 测试无Header:")
        response = await client.post(
            API_URL,
            json={"message": "测试无Header"}
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"错误响应: {response.text}")


def test_curl_commands():
    """测试curl命令"""
    print("\n" + "="*60)
    print("🔧 推荐的curl测试命令:")
    print("="*60)
    
    print("\n1. 标准Header传递:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H "user_id: test_user_123" \\
  -H "session_id: session_001" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "你好，测试Header传递"}' ''')
    
    print("\n2. 使用单引号包围整个header:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" \\
  -H 'user_id: test_user_123' \\
  -H 'session_id: session_001' \\
  -H 'Content-Type: application/json' \\
  -d '{"message": "你好，测试Header传递"}' ''')
    
    print("\n3. 在Windows PowerShell中:")
    print('''curl -X POST "http://localhost:8800/api/v1/chat/complete" `
  -H "user_id: test_user_123" `
  -H "session_id: session_001" `
  -H "Content-Type: application/json" `
  -d '{"message": "你好，测试Header传递"}' ''')


async def main():
    """主测试函数"""
    print("🚀 开始Header参数测试")
    print("=" * 50)
    
    try:
        # 测试Header传递
        await test_headers()
        
        # 显示curl命令示例
        test_curl_commands()
        
        print("\n" + "=" * 50)
        print("✅ 测试完成！")
        print("\n📝 调试说明:")
        print("1. 检查服务器日志中的'请求头信息'输出")
        print("2. 确保Header名称正确：user_id 和 session_id")
        print("3. 检查Content-Type是否设置为application/json")
        print("4. 使用正确的curl命令格式")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
