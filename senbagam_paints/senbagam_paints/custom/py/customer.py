import frappe
import random
import json
import random as r
import random as re
from frappe.utils import cint, get_link_to_form
from frappe import _
import requests
from frappe.utils import comma_and,	get_link_to_form

def user_creation(self,event):
   
    user = frappe.new_doc("User")
    if self.mobile_no1:
        random_number = random.randint(1000, 9999)
        customer_id = self.customer_name + str(random_number)
        b=re.sub(r"\s+", "", customer_id).lower()
        e=b+"@sps.com"
        user.email = e

        user.first_name =self.customer_name
        user.send_welcome_email = 0
        user.user_type = 'System User'
        user.mobile_no =self.mobile_no1
        user.role_profile_name="App User"
        user.save(ignore_permissions=True)
        contact = frappe.new_doc("Contact")
        contact.first_name=self.customer_name
        contact.email_id=e
        contact.user=e
        
        contact.mobile_no=self.mobile_no1
        # contact.append('email_ids',{
        # "email_id":e,
        # "is_primary":1
        # })
        contact.append('phone_nos',{
        "phone":self.mobile_no1,
        "is_primary_mobile_no":1

        })
        contact.append('links',{
        "link_doctype": "Customer",
        "link_name": self.name

        })
        contact.save(ignore_permissions = True)
        self.user=user.name
        self.customer_primary_contact=contact.name
        self.save()
        # # user.new_password = args["password"]
        # user.save(ignore_permissions = True)


    if self.refered_by:
        if not frappe.db.exists("Referral Tree",self.name):
    
            if frappe.db.exists("Referral Tree",self.refered_by):
                doc=frappe.new_doc("Referral Tree")
                doc.customer=self.name
                doc.parent_referral_tree=self.refered_by
                doc.is_group=1
                doc.save(ignore_permissions = True)
            else:
                doc=frappe.new_doc("Referral Tree")
                doc.customer=self.name
                doc.parent_referral_tree="Senbagam Paints"
                doc.is_group=1
                doc.save(ignore_permissions = True)

# @frappe.whitelist()
# def sendotp(otp, mobile_no) :
#     mobile_no=mobile_no
#     otp=otp
# 	token=get_decrypted_password("Api Credentials","Api Credentials","authorization",False)
# 	conn = http.client.HTTPSConnection("gsp.adaequare.com")
# 	payload = ''
# 	token="bearer"+""+token
# 	try:
# 		headers = {
# 		'Content-Type': 'application/json',
# 		'Authorization':f"{token}",
# 		}
# 		conn.request("GET", f"/gsp/others/distance?from={from_pin}&to={to_pin}", payload, headers)
# 		res = conn.getresponse()
# 		data = res.read()
		
# 		result=data.decode("utf-8")
# 		if(frappe.parse_json(result).get('error')):
# 			error = f"Distance Calculation API Failed\n" + result
# 			frappe.log_error(error,"Distance Calculation Api")
# 		return result
# 	except Exception as e:
# 		error = f"Distance Calculation Error" + str(e)
# 		frappe.log_error(error,"Distance Calculation Api")
#     var response = await http.get(
#         Uri.parse(
#             'https://api.msg91.com/api/v5/otp?template_id=63b57319d6fc0504dd28d3c2&mobile=${final_mobile}&authkey=387408ATKT6CcDJGRW63aa76cbP1&otp=${otp}&VAR1=CUSTOMER'),
#         headers: {"Cookie": "PHPSESSID=407l8l1q6v3v69d02b8p9kej50"})

    


@frappe.whitelist()
def otpgen(mobileno,customer=None):   
    otp=""
    for i in range(4):
       otp+=str(r.randint(1,9))
    if customer:
        frappe.db.set_value('Customer', customer, 'original_otp', otp, update_modified=False)
    if mobileno:
        otp_value = frappe.get_doc("OTP Settings")
        url = f"{otp_value.sms_gateway_url}template_id={otp_value.template_id}&mobile=91{mobileno}&authkey={otp_value.authkey}&otp={otp}"

        payload = {}
        headers = {
        'Cookie': f'{otp_value.cookie}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)

    return otp,response
    
def change_workflow(doc, event=None):
    if doc.workflow_state != 'Disabled':
        doc.custom_previous_workflow = doc.workflow_state

    if doc.disabled:
        doc._doc_before_save.workflow_state = 'Disabled'
        doc.db_set("workflow_state", 'Disabled')
    elif doc.workflow_state == 'Disabled':
        doc._doc_before_save.workflow_state = doc.custom_previous_workflow
        doc.db_set("workflow_state", doc.custom_previous_workflow)


def convert_to_painter(doc,event):
    if doc.customer_group=="Painters" and doc.mail_send:
        doc.convert_to_painter=1
    if not doc.qr_code_scanned or not doc.convert_to_painter:
        if doc.customer_group == "Painters":
            frappe.throw("You cannot change the customer group to painters")


@frappe.whitelist()
def painter_conversion_email(doc):
    doc = frappe._dict(json.loads(doc))
    # if doc.qr_code_scanned and doc.enter_otp and not doc.mail_send:
    default_email=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","email")
    message=_("Approval Document {0}").format(
        get_link_to_form(doc["doctype"], doc["name"])
    )
    frappe.sendmail(
        recipients=default_email,
        message=message,
        subject="Approval For Painter Converstion",
        reference_doctype=doc.doctype,
        reference_name=doc["name"],
    )
    frappe.db.set_value(doc["doctype"], doc["name"], "mail_send", 1, update_modified=False)
    # frappe.show_alert("Painter Conversion Approval Send To Admin")

    return True

def copy_mobile_no(self, event):
    if self.mobile_no1 and not self.mobile_no:
        self.mobile_no = self.mobile_no1

# def before_validate(doc,event):
#     custom_franchise = frappe.get_all("Customer",['name'],filters={'custom_franchise':doc.custom_franchise,'name':['!=',doc.name]},pluck='name')
#     if custom_franchise:
#         docs = [frappe.get_value('Customer',{'custom_franchise':doc.custom_franchise},'name')]
#         list_of_links = [get_link_to_form('Customer', p) for p in docs]
        # frappe.msgprint(f'Franchise is already linked in Customer - {format(comma_and(list_of_links))}', title='Warning',indicator="orange",raise_exception=1)
