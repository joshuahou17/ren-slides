# The Ren account playbook

Your six goals, in order, with the part the code does and the part only you can do.

---

## 1. Find viral formats

You already did this — the reference accounts you collected are the research.
Stripped down, there are four things that work in this niche:

| Format | What it is | Why it travels | Where it fails |
|---|---|---|---|
| **Problem → Solution grid** | 2 panels, red arrow, white ground | Decoded in under half a second. No reading required to get the gist. | Most saturated lane on TikTok. You cannot win on craft here, only on subject. |
| **Cause grid** | One question, four labelled culprits | Highest save rate of the four. People screenshot it and send it to a friend. | Generic cells kill it. Every cell must be something the viewer would *deny*. |
| **n-of-1 reveal** | Hypothesis → protocol → chart → verdict | Nobody else posts data. A real chart is a pattern interrupt in a feed of stock photos. | Slow to make, and dead on arrival if the numbers look invented. |
| **Photo listicle** | Aesthetic photo, serif overlay, 5–8 slides | Carries nuance a grid can't, and builds a person rather than a content farm. | Needs a consistent photo library or it reads as a Pinterest board. |
| **Proof stack** | Your own screenshot, then the ranked explanation | The number hooks; the list is what they stay for. A real screenshot is the one claim nobody can clone. | Needs a number worth showing, and burns that number once. Ranking dishonestly kills it. |

The first two you clone. The last two are the ones nobody can clone back, because
they need a person with real data.

**On the proof stack specifically.** The temptation is to lead with the supplements,
because that's what people came for. Don't. Put the boring cause first — the
training volume, the no-alcohol, the fixed bedtime — and mark the supplements as
small. You lose nothing: the number already bought the attention, and the honesty
is what converts a viewer into someone who believes the next post. An account that
says "magnesium got me to 39 bpm" is indistinguishable from every supplement
affiliate on the platform. An account that says "running got me to 39 bpm and
magnesium did nothing I can measure" is the only one of its kind, and it happens
to be selling the tool that tells you which of the two you are.

Burn each number once. A resting heart rate of 39 is one post, not a series.

**Two shapes of proof, and one is better.** A *level* ("my RHR is 39") is a flex —
impressive, but the viewer can't picture themselves in it. An *arc* ("I was 9h40m
down and here's the line coming back") has a beginning, a middle and an end, and
the beginning is a bad week everybody has had. Expect the arc to outperform the
level, and go looking for more of them: a marker that moved between two blood
draws, a deload week, a fortnight of jet lag. Every arc is also a ready-made ad
for a closed loop, which is the thing you're actually selling.

Note what the reference accounts have in common that isn't the format: **every
single one names a specific body part or symptom in the first three words.**
"Weak jawline." "Low sperm count." "Why do I feel so tired." None of them open
with a concept. That is the actual transferable lesson.

## Writing the hook

The hook is the post. Everything after it is delivery. The accounts that travel
write hooks that read as **typed by a person**, not written by a copywriter, and
the difference is mechanical enough to copy:

| Device | Example |
|---|---|
| **Lowercase** | `i woke up at 3am every night for a month and blamed stress` |
| **Long, not punchy** | one or two full sentences, not a four-word headline |
| **A confession** | `i counted the supplements in my cupboard and then worked out what i'd spent` |
| **A parenthetical** | `(the last slide is the part nobody says out loud)` |
| **A trailing ellipsis** | `here's what nobody actually checked…` |
| **A stake you'd recognise** | a number of years, an age, a relationship, an amount of money |
| **Borrowed authority** | `weird hacks my counselor gave me`, `my mum is a professor at Oxford` |
| **"so you don't have to"** | volunteering to have done the boring part |

Two rules on borrowed authority: it has to be **true**, and the person has to be
**specific**. "A doctor told me" is worth nothing. "My GP told me, after I asked
for the third time" is worth a lot, and you can only write it if it happened.

## Two hook genres, and you should test them

Everything above describes **style A** — the first-person confession. There is a
second genre that clipper campaigns run on, **style B**: direct address, second
person, the payoff promised up front, trailing ellipsis.

| | Style A | Style B |
|---|---|---|
| Voice | "i woke up at 3am every night for a month and blamed stress" | "Here's exactly why you keep waking up at 3am…" |
| Sells | a person | a payoff |
| Strength | follows, comments, an account worth following | raw click-through and swipe rate |
| Weakness | slower to hook a stranger | forgettable; nobody follows a promise |

