from typing import Any, Dict, List, Optional, TypeVar, Generic

from pydantic import AnyHttpUrl, BaseSettings, validator
from fastapi import Query
from fastapi_pagination.default import Page as BasePage, Params as BaseParams
import pytz 

T = TypeVar("T")

class Params(BaseParams):
    size: int = Query(500, gt=0, le=1000, description="Page size")

class Page(BasePage[T], Generic[T]):
    __params_type__ = Params


# base_domain = "http://192.168.1.106"
# base_url =""
# device_base_url = "http://cbe.themaestro.in:8024/device_api"
# base_dir="/upload_files"
# base_domain_url = ""
base_url_segment = ""
base_upload_folder = "/var/www/html"

#Test
fusion_baseurl = "https://fa-eubd-test-saasfaprod1.fa.ocs.oraclecloud.com:443"

data_base = "mysql+pymysql://root:W3solutions@localhost/lr"

# data_base = "mysql+pymysql://local_admin:12345@localhost/lcc_demo_3"

api_doc_path = "/docs"
token_ = "AFHDEesdjr788r499"

class Settings(BaseSettings):
    API_V1_STR: str = base_url_segment
    # BASE_UPLOAD_FOLDER: str = base_upload_folder
    # DEVICE_BASE_URL: str = device_base_url
    # BASEURL:str=base_url
    # BASE_DIR=base_dir
    TOKEN = token_
    # SALT_KEY:str="RKv9r34e9345nj3c54h4545"
    SALT_KEY:str="L4jklcv@1qaz!mn71iwe"

    FUSION_URL:str=fusion_baseurl
    SECRET_KEY:str=""
    DATA_BASE:str = data_base
    # BASE_DOMAIN:str = base_domain
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BASE_DOMAIN_URL:str = base_domain_url
    API_DOC_PATH:str = api_doc_path
    otp_resend_remaining_sec:int = 120
    tz_NY = pytz.timezone('Asia/Kolkata')  
    # ApiKey="fa526904-5c64-4efc-b6b5-eeb40cbedc0e"
    # ClientId="1ade59f7-1b0c-4287-b170-bb9c94d3c142"
    # SenderId="TKTMJL"   
    tz_IN = pytz.timezone('Asia/Kolkata')  



    SERVER_NAME:str = "LR"
    ROOT_SERVER_BASE_URL:str =""
    SERVER_HOST:AnyHttpUrl="http://localhost:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000",  "http://localhost:8080", "http://localhost:3000",
                                              "http://localhost:3001", "http://localhost:3002", "https://cbe.themaestro.in", "http://cbe.themaestro.in",
                                              ]       
    
    PROJECT_NAME:str = "LR"

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return data_base

settings = Settings()    
