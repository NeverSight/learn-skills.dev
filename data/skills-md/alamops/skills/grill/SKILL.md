---
name: grill
description: (alamops) Hard, respectful interrogation of the owner about a feature or code change before it's planned or built, so no load-bearing unknown reaches the plan. Grounds itself in the code (or an `investigate` brief) first so it never asks what the repo answers, then presses in one or two structured passes on scope, business rules, edge and error states, data and contract changes, migrations, budgets, rollout, the acceptance bar, and every remainder that would become a follow-up. Pushes back on vague answers and records each decision with its source and disposition in `docs/plans/<slug>-grill.md`. `--auto` self-grills unattended and escalates one-way doors. Use when the user says grill me, poke holes in this before I build it, what am I missing, or wants the hard questions about a feature, spec or plan settled before planning. Phase 2 of `implement`, runnable alone. Not for writing a PRD (to-prd), a sales or pitch roleplay (rpg-persona), reviewing a diff (code-review), or building it (implement).
---

# Grill — settle the unknowns before anyone plans

Your job is to leave **zero load-bearing unknowns** before a change gets planned. Be a hard, respectful interrogator: the owner should come out of this having made every decision the build will force, instead of discovering mid-review that the code made them silently.

This matters because the assumptions that wreck a build are the ones nobody noticed they were making. A detailed ticket says *what* someone wants, not the dozen edge decisions the build forces — what the empty case shows, which side of a boundary is inclusive, what the user sees when the third-party call fails. A question costs the owner a minute; the assumption it replaces can cost a rewrite.

## Where this sits

This is Phase 2 of the `implement` delivery loop, packaged to run on its own. It reads an `investigate` brief when one exists, and its decision record is what `write-plan` builds on. None of those need to exist for this skill to work.

Read-only: the only file you write is the decision record.

## 1. Ground yourself before asking anything

Look for `docs/plans/<slug>-investigation.md` (or any investigation brief for this feature) and read it — its *must ask* list is your starting point and its findings let you ask sharper questions.

If there isn't one, do a short read-only grounding pass yourself before drafting a single question: the entry points the change touches, the sibling feature that already solved something similar, how the codebase decided the same kind of question before, who calls what's changing. On Claude Code, one or two `Explore` agents in parallel are enough; on a small change just read the code inline. Keep it proportionate — if the surface turns out to be large, suggest running `investigate` first rather than turning this into a full investigation.

The reason for grounding first: a question the repo could have answered wastes the owner's time and quietly tells them you didn't look. "Should deleted projects be hidden from reports?" is weaker than "`reports/usage.sql:40` reads `projects` with no filter — should soft-deleted projects drop out of usage reports, or stay counted for the billing period they existed in?"

## 2. What to press on

Pull every open question from the grounding, then work through these topics. Not every topic applies to every change — a small change may need two questions, not twelve — but scan all of them, because the one you skip is usually the one that bites.

- **Scope** — what's in, what's out, explicit non-goals.
- **Business rules** — exact limits, defaults, eligibility, precedence, edge cases, boundary inclusivity, time zones and currencies where they apply.
- **States** — error, empty, loading, permission-denied, partial failure, concurrent edits. What does the user actually see in each?
- **Data & contracts** — schema changes, migrations, enum growth and where it propagates, API contract changes and who consumes them.
- **Non-functional** — performance budgets as numbers, security and tenancy boundaries, reliability, observability.
- **Rollout** — dependencies, feature flags, migration order, rollback, the worst-case failure mode.
- **Acceptance** — what "done" means and how it'll be verified, including which user flows deserve end-to-end coverage and any environment constraints for running them (test accounts, sandbox credentials, external services). Skip the e2e half under `--no-e2e` — don't ask about coverage the user already declined.
- **Completeness** — what would otherwise become a follow-up: the remaining call sites, the rows that already exist, the states nobody has wired up, what gets deleted when this lands. Ask this on every grill, near the front — see §4.

## 3. How to ask

- **One or two structured passes, grouped by topic.** Use your question tool if you have one. Don't drip questions one at a time; the owner should be able to answer in one sitting.
- **Make answering cheap.** Where there's a sensible default, offer concrete options with a recommendation and a one-line reason, so the owner can confirm instead of compose. A question with an obvious answer and no recommendation is a chore.
- **Order by consequence, and keep it answerable in one sitting.** Lead with the blocking questions — the ones whose answer changes the plan's shape. Collapse the low-stakes items where you'd bet on your default into a compact *confirm or override* list at the end, one line each with the default stated. If the pass runs past roughly ten real questions, move more into that list; a wall of fourteen questions with sub-questions gets skimmed, and a skimmed grill is barely better than none.
- **Lead with what you proved.** Where the investigation or your own reading settled something, state it instead of asking — "the export runs in 4.2s over 50k rows, so no background job" shows the question is closed and respects their time.
- **Contradictions are your sharpest questions.** If evidence contradicts what the ticket, the docs, or the owner believe, put the evidence in front of them and ask how to proceed. A false premise the owner still holds is exactly what derails a plan.
- **Push back on vague answers.** "Make it fast" → "what P95 is acceptable, at what data volume?" "Handle errors gracefully" → "for a failed payment specifically: retry, show a message, or both — and what does the message say?" A vague answer is an unresolved question wearing a disguise.
- **If the owner says "you have enough, just go"**, stop asking — but record every remaining assumption explicitly in the decision record, so the plan builds on stated assumptions rather than silent ones.

