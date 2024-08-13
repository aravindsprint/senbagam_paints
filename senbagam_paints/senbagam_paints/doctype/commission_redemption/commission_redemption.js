// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Commission Redemption', {
	// refresh: function(frm) {
		
	// },
	setup: function(frm) {
		frm.set_query("painter", function(doc) {
			return {
				filters: {
					customer_group: "Painters"
					
                }
			}
		});
	},
		loyalty_points_cash:function(frm,cdt,cdn) {
			
			if(frm.doc.loyalty_points_cash && frm.doc.painter){
				frappe.call({
					method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.total_loyalty_points",
					args:{
						"painter":frm.doc.painter
						},
					callback:function(r){
						
						frm.set_value("total_loyalty_points_earned",r.message)
					}
				})
				
		}
	},
		painter_commission:function(frm,cdt,cdn) {
				
			if(frm.doc.painter_commission && frm.doc.painter){
				frappe.call({
					method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.total_commission_points",
					args:{
						"painter":frm.doc.painter
						},
					callback:function(r){
						
						frm.set_value("total_commission_points",r.message)
					}
				})
				
		}
		},
		painter:function(frm,cdt,cdn){
			console.log(frm.doc.painter_commission)
			if(frm.doc.loyalty_points_cash && frm.doc.painter){
				frappe.call({
					method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.total_loyalty_points",
					args:{
						"painter":frm.doc.painter
						},
					callback:function(r){
						
						frm.set_value("total_loyalty_points_earned",r.message)
					}
				})
				if(frm.doc.painter_commission && frm.doc.painter){
					
					frappe.call({
						method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.total_commission_points",
						args:{
							"painter":frm.doc.painter
							},
						callback:function(r){
							
							frm.set_value("total_commission_points",r.message)
						}
					})
				}
				
		}

		},
	
	points_do_redemption:function(frm){
		console.log(frm.doc.points_do_redemption)
		if(frm.doc.points_do_redemption==0){
			frappe.throw({
				message: __("Redemption Amount is Zero"),
				title: __("Note")
			});
		}
		if(frm.doc.points_do_redemption)
		{
			
			if(frm.doc.painter_commission &&frm.doc.points_do_redemption > frm.doc.total_commission_points ){
				
				frappe.throw({
					message: __("Redemption Amount is Greater Than Total Commission Rate."),
					title: __("Note")
				});
			}
			else if(frm.doc.loyalty_points_cash &&frm.doc.points_do_redemption >  frm.doc.total_loyalty_points_earned ){
				
				frappe.throw({
					message: __("Redemption Amount is Greater Than Total Points."),
					title: __("Note")
				});
			}
			else if(frm.doc.loyalty_points_cash &&frm.doc.total_loyalty_points_earned){
				frappe.call({
					method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.tds_percentage",
					args:{
						"amount":frm.doc.points_do_redemption ,
						"total_points":frm.doc.total_loyalty_points_earned

					},
					callback:function(r){
						console.log(r.message)
						if(r.message){
							frm.set_value("available_points_after_tds",r.message || 0)
						}
						
					}
				})

			}
			else if(frm.doc.painter_commission &&frm.doc.total_commission_points){
					
				frappe.call({
					method:"senbagam_paints.senbagam_paints.doctype.commission_redemption.commission_redemption.tds_percentage",
					args:{
						"amount":frm.doc.points_do_redemption ,
						"total_points":frm.doc.total_commission_points 

					},
					callback:function(r){
						console.log(r.message)
						if(r.message){
							frm.set_value("available_points_after_tds",r.message || 0)
						}
						
					}
				})
			}
			
		}

	}
});
