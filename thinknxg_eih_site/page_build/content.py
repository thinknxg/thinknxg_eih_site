import json
from .dsl import *

import os
BROCHURE = "/files/thinkNXG-E-Invoice-Hub-Brochure.pdf"
SVGD = os.path.join(os.path.dirname(__file__), "svg")


def svg(name):
    return open(f"{SVGD}/{name}.web.svg").read()


def eyebrow(s, color="Elec"):
    return text("p", s, st={"fontSize": "13px", "fontWeight": "800", "letterSpacing": "0.16em", "textTransform": "uppercase", "color": c(color), "margin": "0"})


def h2(s, dark=False, align="left"):
    return text("h2", s, st={"fontSize": "clamp(28px, 3.6vw, 44px)", "lineHeight": "1.12", "fontWeight": "800", "color": c("White") if dark else c("Navy"), "margin": "0", "letterSpacing": "-0.01em", "textAlign": align})


def lead(s, dark=False, mw="780px", align="left"):
    return text("p", s, st={"fontSize": "18px", "lineHeight": "1.6", "color": "#B9C7DD" if dark else c("Text"), "margin": "0", "maxWidth": mw, "textAlign": align}, mob={"fontSize": "16px"})


def btn(label, href, kind="primary", track=None):
    base = {"display": "inline-flex", "alignItems": "center", "justifyContent": "center", "paddingTop": "14px", "paddingBottom": "14px", "paddingLeft": "26px", "paddingRight": "26px",
            "borderRadius": "999px", "fontWeight": "800", "fontSize": "16px", "textDecoration": "none", "width": "fit-content", "cursor": "pointer"}
    if kind == "primary":
        base.update({"backgroundImage": f"linear-gradient(135deg, {c('Elec')}, {c('Cyan')})", "color": "#FFFFFF"})
    elif kind == "ghost":
        base.update({"border": "2px solid #6F86AE", "color": "#FFFFFF", "backgroundColor": "transparent"})
    elif kind == "outline":
        base.update({"border": f"2px solid {c('Elec')}", "color": c("Elec"), "backgroundColor": "#FFFFFF"})
    else:
        base.update({"backgroundColor": c("Navy"), "color": "#FFFFFF"})
    return blk("a", text=label, st=base, attrs={"href": href}, custom={"data-track": track or label}, cls=["eih-btn"])


def card(title, body, kind=None, dark=False, accent=None, extra=None, st=None):
    kids = []
    kids.append(text("h3", title, st={"fontSize": "19px", "fontWeight": "800", "color": "#FFFFFF" if dark else c("Navy"), "margin": "0", "lineHeight": "1.25"}))
    kids.append(text("p", body, st={"fontSize": "15px", "lineHeight": "1.55", "color": "#B9C7DD" if dark else c("Text"), "margin": "0"}))
    if extra:
        kids.extend(extra)
    base = {"display": "flex", "flexDirection": "column", "gap": "10px", "padding": "24px", "borderRadius": "18px", "backgroundColor": c("Navy") if dark else "#FFFFFF",
            "border": f"1px solid {'#2A3B5E' if dark else c('Line')}", "borderTop": f"4px solid {accent}" if accent else f"1px solid {'#2A3B5E' if dark else c('Line')}"}
    base.update(st or {})
    return blk("div", kids, st=base, cls=["eih-card"])


def bullets(items, color="Teal", dark=False):
    kids = [text("li", s, st={"fontSize": "15px", "lineHeight": "1.5", "color": "#B9C7DD" if dark else c("Text"), "marginBottom": "8px", "listStyle": "none", "paddingLeft": "20px", "position": "relative"}, cls=[f"eih-li-{color.lower()}"]) for s in items]
    return blk("ul", kids, st={"padding": "0", "margin": "0"})




LOGO = ('<svg width="40" height="40" viewBox="0 0 44 44" role="img" aria-label="thinkNXG E-Invoice Hub logo"><defs><linearGradient id="lgx" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2878E5"/><stop offset="1" stop-color="#21C5D9"/></linearGradient></defs>'
        '<rect width="44" height="44" rx="12" fill="url(#lgx)"/><g stroke="#fff" stroke-width="1.8"><path d="M22 22L11 13M22 22L33 13M22 22L11 31M22 22L33 31"/></g><g fill="#fff"><circle cx="11" cy="13" r="3.2"/><circle cx="33" cy="13" r="3.2"/><circle cx="11" cy="31" r="3.2"/><circle cx="33" cy="31" r="3.2"/><circle cx="22" cy="22" r="5.5"/></g></svg>')

NAV = [("Home", "#top"), ("Platform", "#platform"), ("UAE", "#uae"), ("Oman", "#oman"), ("Global Peppol", "#peppol"), ("Architecture", "#architecture"), ("ERP", "#erp"), ("Features", "#features"), ("FAQ", "#faq")]


