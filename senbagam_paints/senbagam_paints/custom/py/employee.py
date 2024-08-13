import frappe
from frappe import _, msgprint
from frappe.utils import get_link_to_form
from dateutil.relativedelta import relativedelta
from frappe.utils import getdate

def create_sales_person(doc,event):
    sp = frappe.new_doc('Sales Person')
    sp.sales_person_name = f'{doc.employee_name}-{doc.name}'
    sp.employee = doc.name
    sp.save()
    frappe.msgprint(_('Sales Person has been created - {0}').format(get_link_to_form('Sales Person', sp.name)))

def validate(doc,event):
    validate_dob(doc)

def validate_dob(doc):
    if relativedelta(getdate(), getdate(doc.date_of_birth)).years < 18:
        frappe.throw(f"Employee's age is { relativedelta(getdate(), getdate(doc.date_of_birth)).years}, under 18 years old.")