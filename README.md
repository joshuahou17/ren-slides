# Ren slideshow engine

Deck JSON in → finished TikTok slide PNGs + caption out. No design tool, no Canva.

```
brand.yaml            handle, colors, canvas size
content/batch01/      12 decks, one JSON each  ← you edit these
assets/photos/        drop JPG/PNG here to replace the type tiles
formats/deck.html     the eight slide types, as one Jinja template
src/render.py         deck JSON → out/<slug>/01.png … + caption.txt
src/new_deck.py       scaffold a new deck for a format
src/review.py         build the approval board (out/review.html)
src/track.py          log post performance, get kill/keep/clone verdicts
src/library.py        the strategy as data: lanes, formats, hooks, the Ren ladder
posts.csv             your results — edit in a spreadsheet if you prefer
```

## Setup (once)

```bash
pip install playwright jinja2 pyyaml
playwright install chromium
```

Then set your handle in `brand.yaml`.

## The loop

```bash
python3 src/new_deck.py cause_grid --slug sleep-cant-sleep --lane sleep   # scaffold
# …fill in the JSON…
python3 src/render.py content/batch02/                                    # 1080×1350 PNGs
python3 src/review.py --prefix .                                          # out/review.html
# …post…
python3 src/track.py log sleep-cant-sleep --views 8400 --follows 44 --saves 320
python3 src/track.py next                                                 # what to kill / clone
```

`--height 1920` on `render.py` gives you full 9:16 instead of 4:5.

## House rules for a slide

These are now enforced by `src/render.py`. A deck that breaks one does not render
— it prints what's wrong and refuses. Prose rules drifted; these don't.

1. **Every slide carries a photo.** `statement`, `cta` and `protocol` all require
   one. Type-only slides are gone.
2. **Every grid cell and every problem/solution panel needs its own image.** Not
   most of them — all of them. A group with three photos and one type tile looks
   broken, so the renderer refuses it.
3. **Charts and verdicts come from real app screenshots, never from drawn
   graphics.** The synthetic chart and verdict-stamp slide types were removed. If
   you want to show a result, show the Ren, Oura or Whoop screen that produced it,
   on a `proof` slide.
4. **One idea per slide.** Two sentences means two slides.
5. **No slide labels.** The uppercase eyebrow is the loudest generated-design tell.
   Allowed only where it carries information (`99% BUY`, `days 1 to 3`).
6. **Number only real sequences.**
7. **Slide one is a photo with a confession on it** — lowercase, one or two full
   sentences, a parenthetical or an ellipsis, a recognisable stake. Never a
   headline, never an aphorism.
8. **Every closing slide lands on the same claim in different words:** a video
   cannot tell you whether something works on *you*; only a test can. The `CTA`
   dict at the bottom of `src/seed_batch.py` holds all of them in one place.

## Slide types

`statement` · `grid` · `ps` · `protocol` · `proof` · `cta`

Six types, down from nine. `chart`, `verdict` and `list` were removed: the first
two because drawn results are indistinguishable from invented ones, the third
because one-idea-per-slide replaced it.

- **`statement`** — full-bleed photo, one centred line, optional second line.
  Auto-sizes 96→42px; scrim darkness computed per photo. The workhorse.
- **`grid`** — a question plus four labelled cells, each with its own image.
- **`ps`** — Problem→Solution panels with the red arrow, every panel imaged.
- **`protocol`** — the experiment card (what, when, baseline, trial, measured,
  success rule) as a glass panel over a photo.
- **`proof`** — a real screenshot with a stat callout and a source line. The only
  type that carries evidence rather than assertion, and the only one nobody else
  can copy.
- **`cta`** — the closing slide.

## App screenshots

Real captures from the Ren repo live in `assets/photos/` as `ren-*.jpg`:
`ren-verdict-null` (the "no clear effect" screen — the most valuable asset you
have), `ren-verdict-worked`, `ren-full-result`, `ren-chronotype`,
`ren-archetypes`. They go in `proof` slides with a caption naming the source.

To regenerate them from the app, that's a Claude Code job on the Mac, not a
Cowork one — this workspace is Linux with no Xcode. `Ren/scripts/capture-screens.sh`
and `Ren/docs/marketing/SCREENSHOT-BRIEF.md` are the handoff; run the script and
the PNGs land in `Ren/marketing/screens/`, which Cowork can read directly.

One rule on captions: these screens are seeded with the app's DEBUG fixtures, so
caption them as *what the app says*, never as *my result*. Same standard as the
Oura charts.

## Images

`assets/photos/` holds your 47 images, resized to 1400px and renamed to slugs.
Two kinds of slot take them:

- **Full-bleed** — `"photo"` on a `cover`, `list` or `cta` slide. Scrim and white
  text are applied automatically. This is the sydney / heather look.
- **Cell** — `"img"` on a `grid` cell or a `ps` panel. Use these only when you
  have a real object photo for *every* cell in the group; one photo beside three
  type tiles looks broken.

Your library is lifestyle (beds, gyms, running, cycling, coffee, pills). It fills
covers and closers beautifully. It does **not** contain the literal object shots
the Problem→Solution and cause-grid formats want, so those stay typographic
except the magnesium deck, where four distinct pill photos cover all four cells.

**What to grab next:** see `SHOPPING-LIST.md` for exact search terms, ordered by
how much each one unlocks.

Resized copies also live in `pics for slideshows/optimized/` on your Mac — the
originals are untouched.

## One warning

The `chart` slides in `content/batch01/` use **placeholder series**. Replace them
with your own Oura / Apple Health export before posting. An account built on
n-of-1 data dies the first time someone catches invented numbers, and the whole
strategy below depends on that account being trusted.
