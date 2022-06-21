from ast import Str
from asyncore import write
from curses import reset_prog_mode
from datetime import datetime, timedelta
import imp
import json
from mmap import mmap
from ntpath import join
from pickle import PERSID
from tkinter import HIDDEN
from xmlrpc.server import SimpleXMLRPCRequestHandler
from fastapi.encoders import jsonable_encoder
from numpy import sort
from sqlalchemy import between, desc, not_
from sqlalchemy.sql.expression import func

from sqlalchemy.orm import Session
from db.models.guests import Awards
from dateutil.relativedelta import relativedelta


def read_guest(db: Session, id: str=''):
    
    
    guest = db.query(Awards.uid, Awards.user_nm.label('name') , Awards.company_nm.label('company'), Awards.job_gb.label('sector'), Awards.tel, Awards.enter_cnt, Awards.enter_time).filter(Awards.uid == id)
    
    try:
        guest = jsonable_encoder(guest[0])

    except:
        guest = '사전에 등록되지 않은 게스트입니다.'

    return guest
    

