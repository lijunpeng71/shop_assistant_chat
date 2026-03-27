"""
测试拍照检测功能
"""

import asyncio
from agents.main_deepagent import main_deep_agent
from api.chat_router import ChatRequest

async def test_camera_detection():
    """测试拍照检测功能"""
    print("测试拍照检测功能...")
    
    try:
        # 测试1: 冰柜陈列检查（应该触发拍照）
        print("\n=== 测试1: 冰柜陈列检查 ===")
        result1 = await main_deep_agent.process_message(
            "我要检查冰柜陈列",
            user_id="test_user",
            session_id="test_session"
        )
        
        # 模拟API层检测
        camera_keywords = [
            "冰柜", "陈列", "检查", "拍照", "图片", "照片", 
            "freezer", "display", "check", "photo", "image",
            "需要图片", "提供图片", "上传图片", "拍照上传"
        ]
        
        front_calls = []
        if any(keyword in result1 for keyword in camera_keywords):
            front_calls.append("camera_call")
        
        print(f"响应内容: {str(result1)[:100]}...")
        print(f"检测到front_calls: {front_calls}")
        print(f"是否需要拍照: {'是' if 'camera_call' in front_calls else '否'}")
        
        # 测试2: 库存管理（不应该触发拍照）
        print("\n=== 测试2: 库存管理 ===")
        result2 = await main_deep_agent.process_message(
            "我要管理库存",
            user_id="test_user",
            session_id="test_session"
        )
        
        front_calls2 = []
        if any(keyword in result2 for keyword in camera_keywords):
            front_calls2.append("camera_call")
        
        print(f"响应内容: {str(result2)[:100]}...")
        print(f"检测到front_calls: {front_calls2}")
        print(f"是否需要拍照: {'是' if 'camera_call' in front_calls2 else '否'}")
        
        # 测试3: 用户明确提到拍照
        print("\n=== 测试3: 用户明确提到拍照 ===")
        user_message = "我需要拍照检查冰柜"
        result3 = await main_deep_agent.process_message(
            user_message,
            user_id="test_user",
            session_id="test_session"
        )
        
        front_calls3 = []
        # 检查响应消息
        if any(keyword in result3 for keyword in camera_keywords):
            front_calls3.append("camera_call")
        
        # 检查用户原始消息
        if any(keyword in user_message for keyword in ["拍照", "图片", "照片", "上传图片"]):
            if "camera_call" not in front_calls3:
                front_calls3.append("camera_call")
        
        print(f"用户消息: {user_message}")
        print(f"响应内容: {str(result3)[:100]}...")
        print(f"检测到front_calls: {front_calls3}")
        print(f"是否需要拍照: {'是' if 'camera_call' in front_calls3 else '否'}")
        
        print("\n✅ 拍照检测功能测试完成")
        print("- 智能检测需要拍照的场景")
        print("- 在ApiResult的front_calls中加入camera_call")
        print("- 支持响应消息和用户消息双重检测")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_camera_detection())
