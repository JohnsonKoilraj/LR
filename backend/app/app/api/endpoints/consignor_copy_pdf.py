from fastapi import APIRouter, Depends,Form
from app.api.deps import get_db,get_current_user
from fastapi.responses import FileResponse
from fpdf import FPDF
from sqlalchemy.orm import Session
from app.models import *
from datetime import datetime
from app.core.config import settings

class Consignor_pdf(FPDF):
    def header(self):
        self.set_font('helvetica','B',13)
    
    def footer(self):
        pass
router = APIRouter()

@router.post("/create_consignor_copy_pdf")
async def create_consignor_copy_pdf(
    *, db: Session = Depends(get_db),
    current_user:User=Depends(get_current_user),
    gc_no:str=Form(...)
):
    if current_user.user_type==1:
        pdf=Consignor_pdf('L','mm','Letter')

        data=db.query(ConsignorCopy).filter(
            ConsignorCopy.gc_no==gc_no,
            ConsignorCopy.status==1
        ).first()
            
        if data:
            pdf.add_page() 
            
            pdf.set_draw_color(0,0,0)
            pdf.set_line_width(1)
            pdf.rect(5, 5, 270, 205)
            #1 -vertical
            pdf.set_line_width(1)
            pdf.line(88,5,88,78)
        
            pdf.set_line_width(1)
            # 2-vertical
            pdf.line(130,38,130,140)
            # 3-vertical

            pdf.line(210,38,210,118)

            pdf.line(88,22,275,22) 
            
            pdf.line(5,30,275,30) 
            pdf.set_xy(100,21)
            pdf.cell(80,10, "(unit of)", align='C')

            pdf.line(5,38,275,38) 
            pdf.set_xy(7,29)
            pdf.cell(40,10, "Gst No:")

            pdf.set_xy(25,29)
            pdf.cell(40,10,data.gst_no,align="C")

            pdf.set_xy(100,29)
            pdf.cell(80,10, "(unit of)", align='C')
            pdf.line(5,46,275,46) 

            pdf.set_xy(14,38)
            pdf.cell(40,10, "CIN:")

            pdf.set_xy(25,38)
            pdf.cell(40,10, data.cin,align="C")

            pdf.set_fill_color(255, 255, 0)
            pdf.set_xy(5.5,46.5)
            
            pdf.cell(82 ,13, "Consignor copy",fill=1, align='C')
            pdf.line(5,60,88,60)

            pdf.set_fill_color(200,200,200) 

            pdf.set_xy(5.5,60.5)
            pdf.cell(82,9, "Insurance", align='C',fill=1)
            pdf.line(210,58,275,58)

            pdf.set_xy(88.5,46.5)
            pdf.cell(41,16, "GC No.(LR#)",fill=1, align='C')
            pdf.set_xy(88.5,57.5)
            pdf.cell(41,12.5, "(Non Negotiable)",fill=1, align='C')

            pdf.set_xy(135,54)
            pdf.cell(60,10, data.gc_no, align='C')

            pdf.set_xy(210.5,46.5)
            pdf.cell(64,11, "Date", fill=1,align='C')
            pdf.line(5,70,275,70)
            pdf.set_xy(215,60)
            pdf.cell(60,10,str(
                datetime.now(settings.tz_IN).strftime("%Y-%m-%d %H:%M:%S")))
            
            pdf.set_xy(28,69)
            if data.insurance==1:
                pdf.cell(80,10, "Owner's Risk")
            elif data.insurance==2:
                pdf.cell(80,10, "Carrier's Risk")
            #vertical
            # pdf.line(52,70,52,78)
            # pdf.set_xy(52,69)
            # pdf.cell(1,10, "Carrier's Risk")

            pdf.set_xy(88.5,70.5)
            pdf.cell(41,7, "Vehicle No :",fill=1,align="C")
            pdf.set_xy(134,69)
            pdf.cell(15,10, data.vehicle_no)

            #vertical
            pdf.line(179,71,179,86)
            pdf.set_xy(179.5,70.5)
            pdf.cell(30,7, "E-Way Bill :",fill=1)
            pdf.set_xy(212,69.5)
            pdf.cell(40,10,data.e_way_bill)
            pdf.line(5,78,275,78)

            #vertical
            pdf.line(35,78,35,118)
            pdf.set_xy(179.5,78.5)
            pdf.cell(30,8, "To :",fill=1)
            pdf.set_xy(215,76.5)
            pdf.cell(40,10,str(data.to_date))
            
            pdf.set_xy(5.5,78.5)
            pdf.cell(29,7, "Insurer :",fill=1,align="C")
            pdf.set_xy(37,77)
            pdf.cell(40,10, data.insurer,align="C")
            pdf.line(5,86,275,86)

            #vertical
            pdf.line(93,78,93,118)
            pdf.set_xy(93.5,78.5)
            pdf.cell(36,7, "From :",fill=1,align="C")
            pdf.set_xy(134,77)
            pdf.cell(40,10,str(data.from_date))

            pdf.set_xy(5.5,86.5)
            pdf.cell(29,7, "Policy No :",fill=1,align="C")
            pdf.set_xy(37,85)
            pdf.cell(40,10, data.policy_no,align="C")
            pdf.line(5,94,93,94)

            pdf.set_xy(5.5,94.5)
            pdf.cell(29,7, "Policy dt :",fill=1,align="C")
            pdf.set_xy(37,93)
            pdf.cell(40,10,data.policy_dt,align="C")
            pdf.line(5,102,93,102)

            pdf.set_xy(5.5,102.5)
            pdf.cell(29,7, "Policy, Rs :",fill=1,align="C")
            pdf.set_xy(37,101)
            pdf.cell(40,10, data.policy_rs,align="C")
            pdf.line(5,110,93,110)

            pdf.set_xy(5.5,110.5)
            pdf.cell(29,7, "Risk,Rs :",fill=1,align="C")
            pdf.set_xy(37,109)
            pdf.cell(40,10,data.risk_rs,align="C")
            pdf.line(5,118,275,118)

            pdf.set_xy(93.5,86.5)
            pdf.cell(36,16, "Delivery",fill=1,align="C")
            pdf.set_xy(93.5,102.5)
            pdf.cell(36,15, "  Instruction(s)",fill=1)
            pdf.set_xy(134,92)
            pdf.cell(40,10,data.delivery_instruction)

        #booking type
            pdf.set_xy(210.5,86.5)
            pdf.cell(64,7, "Booking Type",fill=1,align="C")
            pdf.line(210,94,275,94)

            pdf.set_xy(224,101)
            if data.booking_type==1:
                pdf.cell(40,10, "Full Truck Load",align="c")
            elif data.booking_type==2:
                pdf.cell(40,10, "Part Load",align="C")
            elif data.booking_type==3:
                pdf.cell(40,10, "Miscellaneous",align="C")

        #consignor and consignee

            pdf.set_xy(5.5,118.5)
            pdf.cell(49,6, "Consignor's",fill=1,align="C")
            pdf.set_xy(5.5,124)
            pdf.cell(49,8, "Name & address",fill=1,align="C")

            pdf.set_xy(55,118)
            pdf.cell(40,10,data.consignor_name)
            pdf.set_xy(95,118)
            pdf.cell(40,10,data.consignor_mobile_no)
            pdf.set_xy(55,124)
            pdf.cell(40,10,data.consignor_address)

            pdf.line(5,132,275,132)
            pdf.set_xy(5.5,132.5)
            pdf.cell(48,8, "GST No :",fill=1,align="C")
            pdf.set_xy(48,132)
            pdf.cell(40,8, data.consignor_gst,align="C")
            pdf.line(5,140,275,140)

            #vertical
            pdf.line(54,118,54,210)

            pdf.set_xy(130.5,118.5)
            pdf.cell(42,6, "Consignee's",fill=1,align="C")
            pdf.set_xy(130.5,124)
            pdf.cell(42,8, "Name & address",fill=1,align="C")

            pdf.set_xy(175,118)
            pdf.cell(40,10,data.consignee_name)
            pdf.set_xy(215,118)
            pdf.cell(40,10,data.consignee_mobile_no)
            pdf.set_xy(175,124)
            pdf.cell(40,10,data.consignee_address)

            pdf.line(5,132,275,132)
            pdf.set_xy(130.5,132.5)
            pdf.cell(42,7, "GST No :",fill=1,align="C")
            pdf.set_xy(175,132)
            pdf.cell(40,8, data.consignee_gst,align="C")

            #vertical
            pdf.line(173,118,173,140)

        #delivery details
            pdf.set_xy(5.5,140.5)
            pdf.cell(48,8, "Packages",fill=1,align="C")

            pdf.set_xy(5.5,149)
            pdf.cell(40,8, data.packages,align="C")
            pdf.line(5,148,275,148)
            
            pdf.line(5,156,275,156)
        
        #packages value box

            pdf.set_xy(54.5,140.5)
            pdf.cell(40,7 , "Actual Weight",align="C",fill=1)
            pdf.set_xy(54,149)
            pdf.cell(40,8, data.actual_weight,align="C")

            #vertical
            pdf.line(95,140,95,156)

            pdf.set_xy(95.5,140.5)
            pdf.cell(45,7, "Chargeable Weight",fill=1,align="C")
            pdf.set_xy(95,149)
            pdf.cell(45,8,data.chargeable_weight,align="C")

            #vertical
            pdf.line(140,140,140,156)

            pdf.set_xy(140.5,140.5)
            pdf.cell(38,7, "Rate/Kg:",fill=1,align="C")
            pdf.set_xy(140.5,149)
            pdf.cell(40,8,data.rate_kg,align="C")

            pdf.set_xy(178.5,140.5)
            pdf.cell(60,7, "Basis of freight",align="C",fill=1)

            pdf.set_xy(178.5,149)
            if data.basis_of_freight==1:
                pdf.cell(60,8, "Paid",align="C")
            elif data.basis_of_freight==2:
                pdf.cell(60,8, "To be Billed",align="C")
            elif data.basis_of_freight==3:
                pdf.cell(60,8, "To Pay",align="C")
    
            #vertical
            pdf.line(239,140,239,156)

            pdf.set_xy(239.5,140.5)
            pdf.cell(35,7, "Rs",align="C",fill=1)

            pdf.set_xy(239.5,149) 
            pdf.cell(35,8, data.rs,align="C")

            #vertical

            pdf.line(178,140,178,210)

            pdf.set_xy(5.5,156.5)
            pdf.cell(48,8, "Description ",fill=1,align="C")
            pdf.set_xy(5.5,164)
            pdf.cell(48,12,"(Said to Contain)",fill=1,align="C")
            pdf.set_xy(55,157)
            pdf.cell(130,8, data.description,align="C")

            pdf.set_xy(178.5,156.5)
            pdf.cell(96,7, "for",align="C",fill=1)
            pdf.line(178,163,275,163)

            pdf.line(5,175,275,175)
            
            pdf.set_xy(5.5,176)
            pdf.cell(48,5, "Declared Value ",fill=1,align="C")        
            pdf.set_xy(5.5,181)
            pdf.cell(48,5, "of goods,Rs",fill=1,align="C")
            pdf.set_xy(5.5,186.5)
            pdf.cell(48,3,data.declared_value_goods,align="C")

            pdf.set_xy(54.5,175.5)
            pdf.cell(40,10, "Invoice/DC No",fill=1,align="C")
            pdf.set_xy(54.5,186.5)
            pdf.cell(40,3, data.invoice_dc_no,align="C")

            #vertical
            pdf.line(95,175,95,210)

            pdf.set_xy(95.5,175.5)
            pdf.cell(45,10, "Invoice/DC No",fill=1,align="C")
            pdf.set_xy(95.5,186.5)
            pdf.cell(45,3, data.invoice_dc_no,align="C")
          
            #vertical
            pdf.line(140,175,140,210)

            pdf.set_xy(140.5,175.5)
            pdf.cell(37,10, "Date of Receipt",fill=1,align="C")

            pdf.set_xy(140.5,186.5)
            pdf.cell(37,3, str(data.date_of_receipt.strftime("%Y-%m-%d")),align="C")

            #vertical
            pdf.line(140,140,140,156)

            pdf.set_xy(178.5,175.5)
            pdf.cell(96,10, "Receiver's Name/Stamp & Signature",align="C",fill=1)

            pdf.set_xy(178.5,186.5)
            pdf.cell(96,3, data.receivers_name,align="C")

            pdf.line(5,185.5,275,185.5)
            pdf.line(5,191,178,191)
            pdf.set_xy(5.5,192.5)
            pdf.cell(40,3, data.receivers_name,align="C")

            #Second page

            pdf.add_page()
            pdf.rect(5, 5, 270, 205)

            pdf.set_xy(124,7)
            pdf.cell(24,6, "Terms and Conditions",align="C")

            pdf.set_xy(8,30)
            pdf.cell(70,4, "1. The subject consignment has been accepted for transportation at OWNER'S RISK only.")

            pdf.set_xy(8,35)
            pdf.cell(180,4,"2. The Company here by declares that contents, nature,quality conditions and value of the subject GCN are unknown to ")
            
            pdf.set_xy(13,40)
            pdf.cell(160,4,"them and that they have accepted the same in good faith for transportion.")

            pdf.set_xy(8,45)
            pdf.cell(70,4,"3. The Consignment is accepted on 'Said to Contain' basis.".encode('UTF-8').decode('latin-1'))
            
            pdf.set_xy(8,50)
            pdf.cell(180,4,"4. The Consignor is responsible to provide appropriate documents and permits as per the prevailing laws for the ")
            pdf.set_xy(13,55)
            pdf.cell(180,4,"transportation of the goods, as applicable. The Company shall not be responsible or liable to the Consignor and ")
            pdf.set_xy(13,60)
            pdf.cell(180,4,"Consignee for any loss damage,short delivery or non-delivery of the subject consignment, attributable to or caused by")
            pdf.set_xy(13,65)
            pdf.cell(180,4," any incorrect or false declaration. ")
        
            pdf.set_xy(8,70)
            pdf.cell(180,4,"5. The Consignor hereby declares that the subject consignment does not contain any contraband or prohibited goods")
            pdf.set_xy(13,75)
            pdf.cell(180,4,"and that the consignment has been correctly valued, properly packed, marked and addressed to ensure for onward")
            pdf.set_xy(13,80)
            pdf.cell(180,4,"transportation and delivery.")

            pdf.set_xy(8,85)
            pdf.cell(180,4,"6. The company shall not be liable or responsible for any loss [direct or consequential irrespective of amount")
            pdf.set_xy(13,90)
            pdf.cell(180,4,"involved] alleged to have been sustained by the Consignor / Consignee occurred by delay in the pickup/delivery of the")
            pdf.set_xy(13,95)
            pdf.cell(180,4,"subject consignment. Company shall not be responsible for delay/ damage to the goods of the subject GCN due to.")
        
            pdf.set_xy(13,100)
            pdf.cell(180,4,"a) Act of God, Acts of enemies of the states, Force majeure, natural calamities, road conditions, weather or conditions")
            pdf.set_xy(13,105)
            pdf.cell(180,4,"of nature causing accidents to the carrying vehicle or by action of terrorists, militants or activists or person acting")
            pdf.set_xy(13,110)
            pdf.cell(180,4,"from a political motive cr caused by resulting from strike, lockout, labour disturbances, rit or civil commotions etc.")
            pdf.set_xy(13,115)
            pdf.cell(180,4,"b) Any act, default, omission on the part of the Consignor / Consignee or any other interested third party whomever")
            pdf.set_xy(13,120)
            pdf.cell(180,4," arising.")
            pdf.set_xy(13,125)
            pdf.cell(180,4,"c) Inherent nature or any special characteristic or combustion nature of the subject consignment.")
        
            pdf.set_xy(8,130)
            pdf.cell(180,4,"7. liability of the Company is restricted to Rs.5000/ or the total freight amount paid, whichever is lower, irrespective of the")
            pdf.set_xy(13,135)
            pdf.cell(180,4,"declared value of the Consignments.")

            pdf.set_xy(8,140)
            pdf.cell(180,4,"8. CLAIM FOR LOSS, DAMAGE, and SHORTAGE TO THE SUBJECT CONSIGNMENT: Any loss or damage to the goods ")
            pdf.set_xy(13,145)
            pdf.cell(180,4,"shall be intimated to the Company immediately upon delivery of the goods. Claim for loss as above must be lodged ")
            pdf.set_xy(13,150)
            pdf.cell(180,4,"by the Consignor/ Consignee delivered in writing to the Company within 3 (three) working days from the delivery of ")
            pdf.set_xy(13,155)
            pdf.cell(180,4,"consignment. Any claim against the Company by the Consignor/Consignee after the expiry of 3(three) working days")
            pdf.set_xy(13,160)
            pdf.cell(180,4,"from the consignment shall not be entertained.")
        
            pdf.set_xy(8,165)
            pdf.cell(180,4,"9. Courtin the city of Bangalore alone shall have Jurisdiction in respect of all claims, disputes or matters ")
            pdf.set_xy(13,170)
            pdf.cell(180,4,"pertaining to the subject GCN.")
            pdf.set_xy(7,175)
            pdf.cell(180,4,"10. The decision of Company on the subject consignment is final and binding on the Consignor/Consignee.")
            pdf.set_xy(7,180)
            pdf.cell(180,4,"11. The Consignor/ authorised representative has read and accepted the Terms and Conditions mentioned herein above.")
        
            pdf.set_xy(190,186)
            pdf.cell(80,1,"......................................................")
            pdf.set_xy(190,190)
            pdf.cell(80,4,"Signature / Stamp of Consignor")
        
            pdf.output('qr.pdf')

            return FileResponse('qr.pdf', headers = {
            "Content-Disposition": f"attachment; filename=consignor_copy.png"
            })
        
        else:
            return {
                "status":"0",
                "msg":"Invalid gc no"
            }
    else:
        return {
        "status":"0",
        "msg":"Invalid user"
        }
