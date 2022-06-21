from fastapi import APIRouter, Request, responses, status, Depends
from fastapi.templating import Jinja2Templates
from db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from webapps.users.forms import UserCreateForm


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("users/users_register.html", {"request": request})


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
   
    return templates.TemplateResponse("users/users_register.html", form.__dict__)
