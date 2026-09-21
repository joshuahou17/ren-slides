"""
library.py — the taste layer.

Everything here is content strategy encoded as data: the lanes, the four slide
formats, the hook patterns that carry them, and the ladder of how hard a deck
points back at Ren. render.py never reads this file; new_batch.py and you do.
"""

# ---------------------------------------------------------------- lanes ----
LANES = {
    "sleep": {
        "title": "Sleep & recovery",
        "promise": "why you wake up tired, and what actually moves deep sleep",
        "ren_hook": "Ren reads Apple Health / Oura / Whoop, so every claim here "
                    "is checkable against your own nights.",
        "metrics": ["deep sleep", "REM", "resting HR", "HRV", "sleep latency",
                    "wake events", "sleep efficiency"],
    },
    "bloodwork": {
        "title": "Bloodwork decoded",
        "promise": "the marker behind the symptom you've been ignoring",
        "ren_hook": "Ren ingests a bloodwork PDF and tells you which markers "
                    "explain what you're feeling.",
        "metrics": ["ferritin", "vitamin D", "B12", "TSH", "free T3", "hs-CRP",
                    "HbA1c", "fasting insulin", "magnesium RBC", "testosterone"],
    },
    "nof1": {
        "title": "Supplement truth / n-of-1",
        "promise": "I ran the experiment on myself so you can see the real delta",
        "ren_hook": "This is literally what Ren does: propose → adhere → reassess.",
        "metrics": ["deep sleep", "HRV", "resting HR", "morning energy 1-10",
                    "time to fall asleep", "afternoon crash"],
        "proof_numbers": "Numbers worth building a proof_stack around: a resting "
                         "HR in the 30s-low 40s, a 100+ ms HRV, a 2h+ deep sleep "
                         "average, a VO2max estimate, a bloodwork marker that moved.",
    },
    "stack": {
        "title": "The stack problem",
        "promise": "you are spending real money on things you cannot prove are working",
        "ren_hook": "This lane IS the product pitch. The viewer already bought in; "
                    "they're looking for permission to stop guessing.",
        "metrics": ["monthly supplement spend", "number of bottles",
                    "things started in the same month", "things never stopped"],
        "note": "Highest purchase intent of the four lanes and the least crowded. "
                "The subtraction angle (stop one, see if anything changes) is the "
                "one nobody else posts, because the niche is funded by addition.",
    },
}

# -------------------------------------------------------------- formats ----
FORMATS = {
    "problem_solution": {
        "slides": "2-4",
        "why_it_works": "Zero reading cost. The eye decodes PROBLEM→SOLUTION in "
                        "under 400ms, which is what buys the swipe.",
        "best_for": ["bloodwork", "sleep"],
        "risk": "Most saturated. You win on specificity, not on format.",
        "schema": "panels[]: {kind: problem|solution|result, label, sub, img}",
    },
    "cause_grid": {
        "slides": "1-3",
        "why_it_works": "One question the viewer is already asking, four culprits. "
                        "Highest save rate of the four — people screenshot it.",
        "best_for": ["sleep", "bloodwork"],
        "risk": "Easy to make generic. Every cell must be a thing they'd deny.",
        "schema": "question, cells[]: {label, sub, img}",
    },
    "nof1_reveal": {
        "slides": "4-6",
        "why_it_works": "Nobody in this niche shows data. A real chart is a "
                        "pattern interrupt in a feed of stock photos.",
        "best_for": ["nof1", "sleep"],
        "risk": "Slower to make; dies if the numbers look fake. Use YOUR data.",
        "schema": "hypothesis, protocol{}, series[], baseline_mean, trial_mean, "
                  "unit, verdict, verdict_note",
    },
    "proof_stack": {
        "slides": "5-6",
        "why_it_works": "A real screenshot of your own data is the only claim on "
                        "this app nobody can copy. The number does the hooking; "
                        "the list is just the explanation people stay for.",
        "best_for": ["nof1", "sleep"],
        "risk": "Only works with a number worth showing, and only once per number. "
                "Ranking the list honestly is what separates it from every other "
                "supplement post — put the boring cause first even though the "
                "supplements are what people came for.",
        "schema": "cover, proof{img, stat, caption}, list[] (ranked), "
                  "list[] (what you can't take credit for), cta",
    },
    "photo_listicle": {
        "slides": "5-8",
        "why_it_works": "Carries nuance a grid can't. Builds a person, not a "
                        "content farm — which is what makes an account followable.",
        "best_for": ["sleep", "nof1"],
        "risk": "Needs a consistent photo library or it looks like a Pinterest board.",
        "schema": "title, kicker, items[]: {text, sub}, photo",
    },
}

