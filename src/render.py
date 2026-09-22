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

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_brand():
    """Brand constants were removed. Only the mechanical bits remain."""
    cfg = yaml.safe_load((ROOT / "brand.yaml").read_text())
    return {}, cfg["canvas"], cfg["output"]


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


SWIPE = "(Swipe right \u2192)"


def apply_hook_style(deck, style):
    """Style A is the first-person confession already in slide one.
    Style B is the direct-address promise stored alongside it."""
    if style != "b":
        return
    if deck.get("hook_b") and deck["slides"][0].get("type") == "statement":
        deck["slides"][0]["text"] = deck["hook_b"]
        deck["slides"][0]["sub"] = deck.get("hook_b_sub", "")
        deck["hook"] = deck["hook_b"]


def add_swipe(deck):
    """Slide one always tells the viewer there is more. Costs nothing, and the
    swipe is the signal the algorithm actually reads."""
    first = deck["slides"][0]
    if first.get("type") == "statement":
        first.setdefault("swipe", SWIPE)


def size_text(deck):
    """Conversational hooks run long. Step the type down so they still fit."""
    for s in deck["slides"]:
        if s.get("type") != "statement":
            continue
        n = len(s.get("text", ""))
        s["size_px"] = (96 if n <= 24 else 82 if n <= 42 else 68 if n <= 68 else
                        56 if n <= 100 else 48 if n <= 140 else 42)
        s["sub_px"] = max(28, min(40, round(s["size_px"] * 0.50)))


def validate(deck):
    """House rules that now FAIL a render instead of merely advising against it."""
    errs = []
    for n, sl in enumerate(deck["slides"], 1):
        t = sl.get("type")
        if t in ("chart", "verdict", "list"):
            errs.append(f"slide {n}: `{t}` was removed. Charts and verdicts must come "
                        f"from a real app screenshot on a `proof` slide.")
        if t in ("statement", "cta", "protocol") and not sl.get("photo"):
            errs.append(f"slide {n}: `{t}` needs a photo. Type-only slides are gone.")
        if t == "grid":
            missing = [c.get("label", "?") for c in sl.get("cells", []) if not c.get("img")]
            if missing:
                errs.append(f"slide {n}: every grid cell needs an image. Missing: "
                            + ", ".join(missing))
        if t == "ps":
            for bi, band in enumerate(sl.get("bands", [])):
                missing = [c.get("label", "?") for c in band.get("cells", []) if not c.get("img")]
                if missing:
                    errs.append(f"slide {n}: every problem/solution panel needs an image. "
                                f"Missing: " + ", ".join(missing))
        if t == "proof" and not sl.get("img"):
            errs.append(f"slide {n}: `proof` needs a screenshot.")
    if errs:
        raise SystemExit("\n  ".join([f"REFUSED {deck['slug']}:"] + errs))


def caption_text(deck, b):
    tags = " ".join("#" + t for t in deck.get("hashtags", []))
    parts = [deck.get("caption", "").strip()]
    if deck.get("cta"):
        parts.append(deck["cta"].strip())
    parts.append(tags)
    return "\n\n".join(p for p in parts if p) + "\n"


def render_deck(path, W, H, outdir, headless_ctx, hook_style="a"):
    b, canvas, _ = load_brand()
    deck = json.loads(pathlib.Path(path).read_text())
    resolve_images(deck)
    validate(deck)
    apply_hook_style(deck, hook_style)
    add_swipe(deck)
    size_text(deck)

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
    ap.add_argument("--hook", choices=["a", "b"], default="a",
                    help="a = first-person confession (default), b = direct-address promise")
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
            slug, k = render_deck(f, W, H, outdir, ctx, a.hook)
            print(f"  ✓ {slug:<38} {k} slides  → out/{slug}/")
        br.close()
    print(f"\n{len(files)} decks rendered at {W}x{H}.")


if __name__ == "__main__":
    main()
