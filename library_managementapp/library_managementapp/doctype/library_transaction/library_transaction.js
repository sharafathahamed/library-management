// Copyright (c) 2026, Faris and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Transaction', {

    refresh(frm) {
        toggle_issue_date(frm);
        apply_article_filter(frm);
    },
    type(frm) {
        toggle_issue_date(frm);
        apply_article_filter(frm);
    },

    library_member(frm) {
        apply_article_filter(frm);
    }
});

function toggle_issue_date(frm){
    if(frm.doc.type === "Return"){
        frm.set_df_property("issue_date", "read_only", 1);
    }
    else{
        frm.set_df_property("issue_date", "read_only", 0);
    }
}

function apply_article_filter(frm) {

    // Apply filter ONLY for Issue
    if (!frm.doc.library_member || frm.doc.type !== "Issue") {
        frm.set_query("article", () => ({}));
        return;
    }

    frm.set_query("article", function () {
        return {
            query: "library_managementapp.library_managementapp.doctype.library_transaction.library_transaction.get_articles_for_member",
            filters: {
                library_member: frm.doc.library_member
            }
        };
    });
}
