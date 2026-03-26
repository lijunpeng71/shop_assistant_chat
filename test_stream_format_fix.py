#!/usr/bin/env python3
"""
测试流式响应格式修复 - 验证避免嵌套data字段
"""

import re


def check_stream_format_fix():
    """检查流式格式修复"""
    print("检查流式格式修复")
    print("=" * 50)
    
    # 检查chat_router.py中的格式修复
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查是否避免了嵌套data字段
        if '"response": parsed_data.get("data")' in content:
            print("[OK] 使用response字段避免嵌套")
        else:
            print("[ERROR] 仍然存在嵌套data字段")
        
        # 检查部分响应是否简化
        if '"partial_content": partial_content' in content:
            print("[OK] 部分响应格式简化")
        else:
            print("[ERROR] 部分响应格式未简化")
        
        # 检查是否移除了嵌套结构
        nested_patterns = [
            '"data": {"partial_content":',
            '"data": {"type": "streaming"',
            '"type": "streaming"'
        ]
        
        nested_found = False
        for pattern in nested_patterns:
            if pattern in content:
                nested_found = True
                print(f"[WARNING] 仍存在嵌套模式: {pattern}")
        
        if not nested_found:
            print("[OK] 成功移除嵌套结构")
        
        # 检查流式响应字段
        stream_fields = ['"partial":', '"finished":', '"partial_content":']
        for field in stream_fields:
            if field in content:
                print(f"[OK] 包含流式字段: {field}")
            else:
                print(f"[ERROR] 缺少流式字段: {field}")
        
        # 检查响应字段
        if '"response":' in content:
            print("[OK] 使用response字段")
        else:
            print("[ERROR] 未使用response字段")
        
    except Exception as e:
        print(f"[ERROR] 检查chat_router.py失败: {e}")


def analyze_fixed_format():
    """分析修复后的格式"""
    print("\n分析修复后的格式")
    print("=" * 50)
    
    print("修复前的问题格式:")
    print("""
data: {
  "code": 0,
  "message": "正在处理...",
  "data": {                    // 嵌套的data字段
    "partial_content": "...",
    "type": "streaming"
  },
  "partial": true,
  "finished": false
}""")
    
    print("\n修复后的正确格式:")
    print("""
# 进行中响应
data: {
  "code": 0,
  "message": "正在处理...",
  "partial_content": "{\\"code\\": 0, \\"message\\": \\"处理成功\\", \\"data\\": {\\"type\\": \\"welcome\\", \\"message\\": \\"欢迎使用智能助手！",
  "partial": true,
  "finished": false
}

# 完成响应
data: {
  "code": 0,
  "message": "处理成功",
  "response": {                // 使用response字段
    "type": "welcome",
    "message": "欢迎使用智能助手！我可以帮您执行任务、管理采购、搜索信息等。请告诉我您需要什么帮助？",
    "data": null,
    "suggestions": ["我要执行任务", "我要采购商品", "搜索信息"]
  },
  "partial": false,
  "finished": true
}""")
    
    print("\n格式特点:")
    print("• 避免了嵌套的data字段")
    print("• 部分响应使用partial_content字段")
    print("• 完成响应使用response字段")
    print("• 保持ApiResult的基本结构")
    print("• 流式字段清晰明确")


def compare_formats():
    """对比格式"""
    print("\n格式对比")
    print("=" * 50)
    
    print("普通接口格式:")
    print("""
{
  "code": 0,
  "message": "处理成功",
  "data": {                    // 业务数据
    "type": "welcome",
    "message": "欢迎使用智能助手！",
    "data": null,
    "suggestions": ["我要执行任务"]
  }
}""")
    
    print("\n流式接口格式:")
    print("""
# 进行中
data: {
  "code": 0,
  "message": "正在处理...",
  "partial_content": "...",
  "partial": true,
  "finished": false
}

# 完成
data: {
  "code": 0,
  "message": "处理成功",
  "response": {                // 业务数据
    "type": "welcome",
    "message": "欢迎使用智能助手！",
    "data": null,
    "suggestions": ["我要执行任务"]
  },
  "partial": false,
  "finished": true
}""")
    
    print("\n一致性:")
    print("• code字段语义相同")
    print("• message字段语义相同")
    print("• 业务数据结构相同")
    print("• 错误处理方式相同")
    print("• 流式字段额外提供")


def test_client_handling():
    """测试客户端处理"""
    print("\n客户端处理示例")
    print("=" * 50)
    
    print("JavaScript处理:")
    print("""
function handleStreamResponse(data) {
    if (data.code === 0) {
        if (data.partial) {
            // 进行中响应
            if (data.partial_content) {
                // 显示部分内容（可选）
                console.log('部分内容:', data.partial_content);
            }
        } else {
            // 完成响应
            if (data.response) {
                // 处理业务数据
                console.log('响应数据:', data.response);
                displayResponse(data.response);
            }
        }
    } else {
        // 错误处理
        console.error('错误:', data.message);
    }
}

// 流式处理
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data.slice(6));
    handleStreamResponse(data);
    
    if (data.finished) {
        eventSource.close();
    }
};
""")
    
    print("\nPython处理:")
    print("""
def handle_stream_response(data):
    if data.get('code') == 0:
        if data.get('partial'):
            # 进行中响应
            if 'partial_content' in data:
                print(f"部分内容: {data['partial_content']}")
        else:
            # 完成响应
            if 'response' in data:
                print(f"响应数据: {data['response']}")
                process_response(data['response'])
    else:
        print(f"错误: {data['message']}")

# 流式处理
for line in response.iter_lines():
    if line.startswith(b'data: '):
        data = json.loads(line[6:])
        handle_stream_response(data)
        if data.get('finished'):
            break
""")


def main():
    """主测试函数"""
    print("流式响应格式修复测试")
    print("=" * 50)
    
    try:
        # 检查流式格式修复
        check_stream_format_fix()
        
        # 分析修复后的格式
        analyze_fixed_format()
        
        # 对比格式
        compare_formats()
        
        # 测试客户端处理
        test_client_handling()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n修复总结:")
        print("1. 避免嵌套 - 移除嵌套的data字段")
        print("2. 字段重命名 - 使用response字段替代嵌套data")
        print("3. 格式简化 - 部分响应直接使用partial_content")
        print("4. 结构清晰 - 流式字段与业务数据分离")
        print("5. 一致性保持 - 与普通接口保持基本结构一致")
        
        print("\n技术优势:")
        print("• 格式清晰明确")
        print("• 避免字段嵌套混乱")
        print("• 客户端处理简化")
        print("• 错误定位准确")
        print("• 调试难度降低")
        
        print("\n用户体验:")
        print("• 响应格式统一")
        print("• 错误信息清晰")
        print("• 部分内容可见")
        print("• 完成数据完整")
        print("• 交互体验流畅")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
