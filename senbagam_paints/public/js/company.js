frappe.ui.form.on('Company', {
    
	qr_content: function(frm) {
       
		frm.set_df_property("qr", "options", '<img src="https://barcode.tec-it.com/barcode.ashx?data={{ frm.doc.qr_content }}&code=QRCode">');
		frm.refresh();
		
	},
	refresh: function(frm) {
		// if(!frm.doc.custom_updated_tax_template && !frm.doc.__islocal){
		// 	frm.add_custom_button(__("Update Item Tax Template"), () => {
		// 		frappe.call({
		// 			'method':"senbagam_paints.senbagam_paints.custom.py.company.update_item_tax_table",
		// 			"args":{
		// 				doc:frm.doc.name
		// 			},
		// 			callback:function(res){
		// 				frm.set_value('custom_updated_tax_template',1)
		// 				frm.save()
		// 			}
		// 		})
		// 	},("Manage"));
		// }


		frm.set_df_property("qr", "options", '<img src="https://barcode.tec-it.com/barcode.ashx?data={{ frm.doc.qr_content }}&code=QRCode">');
		// if(frm.doc.company_type != 'Parent' && !frm.doc.custom_company_mode_of_payment.length && !frm.doc.__islocal){
		// 	frm.set_value('custom_company_mode_of_payment',[])
		// 	frappe.db.get_list('Mode of Payment',{fields:['name']}).then((r)=>{
		// 		r.forEach(element => {
		// 			let child = frm.add_child('custom_company_mode_of_payment')
		// 			child.mode_of_payment = element.name
					
		// 			frm.refresh_field('custom_company_mode_of_payment')
		// 		});
		// 	})
		// }
		
		
	},
	setup:function(frm,cdt,cdn){
        // frm.set_query("account", "custom_company_mode_of_payment", () => {
		// 	return {
		// 		filters: {
		// 			company: frm.doc.name,
		// 		},
		// 	}
		// });
		
    }
});
