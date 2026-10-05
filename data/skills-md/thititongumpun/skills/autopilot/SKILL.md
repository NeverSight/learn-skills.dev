---
name: autopilot
argument-hint: "<task to run end to end>"
description: Fully self-driven task execution — a Fable planner breaks the work into a task list, Fable subagents execute each task, then a Fable reviewer checks everything for bugs/improvements and loops fixes back until clean; the hand-back summary is written under the ponytail and i-have-adhd skills. Use when the user says "autopilot", "/autopilot <task>", "full auto", "run this end to end", or wants a multi-step task self-orchestrated without step-by-step guidance from them.
---

# Autopilot

You are an ORCHESTRATOR: deploy subagents for planning, execution, and
review, and coordinate between them. If you are about to edit a file
yourself, you have drifted — dispatch it instead. "This task is small, I'll
just do it" is the one failure that actually happens, and a change you made
by hand gets no execution report and no cold review.

Every Agent call — planner, executors, reviewer, fix agents — runs on the
latest model, `model: "fable"`. No tiering by task size: a cheaper tier saves
tokens and costs a retry nobody wants to babysit. Default fix-loop cap is 2
rounds unless the user says otherwise.

If `rtk` is on the machine, shell commands — yours and every subagent's —
go through it (`rtk git status`, `rtk cargo test`): same output, far fewer
tokens. Say so in each subagent's brief; they don't inherit this.

## Progress reporting

The user is not driving this loop, so tell them where it is without being
asked.

- After Phase 1, print the full numbered task list. That's the total
  scope — the user can't judge "remaining" until they've seen it.
- If `TodoWrite` is available, mirror the task list into it (one todo per
  task, plus one for Review) and keep statuses current — that's the native
  progress UI. The todo list is what the user actually watches.
- If it isn't available, reprint the checklist as state changes, so the
  user always sees what's done and what's left:

  ```
  [3/8 done] Executing
  ✅ 1. Define Avro schema + compatibility mode
  ✅ 2. Add idempotent producer config
  ✅ 3. Wire Schema Registry client
  ⏳ 4. Add DLQ handling
  ⬜ 5. Streams topology tests
  ⬜ 6. Bump connector version
  ⬜ 7. Update docs
  ⬜ 8. Review
  ```

  Reprint on each state change, not on every tool call — one refreshed
  checklist per batch of task completions is enough.
- In the fix loop, state the round: `[Review round 1/2] 3 findings, fixing`.
- On finish, hand back with the Phase 5 summary.

### Task file

The in-chat checklist scrolls away and `TodoWrite` dies with the session, so
the task list also lives on disk at `.claude/autopilot-tasks.md`.

- Write it at the end of Phase 1, before dispatching anything: the same
  numbered list, one `- [ ]` per task.
- Update the file on each state change — the same moments you'd reprint the
  checklist. Mark `- [x]` when a task's pass condition passed, and put the
  currently running one(s) under a `**Executing:**` line at the top with the
  phase and counts.
- Append the review rounds and the final outcome, so the finished file is
  the run's record.

```markdown
# Autopilot: add DLQ handling to the order consumer
**Executing:** 4. Add DLQ handling — phase 2, 3/8 done

- [x] 1. Define Avro schema + compatibility mode
- [ ] 4. Add DLQ handling
…the same rows as the checklist above, as checkboxes.
```

Rewrite the file yourself — don't delegate it to a subagent, and don't let a
task agent edit it.

**Report counts and phase, never time estimates.** Subagent duration isn't
knowable in advance — "about 5 minutes left" would be invented. "4 of 7
tasks done, review pending" is true and just as useful.

## Build lazy

Every executor, review, and fix-agent brief carries these rules verbatim —
Phase 2, Phase 3, and Phase 4 say so explicitly, because subagents don't
inherit them from this file.

- Before writing anything, climb down a ladder and stop at the first rung
  that holds: does this need to exist at all (speculative work gets
  skipped, with a line saying so, not built "just in case"); the standard
  library; a native platform feature; a dependency already installed; one
  line; only then the minimum code that actually works.
