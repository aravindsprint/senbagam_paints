
import frappe
from frappe.core.doctype.session_default_settings.session_default_settings import set_session_default_values

def create_company_type():
    company_type=["Parent","Franchise"]
    for i in company_type:
        if not frappe.db.exists("Company Type",i):
            if i=="Parent":
                new_doc=frappe.new_doc("Company Type")
                new_doc.update({
                    "type":"Parent"
                })
                new_doc.save(ignore_permissions=True)
            else:
                new_doc=frappe.new_doc("Company Type")
                new_doc.update({
                    "type":i,
                    "sales":1,
                    "purchase":1
                })
                new_doc.save(ignore_permissions=True)



def create_role_profile():
    # if(not frappe.db.exists('Role Profile', 'Company Admin')):
    #     new_doc=frappe.new_doc("Role Profile")
    #     roles=["Accounts Manager","Accounts User","Company Admin","Customer","Expense Approver","Fleet Manager",
    #            "Franchise Admin","HR Manager","HR User","Item Manager","Manufacturing User","Manufacturing Manager",
    #            "Purchase Master Manager","Purchase User","Quality Manager","Report Manager","Sales Manager",
    #            "Sales Master Manager","Stock Manager","Stock User","Supplier","System Manager",
    #             ] 
    #     role_list=[]
    #     for role in roles:
    #         role_dict = frappe._dict({
    #                 "role": role,
    #             })
    #         role_list.append(role_dict)
    #     new_doc.update({
    #         "role_profile":"Company Admin",
    #         "roles":role_list
    #     })
    #     new_doc.save(ignore_permissions=True)
    #     frappe.db.commit()
    
    if(not frappe.db.exists('Role Profile', 'App User')):
        new_doc=frappe.new_doc("Role Profile")

        roles=["Customer","Item Manager","Sales Manager","Sales Master Manager","Sales User","Stock Manager","System Manager"] 
        role_list=[]
        for role in roles:
            role_dict = frappe._dict({
                    "role": role,
                })
            role_list.append(role_dict)
        new_doc.update({
            "role_profile":"App User",
            "roles":role_list
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()
    

def create_role():
    if(not frappe.db.exists('Role', 'Company Admin')): 	
        doc = frappe.new_doc("Role")
        doc.update({"role_name": "Company Admin", "desk_access": 1})
        doc.insert(ignore_permissions=True)


def create_module_profile():
    if not frappe.db.exists('Module Profile', 'Company Admin'):
        new_doc = frappe.new_doc("Module Profile")
        all_modules = frappe.get_all("Module Def")
        block_modules = ["Accounts", "Franchise Automation", "Senbagam Paints Mobile App", "CRM", "Senbagam Api",
                         "Field wise cusomization", "Mobility APIs", 'Senbagam Paints']
        filtered_modules = [module for module in all_modules if module["name"] not in block_modules]
        module_list = []
        for module in filtered_modules: 
            module_dict = frappe._dict({
                "module": module["name"],
            })
            module_list.append(module_dict)
        new_doc.update({
            "module_profile_name": "Company Admin",
            "block_modules": module_list
        })
        new_doc.save(ignore_permissions=True)
        frappe.db.commit()




def create_session_default_for_company():
   
    user = frappe.session.user
    company = frappe.db.get_value('User Permission', {'user':user, 'allow':'Company'}, 'for_value')

    default_values = {
        'Company':company
    }
    frappe.defaults.set_user_default("company",company)