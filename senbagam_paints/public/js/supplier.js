frappe.ui.form.on('Supplier',{
    refresh:function(frm,cdt,cdn){
       
        setTimeout(()=>{
        frm.remove_custom_button('Get Supplier Group Details', "Actions");
        frm.remove_custom_button('Pricing Rule', "Create");
      
       
       
           },550)

    },
})