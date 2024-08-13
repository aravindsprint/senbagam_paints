import frappe
from frappe.utils.data import add_days, comma_and, today

def morning():
    total_hq_sales_purchase()
    total_franchise_sales_purchase()
    new_lead()
    leave_application()
    overdue()
    # hq_required_purchase_qty()
    material_request()
    lead_assignment_count()

def overdue():
    today_ = today()

    hq_company = frappe.get_all("Company",filters={"is_group":1},pluck="name")
    count = 0
    amount = 0

    for company in hq_company:

        # overdue = frappe.get_all("Sales Order",filters={"delivery_date":today_,'rounded_total':['!=',''], "company": company},pluck="grand_total")
        overdue = frappe.db.sql(f'''select name from `tabSales Order` as so where so.delivery_date = '{today_}' and so.rounded_total != so.advance_paid and so.company = '{company}' ''',as_dict=1)
        amt = frappe.db.sql(f'''select sum(so.rounded_total - so.advance_paid) as amt  from `tabSales Order` as so where so.delivery_date = '{today_}' and so.rounded_total != so.advance_paid and so.company = '{company}' ''',as_dict=1)
        count += len(overdue)
        amount = amt[0].get('amt') if amt else 0

    subject = f"Payment moving to overdue today: {count}, Payable: Rs.{amount}"

    email_content = subject+'''<br><button><a href='/app/sales-invoice?due_date=["Between"%2C["{0}"%2C"{0}"]]&docstatus=["!%3D"%2C"2"]'>Open Today's Overdue</a></button>'''.format(today_)
    
    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_sales_invoice_overdue") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile),
        from_user = frappe.session.user, 
        name =  'view', 
        subject = subject,
        doctype = "Sales Invoice", 
        email_content = email_content,
    )

def leave_application():
    hq_company = frappe.get_all("Company",filters={"is_group":1},pluck="name")
    for company in hq_company:
        tomorrow = add_days(today(), +1) 
        today_ = today()
        
        today_leave_count= frappe.get_all("Leave Application",filters={"from_date":["<=",today_],"to_date":[">=",today_],"status":"Approved","company": company},pluck="employee_name")
        tomrrow_leave_count= frappe.get_all("Leave Application",filters={"from_date":["<=",tomorrow],"to_date":[">=",tomorrow],"status":"Approved","company": company},pluck="employee_name")
        pending_approvel = frappe.get_all("Leave Application",filters={"status":"Open","company": company},pluck="name")
        email_content = "Employees on declared leave today: {0}<br>Employees on declared  leave tomorrow: {1}".format(comma_and(today_leave_count),comma_and(tomrrow_leave_count))
        for i in pending_approvel:
            email_content  = email_content+"<br>Leaves pending for approval: <a href='/app/leave-application/{0}'>{0}</a>".format(i)
        
        role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_leave_application") or []]
        if not role_profile:
            return

        notification(
            to_user = get_users_email(role_profile),
            from_user = frappe.session.user, 
            name = 'view', 
            subject = "No. of employees on declared leave today: {0}<br>No. of employees on declared  leave tomorrow: {1}<br>No. of leaves pending for approval: {2}".format(len(today_leave_count),len(tomrrow_leave_count),len(pending_approvel)), 
            doctype = "Leave Application", 
            email_content = email_content,
        )

def new_lead():
    yesterday = add_days(today(), -1) 
    #    yesterday = today()
    lead_count = len(frappe.get_all("Lead", filters={"creation": ["between", [yesterday,yesterday]]},pluck="name"))
    subject = "No. of new leads assigned yesterday: {0}".format(lead_count)
    email_content = subject + '''<br><button><a href='/app/lead?creation=["Between"%2C["{0}"%2C"{0}"]]'>Open Yesterdays Lead</a></button>'''.format(yesterday)
    
    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_new_leads") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile),
        from_user = frappe.session.user, 
        name =  'view', 
        subject = subject,
        doctype = "Lead", 
        email_content = email_content,
    )
   
