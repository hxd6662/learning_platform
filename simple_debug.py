#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    print("1. Importing dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✓ dotenv ok")
except Exception as e:
    print(f"   ✗ dotenv failed: {e}")
    sys.exit(1)

try:
    print("2. Importing FastAPI...")
    from fastapi import FastAPI
    print("   ✓ FastAPI ok")
except Exception as e:
    print(f"   ✗ FastAPI failed: {e}")
    sys.exit(1)

try:
    print("3. Importing ocr module...")
    from src.api import ocr
    print("   ✓ ocr module ok")
    print(f"   Router has {len(ocr.router.routes)} routes")
    for route in ocr.router.routes:
        print(f"     - {route.path}")
except Exception as e:
    print(f"   ✗ ocr module failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Importing services...")
    from src.services import get_deepseek_service, get_photo_search_service, get_aliyun_ocr_service
    print("   ✓ services ok")
except Exception as e:
    print(f"   ✗ services failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All imports successful!")
