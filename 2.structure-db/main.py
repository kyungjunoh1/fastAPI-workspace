from fastapi import FastAPI, APIRouter
import uvicorn
from routes.users_routes import user_router

from contextlib import asynccontextmanager
from database.connection import conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("앱 시작")
    conn()
    yield
    print("앱 종료")

app = FastAPI(lifespan=lifespan)
router = APIRouter()
app.include_router( router )
app.include_router( user_router, prefix="/user" )
#app.include_router( post_router, prefix="/post" )

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)