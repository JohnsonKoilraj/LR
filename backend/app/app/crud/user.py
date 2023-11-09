from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import user
from app.schemas.user import CreateUser
from datetime import datetime
from app.core.security import get_password_hash
from fastapi.encoders import jsonable_encoder
from app.core.config import settings
import random


class CRUDUser(CRUDBase[User, CreateUser]):
    # def get_by_contact_number(self,db:Session,contact_number:int):

    #     return db.query(User).filter(User.mobile_no==contact_number,User.status!=1).first()

    # def get_user_by_email(self,username:str,db:Session):

    #     return db.query(User).filter(User.mobile_no==username).first()

    def check_email(self, email: str, db: Session):
        return db.query(User).filter(User.email_id == email, User.status == 1).first()

    def check_mobile(self, db: Session, mobile: str):
        return db.query(User).filter(User.mobile_no == mobile, User.status == 1).first()

    def create(
        self,
        db: Session,
        *,
        new_user:user.CreateUser,
        
    ):
        obj_in_data = jsonable_encoder(new_user)
        pwd = obj_in_data.pop("password")
        db_obj = self.model(
            **obj_in_data,
            status=1,
            created_at=datetime.now(settings.tz_NY),
            password=get_password_hash(pwd),
            user_type=1
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_user = CRUDUser(User)