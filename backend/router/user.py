from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schema.user import UserCreate, UserResponse
from config.database import get_database

from service.user_service import (
    create_user,
    get_user_by_id
)

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
async def get_users(user_id:int,db:AsyncSession = Depends(get_database)):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    return user
