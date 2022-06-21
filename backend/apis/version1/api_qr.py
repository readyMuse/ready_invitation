from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db

import qrcode

router = APIRouter()


@router.post("/id")
def create_qr(guest: None, db: Session = Depends(get_db)):


   # id에 따른 DB에서 정보 조회
   img = qrcode.make(guest)
   img.save('./static/assets/img/user_qr/{0}.png'.format(guest['uid']))
   
   return './static/assets/img/user_qr/{0}.png'.format(guest['uid'])