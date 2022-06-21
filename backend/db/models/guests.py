from sqlalchemy import Column, Integer, String, TIMESTAMP
from db.base_class import Base


class Awards(Base):
    __tablename__ = "ready_awards"

    uid = Column(Integer, primary_key=True)
    user_nm = Column(String(20))
    company_nm = Column(String(20))
    dept_nm = Column(String(20))
    tel = Column(String(20))
    job_gb = Column(String(20))
    enter_time = Column(TIMESTAMP)
    enter_cnt = Column(Integer)
    manager = Column(String(20))
    car = Column(String(20))
    

