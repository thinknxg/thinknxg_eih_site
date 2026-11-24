import frappe
from frappe import _
from frappe.rate_limiter import rate_limit

FIELDS = ("full_name", "business_email", "company", "country", "erp_system", "required_compliance",
          "existing_asp", "invoice_volume", "message")


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=8, seconds=3600)
def submit_enquiry(**kwargs):
	"""Guest endpoint for the E-Invoice Hub landing page form. Server-side validation lives in the DocType."""
	if (kwargs.get("website_url") or "").strip():  # honeypot
		return {"ok": True}
	data = {k: (kwargs.get(k) or "") for k in FIELDS}
	for k, v in data.items():
		if not isinstance(v, str):
			frappe.throw(_("Invalid submission."))
	doc = frappe.get_doc({"doctype": "E-Invoice Hub Enquiry", **data, "consent": 1 if kwargs.get("consent") else 0,
		"source_page": (kwargs.get("source_page") or "")[:140], "ip_address": frappe.local.request_ip})
	doc.insert(ignore_permissions=True)
	try:
		frappe.sendmail(recipients=[frappe.conf.get("eih_enquiry_recipient") or "sales@kreatao.com"],
			subject=f"New E-Invoice Hub enquiry: {doc.company}", message=f"{doc.full_name} ({doc.business_email}) - {doc.required_compliance}. See {doc.name}.", now=False)
	except Exception:
		frappe.log_error("EIH enquiry notification failed")
	return {"ok": True}
