#!/usr/bin/env python3
"""
track.py — the experiment loop. Without this the account is just vibes.

  python3 src/track.py log sleep-wake-at-3am --views 8400 --likes 610 --follows 44 --saves 320
  python3 src/track.py report
  python3 src/track.py next          # what to make more of, what to kill

Data lives in posts.csv so you can also just edit it in a spreadsheet.
"""
import csv, sys, json, pathlib, argparse, statistics as st, datetime as dt

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "posts.csv"
COLS = ["date", "slug", "lane", "format", "ren_tie", "hook",
        "views", "likes", "saves", "shares", "comments", "follows", "url"]


def meta_for(slug):
    for p in (ROOT / "content").rglob(f"{slug}.json"):
        d = json.loads(p.read_text())
        return {k: d.get(k, "") for k in ("lane", "format", "ren_tie", "hook")}
    return {"lane": "", "format": "", "ren_tie": "", "hook": ""}


def rows():
    if not CSV.exists():
        return []
    with CSV.open() as f:
        return [r for r in csv.DictReader(f)]


def write(rs):
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rs)


def cmd_log(a):
    rs = rows()
    m = meta_for(a.slug)
    rec = {"date": a.date or dt.date.today().isoformat(), "slug": a.slug, **m,
           "views": a.views, "likes": a.likes, "saves": a.saves, "shares": a.shares,
           "comments": a.comments, "follows": a.follows, "url": a.url or ""}
    rs = [r for r in rs if r["slug"] != a.slug] + [rec]
    write(rs)
    print(f"logged {a.slug}: {a.views:,} views, {a.follows} follows "
          f"({(a.follows/a.views*100) if a.views else 0:.2f}% follow rate)")


def num(r, k):
    try:
        return float(r[k] or 0)
    except ValueError:
        return 0.0


def group(rs, key):
    g = {}
    for r in rs:
        g.setdefault(r[key] or "?", []).append(r)
    return g


def summarize(rs):
    v = [num(r, "views") for r in rs]
    f = sum(num(r, "follows") for r in rs)
    s = sum(num(r, "saves") for r in rs)
    tv = sum(v) or 1
    return {"n": len(rs), "median": st.median(v) if v else 0, "best": max(v) if v else 0,
            "follow_rate": f / tv * 100, "save_rate": s / tv * 100}


def table(title, g):
    print(f"\n{title}")
    print(f"  {'':<20}{'n':>4}{'median':>10}{'best':>10}{'follow%':>10}{'save%':>9}")
    for k, rs in sorted(g.items(), key=lambda kv: -summarize(kv[1])["median"]):
        s = summarize(rs)
        print(f"  {k:<20}{s['n']:>4}{s['median']:>10,.0f}{s['best']:>10,.0f}"
              f"{s['follow_rate']:>10.2f}{s['save_rate']:>9.2f}")


def cmd_report(a):
    rs = rows()
    if not rs:
        return print("posts.csv is empty. Log a post first.")
    print(f"{len(rs)} posts logged.")
    table("BY FORMAT", group(rs, "format"))
    table("BY LANE", group(rs, "lane"))
    table("BY REN TIE", group(rs, "ren_tie"))
    print("\nTOP 5")
    for r in sorted(rs, key=lambda r: -num(r, "views"))[:5]:
        print(f"  {num(r,'views'):>9,.0f}  {r['format']:<18} {r['slug']}")


def cmd_next(a):
    rs = rows()
    if len(rs) < 9:
        return print(f"Only {len(rs)} posts logged. The kill rule needs 9 per format "
                     f"before any of this means anything. Keep shipping.")
    gf = group(rs, "format")
    print("\nVERDICTS\n")
    for k, g in gf.items():
        s = summarize(g)
        if s["n"] < 9:
            print(f"  {k:<20} HOLD    only {s['n']} posts — needs {9-s['n']} more")
        elif s["median"] < 3000:
            print(f"  {k:<20} KILL    median {s['median']:,.0f} — stop making these")
        elif s["best"] >= 100000:
            print(f"  {k:<20} CLONE   a post cleared {s['best']:,.0f} — this is a "
                  f"template now, run it across the other lanes")
        else:
            print(f"  {k:<20} KEEP    median {s['median']:,.0f} — iterate the hook, "
                  f"not the format")
    winners = [r for r in rs if num(r, "views") >= 100000]
    if winners:
        print(f"\n{len(winners)} post(s) over 100k. Second-account rule is satisfied "
              f"at 3 — you have {len(winners)}.")
        for r in winners:
            print(f"    · clone {r['slug']} ({r['format']}) into the other two lanes")
    else:
        print("\nNo 100k post yet. Do not open a second account — you'd be "
              "duplicating noise.")


def cmd_health(a):
    """The gate from the launch plan: 200 views in the first 24 hours."""
    rs = sorted(rows(), key=lambda r: r["date"])
    if not rs:
        return print("posts.csv is empty. Log a post first.")
    last = rs[-6:]
    v = [num(r, "views") for r in last]
    med = st.median(v)
    print(f"\nLast {len(last)} posts, median {med:,.0f} views "
          f"(gate is 200 in the first 24h)\n")
    for r in last:
        n = num(r, "views")
        print(f"  {'ok ' if n >= 200 else 'LOW'}  {n:>8,.0f}  {r['date']}  {r['slug']}")
    weak = sum(1 for x in v if x < 200)
    print()
    if med >= 200:
        print("  CLEAR — the account is getting a normal first test. "
              "You can step the volume up one level.")
        if weak:
            print(f"  ({weak} of {len(v)} below 200. One or two weak posts is content, "
                  f"not an account problem.)")
    else:
        print("  HOLD — do not increase volume. Check, in this order:")
        for d in ("a community-guidelines strike or a removed video",
                  "copyrighted audio on a recent post",
                  "a restricted word in a caption (cure, treat, diagnose, disease)",
                  "the same edit reused from another account",
                  "too much posting too early",
                  "almost no For You traffic in analytics"):
            print(f"    - {d}")
        print("\n  If none of those apply, the account is fine and the content is "
              "weak. Warm-up buys a fair test, not a good result.")
    print()


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("log"); p.add_argument("slug")
for fl in ("views", "likes", "saves", "shares", "comments", "follows"):
    p.add_argument(f"--{fl}", type=int, default=0)
p.add_argument("--url", default=""); p.add_argument("--date", default="")
p.set_defaults(fn=cmd_log)
sub.add_parser("report").set_defaults(fn=cmd_report)
sub.add_parser("next").set_defaults(fn=cmd_next)
sub.add_parser("health").set_defaults(fn=cmd_health)
a = ap.parse_args(); a.fn(a)
