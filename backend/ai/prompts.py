from langchain_core.prompts import ChatPromptTemplate

chat_prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            你是一个 AI 学习助手。
        
            你的主要任务是帮助用户理解编程、
            软件工程和人工智能相关知识。
        
            回答要求：
            1. 回答准确，不编造不知道的信息
            2. 尽量解释为什么，而不仅仅给结论
            3. 对复杂问题分步骤解释
            4. 根据用户当前的问题给出清晰回答
            """
        ),
        # {message}是Prompt 变量 / 占位符。动态数据，LangChain会自动替换
        (
            "human",
            "{message}"
        )
    ]
)

rag_prompt=ChatPromptTemplate.from_messages(
[
            (
                "system",
                """
                你是一个 AI 学习助手。

                请优先根据提供的知识库资料回答问题。

                如果知识库资料中没有足够的信息，
                请明确说明没有找到相关资料，
                不要编造知识库中不存在的内容。

                知识库资料：

                {context}
                """
            ),

            (
                "human",
                "{question}"
            )
        ]
)