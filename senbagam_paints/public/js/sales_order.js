frappe.ui.form.on('Sales Order',{
    refresh:function(frm,cdt,cdn){
        frm.set_query("customer", function() {
            return {
                query: "senbagam_paints.senbagam_paints.custom.py.sales_invoice.get_customer",
                filters:{"company":frm.doc.company}
            };
		});
        setTimeout(()=>{
        frm.remove_custom_button('Pick List', "Create");
        frm.remove_custom_button('Work Order', "Create");
        frm.remove_custom_button('Material Request', "Create");
        frm.remove_custom_button('Request for Raw Materials', "Create");
        frm.remove_custom_button('Project', "Create");
        frm.remove_custom_button('Subscription', "Create");
        frm.remove_custom_button('Payment Request', "Create");
        frm.remove_custom_button('Work Order', "Create");
       
           },550)

    },
})