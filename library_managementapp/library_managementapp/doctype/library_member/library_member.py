import frappe
from frappe.model.document import Document

class LibraryMember(Document):
    def before_naming(self):
        self.full_name = f"{self.first_name} {self.last_name or ''}".strip()
    def after_insert(self):
        self.send_mail_html()
        self.create_user()
    def create_user(self):
        if not self.email_address:
            return
        if frappe.db.exists("User", self.email_address):
            return
        user=frappe.new_doc("User")
        user.email=self.email_address
        user.first_name=self.full_name
        user.send_welcome_email=1
        user.enabled=1
        user.append("roles",{
            "role":"Library Member"
		})
        user.insert(ignore_permissions=True)
    
    def send_mail_html(self):
        if not self.email_address:
            return
        link = frappe.utils.get_url(f"/app/library-member/{self.name}")
        member_name = self.full_name
        message = f"""
		<div style="font-family: Arial, sans-serif; background:#0f172a; padding:30px;">
		<div style="max-width:600px; margin:auto; background:#020617; border-radius:12px; padding:30px; color:#e5e7eb;">

			<h1 style="color:#22c55e; text-align:center;">📚 Welcome to Smart Library</h1>

			<p style="font-size:16px;">Hi <b>{member_name}</b>,</p>

			<p style="font-size:15px; line-height:1.6;">
			Your library membership has been successfully created.  
			You can now explore, borrow, and manage your books anytime from your dashboard.
			</p>

			<div style="text-align:center; margin:30px 0;">
			<a href="{link}"
				style="background:#22c55e; color:#020617; padding:14px 26px;
						text-decoration:none; border-radius:8px; font-weight:bold;">
				👉 View My Library Profile
			</a>
			</div>

			<p style="font-size:14px; color:#9ca3af;">
			Tip: Keep your membership active to continue borrowing books without interruption.
			</p>

			<hr style="border:none; border-top:1px solid #1e293b; margin:25px 0;">

			<p style="font-size:12px; color:#64748b; text-align:center;">
			Smart Library Management System © 2026<br>
			Built for seamless learning 📖
			</p>

		</div>
		</div>
		"""

        frappe.sendmail(
            recipients=[self.email_address],
            subject="Welcome to Library",
            message=message
        )
