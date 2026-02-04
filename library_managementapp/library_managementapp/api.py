import frappe 

@frappe.whitelist()
def count_job(member):
    frappe.enqueue(
        "library_managementapp.library_managementapp.jobs.update_transac_count",
        member = member,
        queue="long"
    )
# @frappe.whitelist()
# def get_issued(member):
#     return frappe.get_all(
#         "Library Transaction",
#         filters={
#             "library_member":member,
#             "type":"Issue",
#             "docstatus":1,
#             "transaction_id":["is","not set"]
#         },
#         fields=["article","issue_date","name"]
#     )