# ----------------------------------------------------------- hook banks ----
# %s slots: {metric} {thing} {n} {marker} {symptom}
HOOKS = {
    "cause_grid": [
        "Why do I feel so tired?",
        "Why am I always cold?",
        "Why do I wake up at 3am?",
        "Why is my HRV so low?",
        "Why do I crash at 2pm?",
        "Why can't I fall asleep?",
        "Why do I wake up puffy?",
        "Why is my resting heart rate climbing?",
        "Why do I get sick every month?",
        "Why do I feel hungover without drinking?",
    ],
    "problem_solution": [
        "PROBLEM: {symptom} → SOLUTION: {thing}",
        "99% do this / 1% do this",
        "{thing} is why your {metric} is bad",
        "Stop doing this before bed",
        "Your {marker} explains it",
    ],
    "nof1_reveal": [
        "I took {thing} every night for {n} days. Here's what happened to my {metric}.",
        "{n} days of {thing}. The chart doesn't lie.",
        "Everyone says {thing} fixes {metric}. I tested it on myself.",
        "I ran the {thing} experiment so you don't have to.",
        "{thing}: worked, or placebo? {n} nights of data.",
        "I stopped {thing} for {n} days. My {metric} did this.",
    ],
    "proof_stack": [
        "How I got my {metric} to {n}",
        "My {metric} is {n}. Here's everything that actually did it.",
        "{n} {metric}. Ranked by how much each thing actually mattered.",
        "Everyone asks how I got my {metric} to {n}. The real answer is boring.",
    ],
    "photo_listicle": [
        "{n} things I changed that fixed my sleep",
        "{n} things nobody tells you about {metric}",
        "{n} habits I stole from people who sleep 9 hours",
        "what your {marker} is actually telling you",
        "{n} tests I wish I'd run in my 20s",
    ],
}

# ------------------------------------------------------- the Ren ladder ----
# How hard a deck points back at the app. Ratio target per 10 posts: 6/3/1.
REN_TIE = {
    "none": {
        "ratio": 6,
        "rule": "Pure value. No app, no handle beyond the watermark. "
                "This is what makes the account followable and is most of your reach.",
        "cta": None,
    },
    "soft": {
        "ratio": 3,
        "rule": "Last slide only. Name the mechanism, not the product. "
                "'I track this with an app that reads my Oura data' — comments ask what it is.",
        "cta": "the app I use to track this is in my bio",
    },
    "hard": {
        "ratio": 1,
        "rule": "Explicit. Reserve for decks that already proved they travel — "
                "re-post a winner with a hard CTA rather than gating a fresh one.",
        "cta": "Ren runs this experiment for you — link in bio",
    },
}

# ------------------------------------------------------------ hashtags ----
HASHTAGS = {
    "sleep":     ["sleep", "deepsleep", "sleeptips", "oura", "whoop", "hrv",
                  "sleepbetter", "circadian"],
    "bloodwork": ["bloodwork", "bloodtest", "ferritin", "vitamind", "thyroid",
                  "labresults", "healthtips", "biohacking"],
    "nof1":      ["selfexperiment", "biohacking", "supplements", "magnesium",
                  "healthdata", "quantifiedself", "sleepexperiment"],
    "stack":     ["supplements", "supplementstack", "biohacking", "wastingmoney",
                  "hubermanlab", "healthtok"],
    "always":    ["fyp", "healthtok"],
}

# ----------------------------------------------- posting / test protocol ----
PROTOCOL = {
    "cadence": "3 posts/day, 09:00 / 14:00 / 20:00 ET, 7 days a week.",
    "phase_1": "Days 1-14: 42 posts. One variable at a time — same lane, "
               "rotate format. You are buying information, not followers.",
    "phase_2": "Days 15-28: kill any format under 3k median views. Take the top "
               "3 decks and make 5 variants of each (same format, new subject).",
    "phase_3": "Day 29+: a deck that clears 100k is a TEMPLATE, not a post. "
               "Clone it across the other two lanes, then open account #2 "
               "using only proven templates.",
    "kill_rule": "A format gets 9 posts before you judge it. Median, not mean — "
                 "one lucky 500k hides nine 800s.",
    "double_down": "Only clone to a new account once ONE account has 3+ posts "
                   "over 100k. Before that you're duplicating noise.",
}
