import frappe
def validate_qty(doc,event):
    if doc.purpose == "Stock Reconciliation":
        if frappe.get_value('Selling Settings','Selling Settings','stock_should_not_go_above_the_current_qty_for_franchise')==1 or not frappe.get_value('Company',doc.company,'is_group'):
            for it in doc.items:
                # pass
                # # frappe.errprint(it.quantity_difference > 0)
                # # frappe.errprint(it.quantity_difference)

                if it.quantity_difference > 0:
                    frappe.errprint(f"{it.quantity_difference} {it.current_qty}  {it.qty}")
                    # frappe.throw(f'Qty Not allowed to Enter greater than current qty - Row {it.idx}')
