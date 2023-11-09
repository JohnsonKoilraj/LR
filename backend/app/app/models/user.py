from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True)
    user_type = Column(TINYINT, comment=" 1->Admin; 2->user")
    f_name = Column(String(50))
    l_name = Column(String(50))
    username = Column(String(150))
    password = Column(String(255))
    mobile_no = Column(String(20))
    email_id = Column(String(255))
    address = Column(String(5000))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))
    created_by = Column(Integer, comment="ForeignKey('user.id')")
    created_at = Column(DateTime)
    status = Column(TINYINT, comment="0->inactive,1->active,-1->deleted")
