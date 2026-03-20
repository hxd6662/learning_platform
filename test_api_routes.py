#!/usr/bin/env python3
"""
测试API路由是否正常工作
"""

import requests
import json

print("=" * 60)
print("API路由测试")
print("=" * 60)

BASE_URL = "http://localhost:8001"

# 1. 测试根路径
print("\n[1/4] 测试根路径...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ 根路径正常")
        print(f"  响应: {response.json()}")
    else:
        print(f"  ✗ 根路径异常")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 2. 测试健康检查
print("\n[2/4] 测试健康检查...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ 健康检查正常")
        print(f"  响应: {response.json()}")
    else:
        print(f"  ✗ 健康检查异常")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 3. 测试API文档
print("\n[3/4] 测试API文档...")
try:
    response = requests.get(f"{BASE_URL}/docs")
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ API文档可访问")
    else:
        print(f"  ✗ API文档异常")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 4. 列出所有可用的API路由
print("\n[4/4] 获取OpenAPI schema...")
try:
    response = requests.get(f"{BASE_URL}/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        paths = schema.get("paths", {})
        print(f"  ✓ 找到 {len(paths)} 个API端点:")
        for path, methods in paths.items():
            for method in methods.keys():
                print(f"    - {method.upper()} {path}")
    else:
        print(f"  ✗ 获取schema失败")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
