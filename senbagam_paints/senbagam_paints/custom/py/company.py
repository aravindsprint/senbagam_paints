import frappe
from frappe import _
from frappe.utils import flt, get_link_to_form

def qr_abbr(self,event):
    if self.is_group:
        self.company_type = "Parent"
    else:
        self.company_type = "Franchise"
    if self.abbr:
        self.qr_content = self.abbr
        self.save()


def qr_update_com():
    company_list=frappe.get_all("Company")
    for i in company_list:
        company= frappe.get_doc("Company",i.name)
        company.qr_content = company.abbr
        company.save(ignore_permissions=True)

def validate(doc,event):
    if doc.is_group:
        check = frappe.get_all('Company',{'is_group':1,'name':['!=',doc.name]},pluck='name')
        if len(check):
            company =  check[0]
            frappe.throw(
                _(f"Parent company - {get_link_to_form('Company', company)} already exists"),
                title=_("Warning"),
            )

def after_insert(self,event):
    qr_abbr(self,event)
    default_warehouse(self)

def default_warehouse(self):
    if self.is_group:
        warehouse_list = ['Raw Material','Semi-Finished','Ready for Sales','Damaged','Return']
        for wh in frappe.get_all('Warehouse',{"is_group":0,'company':self.name},['warehouse_name'],pluck='warehouse_name'):
            if wh in warehouse_list:
                warehouse_list.remove(wh)
            else:
                frappe.db.set_value('Warehouse',{'warehouse_name':wh,'company':self.name},'disabled',1)
    else:
        warehouse_list = ['Ready for Sales','Damaged','Return']
        for wh in frappe.get_all('Warehouse',{"is_group":0,'company':self.name},['warehouse_name'],pluck='warehouse_name'):
            if wh in warehouse_list:
                warehouse_list.remove(wh)
            else:
                frappe.db.set_value('Warehouse',{'warehouse_name':wh,'company':self.name},'disabled',1)
    
    for i in warehouse_list:
        wh_doc = frappe.new_doc('Warehouse')
        wh_doc.warehouse_name = i
        wh_doc.company = self.name
        wh_doc.save(ignore_permissions=True)
