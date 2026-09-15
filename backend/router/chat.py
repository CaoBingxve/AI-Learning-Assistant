import logging

from fastapi import APIRouter, Depends, HTTPException

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
    current_user: User = Depends(
        get_current_user
    )
):
    try:
        answer = await ask_copilot(
            message=request.message,
            user_id=current_user.id,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            answer=answer
        )

    except Exception:
        logger.exception(
            "Copilot 调用失败"
        )

        raise HTTPException(
            status_code=500,
            detail="Copilot调用失败"
        )