import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from router.user import router as user_router
from router.learning_record import router as learning_record_router
from router.chat import router as chat_router
from router.conversation import router as conversation_router
from config.database import engine, Base
from model.user import User
from model.learning_record import LearningRecord
from model.conversation import Conversation,ChatMessage
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动：创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 应用关闭
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(learning_record_router)
app.include_router(chat_router)
app.include_router(conversation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )