import asyncio

from langchain_core.messages import (
    HumanMessage
)

from ai.copilot_graph import (
    create_copilot_graph
)


async def main():

    graph = create_copilot_graph(
        user_id=4
    )

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content=
                    # "什么是JWT？"
                    # "Copilot的内部测试代号是什么？"
                    # "我最近学习了什么？"
                    "根据我最近的学习记录和知识库资料，分析一下我接下来最值得复习什么"
                )
            ]
        }
    )

    for message in result["messages"]:
        message.pretty_print()

asyncio.run(main())