def total_hq_sales_purchase():
    yesterday = add_days(today(), -1)
    # yesterday = today()
    total_sales = count_sales = 0
    total_purchase = count_purchase = 0
    hq_company = frappe.get_all("Company",filters={"is_group":1},pluck="name")
    for company in hq_company:
        sales_invoice = frappe.get_all("Sales Invoice", filters={"company":company,"creation": ["between", [yesterday,yesterday]],"docstatus":["=",1]},pluck="grand_total")
        purchase_invoice = frappe.get_all("Purchase Invoice", filters={"company":company,"creation": ["between", [yesterday,yesterday]],"docstatus":["=",1]},pluck="grand_total")
        count_sales = len(sales_invoice) + count_sales
        total_sales = sum(sales_invoice) + total_sales
        total_purchase = len(purchase_invoice) + total_purchase
        count_purchase = sum(purchase_invoice) + count_purchase
    subject = "Total HQ sales Count yesterday:{0}<br>Total HQ sales Grand Total yesterday:{1}<br>Total HQ purchase Count yesterday:{2}<br>Total HQ purchase Grand Total yesterday:{3}".format(count_sales,round(total_sales),total_purchase,round(count_purchase))
    email_content = subject + '''<br><button><a href='/app/purchase-invoice?creation=["Between"%2C["{0}"%2C"{0}"]]&docstatus=["!%3D"%2C"2"]'>Open Yesterdays Purchase</a></button><br><button><a href='/app/sales-invoice?creation=["Between"%2C["{0}"%2C"{0}"]]&docstatus=["!%3D"%2C"2"]'>Open Yesterdays Sales</a></button>'''.format(yesterday)
    
    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_sales_and_purchase_qty_and_amount") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile), 
        from_user = frappe.session.user, 
        name = None, 
        subject = subject,
        doctype = None, 
        email_content = email_content,
    )

def total_franchise_sales_purchase():
    yesterday = add_days(today(), -1)
    # yesterday = today()
    total_sales = count_sales = 0
    total_purchase = count_purchase = 0
    hq_company = frappe.get_all("Company",filters={"is_group":0},pluck="name")
    for company in hq_company:
        sales_invoice = frappe.get_all("Sales Invoice", filters={"company":company,"creation": ["between", [yesterday,yesterday]],"docstatus":["=",1]},pluck="grand_total")
        purchase_invoice = frappe.get_all("Purchase Invoice", filters={"company":company,"creation": ["between", [yesterday,yesterday]],"docstatus":["=",1]},pluck="grand_total")
        count_sales = len(sales_invoice) + count_sales
        total_sales = sum(sales_invoice) + total_sales
        total_purchase = len(purchase_invoice) + total_purchase
        count_purchase = sum(purchase_invoice) + count_purchase
    subject = "Total Franchise sales Count yesterday:{0}<br>Total Franchise sales Grand Total yesterday:{1}<br>Total Franchise purchase Count yesterday:{2}<br>Total Franchise purchase Grand Total yesterday:{3}".format(count_sales,total_sales,total_purchase,count_purchase)
    email_content = subject
    #  + '''<br><button><a href='/app/purchase-invoice?creation=["Between"%2C["{0}"%2C"{0}"]]&docstatus=["!%3D"%2C"2"]'>Open Yesterdays Purchase</a></button><br><button><a href='/app/sales-invoice?creation=["Between"%2C["{0}"%2C"{0}"]]&docstatus=["!%3D"%2C"2"]'>Open Yesterdays Sales</a></button>'''.format(yesterday)
    
    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_sales_and_purchase_qty_and_amount") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile), 
        from_user = frappe.session.user, 
        name = None, 
        subject = subject,
        doctype = None, 
        email_content = email_content,
    )