Both are in the repo. Slide one carries A by default; `--hook b` swaps in the
direct-address version:

```bash
python3 src/render.py content/batch01/ --hook b --out out-b
```

**Style B is the default.** `--hook a` renders the confessional variant if you
want to test it. Every deck carries both.

**Why B suits this account:**
there is no face, no name, and now no watermark. Style A's whole advantage is
that a person accumulates — and nothing here accumulates into a person. Style B
is built for exactly this shape of account.

But don't decide it by argument. You have 27 decks in two hook styles, which is
a real experiment: run style A for a week, style B the next, compare the medians
in `track.py`. That is the single highest-value test available to you, because
the hook decides everything downstream.

**The swipe cue is not optional.** Every slide one carries "(Swipe right →)"
automatically. It costs nothing, and the swipe is the signal the algorithm
actually reads — a viewer who swipes has told TikTok the post held them.

What kills a hook: the aphorism. "Your number isn't my number." "One low night is
weather." Those are good *closing* lines and terrible opening ones, because they
sound authored. Nobody stops scrolling for something that sounds written.

Your own honest borrowed authority is the Oura screenshot. You don't have a
famous parent; you have a resting heart rate of 39 and a chart of your own sleep
debt. That's the version of the device available to you, and it's a better one,
because nobody can borrow it back.

## 2. Find where Ren fits

Ren's loop — intake → propose → adhere → reassess → adjust — maps onto content
better than most apps, because each step is already a slide:

- **intake** → the bloodwork lane. "Your ferritin is why you're exhausted."
- **propose** → the protocol card. A hypothesis with a length and a success rule.
- **reassess** → the chart and the verdict stamp. This is the format nobody has.
- **adjust** → the failure posts. "This one didn't work, here's the chart."

The three lanes you picked map cleanly:

| Lane | Reach | Follow quality | Ren fit |
|---|---|---|---|
| Sleep & recovery | highest | medium | high — wearable intake |
| Bloodwork decoded | medium | **highest** | **highest** — the PDF upload use case, verbatim |
| n-of-1 / supplement truth | lowest | high | it *is* the product |
| **The stack problem** | medium | **highest intent** | **it is the pitch** |

**The fourth lane arrived late and may be the best one.** "You own nine bottles and
can't prove any of them do anything" reaches people who have already spent the
money and are looking for permission to stop guessing. That is a shorter distance
to an install than any amount of sleep-tip reach. Two things make it work: the
**subtraction** angle (stop one thing, see if anything changes), which nobody else
posts because the niche is funded by addition; and the **name-check** posts, where
you summarise someone's protocol honestly and then make the turn that no podcast
can make for you.

On the name-check posts: summarise fairly, never imply endorsement, never invent a
quote, and don't use anyone's likeness. The post only works if the turn is
generous rather than a takedown. "He can tell you what's worth trying, he can't
tell you what works on you" is the line. "He's wrong" is a different, worse post.

Run all three. Expect sleep to bring the views and bloodwork to bring the
installs. If that turns out to be backwards, the tracker will tell you.

**The Ren ladder.** Per 10 posts: 6 with no mention, 3 with a soft last slide,
1 hard CTA. The mistake every app account makes is gating good posts behind a
CTA before anyone trusts them. Batch 01 ships 9 / 2 / 1.

## 2.5 Warm the account up before any of this runs

A new account has no trust, and the fastest way to spend a month at forty views a
post is to create an account and publish a campaign video ten minutes later.
`POST-PLAN.md` has the dated version; this is the shape:

**Before day one.** Confirm the email. Profile photo, username, bio. Two-factor
on, passkey if offered. This is TikTok's cheapest signal that a person owns the
account.

**Days 1 to 3, no posting at all.** Scroll the niche one to two hours a day,
*split across the day*, not in one sitting. Ten videos watched to the end, twenty
to thirty likes, three to five real comments, five to ten follows. Search the
problems your buyer searches, not your product category: "why am i always tired",
"ferritin fatigue", "supplement stack". That is what tells the algorithm which
audience this account belongs to, and it doubles as free research on which hooks
already work.

