from fastapi import FastAPI, APIRouter
import uvicorn

from database.db_config import init_db
from contextlib import asynccontextmanager

from routes.user_route import user_route

@asynccontextmanager
async def lifespan(app : FastAPI):
    await init_db()
    print("db 실행")
    yield
    print("db종료 및 프로그램 종료")

app = FastAPI( lifespan = lifespan )

app.include_router(user_route, prefix="/user")

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)