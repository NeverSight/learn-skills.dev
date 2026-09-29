---
name: create-implementation-plan
description: Turn a refined requirements document into a structured implementation PLAN.md a fresh session can execute. Planning only — decides the "how", not the "what". Invoke manually only.
license: MIT
metadata:
  version: "1.11"
---

# Create Implementation Plan

**Planning only** — no code changes, no execution. You produce one document: an implementation plan
that is the contract for a later execution session.

This is the **"how", not the "what"**. The "what" was settled in an earlier refinement step and
lives in the requirements document you're given; do not redefine scope. But you **must flag** any
gap, ambiguity, or inconsistency you find in the requirements — surface it, never paper over it.

## Golden rule

**Never guess — ask.** With one limit: anything resolvable by reading the codebase, resolve by
reading the codebase; only questions the code cannot settle go to the user.

## Steps

Your task is to **produce the implementation plan**. The steps below build toward it; grilling the
user — interviewing relentlessly to resolve anything the code can't settle — is woven through the
design, not a separate phase that runs before planning starts.

1. **Read the requirements document** the user references (e.g. a `*.REQUIREMENTS.md`). If the path
   is ambiguous, ask.

2. **Verify against the actual codebase.** Open the files the requirements cite and confirm the
   prior-art references still hold; note anything that has shifted since the requirements were
   written. The requirements may also carry verified codebase facts — use any that are there to
   save re-discovery work, aware the code may have moved meanwhile (a pinned commit makes the
   check cheap: `git diff <commit>..HEAD -- <cited paths>`). If the requirements gate
   implementation on missing data or upstream work, verify that gate independently — stale gating
   claims are a common failure mode and easily inflate into a plan's first step when the data is
   in fact already addressable.

3. **Work out the approach.** This is the core of the task: design the "how" — what existing code to
   reuse, what to introduce, where each change goes, and the order of operations that avoids broken
   intermediate states (data model before its consumers, code before its tests). Track dependencies
   between steps. Working this out surfaces the **decision tree**: the forks where more than one
   reasonable approach exists. Typical forks to design through (and grill on when the code can't
   settle them): whether to refactor existing code to reuse it or build anew; which API or interface
   to call; which unit tests to add; code style, file names, and folder structure.

   **Docs generally outrank prior art.** A mirrored analogue doesn't override a documented rule,
   and a rule's rationale doesn't license exceptions to it — existing code may predate the rule.
   When docs and prior art conflict and you're unsure how to resolve it, ask the user; a deviation
   the user approves is recorded in the plan's Overrides section, so the execution session knows
   it's deliberate.

   **Prior art models shape, not content.** Its settings fit its own runtime, tooling and purpose
   and may predate the current ones, so before a step reuses a file, check each setting against
   the new component's target and prescribe only what fits, citing the file for shape; "copy X
   verbatim" is a decision settled line by line, never by the file's existence. A technical claim
   a step rests on ("X needs exactly Y") is verified against a doc, a compile or a test, never
   read off what the prior art happens to do.

   **Grill the user along the way.** Whenever the approach hits a fork you can't settle from the
   code, stop and resolve it with the user before continuing — don't guess, and don't defer the
   decision into the plan. Interview relentlessly until you reach shared understanding, walking each
   branch of the decision tree and resolving dependencies between decisions:
   - One question at a time.
   - Every question carries your recommended answer, worded via `explain-in-simple-language`
     when available.
   - If a question can be answered by exploring the codebase, explore instead of asking.
   - Cover every gap, ambiguity, or inconsistency surfaced while reading, verifying, and designing.

4. **Write the plan** (below) — once the approach is settled and no open question remains.

## Plan file

The output must be self-contained and ready for a **fresh session** that reads **only the plan
file** and starts implementing — it should not need to read the requirements document or the
ticket. This is the single most important constraint. Anything the execution session needs
(acceptance criteria, prior-art citations, file paths, naming/string conventions, type signatures,
override notes) must appear in the plan itself. Repetition from the requirements is intentional:
the plan is the contract, not a diff against the requirements.

