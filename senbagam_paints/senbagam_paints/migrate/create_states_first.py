import frappe

def create_workflow_states():
    """Create workflow states before creating the workflow"""
    
    states = ["Draft", "Processing", "Completed"]
    
    for state in states:
        if not frappe.db.exists("Workflow State", state):
            doc = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state,
                "icon": "icon-ok" if state == "Completed" else "icon-file",
                "style": "Success" if state == "Completed" else "Primary"
            })
            doc.insert()
            print(f"Created Workflow State: {state}")

def create_workflow_actions():
    """Create workflow actions"""
    
    actions = ["Processing", "Complete"]
    
    for action in actions:
        if not frappe.db.exists("Workflow Action", action):
            doc = frappe.get_doc({
                "doctype": "Workflow Action",
                "workflow_action_name": action
            })
            doc.insert()
            print(f"Created Workflow Action: {action}")

def execute():
    create_workflow_states()
    create_workflow_actions()