def hq_required_purchase_qty():
    tmrw = add_days(today(), +1)
    req_qty = order_count = 0
    parent_company = frappe.get_all("Company", filters={"is_group":1}, pluck="name")
    
    if not parent_company:
        return
    
    purchase_order = frappe.db.sql(f"""
        SELECT
            SUM(poi.qty - poi.received_qty) as qty
        FROM `tabPurchase Order Item` poi
        INNER JOIN `tabPurchase Order` po
        ON po.name = poi.parent AND poi.parenttype = 'Purchase Order' AND poi.parentfield = 'items'
        WHERE
            po.docstatus <= 1 AND
            po.status NOT IN ('On Hold', 'Closed') AND
            po.company IN {tuple(parent_company) if len(parent_company)>1 else f"('{parent_company[0]}')"} AND
            poi.schedule_date BETWEEN "{today()}" AND "{tmrw}"
        GROUP BY po.name
    """, as_dict=True)
    purchase_order = [i.qty for i in purchase_order if i.qty]

    req_qty = sum(purchase_order)
    order_count = len(purchase_order)
    
    if not req_qty:
        return
    
    subject = f"Purchase Orders yet to receive: {order_count}<br>Purchase Order qty yet to receive: {req_qty}"
    email_content = subject + '''<br><button><a href='/app/purchase-order?creation=["Between"%2C["{0}"%2C"{1}"]]&docstatus=["!%3D"%2C"2"]'>Open Yesterdays and Todays Purchase Orders</a></button>'''.format( today(),tmrw)
    
    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_purchase_order_req_qty") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile), 
        from_user = frappe.session.user, 
        name = None, 
        subject = subject,
        doctype = None, 
        email_content = email_content,
    )


def get_users_email(role):

    user = []
    for i in role:
        print(i)
        for j in frappe.get_all("User", filters={"role_profile_name": i,"enabled":1}, pluck="name"):
            print(j)
            user.append(j)
    return user

    
def notification(to_user, from_user, name, subject, doctype, email_content):
    for i in to_user:
        doc=frappe.new_doc('Notification Log')
        doc.update({
        'subject': subject,
        'for_user': i,
        'send_email': 1,
        'type': 'Alert',
        'document_type': doctype,
        'document_name': name,
        'from_user':from_user,
        'email_content': email_content
        })
        doc.flags.ignore_permissions=True
        doc.save()

def material_request():

    parent_company = frappe.get_all("Company", filters={"is_group":1}, pluck="name")
    
    if not parent_company:
        return
    
    tomorrow = add_days(today(), +1)

    mr_list_today = frappe.db.sql(f"""
        SELECT
            mri.parent,
            mri.qty,
            mri.item_name
        FROM
            `tabMaterial Request Item` mri,
            `tabMaterial Request` mr
        WHERE
            mri.docstatus = 1 AND
            mri.parent = mr.name AND
            mr.company IN {tuple(parent_company) if len(parent_company)>1 else f"('{parent_company[0]}')"} AND
            mri.schedule_date = "{today()}"
    """, as_dict=True)

    mr_list_tomorrow = frappe.db.sql(f"""
        SELECT
            mri.parent,
            mri.qty,
            mri.item_name
        FROM
            `tabMaterial Request Item` mri,
            `tabMaterial Request` mr
        WHERE
            mri.docstatus = 1 AND
            mri.parent = mr.name AND
            mr.company IN {tuple(parent_company) if len(parent_company)>1 else f"('{parent_company[0]}')"} AND
            mri.schedule_date = "{tomorrow}"
    """, as_dict=True)

    consolidated_today = consolidate_material_requests(mr_list_today)
    consolidated_tomorrow = consolidate_material_requests(mr_list_tomorrow)
    qty_today = sum(entry['qty'] for entry in consolidated_today.values())
    qty_tomorrow = sum(entry['qty'] for entry in consolidated_tomorrow.values())
    subject = "Raw Material arriving today: {0} items / {1} qty / {2} order <br>Raw Material arriving tomorrow: {3} items / {4} qty / {5} order".format(
        len(mr_list_today),qty_today,len(consolidated_today), 
        len(mr_list_tomorrow),qty_tomorrow,len(consolidated_tomorrow))

    email_content = subject + '''<br><button><a href='/app/material-request?schedule_date=["Between"%2C["{0}"%2C"{1}"]]&docstatus=1'>Open Today's and Tomorrow's Material Request</a></button>'''.format(today(),tomorrow)

    role_profile = [row.role_profile for row in frappe.get_single("HQ Notification Settings").get("role_profile_for_material_request") or []]
    if not role_profile:
        return

    notification(
        to_user = get_users_email(role_profile), 
        from_user = frappe.session.user, 
        name = None, 
        subject = subject,
        doctype = None, 
        email_content = email_content,
    )


