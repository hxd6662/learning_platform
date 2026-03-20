#!/usr/bin/env python3
"""
测试拍照搜题功能 - OCR识别 + DeepSeek AI分析
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("拍照搜题功能测试")
print("=" * 60)

# 1. 检查所有配置
print("\n[1/5] 检查环境配置...")

# 检查阿里云OCR配置
access_key_id = os.getenv("ALIYUN_OCR_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIYUN_OCR_ACCESS_KEY_SECRET")
print(f"  阿里云OCR配置: {'✓' if access_key_id and access_key_secret else '✗'}")

# 检查DeepSeek API key配置
assistant_key = os.getenv("DEEPSEEK_API_KEY_ASSISTANT")
photo_search_key = os.getenv("DEEPSEEK_API_KEY_PHOTO_SEARCH")
print(f"  AI助手API Key: {'✓' if assistant_key else '✗'}")
print(f"  拍照搜题API Key: {'✓' if photo_search_key else '✗'}")

# 2. 检查依赖库
print("\n[2/5] 检查依赖库...")
try:
    import requests
    print("  ✓ requests 已安装")
except ImportError:
    print("  ✗ requests 未安装")
    sys.exit(1)

try:
    from openai import OpenAI
    print("  ✓ openai 已安装")
except ImportError:
    print("  ✗ openai 未安装")
    sys.exit(1)

# 3. 测试服务导入
print("\n[3/5] 测试服务模块...")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.services.ocr_service import get_aliyun_ocr_service
    from src.services.ai_service import get_deepseek_service, get_photo_search_service
    print("  ✓ 成功导入服务模块")
except Exception as e:
    print(f"  ✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 测试OCR服务
print("\n[4/5] 测试阿里云OCR服务...")
try:
    ocr_service = get_aliyun_ocr_service()
    print(f"  ✓ OCR服务状态: {ocr_service.is_available}")
except Exception as e:
    print(f"  ✗ OCR服务测试失败: {e}")

# 5. 测试DeepSeek服务
print("\n[5/5] 测试DeepSeek AI服务...")

try:
    # 测试AI助手服务
    assistant_service = get_deepseek_service()
    print(f"  ✓ AI助手服务可用: {assistant_service.is_available()}")
    
    # 测试拍照搜题服务
    photo_search_service = get_photo_search_service()
    print(f"  ✓ 拍照搜题服务可用: {photo_search_service.is_available()}")
    
except Exception as e:
    print(f"  ✗ DeepSeek服务测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试结果总结")
print("=" * 60)

print("\n✅ 基础服务配置检查完成！")
print("\n服务状态:")
print(f"  - 阿里云OCR: {'正常' if access_key_id and access_key_secret else '配置不完整'}")
print(f"  - AI助手API: {'正常' if assistant_key else '未配置'}")
print(f"  - 拍照搜题API: {'正常' if photo_search_key else '未配置'}")

print("\n📋 可用的API端点:")
print("  - POST /api/v1/ocr/recognize  - 纯OCR识别")
print("  - POST /api/v1/ocr/photo-search - 拍照搜题（OCR+AI分析）")

print("\n" + "=" * 60)
print("\n提示: 请通过前端界面或API文档进行实际功能测试")
print("API文档地址: http://localhost:8001/docs")
print("=" * 60)
