import http
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from apis.utils import OAuth2PasswordBearerWithCookie
from fastapi import Depends
from fastapi import APIRouter, HTTPException, status, Request
from db.session import get_db
from sqlalchemy.orm import Session
from core.config import settings
from datetime import timedelta
from core.security import create_access_token
from core.hashing import Hasher
from jose import jwt, JWTError
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

import json
from requests.auth import HTTPBasicAuth

from http.client import HTTPSConnection
from base64 import b64encode

import sys
import os
import hashlib
import hmac
import base64
import requests
import time
from starlette.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def authenticate_user(username: str, password: str, db: Session):
    user = get_users(username=username, db=db)
    print('user 확인: ', jsonable_encoder(user[:]))
    user = jsonable_encoder(user[:])

    if not user:
        print('id error')
        return False
    elif not Hasher.verify_password(password, user[0]['hashed_password']):
        print('password error')
        return False
    return user


@router.post("/token")
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return templates.TemplateResponse(
        "login.html",
        {"request": "정보가 올바르지 않습니다."}
        )   
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid username or password",
        # )
    # print(jsonable_encoder(user[:])[0]['uid'])
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": jsonable_encoder(user[:])[0]['id']}, expires_delta=access_token_expire
    )
    print('access token: ', access_token)
    print('access token: ', datetime.utcnow() + timedelta(minutes=1))
    # response.set_cookie(key="access_tkn", value=f"Bearer {access_token}")
    # response.set_cookie(key="access_tkn", value=access_token, expires= (datetime.utcnow() + timedelta(minutes=1)) )
    
    # return {"access_token": access_token, "token_type": "bearer"}
    return response


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


timestamp = int(time.time() * 1000)
timestamp = str(timestamp)
access_key = "vBlKN4Z6s5GSU1usLIef" # access key id (from portal or Sub Account)
# secret key (from portal or Sub Account)

url = 'https://sens.apigw.ntruss.com'
uri = '/sms/v2/services/ncp:sms:kr:287156821959:sms_test/messages'

def make_signature():
    secret_key = "bZDIT4R4WKz1YsPK2pRfFjzY1ltrmz58vdNknz8G" 
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " " + uri + '\n' + timestamp + '\n' + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

# def sms_page():
    

# @router.post("/v1")
# def token(user_phone: str='', user_id: str=''):

#     # templates.TemplateResponse("sms_auth.html", {"request": 'tmp'})
#     # sms_page()
#     print('사용자 정보입니다:  ', user_phone, user_id)
#     print(make_signature())

#     header = {
#     "Content-Type" : "application/json; charset=utf-8",
#     "x-ncp-apigw-timestamp" : timestamp,
#     "x-ncp-iam-access-key" : access_key,
#     "x-ncp-apigw-signature-v2" : make_signature()
#     }

#     data = {
#         "type":"SMS",
#         "from":"01037038419",
#         "subject":"발신번호테스트",
#         "content":"[레디 모바일TMS] 인증번호 []를 입력해주세요.",
#         "messages":[
#             {
#             "to":"01036111322",
#             }
#         ]
#     }
#     res= requests.post(url=(url+uri),headers=header,data=json.dumps(data))
#     print(res.json())
#     print(res.text)
    
    


@router.post("/auth")
def auth(request: Request, msg: str = None):


    # 운영
    # url = 'https://api.bizppurio.com/v3/message'
    # 검수
    url = 'https://dev-api.bizppurio.com/v3/message'
    data = {
        'account': 'test', 'refkey': 'test1234', 'type': 'sms',
        'from': '01036111322', 'to': '01037038419', 'content': {
        'sms':{
        'message':'SMS 전송'
        } }
    }
    session = requests.Session()
    # 운영인 경우,verify 속성을 True로 변경 # session.verify = True
    session.verify = False
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
    'Authorization': 'Bearer ' + '{인증 토큰}'
    }
    response = session.post(url, data=json.dumps(data), headers=headers)

    print('Status code: ', response.status_code)
    print('Printing Entire Post Request')
    print(response.json())