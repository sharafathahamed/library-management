import frappe


def execute(filters=None):
    if not filters:
        filters = {}

    conditions = []
    values = {}

    if filters.get("library_member"):
        conditions.append("lt.library_member = %(library_member)s")
        values["library_member"] = filters.get("library_member")

    if filters.get("article"):
        conditions.append("lt.article = %(article)s")
        values["article"] = filters.get("article")

    if filters.get("transaction_type"):
        conditions.append("lt.type = %(transaction_type)s")
        values["transaction_type"] = filters.get("transaction_type")

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            lt.library_member,
            lm.full_name,
            lt.article,
            lt.type AS transaction_type,
            lt.date AS transaction_date
        FROM `tabLibrary Transaction` lt
        LEFT JOIN `tabLibrary Membership` lm
            ON lm.library_member = lt.library_member
        {where}
        ORDER BY lt.date DESC
    """

    columns = [
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 180,
        },
        {
            "label": "Full Name",
            "fieldname": "full_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Article",
            "fieldname": "article",
            "fieldtype": "Link",
            "options": "Article",
            "width": 180,
        },
        {
            "label": "Transaction Type",
            "fieldname": "transaction_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Transaction Date",
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "width": 130,
        },
    ]

    data = frappe.db.sql(query, values, as_dict=True)
    return columns, data