Create the file in the **same directory as the requirements document**, named by replacing
`.REQUIREMENTS` with `.PLAN` (e.g. `FOO.REQUIREMENTS.md` → `FOO.PLAN.md`). If the input doesn't
follow that convention, append `.PLAN` before `.md`.

Structure — five parts:

1. **Summary** — 1–3 sentences: what this plan implements and the overall shape of the change (which
   areas are touched).
2. **Conventions and overrides** — two distinct kinds of cross-cutting context:
   - **Conventions**: rules that apply across all steps — naming patterns, user-facing string rules,
     the testing approach (what to test, following existing test conventions in the codebase). Copy
     from the requirements verbatim where applicable.
   - **Overrides**: one-time corrections where the requirements deliberately diverge from a default
     or prior assumption. Each entry: what was assumed, what the actual requirement is, and why. The
     execution session applies each only where it fits.
3. **Steps** — ordered implementation steps. Each is concrete enough to act on but doesn't dictate
   every line. Each step has:
   - **What** — a short imperative.
   - **Where** — concrete file paths and identifiers.
   - **How** — the approach in prose. Reuse decisions go here, with `path:line-range` citations for
     prior art.
   - **Snippet** — *only* when prose is genuinely more ambiguous than code (a non-obvious type
     signature, a tricky nested structure, an unfamiliar call shape). Default to omitting; keep
     under ~10 lines.
   - **Depends on** — earlier step numbers this one requires, if any.

   Each step is self-contained — readable without scrolling back. No "as in step 2" without
   restating what step 2 did. Step 1 must never be discovery work ("find the field names", "explore
   where this lives") — discovery already happened in the steps above. A small deterministic sanity
   check of a known fact is fine; open-ended investigation is not.
4. **Acceptance criteria** — flat checklist the implementation must satisfy, copied from the
   requirements' AC section. If unnumbered, number them (`AC-1`, …). Each references the step
   number(s) that satisfy it (e.g. "AC-3 → steps 4, 7"). Note any AC that needs manual verification
   only. The execution session uses this as its done-check.
5. **Decisions log** — a standing instruction copied into the plan for the execution session:
   "When a settled decision deviates from or extends this plan, append one line — the decision
   and its why — to `<slug>.DECISIONS.md` beside this plan, the moment it's settled." Without
   it, the why behind mid-implementation pivots is lost to later handover and review.

The plan must capture **all the thinking** — every decision needed to implement the feature, so the
execution session re-derives nothing. It may omit only mechanical, locally-reversible detail with no
cross-cutting consequence (a variable name, the exact wording of a log line). Anything that spans
files, depends on knowing the codebase, or is costly to get wrong (which utility to reuse, what
order to change things in, what new types to introduce) belongs in the plan. When unsure whether
something is a decision or a mechanical detail, put it in.

## Boundaries

- Do **not** modify any source files. The only file you write is the plan.
- Do **not** start implementing.
- When preparing the plan from a `*.REQUIREMENTS.md` file, you normally shouldn't need to go back to
  the `*.TICKET.md` — close any gaps with the user instead. Never assume a requirement; ask.
- Write the plan to disk only after every open question is resolved.

State clearly when done that the plan file is ready, referring to it by its **project-relative
path** (relative to the current working directory — never absolute). Then tell the user to start a
**fresh execution session** with a clean context that reads **only the plan file**, implements it,
then runs the project's validation (lint, tests, build).

End with a **single copy-pasteable launch command** — session name and prompt combined, so one
paste starts the execution session. Use the launch syntax of the agent tool in use
(vendor-agnostic — `claude` below is only the example). Name the session `execute-plan-<slug>`,
where `<slug>` is the plan filename's slug (without id prefix or extension), so the phase is
recognizable in the session list, e.g.:

```
claude --name execute-plan-report-approval "Execute the plan .agents/plans/123-report-approval/123-report-approval.PLAN.md"
```

Then offer the alternative — clearing the current session instead (vendor-agnostic — `/clear` below
is only the example; use the clear command of the agent tool in use):

OR /clear and run:

```
Execute the plan .agents/plans/123-report-approval/123-report-approval.PLAN.md
```
