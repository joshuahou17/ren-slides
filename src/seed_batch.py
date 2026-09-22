#!/usr/bin/env python3
"""seed_batch.py — batch 01.

House rules this batch follows:
  slide one is always a photo with a line you'd stop on,
  one idea per slide, text centred, no slide labels,
  and the closing slide sounds like a person recommending something.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "batch01"
OUT.mkdir(parents=True, exist_ok=True)

TAGS = {
 "sleep": ["sleep", "deepsleep", "sleepdebt", "oura", "whoop", "hrv", "fyp"],
 "bloodwork": ["bloodwork", "bloodtest", "ferritin", "thyroid", "labresults", "healthtok", "fyp"],
 "nof1": ["selfexperiment", "biohacking", "supplements", "healthdata", "restingheartrate", "oura", "fyp"],
 "stack": ["supplements", "supplementstack", "biohacking", "wastingmoney", "healthtok", "fyp"],
}
D = []


def deck(**k):
    k["hashtags"] = TAGS[k["lane"]]
    k.setdefault("tier", {"none": "core", "soft": "soft", "hard": "hard"}[k["ren_tie"]])
    D.append(k)


def st(text, photo=None, sub=None, step=None, small=False):
    s = {"type": "statement", "text": text}
    if photo: s["photo"] = photo
    if sub: s["sub"] = sub
    if step: s["step"] = step
    if small: s["small"] = True
    return s


def cta(text, sub=None, photo=None, pill=None):
    s = {"type": "cta", "text": text}
    if sub: s["sub"] = sub
    if photo: s["photo"] = photo
    if pill: s["pill"] = pill
    return s


# ═══════════════════════════════════════════════════════════════ SLEEP ════
deck(slug="sleep-wake-at-3am", lane="sleep", format="cause_grid", ren_tie="none",
 hook="3:14am. Again.",
 caption="Most people have two of these going at once and blame the wrong one.",
 notes="Photo hook now leads, grid is slide two. Watch whether the thumbnail change "
       "costs reach; the grid used to be the thumbnail.",
 slides=[
  st("3:14am. Again.", "sleep-aesthetic-1.jpg", "It's almost never random."),
  {"type": "grid", "question": "“Why do I wake up at 3am?”", "layout": "g2x2", "cells": [
    {"label": "Alcohol", "img": "wine-at-night.jpg"},
    {"label": "A warm room", "img": "sleep-aesthetic.jpg"},
    {"label": "Nothing since 5pm", "img": "coffee-picture-4.jpg"},
    {"label": "A 2pm coffee", "img": "coffee-picture-1.jpg"}]},
  st("Alcohol puts you under fast.", "cycling-picture-2.jpg",
     "Then rebounds about four hours later, which is 3am."),
  st("You have to cool down to stay asleep.", "sleep-aesthetic.jpg",
     "A room above 19°C won't let your core temperature drop."),
  st("Half of a 2pm coffee is still in you at 10pm.", "coffee-picture-1.jpg"),
  st("change all four and you've learned nothing.", "cycling-picture-2.jpg"),
  cta("Change one. Watch one number. Give it two weeks.",
      "That's the whole difference between trying something and testing it.",
      "sleep-aesthetic-3.jpg")])

deck(slug="sleep-deep-sleep-fix", lane="sleep", format="problem_solution", ren_tie="soft",
 hook="Your deep sleep was decided before you got into bed",
 caption="The last ninety minutes of your day matter more than anything you swallow.",
 notes="Put object photos in the four panels the moment you have them. That is what "
       "makes this format travel.",
 slides=[
  st("Your deep sleep was decided before you got into bed.", "sleep-aesthetic-2.jpg"),
  {"type": "ps", "bands": [
    {"head": "PROBLEM", "color": "#d93f3e", "cells": [
      {"label": "Scrolling in bed", "img": "sleep-aesthetic-1.jpg"},
      {"label": "Late heavy dinner", "img": "coffee-picture-4.jpg"}]},
    {"head": "SOLUTION", "color": "#0f9d63", "cells": [
      {"label": "Phone in another room", "img": "sleep-aesthetic-image.jpg"},
      {"label": "Eat 3 hours earlier", "img": "yoga-in-park.jpg"}]}]},
  {"type": "ps", "bands": [
    {"head": "PROBLEM", "color": "#d93f3e", "cells": [
      {"label": "Bedtime drifts 2 hours", "img": "sick-aesthetic-picture.jpg"},
      {"label": "Hot shower at 11pm", "img": "cycling-picture-2.jpg"}]},
    {"head": "SOLUTION", "color": "#0f9d63", "cells": [
      {"label": "Same 30 minute window", "img": "sleep-aesthetic-3.jpg"},
      {"label": "Shower at 9:30", "img": "sleep-aesthetic-4.jpg"}]}]},
  st("You can't feel deep sleep.", "sick-aesthetic-picture.jpg",
     "Which is why people guess about it for years."),
  cta("Pick one and hold it for two weeks.",
      "I use an app called Ren to watch whether it actually moved. It's in my bio if you want it.",
      "sleep-aesthetic-4.jpg")])

deck(slug="sleep-magnesium-14-nights", lane="sleep", format="proof_stack", ren_tie="soft",
 hook="everyone kept telling me magnesium would fix my sleep so i actually tested it for 21 nights",
 caption="seven nights without, fourteen with, same room, same bedtime window. the app graded it, not me.",
 notes="REBUILT: the drawn chart and verdict stamp were removed from the engine. "
       "The result is now the actual Ren verdict screen, which says the quiet part "
       "out loud: magnesium did not move this number.",
 slides=[
  st("everyone kept telling me magnesium would fix my sleep so i actually tested it for 21 nights",
     "sleep-aesthetic.jpg", "the chart is not what i expected\u2026"),
  {"type": "protocol", "title": "Magnesium glycinate, deep sleep",
   "photo": "natalie-hordiiuk.jpg", "rows": [
    [" what ", "400mg glycinate"], [" when ", "60 min before bed"],
    [" baseline ", "7 nights, nothing"], [" trial ", "14 nights"],
    [" measured ", "Oura deep sleep"]],
   "success_rule": "Deep sleep up 8 minutes on average. Under that is noise."},
  {"type": "proof", "img": "ren-verdict-null.jpg",
   "caption": "Ren, verdict screen. Deep sleep 1h12m before, 1h14m after. That sits "
              "inside my own night-to-night noise, so it grades as no effect."},
  st("two minutes. on a metric that swings twenty.", "akshay-chauhan.jpg",
     "that is not a small win. that is nothing."),
  st("i still take it.", "ambitious-studio-by-rick-barrett.jpg",
     "it gets me to sleep faster. it just doesn't do the thing everyone says it does."),
  cta("my +2 minutes is not a prediction about your +2 minutes.",
      "same supplement, same dose, different person, different answer. the only number "
      "that means anything is yours. bio.",
      "sleep-aesthetic-3.jpg")])

deck(slug="sleep-5-non-supplement", lane="sleep", format="photo_listicle", ren_tie="none",
 hook="Five things fixed my sleep. None of them were supplements.",
 caption="Ranked by how much they moved the number, not by how good they sound.",
 notes="One item per slide. Longer deck, but swipe-through is what the algorithm reads.",
 slides=[
  st("Five things fixed my sleep.", "sleep-aesthetic-2.jpg", "None of them were supplements."),
  st("A fixed wake time.", "sleep-aesthetic-3.jpg",
     "Same alarm on Saturday. This did more than everything else combined.", step="01"),
  st("18°C and a cracked window.", "sleep-aesthetic-4.jpg",
     "Your core temperature has to fall for you to fall asleep.", step="02"),
  st("Daylight in the first hour.", "woman-jumping-on-beach-sunset.jpg",
     "Ten minutes outside beats any lamp you'll buy.", step="03"),
  st("Dinner three hours earlier.", "coffee-picture.jpg",
     "Late eating showed up as more wake events every single time.", step="04"),
  st("Caffeine cutoff at 10am.", "coffee-picture-4.jpg",
     "Not because coffee is bad. Because its half life is six hours.", step="05"),
  st("Four of these did nothing for a friend of mine.", "sleep-aesthetic-1.jpg",
     "Population advice is a starting guess, not an answer."),
  cta("The only result that counts is yours.", None, "yoga-in-park.jpg")])

# ═══════════════════════════════════ REAL APP SCREENS (Ren captures) ══════
# These use actual screenshots from the app, not mockups. The numbers in them
# come from the marketing fixture, so caption them as "what the app says",
# never as "my result" — the same rule as the Oura charts.

deck(slug="app-says-no", lane="nof1", format="proof_stack", ren_tie="hard",
 tier="hard",
 hook="i built an app that tells you when a supplement isn't doing anything",
 caption="most health apps only know how to say yes. this is the screen i'm proudest of.",
 notes="STRONGEST PRODUCT POST IN THE BATCH. An app willing to return a null result "
       "is the entire differentiator. Lead with this one for anything product-led.",
 slides=[
  st("most health apps only know how to say yes", "supplement-picture.jpg",
     "so i built one that can say no"),
  {"type": "proof", "img": "ren-verdict-null.jpg",
   "caption": "Ren, verdict screen. Magnesium, 14 nights, deep sleep 1h12m before and "
              "1h14m after. Inside the night-to-night noise, so it grades as no effect."},
  st("\u201cit isn't your lever\u201d", "sleep-aesthetic-2.jpg",
     "not \u201ctry a higher dose\u201d. not \u201cgive it another month\u201d."),
  st("that sentence costs a supplement company money", "amanda-jones.jpg",
     "which is roughly why nothing else says it"),
  st("half of what's in your cupboard is this screen", "natalie-hordiiuk.jpg",
     "you just haven't run it yet"),
  cta("an app that can't tell you no isn't measuring anything.",
      "Ren runs one change at a time against your own baseline and grades it, "
      "including when the answer is that it did nothing.",
      "mariana-rascao.jpg", "Ren, link in bio")])

deck(slug="app-verdict-worked", lane="nof1", format="proof_stack", ren_tie="hard",
 tier="hard",
 hook="the change that moved my recovery 20% wasn't a supplement",
 caption="fourteen nights, one variable, and a number i didn't control. this is the whole loop.",
 notes="The payoff twin of app-says-no. Post it AFTER the null one, never before: "
       "the no is what makes the yes believable.",
 slides=[
  st("the thing that moved my recovery 20% wasn't a supplement",
     "sleep-aesthetic-3.jpg", "it was what time i stopped eating"),
  {"type": "proof", "img": "ren-verdict-worked2.jpg",
   "caption": "Ren, verdict screen. Last bite before 8pm, 14 nights. Recovery 61 to 73, "
              "which is well past the noise floor for that metric."},
  {"type": "proof", "img": "ren-full-result.jpg",
   "caption": "And every number behind it. Effect estimate with its range, the chance it "
              "helped, the chance it did nothing, and how much data it had to work with."},
  st("the range matters more than the number", "fitness-image-2.jpg",
     "\u201c3.2% better\u201d on its own is a marketing claim. with a range it's a result."),
  st("14 nights. one variable. a rule set before night one.", "cycling-picture-5.jpg"),
  cta("this is the part nobody does for themselves.",
      "Not because it's hard, because it's admin. Ren keeps the baseline, holds you to "
      "the rule you set, and grades it at the end.",
      "sleep-aesthetic-4.jpg", "Ren, link in bio")])

deck(slug="app-chronotype", lane="sleep", format="proof_stack", ren_tie="soft",
 tier="soft",
 hook="apparently i'm a moth",
 caption="six ways to spend a night. i genuinely did not expect to feel called out by a sleep app.",
 notes="PERSONALITY-TEST FORMAT, which is the most reliably shareable thing on the "
       "platform. Broadest reach of any product post here. The comments will be people "
       "guessing their own type, which is exactly what you want.",
 slides=[
  st("apparently i'm a moth", "sleep-aesthetic-1.jpg",
     "late, and never twice at the same hour"),
  {"type": "proof", "img": "ren-chronotype.jpg",
   "caption": "31 nights of my own data. Median lights-out 12:59am, 11 nights of 31 "
              "before midnight, earliest ever 10:22pm."},
  {"type": "proof", "img": "ren-archetypes.jpg",
   "caption": "Six types, split by when the middle of your night falls and how much it "
              "wanders. Everyone lands in exactly one."},
  st("the lark, the hare, the heron", "yoga-in-park.jpg",
     "the otter, the owl, and whatever i am"),
  st("chronotype is largely inherited", "cycling-picture-3.jpg",
     "so the lateness is probably just who you are. the wandering is the part that moves."),
  cta("guess yours before you check.",
      "It's built from your own nights, not a quiz. The app I use for it is in my bio.",
      "sleep-aesthetic-image.jpg")])


# ═══════════════════════════════════════ BROAD / WARM-UP (sells nothing) ══
# Days 4 to 6. These exist to tell TikTok who the audience is before any
# campaign content runs. Niche-adjacent, relatable, zero product, no jargon,
# no CTA, no link. If a post here makes you want to mention Ren, cut the line.

deck(slug="broad-screen-time", lane="sleep", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="i checked my screen time for last week and genuinely felt unwell",
 caption="no advice, no lecture. just posting it so i'm not alone in this.",
 notes="WARM-UP. Pure relatability, no product, no protocol. The comments on this "
       "are where your next ten hooks come from.",
 slides=[
  st("i checked my screen time for last week and genuinely felt unwell", "sleep-aesthetic-1.jpg",
     "posting it so i'm not the only one"),
  st("22 hours. in one week.", "sick-aesthetic-picture.jpg", "on one app."),
  st("most of it after 11pm.", "sleep-aesthetic-2.jpg",
     "which explains a lot about how tuesdays feel."),
  st("i'm not going to pretend i've fixed it.", "cycling-picture-2.jpg"),
  st("i just moved the charger to the kitchen.", "sleep-aesthetic-image.jpg",
     "that's the whole post."),
  cta("how bad is yours, honestly", None, "sleep-aesthetic-4.jpg")])

deck(slug="broad-why-so-tired", lane="sleep", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="why is everyone in their twenties this tired",
 caption="genuine question. nobody i know has energy and we all pretend it's normal.",
 notes="WARM-UP. Broadest reach post in the batch. Asks a question rather than "
       "answering one, which is what makes the comments go.",
 slides=[
  st("why is everyone in their twenties this tired", "fitness-image-1.jpg",
     "genuine question"),
  st("nobody i know has any energy", "person-running-motion-blur.jpg",
     "and we've all just decided that's normal"),
  st("everyone's on their third coffee by noon", "coffee-picture-1.jpg"),
  st("and in bed at 10 saying they're exhausted", "sleep-aesthetic.jpg",
     "then on their phone until 1"),
  st("i don't think it's one thing", "runners-in-motion.jpg",
     "i think it's about six small things at once"),
  cta("what's yours", "genuinely curious what people say", "yoga-in-park.jpg")])

deck(slug="broad-morning-routine-lie", lane="sleep", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="every 5am morning routine video leaves out the same thing",
 caption="not hating on them. just saying what nobody films.",
 notes="WARM-UP. Mild contrarian take on a huge existing format. Rides the morning "
       "routine audience without being one.",
 slides=[
  st("every 5am morning routine video leaves out the same thing", "woman-jumping-on-beach-sunset.jpg"),
  st("what time they went to bed", "sleep-aesthetic-3.jpg"),
  st("5am is not impressive on its own", "yoga-picture.jpg",
     "5am after eight hours is a completely different video to 5am after five"),
  st("one of those is a routine", "fitness-image-5.jpg", "the other one is just being awake"),
  st("nobody films the 9pm part", "sleep-aesthetic-image.jpg",
     "because it's boring and it's the only part that matters"),
  cta("if you do get up at 5, what time are you actually going to bed", None,
      "jorge-alberto-vega-barrera-running-image.jpg")])

deck(slug="broad-gym-year", lane="nof1", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="a year of going to the gym four times a week and the honest list of what changed",
 caption="not the list i expected to be writing.",
 notes="WARM-UP. Broad fitness reach, no health-tech framing at all. Set these to "
       "your real year before posting.",
 slides=[
  st("a year of the gym four times a week", "fitness-image-by-eduardo-cano.jpg",
     "here's the honest list of what changed"),
  st("i look slightly different", "fitness-image-3.jpg",
     "genuinely only slightly. a year is not a transformation.", step="01"),
  st("i sleep better", "sleep-aesthetic-4.jpg",
     "this was the biggest one and nobody talks about it", step="02"),
  st("stairs stopped being a thing", "cycling-picture-5.jpg",
     "small, but i notice it every day", step="03"),
  st("i'm noticeably less irritable", "yoga-picture-1.jpg",
     "which my flatmate mentioned before i did", step="04"),
  st("none of that happened in the first three months", "fitness-image-7.jpg",
     "the first three months were just sore and boring"),
  cta("what actually changed for you", None, "man-running-by-fountain.jpg")])

deck(slug="broad-coffee-personality", lane="nof1", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="i cannot function before my second coffee and i've made that my whole personality",
 caption="posting this from my second coffee.",
 notes="WARM-UP. Light, funny, shareable. No advice at all, which is the point. "
       "Feeds the same audience the caffeine cutoff campaign post needs later.",
 slides=[
  st("i cannot function before my second coffee and i've made that my entire personality",
     "coffee-picture-3.jpg"),
  st("the first one isn't even for enjoyment", "coffee-picture-1.jpg",
     "it's just to get back to neutral"),
  st("i've described myself as \u201cnot a morning person\u201d for about nine years",
     "coffee-picture-4.jpg"),
  st("at some point that stopped being a fact about me", "coffee-picture-2.jpg",
     "and started being a thing i just kept saying"),
  st("anyway. second coffee.", "coffee-picture.jpg", "see you tomorrow."),
  cta("how many are you on", None, "fitness-image-4.jpg")])

deck(slug="broad-sunday-night", lane="sleep", format="photo_listicle", ren_tie="none",
 tier="broad",
 hook="the sunday night thing where you're exhausted and cannot fall asleep",
 caption="does this have a name yet or are we all just doing it",
 notes="WARM-UP. Extremely relatable, zero product. Post this on a Sunday evening.",
 slides=[
  st("the sunday night thing where you're exhausted and still can't fall asleep",
     "sleep-aesthetic-2.jpg", "does this have a name yet"),
  st("you got up at 11 on saturday", "sleep-aesthetic-image.jpg",
     "and again on sunday"),
  st("so at 11pm your body thinks it's 9", "sick-aesthetic-picture.jpg"),
  st("then monday's alarm goes off at 7", "sleep-aesthetic-1.jpg",
     "and you start the week two hours behind"),
  st("i'm not going to tell you to stop lying in", "cycling-picture-3.jpg",
     "i'm just saying that's what it is"),
  cta("every single sunday", None, "sleep-aesthetic-3.jpg")])


# ═══════════════════════════════════════════════════════════ BLOODWORK ════
deck(slug="blood-tired-normal-labs", lane="bloodwork", format="problem_solution", ren_tie="soft",
 hook="Eight hours of sleep and you still feel like this",
 caption="Normal range is the band 95% of people fall inside. Exhausted people are in it too.",
 notes="Strongest Ren fit in the batch. This is the bloodwork PDF use case verbatim.",
 slides=[
  st("Eight hours of sleep. Still wrecked.", "fitness-image-1.jpg",
     "And your bloodwork came back “normal”."),
  {"type": "ps", "bands": [
    {"head": "WHAT THEY CHECKED", "color": "#8b8a85", "cells": [
      {"label": "Hemoglobin", "img": "cycling-picture-1.jpg"},
      {"label": "TSH, alone", "img": "runners-in-motion.jpg"}]},
    {"head": "WHAT EXPLAINS IT", "color": "#0f9d63", "cells": [
      {"label": "Ferritin", "img": "mariana-rascao.jpg"},
      {"label": "Free T3 and T4", "img": "natalie-hordiiuk.jpg"}]}]},
  st("Normal range is not your range.", "person-running-motion-blur.jpg",
     "It's the band 95% of people fall inside. Including the exhausted ones."),
  {"type": "grid", "question": "The four that get skipped", "layout": "g2x2", "cells": [
    {"label": "Ferritin", "img": "akshay-chauhan.jpg"},
    {"label": "Vitamin D", "img": "woman-jumping-on-beach-sunset.jpg"},
    {"label": "B12 and folate", "img": "supplement-picture.jpg"},
    {"label": "hs-CRP", "img": "fitness-image-6.jpg"}]},
  st("Ask what your number is.", "mariana-rascao.jpg",
     "Not whether it's in range. Those are two different questions."),
  cta("Take this list to your next appointment.",
      "Then keep the results somewhere that reads them back to you. I use Ren for that, it's in my bio.",
      "cycling-picture-3.jpg")])

deck(slug="blood-always-cold", lane="bloodwork", format="cause_grid", ren_tie="none",
 hook="You're wearing a jacket indoors again",
 caption="Four things worth ruling out before you buy another blanket.",
 notes="GlowUpLexicon question format carrying a lab topic.",
 slides=[
  st("You're wearing a jacket indoors again.", "cycling-picture-4.jpg",
     "Everyone else is fine. You are not being dramatic."),
  {"type": "grid", "question": "“Why am I always cold?”", "layout": "g2x2", "cells": [
    {"label": "Low ferritin", "img": "mariana-rascao.jpg"},
    {"label": "Underactive thyroid", "img": "sick-aesthetic-picture.jpg"},
    {"label": "Eating too little", "img": "coffee-picture-1.jpg"},
    {"label": "Low B12", "img": "akshay-chauhan.jpg"}]},
  st("Ferritin is iron storage.", "fitness-image-6.jpg",
     "It can sit near empty while your hemoglobin looks perfect."),
  st("TSH alone misses it.", "amanda-jones.jpg",
     "Ask for free T3 and free T4 in the same draw."),
  st("Three of these are one blood draw apart.", "cycling-picture-1.jpg"),
  cta("People guess at this for years.", "It's a single panel.", "yoga-picture.jpg")])

deck(slug="blood-hrv-low", lane="bloodwork", format="cause_grid", ren_tie="none",
 hook="You slept eight hours and your HRV still tanked",
 caption="HRV is mostly a mirror. These are the four things it's usually reflecting.",
 notes="Bridges the bloodwork and sleep lanes. Watch whether it pulls sleep viewers.",
 slides=[
  st("You slept eight hours and your HRV still tanked.", "runners-in-motion.jpg"),
  {"type": "grid", "question": "“Why is my HRV so low?”", "layout": "g2x2", "cells": [
    {"label": "Alcohol", "img": "wine-at-night.jpg"},
    {"label": "Training late", "img": "fitness-image-6.jpg"},
    {"label": "Getting sick", "img": "sick-aesthetic-picture.jpg"},
    {"label": "Under-slept", "img": "sleep-aesthetic-1.jpg"}]},
  st("Alcohol is the biggest overnight hit there is.", "cycling-picture-5.jpg"),
  st("HRV drops a day or two before you feel ill.", "sick-aesthetic-picture.jpg"),
  st("One low night is weather.", "fitness-image-3.jpg", "Seven is climate."),
  cta("Compare your week to your own baseline.",
      "Never to someone else's number.", "cycling-camera-strap.jpg")])

deck(slug="blood-5-markers-missed", lane="bloodwork", format="photo_listicle", ren_tie="hard",
 hook="Your labs came back normal. Nobody read them to you.",
 caption="Every one of these can sit inside the reference range and still be the reason you feel bad.",
 notes="Hard CTA. Only scale it once a soft version of the same idea has travelled.",
 slides=[
  st("Your labs came back normal.", "fitness-image-4.jpg", "Nobody actually read them to you."),
  st("Ferritin.", "mariana-rascao.jpg",
     "Iron storage. Can be near the floor while hemoglobin looks fine.", step="01"),
  st("Free T3.", "women-running-silhouette.jpg",
     "The active thyroid hormone. TSH alone can look perfect.", step="02"),
  st("Vitamin D.", "yoga-picture-1.jpg",
     "Low across most of the northern hemisphere, most of the year.", step="03"),
  st("hs-CRP.", "fitness-image-7.jpg",
     "Background inflammation. Cheap, and almost never ordered.", step="04"),
  st("Fasting insulin.", "running-image.jpg",
     "Moves years before fasting glucose does. Not on a standard panel.", step="05"),
  cta("Upload the PDF and have it read back to you.",
      "That's what I built Ren for. It reads your actual bloodwork, tells you which markers "
      "explain what you're feeling, and then sets up a two week test on the one that matters.",
      "man-running-by-fountain.jpg", "Ren, link in bio")])

# ═════════════════════════════════════════════════════ THE STACK PROBLEM ══
deck(slug="stack-nine-bottles", lane="stack", format="photo_listicle", ren_tie="hard",
 hook="Count the bottles in your cupboard",
 caption="I'm not saying they don't work. I'm saying you have no way of knowing which ones do.",
 notes="Highest-intent lane in the batch. These people have already spent the money; "
       "they're looking for permission to stop guessing. Set the counts to YOUR real "
       "cupboard before posting.",
 slides=[
  st("Count the bottles in your cupboard.", "natalie-hordiiuk.jpg",
     "Now tell me which one is doing something."),
  st("Nine.", "natalie-hordiiuk.jpg", "That was mine. About £60 a month.", step="01"),
  st("I started six of them in the same month.", "amanda-jones.jpg",
     "Which means I can't attribute anything to any of them.", step="02"),
  st("I started them all in January.", "cycling-picture-3.jpg",
     "When I felt terrible. I was always going to feel better by March.", step="03"),
  st("I never measured anything first.", "fitness-image-by-samuel-girven.jpg",
     "No baseline. So there was nothing to compare to.", step="04"),
  st("Two of them, I just kept buying.", "ambitious-studio-by-rick-barrett.jpg",
     "Not because they worked. Because stopping felt like a risk.", step="05"),
  st("This is the trap.", "sleep-aesthetic-1.jpg",
     "Supplements are cheap enough to keep buying and subtle enough that you can never tell."),
  cta("You can find out. It just takes two weeks per thing.",
      "That's the whole reason I built Ren. It stops one variable, watches your own numbers, "
      "and tells you whether anything actually changed.",
      "mariana-rascao.jpg", "Ren, link in bio")])

deck(slug="stack-cant-tell", lane="stack", format="cause_grid", ren_tie="soft",
 hook="Why you can't tell if a supplement is working",
 caption="Five reasons, and four of them are things you did without noticing.",
 notes="The methodology post for the stack lane. Save rate should be high on this one.",
 slides=[
  st("Why can't you tell if it's working?", "supplement-picture.jpg",
     "It's not that the effect is invisible. It's that you set the test up wrong."),
  {"type": "grid", "question": "The four mistakes", "layout": "g2x2", "cells": [
    {"label": "Started three at once", "img": "natalie-hordiiuk.jpg"},
    {"label": "Started when you felt awful", "img": "sick-aesthetic-picture.jpg"},
    {"label": "No baseline", "img": "sleep-aesthetic-image.jpg"},
    {"label": "Judging by feel", "img": "person-running-motion-blur.jpg"}]},
  st("Three at once tells you nothing about any of them.", "natalie-hordiiuk.jpg"),
  st("You started when you felt worst.", "sick-aesthetic-picture.jpg",
     "You were going to feel better anyway. That's regression, not the pill."),
  st("Without a baseline there's nothing to compare to.", "fitness-image-5.jpg",
     "Seven days of doing nothing is the most boring and most important week."),
  st("And “I feel sharper” is not a measurement.", "coffee-picture-2.jpg",
     "Pick a number you don't control. Deep sleep. Resting heart rate."),
  cta("One thing. Two weeks. One number.",
      "It's genuinely that simple, it's just annoying to keep track of. That's the part I "
      "let Ren do. It's in my bio.",
      "akshay-chauhan.jpg")])

deck(slug="stack-quit-one", lane="stack", format="photo_listicle", ren_tie="soft",
 hook="The fastest way to find out what's doing nothing",
 caption="Stop them. One at a time. Most people have never tried this and it costs nothing.",
 notes="The subtraction angle. Nobody in this niche posts it, because the niche is funded "
       "by addition. Expect this to travel and to annoy people in the comments.",
 slides=[
  st("The fastest way to find out what's doing nothing", "ambitious-studio-by-rick-barrett.jpg",
     "is to stop taking it."),
  st("Pick the most expensive one.", "amanda-jones.jpg", "Start there.", step="01"),
  st("Stop it. Change nothing else.", "supplement-picture.jpg",
     "This is the hard part. Not the stopping, the nothing else.", step="02"),
  st("Fourteen days.", "sleep-aesthetic-3.jpg",
     "Long enough to clear day-to-day noise. Short enough that you'll actually finish.", step="03"),
  st("Watch one number, not your mood.", "fitness-image-2.jpg",
     "Deep sleep, resting heart rate, time to fall asleep. Something you don't control.", step="04"),
  st("Nothing moved?", "coffee-picture-3.jpg", "You just got that money back. Every month.", step="05"),
  st("Most of my stack didn't survive this.", "natalie-hordiiuk.jpg",
     "Two things did. I'm much more confident about those two than I ever was about nine."),
  cta("Worth doing even if you never buy anything again.",
      "I run these with Ren because remembering what I stopped and when is the bit I always "
      "got wrong. Bio if you want it.",
      "cycling-picture.jpg")])

deck(slug="stack-huberman-1000h", lane="stack", format="photo_listicle", ren_tie="hard",
 hook="I watched 1000 hours of Huberman so you don't have to",
 caption="These are the protocols that come up over and over. He's right that they're worth trying. He cannot tell you which ones are yours.",
 notes="Name-check post. Do not imply endorsement, do not use his likeness, do not invent "
       "quotes. The turn at slide 7 is the whole post; everything before it is the bait.",
 slides=[
  st("I watched 1000 hours of Huberman", "fitness-image-by-eduardo-cano.jpg",
     "so you don't have to. Here's what actually comes up over and over."),
  st("Sunlight in your eyes within an hour of waking.", "woman-jumping-on-beach-sunset.jpg",
     "Ten minutes outside. The single most repeated one.", step="01"),
  st("Delay your first coffee 90 minutes.", "coffee-picture-3.jpg",
     "So adenosine clears on its own instead of getting masked.", step="02"),
  st("Zone 2, two to three hours a week.", "cycling-picture-5.jpg",
     "Slow enough to hold a conversation. Boring on purpose.", step="03"),
  st("Ten minutes of non-sleep deep rest.", "yoga-picture.jpg",
     "Lie down, eyes closed, no input. Not a nap.", step="04"),
  st("The sleep stack: magnesium, theanine, apigenin.", "akshay-chauhan.jpg",
     "The most quoted three, and the most bought three.", step="05"),
  st("Here's the part that took me 1000 hours to notice.", "fitness-image-6.jpg"),
  st("Every one of these is an average.", "runners-in-motion.jpg",
     "It's what happened to a group of people in a study. It is not a prediction about you."),
  st("Two of these did nothing for me.", "sleep-aesthetic-2.jpg",
     "I only know that because I stopped them one at a time and watched what happened."),
  cta("He can tell you what's worth trying. He can't tell you what works on you.",
      "Nobody can, from a podcast. That's the gap Ren fills: one protocol at a time, "
      "against your own baseline, with a verdict at the end.",
      "sleep-aesthetic-4.jpg", "Ren, link in bio")])

# ══════════════════════════════════════════════════════════════ N-OF-1 ════
deck(slug="nof1-caffeine-cutoff", lane="nof1", format="proof_stack", ren_tie="soft",
 hook="i didn't quit coffee. i just moved it four hours earlier",
 caption="same two cups, different hour. i didn't grade this one either, the app did.",
 notes="REBUILT on a real screenshot. NEEDS A FRESH CAPTURE: currently reuses the "
       "worked-verdict screen, which is about a different experiment. Replace "
       "ren-verdict-worked2.jpg with a caffeine-cutoff capture before posting.",
 slides=[
  st("i didn't quit coffee. i just moved it four hours earlier", "coffee-picture-3.jpg",
     "it took 16 minutes off how long i lie there\u2026"),
  {"type": "protocol", "title": "Caffeine cutoff, time to fall asleep",
   "photo": "coffee-picture-2.jpg", "rows": [
    [" what ", "same 2 coffees"], [" change ", "last one before 10am"],
    [" baseline ", "7 days, usual 2pm"], [" trial ", "14 days"],
    [" measured ", "minutes to sleep"]],
   "success_rule": "Time to fall asleep drops 5 minutes or more on average."},
  {"type": "proof", "img": "ren-verdict-worked2.jpg",
   "caption": "Ren, verdict screen. Fourteen nights, well past the noise floor for "
              "this metric. PLACEHOLDER \u2014 swap for the caffeine capture."},
  st("this one costs nothing.", "coffee-picture-4.jpg",
     "no supplement. no purchase. a different hour."),
  cta("16 minutes for me. possibly zero for you.",
      "it costs nothing to find out which, and fourteen days to know for certain. bio.",
      "sleep-aesthetic-image.jpg")])

deck(slug="nof1-magnesium-form", lane="nof1", format="problem_solution", ren_tie="none",
 hook="The magnesium in your cupboard is probably a laxative",
 caption="The cheap one on the shelf is magnesium oxide. Check the back of the bottle.",
 notes="AWOOGA 99/1 format with real object photos in all four panels.",
 slides=[
  st("The magnesium in your cupboard", "supplement-picture.jpg",
     "is probably being sold as a laxative."),
  {"type": "ps", "bands": [
    {"head": "99% BUY", "color": "#d93f3e", "cells": [
      {"label": "Magnesium oxide", "img": "amanda-jones.jpg"},
      {"label": "“Magnesium”, no form", "img": "supplement-picture.jpg"}]},
    {"head": "1% BUY", "color": "#0f9d63", "cells": [
      {"label": "Magnesium glycinate", "img": "akshay-chauhan.jpg"},
      {"label": "Magnesium L-threonate", "img": "natalie-hordiiuk.jpg"}]}]},
  st("Oxide is about 4% absorbed.", "ambitious-studio-by-rick-barrett.jpg",
     "It's the cheapest form to make, which is why it's on every shelf."),
  st("The rest pulls water into your gut.", "fitness-image-5.jpg",
     "That's the laxative effect. It is not the sleep effect."),
  st("right form, wrong person, still nothing.", "mariana-rascao.jpg"),
  cta("Buy the good one. Then check whether it moved a number.",
      None, "sleep-aesthetic-3.jpg")])

deck(slug="nof1-how-to-run-one", lane="nof1", format="photo_listicle", ren_tie="soft",
 hook="You've been guessing for years",
 caption="Five rules, fourteen days, a phone you already own.",
 notes="Methodology post. Low view ceiling, high save and follow ceiling. This is the one "
       "that makes the account worth following instead of scrolling.",
 slides=[
  st("You've been guessing for years.", "person-running-photo.jpg",
     "Here's how to actually test something on yourself."),
  st("One variable.", "fitness-image-by-andrew-valdivia.jpg",
     "Change two and you've learned nothing about either.", step="01"),
  st("Seven days of doing nothing first.", "cycling-picture-5.jpg",
     "The baseline. This is the part everyone skips.", step="02"),
  st("Write the success rule before day one.", "fitness-image-2.jpg",
     "“Deep sleep up 8 minutes.” Decided in advance so you can't move it after.", step="03"),
  st("Pick a number you don't control.", "jorge-alberto-vega-barrera-running-image.jpg",
     "Deep sleep. Resting heart rate. Not “how I felt”.", step="04"),
  st("Let it be a no.", "cycling-picture-1.jpg",
     "Most things won't work for you. That is the result.", step="05"),
  cta("Intake. Propose. Adhere. Reassess. Adjust.",
      "That loop is the entire app I built. If you'd rather not keep the spreadsheet yourself, "
      "it's in my bio.",
      "fitness-image-by-samuel-girven.jpg")])

deck(slug="nof1-what-didnt-work", lane="nof1", format="proof_stack", ren_tie="none",
 hook="i tested this for 14 nights and it did absolutely nothing",
 caption="posting the failures is the only reason to trust the wins.",
 notes="REBUILT on the real null-verdict screen. This is the credibility post; keep "
       "it in the rotation even when it underperforms.",
 slides=[
  st("i tested this for 14 nights and it did absolutely nothing", "supplement-picture.jpg",
     "posting it anyway, because you should see what a no looks like"),
  {"type": "protocol", "title": "Topical magnesium, deep sleep",
   "photo": "amanda-jones.jpg", "rows": [
    [" what ", "magnesium oil, calves"], [" when ", "30 min before bed"],
    [" baseline ", "7 nights"], [" trial ", "14 nights"],
    [" measured ", "Oura deep sleep"]],
   "success_rule": "Deep sleep up 8 minutes on average."},
  {"type": "proof", "img": "ren-verdict-null.jpg",
   "caption": "Ren, verdict screen. Inside the night-to-night noise, so it grades as "
              "no effect. The app is willing to say that. Most aren't."},
  st("a method that can't return no isn't a method.", "cycling-picture-4.jpg"),
  cta("half of what you're taking is probably this screen.",
      "you won't know which half until you stop one and watch.",
      "akshay-chauhan.jpg")])

deck(slug="nof1-rhr-39", lane="nof1", format="proof_stack", ren_tie="hard",
 hook="My resting heart rate is 39",
 caption="Real screenshot. Ranked by how much each thing actually moved it, which means the boring one is first and the supplements are near the bottom.",
 notes="The screenshot is the post; everything after is the explanation.",
 slides=[
  st("My resting heart rate is 39.", "jorge-alberto-vega-barrera-running-image.jpg",
     "Here's everything that did it, including the parts I can't take credit for."),
  {"type": "proof", "stat": "39", "stat_unit": "bpm average", "img": "oura-rhr-week.jpg",
   "caption": "Oura, week of Aug 16 to 22. Range 37 to 45. Eight runs that week."},
  st("Eight runs that week.", "man-running-by-fountain.jpg",
     "Most of them slow enough to hold a conversation. This is most of the answer.", step="01"),
  st("No alcohol.", "cycling-picture-1.jpg",
     "One drink is worth about 3 to 5 bpm on my own numbers.", step="02"),
  st("A fixed sleep window.", "sleep-aesthetic.jpg",
     "Same bedtime within half an hour. Regularity beat total hours.", step="03"),
  st("Magnesium does nothing I can see here.", "ambitious-studio-by-rick-barrett.jpg",
     "It gets me to sleep faster. It does not show up in this number."),
  st("And the part I didn't earn.", "cycling-picture-3.jpg",
     "Years of aerobic base, and being young. Two people doing all of this land in different places."),
  cta("Don't copy my list. Test one line of it on you.",
      "That's the whole idea behind Ren. It takes your Oura or Apple Health data, runs one "
      "change at a time, and tells you after two weeks whether it actually did anything.",
      "person-running-motion-blur.jpg", "Ren, link in bio")])

deck(slug="nof1-sleep-debt-rebound", lane="sleep", format="proof_stack", ren_tie="hard",
 hook="I was 9 hours and 40 minutes behind on sleep",
 caption="Travel, then getting sick. This is the order I did things in, and the Saturday habit that sets most people back.",
 notes="RECOVERY ARC. The chart has a beginning and an end, which the RHR one doesn't. "
       "Lead the account with this.",
 slides=[
  st("I was 9 hours and 40 minutes behind on sleep.", "sleep-aesthetic-2.jpg",
     "Travel, then a cold. Here's the ten days back."),
  {"type": "proof", "stat": "9h 40m", "stat_unit": "down, at the peak", "img": "oura-sleep-debt.jpg",
   "caption": "Oura sleep debt, Aug 16 to Sep 6. Peak 9h40m on Aug 27, against a 7h26m need. Back inside Low by Sep 6."},
  st("Earlier bedtime. Not a later alarm.", "sleep-aesthetic-image.jpg",
     "Sleeping in moves your body clock and costs you the next night.", step="days 1 to 3"),
  st("Training down, not out.", "fitness-image-5.jpg",
     "Hard sessions on top of debt just extend it.", step="days 1 to 3"),
  st("Alcohol at zero.", "cycling-picture.jpg",
     "It's the one input that makes recovery sleep worse while you're asleep.", step="days 1 to 3"),
  st("An extra hour a night, for a week.", "sleep-aesthetic-3.jpg",
     "Debt clears over nights. Not in one long one.", step="days 4 to 10"),
  st("Daylight within 30 minutes of waking.", "yoga-picture-1.jpg",
     "After travel this is what re-anchors the clock.", step="days 4 to 10"),
  st("The twelve hour Saturday made it worse.", "sleep-aesthetic-1.jpg",
     "Felt incredible. Pushed my bedtime two hours late and I paid for it until Tuesday."),
  st("Melatonin is a timing signal, not a sedative.", "mariana-rascao.jpg",
     "Low dose, taken early, to drag a travel-shifted clock back. More doesn't work better."),
  st("The line came down because of hours in bed.", "sick-aesthetic-picture.jpg",
     "That's the honest version."),
  cta("If you want to know which part did it, you have to test one at a time.",
      "I built Ren to do exactly that. It watches your own baseline and tells you, after "
      "two weeks, whether the thing you changed actually mattered.",
      "sleep-aesthetic-4.jpg", "Ren, link in bio")])
# ═════════════════════════════════════════════════════════════ HOOKS ══════
# Slide one, in the register of the accounts that actually travel: long,
# lowercase, a parenthetical or an ellipsis, and a stake you'd recognise.
# Punchy four-word headlines read as written by a copywriter. These read as
# typed by a person, which is the whole game.
HOOKS = {
 "sleep-wake-at-3am": (
   "i woke up at 3am every night for a month and blamed stress",
   "it was four things and none of them were stress"),
 "sleep-deep-sleep-fix": (
   "my deep sleep was 40 minutes a night and i assumed i just wasn't a good sleeper",
   "turns out it's decided before you get into bed"),
 "sleep-magnesium-14-nights": (
   "everyone kept telling me magnesium would fix my sleep so i actually tested it for 21 nights",
   "the chart is not what i expected\u2026"),
 "sleep-5-non-supplement": (
   "5 things that fixed my sleep and cost me nothing",
   "(i wasted about \u00a3400 on supplements before any of these)"),
 "blood-tired-normal-labs": (
   "i was sleeping 8 hours and still falling asleep at my desk by 3pm. my bloodwork came back \u201cnormal\u201d",
   "here's what nobody actually checked\u2026"),
 "blood-always-cold": (
   "if you're the one wearing a hoodie indoors in july, this is probably why",
   "it's four things and they're all on one blood panel"),
 "blood-hrv-low": (
   "my ring kept telling me my hrv was low and i genuinely thought it was broken",
   "it wasn't. it was reflecting four things i was doing"),
 "blood-5-markers-missed": (
   "5 things on your blood test that can be \u201cin range\u201d and still be the reason you feel awful",
   "nobody read these back to you"),
 "stack-nine-bottles": (
   "i counted the supplements in my cupboard and then worked out what i'd spent on them",
   "i felt genuinely sick\u2026"),
 "stack-cant-tell": (
   "why you genuinely cannot tell whether a supplement is working",
   "(four mistakes. i have made all four of them)"),
 "stack-quit-one": (
   "the fastest way to find out which of your supplements do nothing is to stop taking them",
   "nobody in this corner of the internet will tell you this"),
 "stack-huberman-1000h": (
   "i watched 1000 hours of huberman so you don't have to",
   "(the last slide is the part nobody says out loud)"),
 "nof1-caffeine-cutoff": (
   "i didn't quit coffee. i just moved it four hours earlier",
   "it took 16 minutes off how long i lie there\u2026"),
 "nof1-magnesium-form": (
   "the magnesium in your cupboard is probably being sold as a laxative",
   "(go and check the back of the bottle, i'll wait)"),
 "nof1-how-to-run-one": (
   "you've been guessing about your own body for years",
   "here's how to actually test something on yourself in 14 days"),
 "nof1-what-didnt-work": (
   "i tested this for 14 nights and it did absolutely nothing",
   "posting it anyway, because you should see what a no looks like"),
 "nof1-rhr-39": (
   "my resting heart rate is 39 and it's mostly not the thing you think it is",
   "ranked by what actually moved it\u2026"),
 "nof1-sleep-debt-rebound": (
   "i came back from a trip 9 hours and 40 minutes down on sleep and genuinely felt unwell",
   "here's the ten days back\u2026"),
}

for d in D:
    h = HOOKS.get(d["slug"])
    if not h:
        continue
    text, sub = h
    d["hook"] = text
    first = d["slides"][0]
    if first.get("type") == "statement":
        first["text"], first["sub"] = text, sub
    else:                      # grid or ps deck: push a photo hook in front
        d["slides"].insert(0, {"type": "statement", "text": text, "sub": sub,
                               "photo": first.get("photo")})


# ═══════════════════════════════════════════════════════════════ CTAs ═════
# Every closing slide lands on the same claim, in different words: a video
# cannot tell you whether something works on YOU. Only a test can. Vary the
# wording, never the claim.
CTA = {
 "sleep-wake-at-3am": ("none",
   "none of this is advice about you. it's advice about people.",
   "the only way to find out which of the four is yours is to change one, hold it two weeks, and watch one number."),
 "sleep-deep-sleep-fix": ("soft",
   "you cannot feel deep sleep, so you cannot judge this by how you feel.",
   "pick one of the four, hold it fourteen nights, compare the averages. i use an app called Ren to do the comparing. bio."),
 "sleep-magnesium-14-nights": ("soft",
   "my +17 minutes is not a prediction about your +17 minutes.",
   "same supplement, same dose, different person, different answer. the only number that means anything is yours. Ren runs that test. bio."),
 "sleep-5-non-supplement": ("none",
   "four of these did nothing for a friend of mine.",
   "which means the list isn't the point. running one of them for two weeks and watching what happens is the point."),
 "blood-tired-normal-labs": ("soft",
   "a normal range is a statement about a population.",
   "your number is a statement about you, and they are not the same sentence. get the panel, then test one thing against it."),
 "blood-always-cold": ("none",
   "you could guess at this for another two years.",
   "or get one panel, pick the marker that's low, change one thing, and see if the number moves in six weeks."),
 "blood-hrv-low": ("none",
   "stop comparing your hrv to anyone else's.",
   "compare this week to your own last month. that comparison is the only one that can tell you anything."),
 "blood-5-markers-missed": ("hard",
   "knowing the number is step one. finding out what moves YOUR number is the actual work.",
   "Ren reads your bloodwork, picks the marker that explains how you feel, and runs a two-week test on it against your own baseline. link in bio."),
 "stack-nine-bottles": ("hard",
   "you don't need to throw them out. you need to find out.",
   "one at a time, two weeks each, one number you don't control. Ren keeps track so you don't have to. link in bio."),
 "stack-cant-tell": ("soft",
   "every one of those four mistakes has the same fix.",
   "one variable, a baseline first, a rule written down before you start. that's an experiment. everything else is a vibe. bio."),
 "stack-quit-one": ("soft",
   "the stopping is free. the knowing is what you get.",
   "fourteen days without the most expensive one, watching a number you don't control. i use Ren to run it. bio."),
 "stack-huberman-1000h": ("hard",
   "he can tell you what's worth trying. nobody can tell you what works on you.",
   "that gap is not a gap in the science, it's the whole point of n-of-1. Ren closes it: one protocol, your baseline, a verdict in two weeks. link in bio."),
 "nof1-caffeine-cutoff": ("soft",
   "16 minutes for me. possibly zero for you.",
   "it costs nothing to find out which, and fourteen days to know for certain. bio."),
 "nof1-magnesium-form": ("none",
   "right form, wrong person, still nothing.",
   "buying the good one is the easy half. checking whether it moved a number on you is the half everyone skips."),
 "nof1-how-to-run-one": ("soft",
   "this is the whole method and it fits on one slide.",
   "one variable. a baseline first. a rule set in advance. a number you don't control. and a real willingness to get a no. bio."),
 "nof1-what-didnt-work": ("none",
   "half of what you're taking is probably this chart.",
   "you won't know which half until you stop one and watch."),
 "nof1-rhr-39": ("hard",
   "do not copy this list. test one line of it.",
   "years of base and being young are doing more work here than anything you can buy. Ren tells you which line is actually yours. link in bio."),
 "nof1-sleep-debt-rebound": ("hard",
   "i can tell you the order i did things in. i can't tell you which one did it.",
   "neither can anyone else, from the outside. Ren runs them one at a time against your own baseline until the answer is a number. link in bio."),
 "app-says-no": ("hard",
   "an app that can't tell you no isn't measuring anything.",
   "Ren grades one change at a time against your own data, including when the grade is that nothing happened. link in bio."),
 "app-verdict-worked": ("hard",
   "the range matters more than the number.",
   "\u201c3.2% better\u201d is a marketing claim. \u201c3.2% better, 2.4 to 4.0, on your own eight-week baseline\u201d is a result. link in bio."),
 "app-chronotype": ("soft",
   "this one is built from your nights, not a quiz.",
   "which is the difference between a personality test and a measurement. bio."),
 "broad-screen-time": ("none", "how bad is yours, honestly", "no judgement, i'm posting mine."),
 "broad-why-so-tired": ("none", "what's yours", "genuinely curious what people say."),
 "broad-morning-routine-lie": ("none",
   "if you get up at 5, what time are you actually going to bed",
   "that's the number that decides whether it's a routine."),
 "broad-gym-year": ("none", "what actually changed for you", "and how long did it take before you noticed."),
 "broad-coffee-personality": ("none", "how many are you on", "be honest."),
 "broad-sunday-night": ("none", "every single sunday", "tell me it's not just me."),
}

for d in D:
    c = CTA.get(d["slug"])
    if not c:
        continue
    tie, text, sub = c
    last = d["slides"][-1]
    if last.get("type") == "cta":
        last["text"], last["sub"] = text, sub
        if tie == "hard" and not last.get("pill"):
            last["pill"] = "Ren, link in bio"
        if tie != "hard":
            last.pop("pill", None)
    d["ren_tie"] = tie
    d["tier"] = {"none": "core", "soft": "soft", "hard": "hard"}.get(tie, d.get("tier"))
    if d["slug"].startswith("broad-"):
        d["tier"] = "broad"


# ═════════════════════════════════════════════════════ HOOKS, STYLE B ═════
# Direct-address, promise-led, second person, trailing ellipsis. This is the
# clipper-campaign genre: it sells the payoff up front instead of earning it
# with a confession. Higher click-through, weaker at building a person.
#
# Style A (the HOOKS dict above) is first-person confessional. Both are here
# so the account can actually TEST which one works, rather than guess:
#     python3 src/render.py content/batch01/ --hook b
HOOKS_B = {
 "sleep-wake-at-3am": ("Here's exactly why you keep waking up at 3am\u2026", "4 causes, none of them stress"),
 "sleep-deep-sleep-fix": ("4 reasons your deep sleep is so low\u2026", "all four happen before you get into bed"),
 "sleep-magnesium-14-nights": ("Here's exactly what magnesium did to my deep sleep\u2026", "21 nights, graded by the app not by me"),
 "sleep-5-non-supplement": ("5 ways to fix your sleep without buying anything\u2026", "ranked by what actually moved the number"),
 "blood-tired-normal-labs": ("Here's exactly why you're exhausted with \u201cnormal\u201d labs\u2026", "4 markers nobody ordered"),
 "blood-always-cold": ("Here's exactly why you're always cold\u2026", "4 things, all on one blood panel"),
 "blood-hrv-low": ("Here's exactly why your HRV is so low\u2026", "and why it's not the thing you think"),
 "blood-5-markers-missed": ("5 blood markers your doctor never explained\u2026", "every one can be \u201cin range\u201d and still wreck you"),
 "stack-nine-bottles": ("Here's exactly why your supplements aren't working\u2026", "and what they're costing you a month"),
 "stack-cant-tell": ("4 reasons you can't tell if a supplement is working\u2026", "I've made all four"),
 "stack-quit-one": ("Here's exactly how to find the supplements doing nothing\u2026", "it costs nothing and takes 14 days"),
 "stack-huberman-1000h": ("5 protocols Huberman repeats the most\u2026", "and the one thing none of them can tell you"),
 "nof1-caffeine-cutoff": ("Here's exactly what moving your coffee 4 hours does\u2026", "same caffeine, different hour"),
 "nof1-magnesium-form": ("Here's exactly why your magnesium does nothing\u2026", "check the back of the bottle"),
 "nof1-how-to-run-one": ("5 rules for testing anything on yourself\u2026", "14 days and a phone you already own"),
 "nof1-what-didnt-work": ("Here's exactly what 14 nights of magnesium spray did\u2026", "nothing. posting it anyway"),
 "nof1-rhr-39": ("Here's exactly how I got my resting heart rate to 39\u2026", "ranked, and it's not what you'd guess"),
 "nof1-sleep-debt-rebound": ("Here's exactly how to clear 9 hours of sleep debt\u2026", "10 days, in order"),
 "app-says-no": ("Here's exactly how to know a supplement isn't working\u2026", "most apps will never tell you this"),
 "app-verdict-worked": ("Here's exactly what moved my recovery 20%\u2026", "it wasn't a supplement"),
 "app-chronotype": ("6 sleep types. Here's exactly which one you are\u2026", "built from your nights, not a quiz"),
 "broad-screen-time": ("Here's exactly how bad my screen time got\u2026", "no advice, just posting it"),
 "broad-why-so-tired": ("Here's exactly why everyone in their 20s is exhausted\u2026", "it's about 6 small things at once"),
 "broad-morning-routine-lie": ("Here's exactly what every 5am routine video leaves out\u2026", "and it's the only part that matters"),
 "broad-gym-year": ("5 things a year of the gym actually changed\u2026", "not the list I expected"),
 "broad-coffee-personality": ("Here's exactly how many coffees it takes me to function\u2026", "I've made it a personality"),
 "broad-sunday-night": ("Here's exactly why you can't sleep on Sunday nights\u2026", "you did it to yourself on Saturday"),
}

for d in D:
    b = HOOKS_B.get(d["slug"])
    if b:
        d["hook_b"], d["hook_b_sub"] = b


for d in D:
    (OUT / f"{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print(f"wrote {len(D)} decks, {sum(len(d['slides']) for d in D)} slides")
