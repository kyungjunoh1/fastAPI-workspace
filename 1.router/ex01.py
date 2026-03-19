from fastapi import FastAPI , APIRouter, Path, Query, HTTPException, status
from PackBook import User

app = FastAPI(title="TEST FASTAPI",
              description="fastapi example",
              version="1.0.0"
              )
router = APIRouter()

users = []

@router.get("/test")
async def test() -> dict:
    return {"msg":"test msg"}

@router.post("/insert")
async def insert( user : User ) -> dict:
    print( user )
    users.append(user)
    return{"msg":"데이터 추가 성공"}

@router.get("/select", response_model=list[User])
async def select() -> list:
    return users

@router.get("/path/{id}",
    responses={
        200: { "description": "successfully",
            "content": {
                "application/json": { "example": {"id": 1, "name": "홍길동"} }
            },
        },
        404: { "description": "User not found",
            "content": {
                "application/json": { "example": {} }
            },
        },
})

async def get_one(id:int) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {}

@router.get("/path2/{id}", response_model=User)
async def get_one2(id:int = Path(... ,description="사용자 id") ) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {}

@router.get("/query")
async def get_query(id: int) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {}

@router.get("/query2")
async def get_query2(id: int = Query(1, description="사용자 id")) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {}

@router.put("/update/{id}", status_code=200)
async def update(u:User, id:int) -> dict:
    for user in users:
        if user.id == id:
            user.name = u.name
            return{"msg":"update successfully"}
    raise HTTPException(status_code=404, detail="id 없음")

@router.delete("/delete", status_code=status.HTTP_200_OK)
async def del_all() -> dict:
    users.clear()
    return{"msg":"del succ"}

app.include_router( router )