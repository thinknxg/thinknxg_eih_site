import re
import frappe
from frappe import _
from frappe.model.document import Document

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
FREE = {"mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com"}


class EInvoiceHubEnquiry(Document):
	def validate(self):
		for f in ("full_name", "company", "country", "erp_system", "existing_asp", "invoice_volume"):
			v = (self.get(f) or "").strip()
			if re.search(r"[<>]", v):
				frappe.throw(_("Invalid characters in {0}").format(self.meta.get_label(f)))
			self.set(f, v)
		if not EMAIL.match(self.business_email or ""):
			frappe.throw(_("Please enter a valid business email address."))
		if (self.business_email or "").rsplit("@", 1)[-1].lower() in FREE:
			frappe.throw(_("Please use your business email address."))
		if not self.consent:
			frappe.throw(_("Consent is required to submit the enquiry."))
		self.message = frappe.utils.strip_html_tags(self.message or "")[:2000]
