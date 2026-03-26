# 🐳 Docker部署指南

## 📋 目录
- [快速开始](#快速开始)
- [环境要求](#环境要求)
- [配置说明](#配置说明)
- [部署命令](#部署命令)
- [服务监控](#服务监控)
- [故障排除](#故障排除)
- [生产环境](#生产环境)

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd shop_assistant_chat
```

### 2. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
vim .env
```

### 3. 启动服务
```bash
# 使用Makefile（推荐）
make init
make build
make up

# 或使用docker-compose
docker-compose build
docker-compose up -d
```

### 4. 验证部署
```bash
# 检查服务状态
make status

# 健康检查
make health

# 测试API
make test-api

# 查看日志
make logs
```

## 📋 环境要求

### 系统要求
- Docker 20.10+
- Docker Compose 2.0+
- Make（可选，用于便捷命令）

### 硬件要求
- **最小配置**: 1GB RAM, 1 CPU
- **推荐配置**: 2GB RAM, 2 CPU
- **生产环境**: 4GB RAM, 2 CPU

### 网络要求
- 端口 8000: 应用服务
- 端口 6379: Redis（可选）

## ⚙️ 配置说明

### 环境变量配置

#### 必需配置
```bash
# AI模型配置
API_KEY=your_api_key
BASE_URL=http://your-llm-server:8000/v1
MODEL_ID=your-model-name

# Redis配置
REDIS_URL=redis://redis:6379/0
```

#### 可选配置
```bash
# 应用配置
APP_NAME=Shop Assistant Chat
DEBUG=false
LOG_LEVEL=INFO

# OpenAI配置（如果使用OpenAI）
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo

# 搜索服务
BING_SEARCH_API_KEY=your_bing_search_api_key
```

### 服务配置

#### 应用服务配置
- **容器名称**: shop-assistant-chat
- **端口映射**: 8000:8000
- **健康检查**: /health 端点
- **重启策略**: unless-stopped

#### Redis配置
- **容器名称**: shop-assistant-redis
- **端口映射**: 6379:6379
- **数据持久化**: redis_data volume
- **内存限制**: 256MB

## 🛠️ 部署命令

### 使用Makefile（推荐）

```bash
# 查看所有命令
make help

# 构建镜像
make build

# 启动服务
make up

# 前台运行
make up-foreground

# 停止服务
make down

# 重启服务
make restart

# 查看日志
make logs

# 进入容器
make shell

# 健康检查
make health

# API测试
make test-api

# 清理资源
make clean
```

### 使用Docker Compose

```bash
# 构建镜像
docker-compose build

# 启动服务（后台）
docker-compose up -d

# 启动服务（前台）
docker-compose up

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec shop-assistant-chat /bin/bash

# 查看状态
docker-compose ps
```

## 📊 服务监控

### 健康检查
```bash
# 应用健康检查
curl http://localhost:8000/health

# Redis健康检查
docker-compose exec redis redis-cli ping

# 综合健康检查
make health
```

### 资源监控
```bash
# 查看资源使用
docker stats

# 查看容器状态
docker-compose ps

# 查看网络
make network
```

### 日志管理
```bash
# 查看应用日志
make logs-app

# 查看Redis日志
make logs-redis

# 查看所有日志
make logs

# 实时跟踪日志
docker-compose logs -f --tail=100
```

## 🔧 故障排除

### 常见问题

#### 1. 容器启动失败
```bash
# 查看详细错误
docker-compose logs shop-assistant-chat

# 检查配置
docker-compose config

# 重新构建
docker-compose build --no-cache
```

#### 2. 端口冲突
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 修改端口映射
vim docker-compose.yml
```

#### 3. 内存不足
```bash
# 查看内存使用
docker stats

# 清理未使用的资源
docker system prune -a
```

#### 4. 网络问题
```bash
# 检查网络连接
docker network ls

# 重建网络
docker-compose down
docker network prune
docker-compose up -d
```

### 调试模式

#### 启用调试
```bash
# 设置调试模式
DEBUG=true docker-compose up -d

# 进入容器调试
make shell

# 查看详细日志
LOG_LEVEL=DEBUG docker-compose up
```

#### 测试连接
```bash
# 测试API连接
curl -X POST "http://localhost:8000/api/v1/chat/complete" \
  -H "Content-Type: application/json" \
  -H "user_id: test_user" \
  -H "session_id: test_session" \
  -d '{"message": "你好"}'

# 测试流式连接
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -H "user_id: test_user" \
  -H "session_id: test_session" \
  -d '{"message": "你好"}' \
  --no-buffer
```

## 🏭 生产环境

### 生产环境部署

#### 1. 使用生产配置
```bash
# 启动生产环境
make prod

# 或直接使用
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### 2. 安全配置
```bash
# 设置Redis密码
REDIS_PASSWORD=your_strong_password

# 限制网络访问
# 修改docker-compose.prod.yml中的端口映射
```

#### 3. 性能优化
```bash
# 调整资源限制
vim docker-compose.prod.yml

# 配置日志轮转
vim config/logrotate.conf

# 设置监控
# 集成Prometheus/Grafana
```

#### 4. 备份策略
```bash
# 备份Redis数据
make backup

# 设置定时备份
crontab -e
# 添加: 0 2 * * * cd /path/to/project && make backup
```

### 扩展部署

#### 多实例部署
```bash
# 使用Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml shop-assistant

# 使用Kubernetes
kubectl apply -f k8s/
```

## 📝 维护指南

### 日常维护
```bash
# 检查服务状态
make status

# 查看资源使用
make monitor

# 清理日志
find logs/ -name "*.log" -mtime +7 -delete

# 更新服务
make update
```

### 数据管理
```bash
# 备份数据
make backup

# 恢复数据
make restore FILE=backup.rdb

# 清理数据
make clean
```

### 版本更新
```bash
# 更新代码
git pull

# 重新构建
make build

# 滚动更新
docker-compose up -d --no-deps shop-assistant-chat
```

## 📞 支持

如果遇到问题，请：
1. 查看日志: `make logs`
2. 检查配置: `docker-compose config`
3. 健康检查: `make health`
4. API测试: `make test-api`
5. 查看文档: [项目文档](README.md)

---

## 🎯 快速参考

### 基础命令
```bash
make help          # 查看帮助
make build         # 构建镜像
make up            # 启动服务
make down          # 停止服务
make logs          # 查看日志
make health        # 健康检查
make test-api      # API测试
make clean         # 清理资源
```

### 端点地址
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **Redis**: localhost:6379

### 配置文件
- **环境变量**: `.env`
- **Docker配置**: `docker-compose.yml`
- **Redis配置**: `config/redis.conf`

### 服务架构
```
┌─────────────────┐    ┌─────────────────┐
│  App Container  │────│     Redis       │
│   (FastAPI)     │    │   (缓存/会话)    │
│   Port: 8000    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘
```
