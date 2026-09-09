---
name: start-learning
description: >
  One-time onboarding for the CORE / PM curriculum (43 lessons, 7 phases of
  product judgment). Interviews the learner about the decisions they actually
  own, runs the judgment placement, and writes PM-LEARNING.md — the persistent
  plan the learn skill drives. Trigger phrases: "start the course", "start
  learning", "onboard me", "begin CORE PM", "set up my learning plan".
license: MIT
metadata:
  version: 1.0.0
  tags: [onboarding, curriculum, product-management, learning-plan]
---

# Start Learning — CORE / PM

You are onboarding a practicing product manager into **CORE / PM**: 43 lessons
across 7 phases that rebuild the judgment underneath product management.

Your job in this skill is to produce `PM-LEARNING.md` in the learner's course
home — a directory that will still exist next week. It records why they are
here, which real decision they will practice on, where they should start, and
what their route looks like. Every later `learn` session reads and updates that
file, so treat it as the learner's source of truth.

Establish that directory before you ask anything else. See Step 0.

Works with any agent. If your environment has a structured question/option tool,
use it for every question. Otherwise present lettered options as plain text and
wait for the reply.

## Host invocation contract

Skill names are portable. Invocation syntax belongs to the host. Before you show
a next command, use the correct form:

- Claude Code: `/start-learning`, `/learn`, `/review-artifact`.
- Codex: `start-learning`, `learn`, `review-artifact`, or tell the learner to
  pick the skill from `/skills`.
- Any other compatible host: natural language, such as
  `Use learn to teach my first lesson.`

Never present a slash command as universal syntax. When the host is unknown, use
the natural-language form.

## This course has a second subject: their own product

Most courses have one input — the lessons. This one has two. Every lesson asks
the learner to repeat a reasoning move on a live decision from their own
product. Onboarding must capture that live decision, or the transfer step
collapses into a hypothetical and the course loses most of its value.

If they cannot name a real decision yet, that is acceptable. Record
`Working decision: not yet chosen` and have `learn` ask again at the end of
PF-01. Do not stall onboarding over it.

## Resume routing

If `PM-LEARNING.md` already exists, do not overwrite it. Summarize what it says
(mission, working decision, entry point, progress so far) and offer exactly
three options:

- **Resume** — invoke `learn` with the host syntax above. Skip the interview and
  the placement entirely.
- **Re-run placement** — administer the placement again, then update only the
  Placement section and the Route statuses. Leave Mission, Working decision,
  Progress log, Artifacts, and Review queue untouched.
- **Start over** — only after explicit confirmation, rename the existing file to
  `PM-LEARNING-<YYYY-MM-DD>.md` as an archive, then run full onboarding. Never
  delete or silently overwrite their history.

## Step 0 — Establish the course home

This course writes to disk. `PM-LEARNING.md` and an `artifacts/` directory are
the learner's accumulating record, and they are worthless if they live somewhere
that gets wiped. Many agent sessions start in a temporary scratch workspace, so
check before you write.

Look at the working directory. Treat it as **ephemeral** if any of these hold:

- The path sits under `/tmp`, `/private/tmp`, `/var/folders`, or any directory
  named `scratchpad`, `scratch`, or `session`.
- The path contains a session identifier — a long hex or UUID-like segment.
- It is an empty directory with no project of the learner's own in it.

If the directory is ephemeral, say so plainly in one sentence — their progress
would not survive the session — and ask where the course should live. Offer:

- **Their own product repo** — the best answer. This course asks them to
  practice on a live decision from their product, so the record belongs next to
  that product.
- **A dedicated directory**, such as `~/core-pm`.

Wait for a real path. Create it if it does not exist, change into it, and
confirm the absolute path back to them before continuing. Record it as
`Course home` in `PM-LEARNING.md` so `learn` can find its way back from any
directory.

Do not write the plan into a clone of the CORE / PM repository itself. That repo
is the course source, not learner state. If the working directory contains a
`lessons/manifest.json` and a `skills/` directory, it is the course repo — read
lesson content from it, but put `PM-LEARNING.md` and `artifacts/` somewhere that
belongs to the learner.

If the directory is durable, skip all of this. Do not interrogate someone who
is already in a sensible place.

## Step 1 — The interview (4 questions, keep it short)

1. **What decision are you currently getting wrong, or avoiding?** Free text.
   This is the anchor for the whole course. Offer examples if they stall: a
   roadmap trade-off you keep re-litigating, a metric nobody trusts, a rewrite
   you cannot justify, a strategy nobody can act on.
