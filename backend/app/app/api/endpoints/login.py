from fastapi import APIRouter, Depends, HTTPException, Form
from app.api import deps
from app.core import security
from app.core.config import settings
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import or_
from app.models import *
from app.schemas import ChangePassword
router = APIRouter()
    
@router.post("/login/access-token")
def login_access_token(
        db: Session = Depends(deps.get_db),
        *, username: str = Form(...,description="Mobile number",min_length=10),
        password: str = Form(...,description="Minimum 6 characters",
                             min_length=6)):
    
    user_name=username.strip()
    pwd=password.strip()
    user = deps.authenticate(db, username=user_name, password=pwd)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=[{"msg":"Invalid username or password"}])

    elif not deps.is_active(user):
       raise HTTPException(
            status_code=404,
            detail=[{"msg":"Inactive user"}])
    
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token=security.create_access_token(
            user.id, expires_delta=access_token_expires)


    if user:
        return {"access_token":token,
                "user_id":user.id,"user_name":user.username,
                "mobile_no":user.mobile_no if user.mobile_no else "",
                "msg":"Login Successfully!"}


@router.post("/change_password")
async def change_password(db:Session=Depends(deps.get_db),
                        current_user:User=Depends(deps.get_current_user),
                        *, user_in:ChangePassword):
    
    change_pswd = jsonable_encoder(user_in)
    
    if current_user:
        get_user=db.query(User).filter(User.id == current_user.id,
                                       User.status == 1).first()
        if get_user:
            change_pswd = jsonable_encoder(user_in)
            if change_pswd['current_password'] != None:
            
                if security.verify_password(change_pswd['current_password'], get_user.password):
                        get_user.password = get_password_hash(change_pswd['new_password'])
                        db.commit()
                else:
                    raise HTTPException(
                    status_code=400,
                    detail=[{"msg":"Current password is wrong"}],
                    )
            if change_pswd['new_password']:
                get_user.password = get_password_hash(change_pswd['new_password'])
                db.commit()
            else:
                raise HTTPException(
                status_code=400,
                detail=[{"msg":"Wrong current password"}],
                )
        else:
            raise HTTPException(
            status_code=400,
            detail=[{"msg":"User not found"}],
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=[{"msg":"Invalid request"}],
        )

    return JSONResponse(content="Password changed successfully")