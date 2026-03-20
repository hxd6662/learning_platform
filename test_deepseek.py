import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

print("="*60)
print("测试 DeepSeek API")
print("="*60)
print(f"\nAPI Key: {api_key[:10]}...{api_key[-10:] if api_key else 'None'}")
print()

try:
    from openai import OpenAI
    print("✓ OpenAI SDK 已安装")
    
    if api_key and api_key != "your-deepseek-api-key":
        print("✓ API Key 已配置")
        print()
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        print("正在发送测试请求...")
        print()
        
        SYSTEM_PROMPT = """你是一位耐心、友善的青少年学习导师，专门帮助中小学生学习。

请遵循以下原则：
1. 不要直接给出答案，而是通过提问引导学生自己思考，某些必要时刻可以给出提示或线索，甚至是直接给出答案。
2. 多用鼓励的语言
3. 用简单易懂的方式解释概念和原理
4. 帮助学生培养独立思考能力"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "你好，帮我解一下这道题：2x + 5 = 15"}
            ],
            stream=False,
            temperature=0.7,
            max_tokens=500
        )
        
        print("="*60)
        print("AI 回复：")
        print("="*60)
        print(response.choices[0].message.content)
        print("="*60)
        print("\n✓ DeepSeek API 测试成功！")
    else:
        print("✗ API Key 未配置或使用的是默认值")
        print("\n请在 .env 文件中配置正确的 DEEPSEEK_API_KEY")
        
except ImportError:
    print("✗ OpenAI SDK 未安装")
    print("\n请运行: pip install openai")
except Exception as e:
    print(f"✗ 发生错误: {e}")
    import traceback
    traceback.print_exc()

print()
