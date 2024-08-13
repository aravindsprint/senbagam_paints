# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, get_link_to_form
from frappe.model.document import Document

class PainterCommissionRedemption(Document):
	def on_change(doc):
		if doc.workflow_state=="Processing":
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
	print("fdsssss")
	total_comm=frappe.db.sql("""select sum(total_commission_rate) as total from `tabPainter Commission` where painter=%s and docstatus=1""",(painter),as_dict=1)
	if total_comm[0]["total"]:
		all_painter_rate=frappe.get_all("Commission Redemption",{"workflow_state":"Approved","painter":painter})
		v=0
		for i in all_painter_rate:
			redem_value=frappe.get_value("Commission Redemption",i["name"],"points_do_redemption")
			v+=redem_value
		print(v)
		total=float(total_comm[0]["total"]) - v
		print(total)
	return total



@frappe.whitelist()
def total_loyalty_points(painter):
	total=0
	total_comm=[{'total': 0}]
	total_comm=frappe.db.sql("""select sum(loyalty_points) as total from `tabLoyalty Point Entry` where customer=%s """,(painter),as_dict=1)
	if total_comm[0]["total"]:
		all_painter_rate=frappe.get_all("Commission Redemption",{"workflow_state":"Approved","painter":painter})
		v=0
		for i in all_painter_rate:
			redem_value=frappe.get_value("Commission Redemption",i["name"],"points_do_redemption")
			v+=redem_value
		total=float(total_comm[0]["total"]) - v
	return total