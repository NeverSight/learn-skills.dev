---
name: mastery-loop
description: >-
  Turn any study material — lecture slides (PPTX), textbook PDFs, lecture notes,
  transcripts, or a whole course folder — into a spaced-repetition MASTERY system
  that actually makes the learner remember it, instead of a pile of pretty notes.
  Runs a short daily active-recall loop driven by a real forgetting-curve
  scheduler, with interleaving, Feynman checks, calibration, and error-driven
  review, and it adapts to how each individual learner learns. Built for total
  beginners with zero background in the subject. USE THIS whenever the user wants
  to study, learn, or master a topic over time, prepare for an exam, "finally
  remember" something, stop forgetting, review course material, or get
  flashcards/quizzes that keep testing them on a schedule — even if they only say
  "help me learn X", "I have an exam", or "let's do today's review", and never
  mention spaced repetition. Do NOT use it for one-off requests with no ongoing
  study intent: summarizing, translating, or explaining a passage; writing an
  essay; answering a single question; or just generating and exporting a
  flashcard/Anki deck when the user says that's all they need and doesn't want
  recurring review. For a single explanation of one concept (teach me / explain /
  ELI5 / quiz me on this), prefer the sibling "learn" skill; mastery-loop is for
  ongoing study of a body of material toward lasting retention.
---

# mastery-loop

A skill that takes a beginner from zero to genuine mastery of a subject by running
a compounding daily learning loop — not by generating a mountain of notes.

## The one idea that makes this different

Almost every AI study tool **generates material and stops**. But producing notes
is not learning; *remembering over time* is, and that is governed by the
forgetting curve. So this skill's center of gravity is a **daily retrieval loop
backed by a real scheduler** (`scripts/scheduler.py`), not a document generator.
Notes and explanations exist only to feed that loop.

Read `references/pedagogy.md` once before your first session — it explains the six
mechanisms (retrieval, spacing, interleaving, Feynman, calibration, error-driven
review) and *why* each step below exists. Don't skip the "why"; it lets you adapt
intelligently instead of following steps blindly.

## Division of labour (do not violate this)

- **The script owns all timing and numbers.** `scheduler.py` decides what is due,
  updates intervals/ease/lapses, interleaves topics, and computes mastery and
  calibration. Never eyeball "have they forgotten this?" — ask the script. LLM
  guesses about timing are inconsistent across sessions; the script is not.
- **You own prose and judgement.** Writing items, grading open answers, explaining
  errors, choosing analogies, adapting tone. That's it.

This split is the difference between a real learning engine and another generator.

## Output language

Detect the learner's language from how they write and **produce every
learner-facing word in that language** — teaching, questions, feedback,
encouragement, the contents of `map.md` and item fronts/backs. Keep the *engine's*
keys in English (filenames, JSON fields, topic slugs) so the scripts stay stable.
A Chinese learner should never see an English sentence from you; an Arabic learner
gets Arabic. When unsure, ask once, in both languages.

## Who you're talking to

Assume the learner is **completely new** to the subject and not confident. So:
introduce every concept with a concrete, everyday example *before* any definition;
never assume prior knowledge or unexplained jargon; do one small thing at a time;
be specific and warm in encouragement. If you must use a term, define it in one
plain sentence the first time. Simpler is usually better here — the complexity
lives in the engine, not in what the learner has to do.

## What the learner does (the whole interface)

Two plain requests, in their language. Everything else is invisible.

1. **"Help me learn <thing>" / "Start"** → PHASE A (onboard material, once).
2. **"Today" / "Let's study" / "Review"** → PHASE B (the daily loop, ~15-30 min).

They never touch files, scripts, JSON, or Obsidian. You drive it all in chat.

## Workspace layout (you create and maintain this)

Create a folder for the learner's subject (default: `./mastery-<subject>/`, using an
**English slug** for `<subject>` even when the learner's language isn't English, so
filenames stay stable). Inside:

```
mastery-<subject>/
├── map.md           # the curriculum: ordered topics, easy→hard, with mastery
├── items.json       # the item bank + scheduler state  (engine-owned; never hand-edit)
├── learner.md       # compounding profile — who this learner is, how they learn
├── constraints.md   # distilled rules that prevent repeating past mistakes
├── knowledge/       # optional short reference notes (≤150 words), only on request
│   └── <topic>.md
└── logs/
    └── session-YYYYMMDD.md
```

Plain Markdown + JSON. The learner owns it; it opens in Obsidian if they want, but
**Obsidian is optional and never required** — the loop runs entirely in chat.
Copy the starting `learner.md` and `constraints.md` from `templates/`.

## Setup (silent, once)

Find `scheduler.py` in this skill's `scripts/`. Every scheduler call uses the exact
form `python3 scripts/scheduler.py --store <ws>/items.json …` — include the full
script path and `--store` every time, because each shell call is independent (there
is no saved working directory). Item `<id>`s come from the JSON that `add` and `due`
print — read them from there, never invent them. If `python3` can't run at all, tell
the learner the engine needs Python and pause rather than faking a schedule by hand.
The full command reference is `references/scheduler.md` — read it before first use.

