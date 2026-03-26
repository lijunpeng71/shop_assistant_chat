# 🧧 红包工具功能说明

## 🎯 功能概述

将任务执行后发送红包的操作作为一个外包tool调用，实现智能化的奖励发放机制。红包工具可以自动计算奖励金额、调用红包API、记录发放状态，并与DeepAgents智能体无缝集成。

**重要更新**：所有模拟逻辑都在工具中执行，智能体只负责调用工具，实现了职责分离。

## 🏗️ 技术架构

### 1. 红包工具类

#### 核心功能
```python
class RedPacketTool:
    """红包工具类"""
    
    async def send_redpacket(self, user_id: str, amount: float, reason: str, task_type: str = "general") -> Dict[str, Any]:
        """发送红包"""
        
    def calculate_reward(self, task_type: str, performance_score: float, base_amount: float = 8.8) -> float:
        """计算奖励金额"""
        
    async def calculate_and_send_reward(self, user_id: str, task_type: str, performance_score: float, task_description: str) -> Dict[str, Any]:
        """计算并发送奖励"""
        
    def analyze_task(self, message: str, task_type: str = "general") -> Dict[str, Any]:
        """分析任务并生成模拟结果"""
        
    async def simulate_task_execution(self, user_id: str, message: str, task_type: str = "general") -> Dict[str, Any]:
        """模拟任务执行（包含红包发放）"""
```

#### 红包API集成
```python
async def _call_redpacket_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """调用红包API（模拟）"""
    # 支持真实的红包API集成
    # 包含签名验证、错误处理、重试机制
```

### 2. DeepAgents工具集成

#### 工具定义
```python
redpacket_tools = [
    {
        "name": "send_redpacket",
        "description": "发送红包奖励给用户",
        "function": send_redpacket,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "amount": {"type": "number", "description": "红包金额"},
            "reason": {"type": "string", "description": "发送原因"},
            "task_type": {"type": "string", "description": "任务类型"}
        }
    },
    {
        "name": "calculate_and_send_reward",
        "description": "计算并发送任务奖励",
        "function": calculate_and_send_reward,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "task_type": {"type": "string", "description": "任务类型"},
            "performance_score": {"type": "number", "description": "绩效评分 (0-100)"},
            "task_description": {"type": "string", "description": "任务描述"}
        }
    },
    {
        "name": "simulate_task_execution",
        "description": "模拟任务执行（包含红包发放）",
        "function": simulate_task_execution,
        "parameters": {
            "user_id": {"type": "string", "description": "用户ID"},
            "message": {"type": "string", "description": "用户消息"},
            "task_type": {"type": "string", "description": "任务类型"}
        }
    }
]
```

### 3. 智能体集成

#### 任务智能体配置
```python
task_subagent = {
    "name": "task-agent",
    "description": "专门处理任务执行相关的工作",
    "system_prompt": """...模拟执行机制：
- 当LLM未配置或需要模拟时，使用simulate_task_execution工具
- 该工具会分析任务类型、生成模拟结果、计算奖励并发放红包
- 所有模拟逻辑都在工具中执行，智能体只负责调用工具

请始终以专业、准确的方式回应，确保用户充分理解将要执行的任务内容。任务完成后记得使用红包工具发放奖励。在需要模拟时，使用simulate_task_execution工具。""",
    "tools": redpacket_tools,  # 使用红包工具（包含模拟工具）
    "interrupt_on": {
        "task_confirmation": True,
        "image_required": True,
        "user_approval": True
    }
}
```

## 🔄 工作流程

### 1. 模拟任务执行流程

#### 智能体调用工具
```python
# 智能体中的代码（简化）
if any(keyword in message_lower for keyword in ["任务", "执行", "检查", "陈列"]):
    # 使用工具进行模拟任务执行
    from tools.redpacket_tool import simulate_task_execution
    
    user_id = kwargs.get('user_id', 'mock_user_123')
    return await simulate_task_execution(user_id, message, "general")
```

