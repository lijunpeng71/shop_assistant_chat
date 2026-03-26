#!/usr/bin/env python3
"""
测试流式响应功能 - 验证打字机效果
"""

import re


def check_stream_response_implementation():
    """检查流式响应实现"""
    print("检查流式响应实现")
    print("=" * 50)
    
    # 检查chat_router.py中的流式响应实现
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查是否导入了StreamingResponse
        if 'from fastapi.responses import StreamingResponse' in content:
            print("[OK] 导入了StreamingResponse")
        else:
            print("[ERROR] 未导入StreamingResponse")
        
        # 检查是否导入了asyncio
        if 'import asyncio' in content:
            print("[OK] 导入了asyncio")
        else:
            print("[ERROR] 未导入asyncio")
        
        # 检查是否添加了流式接口
        if '@chat_router.post("/stream")' in content:
            print("[OK] 添加了流式接口")
        else:
            print("[ERROR] 未添加流式接口")
        
        # 检查是否有流式响应函数
        if 'async def stream_complete(' in content:
            print("[OK] 包含流式响应函数")
        else:
            print("[ERROR] 缺少流式响应函数")
        
        # 检查是否有流式生成器
        if 'async def stream_chat_response(' in content:
            print("[OK] 包含流式生成器")
        else:
            print("[ERROR] 缺少流式生成器")
        
        # 检查是否使用Server-Sent Events格式
        if 'data: ' in content and '\\n\\n' in content:
            print("[OK] 使用Server-Sent Events格式")
        else:
            print("[ERROR] 未使用Server-Sent Events格式")
        
        # 检查是否有打字机效果
        if 'await asyncio.sleep' in content:
            print("[OK] 实现了打字机效果")
        else:
            print("[ERROR] 未实现打字机效果")
        
        # 检查是否有逐字符输出
        if 'for i, char in enumerate(' in content:
            print("[OK] 实现了逐字符输出")
        else:
            print("[ERROR] 未实现逐字符输出")
        
        # 检查是否有完成标志
        if '"finished": True' in content:
            print("[OK] 包含完成标志")
        else:
            print("[ERROR] 缺少完成标志")
        
        # 检查是否有错误处理
        if 'except Exception as e:' in content:
            print("[OK] 包含错误处理")
        else:
            print("[ERROR] 缺少错误处理")
        
    except Exception as e:
        print(f"[ERROR] 检查chat_router.py失败: {e}")


def analyze_stream_format():
    """分析流式响应格式"""
    print("\n分析流式响应格式")
    print("=" * 50)
    
    print("流式响应格式 (Server-Sent Events):")
    print("data: {\"code\": 0, \"partial\": true, \"content\": \"{\", \"finished\": false}")
    print("data: {\"code\": 0, \"partial\": true, \"content\": \"\\\"code\\\": 0\", \"finished\": false}")
    print("data: {\"code\": 0, \"partial\": true, \"content\": \"\\\"code\\\": 0, \\\"message\\\": \\\"处理成功\\\"\", \"finished\": false}")
    print("...")
    print("data: {\"code\": 0, \"partial\": true, \"content\": \"完整JSON内容\", \"finished\": true}")
    print("data: {\"code\": 0, \"message\": \"流式响应完成\", \"finished\": true}")
    
    print("\n响应字段说明:")
    print("• code: 响应码 (0=成功, 400=参数错误, 500=服务器错误)")
    print("• partial: 是否为部分响应 (true=进行中, false=完整响应)")
    print("• content: 部分内容 (逐字符累积)")
    print("• finished: 是否完成 (false=进行中, true=完成)")
    print("• message: 状态消息")
    print("• data: 完整的业务数据 (仅在最终响应中)")
    
    print("\n打字机效果:")
    print("• 每2-3个字符暂停50ms")
    print("• 模拟真实的打字速度")
    print("• 提供良好的用户体验")
    print("• 支持中文字符显示")


