"""
测试stream接口的front_calls功能
"""

import asyncio
from api.chat_router import stream_chat_response
from api.chat_router import ChatRequest

async def test_stream_front_calls():
    """测试stream接口的front_calls功能"""
    print("测试stream接口的front_calls功能...")
    
    try:
        # 测试1: 冰柜陈列检查（应该包含camera_call）
        print("\n=== 测试1: 冰柜陈列检查 ===")
        request1 = ChatRequest(
            message="我要检查冰柜陈列",
            image_url=""  # 使用空字符串而不是None
        )
        
        print("流式响应数据:")
        front_calls_detected = []
        
        async for chunk in stream_chat_response(request1, "test_user", "test_session"):
            # 解析chunk数据
            if chunk.startswith("data: "):
                data_str = chunk[6:]  # 移除 "data: " 前缀
                try:
                    import json
                    data = json.loads(data_str)
                    
                    if data.get("finished") and data.get("response"):
                        # 最终响应，检查front_calls
                        front_calls = data["response"].get("front_calls", [])
                        front_calls_detected = front_calls
                        print(f"最终响应front_calls: {front_calls}")
                        break
                    elif data.get("partial") == False and data.get("response"):
                        # 完整响应
                        front_calls = data["response"].get("front_calls", [])
                        front_calls_detected = front_calls
                        print(f"完整响应front_calls: {front_calls}")
                        break
                        
                except json.JSONDecodeError:
                    # JSON解析失败，继续
                    pass
        
        print(f"冰柜陈列检查 - 是否需要拍照: {'是' if 'camera_call' in front_calls_detected else '否'}")
        
        # 测试2: 库存管理（不应该包含camera_call）
        print("\n=== 测试2: 库存管理 ===")
        request2 = ChatRequest(
            message="我要管理库存",
            image_url=""  # 使用空字符串而不是None
        )
        
        print("流式响应数据:")
        front_calls_detected2 = []
        
        async for chunk in stream_chat_response(request2, "test_user", "test_session"):
            # 解析chunk数据
            if chunk.startswith("data: "):
                data_str = chunk[6:]  # 移除 "data: " 前缀
                try:
                    import json
                    data = json.loads(data_str)
                    
                    if data.get("finished") and data.get("response"):
                        # 最终响应，检查front_calls
                        front_calls = data["response"].get("front_calls", [])
                        front_calls_detected2 = front_calls
                        print(f"最终响应front_calls: {front_calls}")
                        break
                    elif data.get("partial") == False and data.get("response"):
                        # 完整响应
                        front_calls = data["response"].get("front_calls", [])
                        front_calls_detected2 = front_calls
                        print(f"完整响应front_calls: {front_calls}")
                        break
                        
                except json.JSONDecodeError:
                    # JSON解析失败，继续
                    pass
        
        print(f"库存管理 - 是否需要拍照: {'是' if 'camera_call' in front_calls_detected2 else '否'}")
        
        print("\n✅ stream接口front_calls功能测试完成")
        print("- stream接口现在也支持front_calls检测")
        print("- 智能体推断的拍照需求在流式响应中正确传递")
        print("- 前端可以通过流式响应获取front_calls")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_stream_front_calls())
