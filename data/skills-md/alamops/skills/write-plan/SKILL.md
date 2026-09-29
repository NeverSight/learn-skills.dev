---
name: write-plan
description: (alamops) Writes a decomposition-ready implementation plan to `docs/plans/<slug>.md` — objective, grounded context with file:line anchors, approach and rejected alternatives, a work breakdown where each task owns files disjoint from its wave-siblings, test tasks by layer with an explicit e2e decision and run recipe, execution waves, blast radius, open assumptions, and a completeness ledger dispositioning every would-be follow-up. Builds on `investigate`/`grill` output when present, else grounds itself read-only and asks the load-bearing questions first. Presents the plan for approval and changes no code; `implement` and `execute-plan` can run it as-is. Use when the user asks to write or draft an implementation plan, plan how to build something before coding, break a change into parallelizable work, or turn a spec into an execution plan. Phase 3 of `implement`, runnable alone. Not for product PRDs (to-prd), human-facing engineering tickets (create-tasks), or building the thing (implement).
---

# Write plan — the contract every downstream agent works from

Your job is to turn a change that's understood into a plan that can be **executed by parallel agents without them colliding**, and to save it as a durable artifact under `docs/plans/`. The plan is not a summary of intentions; it's the contract each implementation and test agent works from, which is why it has to say exactly which files each task owns.

## Where this sits

This is Phase 3 of the `implement` delivery loop, packaged to run on its own. It reads an `investigate` brief and a `grill` decision record when they exist; its output is what `execute-plan` (coding waves) and `implement` (the whole loop) execute.

**Read-only on the repo.** The only file you write is the plan. No code changes happen until someone approves it.

## 1. Gather the inputs

Look for, and read, whatever already exists for this feature:

- `docs/plans/<slug>-investigation.md` — findings, spike verdicts, completeness inventory, runnability.
- `docs/plans/<slug>-grill.md` — the owner's decisions, dispositions, and open assumptions.
- The source ask — a ticket, a PRD, a spec, or the conversation.

**If there's no investigation**, do a proportionate read-only grounding pass before writing: the files the change touches, sibling code paths to mirror, every caller of what's changing (including re-exports, barrels, and scripts or jobs outside the main source tree), how the app and its tests run. On Claude Code, a couple of parallel `Explore` agents cover this; on a small change, read inline. A plan without file:line anchors is guessing at the file ownership it's supposed to guarantee.

**If load-bearing questions are still open** and nobody grilled the owner, ask them in one structured pass before writing — the few whose answer would change the plan's shape, not a full interrogation. (For a large or ambiguous change, suggest `grill` instead.) If the owner says "just write it", proceed and log each assumption in §8. Never plan silently over an unasked question: a plan built on an assumption nobody sees is how the wrong thing gets built efficiently.

## 2. Build the completeness ledger first

Before breaking down any work, list every candidate follow-up — every caller still on the old path, every place a shape propagates, the existing rows a migration must backfill, the reachable states with no handling, the docs that will describe the old behavior, the code the change orphans. Then disposition each:

- **In this run** — with the task ID that will own it.
- **Out of scope** — with why it's a different ticket.
- **Owner-deferred** — only if the owner actually decided it (at the grill or when approving this plan), with who and where. Not available under `--no-follow-ups` or `--auto`.

A row that just says "deferred" with no owner behind it isn't a disposition — it's a task you forgot to write.

Do this *before* the breakdown and let it feed the breakdown: a remainder you notice while writing tasks tends to get written down as a note; a remainder you enumerate first gets a task. The ledger is also the honest scope estimate — it's where the owner sees how much finishing the job properly adds, before a line of code is written.

The line between *in* and *out*: would a reviewer call the shipped change **unfinished** without it, or call it **a different ticket**? Adjacent features, drive-by refactors, and dependency upgrades stay out.

## 3. Partition the work — the heart of the plan

Split the change into tasks such that, **within a wave, no two tasks own the same file**, and order the waves so every task's dependencies land in an earlier wave. This is what makes parallel execution safe: agents that edit the same file concurrently corrupt each other's work, and no amount of good briefing fixes that after the fact.

For each task:

- **ID** and a one-line goal.
- **Owned files** — the exact paths it creates or edits. Nothing else.
- **Depends on** — the task(s) or wave that must land first.
- **Acceptance** — how you'd know the task is done, concretely.

Watch the hot spots that make a partition quietly invalid — files that many tasks "just need one line in": route or DI registries, barrel `index` files, schema definitions, migration sequence numbers, lockfiles and package manifests, generated clients, i18n catalogs, shared fixtures and snapshots. Either give that file to exactly one task (often a small wiring task in a later wave) or sequence the tasks that touch it.

