@echo off
echo ========================================
echo 青少年智能学习平台 - 后端启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

echo [1/3] 检查环境配置...
if not exist .env (
    echo [警告] 未找到.env文件，正在从.env.example创建...
    copy .env.example .env
    echo [提示] 请编辑.env文件配置数据库和API密钥
)

echo.
echo [2/3] 初始化数据库...
python scripts/init_db.py
if errorlevel 1 (
    echo [错误] 数据库初始化失败，请检查配置
    pause
    exit /b 1
)

echo.
echo [3/3] 启动FastAPI服务器...
echo.
echo 服务器将在 http://localhost:8000 启动
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务器
echo.

python -m src.app

pause
