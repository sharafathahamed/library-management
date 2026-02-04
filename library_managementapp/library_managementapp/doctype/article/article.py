import frappe
from frappe.model.document import Document


class Article(Document):
    def validate(self):
        self.validate_isbn()
        self.set_default_available_books()
    def set_default_available_books(self):
        if self.custom_total_books and not self.number_of_books_available:
            self.number_of_books_available = self.custom_total_books
    def validate_isbn(self):
        isbn = self.isbn
        if not isbn:
            frappe.throw("Please enter ISBN")
        if not isbn.isdigit():
            frappe.throw("ISBN must contain only digits")
        if len(isbn) != 20:
            frappe.throw("ISBN must be exactly 20 digits")
