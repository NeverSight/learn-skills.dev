---
name: make-it-clear
description: |
  Turn vague asks into confirmed intent and approved designs before any plan,
  spec, or code. One skill combining interrogate, interview, discovery, grill,
  brainstorm, multi-agent review, and questionnaire. Auto-selects the mode from
  conversation context and the user's question — not only trigger phrases.

  Trigger when the ask is underspecified ("build me X"); a plan or design is
  pasted without challenge; a next skill is named but gaps remain; the user
  says "interrogate me", "brief me", "interview me", "grill me", "brainstorm",
  "discovery", "questionnaire", or "make it clear"; when tempted to fill silent
  assumptions; before greenfield features; or when a design needs peer challenge.

  Keywords: make-it-clear, interrogate, context brief, interview, grill,
  discovery, brainstorm, intent, hypothesis, questionnaire, design review,
  gap catalog, mode detect, YAGNI, hard gate, out of scope
version: 1.2.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: cursor-ask-question, optional-task-subagents, optional-visual-companion
  related_skills: team-orch, brainstorming, interview-me, discovery-interview
  primary_output: confirmed-intent | context-brief | approved-design | questionnaire | disposition
  sources_synthesized: interrogate-me, interview-me, discovery-interview, grill-me, brainstorming, multi-agent-brainstorming, to-questionnaire
---

# Make It Clear

Close the gap between what people *ask for* and what they *actually want*
before switching costs exist. **Seven protocols, one skill** — detect the mode
from this conversation and question; don’t wait to be told “grill me.”
**Non-negotiables override speed theater.**

**Announce when activating:**
`Using the make-it-clear skill — mode: <mode> (<one-line why>).`

## When to load which reference

| Need | Read |
|------|------|
| Hard bans / gates | [non-negotiable.md](references/non-negotiable.md) |
| Detect mode from context / question | [context-detect.md](references/context-detect.md) |
| Pick a mode (details) | [modes.md](references/modes.md) |
| Interrogate / Context Brief first | [interrogate-protocol.md](references/interrogate-protocol.md) |
| Gap catalog (marketing + eng) | [gap-catalog.md](references/gap-catalog.md) |
| Interview / intent extraction | [interview-protocol.md](references/interview-protocol.md) |
| Discovery deep-dive categories | [discovery-categories.md](references/discovery-categories.md) |
| Grill an existing plan/design | [grill-protocol.md](references/grill-protocol.md) |
| Design brainstorm → approve | [brainstorm-protocol.md](references/brainstorm-protocol.md) |
| Multi-agent design review | [multi-agent-review.md](references/multi-agent-review.md) |
| Async questionnaire for someone else | [questionnaire.md](references/questionnaire.md) |
| Artifact shapes & paths | [artifacts.md](references/artifacts.md) |
| Types / layouts (“tables & columns”) | [types-and-layouts.md](references/types-and-layouts.md) |
| Pitfalls & rationalizations | [gotchas.md](references/gotchas.md) |
| DO / DON'T | [do-dont.md](references/do-dont.md) |
| Recipes | [examples.md](references/examples.md) |
| Review checklist | [review-checklist.md](references/review-checklist.md) |

---

## Core rules

1. **Clarity before creation** — no plan, spec, scaffold, or code until intent is confirmed (and design approved when inventing behavior).
2. **Scan before ask** — never ask what conversation, CLAUDE.md, or project brief already answered; tailor gaps to the next skill/output.
3. **One question at a time** — never batch 3+ questions; next question may depend on the last answer.
4. **Hypothesis + confidence** — every interview/interrogate turn states a one-line read and an honest 0–100% confidence; below ~70% add *why*.
5. **Guess attached** — each question includes `GUESS:` / “My hypothesis: … Confirm, correct, or expand.”
6. **Want ≠ should-want** — probe sophistication / convention answers; ask what they’d want if they didn’t have to justify it.
7. **Out of scope is mandatory** — half of misalignment is silent disagreement about non-goals.
8. **Explicit yes only** — “sounds good”, “whatever you think”, silence ≠ confirmation.
9. **Stop budget** — usual 3–6 questions; >8 almost always too many; also stop at 95% predict-3.
10. **2–3 approaches before settle** — recommend one; YAGNI ruthlessly.
11. **Mode from context** — auto-select among the seven fused protocols; don’t wait for a mode name ([context-detect.md](references/context-detect.md)). Chain only when the exit feeds the next.

