import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.core.page.permission_manager.permission_manager import add, update

def create_permission():
    create_workflow_state()
    create_workflow()
    customer_group()
    custom_fields()
    # create_workflow_commision()
    # create_customer()
    # create_referral()
    add(parent="Customer", role="Company Admin", permlevel=2)
    update(role="Company Admin", permlevel=2, doctype="Customer", ptype="read", value="1")
    update(role="Company Admin", permlevel=2, doctype="Customer", ptype="write", value="1")


def customer_group():
    if not frappe.db.exists("Customer Group", "Painters"):
        doc = frappe.new_doc("Customer Group")
        doc.parent_customer_group = "All Customer Groups"
        doc.customer_group_name = "Painters"
        doc.save()
        
    if not frappe.db.exists("Customer Group", "Distributor"):
        doc = frappe.new_doc("Customer Group")
        doc.parent_customer_group = "All Customer Groups"
        doc.customer_group_name = "Distributor"
        doc.save()

def create_workflow_state():	
    if not frappe.db.exists("Workflow State", "Enabled"):	
        doc = frappe.new_doc("Workflow State")	
        doc.update({	
            "workflow_state_name": "Enabled",	
            "style": "Primary"	
        })	
        doc.save()	

    if not frappe.db.exists("Workflow State", "Disabled"):	
        doc = frappe.new_doc("Workflow State")	
        doc.update({	
            "workflow_state_name": "Disabled",	
            "style": None	
        })	
        doc.save()	

def custom_fields():
    custom_fields = {
        'Customer': [
            {
                "fieldname": "upi_number",
                "fieldtype": "Data",
                "label": "Upi Number",
                "read_only":1,
                "insert_after" : "refered_by"
            },],
            "User":[
                {
                "fieldname": "referral_id",
                "fieldtype": "Data",
                "label": "Referral ID",
                "read_only":1,
                "insert_after" : "api_sceret"
                }
            ]
            }
    create_custom_fields(custom_fields)

def create_workflow():	
    if frappe.db.exists("Workflow", "Painter Conversion"):	
        return	

    doc = frappe.new_doc("Workflow")	
    doc.update({	
        "workflow_name": "Painter Conversion",	
        "document_type": "Customer",	
        "is_active": 1,	
        "override_status": 0,	
        "send_email_alert": 0,	
        "workflow_state_field": "workflow_state",	
        "doctype": "Workflow",	
        "transitions": [	
            {	
                "state": "Enabled",	
                "action": "Approve",	
                "next_state": "Approved",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Painter Conversion",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition",	
                "condition": "doc.qr_code_scanned == 1"	
            },	
            {	
                "state": "Enabled",	
                "action": "Reject",	
                "next_state": "Rejected",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Painter Conversion",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition",	
                "condition": "doc.qr_code_scanned == 1"	
            },	
            {	
                "state": "Approved",	
                "action": "Reject",	
                "next_state": "Rejected",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Painter Conversion",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition"	
            },	
            {	
                "state": "Rejected",	
                "action": "Approve",	
                "next_state": "Approved",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Painter Conversion",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition"	
            }	
        ],	
        "states": [	
            {	
                "state": "Enabled",	
                "doc_status": "0",	
                "update_field": "workflow_state",	
                "update_value": "Enabled",	
                "is_optional_state": 0,	
                "allow_edit": "Sales Manager",	
                "parent": "Painter Conversion",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Approved",	
                "doc_status": "0",	
                "update_field": "convert_to_painter",	
                "update_value": "1",	
                "is_optional_state": 0,	
                "allow_edit": "Company Admin",	
                "parent": "Painter Conversion",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Rejected",	
                "doc_status": "0",	
                "update_field": "convert_to_painter",	
                "update_value": "0",	
                "is_optional_state": 0,	
                "allow_edit": "Company Admin",	
                "parent": "Painter Conversion",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Disabled",	
                "doc_status": "0",	
                "update_field": "workflow_state",	
                "update_value": "Disabled",	
                "is_optional_state": 0,	
                "allow_edit": "System Manager",	
                "parent": "Painter Conversion",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            }	
        ]	
    })	
    doc.save()	

    customers = frappe.db.get_all("Customer", ["name", "disabled", "convert_to_painter"])	
    for customer in customers:	
        status = 'Enabled'	
        if customer.disabled:	
            status = 'Disabled'	
        elif customer.convert_to_painter:	
            status = 'Approved'	

        frappe.db.set_value("Customer", customer.name, "workflow_state", status, update_modified=False)



def create_workflow_commision():
    if frappe.db.exists("Workflow", "Commission Redemption"):	
        return	

    doc = frappe.new_doc("Workflow")	
    doc.update({	
        "workflow_name": "Commission Redemption",	
        "document_type": "Commission Redemption",	
        "is_active": 1,	
        "override_status": 0,	
        "send_email_alert": 0,	
        "workflow_state_field": "workflow_state",	
        "doctype": "Workflow",	
        "transitions": [	
            {	
                "state": "Draft",	
                "action": "Processing",	
                "next_state": "Processing",	
                "allowed": "Franchise Admin",	
                "allow_self_approval": 1,	
                "parent": "Commission Redemption",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition",
                "condition":"doc.points_do_redemption"	
            },	
            {	
                "state": "Processing",	
                "action": "Approve",	
                "next_state": "Completed",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Commission Redemption",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition",	
            },	
            {	
                "state": "Processing",	
                "action": "Reject",	
                "next_state": "Rejected",	
                "allowed": "Company Admin",	
                "allow_self_approval": 1,	
                "parent": "Commission Redemption",	
                "parentfield": "transitions",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Transition",	
            },	
        ],	
        "states": [	
            {	
                "state": "Draft",	
                "doc_status": "0",	
                # "update_field": "workflow_state",	
                # "update_value": "Enabled",	
                "is_optional_state": 0,	
                "allow_edit": "Franchise Admin",	
                "parent": "Commission Redemption",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Processing",	
                "doc_status": "1",	
                # "update_field": "workflow_state",	
                # "update_value": "Enabled",	
                "is_optional_state": 0,	
                "allow_edit": "Franchise Admin",	
                "parent": "Commission Redemption",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Completed",	
                "doc_status": "1",	
                # "update_field": "convert_to_painter",	
                # "update_value": "1",	
                "is_optional_state": 0,	
                "allow_edit": "Company Admin",	
                "parent": "Commission Redemption",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
            {	
                "state": "Rejected",	
                "doc_status": "2",	
                # "update_field": "convert_to_painter",	
                # "update_value": "0",	
                "is_optional_state": 0,	
                "allow_edit": "Company Admin",	
                "parent": "Commission Redemption",	
                "parentfield": "states",	
                "parenttype": "Workflow",	
                "doctype": "Workflow Document State"	
            },	
        ]	
    })	
    doc.save()
    frappe.db.commit()
    
def create_customer():
    if not frappe.db.exists("Customer", "Senbagam Paints"):
        doc = frappe.new_doc("Customer")
        doc.customer_name = "Senbagam Paints"
        doc.customer_type = "Company"
        doc.territory = "India"
        doc.customer_group = "All Customer Groups"
        doc.refered_by = ""
        doc.save()
        frappe.db.commit()
        
def create_referral():
    if not frappe.db.exists("Referral Tree", "Senbagam Paints"):
        customer = frappe.db.get_value("Customer", {"name":"Senbagam Paints"}, "name")
        if customer:
            doc = frappe.new_doc("Referral Tree")
            doc.customer = "Senbagam Paints"
            doc.is_group = 1
            doc.save()
            frappe.db.commit()
