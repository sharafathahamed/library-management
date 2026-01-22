import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import date_diff, nowdate

class LibraryTransaction(Document):
    def before_validate(self):
        if not self.due_date and self.issue_date:
            self.due_date=frappe.utils.add_days(self.issue_date,7)
    
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            has_membership=self.validate_membership()
            self.validate_maximum_limit()
            if not has_membership:
                self.wallet_validation_check()
                self.amount_deduct_check()
            
        elif self.type == "Return":
            self.validate_return()
            self.calculate_penalty()

    def on_submit(self):
        self.update_article_status()

        
    def update_article_status(self):
        article = frappe.get_doc("Article", self.article)

        if self.type == "Issue":
            if article.number_of_available_books <= 0:
                frappe.throw("No books available")

            article.number_of_available_books -= 1

        elif self.type == "Return":
            if article.number_of_available_books >= article.custom_total_books:
                frappe.throw("All books are already returned")

            article.number_of_available_books += 1

        if article.number_of_available_books == 0:
            article.status = "Issued"
        else:
            article.status = "Available"

        article.save(ignore_permissions=True)


    def wallet_validation_check(self):
        wallet = frappe.get_doc(
            "Wallet",
            {"library_member":self.library_member}
        )
        if wallet.status!="Active":
            frappe.throw("This is no longer active")

        article=frappe.get_doc("Article",self.article)
        amount=article.price

        if wallet.wallet_amount < amount:
            frappe.throw("Insufficient wallet balance")       
        
    def amount_deduct_check(self):
        wallet=frappe.get_doc(
        "Wallet",
        {"library_member":self.library_member}
        )
        article=frappe.get_doc("Article",self.article)
        amount=article.price
        wallet.wallet_amount -= amount
        wallet.save()

    def validate_issue(self):
        exists=frappe.db.exists("Library Transaction",{
            "library_member":self.library_member,
            "article":self.article,
            "type":"Issue",
            "docstatus":1
        })
        if exists:
            frappe.throw("Already issued. pl.return")
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        if article.status == "Issued" or article.number_of_available_books <= 0:
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        if article.status == "Available" and article.number_of_available_books >= article.custom_total_books:
            frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {
                "library_member": self.library_member,
                "type": "Issue",
                "docstatus": DocStatus.submitted(),
            },
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<=", self.issue_date),
                "to_date": (">=", self.issue_date),
            },
        )
        return bool(valid_membership)
    def calculate_penalty(self):
        self.return_date=nowdate()
        wallet=frappe.get_doc(
            "Wallet",
            {"library_member":self.library_member}
        )
        if self.due_date and self.return_date>self.due_date:
            
            delay=date_diff(self.return_date,self.due_date)
            self.delay_days=delay

            fine_per_day = frappe.db.get_single_value(
                "Library Settings", "fine_per_day"
            )
            self.penalty_amount=delay*fine_per_day
            wallet.wallet_amount-=self.penalty_amount
        else:
            self.delay_days=0
            self.penalty_amount=0

@frappe.whitelist()
def get_articles_for_member(doctype, txt, searchfield, start, page_len, filters):

    member = filters.get("library_member")

    return frappe.db.sql("""
        SELECT
            a.name, a.article_name
        FROM `tabArticle` a
        WHERE
            a.number_of_available_books > 0

        AND a.name NOT IN (
            SELECT lt.article
            FROM `tabLibrary Transaction` lt
            WHERE
                lt.library_member = %(member)s
                AND lt.type = 'Issue'
                AND lt.docstatus = 1
        )
        LIMIT %(page_len)s OFFSET %(start)s
    """, {
        "member": member,
        "page_len": page_len,
        "start": start
    })