---

## Non-negotiable

Full contract: [non-negotiable.md](references/non-negotiable.md).

| Rule | Requirement |
|------|-------------|
| Hard gate | No implementation skill / code / scaffold until design approved (when design work applies) |
| Interactive only | Never run in CI, `/loop`, or autonomous non-interactive contexts — flag underspec as blocker |
| Context scan | Interrogate/interview: do not re-ask known facts; skill-aware gaps |
| One Q / turn | Single focused question (or one AskUserQuestion); guess attached in interview/interrogate/grill |
| Q budget | Prefer 3–6; treat >8 as a smell unless discovery floors apply |
| Confirm gate | Restate (Outcome / User / Why now / Success / Constraint / Out of scope) or Context Brief + explicit yes |
| No hollow yes | Reject “whatever you think” / “sounds good” — offer two concrete choices |
| Completeness before spec | Discovery checklist green; no TBD left that blocks implementation |
| Decision log | Multi-agent review invalid without Decision Log |
| Creativity vs critique | One designer; reviewers may not invent features / redesign outside mandate |
| Questionnaire send | Grill *who* and *what you need back* — not the subject domain the recipient owns |
| Save only on confirm | Intent/spec/questionnaire files only after user confirms (or questionnaire write step) |

---

## Gotchas

Summary — [gotchas.md](references/gotchas.md).

- Waiting for “grill me” / “interview me” instead of reading the thread.
- Building the conventional ask (“dashboard”) instead of the real need (“a list”).
- Asking what CLAUDE.md / prior turns already answered.
- Batch questions → skim answers and wrong framing locked in.
- Polite agreement with your guess (sycophancy) mistaken for truth.
- Spec after 3–5 shallow questions = slop.
- Endless interview when foundation is missing — step back, don’t grind.
- >8 interrogate questions when 3–6 would unlock work.
- Multi-agent “swarm brainstorm” without role firewalls → chaos.
- Designer self-approves; objections ignored.
- Questionnaire that interviews the user about the *subject* instead of the *send*.
- Visual companion offered upfront or used for pure text decisions.
- Saving intent/spec before explicit confirmation.

---

## Types (“Data Types”)

| Kind | Values / shape |
|------|----------------|
| Mode | `interrogate` · `interview` · `discovery` · `grill` · `brainstorm` · `multi_agent_review` · `questionnaire` |
| Confidence | `0–100%` integer; reason required if `< ~70%` |
| Question form | `open` · `mcq` · `multi_select` · `confirm_restate` · `research_gate` · `conflict_gate` |
| User type | `technical` · `non_technical` · `hurried` |
| Project type | `backend` · `frontend` · `fullstack` · `cli` · `mobile` · `script` · `library` · `other` |
| Disposition | `APPROVED` · `REVISE` · `REJECT` (multi-agent / grill exit) |
| Artifact kind | `intent` · `context_brief` · `design_spec` · `decision_log` · `questionnaire` · `research_note` |
| Priority | `P0` · `P1` · `P2` (requirements after discovery) |

Details: [types-and-layouts.md](references/types-and-layouts.md).

---

## Layouts (“Tables / Columns”)

### Intent restate columns

| Column | Content |
|--------|---------|
| Outcome | One line — what success produces |
| User | Who benefits |
| Why now | What changed |
| Success | How we know it worked |
| Constraint | Binding limit |
| Out of scope | Explicit non-goals |

### Decision log columns

| Column | Content |
|--------|---------|
| Decision | What was chosen |
| Alternatives | What was considered |
| Objections | Who raised what |
| Resolution | Accept / reject + rationale |

