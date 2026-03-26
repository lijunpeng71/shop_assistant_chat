#!/usr/bin/env python3
"""
测试API响应格式 - 验证统一的响应结构
"""

import re


def check_api_response_format():
    """检查API响应格式"""
    print("检查API响应格式")
    print("=" * 50)
    
    # 检查chat_router.py中的响应格式
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查是否使用ApiResult统一响应
        if 'ApiResult.success(' in content:
            print("[OK] 使用ApiResult.success成功响应")
        else:
            print("[ERROR] 未使用ApiResult.success")
        
        if 'ApiResult.bad_request(' in content:
            print("[OK] 使用ApiResult.bad_request错误响应")
        else:
            print("[ERROR] 未使用ApiResult.bad_request")
        
        if 'ApiResult.forbidden(' in content:
            print("[OK] 使用ApiResult.forbidden权限错误响应")
        else:
            print("[ERROR] 未使用ApiResult.forbidden")
        
        if 'ApiResult.server_error(' in content:
            print("[OK] 使用ApiResult.server_error服务器错误响应")
        else:
            print("[ERROR] 未使用ApiResult.server_error")
        
        # 检查响应格式是否符合要求
        success_responses = re.findall(r'"code": 0', content)
        print(f"[OK] 成功响应code=0数量: {len(success_responses)}")
        
        # 检查错误响应格式
        error_codes = re.findall(r'"code": \d+', content)
        print(f"[OK] 错误响应code数量: {len(error_codes)}")
        
        # 检查data字段
        data_fields = re.findall(r'"data":', content)
        print(f"[OK] data字段数量: {len(data_fields)}")
        
        # 检查message字段
        message_fields = re.findall(r'"message":', content)
        print(f"[OK] message字段数量: {len(message_fields)}")
        
    except Exception as e:
        print(f"[ERROR] 检查chat_router.py失败: {e}")


def check_result_class():
    """检查ApiResult类"""
    print("\n检查ApiResult类")
    print("=" * 50)
    
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/common/result.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: common/result.py")
        
        # 检查成功响应格式
        if '"code": 0' in content:
            print("[OK] 成功响应使用code=0")
        else:
            print("[ERROR] 成功响应未使用code=0")
        
        # 检查各种错误码
        error_codes = {
            '400': 'bad_request',
            '401': 'unauthorized', 
            '403': 'forbidden',
            '404': 'not_found',
            '500': 'server_error'
        }
        
        for code, method in error_codes.items():
            if f'"code": {code}' in content:
                print(f"[OK] {method}使用code={code}")
            else:
                print(f"[ERROR] {method}未使用code={code}")
        
        # 检查响应结构
        response_structure = ['"code":', '"message":', '"data":']
        for field in response_structure:
            if field in content:
                print(f"[OK] 包含{field}字段")
            else:
                print(f"[ERROR] 缺少{field}字段")
        
    except Exception as e:
        print(f"[ERROR] 检查result.py失败: {e}")


def check_error_handling():
    """检查错误处理"""
    print("\n检查错误处理")
    print("=" * 50)
    
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/api/chat_router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: api/chat_router.py")
        
        # 检查user_id验证
        if 'if not user_id:' in content:
            print("[OK] 包含user_id验证")
        else:
            print("[ERROR] 缺少user_id验证")
        
        # 检查session_id验证
        if 'if not session_id:' in content:
            print("[OK] 包含session_id验证")
        else:
            print("[ERROR] 缺少session_id验证")
        
        # 检查异常处理类型
        exception_types = ['ValueError', 'PermissionError', 'Exception']
        for exc_type in exception_types:
            if f'except {exc_type}' in content:
                print(f"[OK] 包含{exc_type}异常处理")
            else:
                print(f"[WARNING] 缺少{exc_type}异常处理")
        
        # 检查错误消息格式
        error_messages = re.findall(r'message="[^"]*"', content)
        print(f"[OK] 错误消息数量: {len(error_messages)}")
        
        # 检查错误数据
        error_data = re.findall(r'data=\{"error":', content)
        print(f"[OK] 错误数据数量: {len(error_data)}")
        
    except Exception as e:
        print(f"[ERROR] 检查错误处理失败: {e}")


def analyze_response_examples():
    """分析响应示例"""
    print("\n分析响应示例")
    print("=" * 50)
    
    # 成功响应示例
    success_example = {
        "code": 0,
        "message": "处理成功",
        "data": {
            "type": "task",
            "message": "任务执行成功",
            "data": {"task_completed": True},
            "suggestions": ["执行下一个任务"]
        }
    }
    
    print("成功响应示例:")
    print(f"code: {success_example['code']}")
    print(f"message: {success_example['message']}")
    print(f"data: {success_example['data']}")
    
    # 错误响应示例
    error_examples = [
        {
            "code": 400,
            "message": "缺少用户ID，请在请求头中提供user_id",
            "data": {"error": "Missing user_id header"}
        },
        {
            "code": 403,
            "message": "权限不足: 用户无权限执行此操作",
            "data": {"error": "用户无权限执行此操作"}
        },
        {
            "code": 500,
            "message": "聊天处理失败，请稍后重试",
            "data": {"error": "Connection timeout"}
        }
    ]
    
    print("\n错误响应示例:")
    for i, example in enumerate(error_examples, 1):
        print(f"\n错误示例{i}:")
        print(f"code: {example['code']}")
        print(f"message: {example['message']}")
        print(f"data: {example['data']}")


def main():
    """主测试函数"""
    print("API响应格式测试")
    print("=" * 50)
    
    try:
        # 检查API响应格式
        check_api_response_format()
        
        # 检查ApiResult类
        check_result_class()
        
        # 检查错误处理
        check_error_handling()
        
        # 分析响应示例
        analyze_response_examples()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n响应格式总结:")
        print("1. 成功响应: code=0, 内容放到data中")
        print("2. 错误响应: code=错误码, 错误消息放到message中")
        print("3. 统一结构: {code, message, data}")
        print("4. 错误码规范: 400(参数错误), 401(未授权), 403(禁止), 404(不存在), 500(服务器错误)")
        print("5. 验证机制: user_id和session_id必需验证")
        
        print("\nAPI响应格式特点:")
        print("• 统一的响应结构")
        print("• 明确的错误分类")
        print("• 详细的错误信息")
        print("• 完整的数据传递")
        print("• 标准的HTTP状态码对应")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
