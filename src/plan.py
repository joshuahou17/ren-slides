#!/usr/bin/env python3
"""
plan.py — the launch schedule, including the warm-up.

  python3 src/plan.py --start 2026-09-25

Writes POST-PLAN.md and plan.csv. The ramp is deliberately slow: a new account
has no trust, and three campaign posts on day one is the fastest way to get a
month of 40-view videos.
"""
import json, csv, pathlib, argparse, datetime as dt

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLOTS = ["09:00", "14:00", "20:00"]

WARMUP = [
    "scroll your niche 1-2 hours, split across the day (not one sitting)",
    "watch 10+ relevant videos all the way to the end",
    "like 20-30 relevant posts",
    "leave 3-5 real comments (a sentence, not an emoji)",
    "follow 5-10 relevant accounts",
]
SEED_SEARCHES = [
    "why am i always tired", "sleep debt", "oura ring review", "magnesium sleep",
    "supplement stack", "bloodwork results explained", "ferritin fatigue",
    "huberman protocol", "resting heart rate", "zone 2 training",
]
GATE = ("Every post should clear 200 views in its first 24 hours. One weak post "
        "is noise. If the MEDIAN of the last 6 is under 200, do not increase "
        "volume — run the checklist below instead.")
DIAGNOSE = [
    "a community-guidelines strike or a removed video",
    "copyrighted audio on a recent post",
    "a restricted word in a caption (cure, treat, diagnose, disease)",
    "the same edit reused from another account",
    "too much posting too early",
    "almost no For You traffic in analytics (check the traffic-source split)",
]


def phases():
    """(day_from, day_to, posts_per_day, allowed tiers, note)"""
    return [
        (1, 3, 0, [], "Warm-up only. Do not post."),
        (4, 6, 1, ["broad"], "Broad posts. Nothing that mentions the product."),
        (7, 10, 1, ["core"], "First campaign posts, still no CTA of any kind."),
        (11, 17, 2, ["core", "soft", "broad"],
         "Gate cleared → 2/day. Soft CTAs start here. Keep broad posts in the mix; "
         "they are what stops the account narrowing to people who already agree with you."),
        (18, 31, 3, ["core", "soft", "broad", "hard"],
         "Gate cleared → 3/day. Hard CTA at most one a day and no more than one post in ten."),
    ]


def load_decks():
    ds = []
    for p in sorted((ROOT / "content" / "batch01").glob("*.json")):
        d = json.loads(p.read_text())
        ds.append({"slug": d["slug"], "tier": d.get("tier", "core"),
                   "lane": d["lane"], "format": d["format"],
                   "hook": d.get("hook", ""), "n": len(d["slides"])})
    return ds


# Strongest first within each tier: the proof stacks carry the account.
PRIORITY = [
    # broad, widest first — these are buying an audience, not making a point
    "broad-why-so-tired", "broad-sunday-night", "broad-screen-time",
    "broad-coffee-personality", "broad-morning-routine-lie", "broad-gym-year",
    # campaign, strongest first — the proof stacks carry the account
    "app-chronotype", "nof1-sleep-debt-rebound", "stack-huberman-1000h",
    "app-says-no", "nof1-rhr-39", "app-verdict-worked",
    "stack-nine-bottles", "sleep-wake-at-3am", "blood-tired-normal-labs",
    "stack-quit-one", "blood-5-markers-missed",
]


def order(ds, tier):
    pool = [d for d in ds if d["tier"] == tier]
    pool.sort(key=lambda d: (PRIORITY.index(d["slug"]) if d["slug"] in PRIORITY else 99,
                             d["slug"]))
    return pool


def build(start):
    ds = load_decks()
    pools = {t: order(ds, t) for t in ("broad", "core", "soft", "hard")}
    used, rows, hard_count, post_no = set(), [], 0, 0
    hard_today = {}

    def take(tiers, day, allowed):
        """Try the rotated tier order, then anything else the phase allows."""
        nonlocal hard_count
        for t in list(tiers) + [x for x in allowed if x not in tiers]:
            if t == "hard":
                # never before day 14, at most one a day, at most one in ten posts
                if day < 14 or hard_today.get(day) or hard_count * 10 >= post_no:
                    continue
            for d in pools[t]:
                if d["slug"] not in used:
                    used.add(d["slug"])
                    if t == "hard":
                        hard_count += 1
                        hard_today[day] = True
                    return d
        return None

    last_lane = None
    for lo, hi, per_day, tiers, note in phases():
        for day in range(lo, hi + 1):
            date = start + dt.timedelta(days=day - 1)
            if per_day == 0:
                rows.append({"day": day, "date": date.isoformat(), "time": "",
                             "tier": "warm-up", "slug": "", "lane": "", "hook": note})
                continue
            for i in range(per_day):
                # rotate tiers so a day isn't all one thing
                t_order = tiers[i % len(tiers):] + tiers[:i % len(tiers)]
                d = take(t_order, day, tiers)
                if not d:
                    continue
                post_no += 1
                rows.append({"day": day, "date": date.isoformat(), "time": SLOTS[i],
                             "tier": d["tier"], "slug": d["slug"], "lane": d["lane"],
                             "hook": d["hook"]})
                last_lane = d["lane"]
    return rows, ds, used


