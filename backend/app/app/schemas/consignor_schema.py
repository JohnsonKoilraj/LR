from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Consignor(BaseModel):
    name:str
    mobile_no:str
    address:str
    consignor_gst:str

class Consignee(BaseModel):
    name:str
    mobile_no:str
    address:str
    consignee_gst:str

class PolicyDetails(BaseModel):
    insurance:int
    insurer:str
    policy_no:str
    policy_dt:str
    policy_rs:str
    risk_rs:str

class DeliveryDetails(BaseModel):
    gst_no:str
    cin:str
    gc_no:str
    # date:str
    vehicle_no:str
    e_way_bill:str
    from_date:str
    to_date:str
    delivery_instruction:str
    booking_type:int

class ConsignorDetails(BaseModel):
    policy_details:list[PolicyDetails]
    delivery_details:list[DeliveryDetails]

    consignor:list[Consignor]
    consignee:list[Consignee]

    packages:str
    description:str
    actual_weight:str
    chargeable_weight:str
    rate_kg:str
    basis_of_freight:int
    rs:str
    declared_value_goods:str
    invoice_dc_no:str
    invoice_dc_dt:str
    receivers_name:str
    date_of_receipt:str
    


