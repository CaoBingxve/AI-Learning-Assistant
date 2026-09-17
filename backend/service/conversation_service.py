from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.conversation import Conversation,ChatMessage

async def create_conversation(db:AsyncSession,user_id:int) -> Conversation:
    """
    为当前用户创建一个新对话。
    """
    conversation = Conversation(
        id=str(uuid4()),
        user_id=user_id,
        title="新对话",
    )
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    return conversation

async def get_conversations_by_user(db:AsyncSession,user_id:int) -> list[Conversation]:
    """
    获取当前用户全部会话，
    最近更新的排在最前。
    """
    result=await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    )
    return list(result.scalars().all())

async def get_conversation_by_user(
    db: AsyncSession,
    conversation_id: str,
    user_id: int
) -> Conversation | None:
    """
    获取一个属于当前用户的会话。

    注意：
    不允许只按照 conversation_id 查询。
    必须同时校验 user_id。
    """
    result = await db.execute(
        select(Conversation)
        .where(
            Conversation.id== conversation_id,
            Conversation.user_id== user_id
        )
    )

    return result.scalar_one_or_none()

async def get_messages_by_conversation(
        db: AsyncSession,
        conversation_id: str,
        user_id: int
)->list[ChatMessage]:
    """
    获取会话历史消息。
    先验证这个会话确实属于当前用户。
    """
    conversation = await get_conversation_by_user(db,conversation_id,user_id)
    if not conversation:
        return []
    result=await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation.id)
        .order_by(ChatMessage.created_at.asc(),ChatMessage.id.asc())
    )

    return list(result.scalars().all())

async def add_message(
        db: AsyncSession,
        conversation_id: str,
        user_id: int,
        role:str,
        content:str
)->ChatMessage|None:
    """
    为当前会话保存一条消息。
    """
    conversation = await get_conversation_by_user(db,conversation_id,user_id)
    if not conversation:
        return None
    message = ChatMessage(
        conversation_id=conversation.id,
        role=role,
        content=content
    )
    db.add(message)
    # 每次有新消息时，
    # 更新会话时间
    conversation.updated_at = (
        datetime.now()
    )
    # 第一条用户消息自动作为标题
    if role=="user" and conversation.title=="新对话":
        title=content.strip().replace("\n"," ")
        if len(title)>30:
            title=title[:30]+"..."

        conversation.title=title or "新对话"

    await db.flush()
    await db.refresh(message)
    return message

