"""Small helpers that emit Frappe Builder block JSON."""
import random, re, string

_rng = random.Random(20261120)


def bid():
    return "".join(_rng.choices(string.ascii_lowercase + string.digits, k=9))


T = {}  # token name -> css var(); filled by install.py


def c(name):
    return T.get(name, name)


def blk(el, children=None, text=None, st=None, tab=None, mob=None, cls=None, attrs=None, custom=None, name=None, raw=False):
    d = {"blockId": bid(), "element": el, "attributes": attrs or {}, "customAttributes": custom or {}, "baseStyles": {"boxSizing": "border-box", "minWidth": "0", **(st or {})},
         "tabletStyles": tab or {}, "mobileStyles": mob or {}, "rawStyles": {}, "classes": cls or [], "children": children or [], "dataKey": None}
    if name:
        d["blockName"] = name
    if text is not None:
        d["innerHTML"] = text
    if raw:
        d["element"] = "div"
        d["originalElement"] = "__raw_html__"
    return d


def div(children=None, st=None, **kw):
    base = {"display": "flex", "flexDirection": "column"}
    base.update(st or {})
    return blk("div", children, st=base, **kw)


def row(children=None, st=None, **kw):
    base = {"display": "flex", "flexDirection": "row", "alignItems": "center"}
    base.update(st or {})
    return blk("div", children, st=base, **kw)


def text(el, s, st=None, **kw):
    return blk(el, text=s, st=st, **kw)


def grid(children, n, gap="20px", st=None, tab_n=2, **kw):
    base = {"display": "grid", "gridTemplateColumns": f"repeat({n}, minmax(0, 1fr))", "gap": gap, "width": "100%"}
    base.update(st or {})
    return blk("div", children, st=base, tab={"gridTemplateColumns": f"repeat({min(n, tab_n)}, minmax(0, 1fr))"}, mob={"gridTemplateColumns": "minmax(0, 1fr)"}, **kw)


def container(children, st=None, **kw):
    base = {"display": "flex", "flexDirection": "column", "width": "100%", "maxWidth": "1200px", "paddingLeft": "24px", "paddingRight": "24px", "gap": "24px", "alignItems": "stretch"}
    base.update(st or {})
    return blk("div", children, st=base, mob={"paddingLeft": "18px", "paddingRight": "18px"}, **kw)


def section(sid, children, bg=None, pad="88px", name=None, st=None, dark=False):
    base = {"display": "flex", "flexDirection": "column", "alignItems": "center", "width": "100%", "paddingTop": pad, "paddingBottom": pad,
            "backgroundColor": bg or "#FFFFFF", "color": "#B9C7DD" if dark else c("Text")}
    base.update(st or {})
    return blk("section", [container(children)], st=base, mob={"paddingTop": "56px", "paddingBottom": "56px"}, custom={"id": sid} if sid else {}, name=name or sid)


def inline_svg(markup, prefix):
    """Namespace ids so several inline SVGs can share one page."""
    ids = set(re.findall(r'\bid="([^"]+)"', markup))
    for i in ids:
        markup = markup.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f"url(#{i})", f"url(#{prefix}-{i})").replace(f'"#{i}"', f'"#{prefix}-{i}"')
    markup = markup.replace('aria-labelledby="t d"', f'aria-labelledby="{prefix}-t {prefix}-d"')
    markup = re.sub(r' width="\d+" height="\d+"', "", markup, count=1)
    return markup


def figure(markup, prefix, label, min_w="940px", st=None):
    """Raw-HTML block holding an inline SVG; scrolls sideways on narrow screens instead of shrinking text."""
    svg = inline_svg(markup, prefix)
    html = f'<div class="eih-scroll" role="group" aria-label="{label}"><div class="eih-figure" style="min-width:{min_w}">{svg}</div></div>'
    base = {"width": "100%"}
    base.update(st or {})
    return blk("div", text=html, st=base, raw=True, name=f"figure-{prefix}")


def chip(kind, label=None):
    labs = {"impl": "Implemented", "ext": "Awaiting validation", "arch": "Architecture ready", "plan": "Planned", "pend": "Pending provider docs"}
    return f'<span class="eih-chip eih-{kind}">{label or labs[kind]}</span>'
