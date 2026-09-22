#!/usr/bin/env python3
"""
prep_photo.py — turn a raw phone photo into a slide-ready asset.

  python3 src/prep_photo.py <in.jpg> <out-name.jpg> --head 0.33 [--target 78]
                            [--x 0.5] [--scale 0.86] [--mono]

Crops to 4:5 with the subject's head anchored wherever you want it, then
normalises the exposure so every photo in the library sits at the same tonal
level. The renderer computes its scrim from the photo's own brightness, so the
text stays readable either way.

`anchor` is the fraction of the FINISHED frame the head lands at. The hook
headline sits at 0.38-0.56, so an anchor in that range puts the text across the
face, which is the look these accounts use — it keeps the person anonymous and
stops the face competing with the hook for attention. `head` is the same
fraction measured on the SOURCE photo, so the two together say "this is where
his head is, put it there". Neither is guessable from the file: shoot, run it,
look at the render, adjust. assets/photo-recipes.json records what each photo in
the library was run with.
"""
import argparse, pathlib
from PIL import Image, ImageOps, ImageEnhance, ImageStat


def prep(src, out, head=0.33, target=78, contrast=1.06, sat=0.94, scale=0.86,
         width=1400, floor=0.45, ceil_=1.40, x=0.5, anchor=0.45):
    """`target` is the mean luminance every photo is normalised to (0-255), so a
    bright bathroom and a dark elevator end up at the same tonal level. That
    consistency is what makes a profile grid read as one account rather than a
    folder. The multiplier is clamped so a very bright source isn't crushed."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    Hc = int(h * scale); Wc = int(Hc * 0.8)
    if Wc > w:
        Wc = w; Hc = int(Wc / 0.8)
    left = max(0, min(w - Wc, int(x * w - Wc / 2)))
    top = max(0, min(h - Hc, int(head * h - anchor * Hc)))
    im = im.crop((left, top, left + Wc, top + Hc))
    # Always land on the same pixel size. A tight crop of a distant subject
    # has fewer source pixels than a close one; the slide is 1080 wide either
    # way, so resize rather than thumbnail (which only ever shrinks).
    im = im.resize((int(width * 0.8), width), Image.LANCZOS)
    mean = ImageStat.Stat(im.convert("L")).mean[0]
    factor = max(floor, min(ceil_, target / max(mean, 1)))
    im = ImageEnhance.Brightness(im).enhance(factor)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(sat)
    im.save(out, "JPEG", quality=90, optimize=True)
    return im.size


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("src"); a.add_argument("out")
    a.add_argument("--head", type=float, default=0.33)
    a.add_argument("--target", type=float, default=78,
                   help="mean luminance to normalise to, 0-255")
    a.add_argument("--scale", type=float, default=0.86)
    a.add_argument("--x", type=float, default=0.5,
                   help="horizontal centre of the crop, 0-1 (default centred)")
    a.add_argument("--mono", action="store_true",
                   help="strip colour. Use on a photo whose background is busy "
                        "and colourful — killing the hue collapses the clutter "
                        "into one dark surface so the text has somewhere to sit.")
    n = a.parse_args()
    sat = 0.0 if n.mono else 0.94
    contrast = 1.10 if n.mono else 1.06
    print(n.out, prep(n.src, n.out, n.head, n.target, contrast=contrast,
                      sat=sat, scale=n.scale, x=n.x))
