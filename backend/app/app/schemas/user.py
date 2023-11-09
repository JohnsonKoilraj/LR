from pydantic import BaseModel, Field, validator
from typing import Optional
from fastapi import HTTPException

class CreateUser(BaseModel):
    f_name: Optional[str] = ""
    l_name: Optional[str] = ""
    username: str
    mobile_no: str
    email_id: Optional[str] = ""
    address: Optional[str] = ""
    password:str

class ChangePassword(BaseModel):
    current_password: Optional[str]
    new_password:str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise HTTPException(
                status_code=400,
                detail=[{"msg":"Password don't match"}],
            )   
       
        return v

    @validator('new_password')
    def new_password_validate(cls, v, values, **kwargs):
        if 'current_password' in values and v == values['current_password']:
            raise HTTPException(
                status_code=400,
                detail=[{"msg":"Current password and new password cannot be same"}],
            ) 
  
        if not len(v) >= 6:
            raise HTTPException(
                status_code=400,
                detail=[{"msg":"Password must has at least 6 characters"}],
            )    
            
        return v