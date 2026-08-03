from fastapi import APIRouter
from schema.user import UserCreate, UserResponse

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse
)
async def register(user: UserCreate):
    return {
        "username": user.username
    }