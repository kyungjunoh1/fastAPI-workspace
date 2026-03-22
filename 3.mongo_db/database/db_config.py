import motor.motor_asyncio
from beanie import init_beanie
from models.user_model import User

MONGODB_URL = "mongodb://localhost:27017"

async def init_db():
    #db와 fastapi 연동(connection)
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    # 사용할 db 설정(있다가 생성-mydatabase)
    database = client.mydatabase
    #db 초기화 및 모델 적용
    await init_beanie(database=database, document_models=[User])