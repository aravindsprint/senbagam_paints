# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class PainterCommission(Document):
	def validate(self):
		commission_rate=0
		painter_comm=frappe.get_all("Painter Commission",filters={"name":["not in",[self.name]]})
		for i in painter_comm:
			comm_doc=frappe.get_doc("Painter Commission",i["name"])
			for j in comm_doc.items:
				
				if self.scan_items == j.serial_no:
					frappe.throw(_("This Serial No Already Scanned {0} in {1}").format(j.serial_no,j.parent))
		for k in self.items:
			commission_rate+=k.painter_commission
		self.total_commission_rate=commission_rate


	def on_submit(self):
		for j in self.items:
			row_name=frappe.db.get_value("Sales Invoice Item",{"parent":j.invoice_no, "serial_no": j.serial_no},"name")
			row_total_qty=frappe.db.get_value("Sales Invoice Item",{"parent":j.invoice_no, "serial_no": j.serial_no},"qty")
			frappe.db.set_value("Sales Invoice Item",row_name,"scanned_serial_no",j.serial_no)
			frappe.db.set_value("Sales Invoice Item",row_name,"yet_to_scanned_qty",row_total_qty-1)
			frappe.db.commit()



			
			






@frappe.whitelist()
def painter_commision_rate(item):
	commission_rate=frappe.get_value("Item",item,"painter_commision")
	return commission_rate

