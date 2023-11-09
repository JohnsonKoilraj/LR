from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.api.deps import get_db,get_current_user
from app.crud import crud_user 

from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *

router=APIRouter()
@router.post("/create_user")
async def create_user(
    *, db: Session = Depends(get_db), create_users: CreateUser,
    current_user=Depends(get_current_user)
):
    if current_user:
   
        data = jsonable_encoder(create_users)

        email = (data["email_id"]).strip()
        mobile_no = data["mobile_no"].strip()
        username = data["username"].strip()

        if username:
            existing_username = (
                db.query(User)
                .filter(User.username == username, User.status == 1)
                .first()
            )
            if existing_username:
                return {"status": 0, "msg": "Username Already Present."}

        if email:
            db_user = crud_user.check_email(email=email, db=db)
            if db_user:
                return {"status": 0, "msg": "Email Id Already Present."}

        if mobile_no:
            if crud_user.check_mobile(db=db, mobile=mobile_no):
                return {"status": 0, "msg": "Mobile_no Already Present."}

        user_create = crud_user.create(
            db, new_user=create_users
        )

        if user_create:
            return {"status": 1, "msg": "User Created Successfully"}

        else:
            return {"status": 0, "msg": "Something went worng!"}

    else:
        return {"status": 0, "msg": "Invalid access"}

