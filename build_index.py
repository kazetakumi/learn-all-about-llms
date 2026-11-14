"""Regenerate lessons/index.html from syllabus.json. Run: python3 build_index.py"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
s = json.loads((ROOT / "syllabus.json").read_text())
MARK = {"done": "✓", "current": "▶"}


def item(x):
    status = x.get("status", "planned")
    title = escape(x["title"])
    lesson = x.get("lesson")
    if lesson and (ROOT / "lessons" / lesson).exists():
        title = f'<a href="{escape(lesson)}">{title}</a>'
    covers = " · ".join(escape(c) for c in x.get("covers", []))
    subs = "".join(item(c) for c in x.get("cruxes", []))
    papers = "".join(f'<li><a href="{escape(r["url"])}">{escape(r["title"])}</a></li>' for r in x.get("papers", []))
    return (
        f'<li class="{status}"><span class="mark">{MARK.get(status, "")}</span>'
        f'<span class="id">{escape(x["id"])}</span> {title}'
        f'<div class="hook">{escape(x.get("hook", ""))}</div>'
        + (f'<div class="covers">{covers}</div>' if covers else "")
        + (f'<ol class="cruxes">{subs}</ol>' if subs else "")
        + (f'<ul class="papers">{papers}</ul>' if papers else "")
        + "</li>"
    )


body = []
for p in s["phases"]:
    tag = " <span class='tag'>parked</span>" if p["status"] == "parked" else ""
    body.append(f'<h2><span class="label">Phase {escape(p["id"])}</span> {escape(p["title"])}{tag}</h2>')
    body.append('<ol class="ladder">' + "".join(item(x) for x in p["parts"]) + "</ol>")

body.append('<h2><span class="label">Branches</span> Prerequisite detours</h2>')
body.append(
    '<ol class="ladder">' + "".join(item(b) for b in s["branches"]) + "</ol>"
    if s["branches"] else '<p class="empty">None yet. A branch opens when a gap shows up.</p>'
)

body.append('<h2><span class="label">Appendix</span> Notes</h2>')
if s["notes"]:
    groups = {}
    for n in s["notes"]:
        groups.setdefault(n["crux"], []).append(n)
    for crux, ns in groups.items():
        body.append(f"<h3>{escape(crux)}</h3><dl>")
        body += [f'<dt>{escape(n["label"])}</dt><dd>{escape(n["note"])}</dd>' for n in ns]
        body.append("</dl>")
else:
    body.append('<p class="empty">No notes yet. Each cleared doubt is recorded here.</p>')

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(s["subject"])}</title>
<style>
:root {{ --paper:#fbfaf6; --ink:#2b2620; --soft:#6b6358; --rule:#e4dfd3; --accent:#355070; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink);
  font:18px/1.6 'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif; }}
main {{ max-width:640px; margin:0 auto; padding:64px 20px 96px; }}
h1 {{ font-size:2rem; line-height:1.2; margin:0 0 .5rem; font-weight:normal; }}
.goal {{ color:var(--soft); margin:0 0 3rem; }}
h2 {{ font-weight:normal; font-size:1.35rem; margin:3rem 0 1rem; border-top:1px solid var(--rule); padding-top:1.5rem; }}
h3 {{ font-weight:normal; color:var(--accent); margin:1.5rem 0 .5rem; }}
.label {{ display:block; font-size:.75rem; letter-spacing:.12em; text-transform:uppercase; color:var(--accent); }}
.tag {{ font-size:.8rem; color:var(--soft); border:1px solid var(--rule); padding:0 .4em; border-radius:3px; }}
ol {{ list-style:none; padding:0; margin:0; }}
li {{ position:relative; padding:.6rem 0 .6rem 2.2rem; }}
.cruxes li {{ padding-left:1.8rem; font-size:.95rem; }}
.cruxes {{ margin-top:.4rem; border-left:1px solid var(--rule); }}
.mark {{ position:absolute; left:0; width:1.6rem; color:var(--accent); }}
.id {{ color:var(--soft); font-variant-numeric:tabular-nums; margin-right:.3rem; }}
.hook {{ color:var(--soft); font-style:italic; font-size:.95rem; }}
.covers {{ color:var(--soft); font-size:.85rem; }}
li.planned > .id, li.planned {{ opacity:.55; }}
li.current {{ opacity:1; }}
li.current > .id {{ color:var(--accent); }}
a {{ color:var(--accent); }}
.papers {{ list-style:none; padding:0; margin:.4rem 0 0; font-size:.85rem; }} .papers li {{ padding:.1rem 0 .1rem 1rem; }}
.empty {{ color:var(--soft); font-style:italic; }}
dt {{ font-weight:bold; margin-top:.8rem; }} dd {{ margin:0 0 0 1.2rem; }}
</style></head><body><main>
<h1>{escape(s["subject"])}</h1>
<p class="goal">{escape(s["goal"])}</p>
{"".join(body)}
</main></body></html>
"""
(ROOT / "lessons" / "index.html").write_text(html)
print("wrote lessons/index.html")