#### 工具执行逻辑
```python
async def simulate_task_execution(user_id: str, message: str, task_type: str = "general") -> Dict[str, Any]:
    # 1. 分析任务类型和绩效评分
    task_analysis = redpacket_tool.analyze_task(message, task_type)
    
    # 2. 构建任务执行结果
    task_result = {
        "type": "task",
        "message": f"模拟任务执行：关于'{message}'的任务已经完成。{task_analysis['result_description']}",
        "data": {
            "task_completed": True,
            "performance_score": task_analysis["performance_score"],
            "task_type": task_analysis["task_type"],
            "execution_details": task_analysis["execution_details"],
            "reward": task_analysis["suggested_reward"]
        }
    }
    
    # 3. 发送红包
    redpacket_result = await calculate_and_send_reward(...)
    
    # 4. 合并结果
    if redpacket_result.get("success"):
        task_result["data"]["redpacket_sent"] = True
        task_result["data"]["redpacket_id"] = redpacket_result.get("redpacket_id")
        task_result["message"] += f"\n\n🎁 **奖励发放**：已成功发放{redpacket_result.get('amount')}元红包"
    
    return task_result
```

### 2. 任务分析机制

#### 智能任务识别
```python
def analyze_task(self, message: str, task_type: str = "general") -> Dict[str, Any]:
    message_lower = message.lower()
    
    # 分析任务类型
    if any(keyword in message_lower for keyword in ["库存", "盘点"]):
        analyzed_task_type = "inventory_check"
        performance_score = 88
        result_description = "经检查，库存管理良好，商品摆放有序，建议发放奖励。"
        execution_details = {
            "total_items": 156,
            "expiring_items": 3,
            "display_compliance": "95%"
        }
    elif any(keyword in message_lower for keyword in ["冰柜", "陈列", "检查"]):
        analyzed_task_type = "freezer_inspection"
        performance_score = 85
        result_description = "经检查，冰柜陈列符合标准，商品可见性良好，建议发放奖励。"
        execution_details = {
            "layout_score": 85,
            "visibility_score": 90,
            "brand_distribution": "良好"
        }
    # ... 其他任务类型
    
    return {
        "task_type": analyzed_task_type,
        "performance_score": performance_score,
        "result_description": result_description,
        "execution_details": execution_details,
        "suggested_reward": self.calculate_reward(analyzed_task_type, performance_score)
    }
```

## 🏗️ 架构优势

### 1. **职责分离**
- **智能体**：专注于任务协调、用户交互、中断处理
- **工具**：负责具体的模拟逻辑、任务分析、红包发放

### 2. **代码复用**
- 模拟逻辑可在多个场景中复用
- 红包发放逻辑统一管理
- 任务分析逻辑独立封装

### 3. **易于测试**
- 工具可以独立测试
- 模拟逻辑与智能体逻辑解耦
- 支持单元测试和集成测试

### 4. **易于维护**
- 修改模拟逻辑只需更新工具
- 智能体代码保持简洁
- 降低代码耦合度

### 5. **扩展性强**
- 新增模拟类型只需扩展工具
- 支持插件化的模拟策略
- 便于添加新的奖励机制

## 🧪 测试验证

### 运行测试脚本
```bash
# 红包工具测试
python test_redpacket_tool.py

# 模拟工具测试
python test_simulation_tool.py
```

### 测试内容
1. **模拟工具直接测试** - 验证工具功能
2. **API集成测试** - 验证智能体调用工具
3. **任务分析测试** - 验证智能任务识别
4. **错误处理测试** - 验证异常情况处理
5. **架构验证测试** - 确认职责分离

### 测试架构验证

#### 验证智能体不包含模拟逻辑
```python
# 智能体代码检查
def _create_mock_agent(self):
    class MockAgent:
        async def __call__(self, message: str, **kwargs) -> Dict[str, Any]:
            # ✅ 只调用工具，不包含模拟逻辑
            from tools.redpacket_tool import simulate_task_execution
            user_id = kwargs.get('user_id', 'mock_user_123')
            return await simulate_task_execution(user_id, message, "general")
```

