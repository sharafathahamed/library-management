import frappe
from frappe.model.document import Document


class Article(Document):

    def validate(self):
        if not self.number_of_available_books:
            self.number_of_available_books = self.custom_total_books
        self.validate_isbn()
    def validate_isbn(self):
        isbn=self.isbn
        if not isbn.isdigit():
            frappe.throw("andha error")
        if len(isbn)!=20:
            frappe.throw("indha error")
        if not isbn:
            frappe.throw("Pl. Enter idbn")