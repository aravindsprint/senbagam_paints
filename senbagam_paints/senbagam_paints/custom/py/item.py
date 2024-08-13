import frappe

@frappe.whitelist()
def update_mobile_app_field_in_item_master(item_group,mobile_field):
    items = frappe.get_list("Item", filters={"item_group": item_group})
    frappe.enqueue(update_item_document, items=items, field=mobile_field)
    return 1

def update_item_document(items, field):
    for item in items:
        item_to_be_updated = frappe.get_doc("Item", item.name)
        item_to_be_updated.show_in_mobile_app = field
        item_to_be_updated.save()