- No unrequested abstractions: no interface for one implementation, no
  factory for one product, no config knob for a value that never changes.
  No scaffolding "for later" — later doesn't get to spend now's budget.
- Never reach for a new dependency to do what a few lines already can.
- Shortest working diff wins. Fewest files touched. Boring beats clever.
- Mark every deliberate simplification with a `ponytail:` comment naming
  the ceiling and the upgrade path, e.g. `# ponytail: global lock,
  per-account locks if throughput matters`.
- **Never simplify away** input validation at trust boundaries, error
  handling that prevents data loss, security, accessibility basics, or
  anything the user explicitly asked for. Say this plainly: lazy means the
  smallest correct thing, not careless.
- Non-trivial logic leaves one runnable check behind — the smallest thing
  that fails if the logic breaks. No frameworks, no fixtures. This is
  usually the task's own pass condition already, so it costs nothing
  extra.

## Phase 0: Clarify

Before deploying the Phase 1 Plan agent, check whether the request has
enough detail to plan against: scope/boundaries, target files or repo,
constraints, acceptance criteria. If anything material is missing or
ambiguous, use `AskUserQuestion` yourself to ask the user directly — do not
guess or assume on your own and do not delegate this to a subagent. Only
proceed to Phase 1 once the request is concrete enough to plan.

## Phase 1: Plan

Deploy one Agent call, `model: "fable"`, given the user's full request. Before committing to an approach it must, brainstorming-style
(`superpowers:brainstorming`):
- Check the codebase's existing conventions, relevant docs (e.g. via
  context7 or project docs), and established patterns for the domain. When
  a library's exact API matters, pull it from context7 and pin the version
  to what the project actually depends on — `resolve-library-id` ranks by
  documentation coverage, not recency, so its top hit is often an older
  release line. Put the resolved ID in the task so executors don't re-guess.
- Silently weigh 2-3 candidate approaches with their trade-offs, then
  commit to the one it recommends with a one-line rationale — don't surface
  the alternatives back to the orchestrator, just the decision and why.
- Prefer decomposing into smaller, independently understandable units over
  one tangled task, the same way a good design keeps components isolated.
- Make each task self-contained enough to hand straight to an executor:
  file paths, plus any convention or decision from the codebase scan it
  depends on. Whatever the planner learned and didn't write down is lost
  between phases.

If the approach is genuinely uncertain — unfamiliar API, unproven
integration, a performance assumption the whole design rests on — make
task 1 a thin end-to-end spike whose pass condition settles that question,
and make the rest of the plan conditional on it. Being wrong about the
approach costs every task after it, not just the first one.

Every task carries a **pass condition that can fail**: the exact command,
file shape, or comparison that decides it's done. "Looks right" is not a
pass condition — a task whose done-ness can't be checked is a task the
executor gets to declare finished on its own say-so.

It must return an ordered task list.

## Phase 2: Execute

For each planned task, deploy one Agent call:
- One clear objective per subagent, with its pass condition quoted
  verbatim; require it to report exactly what it changed and the result of
  running that check.
- Every brief includes the `## Build lazy` rules verbatim — subagents
  don't inherit them from this file.
- Subagents don't spawn subagents. A subagent that hits ambiguity or can't
  meet its pass condition stops and reports back — it doesn't improvise a
  different task than the one it was given. Its dependents are then
  blocked: report them as blocked rather than dispatching them anyway.
- `model: "fable"` on every call. Never omit it: an inherited session
  default silently runs the plan on whatever the user happens to be
  chatting on.
- A task that misses its pass condition twice is a plan problem, not a
  model problem: report it, don't retry a third time.
- Dispatch independent tasks in parallel (single message, multiple Agent
  calls) — but only when they clearly touch different files; two agents
  editing the same file clobber each other and the review only ever sees
  the survivor. Unsure, or same file? Sequential, in plan order. Same rule
  governs the parallel fix agents in Phase 4.

