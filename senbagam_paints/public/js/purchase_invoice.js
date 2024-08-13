
frappe.ui.form.on('Purchase Invoice',{
    
    refresh: function(frm){
        setTimeout(()=>{
            frm.remove_custom_button('Quality Inspection(s)', "Create");
            frm.remove_custom_button('Payment Request', "Create");
            frm.remove_custom_button('Subscription', "Create");   
            frm.remove_custom_button('Block Invoice', "Create");       
        },550)
        let without_serial=0;
        console.log(without_serial)
        console.log(frm.doc.company)
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            console.log(r.company_type)
            frappe.db.get_value('Company Type', r.company_type, 'purchase', (value) => {
                
                without_serial=value.purchase;
                console.log(without_serial)
                
                if (without_serial==0&&frm.is_new()){
                    frm.doc.items.forEach(d=>{
                        console.log(d)
                        frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                    });    
                    
                }
            
            });
        });

        for (var i in frm.doc.items) {
			var item = cur_frm.doc.items[i];
			if(item.purchase_receipt&&frm.is_new()) {
				frm.set_value('update_stock', 0);
                // frm.doc.items.forEach(d=>{
                //     console.log(d)
                //     frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                //     frappe.model.set_value(d.doctype, d.name, "serial_no", "")
                // });
			} 
		}
        
    },
    onload:function(frm){
        
    }
})


frappe.ui.form.on('Purchase Invoice Item', {

item_code(frm,cdt,cdn){
    let d=locals[cdt][cdn]
    let without_serial=0;
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            frappe.db.get_value('Company Type', r.company_type, 'purchase', (value) => {
                
                without_serial=value.purchase;
                
                if (without_serial==0&&frm.is_new()){
                    
                        frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                        frappe.model.set_value(d.doctype, d.name, "serial_no", "")
                    
                }
            
            });
        });
},
serial_no(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    if(row.serial_no){
        frappe.db.get_value('Serial No', row.serial_no, 'batch_no', (value) => {
            console.log(value.batch_no)
            frappe.model.set_value(row.doctype, row.name, "batch_no", value.batch_no)

        });
    }
},
batch_no(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    let without_serial=0;
    frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
            
        frappe.db.get_value('Company Type', r.company_type, 'purchase', (value) => {
            
            without_serial=value.purchase;
            
            if (without_serial==0&&frm.is_new()){
                console.log(without_serial)
                    frappe.model.set_value(row.doctype, row.name, "batch_no", "")
                    
                
            }
        
        });
    });

},
serial_no(frm,cdt,cdn){
    let row=locals[cdt][cdn]
            frappe.db.get_value('Serial No', row.serial_no, 'warehouse', (value) => {
               let warehouse=value.warehouse;
                if (warehouse){
                        frappe.model.set_value(row.doctype, row.name, "warehouse", warehouse)
 
  
                }
            
        });

}

})