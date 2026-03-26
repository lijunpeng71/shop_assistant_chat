# 📡 API响应格式规范

## 🎯 响应格式要求

- **成功响应**：`code=0`，成功的内容放到 `data` 中
- **失败响应**：`code` 对应错误码，错误消息放到 `message` 中
- **统一结构**：`{code, message, data}`

## ✅ 实现状态

### 1. **统一响应结构**

#### 成功响应
```json
{
  "code": 0,
  "message": "处理成功",
  "data": {
    "type": "task",
    "message": "任务执行成功",
    "data": {"task_completed": true, "redpacket_sent": true},
    "suggestions": ["执行下一个任务"]
  }
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "缺少用户ID，请在请求头中提供user_id",
  "data": {"error": "Missing user_id header"}
}
```

### 2. **错误码规范**

| 错误码 | 类型 | 说明 | ApiResult方法 |
|--------|------|------|---------------|
| 0 | 成功 | 请求成功 | `ApiResult.success()` |
| 400 | 客户端错误 | 请求参数错误 | `ApiResult.bad_request()` |
| 401 | 认证错误 | 未授权访问 | `ApiResult.unauthorized()` |
| 403 | 权限错误 | 禁止访问 | `ApiResult.forbidden()` |
| 404 | 资源错误 | 资源不存在 | `ApiResult.not_found()` |
| 500 | 服务器错误 | 服务器内部错误 | `ApiResult.server_error()` |

### 3. **验证机制**

#### Header参数验证
```python
# 验证user_id
if not user_id:
    return ApiResult.bad_request(
        message="缺少用户ID，请在请求头中提供user_id",
        data={"error": "Missing user_id header"}
    )

# 验证session_id
if not session_id:
    return ApiResult.bad_request(
        message="缺少会话ID，请在请求头中提供session_id",
        data={"error": "Missing session_id header"}
    )
```

#### 异常处理
```python
try:
    # 业务逻辑
    result = await chat_service.chat(...)
    return ApiResult.success(data=response_data, message="处理成功")
    
except ValueError as e:
    return ApiResult.bad_request(message=f"请求参数错误: {str(e)}", data={"error": str(e)})
    
except PermissionError as e:
    return ApiResult.forbidden(message=f"权限不足: {str(e)}", data={"error": str(e)})
    
except Exception as e:
    return ApiResult.server_error(message="聊天处理失败，请稍后重试", data={"error": str(e)})
```

## 📊 验证结果

运行 `test_api_response_format.py` 的验证结果：

```
✅ 使用ApiResult.success成功响应
✅ 使用ApiResult.bad_request错误响应
✅ 使用ApiResult.forbidden权限错误响应
✅ 使用ApiResult.server_error服务器错误响应
✅ 成功响应code=0
✅ 错误响应code规范完整
✅ 包含统一的{code, message, data}结构
✅ 包含user_id验证
✅ 包含session_id验证
✅ 包含完整的异常处理
```

## 🔧 API实现

### Chat Router (`api/chat_router.py`)
```python
@chat_router.post("/complete")
async def complete(request: ChatRequest, user_id: str = Header(None), session_id: str = Header(None)):
    try:
        # 验证必需参数
        if not user_id:
            return ApiResult.bad_request(message="缺少用户ID", data={"error": "Missing user_id"})
        
        if not session_id:
            return ApiResult.bad_request(message="缺少会话ID", data={"error": "Missing session_id"})
        
        # 处理业务逻辑
        result = await chat_service.chat(...)
        
        # 返回成功响应
        return ApiResult.success(data=response_data, message="处理成功")
        
    except ValueError as e:
        return ApiResult.bad_request(message=f"请求参数错误: {str(e)}", data={"error": str(e)})
    except PermissionError as e:
        return ApiResult.forbidden(message=f"权限不足: {str(e)}", data={"error": str(e)})
    except Exception as e:
        return ApiResult.server_error(message="聊天处理失败，请稍后重试", data={"error": str(e)})
```

