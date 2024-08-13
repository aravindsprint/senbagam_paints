frappe.ui.form.on('Purchase Order',{
    refresh:function(frm,cdt,cdn){
        setTimeout(()=>{
        frm.remove_custom_button('Subscription', "Create");
        frm.remove_custom_button('Payment Request', "Create");
           },550)

    },
})