def consolidate_material_requests(mr_list):
    consolidated_data = {}

    for mr in mr_list:
        parent = mr.get('parent')
        qty = mr.get('qty')
        item = mr.get('item_name')

        if parent in consolidated_data:
            consolidated_data[parent]['qty'] += qty
            consolidated_data[parent]['items'].append(item)
        else:
            consolidated_data[parent] = {'qty': qty, 'items': [item]}

    return consolidated_data

def lead_assignment_count():

    today_date = today()
    yesterday_date = add_days(today(), -1)

    today_count_list = frappe.get_all("Follow Ups", {"next_followup_date": today_date}, ["count(*) as count",'next_follow_up_by', "next_followup_date"], group_by = "next_follow_up_by")

    yesterday_count_list = frappe.get_all("Follow Ups", {"next_followup_date": yesterday_date}, ["count(*) as count",'next_follow_up_by'], group_by = "next_follow_up_by")

    count_list = today_count_list + yesterday_count_list
   
    count_list = sorted(count_list, key=lambda x: x["next_follow_up_by"])

    i = 0

    while(i < len(count_list)):

        to_user = count_list[i]["next_follow_up_by"]

        today_lead_count = 0

        yesterday_lead_count = 0

        if len(count_list) > 1:
            is_last_head_mapped = False

        else:
            is_last_head_mapped = True

        if count_list[i].get("next_followup_date"):
            today_lead_count = count_list[i]['count']
            
        else:
            yesterday_lead_count = count_list[i]['count']

        for j in range(i + 1, len(count_list), 1):

            is_last_head_mapped = False

            if count_list[i]["next_follow_up_by"] == count_list[j]["next_follow_up_by"]:

                is_last_head_mapped = True

                if count_list[j].get("next_followup_date"):
                    today_lead_count += today_lead_count

                else:
                    yesterday_lead_count += yesterday_lead_count

                i += 1

            else:

                i = j

                break

        subject = f"Today Assigned Lead Count: {today_lead_count} / Yesterday Assigned Lead Count: {yesterday_lead_count}"

        email_content = subject + '''<br><button><a href='/app/lead?next_followup_date=["Between"%2C["{0}"%2C"{1}"]]'>Open Yesterdays and Todays Assigned Lead</a></button>'''.format(yesterday_date, today_date)

        notification(
            to_user = [to_user], 
            from_user = frappe.session.user, 
            name = None, 
            subject = subject,
            doctype = None, 
            email_content = email_content,
        )

        if i == len(count_list) - 1:

            if not is_last_head_mapped:

                if count_list[i].get("next_followup_date"):
                    subject = f"Today Assigned Lead Count: {count_list[i]['count']} / Yesterday Assigned Lead Count: 0"

                else:
                    subject = f"Today Assigned Lead Count: 0 / Yesterday Assigned Lead Count: {count_list[i]['count']}"

                email_content = subject + ''' <br><button><a href='/app/lead?next_followup_date=["Between"%2C["{0}"%2C"{1}"]]'>Open Yesterdays and Todays Assigned Lead</a></button>'''.format(yesterday_date, today_date)

                notification(
                    to_user = [count_list[i]["next_follow_up_by"]], 
                    from_user = frappe.session.user, 
                    name = None, 
                    subject = subject,
                    doctype = None, 
                    email_content = email_content,
                )

            break
