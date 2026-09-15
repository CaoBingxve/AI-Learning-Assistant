import asyncio

from ai.tools import (
    search_knowledge,
    create_learning_record_tool
)


async def main():

    print("===== 知识库 Tool =====")

    result = await search_knowledge.ainvoke(
        {
            "query":
                "Copilot内部测试代号是什么？"
        }
    )

    print(result)


    print("\n===== 学习记录 Tool =====")

    tool = create_learning_record_tool(
        user_id=4
    )

    result = await tool.ainvoke({})

    print(result)


asyncio.run(main())