from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20, description='用户名长度3-20')
    password: str = Field(min_length=6, description='密码最少六位')


class UserResponse(BaseModel):
    username: str