#!/bin/bash

# Polymarket Web应用启动脚本
# 用于简化Web应用的启动过程

echo "🚀 Polymarket Web应用启动脚本"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查Python环境
echo -n "${BLUE}检查Python环境...${NC} "
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到Python3${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python3 已安装${NC}"
fi

# 检查虚拟环境
echo -n "${BLUE}检查虚拟环境...${NC} "
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ 虚拟环境存在${NC}"
else
    echo -e "${YELLOW}⚠️  虚拟环境不存在，正在创建...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ 虚拟环境创建完成${NC}"
fi

# 激活虚拟环境
echo -n "${BLUE}激活虚拟环境...${NC} "
if [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
else
    echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
fi

# 检查依赖
echo -n "${BLUE}检查依赖包...${NC} "
if python -c "import flask" 2>/dev/null && python -c "import requests" 2>/dev/null; then
    echo -e "${GREEN}✅ 核心依赖已安装${NC}"
else
    echo -e "${YELLOW}⚠️  正在安装依赖...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
fi

# 检查环境变量文件
echo -n "${BLUE}检查环境配置...${NC} "
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ 环境配置文件存在${NC}"
else
    echo -e "${YELLOW}⚠️  创建默认配置文件...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ 配置文件创建完成${NC}"
    echo -e "${YELLOW}💡 如需自定义配置，请编辑 .env 文件${NC}"
fi

# 检查端口占用
echo -n "${BLUE}检查端口5000...${NC} "
if lsof -i :5000 &> /dev/null; then
    echo -e "${YELLOW}⚠️  端口5000已被占用${NC}"
    echo -e "${BLUE}尝试使用端口5001...${NC} "
    export PORT=5001
else
    echo -e "${GREEN}✅ 端口5000可用${NC}"
fi

# 停止可能存在的旧进程
echo -n "${BLUE}清理旧进程...${NC} "
pkill -f "python app.py" 2>/dev/null || true
sleep 1

# 启动应用
echo ""
echo -e "${BLUE}🚀 启动Polymarket Web应用...${NC}"
echo -e "${BLUE}启动命令: python app.py${NC}"
echo -e "${BLUE}访问地址: http://localhost:${PORT:-5000}${NC}"
echo ""
echo -e "${YELLOW}💡 按 Ctrl+C 停止应用${NC}"
echo "================================"

# 启动Flask应用
python app.py