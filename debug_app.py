#!/usr/bin/env python3
"""
调试应用加载
"""

import sys
import os

print("=" * 60)
print("应用调试")
print("=" * 60)

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n[1/3] 尝试导入app...")
try:
    from src.app import app
    print("  ✓ app 导入成功")
except Exception as e:
    print(f"  ✗ app 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[2/3] 检查路由...")
print(f"  总路由数: {len(app.routes)}")
print("\n  所有路由:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"    - {route.path}")

print("\n[3/3] 检查OCR相关路由...")
ocr_routes = [route for route in app.routes if hasattr(route, 'path') and 'ocr' in route.path]
print(f"  找到 {len(ocr_routes)} 个OCR路由:")
for route in ocr_routes:
    print(f"    - {route.path}")

print("\n" + "=" * 60)
print("调试完成")
print("=" * 60)
