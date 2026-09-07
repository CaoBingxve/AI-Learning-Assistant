import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from dotenv import load_dotenv


load_dotenv()


# 服务器的秘密钥匙
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# 使用 HS256 算法签名
ALGORITHM = "HS256"


# 生成 Token
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    # 复制一份要放进 JWT 的数据
    to_encode = data.copy()

    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=30
        )

    # 把过期时间放进 JWT
    to_encode["exp"] = expire

    # 生成 JWT
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token:str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        return None