### Context Brief columns (interrogate)

| Column | Content |
|--------|---------|
| What we're doing | Task or output |
| For | Specific who |
| Problem or goal | Specific |
| Differentiator / angle | What makes it sharp |
| Voice / tone | Sound like / never sound like |
| Success | Concrete win |
| Avoid | Constraints, prior attempts, red lines |

### Mode routing (short — detect, don’t wait)

| Signal in thread or question | Mode |
|------------------------------|------|
| Next skill named / “brief me” / “what do you need” | `interrogate` |
| “Build me X” / convention mush / missing who-why-success | `interview` |
| Vague product → they want a spec | `discovery` |
| Plan / PRD / ADR / design already in thread | `grill` |
| Inventing behavior; need options | `brainstorm` |
| High-stakes + design exists | `multi_agent_review` |
| Facts live with someone not in this chat | `questionnaire` |
| Typo / rename / already-clear XS | **skip** |

Full detector + ties: [context-detect.md](references/context-detect.md).

Full layouts & paths: [types-and-layouts.md](references/types-and-layouts.md), [artifacts.md](references/artifacts.md).

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Scan known context first; pick mode from the thread | Re-ask CLAUDE.md; wait for a mode name |
| State hypothesis + confidence first | Dive into libraries/layouts on a fuzzy ask |
| One question + guess (3–6 typical) | Survey dumps; leading “best practice?” frames; >8 without need |
| Probe want vs should-want | Accept “scalable / modern / clean” as goals |
| Context Brief or restate + explicit yes | Treat “sounds good” as lock |
| 2–3 approaches + recommend | Single path presented as inevitable |
| Research loops when uncertain | Guess tech tradeoffs silently |
| Bound multi-agent roles & exit | Parallel idea swarm; self-approve |
| Questionnaire for *send* gap | Make user answer what recipient knows |

Complete: [do-dont.md](references/do-dont.md).

---

## Examples

See [examples.md](references/examples.md):

1. Interrogate: brief me → Context Brief → start work
2. Interview: “dashboard” → personal experiment list
3. Discovery: recipe app through categories + research
4. Grill: API plan stress-test to REVISE
5. Brainstorm: feature design → approved spec path
6. Multi-agent review: Skeptic → Guardian → Advocate → Arbiter
7. Questionnaire: async stakeholder discovery doc
8. Detect from context (pasted plan → grill; “build X” → interview)
9. Mode chain: interrogate → interview → brainstorm → handoff

---

## Critical / Recommended / Nits

Full: [review-checklist.md](references/review-checklist.md).

### Critical
Hard gate skipped; batch questions; re-ask known context; no hypothesis/confidence; hollow yes accepted; out-of-scope omitted; implementation before confirm; multi-agent without Decision Log / role firewall; questionnaire wrong target; non-interactive invocation.

### Recommended
Mode chosen from context (not only phrases); context scan + gap-first; 3–6 Q budget (interrogate); discovery completeness before spec; research when buzzwords; 2–3 approaches; user-type adaptation; intent/brief persisted only on confirm; disposition reported when orchestrated.

### Nits
Confidence reason missing below 70%; MCQ options lack “I’m not sure / Research”; visual companion timing; artifact path naming; Context Brief fields forced when irrelevant.

---

## Decision workflow

1. **Mechanical / unambiguous?** → skip this skill.
2. **Detect mode** from conversation + this question ([context-detect.md](references/context-detect.md)) — announce mode + why.
3. **Scan context** → run that protocol; keep **one Q at a time**.
4. **Context Brief or restate + explicit yes** (intent lock).
5. If inventing behavior → **brainstorm** design sections → approve → write artifact.
6. If high-stakes → **multi_agent_review** until Arbiter disposition.
7. If knowledge lives elsewhere → **questionnaire** file; stop.
8. Handoff downstream (plan / implement) **only** after gates pass; persist artifacts per [artifacts.md](references/artifacts.md).
9. **Re-detect** if the thread changes (plan appears, stakes rise, owner isn’t here).
