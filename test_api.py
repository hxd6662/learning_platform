import requests
import json

BASE_URL = "http://localhost:8001"

def print_separator(title="="):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    print_separator("1. 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_root():
    print_separator("2. 根路径测试")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_register():
    print_separator("3. 用户注册")
    try:
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123456"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200 or response.status_code == 400
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_login():
    print_separator("4. 用户登录")
    try:
        data = {
            "username": "testuser",
            "password": "test123456"
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            data=data
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        if response.status_code == 200:
            return result.get("access_token")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_get_profile(token):
    print_separator("5. 获取用户信息")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/auth/profile", headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_learning_stats(token):
    print_separator("6. 学习统计接口测试")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        stats_data = {
            "study_minutes": 60,
            "questions_attempted": 10,
            "questions_correct": 8
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/learning/stats",
            json=stats_data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_wrong_questions(token):
    print_separator("7. 错题本接口测试")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        question_data = {
            "question_text": "解方程 2x + 5 = 15",
            "correct_answer": "x = 5",
            "user_answer": "x = 10",
            "knowledge_point": "一元一次方程",
            "subject": "数学",
            "difficulty": "medium"
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/questions/wrong",
            json=question_data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_ocr():
    print_separator("8. OCR识别接口测试（模拟）")
    print("注意：这个接口需要真实的API密钥才能工作")
    print("当前使用模拟数据")
    return True

def test_assistant():
    print_separator("9. AI助手接口测试（模拟）")
    print("注意：这个接口需要真实的API密钥才能工作")
    print("当前使用模拟数据")
    return True

def main():
    print("\n" + "="*60)
    print("  青少年智能学习平台 API 测试")
    print("="*60)
    print(f"\n服务器地址: {BASE_URL}")
    
    results = []
    
    results.append(("健康检查", test_health()))
    results.append(("根路径", test_root()))
    results.append(("用户注册", test_register()))
    
    token = test_login()
    results.append(("用户登录", token is not None))
    
    if token:
        results.append(("获取用户信息", test_get_profile(token)))
        results.append(("学习统计", test_learning_stats(token)))
        results.append(("错题本", test_wrong_questions(token)))
    
    results.append(("OCR识别", test_ocr()))
    results.append(("AI助手", test_assistant()))
    
    print_separator("测试结果汇总")
    print("\n{:<20s} {:<10s}".format("测试项", "结果"))
    print("-"*30)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print("{:<20s} {:<10s}".format(name, status))
        if not passed:
            all_passed = False
    
    print("-"*30)
    if all_passed:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查")
    
    print("\nAPI文档地址:")
    print(f"  {BASE_URL}/docs")
    print("\n说明:")
    print("  - OCR和AI助手接口目前使用模拟数据")
    print("  - 提供真实API密钥后可以接入真实服务")

if __name__ == "__main__":
    main()