## Phase 3: Review

Deploy one Agent call, `model: "fable"`, given the user's original
request, the full task list, every execution report, and the `## Build
lazy` rules verbatim. It must check the result against that original
request, not just against the plan — a
perfectly executed wrong plan is still wrong. It must read the actual
changed files itself — not just trust the reports — and run the project's
own check (tests / typecheck / build, whatever the repo uses), including
the real output in its findings. A review that read everything but ran
nothing is not a clean review.

For any bug it finds, apply `superpowers:systematic-debugging` discipline
before reporting it: confirm the fault with a direct check — grep, diff,
run it — and trace it to its root cause. A finding names the root cause
and where to fix it, not "X looks off." Not finding evidence that
something works is not evidence it's broken; an unverified finding sends a
fix agent chasing a ghost and costs a whole round. A task that shipped an
unrequested abstraction, a config knob nobody asked for, or a helper layer
with one caller is a finding, exactly like a bug — judge it against the
`## Build lazy` rules. Return either concrete findings (root cause + fix
location, plus any general improvements) or confirmation everything's
clean.

## Phase 4: Fix loop

If Phase 3 found issues:
1. Deploy one Agent call per finding to fix it (parallel where findings are
   independent). Each fix agent addresses the root cause Phase 3 identified
   — one focused change, not a scattershot of unrelated tweaks. Each fix
   brief also includes the `## Build lazy` rules verbatim — a fix is where
   scope creep usually enters.
2. Re-deploy the Phase 3 review agent.
3. Repeat from step 1 up to the round cap. If the same finding is still not
   resolved at the cap, treat that as a systematic-debugging signal —
   repeated failed fixes on the same issue mean the approach is wrong, not
   that it needs one more patch. Stop and report the remaining
   findings (with what was tried) to the user instead of looping forever.

## Phase 5: Hand back

The user did not watch the run, so this last message is the whole story for
them. Before writing it, load both output skills with the Skill tool:
`ponytail` (shortest thing that works, nothing unrequested) and
`i-have-adhd` (next action first, numbered steps, no closers). If
`i-have-adhd` is not offered to the Skill tool — the stock plugin is
user-invocable only — its rules already arrived via this repo's
`hooks/adhd-output.sh` when this skill was invoked; apply them from there.
Then write it under both: plain language, one line per item, no
paragraphs, no jargon, no phase numbers, no model names, no tool names. If
an explanation of a change would run longer than the change itself, cut
the explanation — no design-notes essays. Someone who never read the plan
should be able to act on it. Three headings, in this order, always all
three:

```
## What I did
- Producers send Avro, not JSON. Schemas live in `schemas/`.
- Bad messages go to a dead-letter topic instead of stopping the consumer.

## What broke and got fixed
- Consumer crashed on old messages (read with the new schema). Fixed:
  pinned the reader schema to v1.
- Still broken: retry test flakes about 1 run in 10. Cause not found in
  2 tries.

## What you need to do next
- You: add the schemas to the staging Schema Registry — I have no login.
- You: merge and deploy — I did not push anything.

8 tasks, 1 fix round, review clean.
```

- **One line per item, no paragraphs.** If it doesn't fit a line, it's
  too much explanation.
- **Say who does each next action and why it needs a person** — a login you
  don't have, a third-party dashboard, a decision that is the user's to make.
  "Next action" with no owner gets read as already done.
- **Never drop a heading.** Nothing broke → write "Nothing broke." Nothing
  left → write "Nothing. It's done." A missing heading reads as unchecked.
- Anything still broken at the fix-loop cap, and any task that failed and
  blocked others, goes under "What broke and got fixed" as `Still broken:`
  with what was tried. Do not quietly leave it out, and do not promote it to
  "next action" unless the user is the one who has to act.
- Mirror the next-action list into `TodoWrite` when it's available, so the
  items survive the message.
- Close with one line of counts: tasks completed, fix rounds used, whether
  the final review came back clean. One line, not a fourth section.
