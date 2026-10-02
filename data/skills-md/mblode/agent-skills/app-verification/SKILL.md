---
name: app-verification
description: Builds and maintains a product's own verification harness inside its repo, a verify CLI, a doctor command, per-worktree isolation, a feature map written from the user's point of view, seed data, and a reproduce-first bug handoff. Use when asked to "build a verification harness", "add a doctor command", "give agents a way to verify this app", "prove every feature still works", or "reproduce this bug report". For one-off browser probes against a fixed UI rule catalogue use ui-verification; for repo-wide module boundaries and lint guardrails use codebase-architecture.
compatibility: Create mode needs a shell and the target repo's own toolchain (whatever starts, seeds, and drives that app). Native and desktop proof paths need a computer-use tool as the last-resort method. Runs only when called by name; see Invocation below.
---

# App Verification

Builds, inside a product's own repository, the harness every agent uses to run that product and prove a claim about it: a verify CLI, a doctor command, an isolated instance per worktree, a feature map written from the user's point of view, seed data and test accounts, and a reproduce-first bug handoff. The harness lives in the target repo, not in this skill; this skill is what scaffolds and then maintains it, so every agent that opens that repo runs the app the same way instead of writing a throwaway script each session.

Builds on Lauren Tan's pstack `create-verification-skill` and `maintain-verification-skill` (MIT): the interview-then-generate method, the outcome-based maintenance loop, and the reproduce-first handoff (pstack's Benny automation) are hers. This skill generalizes that method past one company's Mac-mini and worktree-adapter conventions and adds a machine-checkable proof contract (a feature file every path can be checked or explicitly skipped against, a doctor command with an ordered dependency chain, and named worktree isolation). Credit them; this is not a copy of either file.

- **IS:** scaffolding a project-local verification harness (Create mode) and running or extending one that already exists (Maintain mode): the verify CLI's contract, the feature-map format, per-worktree isolation and seed data, the cheapest-method ladder up to computer use, scoped proof, and the bug-handoff format.
- **IS NOT:** ad hoc browser probes against a fixed catalogue of UI rules (`ui-verification`; this skill's `verify` command can call those probes as one check among several), repo-wide module boundaries and enforcement tooling (`codebase-architecture`; this skill's CI wiring follows its enforcement order), pruning an existing test suite (`test-audit`), or a plan for one feature (`planning`).

## Invocation

Create mode edits the target repo and Maintain mode drives a real running instance of it; both are consequential enough to run only when named, not from a loose "check the app" prompt a lighter skill might serve better. On a host that supports it, add `disable-model-invocation: true` to the installed copy's frontmatter so this skill runs only when called by name rather than through automatic routing; `disable-model-invocation` is a host extension, not a portable field, so it is not shipped in this source (`agent-skills-creator`'s `references/format-specification.md` explains why). Hosts with an equivalent explicit-invocation setting should apply it the same way.

## Contents