### Result Class (`common/result.py`)
```python
class ApiResult:
    @staticmethod
    def success(data: Any = None, message: str = "请求成功") -> dict:
        return {"code": 0, "message": message, "data": data}
    
    @staticmethod
    def error(message: str = "请求失败", code: int = 1, data: Any = None) -> dict:
        return {"code": code, "message": message, "data": data}
    
    @staticmethod
    def bad_request(message: str = "请求参数错误", data: Any = None) -> dict:
        return {"code": 400, "message": message, "data": data}
    
    @staticmethod
    def forbidden(message: str = "禁止访问", data: Any = None) -> dict:
        return {"code": 403, "message": message, "data": data}
    
    @staticmethod
    def server_error(message: str = "服务器内部错误", data: Any = None) -> dict:
        return {"code": 500, "message": message, "data": data}
```

## 🎯 响应示例

### 成功响应示例

#### 1. 任务执行成功
```json
{
  "code": 0,
  "message": "处理成功",
  "data": {
    "type": "task",
    "message": "模拟任务执行：关于'我要检查冰柜陈列'的任务已经完成。冰柜陈列符合标准，建议发放8.8元红包作为奖励。\n\n🎁 奖励发放：已成功发放8.8元红包（红包ID: rp_123456）",
    "data": {
      "task_completed": true,
      "performance_score": 85,
      "task_type": "freezer_inspection",
      "execution_details": "冰柜陈列检查完成，商品摆放整齐，温度适宜",
      "reward": 8.8,
      "redpacket_sent": true,
      "redpacket_id": "rp_123456",
      "actual_reward": 8.8
    },
    "suggestions": ["执行下一个任务", "查看任务历史", "领取更多奖励"]
  }
}
```

#### 2. 欢迎响应
```json
{
  "code": 0,
  "message": "处理成功",
  "data": {
    "type": "welcome",
    "message": "欢迎使用智能助手！我可以帮您执行任务、管理采购、搜索信息等。请告诉我您需要什么帮助？",
    "data": null,
    "suggestions": ["我要执行任务", "我要采购商品", "搜索信息"]
  }
}
```

### 错误响应示例

#### 1. 缺少user_id
```json
{
  "code": 400,
  "message": "缺少用户ID，请在请求头中提供user_id",
  "data": {"error": "Missing user_id header"}
}
```

#### 2. 缺少session_id
```json
{
  "code": 400,
  "message": "缺少会话ID，请在请求头中提供session_id",
  "data": {"error": "Missing session_id header"}
}
```

#### 3. 权限不足
```json
{
  "code": 403,
  "message": "权限不足: 用户无权限执行此操作",
  "data": {"error": "用户无权限执行此操作"}
}
```

#### 4. 服务器错误
```json
{
  "code": 500,
  "message": "聊天处理失败，请稍后重试",
  "data": {"error": "Connection timeout"}
}
```

## 🔄 请求流程

### 正常流程
```
1. 客户端发送请求 → 包含user_id和session_id header
2. API验证参数 → 检查user_id和session_id是否存在
3. 调用业务逻辑 → ChatService处理消息
4. 返回成功响应 → code=0, data包含业务结果
```

### 错误流程
```
1. 客户端发送请求 → 缺少user_id或session_id
2. API验证失败 → 返回400错误
3. 客户端收到错误 → code=400, message包含错误信息
4. 客户端修正请求 → 重新发送完整header
```

## 🎉 总结

通过这次API响应格式标准化，我们实现了：

✅ **统一响应结构** - 所有API都使用 `{code, message, data}` 格式
✅ **标准化错误码** - 遵循HTTP状态码规范
✅ **完整验证机制** - 验证所有必需的header参数
✅ **详细错误信息** - 提供清晰的错误描述和数据
✅ **异常处理覆盖** - 处理各种类型的异常情况
✅ **数据完整性** - 确保成功和失败都有完整的数据传递

现在API响应格式完全符合您的要求：成功时code=0内容放到data中，失败时code为错误码错误消息放到message中！
