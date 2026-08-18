from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer


from utils.jwt import decode_token

'''
自动检查请求头里有没有 Authorization: Bearer <token>
如果没有，直接返回 403 Forbidden（连进函数的机会都不给）
如果有，把 token 封装成一个对象传进来
'''
security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # 取出真正的 JWT 字符串（比如 eyJhbGciOiJIUzI1NiIs...）
    payload = decode_token(token.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token无效"
        )
    return payload