#### 验证工具包含所有模拟逻辑
```python
# 工具代码检查
async def simulate_task_execution(user_id: str, message: str, task_type: str = "general") -> Dict[str, Any]:
    # ✅ 包含完整的模拟逻辑
    task_analysis = redpacket_tool.analyze_task(message, task_type)
    # ... 模拟执行逻辑
    # ... 红包发放逻辑
```

## 📊 对比分析

### 改进前架构
```python
# 智能体中包含模拟逻辑
class MockAgent:
    async def __call__(self, message: str, **kwargs):
        # ❌ 智能体包含大量模拟代码
        task_result = {...}
        redpacket_result = await calculate_and_send_reward(...)
        # ❌ 智能体负责红包发放逻辑
        if redpacket_result.get("success"):
            task_result["data"]["redpacket_sent"] = True
        return task_result
```

### 改进后架构
```python
# 智能体只负责调用工具
class MockAgent:
    async def __call__(self, message: str, **kwargs):
        # ✅ 智能体只调用工具
        from tools.redpacket_tool import simulate_task_execution
        user_id = kwargs.get('user_id', 'mock_user_123')
        return await simulate_task_execution(user_id, message, "general")

# 工具包含所有逻辑
async def simulate_task_execution(user_id: str, message: str, task_type: str = "general"):
    # ✅ 工具包含完整的模拟和红包逻辑
    task_analysis = redpacket_tool.analyze_task(message, task_type)
    # ... 所有模拟逻辑
    # ... 所有红包逻辑
```

## 🎯 使用指南

### 1. **智能体开发者**
- 专注于任务协调逻辑
- 通过工具调用实现具体功能
- 不需要关心模拟和红包的实现细节

### 2. **工具开发者**
- 负责实现具体的业务逻辑
- 提供标准化的工具接口
- 确保工具的可靠性和性能

### 3. **测试人员**
- 可以独立测试工具功能
- 可以独立测试智能体逻辑
- 提高测试覆盖率和效率

## 🎉 总结

红包工具功能带来了：

✅ **职责分离** - 智能体和工具各司其职
✅ **代码复用** - 模拟逻辑可在多处使用
✅ **易于测试** - 工具和智能体可独立测试
✅ **易于维护** - 逻辑集中，便于修改
✅ **扩展性强** - 支持插件化扩展
✅ **架构清晰** - 代码结构更加合理

这个架构实现了真正的职责分离，所有模拟逻辑都在工具中执行，智能体只负责调用工具，大大提高了代码的可维护性和可扩展性！

## 🔄 工作流程

### 1. 任务执行与奖励发放流程

#### 步骤1: 用户发起任务
```bash
curl -X POST "http://localhost:8800/api/v1/chat/complete" \
  -H "user_id: test_user_123" \
  -H "session_id: session_001" \
  -d '{"message": "我要执行库存盘点"}'
```

#### 步骤2: 任务确认
```json
{
    "code": 0,
    "message": "📋 **任务确认**\n\n请确认是否执行此任务...",
    "data": {
        "interrupted": true,
        "interrupt_reason": "task_confirmation",
        "task_info": {
            "task_name": "库存盘点任务",
            "description": "对当前库存进行全面盘点",
            "estimated_time": "约15-20分钟"
        }
    }
}
```

#### 步骤3: 用户确认执行
```bash
curl -X POST "http://localhost:8800/api/v1/chat/complete" \
  -H "user_id: test_user_123" \
  -H "session_id: session_001" \
  -d '{"message": "确认执行"}'
```

#### 步骤4: 任务执行与红包发放
```json
{
    "code": 0,
    "message": "✅ **库存盘点任务执行完成**\n\n任务执行情况：\n📊 **盘点结果**：\n- 总商品数量：156件\n- 保质期检查：3件即将过期\n- 陈列位置：95%符合标准\n\n🎁 **奖励发放**：已成功发放12.6元红包（红包ID: RP_12345678）",
    "data": {
        "task_result": "completed",
        "execution_details": {
            "total_items": 156,
            "expiring_items": 3,
            "display_compliance": "95%"
        },
        "performance_score": 85,
        "redpacket_sent": true,
        "redpacket_id": "RP_12345678",
        "actual_reward": 12.6
    }
}
```

