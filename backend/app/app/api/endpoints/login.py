from fastapi import APIRouter, Depends, HTTPException, Form
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import or_

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


