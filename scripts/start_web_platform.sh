#!/bin/bash

# AI智能学习助手 - Web平台启动脚本 (Linux/Mac - 通用版)

echo "=================================="
echo "AI智能学习助手 - Web平台"
echo "=================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."
PROJECT_ROOT=$(pwd)

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# 检查Python
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ 错误: 未找到Python或Python3"
        echo "请确保Python已安装"
        exit 1
    else
        PYTHON_CMD=python3
    fi
else
    PYTHON_CMD=python
fi

echo "🐍 Python版本:"
$PYTHON_CMD --version
echo ""

# 检查配置文件
if [ ! -f "$PROJECT_ROOT/config/agent_llm_config.json" ]; then
    echo "❌ 错误: 未找到配置文件 config/agent_llm_config.json"
    exit 1
fi

echo "✅ 配置文件检查通过"
echo ""

# 检查并安装依赖
echo "🔍 检查依赖..."
$PYTHON_CMD -c "import fastapi, uvicorn, langchain" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少必要的依赖，正在安装..."
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo ""
fi

echo "✅ 依赖检查通过"
echo ""

# 启动服务
echo "🚀 启动Web服务..."
echo ""
echo "📍 访问地址: http://localhost:8000"
echo "📍 前端页面: http://localhost:8000/static/index.html"
echo ""
echo "⏹️  按 Ctrl+C 停止服务"
echo ""
echo "=================================="
echo ""

# 启动FastAPI服务
cd "$PROJECT_ROOT"
$PYTHON_CMD -m uvicorn src.web_server:app --host 0.0.0.0 --port 8000 --reload --log-level info
