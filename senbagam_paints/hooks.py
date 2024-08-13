from . import __version__ as app_version

app_name = "senbagam_paints"
app_title = "Senbagam Paints"
app_publisher = "Thirvusoft"
app_description = "Senbagam Paints"
app_email = "ts@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/senbagam_paints/css/senbagam_paints.css"
# app_include_js = "/assets/senbagam_paints/js/senbagam_paints.js"

# include js, css files in header of web template
# web_include_css = "/assets/senbagam_paints/css/senbagam_paints.css"
# web_include_js = "/assets/senbagam_paints/js/senbagam_paints.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "senbagam_paints/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js",
			 "Purchase Invoice": "public/js/purchase_invoice.js",
			 "Sales Order":"public/js/sales_order.js",
			 "Delivery Note": "public/js/delivery_note.js",
			 "Purchase Receipt":"public/js/purchase_receipt.js",
			 "Purchase Order" :"public/js/purchase_order.js",
			 "Company":"public/js/company.js",
			 "Item Group":"public/js/item_group.js",
			 "Supplier":"public/js/supplier.js",
			 "Customer":"public/js/customer.js",
			 }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
        "frappe.contacts.doctype.address.address.get_default_address",
        "senbagam_paints.senbagam_paints.custom.py.print_format_salesinvoice.get_invoice_item_and_tax_details"
    ]
#	"filters": "senbagam_paints.utils.jinja_filters"
}

# Installation
# ------------

# before_install = "senbagam_paints.install.before_install"
# after_install = "senbagam_paints.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "senbagam_paints.uninstall.before_uninstall"
# after_uninstall = "senbagam_paints.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "senbagam_paints.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Sales Invoice": "senbagam_paints.senbagam_paints.custom.py.sales_invoice.salesInvoice"
}

after_migrate = [
    "senbagam_paints.senbagam_paints.migrate.selling_settings.ss_custom_fields",
    "senbagam_paints.senbagam_paints.migrate.customer.create_permission",
    "senbagam_paints.senbagam_paints.migrate.create_company_type.create_company_type",
    "senbagam_paints.senbagam_paints.migrate.create_company_type.create_role_profile",
    "senbagam_paints.senbagam_paints.migrate.create_company_type.create_module_profile",
    "senbagam_paints.senbagam_paints.migrate.create_company_type.create_role",
]

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Customer": {
		# "after_insert": "senbagam_paints.senbagam_paints.custom.py.customer.user_creation",
		"validate":[
			"senbagam_paints.senbagam_paints.custom.py.customer.copy_mobile_no",
			"senbagam_paints.senbagam_paints.custom.py.customer.change_workflow",
            "senbagam_paints.senbagam_paints.custom.py.customer.convert_to_painter",
		],
		# "before_validate": "senbagam_paints.senbagam_paints.custom.py.customer.before_validate",

		"autoname": 'senbagam_paints.senbagam_paints.custom.py.naming.customer'
	},
	"Sales Invoice":{
		"on_change":"senbagam_paints.senbagam_paints.custom.py.sales_invoice.loyalty_points",
		"autoname":'senbagam_paints.senbagam_paints.custom.py.naming.sales_invoice',
		"validate":[
            # "senbagam_paints.senbagam_paints.custom.py.sales_invoice.vlidate_sales_order",
			# "senbagam_paints.senbagam_paints.custom.py.sales_invoice.update_sales_person"
        ]
	},
	'Employee':{
		'after_insert':"senbagam_paints.senbagam_paints.custom.py.employee.create_sales_person",
		'validate':"senbagam_paints.senbagam_paints.custom.py.employee.validate"
	},
	"Company":{
		"after_insert":"senbagam_paints.senbagam_paints.custom.py.company.after_insert",
		'validate':"senbagam_paints.senbagam_paints.custom.py.company.validate"
	},
	"Stock Reconciliation":{
		"validate":"senbagam_paints.senbagam_paints.custom.py.stock_reconcilation.validate_qty"
	},
	'Sales Order':{
		'validate':"senbagam_paints.senbagam_paints.custom.py.sales_order.validate"
	}
	# 'Sales Order':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.sales_order'
	# },
	# 'Delivery Note':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.delivery_note'
	# },	
	# 'Quotation':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.quotation'
	# },	
	# 'Purchase Order':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.purchase_order'
	# },	
	# 'Purchase Receipt':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.purchase_receipt'
	# },	
	# 'Purchase Invoice':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.purchase_invoice'
	# },	
	# 'Journal Entry':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.journal_entry'
	# },
	# 'Payment Entry':{
	# 	'autoname':'senbagam_paints.senbagam_paints.custom.py.naming.payment_entry'
	# },
}

# Scheduled Tasks
# ---------------
# boot_session = ["senbagam_paints.senbagam_paints.migrate.create_company_type.create_session_default_for_company"]
scheduler_events = {
	# "all": [
	# 	"senbagam_paints.tasks.all"
	# ],
	# "daily": [
	# 	"senbagam_paints.tasks.daily"
	# ],
	# "hourly": [
	# 	"senbagam_paints.tasks.hourly"
	# ],
	# "weekly": [
	# 	"senbagam_paints.tasks.weekly"
	# ],
	# "monthly": [
	# 	"senbagam_paints.tasks.monthly"
	# ],
    "cron": {
		"55 5 * * *": [
			"senbagam_paints.senbagam_paints.custom.py.notification.morning",
		],
	},
}

# Testing
# -------

# before_tests = "senbagam_paints.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "senbagam_paints.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "senbagam_paints.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["senbagam_paints.utils.before_request"]
# after_request = ["senbagam_paints.utils.after_request"]

# Job Events
# ----------
# before_job = ["senbagam_paints.utils.before_job"]
# after_job = ["senbagam_paints.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"senbagam_paints.auth.validate"
# ]
