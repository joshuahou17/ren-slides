#!/usr/bin/env python3
"""
review.py — build the approval board for a rendered batch.

  python3 src/review.py                 -> out/review.html (open it locally)
  python3 src/review.py --prefix slides -> image paths rewritten for publishing
"""
import json, pathlib, argparse, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = pathlib.Path(__file__).resolve().parents[1]
LANE = {"sleep": ("Sleep & recovery", "lane-sleep"),
        "bloodwork": ("Bloodwork", "lane-blood"),
        "nof1": ("n-of-1", "lane-nof1"),
        "stack": ("The stack problem", "lane-stack")}
FMT = {"cause_grid": "Cause grid", "problem_solution": "Problem → Solution",
       "nof1_reveal": "n-of-1 reveal", "photo_listicle": "Photo listicle"}

HEAD = """<title>Ren Slide Board</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{
  --paper:#f2f1ee; --card:#ffffff; --ink:#16181a; --ink-2:#585c5f; --ink-3:#8b8f92;
  --line:#dedcd6; --well:#eceae4;
  --accent:#0d8a58; --sleep:#4a3aa7; --blood:#2a78d6; --nof1:#0d8a58; --hard:#b4740a;
  --shadow:0 1px 2px rgba(20,22,24,.06),0 8px 24px rgba(20,22,24,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#111315; --card:#1b1e20; --ink:#f0efec; --ink-2:#a9aeb1; --ink-3:#71777a;
  --line:#2c3033; --well:#242829;
  --accent:#3fc48d; --sleep:#9085e9; --blood:#5598e7; --nof1:#3fc48d; --hard:#e0a63c;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.34);
}}
:root[data-theme="dark"]{
  --paper:#111315; --card:#1b1e20; --ink:#f0efec; --ink-2:#a9aeb1; --ink-3:#71777a;
  --line:#2c3033; --well:#242829;
  --accent:#3fc48d; --sleep:#9085e9; --blood:#5598e7; --nof1:#3fc48d; --hard:#e0a63c;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.34);
}
*{box-sizing:border-box;}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:Archivo,"Helvetica Neue",Arial,sans-serif;font-size:15px;line-height:1.45;}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px;padding-block:28px 72px;}
h1{font-size:clamp(28px,4vw,40px);font-weight:800;letter-spacing:-.03em;margin:0;
  text-wrap:balance;}
.lede{color:var(--ink-2);max-width:62ch;margin:10px 0 0;}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--paper);
  border-bottom:1px solid var(--line);margin:26px -20px 0;padding:12px 20px;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;}
.bar .lbl{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-right:2px;}
.chip{font:inherit;font-size:13px;font-weight:500;border:1px solid var(--line);
  background:var(--card);color:var(--ink-2);border-radius:999px;padding:5px 13px;cursor:pointer;}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink);}
.chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
.count{margin-left:auto;font-size:13px;color:var(--ink-3);font-variant-numeric:tabular-nums;}

.deck{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:26px;
  padding:26px 0;border-bottom:1px solid var(--line);align-items:start;}
@media(max-width:760px){.deck{grid-template-columns:1fr;gap:16px;}}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;}
.tag{font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
  padding:3px 9px;border-radius:5px;background:var(--well);color:var(--ink-2);}
.tag.lane-sleep{color:var(--sleep);} .tag.lane-blood{color:var(--blood);}
.tag.lane-nof1{color:var(--nof1);} .tag.lane-stack{color:var(--hard);}
.tag.tie-hard{color:var(--hard);border:1px solid currentColor;background:transparent;}
.tag.tier-broad{color:var(--ink-2);border:1px dashed var(--line);background:transparent;}
.tag.sched{background:var(--ink);color:var(--paper);}
.hook{font-size:19px;font-weight:600;letter-spacing:-.015em;margin:0 0 8px;text-wrap:balance;}
.slug{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11.5px;color:var(--ink-3);
  margin-bottom:14px;}
.note{font-size:13.5px;color:var(--ink-2);border-left:2px solid var(--line);padding-left:11px;
  margin:0 0 14px;}
.capwrap{display:flex;flex-direction:column;align-items:flex-start;gap:8px;}
.cap{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;line-height:1.6;
  background:var(--well);border:1px solid var(--line);border-radius:9px;padding:12px;
  white-space:pre-wrap;color:var(--ink-2);max-height:200px;overflow:auto;align-self:stretch;}
.copy{font:inherit;font-size:12px;font-weight:600;
  border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:7px;
  padding:5px 11px;cursor:pointer;}
.copy:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
.strip{display:flex;gap:12px;overflow-x:auto;padding-bottom:6px;}
.strip figure{margin:0;flex:0 0 auto;width:168px;}
.strip img{display:block;width:100%;aspect-ratio:4/5;max-width:100%;object-fit:cover;
  border-radius:9px;border:1px solid var(--line);background:var(--card);box-shadow:var(--shadow);
  cursor:zoom-in;}
.strip figcaption{font-size:11px;color:var(--ink-3);margin-top:5px;
  font-variant-numeric:tabular-nums;}
dialog{border:0;padding:0;background:transparent;max-width:none;max-height:none;}
dialog::backdrop{background:rgba(10,11,12,.86);}
dialog img{max-width:min(92vw,520px);max-height:88vh;border-radius:12px;display:block;}
.foot{color:var(--ink-3);font-size:13px;padding-top:26px;max-width:62ch;}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;}}
</style>"""


