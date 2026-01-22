// Copyright (c) 2026, Faris and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Transaction", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Transaction',{
    type: function(frm){
        toggle_issue_date(frm);
    },
    refresh: function(frm){
        toggle_issue_date(frm);
        setFilter(frm)
    }
});
function toggle_issue_date(frm){
    if(frm.doc.type == "Return"){
        frm.set_df_property("issue_date","read_only",1);
    }
    else{
        frm.set_df_property("issue_date","read_only",0);
    }
}
frappe.ui.form.on('Library Transaction', {

    library_member(frm) {
        apply_article_filter(frm);
    },

    refresh(frm) {
        apply_article_filter(frm);
    },

    type(frm) {
        apply_article_filter(frm);
    }
});


function apply_article_filter(frm) {

    if (!frm.doc.library_member || frm.doc.type !== "Issue") return;

    frm.set_query("article", function () {
        return {
            query: "library_managementapp.library_managementapp.doctype.library_transaction.library_transaction.get_articles_for_member",
            filters: {
                library_member: frm.doc.library_member
            }
        };
    });
}


function setFilter(frm){
    frm.set_query("article",function(){
        if(frm.doc.type=="Issue"){
            return{
                filters:{
                    status:"Available"
                }
            };
        }
        else if(frm.doc.type=="Return"){
            return{
                filters:{
                    status:"Issued"
                }
            }
        }
        return {};
    });
}
