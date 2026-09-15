from fastapi import APIRouter,Depends,HTTPException

from model.user import User
from schema.chat import ChatRequest,ChatResponse

from service.ai_service import ask_ai, ask_rag, ask_copilot
from utils.auth import get_current_user

router = APIRouter(prefix="/chat",tags=["AI助手"])

@router.post("",response_model=ChatResponse)
async def chat(
        request:ChatRequest,
        current_user:User = Depends(get_current_user)
):
    try:
        answer=await ask_ai(request.message)
        return ChatResponse(answer=answer)
    except Exception:
        raise HTTPException(status_code=500,detail="服务调用失败")


# 验收rag，暂时
@router.post(
    "/rag",
    response_model=ChatResponse
)
async def rag_chat(
    request: ChatRequest,

    current_user: User = Depends(
        get_current_user
    )
):
    try:

        answer = await ask_rag(
            request.message
        )

        return ChatResponse(
            answer=answer
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="RAG服务调用失败"
        )

@router.post("/copilot",response_model=ChatResponse)
async def copilot_chat(
        request: ChatRequest,
        current_user: User = Depends(get_current_user)
):
    try:
        answer = await ask_copilot(
            message=request.message,
            use_id=current_user.id
        )
        return ChatResponse(answer=answer)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Copilot调用失败"
        )