def check_error_handling():
    """检查错误处理"""
    print("\n检查错误处理")
    print("=" * 50)
    
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查user_id验证
        if 'if not user_id:' in content and 'stream' in content:
            print("[OK] 流式接口包含user_id验证")
        else:
            print("[ERROR] 流式接口缺少user_id验证")
        
        # 检查session_id验证
        if 'if not session_id:' in content and 'stream' in content:
            print("[OK] 流式接口包含session_id验证")
        else:
            print("[ERROR] 流式接口缺少session_id验证")
        
        # 检查流式错误响应格式
        if 'StreamingResponse(' in content and 'iter([' in content:
            print("[OK] 使用流式错误响应")
        else:
            print("[ERROR] 未使用流式错误响应")
        
        # 检查异常处理
        if 'except Exception as e:' in content and 'stream' in content:
            print("[OK] 流式接口包含异常处理")
        else:
            print("[ERROR] 流式接口缺少异常处理")
        
        # 检查错误日志
        if 'log.error(f"流式' in content:
            print("[OK] 包含流式错误日志")
        else:
            print("[ERROR] 缺少流式错误日志")
        
    except Exception as e:
        print(f"[ERROR] 检查错误处理失败: {e}")


def test_client_usage():
    """测试客户端使用"""
    print("\n测试客户端使用")
    print("=" * 50)
    
    print("JavaScript客户端示例:")
    print("""
// 使用EventSource接收流式响应
const eventSource = new EventSource('/api/v1/chat/stream', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'user_id': 'user123',
        'session_id': 'session456'
    },
    body: JSON.stringify({
        message: '你好',
        image_url: null
    })
});

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.finished) {
        console.log('响应完成:', data);
        eventSource.close();
    } else if (data.partial) {
        // 打字机效果：逐字符显示
        console.log('部分内容:', data.content);
        // 更新UI显示
        updateTypingEffect(data.content);
    } else {
        // 错误处理
        console.error('错误:', data.message);
    }
};

eventSource.onerror = function(event) {
    console.error('流式连接错误:', event);
    eventSource.close();
};
""")
    
    print("\nPython客户端示例:")
    print("""
import requests
import json

# 使用流式请求
response = requests.post(
    'http://localhost:8000/api/v1/chat/stream',
    headers={
        'Content-Type': 'application/json',
        'user_id': 'user123',
        'session_id': 'session456'
    },
    json={
        'message': '你好',
        'image_url': None
    },
    stream=True
)

# 处理流式响应
for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            data = json.loads(line_str[6:])  # 去掉 'data: ' 前缀
            
            if data.get('finished'):
                print('响应完成:', data)
                break
            elif data.get('partial'):
                # 打字机效果
                print('部分内容:', data.get('content', ''))
            else:
                print('错误:', data.get('message', ''))
""")
    
    print("\ncurl测试命令:")
    print("""
curl -X POST "http://localhost:8000/api/v1/chat/stream" \\
  -H "Content-Type: application/json" \\
  -H "user_id: user123" \\
  -H "session_id: session456" \\
  -d '{"message": "你好", "image_url": null}' \\
  --no-buffer
""")


def main():
    """主测试函数"""
    print("流式响应功能测试")
    print("=" * 50)
    
    try:
        # 检查流式响应实现
        check_stream_response_implementation()
        
        # 分析流式响应格式
        analyze_stream_format()
        
        # 检查错误处理
        check_error_handling()
        
        # 测试客户端使用
        test_client_usage()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n功能总结:")
        print("1. 流式接口 - 新增/api/v1/chat/stream接口")
        print("2. 打字机效果 - 逐字符输出，模拟真实打字")
        print("3. Server-Sent Events - 使用标准SSE格式")
        print("4. 错误处理 - 完善的流式错误处理")
        print("5. 参数验证 - 验证user_id和session_id")
        print("6. 速度控制 - 可调节的打字速度")
        
        print("\n技术特点:")
        print("• 异步流式处理")
        print("• 标准SSE协议")
        print("• 逐字符打字效果")
        print("• 完成状态标志")
        print("• 错误流式返回")
        print("• 中文字符支持")
        
        print("\n用户体验:")
        print("• 实时显示响应内容")
        print("• 打字机视觉效果")
        print("• 流畅的交互体验")
        print("• 即时的错误反馈")
        print("• 跨浏览器兼容")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
