"""
chart.py — the n-of-1 reveal chart as inline SVG.

Form choice: change-over-time for ONE metric across two phases. A bar chart
would have to start at zero (non-negotiable), which flattens a 12%% delta into
nothing; a line/dot chart may legitimately use a non-zero floor as long as the
floor is labeled — so: line + markers, segment-colored by phase, with each
phase's mean drawn as a direct-labeled reference line. One axis. Legend in the
template. Stroke/marker sizes are scaled ~2.5x from the spec's screen values
because this renders at 1080px wide and is viewed at phone size.
"""
from html import escape


def nof1_svg(series, split, b, unit="", w=936, h=720,
             baseline_label="baseline", trial_label="on protocol"):
    """series: list of floats (one per day). split: index where the trial starts."""
    n = len(series)
    pad_l, pad_r, pad_t, pad_b = 8, 210, 26, 66
    pw, ph = w - pad_l - pad_r, h - pad_t - pad_b

    lo, hi = min(series), max(series)
    span = max(hi - lo, 1e-6)
    floor = lo - span * 0.35
    ceil_ = hi + span * 0.22
    rng = ceil_ - floor

    def X(i): return pad_l + (pw * i / max(n - 1, 1))
    def Y(v): return pad_t + ph - (ph * (v - floor) / rng)

    base = series[:split]
    trial = series[split:]
    bm = sum(base) / len(base) if base else 0
    tm = sum(trial) / len(trial) if trial else 0

    def fmt(v): return f"{v:.0f}" if abs(v) >= 10 else f"{v:.1f}"

    p = []
    a = ['<svg viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
         'aria-label="%s over %d days, baseline mean %s, protocol mean %s %s">'
         % (w, h, w, h,
            escape(f"{baseline_label} vs {trial_label}"), n, fmt(bm), fmt(tm), escape(unit))]

    # recessive horizontal grid at the two means only (no grid clutter)
    # phase shading for the trial window
    a.append(f'<rect x="{X(split)-((X(1)-X(0))/2):.1f}" y="{pad_t}" '
             f'width="{pad_l+pw-(X(split)-((X(1)-X(0))/2)):.1f}" height="{ph}" '
             f'fill="{b["trial"]}" opacity="0.055" rx="10"/>')

    # axis floor rule
    a.append(f'<line x1="{pad_l}" y1="{pad_t+ph:.1f}" x2="{pad_l+pw:.1f}" y2="{pad_t+ph:.1f}" '
             f'stroke="{b["rule"]}" stroke-width="3"/>')

    # mean reference lines + direct labels (this is the relief for the contrast WARN)
    for val, col, lab, dash in ((bm, b["baseline"], baseline_label, "10 12"),
                                (tm, b["trial"], trial_label, None)):
        y = Y(val)
        a.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+pw:.1f}" y2="{y:.1f}" '
                 f'stroke="{col}" stroke-width="3" opacity=".55"'
                 + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        a.append(f'<text x="{pad_l+pw+22:.1f}" y="{y-10:.1f}" font-size="30" '
                 f'font-weight="800" fill="{col}" '
                 f'font-family="Inter,sans-serif">{fmt(val)} {escape(unit)}</text>')
        a.append(f'<text x="{pad_l+pw+22:.1f}" y="{y+24:.1f}" font-size="24" '
                 f'font-weight="600" fill="{b["ink_muted"]}" '
                 f'font-family="Inter,sans-serif">{escape(lab)}</text>')

    # the line, in two phase-colored segments that share the joining point
    def path(idx0, idx1):
        return "M " + " L ".join(f"{X(i):.1f} {Y(series[i]):.1f}" for i in range(idx0, idx1))

    a.append(f'<path d="{path(0, split)}" fill="none" stroke="{b["baseline"]}" '
             f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    a.append(f'<path d="{path(split-1, n)}" fill="none" stroke="{b["trial"]}" '
             f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

    # markers — 2px surface ring so overlaps stay legible
    for i, v in enumerate(series):
        col = b["baseline"] if i < split else b["trial"]
        a.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="8" fill="{col}" '
                 f'stroke="{b["surface"]}" stroke-width="3"/>')

    # phase divider
    xd = X(split) - ((X(1) - X(0)) / 2)
    a.append(f'<line x1="{xd:.1f}" y1="{pad_t}" x2="{xd:.1f}" y2="{pad_t+ph:.1f}" '
             f'stroke="{b["ink_muted"]}" stroke-width="2" stroke-dasharray="6 10"/>')

    # x labels: first, split, last only
    for i, lab in ((0, "day 1"), (split, f"day {split+1}"), (n - 1, f"day {n}")):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        a.append(f'<text x="{X(i):.1f}" y="{pad_t+ph+42:.1f}" font-size="25" '
                 f'font-weight="600" fill="{b["ink_muted"]}" text-anchor="{anchor}" '
                 f'font-family="Inter,sans-serif">{lab}</text>')

    a.append("</svg>")
    return "\n".join(a), bm, tm
