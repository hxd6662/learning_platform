import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    OpenAI = None

ASSISTANT_SYSTEM_PROMPT = """你是一位温柔风趣、谈吐优雅、有耐心、有风度的全科学习辅导老师，面向中小学生，专注于学习辅导、知识点讲解、作业答疑、错题分析与学习计划制定。

你的风格要求：
1. 幽默轻松但不失稳重，说话亲切自然，不幼稚、不油腻、不严肃刻板，像一位让人喜欢又值得信任的良师益友。
2. 始终温柔包容，不批评、不指责、不打击学生，遇到不会、答错、走神、畏难的情况，先安抚情绪再耐心引导。

你的核心能力与行为规则：

一、答题与讲解原则（全科辅导）
1. 覆盖语文、数学、英语、物理、化学、生物、历史、地理、政治等所有中小学学科。
2. 不直接给出最终答案，而是拆解步骤、提示关键点、引导思路，让学生自己思考得出结果。
3. 用简单易懂、生活化的比喻讲解知识点，结构清晰，重点突出，便于青少年理解记忆。

二、错题讲解能力
1. 学生发来错题时，先温和指出错误原因，如概念不清、粗心、步骤遗漏、思路偏差。
2. 不直接纠正，而是一步步引导学生发现问题，再给出正确思路和规范步骤。
3. 总结同类题目的解题技巧，帮助学生避免再犯类似错误。
4. 结尾一定搭配鼓励，强化信心。

三、鼓励话术机制
1. 学生认真思考、主动提问、有所进步时，及时给予具体、真诚的表扬。
2. 学生做错题、不会做、情绪低落时，使用鼓励式语言，如：
   - 没关系，我们慢慢来，你已经在思考了，这就很棒。
   - 错一次不可怕，弄懂它，下次它就是你的得分点。
   - 你很有潜力，再坚持一下就懂了。
   - 能主动问问题，说明你特别认真。
3. 全程保持正向、温暖、有力量。

四、学习计划小功能
1. 可根据学生年级、科目薄弱点、可用时间，帮其制定简洁、可执行的每日/每周学习小计划。
2. 计划合理不繁重，侧重碎片时间利用、薄弱科目补强、错题回顾、预习复习节奏。
3. 提醒学习方法，如错题本使用、记忆技巧、专注小技巧，不制造焦虑。

五、边界与安全
1. 只专注学习相关内容，温和拒绝无关闲聊、不良信息、游戏娱乐等请求。
2. 不布置过量任务，不给学生压力，注重保护学习兴趣。
3. 谈吐文明得体，积极向上，传递健康价值观。

请始终以温柔、风趣、专业、有风度的全科辅导老师身份，陪伴学生高效、快乐地学习。"""

PHOTO_SEARCH_SYSTEM_PROMPT = """你是一位专业、高效的解题专家，专门负责解决学生的题目问题。

你的工作方式：
1. 快速准确地理解题目内容
2. 给出清晰、详细的解题步骤和思路
3. 提供完整的解答过程和最终答案
4. 确保解析通俗易懂，逻辑清晰

回答格式要求：
1. 【题目分析】简要说明题目考察的知识点和解题方向
2. 【解题思路】分步骤引导思考，说明每一步的目的
3. 【详细解答】给出完整的解题过程，包括计算、推理等
4. 【最终答案】明确给出最终答案
5. 【知识点总结】总结本题涉及的关键知识点

请用专业、高效、清晰的方式回答问题，确保学生能够理解解题过程并学会类似题目的解法。"""

class DeepSeekService:
    def __init__(self, api_key_env: str = "DEEPSEEK_API_KEY_ASSISTANT", system_prompt: str = ASSISTANT_SYSTEM_PROMPT):
        self.api_key = os.getenv(api_key_env)
        self.base_url = "https://api.deepseek.com"
        self.system_prompt = system_prompt
        self.client = None
        if HAS_OPENAI and self.api_key and self.api_key != "your-deepseek-api-key" and self.api_key != "sk-your-old-assistant-api-key":
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
    
    def is_available(self):
        return self.client is not None
    
    def chat(self, user_message: str, conversation_history: list = None) -> str:
        if not self.is_available():
            if HAS_OPENAI:
                return (
                    "你好！我是你的AI学习助手。\n\n"
                    "关于你的问题：{}\n\n"
                    "这是一个模拟回复。DeepSeek API已配置，可以使用真实服务了！"
                ).format(user_message)
            else:
                return (
                    "你好！我是你的AI学习助手。\n\n"
                    "关于你的问题：{}\n\n"
                    "提示：请先安装OpenAI SDK：pip install openai"
                ).format(user_message)
        
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"抱歉，发生了一些问题：{str(e)}\n\n让我们稍后再试吧！"
    
    def analyze_question(self, question_text: str, subject: str = None) -> dict:
        if not self.is_available():
            return {
                "question_type": subject or "题目",
                "knowledge_point": "相关知识点",
                "difficulty": "medium",
                "analysis": "这是一道{0}题目。\n\n解题提示：\n1. 先理解题目要求\n2. 回忆相关知识点\n3. 一步步思考解题方法\n\n相信你可以自己解决的！".format(subject or "学习"),
                "correct_answer": None,
                "similar_questions": [],
                "related_resources": []
            }
        
        try:
            prompt = f"""请分析以下题目，返回JSON格式（不要包含markdown代码块标记，直接返回JSON）：

题目：{question_text}
{'科目：' + subject if subject else ''}

请返回以下格式的JSON：
{{
    "question_type": "题目类型（如：数学题、语文题等）",
    "knowledge_point": "考察的知识点",
    "difficulty": "难度（easy/medium/hard）",
    "analysis": "引导式的解题分析，不要直接给出答案，而是用提问的方式引导思考",
    "similar_questions": [
        {{"id": 1, "text": "类似题目1"}},
        {{"id": 2, "text": "类似题目2"}}
    ],
    "related_resources": [
        {{"id": 1, "title": "相关知识点教程", "type": "video/article"}}
    ]
}}"""

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的题目分析专家。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False,
                temperature=0.3
            )
            
            import json
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except:
                return {
                    "question_type": subject or "题目",
                    "knowledge_point": "相关知识点",
                    "difficulty": "medium",
                    "analysis": content,
                    "similar_questions": [],
                    "related_resources": []
                }
        
        except Exception as e:
            return {
                "question_type": subject or "题目",
                "knowledge_point": "相关知识点",
                "difficulty": "medium",
                "analysis": f"分析时出错：{str(e)}",
                "similar_questions": [],
                "related_resources": []
            }


_assistant_service = None
_photo_search_service = None

def get_deepseek_service() -> DeepSeekService:
    global _assistant_service
    if _assistant_service is None:
        _assistant_service = DeepSeekService(
            api_key_env="DEEPSEEK_API_KEY_ASSISTANT",
            system_prompt=ASSISTANT_SYSTEM_PROMPT
        )
    return _assistant_service

def get_photo_search_service() -> DeepSeekService:
    global _photo_search_service
    if _photo_search_service is None:
        _photo_search_service = DeepSeekService(
            api_key_env="DEEPSEEK_API_KEY_PHOTO_SEARCH",
            system_prompt=PHOTO_SEARCH_SYSTEM_PROMPT
        )
    return _photo_search_service
