#!/usr/bin/env python3
"""
Docker部署测试脚本
"""

import requests
import time
import json
import sys


def test_health_check():
    """测试健康检查端点"""
    print("🔍 测试健康检查端点...")
    
    try:
        response = requests.get("http://localhost:8800/health", timeout=10)
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False


def test_root_endpoint():
    """测试根端点"""
    print("\n🔍 测试根端点...")
    
    try:
        response = requests.get("http://localhost:8800/", timeout=10)
        if response.status_code == 200:
            print("✅ 根端点正常")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 根端点失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 根端点异常: {e}")
        return False


def test_chat_complete():
    """测试聊天完成接口"""
    print("\n🔍 测试聊天完成接口...")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "user_id": "test_user",
            "session_id": "test_session"
        }
        
        data = {
            "message": "你好，这是一个测试消息",
            "image_url": None
        }
        
        response = requests.post(
            "http://localhost:8800/api/v1/chat/complete",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天完成接口正常")
            print(f"响应类型: {result.get('code')}")
            print(f"响应消息: {result.get('message')}")
            if result.get('data'):
                print(f"业务数据类型: {result.get('data', {}).get('type')}")
            return True
        else:
            print(f"❌ 聊天完成接口失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 聊天完成接口异常: {e}")
        return False


def test_chat_stream():
    """测试流式聊天接口"""
    print("\n🔍 测试流式聊天接口...")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "user_id": "test_user",
            "session_id": "test_session"
        }
        
        data = {
            "message": "你好，这是一个流式测试",
            "image_url": None
        }
        
        response = requests.post(
            "http://localhost:8800/api/v1/chat/stream",
            headers=headers,
            json=data,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ 流式聊天接口正常")
            
            # 读取前几行流式数据
            line_count = 0
            for line in response.iter_lines():
                if line and line_count < 5:  # 只显示前5行
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_part = line_str[6:]  # 去掉 'data: ' 前缀
                        try:
                            json_data = json.loads(data_part)
                            print(f"流式数据 {line_count + 1}: code={json_data.get('code')}, finished={json_data.get('finished')}")
                        except:
                            print(f"流式数据 {line_count + 1}: {data_part[:50]}...")
                    line_count += 1
                
                if line_count >= 5:
                    break
            
            return True
        else:
            print(f"❌ 流式聊天接口失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 流式聊天接口异常: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n🔍 测试错误处理...")
    
    try:
        # 测试缺少user_id
        headers = {
            "Content-Type": "application/json",
            "session_id": "test_session"
        }
        
        data = {
            "message": "测试错误处理",
            "image_url": None
        }
        
        response = requests.post(
            "http://localhost:8800/api/v1/chat/complete",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 400:
            result = response.json()
            print("✅ 错误处理正常")
            print(f"错误码: {result.get('code')}")
            print(f"错误消息: {result.get('message')}")
            return True
        else:
            print(f"❌ 错误处理失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 错误处理异常: {e}")
        return False


def wait_for_service(max_attempts=30, interval=2):
    """等待服务启动"""
    print("⏳ 等待服务启动...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8800/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ 服务已启动 (耗时: {attempt * interval}秒)")
                return True
        except:
            pass
        
        print(f"等待服务启动... ({attempt + 1}/{max_attempts})")
        time.sleep(interval)
    
    print("❌ 服务启动超时")
    return False


def main():
    """主测试函数"""
    print("🐳 Docker部署测试")
    print("=" * 50)
    
    # 等待服务启动
    if not wait_for_service():
        sys.exit(1)
    
    # 运行测试
    tests = [
        ("健康检查", test_health_check),
        ("根端点", test_root_endpoint),
        ("聊天完成接口", test_chat_complete),
        ("流式聊天接口", test_chat_stream),
        ("错误处理", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Docker部署成功！")
        sys.exit(0)
    else:
        print("⚠️ 部分测试失败，请检查服务状态")
        sys.exit(1)


if __name__ == "__main__":
    main()
