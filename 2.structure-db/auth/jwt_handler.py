import time
from datetime import datetime

from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader

from jose import jwt, JWTError

SECRET_KEY = "값 처리"

api_key_header = APIKeyHeader(name="Authorization")

def create_access_token(email:str) -> str:
    payload = {"sub":email, "expires":time.time() + 20} #만료시간 20초 후


    #헤더(알고리즘),페이로드(변환된값),서명
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("token : ", token, type(token) )
    return token

def verify_access_token(token:str = Security(api_key_header) ) -> str:
    #print("verify_access_token : ", token)
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256" )
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="로그인 먼저 하세요"
            )
        if datetime.now() > datetime.fromtimestamp( expire ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="토큰 만료 됨!!!"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="토큰에 문제 있음!!!"
        )
    return "내용 확인"