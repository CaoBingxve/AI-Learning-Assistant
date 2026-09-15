from unittest import result

from overrides import final

from ai.chat_chain import chat_chain
from ai.rag.rag_chain import rag_chain
from langchain_core.messages import HumanMessage
from ai.copilot_graph import create_copilot_graph

async def ask_ai(message:str)->str:
    answer = await chat_chain.ainvoke(
        {"message":message}
    )
    return answer

# retriever接收的输入是字符串，所以整个 rag_chain 最外层输入必须传字符串，不能传字典！
async def ask_rag(message: str) -> str:
    answer=await rag_chain.ainvoke(
        message
    )
    return answer

async def ask_copilot(
    message: str,
    user_id: int,
    conversation_id: str
) -> str:
    graph=create_copilot_graph(user_id)
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
                HumanMessage(content=message)
            ]
        },
        config=config
    )

    final_message=result["messages"][-1]

    return final_message.text