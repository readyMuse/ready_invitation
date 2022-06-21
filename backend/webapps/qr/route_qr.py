from datetime import datetime, timedelta
import imp
from time import time
from fastapi import APIRouter, Depends
from fastapi import Request, status, responses, Response, requests
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from apis.version1.api_qr import create_qr ## qr 생성 api
from db.repository.guests import read_guest ## qr로 읽은 데이터 들고 게스트 정보 읽어오기.


templates = Jinja2Templates(directory="templates") # templates 디렉토리를 설정.
router = APIRouter()

access_time = datetime.now()


@router.get("/{id}")
def home(request: Request, db: Session = Depends(get_db), id : str=''):

    now_year = datetime.today().year
    years = [i for i in range(now_year-1, 1930, -1)]
    guest = read_guest(db=db, id=id)
    img_path = create_qr(guest, db=db) # qr생성 api 함수에 id 전달
    

    print('user 정보 요청 결과: ', guest)

    return templates.TemplateResponse(
        "index.html", {"request": request, 'img': img_path}
    )

    