def nav():
    links = [text("a", n, st={"color": "#DCE6F5", "fontSize": "14px", "fontWeight": "600", "textDecoration": "none", "padding": "8px 10px", "whiteSpace": "nowrap"}, attrs={"href": h}, cls=["eih-navlink"], custom={"data-track": f"nav-{n}"}) for n, h in NAV]
    links.append(btn("Request a Demo", "#contact", "primary", "nav-request-demo"))
    brand = blk("a", [blk("div", text=LOGO, raw=True, st={"display": "flex"}),
                      div([text("span", "thinkNXG", st={"fontSize": "17px", "fontWeight": "800", "color": "#FFFFFF", "lineHeight": "1.1"}), text("span", "E-Invoice Hub", st={"fontSize": "13px", "color": "#9FB4D6", "fontWeight": "600", "lineHeight": "1.2"})])],
                st={"display": "flex", "flexDirection": "row", "alignItems": "center", "gap": "10px", "textDecoration": "none"}, attrs={"href": "#top"})
    burger = blk("button", text="Menu", st={"display": "none", "backgroundColor": "transparent", "color": "#FFFFFF", "border": "1.5px solid #6F86AE", "borderRadius": "10px", "padding": "8px 14px", "fontWeight": "700", "fontSize": "14px"},
                 mob={"display": "block"}, cls=["eih-burger"], custom={"aria-label": "Toggle navigation", "aria-expanded": "false"})
    menu = row(links, st={"gap": "2px", "flexWrap": "wrap", "justifyContent": "flex-end"}, mob={"display": "none", "flexDirection": "column", "alignItems": "stretch", "width": "100%", "paddingTop": "10px"}, tab={"gap": "0"}, cls=["eih-navlinks"])
    inner = row([brand, burger, menu], st={"justifyContent": "space-between", "maxWidth": "1280px", "width": "100%", "paddingLeft": "24px", "paddingRight": "24px", "paddingTop": "12px", "paddingBottom": "12px", "gap": "16px", "flexWrap": "wrap"},
                mob={"flexWrap": "wrap"})
    return blk("nav", [inner], st={"position": "sticky", "top": "0px", "zIndex": "60", "width": "100%", "display": "flex", "flexDirection": "column", "alignItems": "center", "backgroundColor": c("Navy"), "borderBottom": "1px solid #20335A"},
               custom={"aria-label": "Main"}, name="navigation")




COUNTRIES = ["UAE", "Oman", "UAE and Oman", "Global Peppol / other countries"]
ERPS = ["thinkNXG ERP", "ERPNext", "SAP", "Oracle", "Microsoft Dynamics", "Odoo", "Zoho", "Other ERP System"]
VOLS = ["Under 1,000 invoices / month", "1,000 - 10,000 / month", "10,000 - 100,000 / month", "Over 100,000 / month", "Not sure yet"]


def form_html():
    opt = lambda xs: "".join(f'<option value="{x}">{x}</option>' for x in xs)
    f = lambda i, label, inner, req=False: f'<div class="eih-field"><label for="{i}">{label}{" *" if req else ""}</label>{inner}</div>'
    return ('<form id="eih-enquiry" class="eih-form" novalidate autocomplete="on"><div class="eih-grid">'
            + f("eih-name", "Name", '<input id="eih-name" name="full_name" type="text" maxlength="120" required autocomplete="name">', True)
            + f("eih-email", "Business Email", '<input id="eih-email" name="business_email" type="email" maxlength="140" required autocomplete="email">', True)
            + f("eih-company", "Company", '<input id="eih-company" name="company" type="text" maxlength="160" required autocomplete="organization">', True)
            + f("eih-country", "Country", '<input id="eih-country" name="country" type="text" maxlength="80" required autocomplete="country-name">', True)
            + f("eih-erp", "ERP System", f'<select id="eih-erp" name="erp_system" required><option value="">Select...</option>{opt(ERPS)}</select>', True)
            + f("eih-compliance", "E-Invoicing Requirements", f'<select id="eih-compliance" name="required_compliance" required><option value="">Select...</option>{opt(COUNTRIES)}</select>', True)
            + f("eih-asp", "ASP / Access Point", '<input id="eih-asp" name="existing_asp" type="text" maxlength="160" placeholder="If you already use one">')
            + f("eih-volume", "Invoice Volume", f'<select id="eih-volume" name="invoice_volume"><option value="">Select...</option>{opt(VOLS)}</select>')
            + '</div>' + f("eih-message", "Message", '<textarea id="eih-message" name="message" rows="4" maxlength="2000" placeholder="Tell us about your ERP, countries and timeline"></textarea>')
            + '<div class="eih-hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website_url" tabindex="-1" autocomplete="off"></label></div>'
            + '<label class="eih-consent"><input id="eih-consent" name="consent" type="checkbox" required> I agree that Kreatao may store these details to respond to my enquiry. <a href="#privacy">Privacy note</a> *</label>'
            + '<button type="submit" class="eih-submit">Request a Demo</button><p id="eih-status" class="eih-status" role="status" aria-live="polite"></p></form>')


def contact():
    cta = [text("h2", "One Hub. Every ERP. Connected E-Invoicing.", st={"fontSize": "clamp(30px, 4vw, 50px)", "lineHeight": "1.1", "fontWeight": "800", "color": "#FFFFFF", "margin": "0"}),
           lead("Connect thinkNXG ERP, ERPNext and other enterprise applications to UAE PINT AE, Oman Fawtara and global Peppol through one hub.", True),
           row([btn("Request a Demo", "#eih-enquiry", "primary", "final-request-demo"), btn("Contact Our Team", "#eih-enquiry", "ghost", "final-talk-team"), btn("Download Brochure", BROCHURE, "ghost", "final-download-brochure")], st={"gap": "14px", "flexWrap": "wrap"}),
           blk("div", text=form_html(), raw=True, st={"width": "100%", "maxWidth": "920px", "marginTop": "12px"}, name="enquiry-form"),
           blk("div", text='<div id="privacy" style="font-size:13px;line-height:1.6;color:#8FA3C4;max-width:820px"><b style="color:#DCE6F5">Privacy note.</b> Details you submit are stored in this website\'s enquiry records and used to respond to your request. Please do not include invoices, credentials or other confidential data in the message field.</div>', raw=True)]
    return section("contact", cta, bg=c("Navy"), dark=True, pad="96px", name="final-cta")


