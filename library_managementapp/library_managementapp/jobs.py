import frappe

def update_transac_count(member):
    count = frappe.db.count(
        "Library Transaction",
        {"library_member": member}
    )
    frappe.db.set_value(
        "Library Member",
        member,
        "total_transaction",
        count
    )
    frappe.db.commit()
    frappe.logger().info(f"Updated transaction for {member}: {count}")
