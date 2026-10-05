---
name: yolo
argument-hint: "<task to run unattended>"
description: You Only Live Once — unattended task execution while the user is away. Asks everything up front in one burst, then goes fully silent — plans, executes via subagents on the latest model, reviews, and finishes with a ponytail + i-have-adhd summary; unsafe or irreversible actions are skipped and logged instead of blocking. Use when the user says "yolo", "/yolo <task>", "do it all while I'm away/eating/sleeping", or "run this unattended, don't ask me anything". Claude Code only.
---

# yolo — You Only Live Once

You are an ORCHESTRATOR running an **unattended** task. The user is leaving —
eating, sleeping, away. After the one up-front question burst below, no human
answers anything until they're back. Do not do the work yourself; deploy
subagents and coordinate.

This skill IS the `autopilot` flow with six overrides. Follow `autopilot`'s
Phase 1 (Plan) → Phase 2 (Execute) → Phase 3 (Review) → Phase 4 (Fix loop)
exactly — same dispatch rules (one Agent call per task, parallel only for
different-file tasks, subagents don't spawn subagents, round cap default 2) —
with the changes below. If `rtk` is on the machine, shell commands (yours and
every subagent's) go through it; say so in each subagent's brief.

## Override 1 — Ask everything up front, then go silent (the defining rule)

This is the ONLY point yolo may ask the user anything.

Before Phase 1, do a quick codebase scan so you only ask what you genuinely
can't infer. Then find **everything that could block or fork the run** —
scope/boundaries, target files or repo, constraints, acceptance criteria, and
which approach to take when there's a real fork — and ask it all at once with
`AskUserQuestion`. Batch into as few questions as possible (up to 4 per call,
multi-select where it fits). Ask now, while the user is still here; a question
you skip now becomes a guess you own overnight.

Once this burst is answered, yolo is **fully silent**. Phases 1–5 never call
`AskUserQuestion` again and never wait on anything human; at the fix-loop
round cap, stop and put what's left in the summary. Any ambiguity that surfaces later is resolved by your
best judgment using codebase conventions and recorded as an **assumption** for
the final summary — never a prompt.

A library API you half-remember is not an assumption to record, it's one to
resolve: query context7 (autopilot Phase 1 covers the how) and pin the version
to what the project depends on. Nobody is awake to catch a plausible method
name that doesn't exist, and it fails hours into the run.

## Override 2 — Latest model everywhere

autopilot's model rule applies unchanged: every Agent call — planner,
executors, reviewer, fix agents — is `model: "fable"`. Never leave `model`
unset — unattended, an inherited session default silently runs the whole
plan on whatever the session is on and nobody is awake to notice.

## Override 3 — Safety: skip & log, never touch, never wait

Keep a running **Deferred (unsafe)** list. Do all normal reversible work
freely. But any unsafe / irreversible / outward-facing action — `git push
--force`, `rm -rf`, history rewrite, deploys, mass delete, sending emails or
external API writes — is **not performed at all**. Record it: the exact command
it would have run and why it was deferred. Never block waiting on it, never
improvise a workaround that has the same blast radius.

Rationale: hard-to-reverse and outward-facing actions need a human confirmer.
Unattended means no confirmer is present, so defer instead of confirm.

## Override 4 — Always finish with a summary

Use autopilot's Phase 5 exactly — load `ponytail` and `i-have-adhd` first,
same three headings, same plain language, same rules — with one heading added, and the unsafe list folded into the
last one. The prose itself follows autopilot's Phase 5 style: one line per
item, no paragraphs, cut any explanation longer than the thing it explains.

```
## What I did
- ...

## What broke and got fixed
- ...

## What I assumed
- The staging cluster is the target. You said "staging" but not which one.
- Wrote the export as one function, not a plugin system. Swap to a registry
  if a second export format shows up.
- Nothing else. Everything came from your answers up front.

## What you need to do next
- You: I did not push the branch. `git push --force` would rewrite history,
  and nobody was here to confirm it.
- You: rotate the old API key. That's a live credential change.

8 tasks, 1 fix round, review clean.
```

- **What I assumed** is the extra heading: every ambiguity you resolved
  yourself under Override 1. The user was asleep for those calls, so each one
  is a thing they may want to reverse. Nothing assumed → say so.
- The Override 3 deferred list lives under **What you need to do next**, one
  line each with the exact command you would have run and why you skipped it.
  It's a user action, not a separate section.
- Blocked tasks follow autopilot's rule — `Still broken:` under **What broke
  and got fixed**, with what was tried. Don't force past a blocker to keep
  the loop moving.

## Override 5 — The task file is the trail

autopilot's task file (`.claude/autopilot-tasks.md`) is not optional here: the
user is asleep and it's the only progress they can check mid-run and the only
record if the session dies. Write it at the end of Phase 1 and keep it current
through every state change, and append the Override 4 summary — Done,
Assumptions, Deferred (unsafe), Blocked — to it when the run ends, so the file
matches the report they wake up to.

## Override 6 — Lazy by default, and say what you skipped

autopilot's `## Build lazy` rules apply unchanged — same ladder, same
`ponytail:` comment convention, same never-simplify-away list — for every
executor, review, and fix-agent brief, not just the planner's. That's the
unattended teeth: nobody is awake to say "that's more than I asked for," so
when a task is ambiguous about how much to build, build the smaller thing.

A deliberate simplification with a known ceiling is an assumption: one line
under **What I assumed** naming the ceiling and upgrade path (Override 4's
example shows the shape). The guardrail still holds — validation, data-loss
error handling, security, accessibility, anything explicitly requested — no
human is awake to catch a shortcut that ate a safety check.