def footer():
    def col(title, links):
        return div([text("p", title, st={"fontSize": "13px", "fontWeight": "800", "letterSpacing": "0.14em", "textTransform": "uppercase", "color": "#FFFFFF", "margin": "0 0 8px 0"})] +
                   [text("a", l, st={"color": "#9FB4D6", "fontSize": "14px", "textDecoration": "none", "padding": "4px 0"}, attrs={"href": h}) for l, h in links], st={"gap": "2px"})
    brand = div([blk("div", text=LOGO, raw=True), text("p", "thinkNXG E-Invoice Hub", st={"color": "#FFFFFF", "fontWeight": "800", "fontSize": "18px", "margin": "0"}),
                 text("p", "Powering the Future of Multi-Country E-Invoicing.", st={"color": "#9FB4D6", "fontSize": "14px", "margin": "0", "lineHeight": "1.5"}),
                 text("p", "Transmission to Peppol and national networks runs through the Accredited Service Providers and Access Points you configure.", st={"color": "#6F86AE", "fontSize": "12px", "margin": "0", "lineHeight": "1.5"})], st={"gap": "10px"})
    cols = grid([brand, col("Product", [("Platform", "#platform"), ("Architecture", "#architecture"), ("ERP Connectivity", "#erp"), ("Features", "#features"), ("Lifecycle", "#lifecycle")]), col("Solutions", [("UAE E-Invoicing", "#uae"), ("Oman Fawtara", "#oman"), ("Global Peppol", "#peppol")]),
                 col("Resources", [("Documentation", "https://github.com/thinknxg/thinkNXG-E-Invoice-Hub/tree/main/docs"), ("Product brochure", BROCHURE), ("FAQ", "#faq")]), col("Company", [("Contact", "#contact"), ("Privacy", "#privacy"), ("Kreatao", "https://kreatao.com")])], 5, gap="32px", st={"gridTemplateColumns": "1.6fr 1fr 1fr 1fr 1fr"})
    cols["tabletStyles"] = {"gridTemplateColumns": "repeat(2, minmax(0, 1fr))"}
    return blk("footer", [container([cols, text("p", "© 2026 Kreatao. thinkNXG E-Invoice Hub. All rights reserved.", st={"color": "#6F86AE", "fontSize": "13px", "margin": "0", "borderTop": "1px solid #20335A", "paddingTop": "18px"})])],
               st={"display": "flex", "flexDirection": "column", "alignItems": "center", "width": "100%", "backgroundColor": "#0B1428", "paddingTop": "56px", "paddingBottom": "32px"}, name="footer")




# ------------------------------------------------------------------------------------------ v2 sections
def svg(name):
    return open(f"{SVGD}/{name}.web.svg").read()


def _ic(paths):
    return f'<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


