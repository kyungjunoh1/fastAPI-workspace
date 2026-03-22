from fastapi import FastAPI, APIRouter
import uvicorn
from routes.users_routes import user_router

from contextlib import asynccontextmanager
from database.connection import conn
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("앱 시작")
    conn()
    yield
    print("앱 종료")

app = FastAPI(lifespan=lifespan)

# 허용할 출처 리스트
#origins = [ "http://localhost:3000", "https://myfrontend.com" ]
origins = ["*"] #모든 요청 허용

# 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처( 위에서 지정한 모든 경로 허용 * )
    allow_credentials=True, # 쿠키, 인증 토큰 전송 허용 여부
    allow_methods=["*"],    # 모든 HTTP 메서드 허용(GET, POST 등)
    allow_headers=["*"],    # 클라이언트가 보내는 모든 헤더 허용
)

router = APIRouter()
app.include_router( router )
app.include_router( user_router, prefix="/user" )
#app.include_router( post_router, prefix="/post" )

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)