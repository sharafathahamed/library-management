// Copyright (c) 2026, Faris and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Member", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Member',{
    refresh: function(frm){
        frm.add_custom_button('Calculate transaction count', ()=> {
            frappe.call({
                method: "library_managementapp.library_managementapp.api.count_job",
                args:{
                    member:frm.doc.name
                },
                callback(){
                    frappe.msgprint("Background job start. Pl.refresh");
                }
            });
        });
        frm.add_custom_button('Create Transaction', () => {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            })
        })
    }
})