def build(decks, prefix):
    parts = [HEAD, '<div class="wrap">',
             '<h1>Batch 01</h1>',
             '<p class="lede">Every slide of every deck, with the caption ready to copy. '
             'Ordered by the day they post. Three warm-up days first, then broad posts that sell nothing, '
             'then the campaign decks as the volume ramps. '
             'Approve here, post from your phone, then log the numbers with '
             '<code>track.py</code>.</p>',
             '<div class="bar"><span class="lbl">Lane</span>']
    for k, (lab, _) in LANE.items():
        parts.append(f'<button class="chip" data-f="lane" data-v="{k}" aria-pressed="false">{lab}</button>')
    parts.append('<span class="lbl" style="margin-left:10px">Format</span>')
    for k, lab in FMT.items():
        parts.append(f'<button class="chip" data-f="format" data-v="{k}" aria-pressed="false">{lab}</button>')
    parts.append('<span class="count" id="count"></span></div>')

    for d in decks:
        lane_lab, lane_cls = LANE.get(d["lane"], (d["lane"], ""))
        tie = d.get("ren_tie", "none")
        tie_tag = (f'<span class="tag tie-{tie}">{"hard CTA" if tie=="hard" else tie+" CTA" if tie=="soft" else "no CTA"}</span>')
        parts.append(f'<article class="deck" data-lane="{d["lane"]}" data-format="{d["format"]}">')
        parts.append('<div>')
        sc = d.get("sched")
        sched_tag = (f'<span class="tag sched">day {sc[0]} · {sc[2]}</span>' if sc
                     else '<span class="tag">unscheduled</span>')
        tier_tag = ('<span class="tag tier-broad">warm-up, sells nothing</span>'
                    if d.get("tier") == "broad" else "")
        parts.append(f'<div class="tags">{sched_tag}<span class="tag {lane_cls}">{lane_lab}</span>'
                     f'<span class="tag">{FMT.get(d["format"], d["format"])}</span>{tie_tag}'
                     f'{tier_tag}<span class="tag">{len(d["shots"])} slides</span></div>')
        parts.append(f'<p class="hook">{html.escape(d.get("hook") or d["slug"])}</p>')
        parts.append(f'<div class="slug">{d["slug"]}</div>')
        if d.get("notes"):
            parts.append(f'<p class="note">{html.escape(d["notes"])}</p>')
        parts.append(f'<div class="capwrap"><div class="cap" id="cap-{d["slug"]}">'
                     f'{html.escape(d["caption_text"])}</div>'
                     f'<button class="copy" data-for="cap-{d["slug"]}">Copy caption</button></div>')
        parts.append('</div><div class="strip">')
        for i, s in enumerate(d["shots"], 1):
            parts.append(f'<figure><img src="{prefix}/{d["slug"]}/{s}" loading="lazy" '
                         f'alt="Slide {i} of {d["slug"]}"><figcaption>{i} / {len(d["shots"])}</figcaption></figure>')
        parts.append('</div></article>')

    parts.append('<p class="foot">Charts in the n-of-1 decks use placeholder series. '
                 'Swap in your own Oura / Apple Health export before any of those go out — '
                 'the credibility of the whole account rests on those numbers being real.</p>')
    parts.append('</div><dialog id="lb"><img alt=""></dialog>')
    parts.append("""<script>
const chips=[...document.querySelectorAll('.chip')],decks=[...document.querySelectorAll('.deck')],
      count=document.getElementById('count');
function apply(){
  const on={lane:new Set(),format:new Set()};
  chips.forEach(c=>{if(c.getAttribute('aria-pressed')==='true')on[c.dataset.f].add(c.dataset.v);});
  let n=0;
  decks.forEach(d=>{
    const ok=(!on.lane.size||on.lane.has(d.dataset.lane))&&(!on.format.size||on.format.has(d.dataset.format));
    d.hidden=!ok; if(ok)n++;
  });
  count.textContent=n+' of '+decks.length+' decks';
}
chips.forEach(c=>c.addEventListener('click',()=>{
  c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');apply();}));
apply();
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{
  const t=document.getElementById(b.dataset.for).textContent;
  try{await navigator.clipboard.writeText(t);b.textContent='Copied';}
  catch(e){const r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.for));
    getSelection().removeAllRanges();getSelection().addRange(r);b.textContent='Select + copy';}
  setTimeout(()=>b.textContent='Copy caption',1600);}));
const lb=document.getElementById('lb');
document.querySelectorAll('.strip img').forEach(i=>i.addEventListener('click',()=>{
  lb.querySelector('img').src=i.src;lb.querySelector('img').alt=i.alt;lb.showModal();}));
lb.addEventListener('click',()=>lb.close());
</script>""")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="batch01")
    ap.add_argument("--prefix", default="../out" if False else "slides")
    ap.add_argument("--out", default=str(ROOT / "out" / "review.html"))
    ap.add_argument("--embed", action="store_true",
                    help="inline every PNG as a data URI (self-contained page)")
    a = ap.parse_args()

    sched = {}
    planp = ROOT / "plan.csv"
    if planp.exists():
        import csv as _csv
        with planp.open() as f:
            for r in _csv.DictReader(f):
                if r["slug"]:
                    sched[r["slug"]] = (r["day"], r["date"], r["time"])

    decks = []
    for p in sorted((ROOT / "content" / a.batch).glob("*.json")):
        d = json.loads(p.read_text())
        od = ROOT / "out" / d["slug"]
        if not od.exists():
            continue
        d["shots"] = sorted(f.name for f in od.glob("*.png"))
        d["caption_text"] = (od / "caption.txt").read_text().strip()
        d["sched"] = sched.get(d["slug"])
        decks.append(d)
    decks.sort(key=lambda d: (int(d["sched"][0]) if d.get("sched") else 999,
                              d["lane"], d["format"]))
    page = build(decks, a.prefix)
    if a.embed:
        import base64, re, io
        from PIL import Image
        def sub(m):
            f = ROOT / "out" / m.group(1) / m.group(2)
            im = Image.open(f).convert("RGB")
            im.thumbnail((520, 650), Image.LANCZOS)
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=76, optimize=True)
            return 'src="data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode() + '"'
        page = re.sub(r'src="\./([^/"]+)/([^"]+)"', sub, page)
    pathlib.Path(a.out).write_text(page)
    print(f"→ {a.out}  ({len(decks)} decks, prefix={a.prefix})")


main()
