from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_database
from service.user_service import get_user_by_id
from utils.jwt import decode_access_token

'''
自动检查请求头里有没有 Authorization: Bearer <token>
如果没有，直接返回 403 Forbidden（连进函数的机会都不给）
如果有，把 token 封装成一个对象传进来
'''
security = HTTPBearer()

async def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    db:AsyncSession=Depends(get_database)
):
  token=credentials.credentials
  payload=decode_access_token(token)

  if payload is None:
    raise HTTPException(
      status_code=401,
      detail='Token无效或者过期'
    )

  user_id=payload.get('user_id')

  if user_id is None:
    raise HTTPException(
      status_code=401,
      detail='Token中缺少用户信息'
    )
  user=await get_user_by_id(db,user_id)

  if user is None:
    raise HTTPException(
      status_code=401,
      detail='用户不存在'
    )

  return user