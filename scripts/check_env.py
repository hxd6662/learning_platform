#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
环境检查脚本
检查所有必要的依赖是否已安装
"""

import sys

def check_module(module_name, display_name=None):
    """检查模块是否已安装"""
    if display_name is None:
        display_name = module_name

    try:
        __import__(module_name)
        version = None

        # 尝试获取版本
        try:
            module = sys.modules[module_name]
            if hasattr(module, '__version__'):
                version = module.__version__
        except:
            pass

        if version:
            print(f"✅ {display_name}: {version}")
        else:
            print(f"✅ {display_name}: 已安装")
        return True
    except ImportError:
        print(f"❌ {display_name}: 未安装")
        return False

def main():
    print("=" * 50)
    print("AI智能学习助手 - 环境检查")
    print("=" * 50)
    print()

    print("Python信息:")
    print(f"  版本: {sys.version}")
    print(f"  路径: {sys.executable}")
    print()

    print("依赖检查:")
    print("-" * 50)

    modules = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("langchain", "LangChain"),
        ("langchain_core", "LangChain Core"),
        ("langchain_openai", "LangChain OpenAI"),
        ("langgraph", "LangGraph"),
        ("pydantic", "Pydantic"),
        ("langchain_core.messages", "LangChain Messages"),
    ]

    all_ok = True
    for module, display in modules:
        if not check_module(module, display):
            all_ok = False

    print("-" * 50)
    print()

    if all_ok:
        print("🎉 所有依赖都已安装！")
        print()
        print("可以运行以下命令启动Web平台:")
        print("  Windows: scripts\\start_web_platform.bat")
        print("  Linux/Mac: ./scripts/start_web_platform.sh")
        return 0
    else:
        print("⚠️  部分依赖未安装")
        print()
        print("请运行以下命令安装依赖:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
