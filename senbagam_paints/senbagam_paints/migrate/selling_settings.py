import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def ss_custom_fields():
    custom_fields = {
        'Selling Settings': [
            {
                "fieldname": "thirvu_selling_settings",
                "fieldtype": "Tab Break",
                "label": "Selling Settings",
                "insert_after" : "enable_discount_accounting"
            },
            {
                "fieldname": "paid_so_required_for_child_company",
                "fieldtype": "Check",
                "label": "For Child Company, Paid sales order is required to create <b>Sales Invoice</b>",
                "insert_after" : "thirvu_selling_settings"
            },
            {
                "fieldname": "si_without_so_role",
                "fieldtype": "Link",
                "options": "Role",
                "label": "Role allowed to create sales invoice without paid sales order",
                "insert_after" : "paid_so_required_for_child_company"
            },
            {
                "fieldname":"inventory_settings",
                "fieldtype":"Section Break",
                "label":"Inventory Settings",
                "insert_after":"si_without_so_role"

            },
            {
                "fieldname":"stock_should_not_go_above_the_current_qty_for_franchise",
                "fieldtype":"Check",
                "label":"Reconciled Stock Shouldn't go above the current qty for franchise",
                "insert_after":"inventory_settings"
            }
        ]
    }

    create_custom_fields(custom_fields)

    for field in [
        "customer_defaults_section",
        "item_price_settings_section",
        "sales_transactions_settings_section"
    ]:
        make_property_setter(
				"Selling Settings", field, "depends_on", "eval: frappe.session.user == 'Administrator'", "Data"
			)
    