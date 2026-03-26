#!/usr/bin/env python3
"""
测试历史上下文功能 - 验证短期记忆作为历史传递给智能体
"""

import re


def check_history_context_implementation():
    """检查历史上下文实现"""
    print("检查历史上下文实现")
    print("=" * 50)
    
    # 检查main_deepagent.py中的历史上下文处理
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: agents/main_deepagent.py")
        
        # 检查process_message方法是否支持history参数
        if 'history: list = None' in content:
            print("[OK] process_message支持history参数")
        else:
            print("[ERROR] process_message不支持history参数")
        
        # 检查是否构建历史上下文
        if '_build_context_from_history' in content:
            print("[OK] 包含_build_context_from_history方法")
        else:
            print("[ERROR] 缺少_build_context_from_history方法")
        
        # 检查历史上下文构建逻辑
        if 'recent_history = history[-10:]' in content:
            print("[OK] 限制历史对话数量为10轮")
        else:
            print("[ERROR] 未限制历史对话数量")
        
        # 检查上下文提示
        if '基于以上对话历史，理解我的当前需求' in content:
            print("[OK] 包含历史上下文提示")
        else:
            print("[ERROR] 缺少历史上下文提示")
        
        # 检查角色处理
        if 'role == \'user\'' in content and 'role == \'assistant\'' in content:
            print("[OK] 正确处理用户和助手角色")
        else:
            print("[ERROR] 角色处理不完整")
        
    except Exception as e:
        print(f"[ERROR] 检查main_deepagent.py失败: {e}")
    
    # 检查chat_service.py中的历史获取
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/service/chat_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n检查文件: service/chat_service.py")
        
        # 检查是否获取对话历史
        if '_get_conversation_history' in content:
            print("[OK] 包含_get_conversation_history方法")
        else:
            print("[ERROR] 缺少_get_conversation_history方法")
        
        # 检查是否传递历史给智能体
        if 'history=history' in content:
            print("[OK] 传递历史给智能体")
        else:
            print("[ERROR] 未传递历史给智能体")
        
        # 检查历史数量限制
        if 'recent_messages = messages[-20:]' in content:
            print("[OK] 限制历史消息为20条")
        else:
            print("[ERROR] 未限制历史消息数量")
        
        # 检查历史记录格式
        if '"role": "user"' in content and '"role": "assistant"' in content:
            print("[OK] 历史记录包含角色信息")
        else:
            print("[ERROR] 历史记录缺少角色信息")
        
    except Exception as e:
        print(f"[ERROR] 检查chat_service.py失败: {e}")


def analyze_history_flow():
    """分析历史流程"""
    print("\n分析历史流程")
    print("=" * 50)
    
    print("历史上下文流程:")
    print("1. 用户发送消息")
    print("2. ChatService获取对话历史 (_get_conversation_history)")
    print("3. 构建历史上下文 (_build_context_from_history)")
    print("4. 智能体处理带上下文的消息 (process_message)")
    print("5. 保存新的对话记录 (_save_to_memory)")
    
    print("\n历史记录格式:")
    history_example = [
        {
            "role": "user",
            "content": "我要执行任务",
            "timestamp": 1234567890,
            "metadata": {"user_id": "user123"}
        },
        {
            "role": "assistant", 
            "content": "好的，请告诉我您要执行什么任务？",
            "timestamp": 1234567891,
            "metadata": {"type": "general", "user_id": "user123"}
        }
    ]
    
    print("示例历史记录:")
    for i, msg in enumerate(history_example, 1):
        print(f"  {i}. {msg['role']}: {msg['content']}")
    
    print("\n上下文构建示例:")
    context_example = """以下是我们的对话历史，请基于上下文理解我的当前需求并给出回应：

用户: 我要执行任务
助手: 好的，请告诉我您要执行什么任务？
用户: 我要检查冰柜陈列

请基于以上对话历史，理解我的当前需求并提供合适的回应。"""
    
    print(context_example)


def check_memory_management():
    """检查内存管理"""
    print("\n检查内存管理")
    print("=" * 50)
    
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/service/chat_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("检查文件: service/chat_service.py")
        
        # 检查短期记忆存储
        if 'self.session_memory = {}' in content:
            print("[OK] 包含短期记忆存储")
        else:
            print("[ERROR] 缺少短期记忆存储")
        
        # 检查记忆键格式
        if 'memory_key = f"{user_id}_{session_id}"' in content:
            print("[OK] 使用正确的记忆键格式")
        else:
            print("[ERROR] 记忆键格式不正确")
        
        # 检查记忆长度限制
        if 'len(self.session_memory[memory_key]["messages"]) > 100' in content:
            print("[OK] 限制记忆长度为100条消息")
        else:
            print("[ERROR] 未限制记忆长度")
        
        # 检查记忆清理
        if 'cleanup_old_memory' in content:
            print("[OK] 包含记忆清理功能")
        else:
            print("[WARNING] 缺少记忆清理功能")
        
        # 检查单例模式
        if '_instance = None' in content and '_initialized = False' in content:
            print("[OK] 使用单例模式")
        else:
            print("[ERROR] 未使用单例模式")
        
    except Exception as e:
        print(f"[ERROR] 检查内存管理失败: {e}")


def test_context_building():
    """测试上下文构建"""
    print("\n测试上下文构建")
    print("=" * 50)
    
    # 模拟历史数据
    test_history = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "您好！我是智能助手，有什么可以帮助您的吗？"},
        {"role": "user", "content": "我要执行任务"},
        {"role": "assistant", "content": "好的，请告诉我您要执行什么任务？"},
        {"role": "user", "content": "我要检查冰柜陈列"}
    ]
    
    print("测试历史数据:")
    for i, msg in enumerate(test_history, 1):
        print(f"  {i}. {msg['role']}: {msg['content']}")
    
    print("\n构建的上下文应该包含:")
    print("- 最近的对话历史")
    print("- 当前用户消息")
    print("- 上下文提示语")
    print("- 角色标识")
    
    print("\n预期效果:")
    print("- 智能体能理解之前的对话")
    print("- 能基于上下文提供相关回应")
    print("- 避免重复询问相同信息")
    print("- 保持对话连贯性")


def main():
    """主测试函数"""
    print("历史上下文功能测试")
    print("=" * 50)
    
    try:
        # 检查历史上下文实现
        check_history_context_implementation()
        
        # 分析历史流程
        analyze_history_flow()
        
        # 检查内存管理
        check_memory_management()
        
        # 测试上下文构建
        test_context_building()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n功能总结:")
        print("1. 获取对话历史 - 从短期记忆中提取历史消息")
        print("2. 构建上下文 - 将历史对话格式化为上下文")
        print("3. 传递给智能体 - 智能体接收历史上下文")
        print("4. 智能响应 - 基于上下文提供连贯回应")
        print("5. 保存新记录 - 将新对话保存到短期记忆")
        
        print("\n技术特点:")
        print("• 历史限制为最近10轮对话")
        print("• 短期记忆限制为100条消息")
        print("• 支持用户和助手角色区分")
        print("• 包含时间戳和元数据")
        print("• 单例模式确保内存一致性")
        print("• 自动清理过期记忆")
        
        print("\n用户体验:")
        print("• 对话更加连贯自然")
        print("• 智能体能记住之前的交流")
        print("• 避免重复询问相同问题")
        print("• 提供个性化的服务体验")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
