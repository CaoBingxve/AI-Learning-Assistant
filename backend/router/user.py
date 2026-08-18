from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schema.user import UserCreate, UserResponse,UserLogin
from config.database import get_database

from service.user_service import (
    create_user,
    get_user_by_id, authenticate_user
)
from utils.jwt import create_access_token
from utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["用户模块"])

@router.post(
    "/register",
    response_model=UserResponse
)
async def register(user:UserCreate, db:AsyncSession = Depends(get_database)):
    result=await create_user(db, user)
    if result is None:
        raise HTTPException(status_code=400,detail="用户名已经存在")

    return result

@router.get('/{user_id}', response_model=UserResponse)
async def get_users(user_id:int,current_user=Depends(get_current_user),db:AsyncSession = Depends(get_database)):
    user = await get_user_by_id(db, user_id)
    # if user is None:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="用户不存在"
    #     )
    return user

@router.post("/login")
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_database)
):
    result=await authenticate_user(db, user.username, user.password)
    if result is None:
        raise HTTPException(status_code=404,detail='用户名或密码错误')
    access_token = create_access_token(
        data={
            "user_id": result.id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }