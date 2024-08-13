import frappe
from frappe.model.naming import parse_naming_series

def customer(doc,event):
    if not doc.is_internal_customer:
        doc.name = parse_naming_series(f'{doc.customer_name}-{doc.mobile_no1 or ""}')
    else:
        doc.name = parse_naming_series(f'{doc.customer_name}')

def sales_invoice(self,event):
    if self.is_return :
        self.name=parse_naming_series(f'SR{self.city_abbr}{self.abbr}.YYYY.####')  
    else:
        self.name=parse_naming_series(f'SI{self.city_abbr}{self.abbr}.YYYY.####')  
#     fy = get_fiscal_year_short_form()
#     abbr = frappe.get_value('Company',doc.company,'abbr')
#     if not doc.is_return:
#         doc.name = parse_naming_series(f'SI-{fy}-{abbr}-.###')
#     else:
#         doc.name = parse_naming_series(f'SR-{fy}-{abbr}-.###')

def sales_order(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'SO-{fy}-{abbr}-.###')

def delivery_note(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'DN-{fy}-{abbr}-.###')

def quotation(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'QT-{fy}-{abbr}-.###')

def purchase_invoice(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    if not doc.is_return:
        doc.name = parse_naming_series(f'PI-{fy}-{abbr}-.###')
    else:
        doc.name = parse_naming_series(f'PR-{fy}-{abbr}-.###')

def purchase_order(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'PO-{fy}-{abbr}-.###')

def purchase_receipt(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'PR-{fy}-{abbr}-.###')

def journal_entry(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'JE-{fy}-{abbr}-.###')

def payment_entry(doc,event):
    fy = get_fiscal_year_short_form()
    abbr = frappe.get_value('Company',doc.company,'abbr')
    doc.name = parse_naming_series(f'PE-{fy}-{abbr}-.###')


def get_fiscal_year_short_form():
    fy =  frappe.db.get_single_value('Global Defaults', 'current_fiscal_year')
    return fy.split('-')[0][2:]
