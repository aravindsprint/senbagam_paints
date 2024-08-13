// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
let item_details=[]
frappe.ui.form.on('Painter Commission', {
	refresh: function(frm){
		frm.set_value("scan_items", "");
        frm.set_query('painter', function(frm){
            return{
                filters:{
                    'customer_group':'Painters'
                }
            }
        })
    },
	
	scan_items:function(frm,cdt,cdn) {
		// const barcode_scanner = new erpnext.utils.BarcodeScanner({frm:frm});
		// barcode_scanner.process_scan();
		
			if(frm.doc.scan_items){
				// frm.doc.items.forEach(d=>{
				// 	if(d.serial_no==frm.doc.scan_items){
				// 		frappe.throw(__("This Serial No already Added"));
				// 	}
					
				// })
				let value=true;
				console.log("fdsfffffffffffffffffff")
				frappe.db.get_list("Painter Commission",
				{filters:[["Painter Commission Items","serial_no","like",frm.doc.scan_items]],
				fields:["`tabPainter Commission`.name"]}).then(scanned_serial => {
					(scanned_serial || []).forEach(data => {
						if(data){
							
							console.log(data)
							frm.doc.scan_items=""
							value=false;
							frappe.throw(__("This Serial No already Scanned in {0}",[ data["name"]]));
						}

					})})
					
					frappe.db.get_list("Sales Invoice",
						{filters:[["Sales Invoice Item","serial_no","like",frm.doc.scan_items],
						["Sales Invoice","painters","like",frm.doc.painter],
						["Sales Invoice","docstatus","not like",2]
					],
						fields:["`tabSales Invoice Item`.serial_no",
						"`tabSales Invoice Item`.item_code",
						"`tabSales Invoice Item`.parent"]})
						.then(invoice_details => {
							
							(invoice_details || []).forEach(data => {
								if(value==true){
									(frm.doc.items||[]).forEach(d=>{
										if(d.serial_no==frm.doc.scan_items){
												frappe.throw(__("This Serial No already Added"));
										}
									})
									item_details.push(data)
								var child = frm.add_child('items')
								child.invoice_no=data.parent
								child.item=data.item_code
								child.serial_no=data.serial_no
								}
								
								
							})
							// frm.set_value("scan_items", "");
							frm.refresh();
							(frm.doc.items || []).forEach(d=>{
								
									frappe.db.get_value('Item', d.item, 'custom_painter_commision', (value) => {
										let commission=value.custom_painter_commision;
										if(commission){
										console.log(d)
										frappe.model.set_value(d.doctype, d.name, "painter_commission", commission)
										}
				
									})
							
								// else{
								
								// }
							})
					
					}
					)
			
				}
	},
});

let total_commission_rate=0
frappe.ui.form.on("Painter Commission Items", {
    painter_commission: function (frm, cdt, cdn) {
		let data=locals[cdt][cdn];
		
		if(data.painter_commission){
			total_commission_rate+=data.painter_commission
			
			frm.set_value("total_commission_rate", total_commission_rate);

		}

       
    },
   
})
