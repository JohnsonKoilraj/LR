from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__="customer"
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    mobile_no=Column(String(50))
    address=Column(String(250))
    status= Column(TINYINT, comment="1-active,2-inactive")
    created_at = Column(DateTime)

class ConsignorCopy(Base):
    __tablename__ = "consignor_copy"
    id = Column(Integer, primary_key=True)
    gst_no=Column(String(20))
    cin=Column(String(50))
    insurance = Column(TINYINT, comment="1-Owner's Risk,2-Carrier's Risk")
    insurer = Column(String(50))
    policy_no = Column(String(50))
    policy_dt = Column(String(50))
    policy_rs = Column(String(50))
    risk_rs = Column(String(50))
    gc_no = Column(String(50))
    date = Column(DateTime)
    vehicle_no = Column(String(50))
    e_way_bill = Column(String(50))
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    delivery_instruction = Column(String(250))
    booking_type = Column(TINYINT, comment="1-Full Truck Load,2-Part Load,3-Miscellaneous")
    consignor_name = Column(String(50))
    consignor_mobile_no = Column(String(50))
    consignor_address = Column(String(250))
    consignor_gst = Column(String(50))
    consignee_name = Column(String(50))
    consignee_mobile_no = Column(String(50))
    consignee_address = Column(String(250))
    consignee_gst = Column(String(50))
    packages = Column(String(50))
    description = Column(String(50))
    actual_weight = Column(String(50))
    chargeable_weight = Column(String(50))
    rate_kg = Column(String(50))
    basis_of_freight = Column(TINYINT, comment="1-paid,2-to be filled,3-to pay")
    rs = Column(String(50))
    declared_value_goods = Column(String(50))
    invoice_dc_no = Column(String(50))
    invoice_dc_dt = Column(String(50))
    receivers_name = Column(String(50))
    date_of_receipt = Column(DateTime)
    status = Column(TINYINT, comment="1-active,2-inactive")
    created_at = Column(DateTime)


