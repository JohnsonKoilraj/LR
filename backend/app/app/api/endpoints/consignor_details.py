from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.schemas import ConsignorDetails
from app.api.deps import get_db,get_current_user
from datetime import datetime
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models import *


router = APIRouter()

@router.post("/create_consignor_copy")
async def create_consignor_copy(
    *, db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user),
    create_consignor_copy: ConsignorDetails
):
    data=jsonable_encoder(create_consignor_copy)

    if current_user.user_type==1:  
        create_consignor_copy=ConsignorCopy(
            gst_no=data["gst_no"],
            cin_no=data["cin"],
            insurance=data["policy_details"][0]["insurance"],
            insurer=data["policy_details"][0]["insurer"],
            policy_no=data["policy_details"][0]["policy_no"],
            policy_dt=data["policy_details"][0]["policy_dt"],
            policy_rs=data["policy_details"][0]["policy_rs"],
            risk_rs=data["policy_details"][0]["risk_rs"],
            gc_no=data["delivery_details"][0]["gc_no"],
            date=datetime.now(settings.tz_NY),
            vehicle_no=data["delivery_details"][0]["vehicle_no"],
            e_way_bill=data["delivery_details"][0]["e_way_bill"],
            from_date=data["delivery_details"][0]["from_date"],
            to_date=data["delivery_details"][0]["to_date"],
            delivery_instruction=data["delivery_details"][0]["delivery_instruction"],
            booking_type=data["delivery_details"][0]["booking_type"],
            consignor_name= data["consignor"][0]["name"],
            consignor_mobile_no= data["consignor"][0]["mobile_no"],
            consignor_address= data["consignor"][0]["address"],
            consignor_gst=data["consignor"][0]["consignor_gst"],
            consignee_name= data["consignee"][0]["name"],
            consignee_mobile_no= data["consignee"][0]["mobile_no"],
            consignee_address= data["consignee"][0]["address"],
            consignee_gst=data["consignee"][0]["consignee_gst"],
            packages=data["packages"],
            description=data["description"],
            actual_weight=data["actual_weight"],
            chargeable_weight=data["chargeable_weight"],
            rate_kg=data["rate_kg"],
            basis_of_freight=data["basis_of_freight"],
            rs=data["rs"],
            declared_value_goods=data["declared_value_goods"],
            invoice_dc_no=data["invoice_dc_no"],
            invoice_dc_dt=data["invoice_dc_dt"],
            receivers_name=data["receivers_name"],
            date_of_receipt=data["date_of_receipt"],
            status=1,
            created_at=datetime.now(settings.tz_NY)

        )
        db.add(create_consignor_copy)
        db.commit()

        check_customer=db.query(Customer).filter(
            Customer.mobile_no==data["consignee"][0]["mobile_no"],
            Customer.status==1).first()
            
        if not check_customer:
            create_customer=Customer(
                name=data["consignee"][0]["name"],
                mobile_no=data["consignee"][0]["mobile_no"],
                address=data["consignee"][0]["address"],
                status=1,
                created_at=datetime.now(settings.tz_NY)
            )

            db.add(create_customer)
            db.commit()

        return {"status":"1","msg":"Successfully Created"}
    else:
        return "error"