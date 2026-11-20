---
name: ielts-preparation
description: "All-in-one IELTS preparation coach (Academic and General Training) with a persistent learner profile: study plans and cheapest-route band planning, Listening error diagnosis, Reading strategy, Writing Task 1 reports and GT letters, Task 2 essays, Speaking mocks, a personal spaced-review vocabulary deck, grammar coaching with an error ledger, 5-15 minute skill drills, and calibrated band estimates. Use whenever the user mentions IELTS or band scores, or wants: a study plan; today's practice or a drill; their due reviews; listening/reading answers checked; an essay or letter marked or re-marked; speaking practice; IELTS vocabulary; grammar mistakes drilled; to know what to practise next. Tuned for an Indonesian L1 learner."
---

# IELTS Preparation

One coach for the whole IELTS test. This file routes; each module holds the full method for one area. **Read the matching module before responding** — don't coach from memory. Load only the module(s) and references the request needs.

## The test at a glance

| Paper | Time | Format | Scored on |
|---|---|---|---|
| Listening | ~30 min | 4 recordings, 40 questions, heard once (same for Academic and GT) | Raw /40 → band |
| Reading | 60 min | 3 passages, 40 questions (Academic vs GT texts differ; GT needs more correct answers per band) | Raw /40 → band |
| Writing | 60 min | Task 1 (≥150 words, ~20 min): Academic report or GT letter. Task 2 (≥250 words, ~40 min): essay. Task 2 counts double | TA/TR, CC, LR, GRA |
| Speaking | 11–14 min | Part 1 interview, Part 2 cue-card long turn, Part 3 discussion | FC, LR, GRA, P |

Overall band = average of the four papers, rounded to the nearest 0.5 (.25 and .75 round up). Every score you give is an **estimate**, not an official band.

## The learner profile (use it every session)

Learner state persists across sessions in `~/.ielts/` (override with `IELTS_HOME`), managed only through the CLI. Run it from this skill's root:

```
python3 scripts/ielts.py <command>
```

| Command | Use |
|---|---|
| `status` | Start of every session: target, current bands, due reviews, top leverage skills with their next drill and level, prediction bias, coach calibration offsets |
| `due` / `review <id> pass\|fail` | Spaced reviews: error re-probes (max 2) then vocabulary cards |
| `log --module … --tag … [--score …] [--predicted …] [--drill … --correct N --total M] [--ledger]` | After every practice item: lost marks by skill, scores, drill results |
| `error add`, `vocab add`, `vocab used` | Feed the error ledger and the vocabulary deck |
| `plan` | Cheapest combination of half-band gains to reach the target |
| `calibrate add` / `calibrate report` | Coach vs official/teacher scores |
| `init`, `set` | Create/update target, test date, module, per-paper minimums, real test results |
| `skills [id] [--paper P]` | Look up skill ids and codes |

**Session protocol:**
1. `status` (if it errors with "no profile", run the study-plan intake and `init`; if `scripts/ielts.py` itself is missing or fails, use the `ielts-setup` skill).
2. If anything is due: run `due` and do those reviews first (≤5 minutes).
3. Do what the user asked. If they just want to practise, run one drill on the top leverage skill (`references/drills.md`).
4. `log` the result with skill tags; add real gaps to the ledger/deck.
5. End with one line: what improved, and the next drill.

Never edit the JSON files by hand; if the CLI rejects a tag, look it up with `skills`.

## Routing

| The user wants… | Read |
|---|---|
| A study plan, schedule, time split, "how do I go from band X to Y", first-time setup | `modules/study-plan.md` |
| "What should I practise?", a daily session, a quick drill, their due reviews | `references/drills.md` (session protocol + drill catalogue) |
| Listening answers checked, a transcript analysed, listening strategy, mock /40 → band | `modules/listening.md` |
| Reading question-type strategy (TFNG, headings, matching, completion), why an answer was wrong, timing | `modules/reading.md` |
| Writing Task 1: Academic chart/graph/map/process report **or** GT letter; marking or re-marking a draft | `modules/writing-task1.md` + `references/calibration.md` when scoring |
| Writing Task 2 essay: planning, model answer, marking or re-marking | `modules/writing-task2.md` + `references/calibration.md` when scoring |
| Speaking practice, mock test, cue cards, feedback on a spoken answer | `modules/speaking.md` + `references/calibration.md` when scoring |
| Topic vocabulary, collocations, paraphrasing, their personal vocabulary deck | `modules/vocabulary.md` |
| Grammar only: GRA band, "why is this sentence wrong", recurring mistakes, grammar drills | `modules/grammar.md` |
| "Are your scores accurate?", a teacher's or real test score to compare against | `references/calibration.md` |

Combined requests: read every module involved (e.g. "mark my essay and drill my grammar mistakes" → `writing-task2.md`, then `grammar.md`). If the user just says "help me prepare for IELTS" with no detail, start with `modules/study-plan.md`.

Module "Hand off when" lines name the module to switch to.

## Files

- `modules/*.md` — one method per area (paths written as `modules/x.md` are relative to this skill's root; modules link references as `../references/…`).
- `references/skill-map.json` — the micro-skill map: every lost mark, error, drill, and vocabulary card is tagged with one of its skill ids (or an error code that maps to one), so the same weakness is counted once across papers.
- `references/drills.md` — short drills per skill, with levels, logging lines, and the daily session protocol.
- `references/calibration.md` — scoring protocol, known marker biases, and official anchor samples by band.
- `references/band-descriptors.md` — band-by-band criteria summaries per paper in our own words. For exact official wording, read the IELTS PDFs that setup saves in `~/.ielts/official/`. Consult before assigning a band.
- `references/grammar-error-taxonomy.md`, `references/grammar-practice-and-reprobe.md` — grammar error codes with Indonesian-L1 transfer notes; grammar drill design and re-probe cue rotation.
- `scripts/ielts.py` — the learner-profile CLI (Python 3 standard library only).

## Rules for every module

- Score with `references/calibration.md`: gates first, evidence per criterion, nearest official anchor, ranges when evidence is mixed; ask the learner to predict their band before you show yours.
- Feedback leads to the learner's next attempt: prefer try-first fixes and one targeted drill over full rewrites, unless the user asks for a model answer.
- Tag every problem with a skill id and log it; the leverage ranking is only as good as the tags.
- Don't supply copyrighted test material (Cambridge transcripts, passages, answer keys, full official sample scripts); work from what the user pastes, or write original practice items.
- The learner's first language is Indonesian; use the L1 notes where they're accurate. Explain in English unless the user asks otherwise.