**Days 4 to 6, broad posts only.** Batch 01 has six decks tagged `tier: broad`
for exactly this. They fit the niche and sell nothing: no product, no protocol,
no CTA, no link. An investing app opens with "realising how much i spent last
month", not "download our portfolio tracker". A health app opens with "why is
everyone in their twenties this tired". The broad version gives TikTok a bigger,
clearer audience to test against, which is worth more than an early install.

**Day 7 onwards, one campaign post a day.** Not three. Volume goes up only after
the posts are getting normal For You traffic.

**The gate between every step: 200 views in the first 24 hours.** One weak post
is content. Six weak posts is an account problem. `python3 src/track.py health`
checks the median of your last six and tells you whether to step up or stop.

Two things worth being clear-eyed about. Warm-up does not make weak content
perform; it buys strong content a fair first test, which is a smaller claim than
most people selling this advice make for it. And when you open account two, never
publish the same export twice: TikTok matches on the file, and a duplicate
suppresses *every* copy including the original. Change the hook and the opening
photo and re-render.

## 3. Experiment until you build taste

Taste here is just memory of what died. The tracker makes that memory external.

- **3 posts a day**, 09:00 / 14:00 / 20:00 ET. Same lane, rotate format.
- **Nine posts before you judge a format.** Median, never mean — one lucky 500k
  hides nine 800s.
- **One variable at a time.** If you change the format *and* the lane *and* the
  hook, a win teaches you nothing.
- Days 1–14 you are buying information, not followers. 42 posts.

The one thing the code can't do: read the comments. The comments are where the
next ten hooks come from. A question asked twice under a post is a post.

```bash
python3 src/track.py report   # medians by format, lane, CTA level
python3 src/track.py next     # KILL / KEEP / CLONE per format
```

Kill rule: median under 3k after 9 posts → stop making them.
Clone rule: any single post over 100k → that deck is now a template.

## 4. Hit multiple virals on one account

A viral is a template, not a post. When one clears 100k:

1. Keep the **structure** exactly — same slide count, same layout, same rhythm.
2. Swap the **subject** only. "Why do I wake up at 3am" → "Why am I always cold"
   → "Why is my HRV so low". Same skeleton, three posts.
3. Make five variants before you touch anything else. Most accounts abandon a
   winner after one repeat; the algorithm hasn't finished distributing it.
4. Re-post the original a month later with a hard CTA. A proven deck is where the
   CTA belongs — not a fresh one.

Posting three a day is what makes this possible: the format gets enough shots for
the distribution to show up.

## 5. Double down across more accounts

**Do not open account #2 until one account has three posts over 100k.** Before
that you're duplicating noise and halving your posting attention.

When you do:

- One account per lane, not per format. `@rensleep`, `@renlabs`, `@renxp`.
- Account #2 posts **only proven templates** from day one. It never runs the
  discovery phase again — that's the whole point of having done it once.
- Different handle, different bio, different opening frame. Same engine.
- `brand.yaml` is per-account: copy the folder, change the handle and the accent.

Three accounts × 3 posts/day is 270 posts a month out of one JSON schema.

## 6. Generate the slides

That's `render.py`. See `README.md`.

The honest limit: the engine generates layout, type and charts perfectly and
cannot generate photography. Put ~40 images in `assets/photos/` once — food,
supplements, faces, rooms, bottles — and the Problem→Solution and cause-grid
decks stop looking like text and start looking like the accounts you screenshotted.

---

## Why these colors

The chart palette isn't decorative. Baseline `#2a78d6` against trial `#1baf7a`
is a validated pair: worst-case colorblind separation ΔE 23.1, normal-vision
24.0, both well clear of the floors. Each phase mean is direct-labelled with its
number, which is what lets the green sit below 3:1 contrast without becoming
unreadable. The chart is a line, not bars, because bars must start at zero and a
zero-based axis flattens an 18-minute deep-sleep gain into nothing — the floor is
non-zero and the day labels say so.

Small thing. But the entire n-of-1 lane rests on the charts looking like someone
who knows what a chart is made them.

## What will actually decide this

Not the format. Three things, in order:

1. **Whether the data is real.** The moment a chart is caught invented, the lane
   that differentiates you is gone and you're another glowup account.
2. **Specificity of the first three words.** "Your ferritin" beats "your iron"
   beats "your bloodwork" beats "your health".
3. **Whether you post 42 times in 14 days.** Almost nobody does. The accounts you
   screenshotted all did.
