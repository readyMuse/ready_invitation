from fastapi import APIRouter
from webapps.qr import route_qr # webapps.qr 디렉토리의 route_qr 파일 임포트
from webapps.users import route_users
from webapps.auth import route_login

api_router = APIRouter(include_in_schema=False)

api_router.include_router(route_qr.router, tags=["homepage"]) # router_qr.py 파일 내에 API router 설정되어 있는 내용들 
api_router.include_router(route_users.router, tags=["users"])
api_router.include_router(route_login.router, tags=["Auth"])
