# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, get_link_to_form
from frappe.model.document import Document

class CommissionRedemption(Document):
	def on_change(doc):
		if doc.workflow_state=="Processing" and doc.points_do_redemption:
			default_email=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","email")
			message=_("Approval Document {0}").format(
				get_link_to_form(doc.doctype, doc.name)
			)
			frappe.sendmail(
				recipients=default_email,
				message=message,
				subject="Approval For Commission Redemption",
				reference_doctype=doc.doctype,
				reference_name=doc.name,
			)
			frappe.msgprint("Commission Redemption Approval Send To Admin")
	


@frappe.whitelist()
def total_commission_points(painter):

	total=0
	if frappe.db.exists("Commission Redemption",{"painter":painter,"workflow_state":"Completed"}):
		last_doc=frappe.get_last_doc("Commission Redemption",{"painter":painter,"workflow_state":"Completed"})
		total=last_doc.available_points_after_tds
	
	total_comm=frappe.db.sql("""select sum(total_commission_rate) as total from `tabPainter Commission` where painter=%s and docstatus=1""",(painter),as_dict=1)
	frappe.errprint(total_comm)
	if total_comm[0]["total"]:
		all_painter_rate=frappe.get_all("Commission Redemption",{"workflow_state":"Completed","painter":painter})
		v=0
		if all_painter_rate:
			for i in all_painter_rate:
				redem_value=frappe.get_value("Commission Redemption",i["name"],"points_do_redemption")
				v+=redem_value
			
		total=float(total_comm[0]["total"]) - v
		
	
	frappe.errprint("sfdgdfgfghf")
	return total



@frappe.whitelist()
def total_loyalty_points(painter):
	total=0
	if frappe.db.exists("Commission Redemption",{"painter":painter}):
		last_doc=frappe.get_last_doc("Commission Redemption",{"painter":painter,"workflow_state":"Completed"})
		total=last_doc.available_points_after_tds
	else:
		total_comm=[{'total': 0}]
		total_comm=frappe.db.sql("""select sum(loyalty_points) as total from `tabLoyalty Point Entry` where customer=%s """,(painter),as_dict=1)
		print(total_comm[0]["total"])
		if total_comm[0]["total"]:
			all_painter_rate=frappe.get_all("Commission Redemption",{"workflow_state":"Completed","painter":painter})
			v=0
			for i in all_painter_rate:
				redem_value=frappe.get_value("Commission Redemption",i["name"],"points_do_redemption")
				v+=redem_value
			total=float(total_comm[0]["total"]) - v
		print(total)
	return total


@frappe.whitelist()
def tds_percentage(amount,total_points):
	total=0
	percentage=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","commission_tds_percentage")
	if percentage:
		total=float(amount)*(float(percentage))/100
	total=float(total_points)-float(amount)-float(total)
	return total