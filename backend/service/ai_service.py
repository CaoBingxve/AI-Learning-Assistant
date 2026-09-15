from langchain_core.messages import HumanMessage

from ai.copilot_graph import create_copilot_graph


async def ask_copilot(
    message: str,
    user_id: int,
    conversation_id: str
) -> str:

    graph = create_copilot_graph(
        user_id
    )

    thread_id = (
        f"user_{user_id}:"
        f"{conversation_id}"
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content=message
                )
            ]
        },
        config=config
    )

    final_message = (
        result["messages"][-1]
    )

    return final_message.text