**Keep every barrier green.** Each wave ends in a checkpoint commit that later work resumes from, so at every barrier the tree should build and the suite should pass — a plan whose checkpoints are knowingly red makes "resume from the last green wave" meaningless. Tasks in the same wave can code against an interface the plan pins down (a signature, a type, a column name), so a breaking change and the callers and tests it breaks usually belong in the *same* wave as separate tasks, not in consecutive ones. Where a red barrier is genuinely unavoidable, say so in §6 and name exactly which tests are expected to fail and which task turns them green.

Keep the fleet proportionate: group trivially small edits into one task rather than one task per file, and don't force parallelism onto work that shares context and ordering — two sequential waves beat one colliding wave. Coding parallelizes worse than research.

**Validate before you finish.** Cross-check the owned-files lists of every wave; if any path appears twice in one wave, the wave is invalid — re-partition it.

## 4. Plan the tests

List test tasks by layer (unit / integration / e2e), which implementation task each covers, and their owned test files — partitioned the same way, by module under test.

**Decide e2e applicability explicitly.** It applies when the change has a user-visible flow or crosses a process boundary (UI → API → DB, service → service, CLI → filesystem) and the app can run locally. It doesn't apply to a pure library or helper change fully exercised by unit tests — and then the plan says so. "Not applicable" is a recorded decision, never a silent omission. When it applies, record the **run recipe**: the e2e command, how the app and its services start, seed data, credentials and environment prerequisites. If the repo has no e2e harness, don't quietly plan heavyweight infrastructure — propose the minimal ecosystem-standard harness scoped to this feature's flows as a decision for the owner.

Under `--no-e2e`, record e2e as *skipped by flag* and plan unit/integration only.

## 5. Write the plan

Save to `docs/plans/<slug>.md` — reuse the slug from an existing investigation or grill record; create the folder if missing; suffix `-YYYY-MM-DD` if an unrelated plan already has that name. Use this template (it matches the one `implement` writes, so either skill can execute it):

```markdown
# Plan — <Feature Name>
| Field | Value |
| --- | --- |
| Date | <YYYY-MM-DD> |
| Source | <task / PRD path / investigation + grill records / conversation> |
| Flags | <e.g. --no-e2e --no-follow-ups, or "none"> |
| Gates | <"grilled + approved by owner", "approved by owner (no grill)", or "self-resolved under --auto"> |
| Branch | TBD — set when execution starts |
| Base SHA | TBD — set when execution starts |

## 1. Objective & success criteria
## 2. Context & constraints   (grounded findings with file:line anchors; spike verdicts
   with what was measured and under which versions)
## 3. Approach & key decisions   (alternatives considered and why this one; mark which
   decisions rest on evidence vs. reasoning)
## 4. Work breakdown — implementation tasks
   | ID | Goal | Owned files | Depends on | Acceptance |
## 5. Work breakdown — test tasks
   | ID | Layer | Covers | Owned files | Acceptance |
   E2e: applies to <flows> / not applicable because <reason> / skipped via --no-e2e.
   Run recipe: <command, app + services startup, seed data, credentials>
## 6. Execution waves   (which tasks run in parallel; the barrier between waves)
## 7. Blast radius & risks   (callers, sibling paths, migrations, rollback, feature flags)
## 8. Open questions / assumptions   (what the owner left open and what you're proceeding
   on; under --auto, the self-answered Q&A — question / answer / source / confidence —
   plus any one-way decision scoped out for a human. Not a bin for remainder: that's §9)
## 9. Completeness ledger
   | Item | Disposition | Task ID / reason / who deferred |
```

## 6. Present it and get approval

Give the owner a short read of the plan rather than the whole file: the objective, the approach and the key decision behind it, the waves at a glance (how many tasks, how parallel), how big the ledger made the job, the top risks, and every open assumption. Then ask for approval or changes. This is the last cheap moment to change direction — once code is written against a plan, changing the plan costs a rewrite.

If the ledger turned up remainder an order of magnitude larger than the original ask (the migration touches 200 call sites across three services), say so plainly and let the owner choose scope — don't let the size hide inside §9.

**Under `--auto`**, don't wait: write the plan, mark it self-approved in `Gates`, and put the §8 decisions the owner should check first at the top of your summary.

Once it's approved, suggest the next step: `execute-plan` to run the coding waves, or `implement` to take the plan through code, review and tests to green.