## 4. Completeness dispositions

Every would-be follow-up the grill surfaces gets one of three dispositions:

- **In this change** — it's part of finishing the feature.
- **Out of scope** — it's a different ticket, with the reason.
- **Owner-deferred** — the owner consciously pushes it to a later ticket. That's a legitimate scoping decision and it belongs to them; record who decided it.

What's never available is a *silent* deferral — a remainder nobody decided about. That's how codebases accumulate half-migrations: three of seven callers moved to the new path, the backfill "for later", nobody with authority ever choosing it. A remainder the grill never asked about isn't deferred; it's unfinished work the plan now owns.

The test that separates *in* from *out*: if this shipped as-is, would a reviewer call it **unfinished**, or would they call the missing piece **a different ticket**? Unfinished is in. A different ticket is out. Completeness is not scope expansion — adjacent features, drive-by refactors, and "while we're in there" cleanups stay out.

**Under `--no-follow-ups`** (also accepted: `--no-follow-up`, `--no-followups`, `--no-followup`, `--nofollowups`, `--nofollowup` — record it under the canonical name), owner deferral is off too: every remainder resolves to *in* or *out*, and "we'll handle that later" gets answered with "not available under this flag — in or out?".

## 5. `--auto` — grilling with nobody there

Run unattended only when it's declared: `--auto` on the invocation, the user saying in plain words that no one will answer ("just decide, I'm offline"), or you genuinely having no channel to a human. A detailed ticket, a confident read of the task, or being spawned by another agent are not signs the owner left. If you can ask, ask.

Under `--auto` you play both roles, and the order matters:

1. **Draft the full question set first** — the same structured pass you'd have sent the owner, edge cases and non-goals included. The value is mostly in *generating* the questions, and writing them before answering keeps them coming from the topic list rather than from the answer you already had in mind.
2. **Answer each from the strongest source available, and name it**: investigation evidence (spike verdict, file:line) → the repo's own conventions and how sibling features decided this → the ecosystem or library default → your judgment. An answer from the codebase is a finding; an answer from judgment is a guess, and the record should let a reader tell them apart at a glance.
3. **When it's down to judgment, take the reversible option** — narrower scope, safer default (deny over allow, flag-off over flag-on, additive over destructive) — and note the alternative you passed on, so the owner can flip it cheaply. "Narrower" chooses between tickets, never between finished and unfinished: a migration that reaches four of seven callers isn't the narrow option, it's the broken one.
4. **Mark confidence and blast radius.** Flag every low-confidence answer whose other outcome would change the *shape* of the plan — those are what the owner reads first.
5. **Escalate one-way doors instead of answering them.** Destroying or migrating data non-additively, breaking a public API contract, relaxing an auth or tenancy boundary, anything touching money, secrets, or production: don't pick an answer. Mark it scoped out, pending a human decision, and put it at the top of the record.
6. There's no owner to defer to, so every remainder resolves to *in* or *out*.

## 6. Write the decision record

Save to `docs/plans/<slug>-grill.md`, reusing the slug of an existing investigation brief if there is one (create the folder if missing; suffix `-YYYY-MM-DD` rather than overwrite an unrelated record):

```markdown
# Grill — <feature>
| Field | Value |
| --- | --- |
| Date | <YYYY-MM-DD> |
| Source | <ticket / PRD path / investigation brief / conversation> |
| Mode | <interactive, answered by <owner>> or <--auto, self-answered> |
| Flags | <--auto --no-follow-ups --no-e2e, or "none"> |

## One-way doors awaiting a human   (--auto only; omit otherwise)

## Decisions
| # | Topic | Question | Answer | Source | Confidence |
<Source: owner / evidence (file:line or spike) / repo convention / ecosystem default / judgment.
 Confidence column only under --auto.>

## Completeness dispositions
| Item | Disposition | Owner or reason |
<in this change / out of scope (why it's a different ticket) / owner-deferred (who decided)>

## Assumptions still open
<assumption → what changes if it's wrong; include anything logged after "just go">
```

## 7. Hand off

Summarize the decisions that changed the shape of the work, anything still open, and — under `--auto` — the low-confidence, high-blast-radius answers the owner should check first. Suggest `write-plan` next (it reads this record), or `implement` to drive the whole loop from here.
