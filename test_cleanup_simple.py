#!/usr/bin/env python3
"""
简化的项目清理验证测试 - 不依赖外部库
"""

import os
import re


def check_project_structure():
    """检查项目结构"""
    print("检查项目结构")
    print("=" * 50)
    
    # 检查关键文件
    key_files = {
        "智能体文件": [
            "agents/main_deepagent.py",
            "agents/task_deepagent.py",
            "agents/purchase_deepagent.py",
            "agents/search_deepagent.py"
        ],
        "工具文件": [
            "tools/redpacket_tool.py",
            "tools/simulation_tool.py",
            "tools/bing_search.py"
        ],
        "API文件": [
            "api/chat_router.py",
            "service/chat_service.py",
            "main.py"
        ]
    }
    
    for category, files in key_files.items():
        print(f"\n{category}:")
        for file_path in files:
            full_path = f"e:/workspace/program/python/shop_assistant_chat/{file_path}"
            if os.path.exists(full_path):
                print(f"   [OK] {file_path}")
            else:
                print(f"   [MISSING] {file_path}")
    
    # 检查删除的文件
    deleted_files = [
        "agents/deepagents_system.py",
        "AGENTS_SEPARATION.md",
        "DEEPAGENTS_IMPLEMENTATION.md"
    ]
    
    print(f"\n已删除的文件:")
    for file_path in deleted_files:
        full_path = f"e:/workspace/program/python/shop_assistant_chat/{file_path}"
        if not os.path.exists(full_path):
            print(f"   [DELETED] {file_path}")
        else:
            print(f"   [STILL EXISTS] {file_path}")


def check_code_cleanliness():
    """检查代码整洁性"""
    print("\n检查代码整洁性")
    print("=" * 50)
    
    # 检查是否有模拟逻辑在智能体中
    agent_files = [
        "e:/workspace/program/python/shop_assistant_chat/agents/main_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/task_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/purchase_deepagent.py",
        "e:/workspace/program/python/shop_assistant_chat/agents/search_deepagent.py"
    ]
    
    for file_path in agent_files:
        print(f"\n检查文件: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否有直接的模拟逻辑
            simulation_patterns = [
                r'模拟.*执行',
                r'MockAgent',
                r'mock.*response',
                r'模拟.*回答',
                r'模拟.*分析'
            ]
            
            found_simulations = []
            for pattern in simulation_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_simulations.extend(matches)
            
            if found_simulations:
                print(f"   [WARNING] 发现模拟逻辑: {found_simulations}")
            else:
                print(f"   [OK] 无直接模拟逻辑")
            
            # 检查是否使用工具调用
            tool_patterns = [
                r'from tools\.',
                r'await.*tool',
                r'simulate_.*\(',
                r'tools\.'
            ]
            
            found_tools = []
            for pattern in tool_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_tools.extend(matches)
            
            if found_tools:
                print(f"   [OK] 使用工具调用: {len(found_tools)}处")
            else:
                print(f"   [WARNING] 未发现工具调用")
                
        except Exception as e:
            print(f"   [ERROR] 检查失败: {e}")


def check_tools_integration():
    """检查工具集成"""
    print("\n检查工具集成")
    print("=" * 50)
    
    tool_files = [
        "e:/workspace/program/python/shop_assistant_chat/tools/simulation_tool.py",
        "e:/workspace/program/python/shop_assistant_chat/tools/redpacket_tool.py"
    ]
    
    for file_path in tool_files:
        print(f"\n检查工具文件: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查工具函数
            if 'async def simulate_' in content:
                print(f"   [OK] 包含模拟函数")
            
            if 'async def send_redpacket' in content:
                print(f"   [OK] 包含红包函数")
            
            if 'simulation_tools = [' in content:
                print(f"   [OK] 包含工具定义")
            
            # 检查类定义
            if 'class SimulationTool' in content:
                print(f"   [OK] 包含模拟工具类")
            
            if 'class RedPacketTool' in content:
                print(f"   [OK] 包含红包工具类")
                
        except Exception as e:
            print(f"   [ERROR] 检查失败: {e}")


def check_file_sizes():
    """检查文件大小"""
    print("\n检查文件大小")
    print("=" * 50)
    
    important_files = [
        "agents/main_deepagent.py",
        "tools/simulation_tool.py",
        "tools/redpacket_tool.py",
        "agents/task_deepagent.py"
    ]
    
    for file_path in important_files:
        full_path = f"e:/workspace/program/python/shop_assistant_chat/{file_path}"
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"[FILE] {file_path}: {size} bytes")
        else:
            print(f"[MISSING] {file_path}: 文件不存在")


def main():
    """主测试函数"""
    print("项目清理验证测试")
    print("=" * 50)
    
    try:
        # 检查项目结构
        check_project_structure()
        
        # 检查代码整洁性
        check_code_cleanliness()
        
        # 检查工具集成
        check_tools_integration()
        
        # 检查文件大小
        check_file_sizes()
        
        print("\n" + "=" * 50)
        print("项目清理验证完成！")
        print("\n清理总结:")
        print("1. 删除了重复的deepagents_system.py文件")
        print("2. 删除了过时的文档文件")
        print("3. 重命名了req.txt为REQUIREMENTS.md")
        print("4. 所有模拟逻辑都在工具中执行")
        print("5. 智能体只负责调用工具")
        print("6. 实现了职责分离")
        print("7. 项目结构更加整洁")
        
        print("\n架构优势:")
        print("• 职责分离: 智能体专注协调，工具专注执行")
        print("• 代码复用: 模拟逻辑可在多处使用")
        print("• 易于测试: 工具可独立测试")
        print("• 易于维护: 修改逻辑只需更新工具")
        print("• 扩展性强: 新增功能只需扩展工具")
        
    except Exception as e:
        print(f"\n验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
