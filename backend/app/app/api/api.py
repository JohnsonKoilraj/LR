from fastapi import APIRouter
from .endpoints import consignor_details,consignor_copy_pdf,report,user,login

api_router = APIRouter()

api_router.include_router(consignor_details.router, tags=["consigner_details"])
api_router.include_router(consignor_copy_pdf.router, tags=["consigner_copy_pdf"])
api_router.include_router(report.router, tags=["report"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(login.router,tags=["login"])

