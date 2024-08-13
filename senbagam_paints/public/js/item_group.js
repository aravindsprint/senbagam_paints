frappe.ui.form.on('Item Group', {
	refresh: function(frm) {
		if(! frm.doc.__islocal){
			frm.add_custom_button(__('Update Mobile App Field'), function(){
				frappe.confirm(
					'Are you sure? '+frm.doc.name+'</b>.',
					function(){
						frappe.call({
							args:{
								mobile_field: frm.doc.show_in_mobile_app,
								item_group: frm.doc.name
							},
							method: 'senbagam_paints.senbagam_paints.custom.py.item.update_mobile_app_field_in_item_master',
							callback: function(r) {
								if(r.message){
									frappe.show_alert(__('Item updated'));
								}
							}
						});
					}
				);
			});
		}
	}
});