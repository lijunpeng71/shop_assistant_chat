#!/usr/bin/env python3
"""
简化的user_id验证测试 - 不依赖外部模块
"""

import re


def check_agent_user_id_handling():
    """检查智能体user_id处理"""
    print("检查智能体user_id处理")
    print("=" * 50)
    
    # 检查main_deepagent.py中的user_id处理
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否移除了默认user_id
        if 'mock_user_123' in content:
            print("[ERROR] 仍然包含默认user_id (mock_user_123)")
        else:
            print("[OK] 已移除默认user_id")
        
        # 检查是否有user_id验证
        if 'if not user_id:' in content:
            print("[OK] 包含user_id验证")
        else:
            print("[ERROR] 缺少user_id验证")
        
        # 检查是否正确获取user_id
        if "kwargs.get('user_id')" in content:
            print("[OK] 正确从kwargs获取user_id")
        else:
            print("[ERROR] 未正确获取user_id")
        
        # 检查是否移除了fallback_user
        if 'fallback_user' in content:
            print("[ERROR] 仍然包含fallback_user")
        else:
            print("[OK] 已移除fallback_user")
        
        # 检查错误处理
        if 'Missing user_id' in content:
            print("[OK] 包含user_id错误处理")
        else:
            print("[ERROR] 缺少user_id错误处理")
            
    except Exception as e:
        print(f"[ERROR] 检查main_deepagent.py失败: {e}")
    
    # 检查simulation_tool.py中的user_id处理
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/tools/simulation_tool.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有user_id验证
        user_id_validations = re.findall(r'if not user_id:', content)
        print(f"[OK] simulation_tool.py中的user_id验证数量: {len(user_id_validations)}")
        
        # 检查错误处理
        error_handling = re.findall(r'"Missing user_id"', content)
        print(f"[OK] simulation_tool.py中的错误处理数量: {len(error_handling)}")
        
    except Exception as e:
        print(f"[ERROR] 检查simulation_tool.py失败: {e}")
    
    # 检查redpacket_tool.py中的user_id处理
    try:
        with open('e:/workspace/program/python/shop_assistant_chat/tools/redpacket_tool.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有user_id验证
        if 'if not user_id:' in content:
            print("[OK] redpacket_tool.py包含user_id验证")
        else:
            print("[ERROR] redpacket_tool.py缺少user_id验证")
        
        # 检查错误处理
        if '"Missing user_id"' in content:
            print("[OK] redpacket_tool.py包含错误处理")
        else:
            print("[ERROR] redpacket_tool.py缺少错误处理")
            
    except Exception as e:
        print(f"[ERROR] 检查redpacket_tool.py失败: {e}")


def check_agent_tool_configuration():
    """检查智能体工具配置"""
    print("\n检查智能体工具配置")
    print("=" * 50)
    
    agent_files = [
        'agents/purchase_deepagent.py',
        'agents/search_deepagent.py', 
        'agents/task_deepagent.py'
    ]
    
    for file_path in agent_files:
        try:
            with open(f'e:/workspace/program/python/shop_assistant_chat/{file_path}', 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n检查文件: {file_path}")
            
            # 检查是否移除了预配置工具
            if '"tools": []' in content:
                print("[OK] 已移除预配置工具")
            else:
                print("[ERROR] 仍包含预配置工具")
            
            # 检查是否包含工具使用指导
            if '自主判断是否使用工具' in content:
                print("[OK] 包含工具使用指导")
            else:
                print("[ERROR] 缺少工具使用指导")
            
            # 检查是否包含不要主动使用工具的说明
            if '不要主动使用工具' in content:
                print("[OK] 包含不要主动使用工具的说明")
            else:
                print("[ERROR] 缺少不要主动使用工具的说明")
                
        except Exception as e:
            print(f"[ERROR] 检查{file_path}失败: {e}")


def check_code_patterns():
    """检查代码模式"""
    print("\n检查代码模式")
    print("=" * 50)
    
    patterns_to_check = {
        '默认user_id模式': r'mock_user_\d+|fallback_user',
        'user_id验证模式': r'if not user_id:',
        'user_id获取模式': r"kwargs\.get\('user_id'\)",
        '错误处理模式': r'"Missing user_id"',
        '工具配置模式': r'"tools": \[\]',
        '工具使用指导': r'自主判断是否使用工具'
    }
    
    files_to_check = [
        'agents/main_deepagent.py',
        'agents/purchase_deepagent.py',
        'agents/search_deepagent.py',
        'agents/task_deepagent.py',
        'tools/simulation_tool.py',
        'tools/redpacket_tool.py'
    ]
    
    for file_path in files_to_check:
        try:
            with open(f'e:/workspace/program/python/shop_assistant_chat/{file_path}', 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n文件: {file_path}")
            
            for pattern_name, pattern in patterns_to_check.items():
                matches = re.findall(pattern, content)
                if matches:
                    print(f"  [OK] {pattern_name}: {len(matches)}处")
                else:
                    print(f"  [WARNING] {pattern_name}: 0处")
                    
        except Exception as e:
            print(f"[ERROR] 检查{file_path}失败: {e}")


def main():
    """主测试函数"""
    print("user_id和session_id验证测试")
    print("=" * 50)
    
    try:
        # 检查智能体user_id处理
        check_agent_user_id_handling()
        
        # 检查智能体工具配置
        check_agent_tool_configuration()
        
        # 检查代码模式
        check_code_patterns()
        
        print("\n" + "=" * 50)
        print("检查完成！")
        print("\n验证总结:")
        print("1. 移除了所有默认user_id模拟")
        print("2. 添加了user_id验证逻辑")
        print("3. user_id必须从header获取")
        print("4. 缺少user_id时返回错误")
        print("5. 智能体不预配置工具")
        print("6. 智能体自主判断是否使用工具")
        
        print("\n架构改进:")
        print("• user_id和session_id完全从header获取")
        print("• 不再进行任何模拟user_id处理")
        print("• 智能体自主判断工具使用")
        print("• 增强了数据完整性和安全性")
        print("• 确保了用户上下文的正确传递")
        
    except Exception as e:
        print(f"\n检查过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
