# Bootstrap (read me first on any fresh session)

This project renders TikTok slideshow decks for Ren. A scheduled run starts in a
brand new container with nothing in it, so the first job is always to get this
repo back:

```bash
git clone https://github.com/joshuahou17/ren-slides.git
cd ren-slides
pip install playwright jinja2 pyyaml --break-system-packages
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   # chromium is preinstalled
```

If the clone fails with an auth or "not available" error, **stop**. Say so in one
line and do not attempt to rebuild the project from scratch — the decks, the
photo library and the plan all live here and cannot be recreated from memory.

## What's where

| Path | What |
|---|---|
| `content/batch01/*.json` | 27 decks. One file per post. |
| `assets/photos/` | Photo library + real Ren app captures (`ren-*.jpg`). |
| `plan.csv` / `POST-PLAN.md` | The dated posting schedule. |
| `posts.csv` | Logged performance. |
| `src/render.py` | deck JSON → `out/<slug>/NN.png` + `caption.txt` |
| `src/plan.py` | regenerates the schedule |
| `src/track.py` | `log`, `report`, `next`, `health` |
| `src/new_deck.py` | scaffolds a deck in the house style |
| `src/library.py` | lanes, formats, hook patterns, the Ren ladder |
| `PLAYBOOK.md` | strategy, hook-writing rules, warm-up protocol |
| `README.md` | house rules for a slide |

## Render one deck

```bash
python3 src/render.py content/batch01/<slug>.json
# PNGs land in out/<slug>/01.png … and out/<slug>/caption.txt
```

## Always commit and push before the session ends

```bash
git add -A && git commit -m "<what changed>" && git push
```

Anything not pushed is lost when the container is reclaimed.
