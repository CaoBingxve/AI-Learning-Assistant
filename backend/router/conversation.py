from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_database
from model.user import User
from schema.conversation import ConversationResponse,ChatMessageResponse
from service.conversation_service import (
    create_conversation,
    get_conversation_by_user,
    get_conversations_by_user,
    get_messages_by_conversation
)

from utils.auth import get_current_user

router = APIRouter(prefix="/conversations",tags=["会话"])

@router.post("",response_model=ConversationResponse)
async def create_new_conversation(
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    创建新的聊天会话。
    """
    conversation = await create_conversation(db, current_user.id)
    return conversation

@router.get("",response_model=list[ConversationResponse])
async def get_conversations(
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    获取当前用户历史会话列表。
    """
    return (
        await get_conversations_by_user(db, current_user.id)
    )

@router.get("/{conversation_id}/messages",response_model=list[ChatMessageResponse])
async def get_conversation_messages(
        conversation_id: str,
        db: AsyncSession = Depends(get_database),
        current_user: User = Depends(get_current_user)
):
    """
    获取一个会话中的历史消息。
    """
    conversation = await get_conversation_by_user(db, conversation_id,current_user.id)

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="会话不存在"
        )
    return await get_messages_by_conversation(db, conversation_id,current_user.id)