def write(rows, ds, used, start):
    with (ROOT / "plan.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, ["day", "date", "time", "tier", "slug", "lane", "hook"])
        w.writeheader(); w.writerows(rows)

    L = ["# Post plan", "",
         f"Starting {start.strftime('%A %-d %B %Y')}. Times are ET; TikTok cares more "
         "about consistency than the exact hour, so pick these once and keep them.", ""]

    L += ["## Days 1 to 3 — do not post", "",
          "Confirm the email. Profile photo, username, bio. Two-factor on, passkey if "
          "offered. Then spend three days using the account like a person, spread "
          "across the day rather than in one sitting:", ""]
    L += [f"- {w}" for w in WARMUP]
    L += ["", "Search these so the algorithm learns who the account is for:", "",
          "  " + " · ".join(f"`{q}`" for q in SEED_SEARCHES), "",
          "Engaging with the audience's *problems* is what teaches TikTok the account's "
          "lane. It also shows you which hooks are already working in the niche, which "
          "is free research you'd otherwise guess at.", ""]

    cur = None
    for r in rows:
        if r["tier"] == "warm-up":
            continue
        ph = next(p for p in phases() if p[0] <= r["day"] <= p[1])
        if ph != cur:
            cur = ph
            L += ["", f"## Days {ph[0]} to {ph[1]} — {ph[2]}/day", "", ph[4], "",
                  "| Day | Date | Time | Tier | Deck | Hook |",
                  "|---|---|---|---|---|---|"]
        d = dt.date.fromisoformat(r["date"])
        L.append(f"| {r['day']} | {d.strftime('%a %-d %b')} | {r['time']} | "
                 f"{r['tier']} | `{r['slug']}` | {r['hook'][:58]} |")

    L += ["", "## The gate between every phase", "", GATE, "",
          "```", "python3 src/track.py health", "```", "",
          "If it says HOLD, check for:", ""]
    L += [f"- {d}" for d in DIAGNOSE]
    L += ["", "Warm-up cannot make weak content perform. It gives strong content a "
          "fair first test, which is a different and smaller claim than most people "
          "make for it.", ""]

    scheduled = sum(1 for r in rows if r["slug"])
    last_day = max(r["day"] for r in rows if r["slug"])
    need = 0
    for lo, hi, per, _t, _n in phases():
        need += per * (hi - lo + 1)
    short = need - scheduled
    if short > 0:
        L += ["", "## You run out on day %d" % last_day, "",
              f"The full ramp to day 31 needs **{need} posts**. Batch 01 has "
              f"**{scheduled}**, so you are **{short} decks short** of finishing the "
              "month at 3/day.", "",
              "That is the real constraint on this whole plan, and it is not a design "
              "problem. Two ways to close it, in order of how much they cost you:", "",
              "1. **Clone the winners.** Once a deck clears 100k it is a template, not "
              "a post. Same structure, new subject: `why do i wake up at 3am` becomes "
              "`why am i always cold` becomes `why is my hrv so low`. Five variants of "
              "one proven deck beats fifteen fresh guesses.",
              "2. **Write more broad-tier decks.** They are the fastest to write "
              "because they need no research, and they keep the ratio honest as volume "
              "climbs.", "",
              "Do not close it by posting the same export twice.", ""]

    left = [d["slug"] for d in ds if d["slug"] not in used]
    if left:
        L += ["## Not scheduled yet", "",
              "Held back for the second month, or for a second account once one post "
              "here clears 100k:", ""]
        L += [f"- `{s}`" for s in left] + [""]

    L += ["## If you open a second account", "",
          "Never publish the same export twice. TikTok matches on the file, and a "
          "duplicate reduces the reach of *every* copy, including the original. "
          "Re-render with a different hook and a different opening photo — that's a "
          "two-line change in the deck JSON — and write a fresh caption.", "",
          "```", "# change the hook and the slide-one photo, then:",
          "python3 src/render.py content/batch01/<slug>.json --out out-account2", "```", ""]

    (ROOT / "POST-PLAN.md").write_text("\n".join(L))
    print(f"→ POST-PLAN.md and plan.csv  ({sum(1 for r in rows if r['slug'])} posts "
          f"across {rows[-1]['day']} days)")


a = argparse.ArgumentParser()
a.add_argument("--start", default=dt.date.today().isoformat())
n = a.parse_args()
start = dt.date.fromisoformat(n.start)
rows, ds, used = build(start)
write(rows, ds, used, start)
