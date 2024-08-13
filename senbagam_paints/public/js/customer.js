frappe.ui.form.on('Customer', {
    refresh: function (frm, cdt, cdn) {
        setTimeout(() => {
            frm.remove_custom_button('Pricing Rule', "Create");
            frm.remove_custom_button('Get Customer Group Details', "Actions");
            //frm.set_value("enter_otp",'')
            if (frm.doc.convert_to_painter){
                frm.set_df_property('enter_otp', 'hidden', 1);
                frm.set_df_property('send_otp', 'hidden', 1);
            }

        }, 550)
        frm.set_query("custom_franchise", function() {
            return {
                filters: {
                    'is_group':0,
                }
            };
        });
    },
    send_otp:  function (frm) {
        frappe.call({
            method: 'senbagam_paints.senbagam_paints.custom.py.customer.otpgen',
            args: {
                customer: frm.doc.name,
                mobileno: frm.doc.otp_mobile_no
            },
            callback: async function (r) {
                if (r.message) {
                    frm.doc.original_otp = r.message[0]
                    frm.doc.enter_otp = ''
                    frm.refresh_field('original_otp');
                    frm.save()
                    if (r.message[1]){
                        frappe.show_alert({message: 'OPT Sent to Mobile Number', indicator: 'green' });}
                }
            }
        });
    },
    qr_code_scanned: function (frm) {
        if (frm.doc.qr_code_scanned) {
            frm.set_value("otp_mobile_no", frm.doc.mobile_no)
        }
    },
    verify_otp: async function (frm) {
        if (frm.doc.enter_otp) {
            if (frm.doc.original_otp != frm.doc.enter_otp) {
                frappe.throw(__("OTP Not Matched, Please Try Again"));
            }
            else {
                frappe.call({
                    method: 'senbagam_paints.senbagam_paints.custom.py.customer.painter_conversion_email',
                    args: {
                        "doc": frm.doc
                    },
                    callback: await function (r) {
                        if (r.message == true) {
                            frm.set_df_property('enter_otp', 'hidden', 1);
                            frm.set_df_property('otp_mobile_no', 'read_only', 1);
                            frm.doc.mail_send = 1
                            frm.refresh_field('mail_send');
                            frm.save()
                            frappe.show_alert({message: "Painter Conversion Approval Send To Admin", indicator: 'green' })
                        }
                    }
                });
            }
        }
    }
});