
frappe.ui.form.on('Delivery Note',{
    
    refresh: function(frm){
        setTimeout(()=>{
            frm.remove_custom_button('Quality Inspection(s)', "Create"); 
            frm.remove_custom_button('Packing Slip', "Create");       
        },550)

        let without_serial=0;
        console.log(without_serial)
        console.log(frm.doc.company)
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            console.log(r.company_type)
            frappe.db.get_value('Company Type', r.company_type, 'sales', (value) => {
                
                without_serial=value.sales;
                console.log(without_serial)
                
                if (without_serial==0&&frm.is_new()){
                    frm.doc.items.forEach(d=>{
                        console.log(d)
                        frappe.model.set_value(d.doctype, d.name, "batch_no", "")
                    });    
                    
                }
            
            });
        });

       
    },
    onload:function(frm){
        
    }
})


frappe.ui.form.on('Delivery Note Item', {

item_code(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    let without_serial=0;
        frappe.db.get_value('Company', frm.doc.company, 'company_type', (r) => { 
				
            frappe.db.get_value('Company Type', r.company_type, 'sales', (value) => {
                
                without_serial=value.sales;
                
                if (without_serial==0&&frm.is_new()){
                   console.log(without_serial)
                        frappe.model.set_value(row.doctype, row.name, "batch_no", "")
                        frappe.model.set_value(row.doctype, row.name, "serial_no", "")
                 
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
                    console.log(without_serial)
                    console.log("gfffffffffffffffffffff")
                        frappe.model.set_value(row.doctype, row.name, "batch_no", "")
                   
                   
                        
                    
                }
            
            });
        });
    }


})