import frappe

def library_member_condition(user):
    if "System Manager" in frappe.get_roles(user) or "Librarian" in frappe.get_roles(user):
        return ""
    member = frappe.db.get_value("Library Member",{"email_address":user},"name")
    if "Library Member" in frappe.get_roles(user):
        if not member:
            return "1=0"
        return f"`tabLibrary Member`.name='{member}'"
    return "1=0"
def library_transaction_condition(user):
    if "System Manager" in frappe.get_roles(user) or "Librarian" in frappe.get_roles(user):
        return None
    member = frappe.db.get_value("Library Member",{"email_address":user},"name")
    if not member:
        return "1=0"
    return f"`tabLibrary Transaction`.library_member='{member}'"