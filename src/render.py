#!/usr/bin/env python3
"""
render.py — deck JSON -> finished slide PNGs + caption file.

  python3 src/render.py content/*.json
  python3 src/render.py content/ --height 1920     # full 9:16
"""
import sys, os, json, base64, mimetypes, argparse, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml
from jinja2 import Template
from chart import nof1_svg

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_brand():
    cfg = yaml.safe_load((ROOT / "brand.yaml").read_text())
    return cfg["brand"], cfg["canvas"], cfg["output"]


def data_uri(path):
    if not path:
        return None
    p = pathlib.Path(path)
    if not p.is_absolute():
        for cand in (ROOT / path, ROOT / "assets" / "photos" / path):
            if cand.exists():
                p = cand
                break
    if not p.exists():
        print(f"    ! missing image {path} — falling back to a type tile")
        return None
    mime = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def _find(path):
    p = pathlib.Path(path)
    if p.exists():
        return p
    for cand in (ROOT / path, ROOT / "assets" / "photos" / path):
        if cand.exists():
            return cand
    return None


def resolve_images(deck):
    for s in deck["slides"]:
        if s.get("photo"):
            f = _find(s["photo"])
            a, b_, c = scrim_for(f) if f else (.50, .58, .66)
            s["scrim"] = (f"linear-gradient(180deg,rgba(0,0,0,{a}) 0%,"
                          f"rgba(0,0,0,{b_}) 45%,rgba(0,0,0,{c}) 100%)")
            s["photo"] = data_uri(s["photo"])
        if s.get("type") in ("proof",) and s.get("img"):
            s["img"] = data_uri(s["img"])
        for key in ("cells",):
            for c in s.get(key, []) or []:
                c["img"] = data_uri(c.get("img"))
        for band in s.get("bands", []) or []:
            for c in band.get("cells", []) or []:
                c["img"] = data_uri(c.get("img"))


def scrim_for(path):
    """Match the scrim to the photo so a dark shot doesn't go to mud."""
    from PIL import Image, ImageStat
    try:
        im = Image.open(path).convert("L")
        im.thumbnail((160, 160))
        mean = ImageStat.Stat(im).mean[0]
    except Exception:
        mean = 110
    if mean < 62:    return (.26, .32, .44)
    if mean < 100:   return (.40, .46, .56)
    if mean < 150:   return (.50, .58, .66)
    return (.58, .66, .74)


def size_text(deck):
    """Conversational hooks run long. Step the type down so they still fit."""
    for s in deck["slides"]:
        if s.get("type") != "statement":
            continue
        n = len(s.get("text", ""))
        s["size_px"] = (96 if n <= 24 else 82 if n <= 42 else 68 if n <= 68 else
                        56 if n <= 100 else 48 if n <= 140 else 42)
        s["sub_px"] = max(28, min(40, round(s["size_px"] * 0.50)))


def build_charts(deck, b):
    """Turn any chart slide's raw series into SVG + hero numbers."""
    for s in deck["slides"]:
        if s.get("type") != "chart":
            continue
        svg, bm, tm = nof1_svg(
            s["series"], s["split"], b, s.get("unit", ""),
            baseline_label=s.get("baseline_label", "baseline"),
            trial_label=s.get("trial_label", "on protocol"),
        )
        d = tm - bm
        pct = (d / bm * 100) if bm else 0
        s["svg"] = svg
        s["delta_label"] = f"{'+' if d >= 0 else ''}{d:.0f}" if abs(d) >= 10 else f"{'+' if d>=0 else ''}{d:.1f}"
        s["delta_color"] = b["worked"] if d > 0 else b["failed"]
        s.setdefault("delta_sub",
                     f"{'+' if pct>=0 else ''}{pct:.0f}% vs baseline · "
                     f"{len(s['series'])} nights, same room, same bedtime window")
        s.setdefault("baseline_label", "baseline")
        s.setdefault("trial_label", "on protocol")


VERDICT_COLORS = {"worked": "worked", "partly worked": "partly",
                  "didn't work": "failed", "not enough data": "unclear"}


def apply_verdicts(deck, b):
    for s in deck["slides"]:
        if s.get("type") == "verdict" and "color" not in s:
            key = VERDICT_COLORS.get(s["text"].strip().lower(), "unclear")
            s["color"] = b[key]


def caption_text(deck, b):
    tags = " ".join("#" + t for t in deck.get("hashtags", []))
    parts = [deck.get("caption", "").strip()]
    if deck.get("cta"):
        parts.append(deck["cta"].strip())
    parts.append(tags)
    return "\n\n".join(p for p in parts if p) + "\n"


def render_deck(path, W, H, outdir, headless_ctx):
    b, canvas, _ = load_brand()
    deck = json.loads(pathlib.Path(path).read_text())
    resolve_images(deck)
    build_charts(deck, b)
    size_text(deck)
    apply_verdicts(deck, b)

    css = (ROOT / "formats" / "base.css").read_text()
    css = css.replace("FONT_INTER_I", (ROOT / "fonts" / "InterVariable-Italic.ttf").as_uri())
    css = css.replace("FONT_INTER", (ROOT / "fonts" / "InterVariable.ttf").as_uri())

    tpl = Template((ROOT / "formats" / "deck.html").read_text())
    html = tpl.render(deck=deck, b=b, base_css=css, W=W, H=H, pad=int(W * 0.0667))

    dest = pathlib.Path(outdir) / deck["slug"]
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "_preview.html").write_text(html)

    page = headless_ctx.new_page()
    page.set_viewport_size({"width": W + 80, "height": H + 80})
    page.goto((dest / "_preview.html").as_uri(), wait_until="networkidle")
    page.wait_for_timeout(250)
    slides = page.query_selector_all(".slide")
    for i, el in enumerate(slides, 1):
        el.screenshot(path=str(dest / f"{i:02d}.png"))
    page.close()

    (dest / "caption.txt").write_text(caption_text(deck, b))
    (dest / "meta.json").write_text(json.dumps(
        {k: deck.get(k) for k in ("slug", "format", "lane", "hook", "ren_tie", "notes")},
        indent=2) + "\n")
    return deck["slug"], len(slides)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--height", type=int)
    ap.add_argument("--width", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()

    _, canvas, outcfg = load_brand()
    W = a.width or canvas["width"]
    H = a.height or canvas["height"]
    outdir = a.out or (ROOT / outcfg["dir"])

    files = []
    for p in a.paths:
        p = pathlib.Path(p)
        files += sorted(p.glob("*.json")) if p.is_dir() else [p]

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--force-color-profile=srgb",
                                      "--font-render-hinting=none"])
        ctx = br.new_context(device_scale_factor=1)
        for f in files:
            slug, k = render_deck(f, W, H, outdir, ctx)
            print(f"  ✓ {slug:<38} {k} slides  → out/{slug}/")
        br.close()
    print(f"\n{len(files)} decks rendered at {W}x{H}.")


if __name__ == "__main__":
    main()
