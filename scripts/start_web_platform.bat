@echo off
REM AI智能学习助手 - Web平台启动脚本 (Windows - 通用版)

echo ==================================
echo AI智能学习助手 - Web平台
echo ==================================
echo.

REM 获取脚本所在目录
cd /d "%~dp0"
set PROJECT_ROOT=%CD%

echo 📁 项目目录: %PROJECT_ROOT%
echo.

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python
    echo 请确保Python已安装并添加到系统PATH
    pause
    exit /b 1
)

REM 显示Python版本
echo 🐍 Python版本:
python --version
echo.

REM 进入项目根目录
cd /d "%PROJECT_ROOT%"

REM 检查配置文件
if not exist "config\agent_llm_config.json" (
    echo ❌ 错误: 未找到配置文件 config\agent_llm_config.json
    pause
    exit /b 1
)

echo ✅ 配置文件检查通过
echo.

REM 检查并安装依赖
echo 🔍 检查依赖...
python -c "import fastapi, uvicorn, langchain" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  缺少必要的依赖，正在安装...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo.
)

echo ✅ 依赖检查通过
echo.

REM 启动服务
echo 🚀 启动Web服务...
echo.
echo 📍 访问地址: http://localhost:8000
echo 📍 前端页面: http://localhost:8000/static/index.html
echo.
echo ⏹️  按 Ctrl+C 停止服务
echo.
echo ==================================
echo.

REM 启动FastAPI服务
python -m uvicorn src.web_server:app --host 0.0.0.0 --port 8000 --reload --log-level info

pause
