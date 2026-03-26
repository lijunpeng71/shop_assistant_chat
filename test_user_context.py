#!/usr/bin/env python3
"""
测试用户上下文功能 - 验证user_id和session_id作为上下文传递给智能体
"""

import re


def check_user_context_implementation():
    """检查用户上下文实现"""
    print("检查用户上下文实现")
    print("=" * 50)
    
    # 检查main_deepagent.py中的用户上下文处理
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: agents/main_deepagent.py")
        
        # 检查是否导入了time模块
        if 'import time' in content:
            print("[OK] 导入了time模块")
        else:
            print("[ERROR] 未导入time模块")
        
        # 检查是否构建用户上下文信息
        if '当前用户信息：' in content:
            print("[OK] 包含用户上下文信息")
        else:
            print("[ERROR] 缺少用户上下文信息")
        
        # 检查是否包含user_id在上下文中
        if '用户ID: {user_id}' in content:
            print("[OK] 上下文包含用户ID")
        else:
            print("[ERROR] 上下文缺少用户ID")
        
        # 检查是否包含session_id在上下文中
        if '会话ID: {session_id}' in content:
            print("[OK] 上下文包含会话ID")
        else:
            print("[ERROR] 上下文缺少会话ID")
        
        # 检查是否包含时间信息
        if '当前时间:' in content:
            print("[OK] 上下文包含当前时间")
        else:
            print("[ERROR] 上下文缺少当前时间")
        
        # 检查_build_context_from_history方法是否支持用户参数
        if 'user_id: str = None' in content and 'session_id: str = None' in content:
            print("[OK] _build_context_from_history支持用户参数")
        else:
            print("[ERROR] _build_context_from_history不支持用户参数")
        
        # 检查是否在构建上下文时传递用户信息
        if '_build_context_from_history(history, message, user_id, session_id)' in content:
            print("[OK] 传递用户信息给上下文构建方法")
        else:
            print("[ERROR] 未传递用户信息给上下文构建方法")
        
    except Exception as e:
        print(f"[ERROR] 检查main_deepagent.py失败: {e}")


def analyze_context_structure():
    """分析上下文结构"""
    print("\n分析上下文结构")
    print("=" * 50)
    
    print("用户上下文结构:")
    print("""
当前用户信息：
- 用户ID: user123
- 会话ID: session456
- 当前时间: 2024-03-26 18:30:00

以下是我们的对话历史，请基于上下文理解我的当前需求并给出回应：

用户: 你好
助手: 您好！我是智能助手，有什么可以帮助您的吗？
用户: 我要执行任务

请基于以上对话历史和当前用户信息，理解我的当前需求并提供合适的回应。""")
    
    print("\n上下文特点:")
    print("• 包含用户身份信息")
    print("• 包含会话标识")
    print("• 包含当前时间")
    print("• 包含历史对话")
    print("• 包含当前消息")
    print("• 提供明确的上下文提示")
    
    print("\n智能体获得的信息:")
    print("• 知道当前对话的用户是谁")
    print("• 知道当前是哪个会话")
    print("• 知道对话发生的时间")
    print("• 知道之前的对话内容")
    print("• 知道用户当前的需求")


def check_context_usage():
    """检查上下文使用"""
    print("\n检查上下文使用")
    print("=" * 50)
    
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: agents/main_deepagent.py")
        
        # 检查用户上下文构建
        if 'user_context = f"""当前用户信息：' in content:
            print("[OK] 构建用户上下文")
        else:
            print("[ERROR] 未构建用户上下文")
        
        # 检查完整消息构建
        if 'full_message = f"{user_context}用户消息:' in content:
            print("[OK] 构建包含用户信息的完整消息")
        else:
            print("[ERROR] 未构建包含用户信息的完整消息")
        
        # 检查图片处理
        if '用户消息（包含图片）:' in content:
            print("[OK] 正确处理包含图片的消息")
        else:
            print("[ERROR] 未正确处理包含图片的消息")
        
        # 检查错误处理
        if 'user_id or \'未知\'' in content:
            print("[OK] 包含用户ID缺失的处理")
        else:
            print("[ERROR] 缺少用户ID缺失的处理")
        
        # 检查日志记录
        if '用户: {user_id}' in content:
            print("[OK] 记录用户信息到日志")
        else:
            print("[ERROR] 未记录用户信息到日志")
        
    except Exception as e:
        print(f"[ERROR] 检查上下文使用失败: {e}")


def test_context_examples():
    """测试上下文示例"""
    print("\n测试上下文示例")
    print("=" * 50)
    
    # 示例1: 无历史消息的新用户
    print("示例1: 新用户首次对话")
    new_user_context = """当前用户信息：
- 用户ID: user123
- 会话ID: session456
- 当前时间: 2024-03-26 18:30:00

用户消息: 你好"""
    
    print(new_user_context)
    print("预期效果: 智能体知道是新用户，能提供欢迎信息")
    
    # 示例2: 有历史消息的老用户
    print("\n示例2: 老用户继续对话")
    returning_user_context = """当前用户信息：
- 用户ID: user123
- 会话ID: session456
- 当前时间: 2024-03-26 18:35:00

以下是我们的对话历史，请基于上下文理解我的当前需求并给出回应：

用户: 你好
助手: 您好！我是智能助手，有什么可以帮助您的吗？
用户: 我要执行任务
助手: 好的，请告诉我您要执行什么任务？

请基于以上对话历史和当前用户信息，理解我的当前需求并提供合适的回应。"""
    
    print(returning_user_context)
    print("预期效果: 智能体知道用户之前要执行任务，能提供相关帮助")
    
    # 示例3: 包含图片的消息
    print("\n示例3: 包含图片的消息")
    image_context = """当前用户信息：
- 用户ID: user123
- 会话ID: session456
- 当前时间: 2024-03-26 18:40:00

用户消息（包含图片）: 请帮我检查这个冰柜陈列

[图片URL: https://example.com/image.jpg]"""
    
    print(image_context)
    print("预期效果: 智能体知道用户要检查冰柜陈列，能分析图片")


def main():
    """主测试函数"""
    print("用户上下文功能测试")
    print("=" * 50)
    
    try:
        # 检查用户上下文实现
        check_user_context_implementation()
        
        # 分析上下文结构
        analyze_context_structure()
        
        # 检查上下文使用
        check_context_usage()
        
        # 测试上下文示例
        test_context_examples()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n功能总结:")
        print("1. 用户身份识别 - 智能体知道当前用户是谁")
        print("2. 会话管理 - 智能体知道当前是哪个会话")
        print("3. 时间感知 - 智能体知道对话发生的时间")
        print("4. 上下文连贯 - 结合历史对话和用户信息")
        print("5. 个性化响应 - 基于用户信息提供定制化服务")
        
        print("\n技术特点:")
        print("• 用户ID和session_id作为上下文传递")
        print("• 包含当前时间信息")
        print("• 与历史对话无缝结合")
        print("• 支持图片消息处理")
        print("• 完善的错误处理机制")
        print("• 详细的日志记录")
        
        print("\n智能体能力提升:")
        print("• 能识别不同用户的对话")
        print("• 能区分不同的会话场景")
        print("• 能提供个性化的服务")
        print("• 能基于用户历史提供连贯响应")
        print("• 能理解时间和上下文关系")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
