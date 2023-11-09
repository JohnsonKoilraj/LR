from fastapi import APIRouter, Depends,Form,HTTPException
from app.api.deps import get_db,get_current_user
from datetime import datetime
from sqlalchemy import or_
from utils import pagination,paginate
from sqlalchemy.orm import Session
from app.models import *


router = APIRouter()
@router.post("/consignor_report")
async def consignor_details(
    *, db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
    page:int=1,
    size:int=10,
    insurance:str=Form(None,description="1-Owner's Risk,2-Carriers Risk"),
    insurer_name:str=Form(None),
    booking_type:int=Form(None,
            description="1-FullTruck Load,2-Part Load ,3-Miscellaneous"),
    from_time: datetime = Form(None),
    to_time: datetime = Form(None)
):
    if current_user:
        list_details=db.query(ConsignorCopy).filter(
            ConsignorCopy.status==1
        )

        if insurance:
            list_details = list_details.filter(
                ConsignorCopy.insurance==insurance
            )

        if insurer_name:
            list_details = list_details.filter(
                ConsignorCopy.insurer==insurer_name
            )

        if booking_type:
            list_details = list_details.filter(
                ConsignorCopy.booking_type==booking_type
            )

        if from_time and not to_time:
            list_details = list_details.filter(
                or_(
                    ConsignorCopy.from_date.between(from_time, datetime.now()),
                    ConsignorCopy.to_date.between(from_time, datetime.now()),
                )
            )
        if from_time and to_time:
            list_details = list_details.filter(
                or_(
                    ConsignorCopy.from_date.between(from_time, to_time),
                    ConsignorCopy.to_date.between(from_time, to_time),
                )
            )
        list_details=list_details.order_by(ConsignorCopy.id.desc())
        
        details_count=list_details.count()

        limit,offset=pagination(details_count,page,size)

        list_details=list_details.limit(limit).offset(offset).all()
        consignor_data=[]

        for row in list_details:
            consignor_data.append({"gst_no":row.gst_no,"cin":row.cin,
                            "insurance":row.insurance,
                            "insurer":row.insurer if row.insurer else "",
                            "policy_no":row.policy_no if row.policy_no else "",
                            "policy_dt":row.policy_dt if row.policy_dt else "",
                            "policy_rs":row.policy_rs if row.policy_rs else "",
                            "risk_rs":row.risk_rs if row.risk_rs else "",
                            "gc_no":row.gc_no if row.gc_no else "",
                            "date":row.date if row.date else "",
                            "vehicle_no":row.vehicle_no if row.vehicle_no else "",
                            "e_way_bill":row.e_way_bill if row.e_way_bill else "",
                            "from_date":row.from_date if row.from_date else "",
                            "to_date":row.to_date if row.to_date else "",
                            "delivery_instruction":row.delivery_instruction if row.delivery_instruction else "",
                            "booking_type":row.booking_type if row.booking_type else "",
                            "consignor_name":row.consignor_name if row.consignor_name else "",
                            "consignor_mobile_no":row.consignor_mobile_no if row.consignor_mobile_no else "",
                            "consignor_address":row.consignor_address if row.consignor_address else "",
                            "consignor_gst":row.consignor_gst if row.consignor_gst else "",
                            "consignee_name":row.consignee_name if row.consignee_name else "",
                            "consignee_mobile_no":row.consignee_mobile_no if row.consignee_mobile_no else "",
                            "consignee_address":row.consignee_address if row.consignee_address else "",
                            "consignee_gst":row.consignee_gst if row.consignee_gst else "",
                            "packages":row.packages if row.packages else "",
                            "description":row.description if row.description else "",
                            "actual_weight":row.actual_weight if row.actual_weight else "",
                            "chargeable_weight":row.chargeable_weight if row.chargeable_weight else "",
                            "rate_kg":row.rate_kg if row.rate_kg else "",
                            "basis_of_freight":row.basis_of_freight if row.basis_of_freight else "",
                            "rs":row.rs if row.rs else "",
                            "declared_value_goods":row.declared_value_goods if row.declared_value_goods else "",
                            "invoice_dc_no":row.invoice_dc_no if row.invoice_dc_no else "",
                            "invoice_dc_dt":row.invoice_dc_dt if row.invoice_dc_dt else "",
                            "receivers_name":row.receivers_name if row.receivers_name else "",
                            "date_of_receipt":row.date_of_receipt if row.date_of_receipt else "",
                            "created_at":row.created_at})

        return paginate(page, size, consignor_data, details_count)
    else:
        return {"status":"0","msg":"Not Authenticated"}

@router.get("/view_profile/{customer_id}")
async def view_profile(*,db:Session=Depends(get_db),
                       current_user=Depends(get_current_user), 
                       user_id:int):
    
    if current_user:
        check_customer=db.query(Customer).filter(
            Customer.id == user_id,Customer.status == 1).first()
        profile={}
        if check_customer:
            profile.update({"customer_name":check_customer.name
                                if check_customer.name else "",
                            "mobile_no":check_customer.mobile_no 
                            if check_customer.mobile_no else "",
                            "address":check_customer.address 
                            if check_customer.address else "",
                            "created_at":check_customer.created_at
                            })

            return profile
        else:
            raise HTTPException(
                status_code=400,
                detail=[{"msg":"Customer not found"}],)
    else:
        return {"status":"0","msg":"Not Authenticated"}

@router.post("/customer_list")
async def customer_list(
    *, db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
    page:int=1,
    size:int=10,
    from_time: datetime = Form(None),
    to_time: datetime = Form(None)
):
    if current_user:
        list_customer=db.query(Customer).filter(
            Customer.status==1
        )

        if from_time and not to_time:
            list_customer = list_customer.filter(
                or_(
                    Customer.created_at.between(from_time, datetime.now())
                )
            )

        if from_time and to_time:
            list_customer = list_customer.filter(
                Customer.created_at.between(from_time, to_time)
                )
            
        list_customer=list_customer.order_by(Customer.id.desc())
        
        customer_count=list_customer.count()

        limit,offset=pagination(customer_count,page,size)

        list_customer=list_customer.limit(limit).offset(offset).all()
        customer_data=[]

        for row in list_customer:
            customer_data.append({
                            "name":row.name,
                            "mobile_no":row.mobile_no if row.mobile_no else "",
                            "address":row.address if row.address else "",
                            "created_at":row.created_at})

        return paginate(page, size, customer_data, customer_count)
    
    else:
        return {"status":"0","msg":"Not Authenticated"}