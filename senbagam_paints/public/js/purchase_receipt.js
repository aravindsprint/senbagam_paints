frappe.ui.form.on('Purchase Receipt',{
    refresh:function(frm,cdt,cdn){
        setTimeout(()=>{
        frm.remove_custom_button('Make Stock Entry', "Create");
        frm.remove_custom_button('Retention Stock Entry', "Create");
        frm.remove_custom_button('Subscription', "Create");       
    },550)

    },
})