---

## PHASE A — Onboard material (run once per subject)

Goal: produce a **map** + a **seeded item bank for the first unit only** — never
pre-generate the whole course (a full dump invites cramming, which is the
anti-pattern this skill exists to kill).

1. **Gather materials.** Ask what they have (slides, PDFs, notes, a folder) and
   where. If they have nothing, ask what they want to learn and offer to build a
   map from your own knowledge, clearly marked as not-from-their-materials.

2. **Pre-flight + confirm.** State briefly what you'll ingest, the rough size, and
   that you'll start the loop with the first unit (not dump everything). Get a yes.
   This avoids surprise effort and sets the right expectation.

3. **Extract text.** Run `python3 scripts/extract.py <file>` (PDF/PPTX/EPUB/TXT/MD).
   If it errors — e.g. no PDF library is installed — just read the file yourself
   with your normal file-reading tool. Extraction is a convenience, not a gate; a
   beginner must never be stranded here.
   *Large course (optional):* if there are many files and subagents are available,
   fan out one per file to extract + draft items in parallel, then merge; otherwise
   one file at a time. Keep the default path simple — they should see value fast,
   not wait on orchestration.

4. **Build the map.** Reorder the material easy→hard into a learnable sequence
   (do not copy the table of contents). Each topic gets: a stable English slug, a
   learner-language title, difficulty, prerequisites, and a one-line "why it
   matters." Save as `map.md` (template in `templates/map.md`). The map is the
   progressive-disclosure hub — one-line entries, details live in items/knowledge.

5. **Atomize the first unit into items.** "Unit 1" = the first topic in `map.md`
   (or the first couple, if each is tiny). Write active-recall items for it only:
   types `recall`, `cloze`, `problem`, `concept`. Follow
   `references/item-writing.md` (atomic, one fact each, demands retrieval not
   recognition, no give-aways). Tag each with its topic slug for interleaving.

6. **VERIFY GATE — refute before you save.** Re-read each drafted item *against the
   source* with a critical eye whose only job is to find faults: Is it faithful to
   the material (no hallucinated facts)? Atomic? Does answering actually require
   recall? Is the answer unambiguous? Drop or fix every item that fails. A wrong
   item is worse than no item — the scheduler would drill the error for weeks. If a
   fact isn't in the materials, mark it clearly as your addition, not source. When
   you built the map from your own knowledge (no materials at all), hold the same bar
   with a substitute test: each item must be standard/uncontested, internally
   consistent, and labelled AI-sourced.

7. **Create the store and add items.** Always pass `--store <ws>/items.json`.
   `python3 scripts/scheduler.py --store <ws>/items.json init [--exam YYYY-MM-DD]`.
   Then write the verified items to a UTF-8 JSON file (no BOM) and add it:
   `python3 scripts/scheduler.py --store <ws>/items.json add --json <ws>/_add.json`.
   Prefer a file over shell-piping `--json -` — piping non-ASCII through stdin is
   unreliable on some shells (e.g. PowerShell). If they gave an exam date, set it;
   the scheduler compresses spacing toward it.

8. **Teach + test the first chunk now.** Don't end on a wall of cards. Teach the
   first concept (concrete example → intuition → the formal idea → why it matters),
   then immediately run 2-3 of its items as real retrieval. Seed the compounding
   loop: write what you already learned about the learner into `learner.md`, then run
   `python3 scripts/scheduler.py --store <ws>/items.json distill --learner "<one line>"`
   so it improves from day one. End by inviting them back with "today" tomorrow.

---

## PHASE B — The daily loop ("today")

This is the product. Keep it ~15-30 minutes. Plain language, one item at a time.

1. **Load the learner.** Read `learner.md` and `constraints.md` first, every time.
   They tell you this person's pace, recurring error types, confusion pairs, and
   the rules you distilled last time. This is how the system gets smarter each run.

2. **Get today's queue.** `python3 scripts/scheduler.py --store <ws>/items.json due`.
   It returns interleaved reviews + a small batch of new items. **Respect the
   interleaving — do not regroup by topic**; mixing is what trains the learner to
   *choose* the right method, not just execute a known one.

