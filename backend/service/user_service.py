from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.user import User
from schema.user import UserCreate

from utils.security import hash_password
async def create_user(db: AsyncSession, user:UserCreate):
    # 1.查询用户名是否存在
    result=await db.execute(
        select(User).where(User.username == user.username)
    )
    exist_user=result.scalar_one_or_none()
    if exist_user:
        return None
    # 2. 创建用户对象
    new_user=User(
        username=user.username,
        password_hash=hash_password(
            user.password
        )
    )
    # 3. 添加数据库
    db.add(new_user)

    # 4. 提交
    await db.commit()

    # 5. 刷新获取id
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id: int):
    result=await db.execute(
        select(User).where(User.id == user_id)
    )
    user=result.scalar_one_or_none()
    return user