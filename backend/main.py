import uvicorn
from fastapi import FastAPI
from router.user import router as user_router
from config.database import engine
from model.user import Base

app = FastAPI()
app.include_router(user_router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )