// Copyright (c) 2026, Faris and contributors
// For license information, please see license.txt
frappe.ui.form.on('Article',{
    isbn(frm){
        if(!frm.doc.isbn){
            frappe.msgprint("Enter ISBN");
        }
        else if(frm.doc.isbn.length()!=5){
            frappe.msgprint("Only 5 digits");
        }
        else if(!frm.doc.isbn.digits()){
            frappe.msgprint("please enter valid isbn only digits")
        }
    }
})