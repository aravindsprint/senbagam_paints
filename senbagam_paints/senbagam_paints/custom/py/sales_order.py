import frappe
def validate(self,event):
    qty_validation(self)

def qty_validation(self):
    for i in self.items:
        if i.purchase_order_item:
            qty = frappe.get_value('Purchase Order Item',i.purchase_order_item,'qty')
            if i.qty > qty:
                frappe.throw(f'Row - {i.idx} Qty should not be greater than Purchase Qty <b>({qty})</b> for Item - <b>{i.item_code}</b>')
