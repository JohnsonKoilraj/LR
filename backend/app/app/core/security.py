from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def get_password_hash(password: str):
    result = hashlib.sha1(password.encode())
    return result.hexdigest()


def create_access_token(subject: Union[str, Any], 
                        expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, password: str):
    result = hashlib.sha1(plain_password.encode())
    if password == result.hexdigest():
        return True
    else:
        return None