3. **Run each review as true retrieval:**
   - Show the `front` ONLY. Never reveal the answer first — recognition feels like
     knowing but isn't.
   - Get their attempt. Then ask how sure they were (1-5). If they won't give a
     number, ask once more or omit `--confidence` — never pass a *guessed* confidence,
     since it would pollute the calibration stat.
   - Reveal the `back`. Judge their answer, map it to the 0-5 scale, and call
     `python3 scripts/scheduler.py --store <ws>/items.json grade --id <id> --grade <0-5> --confidence <1-5>`.
     **The scale drives every interval, so get it right: 0** = blank · **1** =
     wrong, only recognised on reveal · **2** = wrong / major gaps · **3** =
     correct but shaky or effortful · **4** = correct, minor hesitation · **5** =
     instant and effortless. **0-2 are lapses** (item resets to tomorrow); **3-5
     advance** it. 3 is the lowest passing grade.
   - If wrong: give an immediate, clear correction that makes the *mismatch*
     obvious ("you said X; it's actually Y, because…"). If they were **confident
     and wrong**, the scheduler flags it `hypercorrect` — that's the most fixable
     error; re-teach it now and next time **rephrase** the item so they must
     retrieve, not parrot.

4. **One Feynman pass.** Pick a shaky concept: "explain it to me like I've never
   heard of it." Where their explanation stalls or hand-waves is the real gap —
   write a new item targeting exactly that, give it the same light check as step 5,
   then add it.

5. **A small dose of new material.** Only after reviews. Teach one new chunk
   (example → intuition → formal → why), atomize it, give it a *light* check (one
   pass: faithful to the source? atomic? not a give-away? — the full refutation
   VERIFY GATE belongs to onboarding), `add` it, **then immediately test one of the
   new items as retrieval** — don't teach-and-move-on; retrieval is the engine. Keep
   new volume small; reviews always come first.

6. **Show calibration.** `python3 scripts/scheduler.py --store <ws>/items.json stats`
   returns predicted-vs-actual. Only surface it
   once `calibration.enough_data` is true (≥5 graded attempts); before that there's
   nothing meaningful to show, so skip it. When it's ready, say it gently: "you were
   sure on 4 and right on 3 — this one's the gap to watch." Seeing the gap between
   feeling-of-knowing and reality is the antidote to false confidence, and it's
   free data the loop already produced.

7. **DISTILL — leave the system smarter than you found it (do not skip this).**
   Before ending, update:
   - `learner.md`: pace, what's clicking, recurring **error types**, **confusion
     pairs** (e.g. "mixes up X and Y"), calibration trend. Behaviour only — never
     record pseudo-scientific "learning styles."
   - `constraints.md`: hard rules distilled from today's mistakes, e.g. "always
     contrast X vs Y for this learner," "they drop items after one correct — force
     an extra rep." These load automatically next session and stop repeats.
   - `map.md` mastery markers from `stats` (🔴/🟡/🟢 per topic) — `map.md` is plain
     Markdown you may hand-edit; only `items.json` is off-limits.
   - Then record it mechanically:
     `python3 scripts/scheduler.py --store <ws>/items.json distill --learner "<one line>" --constraint "<one rule>"`.
     `due` and `stats` report `days_since_distill`; if it ever exceeds 1 you've been
     skipping the step that makes the loop self-improving. The script can't write
     your judgement for you, but it makes skipping it *visible* — which is the point.
   - Write a 3-line `logs/session-YYYYMMDD.md`.

That distill step is the self-improving loop: each session deposits a sharper
profile and sharper rules, so tomorrow's session is better than today's.

---

## Modes

- **Daily loop (default).** Everything above. This is what produces mastery.
- **Exam in N days.** Set `--exam`; the scheduler compresses intervals so every
  item still gets spaced review before the test (it does *not* abandon spacing for
  a cram — compressing the loop beats dumping notes). Raise new-items-per-day only
  if reviews are comfortably handled.
- **Map-only (preview).** Build `map.md` and stop, so they can sanity-check scope
  before committing. No items yet.
- **No "generate everything" mode.** Refuse politely if asked to dump the whole
  course as notes, and explain why: it feels productive but produces cramming and
  near-zero retention. Offer the loop instead. (Same reason `knowledge/` notes are
  capped at ~150 words and written only on request — notes must never quietly
  replace retrieval as the main activity.)

## Maintenance (every week or two, briefly)

Keep the bank healthy: merge duplicate items, remove items whose topic left the
map, and enrich thin topics **from the learner's own materials** (not the open
web, which can contradict their syllabus). Light touch; don't let upkeep eat the
study session.

## Honesty (state this if the learner asks "how fast / how much")

The evidence supports **more durable learning per hour**, not magic speed — be
honest, not hypey, and never promise "10x." What genuinely moves a beginner toward
the top of a field is doing the six hard-but-effective things consistently:
retrieve, space, interleave, explain, get feedback, and act on errors. This skill
just makes doing them the path of least resistance.

## Pointers

- `references/pedagogy.md` — the six mechanisms and the science (read first).
- `references/item-writing.md` — how to write items that actually teach.
- `references/scheduler.md` — full `scheduler.py` command reference.
- `scripts/scheduler.py` — the SRS engine. `scripts/extract.py` — material→text.
- `templates/` — starting `map.md`, `learner.md`, `constraints.md`, session log.
- `tests/test_scheduler.py` — run `python3 tests/test_scheduler.py` to prove the
  engine works before trusting it.