2. **What is your scope today?** Options: single feature area, whole product,
   multiple products, leading other PMs. This sets which phases matter most and
   whether the Product Leadership phase is relevant now or later.
3. **How much time per week?** Options: ~1 h, ~3 h, ~5 h, "as fast as possible".
   Used only to phrase pace honestly, never to cut content.
4. **Do you want to practice on your own product, on the shared Noted case, or
   both?** Default and recommendation is **both**: Noted for comparison, their
   product for consequence. Record the answer.

Do not ask more than these four. The placement measures judgment; the interview
captures intent and the working decision.

## Step 2 — Placement

Run the placement from the `find-your-level` skill, which installs alongside
this one: 14 scenarios, two per phase, scored on reasoning rather than recall.

Preserve that skill's answer-isolation contract. Do not preload the answer key,
do not reveal which option is strongest before the learner answers, and do not
replace neutral `<letter>` placeholders with real option letters.

If the learner says they already know where to start ("just start me at
Evidence"), respect that and skip the placement, with the same output contract
so that `learn` always finds a well-formed plan:

- Validate the phase against the seven phase IDs (PF, PJ, EV, ST, TJ, DS, LD)
  and resolve its canonical name. If it does not resolve, list the seven phases
  and ask them to pick.
- In the Route table, phases before the entry point are `Skip`, the entry point
  and everything after are `Do`. There are no `Review` rows, because there are
  no scenario scores to infer them from.
- In the Placement section, write `Score: self-selected` instead of a number.

Never place someone out of Phase 01. PF-01 through PF-06 are the shared
vocabulary that every later phase depends on. A strong placement result changes
PF from `Do` to `Review` — it never becomes `Skip`.

## Step 3 — Choose the route

Four routes exist. Recommend one based on the scope answer from question 2, then
let the learner override:

| Route | Lessons | Hours | Recommend when |
|---|---:|---:|---|
| Complete foundation | 43 | ~22 | They want the whole rebuild, or scope is "whole product" |
| Decision field path | 12 | ~6 | They want one consequential decision end to end, or time is ~1 h/week |
| Technical + AI judgment | 13 | ~7 | Scope involves engineering or AI systems closely |
| Product leadership | 15 | ~8 | Scope is "leading other PMs" |

The lesson standard is identical on every route. A route changes order and
depth, never the bar.

## Step 4 — Write PM-LEARNING.md

Create `PM-LEARNING.md` in the course home from Step 0 with exactly these
sections:

```markdown
# My CORE / PM Path
<!-- Managed by the CORE / PM learning skills.
     Repo: https://github.com/raziiabraham/core-pm -->

## Course home
<absolute path to the directory holding this file, from Step 0>

## Mission
<their answer to question 1, in their own words>

## Working decision
<the live product decision they will carry through the course, or
 "not yet chosen">
- Product: <name>
- Practice on: <own product | Noted | both>

## Placement
- Date: <YYYY-MM-DD>
- Route: <route name>
- Score: <total>/14 with the per-phase breakdown, or exactly `self-selected`
- Entry point: <PHASE-ID> — <phase name>
- Pace: ~<hours>/week

## Route
| Phase | Name | Status | Lessons | Est. hours |
|-------|------|--------|---------|------------|
<all seven phases. Status is Skip, Review, Do, or Done. Lessons and hours
 come from lessons/manifest.json — read it locally if the repo is cloned,
 otherwise fetch
 https://raw.githubusercontent.com/raziiabraham/core-pm/main/lessons/manifest.json>

## Progress log
| Date | Lesson | Check | Note |
|------|--------|-------|------|

## Artifacts
| Lesson | Artifact | Where it lives | Reviewed |
|--------|----------|----------------|----------|

## Review queue
<empty for now; learn adds lessons whose checks exposed weak reasoning>
```

The Artifacts table is what makes this course cumulative. Every lesson produces
one decision object, and together they become the learner's Product Decision
Case. Never drop this section.

## Step 5 — Hand off

Close with three lines, nothing more:

- Their entry point, their route, and the total estimated hours for the
  `Review` and `Do` phases.
- The host-correct invocation for `learn`, and that it teaches the next lesson
  and picks up from this file every time.
- The host-correct invocation for `course-guide <topic>`, and that it can jump
  straight to a topic instead.
