from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy.future import select
from models.users_models import User, UserSignIn
from database.connection import get_session
from auth.hash_password import HashPassword

from auth.jwt_handler import create_access_token, verify_access_token

user_router = APIRouter(tags=["User"])
hash_password = HashPassword()
users = []

@user_router.get("/test")
async def test() -> dict:
    return {"msg": "test"}

import bcrypt

@user_router.post("/signup", status_code=201)
async def insert(data: User, session = Depends(get_session) ) -> dict:

    if any(user.email == data.email for user in users): # = for user in users: if data.email == user.email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="존재하는 email"
        )
    #users.append(data)
    data.password = hash_password.create_hash( data.password )
    session.add(data)
    session.commit()

    session.refresh(data)
    print("refresh : ", data)

    return {"msg": "가입 성공"}

@user_router.post("/signin")
async def signin_user(data : UserSignIn = Form(...), session = Depends(get_session)) -> dict:
    # email, pwd 비교
    stmt = select(User).where(User.email == data.email)
    result = session.execute(stmt).scalar_one_or_none();
    if result:
        if hash.password.verify_hash(data.password, result.password):
            token = create_access_token(data.email)
            return{"token":token, "type":"bearer"}
        raise HTTPException(
                    status_code= status.HTTP_403_FORBIDDEN,
                    detail="비밀번호 틀림")
    raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 email")

    print("result : ", result)
    return{"msg" : "인증 성공"}
    '''
    print("signin : ", data)
    for user in users:
        if data.email == user.email:
            if hash.password.verify_hash(data.password, user.password):
                return {"msg":"인증 성공"}
            else:
                raise HTTPException(
                    status_code= status.HTTP_401_UNAUTHORIZED,
                    detail="비밀번호 틀림"
                )
    raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 email"
            )
    '''

@user_router.get("/all")
async def all_users(session = Depends(get_session)) -> list:
    users = session.query(User).all()
    return users

@user_router.get("/one")
async def one_users( id:int, token:str = Depends(verify_access_token), session = Depends(get_session)) -> dict:
    print("re_token : ", token)

    user = session.get(User, id)
    print("user dict : ", user.model_dump() )
    return user.dict()

@user_router.put("/put/{put_id}")
async def put_users( put_id : int, user : User, session = Depends(get_session)) -> dict:
    m_user = session.get(User, put_id)
    m_user.password = user.password
    m_user.name = user.name
    session.commit()
    return{"msg" : "수정성공"}

@user_router.delete("/del/{del_id}")
async def del_users( del_id : int, session = Depends(get_session)) -> dict:
    user = session.get(User, del_id)
    session.delete(user)
    session.commit()
    return{"msg" : "삭제 성공"}