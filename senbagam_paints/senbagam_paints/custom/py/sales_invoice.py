import frappe
import datetime
from frappe.utils import add_days
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

def update_sales_person(doc,event):
    user = frappe.session.user
    doc.sales_team = []
    if frappe.db.exists('Employee',{'user_id':user}):
        employee = frappe.get_value('Employee',{'user_id':user},'name')
        if frappe.db.exists('Sales Person',{'employee':employee}):
            sales_person = frappe.get_doc("Sales Person",{''})
            allocated_amount = sum(
                    item.base_net_amount for item in doc.items if item.grant_commission
                )* (float(sales_person.custom_contribution__ or 0)/100)
            doc.append('sales_team',{
                'sales_person':sales_person.name,
                'allocated_percentage':sales_person.custom_contribution__,
                'commission_rate':sales_person.commission_rate,
                'allocated_amount':allocated_amount,
                'incentives':allocated_amount * (float(sales_person.commission_rate or 0)/100)
            })
    if doc.is_return:
        check_return_invoice(doc)

def check_return_invoice(doc):
    for it in doc.items:
        if not it.is_seald:
            frappe.throw(f'Only Sealed Items can be returned - Row {it.idx}')

            


class salesInvoice(SalesInvoice): 
    def validate(self):
        customer_group=frappe.get_value("Customer",self.customer,"customer_group")
        if customer_group == "Individual":
            percentage=frappe.db.sql(f"""select percentage from `tabFranchise To User` pd 
            where pd.parent="Sales Value Based Discount Settings" and pd.start_amount <= '{self.net_total}' and pd.upto >= '{self.net_total}'  """.format(self.net_total,self.net_total),as_dict=1)

            if percentage and not self.additional_discount_percentage and not self.discount_amount:
                dis_pers=percentage[0]["percentage"]
                self.apply_discount_on="Net Total"
                self.additional_discount_percentage=dis_pers

                # self.discount_amount=self.net_total*(float(dis_pers))/100
        super(SalesInvoice, self).validate()
        


def vlidate_sales_order(doc,event):
    selling_settings = frappe.get_single("Selling Settings")
    
    if selling_settings.si_without_so_role and selling_settings.si_without_so_role in frappe.get_roles():
        return

    if frappe.get_value("Company", doc.company, "is_group") or selling_settings.paid_so_required_for_child_company:
        for row in doc.items:
            if not row.sales_order:
                frappe.throw(f"Sales Invoice should be created against a Sales Order in items")
            elif row.sales_order:
                sales_order = frappe.db.get_value("Sales Order", row.sales_order, ['rounded_total', 'advance_paid'], as_dict=True)
                if sales_order.rounded_total != sales_order.advance_paid:
                    frappe.throw(f"Cannot create sales invoice against unpaid sales order {row.sales_order} in items row {row.idx}")



def loyalty_points(doc,event):
    company_doc=frappe.get_doc("Company",{"company_type":"Parent"})
    if doc.status == "Paid":
        customer_group=frappe.get_value("Customer",doc.customer,"customer_group")
        if customer_group == "Individual":
            reference1=frappe.get_value("Customer",doc.customer,"refered_by")
            reference2=frappe.get_value("Customer",reference1,"refered_by")
            if reference1 and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name}):
                loyalty_percentage=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","first_parent")
                loyalty_points=doc.net_total*(float(loyalty_percentage))/100
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=reference1
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.expiry_date=add_days(doc.posting_date, +100)
                create_doc.company=doc.company
                create_doc.save(ignore_permissions=True)

            if reference2 and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name,"customer":reference2}):
                loyalty_percentage=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","second_parent_")
                loyalty_points=doc.net_total*(float(loyalty_percentage))/100
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=reference2
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.expiry_date=add_days(doc.posting_date, +100)
                create_doc.company=doc.company
                create_doc.save(ignore_permissions=True)
        if customer_group == "Dealer" and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name,"customer":doc.customer}):
            percentage=frappe.db.sql("""select percentage from `tabParent To Dealer` pd 
            where pd.parent="Sales Value Based Discount Settings" and '%s' between pd.start_amount and pd.upto""".format(doc.net_total),as_dict=1)
            if percentage:
                loyalty_pers=percentage[0]["percentage"]
                loyalty_points=doc.net_total*(float(loyalty_pers))/100
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=doc.customer
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.company=company_doc.name or doc.company
                create_doc.save(ignore_permissions=True)
        if customer_group == "Franchise" and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name,"customer":doc.customer}):
            percentage=frappe.db.sql("""select percentage from `tabParent To Franchise` pd 
            where pd.parent="Sales Value Based Discount Settings" and '%s' between pd.start_amount and pd.upto""".format(doc.net_total),as_dict=1)
            reference1=frappe.get_value("Customer",doc.customer,"refered_by")
            reference2=frappe.get_value("Customer",reference1,"refered_by")
            if percentage:
                loyalty_pers=percentage[0]["percentage"]
                loyalty_points=doc.net_total*((float(loyalty_pers))/100)
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=doc.customer
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.company=company_doc.name or doc.company
                create_doc.save(ignore_permissions=True)
            if reference1 and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name,"customer":reference1}):
                loyalty_percentage=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","first_parent")
                loyalty_points=doc.net_total*(float(loyalty_percentage))/100
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=reference1
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.expiry_date=add_days(doc.posting_date, +100)
                create_doc.company=doc.company
                create_doc.save(ignore_permissions=True)
            if reference2 and not frappe.db.exists("Loyalty Point Entry",{"invoice":doc.name,"customer":reference2}):
                loyalty_percentage=frappe.get_value("Sales Value Based Discount Settings","Sales Value Based Discount Settings","second_parent_")
                loyalty_points=doc.net_total*(float(loyalty_percentage))/100
                create_doc=frappe.new_doc("Loyalty Point Entry")
                create_doc.customer=reference2
                create_doc.invoice_type=doc.doctype
                create_doc.invoice=doc.name
                create_doc.loyalty_points= loyalty_points
                create_doc.purchase_amount=doc.net_total
                create_doc.posting_date=doc.posting_date
                create_doc.expiry_date=add_days(doc.posting_date, +100)
                create_doc.company=doc.company
                create_doc.save(ignore_permissions=True)
            

            

# def end_user_discount(doc,event):
#     customer_group=frappe.get_value("Customer",doc.customer,"customer_group")
#     if customer_group == "Individual":
#         percentage=frappe.db.sql("""select percentage from `tabFranchise To User` pd 
#         where pd.parent="Sales Value Based Discount Settings" and '%s' between pd.start_amount and pd.upto""".format(doc.net_total),as_dict=1)
#         print(percentage[0]["percentage"])
#         if percentage and not doc.additional_discount_percentage and not doc.discount_amount:
#             dis_pers=percentage[0]["percentage"]
#             doc.apply_discount_on="Net Total"
#             doc.additional_discount_percentage=dis_pers
#             doc.discount_amount=doc.net_total*(float(dis_pers))/100
            



    
@frappe.whitelist()
def get_customer(doctype, txt, searchfield, start, page_len, filters):
    cond = ""
    if filters and filters.get("company"):
        account_type = frappe.db.get_value("Company", filters.get("company"), "is_group")
        if account_type:
            cond = "and customer_group = 'Distributor' or (represents_company != name and is_internal_customer = 1)"
            
    return frappe.db.sql(
        """select name from `tabCustomer`
            where `{key}` LIKE %(txt)s {cond}
            order by name limit %(page_len)s offset %(start)s""".format(
            key=searchfield, cond=cond
        ),
        {"txt": "%" + txt + "%", "start": start, "page_len": page_len},
    )
