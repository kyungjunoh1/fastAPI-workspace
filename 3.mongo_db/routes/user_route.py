from fastapi import APIRouter
from models.user_model import User

user_route = APIRouter(tags=["User"])

@user_route.get("/all")
async def all_user():
    users = User.find_all()
    print("users : ", users)
    data = await users.to_list()
    print("실제 데이터 : ", data)
    return data

@user_route.post("/insert")
async def insert(user : User):
    await user.create()
    return {"id":str(user.id)}

@user_route.get("/one/{user_id}")
async def one_user(user_id : str):
    user = User.get(user_id)
    if user:
        return await user
    return{"msg":"데이터 없음"}

@user_route.get("/name/{user_name}")
async def one_user(user_name : str):
    user = await User.find_one(User.name == user_name)
    if user:
        return  user
    return{"msg":"데이터 없음"}

@user_route.delete("/del/{user_name}")
async def del_user(user_name : str):
    count = await User.find_one(User.name == user_name).delete()
    return{"msg" : f"삭제 된 수 : {count}"}

@user_route.put("/update/{user_name}")
async def update_user(user_name:str, new_age:int):
    user = await User.find_one(User.name == user_name)
    user.age = new_age
    await user.save()
    return{"msg" : "수정 성공", "user" : user}