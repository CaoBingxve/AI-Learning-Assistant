import uvicorn
from fastapi import FastAPI
from router import user


app = FastAPI()

app.include_router(
    user.router,
    prefix="/user"
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )