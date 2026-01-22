from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
import frappe

class LibraryMembership(Document):
    def before_save(self):
        self.validate_existing_member()
        self.setMembAmount()
        self.validate_balance()
        self.deduct_amount()
        self.set_date()
    def validate_existing_member(self):
        exists=frappe.db.exists(
            "Library Membership",
            {
                "library_member":self.library_member,
                "docstatus":DocStatus.submitted(),
                "to_date":(">=",self.from_date),
            },
        )
        if exists:
            frappe.throw("This member already has an active membership.")

    def setMembAmount(self):
        if self.membership_plans=="1 month":
            self.amount=120
            self.duration_days=30
        elif self.membership_plans=="3 months":
            self.amount=300
            self.duration_days=90
        elif self.membership_plans=="1 year":
            self.amount=1000
            self.duration_days=365
        else:
            frappe.throw("Invalid membership plan selected")

    def validate_balance(self):
        wallet=frappe.get_doc(
            "Wallet",
            {"library_member":self.library_member}
        )
        if wallet.status!="Active":
            frappe.throw("Wallet is not active")
        if wallet.wallet_amount<self.amount:
            frappe.throw("Insufficient Balance")
        
    def deduct_amount(self):
        wallet=frappe.get_doc(
            "Wallet",
            {"library_member":self.library_member}
        )
        wallet.wallet_amount-=self.amount
        wallet.save()
    def set_date(self):
        self.to_date=frappe.utils.add_days(self.from_date,self.duration_days)