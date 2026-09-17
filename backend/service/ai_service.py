from langchain_core.messages import AIMessage,HumanMessage

from sqlalchemy.ext.asyncio import AsyncSession

from ai.copilot_graph import create_copilot_graph

from service.conversation_service import (
    add_message,
    get_conversation_by_user,
    get_messages_by_conversation,
)

async def ask_copilot(
    message: str,
    user_id: int,
    conversation_id: str,
    db: AsyncSession
) -> str:
    """
    Copilot 核心调用。
    流程：
    1. 验证会话属于当前用户
    2. 保存用户消息
    3. 从MySQL读取完整历史
    4. 转成LangChain Messages
    5. 交给LangGraph Agent
    6. 保存AI回答
    """

    conversation = await get_conversation_by_user(db,conversation_id,user_id)

    if not conversation:
        raise ValueError(
            "conversation_not_found"
        )


    # =========================
    # 保存用户消息
    # =========================

    await add_message(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=message
    )


    # =========================
    # 加载完整历史
    # =========================

    history = await get_messages_by_conversation(db,conversation_id,user_id)
    role_map={"user":HumanMessage,"assistant":AIMessage}
    langchain_messages = [
        role_map[item.role](content=item.content)
        for item in history
        if item.role in role_map
    ]


    # =========================
    # 调用Agent
    # =========================

    graph = create_copilot_graph(user_id)

    result = await graph.ainvoke(
        {
            "messages":langchain_messages
        }
    )

    final_message = result["messages"][-1]

    content = final_message.content

    if isinstance(content,str):
        answer = content
    elif isinstance(content, list):
        # 提取所有 text 类型的块
        text_parts = [
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        answer = "".join(text_parts)
    else:
        answer = str(content)


    # =========================
    # 保存AI回答
    # =========================

    await add_message(
        db=db,
        conversation_id=(
            conversation_id
        ),
        user_id=user_id,
        role="assistant",
        content=answer
    )


    return answer