- [Modes](#modes)
- [The harness contract](#the-harness-contract)
- [Create mode](#create-mode)
- [Maintain mode](#maintain-mode)
- [References](#references)
- [Gotchas](#gotchas)
- [Related skills](#related-skills)

## Modes

Pick by what exists, and say which you picked.

| Mode | You are here when | Output |
|---|---|---|
| **Create** | The repo has no verify CLI, doctor command, or feature map yet | A working harness, proven once end to end against a real feature, handed off to Maintain mode |
| **Maintain** | A harness already exists and needs to run this session, gain a feature, or investigate a bug report | A `clean` / `changed` / `blocked` outcome, or a reproduce-first bug handoff |

Copy this to track progress:

```text
App verification progress:
- [ ] Mode chosen and stated (Create / Maintain)
- [ ] doctor run first, read-only, before any drive
- [ ] Isolation confirmed: own port, own database, own browser profile; refused (not fell back to) the main instance
- [ ] Every path in scope checked or named as a skip with a reason
- [ ] Native/desktop paths, if any, verified with computer use as the last-resort method, not the first
- [ ] Outcome stated: clean / changed / blocked, or a reproduce-first handoff
```

## The harness contract

Both modes build toward the same three commands, kept inside a skill folder in the target repo (for example `.claude/skills/verify-<app>/` or that host's equivalent project-skill location) so the commands live at one path every session finds the same way, rather than as a script an agent reconstructs from memory each time.

| Command | Does | Must |
|---|---|---|
| `doctor` | One read-only pass answering "is this instance worth driving": toolchain, isolation, ports, database, migrations, seed, build freshness, and whichever driver (browser, computer-use) the harness needs | Changes nothing. Exits non-zero per failure with the exact fix, not just the symptom. Stops naming a check as failed once an earlier one it depends on has already failed, printing `blocked by <id>` instead of a cascade of unrelated-looking failures |
| `seed` | Loads fixed test accounts and demo data | Idempotent: safe to run twice, safe against a database that already has the seed. Refuses a non-local or main-instance database rather than seeding it |
| `verify` | Runs the checks a feature file lists, cheapest method first, and reports what ran, what it covered, what it skipped, and why | Every path a feature file lists gets a check or a named skip. Nothing merges silently uncovered under a completeness flag; a skip with no reason invalidates the proof, not just that one line |

`doctor` and `verify` are separate commands: one is read-only triage, the other drives and reports. Merging them hides the read-only fast check behind the slow one every time.

## Create mode

`references/create-mode.md`. Interview the repo (surface, run, drive, observe, isolate), scaffold `doctor`, `seed`, `verify`, and a `features/` folder per the contract above, wire isolation before writing the first feature file, seed the top three to five features, then prove the generated harness end to end before calling it done. A harness nobody has run is a draft, not a deliverable.

## Maintain mode

`references/maintain-mode.md`. Run `doctor` first, every session, before the first drive and after any failed one. Pick one outcome and say which: `clean` (nothing needed changing), `changed` (one PR or commit of proven corrections to the harness itself, never to product code), or `blocked` (name exactly what blocked it). A maintenance run that finds a real product bug reports it; it does not quietly patch around it inside the harness.

Two things this mode owns that a lighter probe skill does not:

- **Scoped proof.** Every path a feature file lists gets checked or gets named as a skip with a reason; a proof that only tried one way into a feature is incomplete even when that one way passed. `references/feature-map-format.md` and the coverage rule in `references/maintain-mode.md`.
- **Reproduce-first bug handoff.** Reproduce in an isolated instance before doing anything else, then hand off in the format `references/bug-handoff.md` defines: it opens with `Reproduced` or `Reproduced but already fixed on main`, then the root cause, then the specific case no test covers, then the instruction to re-run the repro, write a failing test, then fix.

## References

Load only when the condition applies.

| Reference | Mode | Read when |
|---|---|---|
| [references/create-mode.md](references/create-mode.md) | Create | Bootstrapping a harness where none exists |
| [references/maintain-mode.md](references/maintain-mode.md) | Maintain | Running or extending an existing harness, or auditing one for drift |
| [references/feature-map-format.md](references/feature-map-format.md) | Both | Writing or reading a feature file, or checking the map for completeness |
| [references/verification-ladder.md](references/verification-ladder.md) | Both | Choosing a method for a path, or deciding whether a native/desktop path finally needs computer use |
| [references/worktree-isolation.md](references/worktree-isolation.md) | Both | Setting up or checking port, database, and browser-profile isolation, or seeding test accounts |
| [references/bug-handoff.md](references/bug-handoff.md) | Maintain | Investigating a bug report |

## Gotchas

- A prompt telling an agent to use its own port does not survive a rushed session; the refusal has to live in the CLI (`doctor` and `verify` hard-fail on the main instance's port or database) or two worktrees eventually collide.
- A dev-only sign-in shortcut or a fixed test-account secret is a production backdoor the moment it ships enabled. Gate it on development mode and a local database, add a boot check that refuses to start with it on against anything resembling production, and verify the guard itself, not only the feature it shortcuts.
- `verify --fast` (or its equivalent cli-only mode) is a development convenience, never a merge gate on its own; a run that skipped every browser and computer-use check is not the same proof as a complete one, and reporting it as such is how a broken native path ships unnoticed.
- A feature file's `id` is load-bearing: verify's history and any proof record reference it. Renaming the id is a breaking change to that history, not a free-form rename.
- Two feature maps drift the moment a second one exists. Keep one canonical map per app; if a lighter probe skill also tracks routes or components, point at this map rather than growing a parallel one.
- `manual` is a standing task to make a path drivable, not a permanent excuse. It always reports as skipped with a reason, and the reason should shrink over time, not accumulate.

## Related skills

- `ui-verification`: scoped browser probes against a fixed UI rule catalogue, one finding at a time. This skill's `verify` command can call those probes for the paths they cover; it does not replace them for a rule-by-rule audit.
- `codebase-architecture`: repo-wide module boundaries, CI guardrails, and the enforcement order this skill's own CI wiring follows.
- `test-audit`: suite-wide pruning of a durable test suite, a different asset from the feature map here. Gating a new test in a diff is `tidy`.
- `planning`: a plan for one feature; a new feature's plan is where its eventual feature file starts.

Maintenance only: `evals/evals.json` holds the behavioural scenarios and routing prompts for anyone changing this skill. It never loads during a verification run.
