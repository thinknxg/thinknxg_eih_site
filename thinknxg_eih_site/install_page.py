"""Creates the thinkNXG E-Invoice Hub landing page in Frappe Builder.

Run:  bench --site <site> execute thinknxg_eih_site.install_page.run
Idempotent: only objects it owns are touched (tokens prefixed 'EIH ', scripts and the page named below).
It refuses to overwrite a different, pre-existing page that already uses the route.
"""
import json
import os

import frappe

HERE = os.path.dirname(__file__)
ROUTE = "E-InvoiceHub"
PAGE_NAME = "e-invoicehub"
TITLE = "thinkNXG E-Invoice Hub | UAE, Oman & Global Peppol E-Invoicing"
DESC = ("Discover thinkNXG E-Invoice Hub, a universal multi-country e-invoicing integration platform connecting thinkNXG ERP, ERPNext and enterprise systems with UAE PINT AE, Oman Fawtara and Peppol networks.")
CANON = "https://kreatao.com/E-InvoiceHub"
PALETTE = {"Navy": "#101C35", "Deep": "#163B70", "Elec": "#2878E5", "Cyan": "#21C5D9", "Teal": "#16B8A5", "White": "#FFFFFF", "Light": "#F4F7FB",
	"Text": "#536174", "Line": "#E3EAF3", "UAE": "#17B890", "Oman": "#2E9D62", "Amber": "#D98E0B"}


def _file(path, fname):
	name = frappe.db.get_value("File", {"file_name": fname, "is_private": 0})
	if name:
		frappe.delete_doc("File", name, force=True, ignore_permissions=True)
	with open(path, "rb") as f:
		d = frappe.get_doc({"doctype": "File", "file_name": fname, "content": f.read(), "is_private": 0}).insert(ignore_permissions=True)
	return d.file_url


def _token(key, val):
	tname = f"EIH {key}"
	name = frappe.db.get_value("Builder Token", {"token_name": tname})
	if not name:
		name = frappe.get_doc({"doctype": "Builder Token", "token_name": tname, "type": "Color", "value": val, "group": "thinkNXG E-Invoice Hub"}).insert(ignore_permissions=True).name
	else:
		frappe.db.set_value("Builder Token", name, "value", val)
	return f"var(--{name})"


def _script(kind, key, src):
	"""Builder Client Script identified by a marker comment."""
	marker = f"/* {key} */\n"
	existing = frappe.db.get_value("Builder Client Script", {"script_type": kind, "script": ["like", f"{marker}%"]})
	body = marker + src
	if existing:
		d = frappe.get_doc("Builder Client Script", existing)
		d.script = body
		d.save(ignore_permissions=True)
		return existing
	return frappe.get_doc({"doctype": "Builder Client Script", "script_type": kind, "script": body}).insert(ignore_permissions=True).name


def run():
	from .page_build import content, dsl
	existing = frappe.db.get_value("Builder Page", {"route": ROUTE}) or frappe.db.get_value("Builder Page", {"route": ROUTE.lower()})
	if existing and frappe.db.get_value("Builder Page", existing, "canonical_url") != CANON:
		frappe.throw(f"Route {ROUTE} is already used by Builder Page {existing}; not overwriting.")
	for k, v in PALETTE.items():
		dsl.T[k] = _token(k, v)
	pdf = _file(os.path.join(HERE, "page_build/assets/thinkNXG-E-Invoice-Hub-Brochure.pdf"), "thinkNXG-E-Invoice-Hub-Brochure.pdf")
	css_src = open(os.path.join(HERE, "page_build/assets/eih.css")).read()
	for w in (500, 600, 700, 800):
		css_src = css_src.replace(f"__FONT_{w}__", _file(os.path.join(HERE, f"page_build/assets/pjs-{w}.woff2"), f"thinknxg-pjs-{w}.woff2"))
	css = _script("CSS", "eih-css", css_src)
	js = _script("JavaScript", "eih-js", open(os.path.join(HERE, "page_build/assets/eih.js")).read())
	og = ""
	ogp = os.path.join(HERE, "page_build/assets/og-image.png")
	if os.path.exists(ogp):
		og = _file(ogp, "eih-og-image.png")
	content.BROCHURE = pdf
	blocks = content.build_page()
	vals = {"page_name": PAGE_NAME, "page_title": TITLE, "route": ROUTE, "blocks": json.dumps(blocks), "draft_blocks": json.dumps(blocks), "meta_description": DESC,
		"canonical_url": CANON, "language": "en", "meta_image": og or None, "head_html": content.head_meta("https://kreatao.com" + og if og.startswith("/") else og) + content.jsonld(), "published": 0}
	cur = frappe.db.get_value("Builder Page", {"canonical_url": CANON})
	if cur:
		doc = frappe.get_doc("Builder Page", cur)
		doc.update(vals)
		doc.client_scripts = []
	else:
		doc = frappe.get_doc({"doctype": "Builder Page", **vals})
	for s in (css, js):
		doc.append("client_scripts", {"builder_script": s})
	doc.save(ignore_permissions=True)
	doc.publish() if hasattr(doc, "publish") else None
	frappe.db.commit()
	print("page", doc.name, "route", doc.route, "published", frappe.db.get_value("Builder Page", doc.name, "published"), "brochure", pdf)
