from typing import Generator
from jose import jwt
from app.schemas import TokenPayload
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import *
from typing import Generator, Any, Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core import security
from sqlalchemy import or_
from pydantic import ValidationError




def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_by_user(db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.mobile_no != None,
                                      User.mobile_no == username,
                                      User.status != -1).first()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg":"Could not validate credentials"}],
        )
    user = get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail=[{"msg":"User not found"}])
    return user

def get(db: Session, id: Any) -> Optional[User]:
    user = db.query(User).filter(User.id == id,User.status != -1).first()
    return user

def authenticate(
    db: Session, *, username: str, password: str
) -> Optional[User]:
    user = get_by_user(db, username=username)
    if not user or user.password == None:
        return None
    
    if not security.verify_password(password, user.password):
        return None
    return user


def is_active(user: User):
    if user.status == 1:
        return user.status
    else:
        return None





