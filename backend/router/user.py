from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user: User):
    return {
        "message": "注册成功",
        "username": user.username
    }