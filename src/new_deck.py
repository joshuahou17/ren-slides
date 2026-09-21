#!/usr/bin/env python3
"""
new_deck.py — scaffold an empty deck so you're filling blanks, not staring at JSON.

  python3 src/new_deck.py cause_grid --slug sleep-cant-fall-asleep --lane sleep
  python3 src/new_deck.py nof1_reveal --slug nof1-creatine --lane nof1 --tie soft
"""
import json, argparse, pathlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library import HASHTAGS, REN_TIE

ROOT = pathlib.Path(__file__).resolve().parents[1]

def S(text, sub="", step=None):
    d = {"type": "statement", "text": text, "photo": None}
    if sub: d["sub"] = sub
    if step: d["step"] = step
    return d


SKEL = {
 "cause_grid": [
   {"type": "grid", "question": "“Why do I ...?”", "layout": "g2x2", "cells": [
     {"label": "CAUSE 1", "sub": "one line of mechanism", "tone": "neg", "img": None},
     {"label": "CAUSE 2", "sub": "", "tone": "neg", "img": None},
     {"label": "CAUSE 3", "sub": "", "tone": "neg", "img": None},
     {"label": "CAUSE 4", "sub": "", "tone": "neg", "img": None}]},
   {"type": "grid", "question": "What to change first", "layout": "g2x2", "cells": [
     {"label": "FIX 1", "sub": "", "tone": "pos", "img": None},
     {"label": "FIX 2", "sub": "", "tone": "pos", "img": None},
     {"label": "FIX 3", "sub": "", "tone": "pos", "img": None},
     {"label": "FIX 4", "sub": "", "tone": "pos", "img": None}]},
   S("The mechanism behind cause 1", "one line, no more"),
   S("The mechanism behind cause 2", ""),
   S("A short line with no photo, as a beat"),
   {"type": "cta", "text": "closing line", "sub": "", "photo": None, "pill": None}],
 "problem_solution": [
   {"type": "ps", "kicker": "topic", "bands": [
     {"head": "PROBLEM", "color": "#d93f3e", "cells": [
       {"label": "THING 1", "tone": "neg", "img": None},
       {"label": "THING 2", "tone": "neg", "img": None}]},
     {"head": "SOLUTION", "color": "#0f9d63", "cells": [
       {"label": "FIX 1", "tone": "pos", "img": None},
       {"label": "FIX 2", "tone": "pos", "img": None}]}]},
   S("Why the solution works", "one line"),
   S("The line that reframes it"),
   {"type": "cta", "text": "closing line", "sub": "", "photo": None, "pill": None}],
 "nof1_reveal": [
   {"type": "cover", "kicker": "n-of-1 · experiment 0XX",
    "text": "I did X every night for 14 nights.", "sub": "Here's the chart."},
   {"type": "protocol", "title": "X → metric", "rows": [
     [" what ", ""], [" when ", ""], [" baseline ", "7 nights, nothing"],
     [" trial ", "14 nights"], [" measured by ", ""]],
    "success_rule": "Average <metric> goes up by N. Anything under that is noise."},
   {"type": "chart", "title": "<metric>, nightly", "unit": "min",
    "baseline_label": "baseline", "trial_label": "on X", "split": 7,
    "series": [0] * 21},
   {"type": "verdict", "text": "worked", "note": ""},
   S("The line that stops it being a supplement ad"),
   {"type": "cta", "text": "", "sub": "", "photo": None, "pill": None}],
 "proof_stack": [
   S("My <metric> is <N>.", "Everything that actually did it, ranked honestly."),
   {"type": "proof", "stat": "<N>", "stat_unit": "<unit>",
    "img": "<your-screenshot.jpg>", "caption": "<source, date range, range>"},
   S("The boring cause", "put the real one first", step="01"),
   S("The second cause", "", step="02"),
   S("The third cause", "", step="03"),
   S("The supplement people came for", "say plainly how small it is"),
   S("And the part I can't take credit for", "genetics, years, luck"),
   {"type": "cta", "text": "Your number isn't my number.",
    "sub": "", "pill": None, "photo": None}],
 "photo_listicle": [
   S("The hook, as a sentence someone would stop on"),
   S("Item one", "one line", step="01"),
   S("Item two", "", step="02"),
   S("Item three", "", step="03"),
   S("Item four", "", step="04"),
   S("Item five", "", step="05"),
   S("The line that undercuts your own list"),
   {"type": "cta", "text": "closing line", "sub": "", "photo": None, "pill": None}],
}

a = argparse.ArgumentParser()
a.add_argument("format", choices=SKEL)
a.add_argument("--slug", required=True)
a.add_argument("--lane", required=True, choices=["sleep", "bloodwork", "nof1"])
a.add_argument("--tie", default="none", choices=list(REN_TIE))
a.add_argument("--batch", default="batch02")
n = a.parse_args()

deck = {"slug": n.slug, "lane": n.lane, "format": n.format, "ren_tie": n.tie,
        "hook": "", "caption": "", "notes": "what this post is testing",
        "hashtags": HASHTAGS[n.lane] + HASHTAGS["always"],
        "slides": SKEL[n.format]}
if REN_TIE[n.tie]["cta"]:
    deck["cta"] = REN_TIE[n.tie]["cta"]

d = ROOT / "content" / n.batch
d.mkdir(parents=True, exist_ok=True)
p = d / f"{n.slug}.json"
p.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n")
print(f"→ {p.relative_to(ROOT)}\n  fill it in, then: python3 src/render.py {p.relative_to(ROOT)}")
