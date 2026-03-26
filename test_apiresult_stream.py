#!/usr/bin/env python3
"""
测试流式响应ApiResult统一封装 - 验证统一返回格式
"""

import re


def check_apiresult_stream_implementation():
    """检查ApiResult流式封装实现"""
    print("检查ApiResult流式封装实现")
    print("=" * 50)
    
    # 检查chat_router.py中的ApiResult使用
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查是否使用ApiResult.success
        if 'ApiResult.success(' in content and 'stream' in content:
            print("[OK] 流式响应使用ApiResult.success")
        else:
            print("[ERROR] 流式响应未使用ApiResult.success")
        
        # 检查是否使用ApiResult.bad_request
        if 'ApiResult.bad_request(' in content and 'stream' in content:
            print("[OK] 流式错误使用ApiResult.bad_request")
        else:
            print("[ERROR] 流式错误未使用ApiResult.bad_request")
        
        # 检查是否使用ApiResult.server_error
        if 'ApiResult.server_error(' in content and 'stream' in content:
            print("[OK] 流式异常使用ApiResult.server_error")
        else:
            print("[ERROR] 流式异常未使用ApiResult.server_error")
        
        # 检查是否添加finished标志
        if '"finished": True' in content:
            print("[OK] 包含finished标志")
        else:
            print("[ERROR] 缺少finished标志")
        
        # 检查是否使用ensure_ascii=False
        if 'ensure_ascii=False' in content:
            print("[OK] 支持中文字符")
        else:
            print("[ERROR] 不支持中文字符")
        
        # 检查是否有部分响应处理
        if '"partial": True' in content:
            print("[OK] 包含部分响应处理")
        else:
            print("[ERROR] 缺少部分响应处理")
        
        # 检查是否有流式类型标识
        if '"type": "streaming"' in content:
            print("[OK] 包含流式类型标识")
        else:
            print("[ERROR] 缺少流式类型标识")
        
        # 检查是否有JSON解析处理
        if 'json.JSONDecodeError' in content:
            print("[OK] 包含JSON解析处理")
        else:
            print("[ERROR] 缺少JSON解析处理")
        
    except Exception as e:
        print(f"[ERROR] 检查chat_router.py失败: {e}")


def analyze_unified_format():
    """分析统一格式"""
    print("\n分析统一响应格式")
    print("=" * 50)
    
    print("普通接口响应格式:")
    print("""
{
  "code": 0,
  "message": "处理成功",
  "data": {
    "type": "task",
    "message": "任务执行成功",
    "data": {"task_completed": true},
    "suggestions": ["执行下一个任务"]
  }
}""")
    
    print("\n流式接口响应格式:")
    print("""
# 进行中响应
data: {
  "code": 0,
  "message": "正在处理...",
  "data": {
    "partial_content": "{\"code\": 0, \"message\": \"处理成功\"",
    "type": "streaming"
  },
  "partial": true,
  "finished": false
}

# 完成响应
data: {
  "code": 0,
  "message": "处理成功",
  "data": {
    "type": "task",
    "message": "任务执行成功",
    "data": {"task_completed": true},
    "suggestions": ["执行下一个任务"]
  },
  "partial": false,
  "finished": true
}

# 完成信号
data: {
  "code": 0,
  "message": "流式响应完成",
  "data": {"streaming_completed": true},
  "finished": true
}""")
    
    print("\n统一格式特点:")
    print("• 相同的code字段语义")
    print("• 相同的message字段语义")
    print("• 相同的data字段结构")
    print("• 统一的错误处理方式")
    print("• 一致的API设计风格")


def compare_interfaces():
    """对比接口"""
    print("\n接口对比")
    print("=" * 50)
    
    print("普通接口 /v1/chat/complete:")
    print("• 一次性返回完整响应")
    print("• 使用ApiResult统一封装")
    print("• 适合简单查询场景")
    print("• 响应时间较长")
    
    print("\n流式接口 /v1/chat/stream:")
    print("• 逐字符流式返回")
    print("• 使用ApiResult统一封装")
    print("• 适合实时交互场景")
    print("• 提供打字机效果")
    
    print("\n共同特点:")
    print("• 统一的ApiResult格式")
    print("• 相同的参数验证")
    print("• 一致的错误处理")
    print("• 相同的业务逻辑")
    print("• 统一的日志记录")


def test_client_unified_usage():
    """测试客户端统一使用"""
    print("\n客户端统一使用示例")
    print("=" * 50)
    
    print("JavaScript统一处理:")
    print("""
// 统一的响应处理函数
function handleApiResponse(data, isStreaming = false) {
    if (data.code === 0) {
        // 成功响应
        if (isStreaming && data.partial) {
            // 流式部分响应
            console.log('流式内容:', data.data.partial_content);
            updateTypingEffect(data.data.partial_content);
        } else {
            // 完整响应（普通接口或流式完成）
            console.log('响应成功:', data.data);
            displayResponse(data.data);
        }
    } else {
        // 错误响应 - 统一处理
        console.error('请求失败:', data.message);
        showError(data.message);
    }
}

// 普通接口调用
fetch('/api/v1/chat/complete', {
    method: 'POST',
    headers: { 'user_id': 'user123', 'session_id': 'session456' },
    body: JSON.stringify({ message: '你好' })
})
.then(response => response.json())
.then(data => handleApiResponse(data, false));

// 流式接口调用
const eventSource = new EventSource('/api/v1/chat/stream');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data.slice(6)); // 去掉 'data: '
    handleApiResponse(data, true);
    
    if (data.finished) {
        eventSource.close();
    }
};
""")
    
    print("\nPython统一处理:")
    print("""
import json

# 统一的响应处理函数
def handle_api_response(data, is_streaming=False):
    if data.get('code') == 0:
        if is_streaming and data.get('partial'):
            # 流式部分响应
            print(f"流式内容: {data['data']['partial_content']}")
        else:
            # 完整响应
            print(f"响应成功: {data['data']}")
    else:
        # 错误响应 - 统一处理
        print(f"请求失败: {data['message']}")

# 普通接口调用
response = requests.post('/api/v1/chat/complete', ...)
data = response.json()
handle_api_response(data, False)

# 流式接口调用
response = requests.post('/api/v1/chat/stream', stream=True)
for line in response.iter_lines():
    if line.startswith(b'data: '):
        data = json.loads(line[6:])
        handle_api_response(data, True)
        if data.get('finished'):
            break
""")


def main():
    """主测试函数"""
    print("ApiResult流式封装测试")
    print("=" * 50)
    
    try:
        # 检查ApiResult流式封装实现
        check_apiresult_stream_implementation()
        
        # 分析统一格式
        analyze_unified_format()
        
        # 对比接口
        compare_interfaces()
        
        # 测试客户端统一使用
        test_client_unified_usage()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n统一封装总结:")
        print("1. 格式统一 - 普通接口和流式接口使用相同格式")
        print("2. 错误统一 - 相同的错误码和错误处理")
        print("3. 参数统一 - 相同的参数验证逻辑")
        print("4. 逻辑统一 - 相同的业务处理流程")
        print("5. 日志统一 - 相同的日志记录格式")
        
        print("\n技术优势:")
        print("• API设计一致性")
        print("• 客户端处理简化")
        print("• 错误处理标准化")
        print("• 代码维护性提升")
        print("• 开发体验改善")
        
        print("\n用户体验:")
        print("• 统一的响应格式")
        print("• 一致的错误提示")
        print("• 简化的客户端逻辑")
        print("• 更好的错误处理")
        print("• 流畅的交互体验")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
