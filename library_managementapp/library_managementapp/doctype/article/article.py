import frappe
from frappe.model.document import Document
class Article(Document):
    def validate(self):
        self.validate_isbn()
        self.set_default_available_books()

    def set_default_available_books(self):
        if self.number_of_available_books and not self.custom_total_books:
            self.custom_total_books = self.number_of_available_books

    def validate_isbn(self):
        isbn = self.isbn
        if not isbn:
            frappe.throw("Please enter ISBN")
        if not isbn.isdigit():
            frappe.throw("ISBN must contain only digits")
        if len(isbn) != 5:
            frappe.throw("ISBN must be exactly 5 digits")