### 2. 冰柜检查与奖励发放

#### 带图片的冰柜检查
```bash
curl -X POST "http://localhost:8800/api/v1/chat/complete" \
  -H "user_id: test_user_123" \
  -H "session_id: session_001" \
  -d '{
    "message": "我要检查冰柜陈列",
    "image_url": "https://example.com/freezer_photo.jpg"
  }'
```

#### 检查结果与奖励
```json
{
    "code": 0,
    "message": "我已经收到您提供的冰柜照片。基于照片分析，冰柜陈列情况如下...\n\n🎁 **奖励发放**：已成功发放8.8元红包（红包ID: RP_87654321）",
    "data": {
        "inspection_result": "良好",
        "score": 85,
        "performance_score": 85,
        "redpacket_sent": true,
        "redpacket_id": "RP_87654321",
        "actual_reward": 8.8
    }
}
```

## 💰 奖励计算机制

### 1. 任务类型系数
```python
task_multipliers = {
    "inventory_check": 1.2,      # 库存盘点
    "freezer_inspection": 1.0,   # 冰柜检查
    "sales_analysis": 1.1,        # 销售分析
    "general_task": 0.9,          # 一般任务
    "purchase_task": 1.3         # 采购任务
}
```

### 2. 绩效评分系数
```python
if performance_score >= 90:
    performance_bonus = 1.5  # 优秀表现
elif performance_score >= 80:
    performance_bonus = 1.2  # 良好表现
elif performance_score >= 70:
    performance_bonus = 1.0  # 标准表现
else:
    performance_bonus = 0.8  # 需要改进
```

### 3. 奖励金额计算
```python
final_amount = base_amount * task_multiplier * performance_bonus
final_amount = max(1.0, min(final_amount, 50.0))  # 限制在1-50元之间
final_amount = round(final_amount, 1)  # 保留一位小数
```

### 4. 计算示例
| 任务类型 | 绩效评分 | 基础金额 | 任务系数 | 绩效系数 | 最终金额 |
|---------|---------|---------|---------|---------|---------|
| 库存盘点 | 90分 | 8.8元 | 1.2 | 1.5 | 15.8元 |
| 冰柜检查 | 85分 | 8.8元 | 1.0 | 1.2 | 10.6元 |
| 销售分析 | 75分 | 8.8元 | 1.1 | 1.0 | 9.7元 |
| 一般任务 | 65分 | 8.8元 | 0.9 | 0.8 | 6.3元 |

## 🔧 工具API详解

### 1. send_redpacket
```python
async def send_redpacket(user_id: str, amount: float, reason: str, task_type: str = "general") -> Dict[str, Any]
```

#### 参数说明
- **user_id**: 用户ID（必需）
- **amount**: 红包金额（必需，范围1.0-50.0）
- **reason**: 发送原因（必需）
- **task_type**: 任务类型（可选，默认"general"）

#### 返回结果
```json
{
    "success": true,
    "redpacket_id": "RP_12345678",
    "amount": 8.8,
    "user_id": "test_user_123",
    "reason": "库存盘点任务完成 - 绩效评分: 85分",
    "status": "sent",
    "message": "成功发送8.8元红包给用户test_user_123"
}
```

### 2. calculate_and_send_reward
```python
async def calculate_and_send_reward(user_id: str, task_type: str, performance_score: float, task_description: str) -> Dict[str, Any]
```

#### 参数说明
- **user_id**: 用户ID（必需）
- **task_type**: 任务类型（必需）
- **performance_score**: 绩效评分（必需，0-100）
- **task_description**: 任务描述（必需）

#### 返回结果
```json
{
    "success": true,
    "redpacket_id": "RP_12345678",
    "amount": 10.6,
    "user_id": "test_user_123",
    "reason": "冰柜陈列检查任务 - 绩效评分: 85分",
    "status": "sent",
    "message": "成功发送10.6元红包给用户test_user_123"
}
```

## 🛡️ 错误处理机制

### 1. 红包发送失败
```json
{
    "success": false,
    "error": "Insufficient balance",
    "amount": 8.8,
    "user_id": "test_user_123",
    "reason": "库存盘点任务完成",
    "status": "failed",
    "message": "红包发送失败: Insufficient balance"
}
```

