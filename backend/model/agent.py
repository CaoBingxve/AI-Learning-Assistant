import asyncio

class QuestionAgent:
    def __init__(self):
        self.name = '问答智能体'

    async def ask(self, question):
        await asyncio.sleep(0.5)
        return {
            "agent_name": self.name,
            "question": question,
            "answer": f"智能体收到问题：{question}，正在解析内容"
        }

class ErrorAgent:
    def __init__(self):
        self.name = '错题智能体'
        self.error_list = []

    def add_error(self, error):
        self.error_list.append(error)

    async def analyze_error(self, question):
        await asyncio.sleep(0.5)
        return {
            "agent_name": self.name,
            'question': question,
            'analyze': '解析错误和考点'
        }

class PlanningAgent:
    def __init__(self):
        self.name = '计划智能体'

    async def generate_plan(self, subject, error_list):
        await asyncio.sleep(0.5)
        return {
            "agent_name": self.name,
            'subject': subject,
            'error_list': error_list,
            'plan': '生成的计划'
        }

async def main():
    # 实例化三个智能体
    qa_agent = QuestionAgent()
    err_agent = ErrorAgent()
    plan_agent = PlanningAgent()

    # 1.问答智能体提问
    print(await qa_agent.ask("什么是Python异步？"))

    # 2.错题智能体添加错题、解析错题
    err_agent.add_error("for循环边界写错")
    print(await err_agent.analyze_error("for循环遍历报错"))

    # 3.计划智能体根据错题生成学习计划
    print(await plan_agent.generate_plan("Python基础", err_agent.error_list))

asyncio.run(main())