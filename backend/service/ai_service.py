from ai.chat_chain import chat_chain
from ai.rag.rag_chain import rag_chain

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
