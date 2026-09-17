import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_database
from model.user import User
from schema.chat import ChatResponse, CopilotRequest
from service.ai_service import ask_copilot
from utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["AI助手"]
)


@router.post(
    "/copilot",
    response_model=ChatResponse
)
async def copilot_chat(
    request: CopilotRequest,
    db: AsyncSession = Depends(
            get_database
        ),
    current_user: User = Depends(
        get_current_user
    )
):
    try:
        answer = await ask_copilot(
            message=request.message,
            user_id=current_user.id,
            conversation_id=request.conversation_id,
            db=db
        )

        return ChatResponse(
            answer=answer
        )
    except ValueError as error:
        if str(error)== "conversation_not_found":
            raise HTTPException(
                status_code=404,
                detail="会话不存在"
            )
        raise
    except Exception:
        logger.exception("Copilot 调用失败")

        raise HTTPException(
            status_code=500,
            detail="Copilot调用失败"
        )