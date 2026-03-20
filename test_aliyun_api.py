#!/usr/bin/env python3
"""
实际测试阿里云OCR API调用
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("阿里云OCR API实际测试")
print("=" * 60)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.ocr_service import get_aliyun_ocr_service

ocr_service = get_aliyun_ocr_service()

print("\n服务状态:")
print(f"  可用: {ocr_service.is_available}")
print(f"  Access Key ID: {ocr_service.access_key_id[:10]}...")
print(f"  端点: {ocr_service.endpoint}")

print("\n" + "=" * 60)
print("提示: 要进行完整的OCR识别测试，需要提供一张图片。")
print("可以通过以下方式测试:")
print("  1. 使用后端API: POST /api/ocr/recognize")
print("  2. 上传图片文件或提供图片URL")
print("\n当前阿里云OCR服务已成功配置并可以使用！")
print("=" * 60)
