# Makefile for Shop Assistant Chat

.PHONY: help build up down logs clean test lint format

# 默认目标
help: ## 显示帮助信息
	@echo "Shop Assistant Chat - Docker部署"
	@echo ""
	@echo "可用命令:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# 构建镜像
build: ## 构建Docker镜像
	@echo "构建Docker镜像..."
	docker-compose build

# 启动服务
up: ## 启动所有服务
	@echo "启动所有服务..."
	docker-compose up -d

# 启动服务（前台运行）
up-foreground: ## 前台启动所有服务
	@echo "前台启动所有服务..."
	docker-compose up

# 停止服务
down: ## 停止所有服务
	@echo "停止所有服务..."
	docker-compose down

# 重启服务
restart: ## 重启所有服务
	@echo "重启所有服务..."
	docker-compose restart

# 查看日志
logs: ## 查看服务日志
	@echo "查看服务日志..."
	docker-compose logs -f

# 查看应用日志
logs-app: ## 查看应用服务日志
	@echo "查看应用服务日志..."
	docker-compose logs -f shop-assistant-chat

# 清理资源
clean: ## 清理Docker资源
	@echo "清理Docker资源..."
	docker-compose down
	docker system prune -f

# 完全清理
clean-all: ## 完全清理Docker资源（包括镜像）
	@echo "完全清理Docker资源..."
	docker-compose down --rmi all
	docker system prune -af

# 进入应用容器
shell: ## 进入应用容器
	@echo "进入应用容器..."
	docker-compose exec shop-assistant-chat /bin/bash

# 运行测试
test: ## 运行测试
	@echo "运行测试..."
	docker-compose exec shop-assistant-chat python -m pytest

# 代码检查
lint: ## 代码检查
	@echo "运行代码检查..."
	docker-compose exec shop-assistant-chat python -m flake8 .

# 代码格式化
format: ## 代码格式化
	@echo "格式化代码..."
	docker-compose exec shop-assistant-chat python -m black .

# 查看服务状态
status: ## 查看服务状态
	@echo "查看服务状态..."
	docker-compose ps

# 健康检查
health: ## 检查服务健康状态
	@echo "检查服务健康状态..."
	@curl -f http://localhost:8800/health || echo "应用服务不健康"

# 更新服务
update: ## 更新服务（拉取最新代码并重新构建）
	@echo "更新服务..."
	git pull
	docker-compose build
	docker-compose up -d

# 开发环境启动
dev: ## 启动开发环境
	@echo "启动开发环境..."
	DEBUG=true docker-compose up -d

# 生产环境启动
prod: ## 启动生产环境
	@echo "启动生产环境..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 监控资源使用
monitor: ## 监控资源使用
	@echo "监控资源使用..."
	docker stats

# 初始化项目
init: ## 初始化项目（首次部署）
	@echo "初始化项目..."
	cp .env.example .env
	@echo "请编辑 .env 文件配置相关参数"
	@echo "然后运行: make build && make up"

# API测试
test-api: ## 测试API接口
	@echo "测试API接口..."
	python test_docker_deployment.py

# Redis连接测试
test-redis: ## 测试Redis连接
	@echo "测试Redis连接..."
	docker-compose exec shop-assistant-chat python -c "
import redis
import os
from urllib.parse import urlparse
redis_url = 'redis://:acctrue666888666@183.222.230.18:6379/0'
try:
    r = redis.from_url(redis_url)
    r.ping()
    print('✅ Redis连接成功')
except Exception as e:
    print(f'❌ Redis连接失败: {e}')
"
