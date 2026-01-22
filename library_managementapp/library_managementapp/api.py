import frappe 

@frappe.whitelist()
def count_job(member):
    frappe.enqueue(
        "library_managementapp.library_managementapp.jobs.update_transac_count",
        member = member,
        queue="long"
    )
    