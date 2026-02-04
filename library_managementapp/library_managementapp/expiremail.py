import frappe
from frappe.utils import add_days, nowdate

def send_memb_exp():
    today=nowdate()
    reminder_date=add_days(today,3)

    membership=frappe.get_all(
        "Library Memebership",
        filters={
            "end_date": reminder_date,
            "docstatus": 1
        },
        fields=["name","library_member"]
    )
    for m in membership:
        send_email(m.library_member)

def send_email(member_name):
    member=frappe.get_doc("Library Member",member_name)

    if not member.email:
        return
    subject="Library Membership Expiry"
    message=f"""
    Hello {member.first_name},

    Your library membership will expire soon.
    Please renew it to continue borrowing books.

    Thank you,
    Library Team
    """
    frappe.sendmail(
        recipients=[member.email],
        subject=subject,
        message=message
    )

