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

These are what stop a deck reading as generated. The templates allow more than
this; the rules are the discipline.

1. **One idea per slide.** If a slide needs two sentences to land, it's two slides.
   A long deck is not a cost — every swipe is a signal the algorithm reads.
2. **No labels.** The uppercase eyebrow over a heading is the single loudest tell.
   `kicker` still exists for the three places it carries real information
   (`99% BUY`, `days 1 to 3`); everywhere else, leave it out.
3. **Number only real sequences.** `step` is for days 1 to 3 or a ranked list.
   Never as decoration on three unordered items.
4. **A photo unless there's a reason not to.** A type-only slide is a deliberate
   beat between photos, not a gap where a photo should be.
5. **The first slide is a photo with a confession on it.** Lowercase, one or two
   full sentences, a parenthetical or an ellipsis, and a stake someone would
   recognise. Not a headline, and never an aphorism. `PLAYBOOK.md` has the full
   pattern; the `HOOKS` dict at the bottom of `src/seed_batch.py` has 18 worked
   examples in one place, which is also the easiest place to rewrite them.

Statement text auto-sizes to its length (96px down to 42px), so a long hook still
fits and a short beat still lands hard. The scrim over each photo is chosen from
that photo's own brightness, so a dark bedroom shot keeps its detail instead of
going to mud.

## Slide types

`statement` · `grid` · `ps` · `protocol` · `chart` · `proof` · `verdict` · `cover` · `list` · `cta`

`statement` is the workhorse: full-bleed photo, one line, an optional second line.
Drop `photo` and it renders as large type on the surface, which is what you use
for a beat. `cover` and `list` are the older, denser slides; batch 01 barely uses
them.

`proof` is the screenshot slide: a dark panel holding a real screenshot from Oura,
Apple Health, or a lab report, with a stat callout above and a source line below.

Two rules for the screenshot. **Crop the status bar and any notification off** —
`oura-rhr-week.jpg` and `oura-sleep-debt.jpg` in `assets/photos/` show the crop.
And **crop tight to the chart**, roughly 1.3–1.5 wide-to-tall. The slide gives the
image about 700px of height; a full-length phone screenshot shrinks to a narrow
column in the middle and the numbers stop being readable at feed size.

A deck mixes them freely — a format is just a habitual sequence. See any file in
`content/batch01/` for a worked example of each.

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