### 2. 智能体错误处理
```python
try:
    redpacket_result = await calculate_and_send_reward(
        user_id=user_id,
        task_type="freezer_inspection",
        performance_score=85,
        task_description="冰柜陈列检查任务"
    )
    
    if redpacket_result.get("success"):
        task_result["data"]["redpacket_sent"] = True
        task_result["message"] += f"\n\n🎁 **奖励发放**：已成功发放{redpacket_result.get('amount')}元红包"
    else:
        task_result["data"]["redpacket_sent"] = False
        task_result["message"] += f"\n\n⚠️ **奖励发放失败**：{redpacket_result.get('error')}"
except Exception as e:
    task_result["data"]["redpacket_sent"] = False
    task_result["message"] += f"\n\n⚠️ **奖励发放异常**：{str(e)}"
```

## 🧪 测试验证

### 运行测试脚本
```bash
python test_redpacket_tool.py
```

### 测试内容
1. **任务执行和红包发放测试** - 验证完整工作流程
2. **冰柜检查和红包发放测试** - 验证图片分析任务
3. **红包工具直接测试** - 验证工具API功能
4. **模拟智能体红包测试** - 验证回退机制
5. **奖励金额计算测试** - 验证计算逻辑

### 测试场景

#### 场景1: 库存盘点奖励
```bash
# 用户发起任务
{"message": "我要执行库存盘点"}

# 确认执行
{"message": "确认执行"}

# 预期结果：任务完成 + 红包发放（约12.6元）
```

#### 场景2: 冰柜检查奖励
```bash
# 带图片的检查
{"message": "我要检查冰柜陈列", "image_url": "https://example.com/photo.jpg"}

# 预期结果：图片分析 + 红包发放（约8.8元）
```

## 📊 状态追踪

### 1. 红包发放状态
- **sent**: 发送成功
- **failed**: 发送失败
- **pending**: 发送中
- **error**: 发送异常

### 2. 数据记录
```json
{
    "redpacket_sent": true,
    "redpacket_id": "RP_12345678",
    "actual_reward": 10.6,
    "redpacket_error": null,
    "redpacket_status": "sent"
}
```

## 🚀 扩展功能

### 1. 红包模板系统
```python
redpacket_templates = {
    "excellent_performance": {
        "base_amount": 15.0,
        "message": "优秀表现奖励"
    },
    "good_performance": {
        "base_amount": 10.0,
        "message": "良好表现奖励"
    }
}
```

### 2. 批量红包发放
```python
async def send_batch_redpackets(redpacket_list: List[Dict]) -> Dict[str, Any]:
    """批量发送红包"""
    # 支持批量处理，提高效率
```

### 3. 红包统计报表
```python
def generate_redpacket_report(user_id: str, date_range: str) -> Dict[str, Any]:
    """生成红包发放报表"""
    # 统计分析功能
```

## 📝 最佳实践

### 1. 奖励策略
- **公平性**: 基于客观的绩效评分
- **激励性**: 优秀表现获得更高奖励
- **可持续性**: 控制奖励总额在合理范围

### 2. 错误处理
- **优雅降级**: 红包发放失败不影响任务完成
- **重试机制**: 网络错误自动重试
- **日志记录**: 完整的操作日志

### 3. 用户体验
- **及时反馈**: 实时显示红包发放状态
- **详细信息**: 显示红包ID和金额
- **错误提示**: 清晰的失败原因说明

## 🎉 总结

红包工具功能带来了：

✅ **自动化奖励** - 任务完成后自动发放红包
✅ **智能计算** - 基于任务类型和绩效动态计算金额
✅ **工具集成** - 与DeepAgents智能体无缝集成
✅ **错误处理** - 完善的错误处理和状态反馈
✅ **状态追踪** - 详细的红包发放状态记录
✅ **扩展性** - 易于扩展和定制奖励策略

这个实现将奖励发放完全外包为工具调用，让智能体专注于任务执行，同时提供了完整的奖励管理功能！