ICONS = {
    "hub": _ic('<circle cx="12" cy="12" r="2.6"/><circle cx="4.5" cy="5" r="1.8"/><circle cx="19.5" cy="5" r="1.8"/><circle cx="4.5" cy="19" r="1.8"/><circle cx="19.5" cy="19" r="1.8"/><path d="M10 10 5.8 6.3M14 10l4.2-3.7M10 14l-4.2 3.7M14 14l4.2 3.7"/>'),
    "doc": _ic('<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h4"/>'),
    "globe": _ic('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>'),
    "shield": _ic('<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="m9 12 2 2 4-4"/>'),
    "cloud": _ic('<path d="M7 18a4 4 0 0 1 0-8 5 5 0 0 1 9.6-1A4.5 4.5 0 0 1 17 18z"/>'),
    "code": _ic('<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>'),
    "flow": _ic('<path d="M4 8h13m-4-4 4 4-4 4M20 16H7m4-4-4 4 4 4"/>'),
    "chart": _ic('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
    "refresh": _ic('<path d="M20 11a8 8 0 0 0-14-4L4 9M4 4v5h5M4 13a8 8 0 0 0 14 4l2-2M20 20v-5h-5"/>'),
    "file": _ic('<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v5h4M10 14l2 2 3-3"/>'),
    "layers": _ic('<path d="m12 3 9 5-9 5-9-5zM3 13l9 5 9-5M3 17.5l9 5 9-5" />'),
    "lock": _ic('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'),
    "plug": _ic('<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/>'),
    "bolt": _ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
}


def fcard(title, body, icon, accent="Elec", st=None, dark=False):
    ic = blk("div", text=ICONS[icon], st={"width": "48px", "height": "48px", "borderRadius": "14px", "display": "flex", "alignItems": "center", "justifyContent": "center",
                                           "backgroundColor": "rgba(40,120,229,.12)" if accent == "Elec" else "rgba(22,184,165,.14)", "color": c(accent) if not dark else "#21C5D9"}, raw=True)
    base = {"gap": "12px", "padding": "24px"}
    base.update(st or {})
    return card(title, body, extra=None, dark=dark, accent=c(accent), st=base) if False else _icard(ic, title, body, accent, base, dark)


def _icard(ic, title, body, accent, st, dark):
    kids = [ic, text("h3", title, st={"fontSize": "18px", "fontWeight": "800", "color": "#FFFFFF" if dark else c("Navy"), "margin": "0", "lineHeight": "1.25"}),
            text("p", body, st={"fontSize": "15px", "lineHeight": "1.55", "color": "#B9C7DD" if dark else c("Text"), "margin": "0"})]
    base = {"display": "flex", "flexDirection": "column", "borderRadius": "18px", "backgroundColor": c("Navy") if dark else "#FFFFFF", "border": f"1px solid {'#2A3F6B' if dark else c('Line')}"}
    base.update(st)
    return blk("div", kids, st=base, cls=["eih-card"])


ERP_ORDER = ["thinkNXG ERP", "ERPNext", "SAP", "Oracle", "Microsoft Dynamics", "Odoo", "Zoho", "Other ERP Systems"]


def erp_tiles(dark=False):
    """Native tiles in the mandated order; thinkNXG ERP is the full-width hero tile."""
    tiles = []
    for i, n in enumerate(ERP_ORDER):
        if i == 0:
            t = blk("div", [text("p", "FLAGSHIP INTEGRATION", st={"fontSize": "12px", "fontWeight": "800", "letterSpacing": "0.14em", "color": "#EAF6FF", "margin": "0"}),
                            text("h3", n, st={"fontSize": "clamp(28px,3.4vw,40px)", "fontWeight": "800", "color": "#FFFFFF", "margin": "0", "lineHeight": "1.1"}),
                            text("p", "Native connector: invoices, customers, items and statuses flow both ways.", st={"fontSize": "16px", "color": "#EAF6FF", "margin": "0"})],
                    st={"display": "flex", "flexDirection": "column", "gap": "8px", "padding": "28px", "borderRadius": "20px", "backgroundImage": f"linear-gradient(135deg, {c('Elec')}, {c('Cyan')})", "gridColumn": "1 / -1"}, cls=["eih-card", "eih-erp-hero"])
        else:
            tag = "Native connector" if i == 1 else "Universal API"
            t = blk("div", [text("h3", n, st={"fontSize": "18px", "fontWeight": "800", "color": "#FFFFFF" if dark else c("Navy"), "margin": "0"}),
                            text("p", tag, st={"fontSize": "13px", "fontWeight": "600", "color": c("Cyan") if dark else c("Elec"), "margin": "0"})],
                    st={"display": "flex", "flexDirection": "column", "gap": "4px", "padding": "18px 20px", "borderRadius": "14px", "backgroundColor": "#14264A" if dark else "#FFFFFF",
                        "border": f"1.5px solid {c('Elec') if i == 1 else ('#2A3F6B' if dark else c('Line'))}"}, cls=["eih-card"])
        tiles.append(t)
    return grid(tiles, 4, gap="14px", tab_n=2, st={"gridTemplateColumns": "repeat(4, minmax(0, 1fr))"})


def hero_stack():
    """Native vertical version of the hero for phones; the SVG scene is shown from tablet width up."""
    chip_ = lambda n, hero=False: text("span", n, st={"fontSize": "15px" if not hero else "20px", "fontWeight": "800", "padding": "8px 14px" if not hero else "14px 18px", "borderRadius": "12px",
                                                         "backgroundImage": f"linear-gradient(135deg, {c('Elec')}, {c('Cyan')})" if hero else "none", "backgroundColor": "transparent" if hero else "#14264A",
                                                         "border": "1px solid #2A3F6B", "color": "#FFFFFF", "display": "block"})
    erps = div([chip_(ERP_ORDER[0], True)] + [chip_(n) for n in ERP_ORDER[1:]], st={"gap": "8px"})
    arrow = text("p", "⇅", st={"textAlign": "center", "fontSize": "26px", "color": "#21C5D9", "margin": "0"})
    hubc = div([text("p", "thinkNXG E-Invoice Hub", st={"fontSize": "20px", "fontWeight": "800", "color": "#FFFFFF", "margin": "0", "textAlign": "center"}),
                text("p", "Canonical model · Processing · Lifecycle tracking", st={"fontSize": "14px", "color": "#B9C7DD", "margin": "0", "textAlign": "center"})],
               st={"padding": "20px", "borderRadius": "20px", "border": "2px solid #21C5D9", "backgroundColor": "#10306A", "gap": "6px"})
    pil = div([text("span", n, st={"fontSize": "15px", "fontWeight": "800", "color": "#FFFFFF", "padding": "12px 14px", "borderRadius": "12px", "border": f"2px solid {col}", "backgroundColor": "#14264A", "display": "block"})
               for n, col in (("UAE PINT AE", "#17B890"), ("Oman Fawtara", "#2E9D62"), ("Global Peppol", "#2878E5"), ("ASP / Access Point providers", "#21C5D9"))], st={"gap": "8px"})
    return blk("div", [erps, arrow, hubc, arrow, pil], st={"display": "none", "flexDirection": "column", "gap": "10px", "width": "100%"}, mob={"display": "flex"}, tab={"display": "none"}, cls=["eih-herostack"])


def hero():
    left = [eyebrow("UAE | Oman | Global Peppol", "Cyan"),
            text("h1", "One Universal Hub for Multi-Country E-Invoicing.", st={"fontSize": "clamp(36px, 5.4vw, 66px)", "lineHeight": "1.05", "fontWeight": "800", "color": "#FFFFFF", "margin": "0", "letterSpacing": "-0.02em", "maxWidth": "900px"}),
            lead("Connect your ERP systems to country-specific compliance frameworks and Peppol networks through one intelligent integration platform.", True, "720px"),
            row([btn("Request a Demo", "#contact", "primary", "hero-request-demo"), btn("Explore the Architecture", "#architecture", "ghost", "hero-explore-architecture")], st={"gap": "14px", "flexWrap": "wrap", "marginTop": "6px"})]
    art = figure(svg("hero"), "hero", "Animated network: thinkNXG ERP, ERPNext and other ERP systems connect to the universal hub, which serves UAE PINT AE, Oman Fawtara, the global Peppol ecosystem and ASP or Access Point providers", "940px", st={"marginTop": "20px"})
    art["classes"] = ["eih-herofig"]
    return section("top", [div(left, st={"gap": "20px"}), art, hero_stack()], bg=c("Navy"), pad="72px", dark=True, name="hero")


def challenge():
    pts = [("Different national regulations", "Each market defines its own e-invoicing law."), ("Multiple invoice formats", "Structures, identifiers and code lists differ."), ("Different compliance requirements", "Tax and reporting rules vary and evolve."),
           ("Multiple service providers", "Every provider has its own API and statuses."), ("Complex ERP integrations", "Each ERP, country and provider multiplies the work."), ("Fragmented monitoring", "Status scatters across portals and spreadsheets.")]
    return section("challenge", [eyebrow("The global challenge"), h2("Different Countries. Different Regulations. One Universal Solution."),
                                 lead("Every country asks for its own invoice format, tax data and route to the authority, and every ERP needs its own connection to each of them. One hub replaces that web with a single integration."),
                                 figure(svg("challenge"), "challenge", "Before and after: separate integrations for every ERP, country and provider compared with one universal hub", "1000px"),
                                 grid([card(t, d, accent=c("Amber")) for t, d in pts], 3, tab_n=2)], bg=c("Light"), name="challenge")


def platform():
    cards = [fcard("Universal ERP integration", "thinkNXG ERP, ERPNext and other enterprise applications connect once, through connectors and the Universal API.", "plug"),
             fcard("Canonical invoice model", "Every invoice is normalised into one structure, so country and provider logic never depends on your ERP.", "layers", "Teal"),
             fcard("Multi-country compliance", "Dedicated UAE and Oman engines apply each country's rules, identifiers and documents on the same foundation.", "globe")]
    return section("platform", [eyebrow("Introducing thinkNXG E-Invoice Hub"), h2("Introducing thinkNXG E-Invoice Hub."),
                                lead("thinkNXG E-Invoice Hub connects enterprise ERP systems, country-specific compliance engines, Accredited Service Providers, Peppol Access Points and national e-invoicing networks through one universal integration platform. A common invoice model means every country, provider and ERP speaks the same language inside the hub."),
                                grid(cards, 3), figure(svg("hub"), "hub", "Universal e-invoicing hub: thinkNXG ERP, ERPNext and other ERP systems, universal hub, country compliance, ASP or Access Point and the Peppol network", "1100px")], name="platform")


def solutions():
    def country(title, sub, accent, pts, href):
        return card(title, sub, accent=accent, st={"gap": "14px", "padding": "28px"}, extra=[bullets(pts), btn("Explore " + title.split(" ")[0] if title != "Global Peppol" else "Explore Global Peppol", href, "outline", f"cta-{title}")])
    cs = [country("UAE E-Invoicing", "Peppol PINT AE for the UAE five-corner model.", c("UAE"), ["PINT AE 1.0.5", "Five-corner architecture", "ASP connectivity", "FTA reporting lifecycle"], "#uae"),
          country("Oman Fawtara", "Peppol PINT OM for Oman's national e-invoicing.", c("Oman"), ["Oman electronic invoicing", "Country-specific compliance", "Oman VAT requirements", "Provider integration"], "#oman"),
          country("Global Peppol", "One engine, country-specific profiles.", c("Elec"), ["Country-specific profiles", "UBL and Peppol interoperability", "Access Point connectivity", "Cross-border invoice exchange"], "#peppol")]
    return section("solutions", [eyebrow("Global country solutions"), h2("One Platform. Three Solution Pillars."), grid(cs, 3)], bg=c("Light"), name="solutions")


LAYERS = [("ERP systems", "thinkNXG ERP, ERPNext, SAP, Oracle, Microsoft Dynamics, Odoo, Zoho and other ERP systems hold the source invoice. thinkNXG ERP is the flagship connector.", "Outbound: invoice created or approved in the ERP. Inbound: purchase invoice drafted in the ERP."),
          ("ERP connectors", "The native thinkNXG ERP and ERPNext connector, the Universal REST connector, mapping configuration and signed ERP webhooks.", "Your ERP never integrates with a provider directly."),
          ("Canonical invoice model", "One invoice structure for every ERP and country. The source payload, canonical form and country documents are kept as immutable records.", "Normalisation happens once."),
          ("Invoice processing engine", "Outbound and inbound pipelines, retry engine, duplicate protection, transaction locks and reconciliation.", "Every transaction has one owner at a time."),
          ("Country compliance engine", "UAE PINT AE 1.0.5 and Oman PINT OM 1.0.1: tax validation, identifiers and UBL 2.1 document generation, selected per invoice.", "Each country keeps its own rule set."),
          ("ASP / Access Point connectors", "A configurable REST adapter framework, provider directory, credential verification and XML and PDF retrieval.", "Choose and change providers without touching the ERP link."),
          ("Peppol and national networks", "The Peppol network, UAE e-invoicing with FTA reporting and Oman Fawtara with OTA reporting, reached through your providers.", "Status returns to the hub and on to the ERP.")]


def architecture():
    btns = []
    for i, (t, d, n) in enumerate(LAYERS):
        btns.append(blk("button", [text("span", f"{i + 1:02d}", st={"fontSize": "13px", "fontWeight": "800", "color": "#21C5D9", "width": "28px"}), text("span", t, st={"fontSize": "16px", "fontWeight": "700", "color": "#FFFFFF"})],
                        st={"display": "flex", "flexDirection": "row", "alignItems": "center", "gap": "8px", "textAlign": "left", "padding": "14px 16px", "borderRadius": "12px", "backgroundColor": "#14264A", "border": "1.5px solid #2A3F6B", "cursor": "pointer", "width": "100%"},
                        cls=["eih-layer"] + (["on"] if i == 0 else []), custom={"data-eih-layer": str(i), "type": "button"}))
    panels = []
    for i, (t, d, n) in enumerate(LAYERS):
        panels.append(blk("div", [text("p", f"LAYER {i + 1}", st={"fontSize": "12px", "fontWeight": "800", "letterSpacing": "0.14em", "color": "#21C5D9", "margin": "0"}),
                                  text("h3", t, st={"fontSize": "26px", "fontWeight": "800", "color": "#FFFFFF", "margin": "0"}), text("p", d, st={"fontSize": "17px", "lineHeight": "1.6", "color": "#DCE8FA", "margin": "0"}),
                                  text("p", n, st={"fontSize": "15px", "lineHeight": "1.55", "color": "#8FA3C4", "margin": "0"})],
                         st={"flexDirection": "column", "gap": "12px", "padding": "28px", "borderRadius": "18px", "backgroundColor": "#14264A", "border": "1px solid #2A3F6B", "minHeight": "260px"},
                         cls=["eih-panel"] + (["on"] if i == 0 else []), custom={"data-eih-panel": str(i)}))
    inter = blk("div", [div(btns, st={"gap": "8px"}), div(panels)], st={"display": "grid", "gridTemplateColumns": "minmax(0,1fr) minmax(0,1.4fr)", "gap": "22px", "width": "100%"}, mob={"gridTemplateColumns": "minmax(0, 1fr)"}, tab={"gridTemplateColumns": "minmax(0, 1fr)"})
    return section("architecture", [eyebrow("Universal architecture", "Cyan"), h2("A Universal Integration Hub, Layer by Layer.", True),
                                    lead("thinkNXG ERP, then ERPNext, then every other ERP, all flowing through one canonical model, one processing engine and one compliance layer. Select a layer to explore it.", True),
                                    inter, figure(svg("layers"), "layers", "Seven-layer universal architecture from ERP systems to Peppol and national networks", "1100px")], bg=c("Navy"), dark=True, name="architecture")


FEATURES = [("Universal ERP Integration", "Connect thinkNXG ERP, ERPNext and other enterprise applications once.", "plug", "Elec"), ("Canonical Invoice Model", "One structure for invoices, credit notes, self-billing and purchase documents.", "layers", "Teal"),
            ("Multi-Country Compliance", "A dedicated rule set per country on one shared foundation.", "globe", "Elec"), ("UAE PINT AE", "PINT AE 1.0.5 invoices with TRN, VAT category and AED handling.", "doc", "Teal"),
            ("Oman Fawtara", "PINT OM 1.0.1 invoices with VATIN, OMR amounts, UUIDs and QR payload.", "doc", "Elec"), ("Global Peppol Connectivity", "UBL 2.1 documents and country profiles built for Peppol exchange.", "hub", "Teal"),
            ("ASP Integration", "A provider-neutral adapter framework for your chosen ASP or Access Point.", "cloud", "Elec"), ("REST API", "Submit, validate, track and retrieve invoices from any system.", "code", "Teal"),
            ("Signed Webhooks", "HMAC-signed events in both directions; unsigned calls are rejected.", "shield", "Elec"), ("Inbound and Outbound Processing", "Send invoices out and bring received documents into your ERP.", "flow", "Teal"),
            ("Invoice Lifecycle Tracking", "Validation, provider, regulatory and Peppol delivery states kept apart.", "chart", "Elec"), ("Retry and Reconciliation", "Automatic retries and provider status matched to every invoice.", "refresh", "Teal"),
            ("XML / PDF Retrieval", "Fetch the XML and PDF the provider holds for any submitted document.", "file", "Elec"), ("Multi-Tenant Architecture", "Each tenant's companies, connections and data stay isolated.", "lock", "Teal")]


def features():
    return section("features", [eyebrow("Core features"), h2("Everything Between Your ERP and the Network."), grid([fcard(t, d, i, a) for t, d, i, a in FEATURES], 4, tab_n=2)], name="features")


def erp():
    return section("erp", [eyebrow("ERP connectivity"), h2("Your ERP. One Universal Integration."),
                           lead("Keep the ERP you run today. thinkNXG ERP and ERPNext connect through the native connector; SAP, Oracle, Microsoft Dynamics, Odoo, Zoho and other systems connect through the Universal REST API, signed webhooks and mapping configuration."),
                           erp_tiles(), figure(svg("erp"), "erp", "ERP integration ecosystem in order: thinkNXG ERP, ERPNext, SAP, Oracle, Microsoft Dynamics, Odoo, Zoho and other ERP systems connected to one hub", "1100px")], bg=c("Light"), name="erp")


def _solution(sid, eyb, title, lead_s, fig, alt, pts, accent, bg=None, dark=False):
    return section(sid, [eyebrow(eyb, "UAE" if sid == "uae" else ("Oman" if sid == "oman" else "Elec")), h2(title, dark), lead(lead_s, dark), figure(svg(fig), fig, alt, "1100px"),
                         grid([card(t, d, accent=accent, dark=dark) for t, d in pts], 3, tab_n=2)], bg=bg, dark=dark, name=sid)


def uae():
    return _solution("uae", "UAE e-invoicing", "UAE E-Invoicing. Simplified Through One Integration Hub.",
                     "Prepare, validate and submit UAE PINT AE invoices from your ERP, and follow each one through ASP submission, FTA reporting and Peppol delivery.", "uae",
                     "UAE five-corner architecture: supplier, hub, supplier ASP, buyer ASP, buyer and the Federal Tax Authority", [
                         ("PINT AE 1.0.5", "Invoices built to the UAE Peppol specification, with its published validation rules applied."), ("Five-corner architecture", "Supplier, ASP, buyer ASP, buyer and FTA relationships modelled end to end."),
                         ("Country-specific processing", "TRN identification, VAT categories, exemption and reverse-charge handling and AED reporting values."), ("ASP connectivity", "Submit through the Accredited Service Provider you choose."),
                         ("FTA reporting lifecycle", "Regulatory reporting status tracked separately from delivery."), ("Credit notes and self-billing", "The full UAE document range, synchronised back to your ERP.")], c("UAE"))


def oman():
    return _solution("oman", "Oman Fawtara", "Oman Fawtara. Connected Through a Unified Integration Platform.",
                     "A dedicated Oman engine prepares Fawtara-ready PINT OM invoices on the same canonical model, pipeline and monitoring you use for every other country.", "oman",
                     "Oman Fawtara architecture: seller, hub, seller provider, buyer provider, buyer, OTA Access Point and Oman Tax Authority", [
                         ("PINT OM 1.0.1", "Invoices built to the Peppol PINT OM specification, with its published rules applied."), ("Oman VAT requirements", "VATIN, effective-dated rates, reason codes and OMR amounts to three decimals."),
                         ("Country-specific invoice data", "Invoice and Seller UUIDs, transaction type flags and the QR payload for the printed invoice."), ("Every invoice type", "Tax invoices, credit notes, self-billing, B2C, exports and foreign currency."),
                         ("Provider integration", "Submit through your accredited provider using a configurable adapter."), ("Reporting and status management", "Provider and authority status messages mapped to clear outcomes.")], c("Oman"), bg=c("Light"))


def peppol():
    return _solution("peppol", "Global Peppol", "One Universal Hub. A Connected Global E-Invoicing Ecosystem.",
                     "Country profiles sit on one universal engine. UAE and Oman run side by side today, and every further country follows the same pattern.", "peppol",
                     "World map with UAE PINT AE and Oman PINT OM country profiles connected to one universal integration engine", [
                         ("Country-specific profiles", "Each country keeps its own rules, identifiers and code lists."), ("UBL and Peppol interoperability", "UBL 2.1 documents built for exchange over the Peppol network."),
                         ("Access Point connectivity", "Reach Peppol and national networks through your chosen providers.")], c("Elec"), dark=False)


def providers():
    return section("asp", [eyebrow("ASP integration"), h2("Connect Your Preferred E-Invoicing Service Providers."),
                           lead("A provider-neutral adapter framework lets you connect the ASP or Access Point you prefer, and change it without touching the ERP link. No ERP ever talks to a provider directly."),
                           figure(svg("providers"), "providers", "Provider adapter framework connecting the hub to your ASP, Access Point and onward to Peppol and national networks", "1000px")], bg=c("Light"), name="asp")


def dashboard():
    ind = [("Internal validation", "Country rules and tax checks before anything leaves the hub."), ("Provider submission", "Acceptance by your ASP or Access Point."), ("Regulatory reporting", "Reporting to the tax authority through your provider."), ("Peppol delivery", "Delivery to the buyer over the Peppol network.")]
    return section("lifecycle", [eyebrow("Invoice lifecycle dashboard"), h2("See Every Invoice, From ERP to Delivery."),
                                 lead("Ten transaction statuses and four independent indicators show exactly where each invoice stands. The dashboard below is an illustration with sample data."),
                                 figure(svg("dashboard"), "dashboard", "Illustrative dashboard: ten statuses and separate indicators for internal validation, provider submission, regulatory reporting and Peppol delivery", "1000px"),
                                 grid([card(t, d, accent=c("Teal")) for t, d in ind], 4, tab_n=2)], name="lifecycle")


def security():
    return section("enterprise", [eyebrow("Enterprise architecture", "Cyan"), h2("Built for Enterprise Operations.", True),
                                  lead("Multi-tenant isolation, secure credentials, signed webhooks, transaction locks and duplicate protection, with monitoring and audit records around every invoice.", True),
                                  figure(svg("enterprise"), "enterprise", "Enterprise capabilities: multi-tenancy, secure credentials, signed webhooks, API, monitoring, retry, reconciliation and document management", "1100px")], bg=c("Navy"), dark=True, name="enterprise")


def value():
    old = ["One integration per ERP, country and provider", "Separate formats and rules to maintain", "Provider change means rebuilding", "Status scattered across portals", "Every new country is a new project"]
    new = ["Connect each ERP once", "One canonical invoice model", "Provider-neutral adapters", "One lifecycle view for every invoice", "New countries plug into the same engine"]
    a = card("Traditional integration", "", accent=c("Amber"), extra=[bullets(old, "Amber")], st={"padding": "28px"})
    b = card("Universal integration with thinkNXG E-Invoice Hub", "", accent=c("Teal"), extra=[bullets(new, "Teal")], st={"padding": "28px"})
    return section("benefits", [eyebrow("Business benefits"), h2("Transform the Way Your Business Handles E-Invoicing."), grid([a, b], 2),
                                figure(svg("benefits"), "benefits", "Eight enterprise benefits of one universal hub", "1100px")], bg=c("Light"), name="benefits")


FAQ = [("What is thinkNXG E-Invoice Hub?", "thinkNXG E-Invoice Hub is a universal, multi-country e-invoicing integration platform. It connects ERP systems to country compliance engines, Accredited Service Providers, Peppol Access Points and national networks through one canonical invoice model. Transmission runs through the ASP or Access Point you choose."),
       ("Does it integrate with thinkNXG ERP?", "Yes. thinkNXG ERP is the flagship integration, connected through the native thinkNXG ERP and ERPNext connector."),
       ("Does it support ERPNext?", "Yes. ERPNext uses the same native connector as thinkNXG ERP."),
       ("Can other ERPs connect?", "Yes. SAP, Oracle, Microsoft Dynamics, Odoo, Zoho and other ERP systems connect through the Universal REST API, signed webhooks and configurable mapping."),
       ("What is UAE PINT AE?", "PINT AE is the Peppol international invoice specification for the UAE e-invoicing model. The hub builds invoices to PINT AE 1.0.5, validates them against the country rules and tracks them through ASP submission, FTA reporting and Peppol delivery."),
       ("What is Oman Fawtara?", "Fawtara is Oman's national electronic invoicing system, built on the Peppol PINT OM specification. The hub prepares PINT OM 1.0.1 invoices with the Oman VAT data, identifiers and QR payload, and tracks provider and authority status."),
       ("What is Peppol?", "Peppol is an international network and set of specifications for exchanging electronic business documents between companies through Access Points, using UBL-based formats."),
       ("Can multiple countries be supported?", "Yes. The UAE and Oman engines run side by side on the same canonical model, and a tenant can hold companies in several countries. Inbound documents are routed to the right engine automatically."),
       ("Can multiple ASPs be connected?", "Yes. The provider-neutral adapter framework lets each tenant configure the ASPs and Access Points it uses."),
       ("Does it support inbound and outbound invoices?", "Yes. Outbound invoices are validated, generated and submitted; inbound documents are parsed, matched to your company and drafted as purchase invoices in your ERP."),
       ("How can enterprises request a demo?", "Use the enquiry form on this page or the Request a Demo button, and our team will respond to arrange a walkthrough.")]


def faq():
    items = []
    for q, a in FAQ:
        items.append(blk("details", [text("summary", q, st={"fontSize": "17px", "fontWeight": "700", "color": c("Navy"), "cursor": "pointer", "padding": "18px 0", "lineHeight": "1.4"}),
                                     text("p", a, st={"fontSize": "16px", "lineHeight": "1.65", "color": c("Text"), "margin": "0", "paddingBottom": "18px"})], st={"borderBottom": f"1px solid {c('Line')}", "width": "100%"}, cls=["eih-faq"]))
    dl = grid([card("Product brochure", "The 12-page A4 overview of the platform.", extra=[btn("Download Brochure", BROCHURE, "primary", "download-brochure")]),
               card("Documentation", "Architecture, provider guide and operations guides.", extra=[btn("Open documentation", "https://github.com/thinknxg/thinkNXG-E-Invoice-Hub/tree/main/docs", "outline", "open-docs")])], 2)
    return section("faq", [eyebrow("Resources and FAQ"), h2("Frequently Asked Questions."), dl, div(items, st={"width": "100%", "maxWidth": "900px"})], bg=c("Light"), name="faq")


def build_page():
    body = [nav(), hero(), challenge(), platform(), solutions(), architecture(), features(), erp(), uae(), oman(), peppol(), providers(), dashboard(), security(), value(), faq(), contact(), footer()]
    root = blk("div", body, st={"display": "flex", "flexDirection": "column", "alignItems": "center", "width": "100%", "fontFamily": "Plus Jakarta Sans, Inter, Manrope, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif", "color": c("Text"), "backgroundColor": "#FFFFFF", "minHeight": "100vh"}, name="body")
    root["blockId"] = "root"; root["blockName"] = "body"; root["originalElement"] = "body"
    return [root]


TITLE = "thinkNXG E-Invoice Hub | UAE, Oman & Global Peppol E-Invoicing"
DESC = ("Discover thinkNXG E-Invoice Hub, a universal multi-country e-invoicing integration platform connecting thinkNXG ERP, ERPNext and enterprise systems with UAE PINT AE, Oman Fawtara and Peppol networks.")
CANON = "https://thinknxg.com/kreatao/E-InvoiceHub"
KEYWORDS = "thinkNXG E-Invoice Hub, UAE E-Invoicing Integration, Oman Fawtara Integration, Global Peppol Integration, Multi-Country E-Invoicing, ERP E-Invoicing Integration, thinkNXG ERP E-Invoicing, Electronic Invoice Automation, ASP Integration Platform"


def head_meta(og_url):
    import html as H
    m = [("og:type", "website"), ("og:site_name", "thinkNXG E-Invoice Hub"), ("og:title", TITLE), ("og:description", DESC), ("og:url", CANON), ("og:image", og_url), ("og:image:alt", "thinkNXG E-Invoice Hub connecting thinkNXG ERP, ERPNext and other ERP systems to UAE, Oman and Peppol")]
    t = [("twitter:card", "summary_large_image"), ("twitter:title", TITLE), ("twitter:description", DESC), ("twitter:image", og_url)]
    out = f'<meta name="keywords" content="{H.escape(KEYWORDS)}">\n<meta name="robots" content="index,follow">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    out += "".join(f'<meta property="{k}" content="{H.escape(v)}">\n' for k, v in m) + "".join(f'<meta name="{k}" content="{H.escape(v)}">\n' for k, v in t)
    return out


def jsonld():
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "thinkNXG E-Invoice Hub", "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
           "description": "Universal multi-country e-invoicing integration platform connecting thinkNXG ERP, ERPNext and other ERP systems with UAE PINT AE, Oman Fawtara and Peppol networks.",
           "url": CANON, "publisher": {"@type": "Organization", "name": "Kreatao", "url": "https://kreatao.com"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Kreatao", "item": "https://kreatao.com"}, {"@type": "ListItem", "position": 2, "name": "thinkNXG E-Invoice Hub", "item": CANON}]}
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (app, faq, crumbs))
