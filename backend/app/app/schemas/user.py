from pydantic import BaseModel, Field, validator
from typing import Optional

class CreateUser(BaseModel):
    f_name: Optional[str] = ""
    l_name: Optional[str] = ""
    username: str
    mobile_no: str
    email_id: Optional[str] = ""
    address: Optional[str] = ""
    password:str