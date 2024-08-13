// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Value Based Discount Settings', {
	image: function(frm) {
		
		frappe.call({
            method: "senbagam_paints.senbagam_paints.doctype.sales_value_based_discount_settings.sales_value_based_discount_settings.img_preview",
            args: {
                "image": frm.doc.image,
              
            },
            callback: function (r) {
               frm.set_df_property("image_preview","options",r.message)
            },
        })
	}
});

frappe.ui.form.on('Franchise To User', {
    

	start_amount: function(frm, cdt, cdn) {

        var data = locals[cdt][cdn]

		if (data.start_amount){

            if(data.start_amount < data.upto || !data.upto){

                frappe.call({
                    method: "senbagam_paints.senbagam_paints.doctype.sales_value_based_discount_settings.sales_value_based_discount_settings.table_data_validation",
                    args: {
                        "tabel_rows": frm.doc.franchise_to_user,
                        "enter_value": data.start_amount,
                        "enter_idx": data.idx

                    
                    },

                    callback: function (r) {
                        
                        if(r.message){
                            frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.start_amount + "</b> Is Already Given In The Row <b style = 'color: #7752FE'>" + r.message + "</b>.")
                            frappe.model.set_value(cdt, cdn, "start_amount", 0)
                        }
                    
                    }
                })
            }

            else{
                frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.start_amount + "</b> Must Be Less Than The <b style = 'color: #7743DB'>" + data.upto + "</b> In The Row <b style = 'color: #7752FE'>" + data.idx + "</b>.")
                frappe.model.set_value(cdt, cdn, "start_amount", 0)
            }
        }
	},

    upto: function(frm, cdt, cdn) {

		var data = locals[cdt][cdn]

		if (data.upto){

            if(data.upto > data.start_amount || !data.start_amount){

                frappe.call({
                    method: "senbagam_paints.senbagam_paints.doctype.sales_value_based_discount_settings.sales_value_based_discount_settings.table_data_validation",
                    args: {
                        "tabel_rows": frm.doc.franchise_to_user,
                        "enter_value": data.upto,
                        "enter_idx": data.idx
                    },

                    callback: function (r) {
                        
                        if(r.message){
                            frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.upto + "</b> Is Already Given In The Row <b style = 'color: #7752FE'>" + r.message + "</b>.")
                            frappe.model.set_value(cdt, cdn, "upto", 0)
                        }
                    
                    }
                })
            }

            else{
                frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.upto + "</b> Must Be Greater Than The <b style = 'color: #7743DB'>" + data.start_amount + "</b> In The Row <b style = 'color: #7752FE'>" + data.idx + "</b>.")
                frappe.model.set_value(cdt, cdn, "upto", 0)
            }
        }
	}
});


frappe.ui.form.on('Parent To Franchise', {
	start_amount: function(frm, cdt, cdn) {

        var data = locals[cdt][cdn]

		if (data.start_amount){

            if(data.start_amount < data.upto || !data.upto){

                frappe.call({
                    method: "senbagam_paints.senbagam_paints.doctype.sales_value_based_discount_settings.sales_value_based_discount_settings.table_data_validation",
                    args: {
                        "tabel_rows": frm.doc.parent_to_franchise,
                        "enter_value": data.start_amount,
                        "enter_idx": data.idx

                    
                    },

                    callback: function (r) {
                        
                        if(r.message){
                            frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.start_amount + "</b> Is Already Given In The Row <b style = 'color: #7752FE'>" + r.message + "</b>.")
                            frappe.model.set_value(cdt, cdn, "start_amount", 0)
                        }
                    
                    }
                })
            }

            else{
                frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.start_amount + "</b> Must Be Less Than The <b style = 'color: #7743DB'>" + data.upto + "</b> In The Row <b style = 'color: #7752FE'>" + data.idx + "</b>.")
                frappe.model.set_value(cdt, cdn, "start_amount", 0)
            }
        }
	},

    upto: function(frm, cdt, cdn) {
        
		var data = locals[cdt][cdn]

		if (data.upto){

            if(data.upto > data.start_amount || !data.start_amount){

                frappe.call({
                    method: "senbagam_paints.senbagam_paints.doctype.sales_value_based_discount_settings.sales_value_based_discount_settings.table_data_validation",
                    args: {
                        "tabel_rows": frm.doc.parent_to_franchise,
                        "enter_value": data.upto,
                        "enter_idx": data.idx

                    
                    },

                    callback: function (r) {
                        
                        if(r.message){
                            frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.upto + "</b> Is Already Given In The Row <b style = 'color: #7752FE'>" + r.message + "</b>.")
                            frappe.model.set_value(cdt, cdn, "upto", 0)
                        }
                    
                    }
                })
            }
            
            else{
                frappe.msgprint("Enter Value <b style = 'color: #39A7FF'>" + data.upto + "</b> Must Be Greater Than The <b style = 'color: #7743DB'>" + data.start_amount + "</b> In The Row <b style = 'color: #7752FE'>" + data.idx + "</b>.")
                frappe.model.set_value(cdt, cdn, "upto", 0)
            }
        }
	}
});