
frappe.ui.form.on('Sales Invoice',{
    setup: function(frm) {
		frm.set_query("painters", function(doc) {
			return {
				filters: {
					customer_group: "Painters"
					
                }
			}
		});
	},
    
    refresh: function(frm,cdt,cdn){
        frm.set_query("customer", function() {
            return {
                query: "senbagam_paints.senbagam_paints.custom.py.sales_invoice.get_customer",
                filters:{"company":frm.doc.company}
            };
		});
        setTimeout(()=>{
           
         
        frm.remove_custom_button(__("Fetch Timesheet"))
        frm.remove_custom_button('Quality Inspection(s)', "Create");
        frm.remove_custom_button('Dunning', "Create");
        frm.remove_custom_button('Maintenance Schedule', "Create");
        frm.remove_custom_button('Subscription', "Create");
        frm.remove_custom_button('Invoice Discounting', "Create");
        frm.remove_custom_button('Payment Request', "Create");
           },550)
        
        let without_serial=0;
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            frappe.db.get_value('Company Type', r.company_type, 'sales', (value) => {
                
                without_serial=value.sales;
                
                if (without_serial==0&&frm.is_new()){
                    frm.doc.items.forEach(d=>{
                        frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                    });
                   
                        
                    
                }
            
            });
        });

        for (var i in frm.doc.items) {
			var item = cur_frm.doc.items[i];
			if(item.delivery_note&&frm.is_new()) {
				frm.set_value('update_stock', 0);
                // frm.doc.items.forEach(d=>{
                //     console.log(d)
                //     frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                //     frappe.model.set_value(d.doctype, d.name, "serial_no", "")
                // });
			} 
		}
        
    },
   
})


frappe.ui.form.on('Sales Invoice Item', {

item_code(frm,cdt,cdn){
    
    let row=locals[cdt][cdn]
    let without_serial=0;
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            frappe.db.get_value('Company Type', r.company_type, 'sales', (value) => {
                
                without_serial=value.sales;
                
                if (without_serial==0&&frm.is_new()){
                        frappe.model.set_value(row.doctype, row.name, "batch_no", "")
                   
                   
                   
                        
               
                   
                        
                    
                }
            
            });
        });
},
batch_no(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    let without_serial=0;
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            frappe.db.get_value('Company Type', r.company_type, 'sales', (value) => {
                
                without_serial=value.sales;
                
                if (without_serial==0&&frm.is_new()){
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