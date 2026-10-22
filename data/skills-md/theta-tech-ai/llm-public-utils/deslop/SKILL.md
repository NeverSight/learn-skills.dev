---
name: deslop
description: "Analyze and refactor code against a library of 50+ coding principles — clean code, architecture, reliability, and data layer — finding and fixing slop, duplication, dead code, over-abstraction, god files and needless complexity, measuring it honestly, and running whole-codebase simplification campaigns. It also extends the library, by researching a missing principle and merging it in. Use for deslop passes, code-quality and PR review, dedup and cleanup sweeps, tech-debt triage, refactor planning, complexity analysis, or when code is called messy, bloated, overcomplicated, copy-pasted, hard to read, or in need of a cleanup."
---

# Deslop: Code Quality Analysis Command
<sub><sup>Size: this file is ≈16 KB (≈4k tokens) and the `references/` tree is ≈325 KB across 72 markdown files. Only this file loads when the skill activates; everything else is opened by path, so nothing here is paid for twice.</sup></sub>

> A comprehensive command `/deslop` or $deslop (depending on your harness) for identifying and fixing "slop" in your codebase.

This command combines a code analysis workflow with an extensive library of coding principles living in [references/](references/). When you run `/deslop [file-or-directory]`, or even just `/deslop` or perhaps `/deslop my frontend typescript code` the AI will read your code, cross-reference it against these principles, and suggest specific fixes with before/after examples.

**Scoped pass or whole-codebase campaign?** The default is a pass over the file, directory, or diff you name. When the ask is a **campaign** — "massive simplification", "across the board", "minimum 30% LOC", "break up the god files", "get it all done, no excuses, present me a PR" — follow [references/modes/campaign.md](references/modes/campaign.md) instead, and measure it with [references/library/measuring.md](references/library/measuring.md).

Whether or not you use this deslop command on your code base, you should read all the coding principles yourself, as a human - you might actually learn something useful.

---

## Where to read what

One row per file, in the order a pass meets them. Every markdown in this skill is reachable from this table or from a category index below, and CI fails if one is not.

| File | When |
|------|------|
| [references/readings/auditing.md](references/readings/auditing.md) | **Always** — the audit itself: persona, the mode question, the autonomy rule, violation report format, and the **input census** (for each external input: who owns turning it into a decision, and how many places re-interpret it — zero owners or several is a finding, reported even when it ranks last) |
| [references/readings/when-to-relax.md](references/readings/when-to-relax.md) | **With every reading** — the guardrail: contexts where a principle is over-applied, and the meta-principle that says a violation worth "fixing" into worse code is not a violation |
| [references/stages/recipes.md](references/stages/recipes.md) | **At the start of any pass** — five asks, five invocations: scoped pass, directed cell, coverage pass, campaign, library extension. Pick the shape before the readings |
| [references/stages/planning.md](references/stages/planning.md) | **Before a pass that must cover the library** — or after a pass that missed something: survey, slice, group the principles, write the permutation list, rank it against a budget, choose the execution mechanism you actually have |
| [references/stages/aggregation.md](references/stages/aggregation.md) | **The moment more than one reading has reported** — merge on locus + principle into corroborated / single / disputed, account for coverage, and mark a cell that quotes nothing as a failed reading |
| [references/stages/consolidation.md](references/stages/consolidation.md) | **After aggregation, before anything is reported or filed** — verify, apply the guardrail, bucket into now / next / wait-or-drop, collapse findings into concerns, group into a milestone |
| [references/stages/reporting.md](references/stages/reporting.md) | **Immediately before you speak to the person who asked** — lead with the answer, bucket the work, keep it short, and never bury the result in method |
| [references/modes/campaign.md](references/modes/campaign.md) | **Whole-codebase campaigns** — "massive simplification", "across the board", "minimum 30% LOC", "get it all done", "present me a PR". The five sweeps, the target discipline, running it at scale, and the delivery protocol |
| [references/modes/loop-until-dry.md](references/modes/loop-until-dry.md) | Thorough passes ("keep going") — iterate until a full scan finds nothing actionable |
| [references/library/evaluation.md](references/library/evaluation.md) | **Before claiming a pass proved anything**, and after any control run — the recorded controls, their numbers, and how to add one |
| [references/library/measuring.md](references/library/measuring.md) | **Any pass that will claim a number** — the four measurement harnesses, the unbiased task corpus, the metrics that carry the story (nesting depth, `elif` chains, cyclomatic complexity), and the honest before/after reporting skeleton |
| [references/library/extending-the-library.md](references/library/extending-the-library.md) | **Adding a principle** — the ask is a *gap* in the library, not a pass over code: discovery against every existing principle, research, the house draft format, both indexes, and the publish path |
| [references/library/detecting-slop.md](references/library/detecting-slop.md) | Building or questioning a detector — what the tools cannot see, and the control a detector script must pass to earn its lines |
| [references/principles/data-layer.md](references/principles/data-layer.md) | The target has a database — schema, SQL, migrations, foreign keys, normalization, constraints, **indexes and join access paths alongside the queries that must use them** (**The Data Layer**). Treat the schema as a slice in its own right: it usually sits outside the directory being audited, and no index finding is provable from the DDL alone |
| [references/readings/duplication.md](references/readings/duplication.md) | Running a dedup sweep — hunting duplication beyond token scanners: the primitives to grep for, the field-overlap recipe for one entity described many times, and the shape-clone scripts in [scripts/](scripts/) |
| [references/library/case-study-simplification-agent-fleet.md](references/library/case-study-simplification-agent-fleet.md) | Worked KISS example — a real pass that collapsed an LLM agent fleet into one agent |
| [references/library/further-reading.md](references/library/further-reading.md) | Background bibliography and concept attribution (not needed mid-audit) |
| [references/lenses.json](references/lenses.json) | Grouping the principles for a planned pass — the default partition of 54 principle files into 9 reading stances (validated by `scripts/swarm_lenses.py --check`); regroup it if the codebase asks for different stances |

## How the library is organised

`references/` is a taxonomy by **role in the pass**, not by topic — topic is already carried by the principle
category. The directory a file sits in tells a reader what to do with it, and the check in
`scripts/swarm_lenses.py --check` fails if a markdown has no role:

| Directory | Role | Read |
|---|---|---|
| `references/stages/` | the four moments of a pass — `planning`, `aggregation`, `consolidation`, `reporting` | at its stage, in order |
| `references/readings/` | what a single reading carries — `auditing` (the report format and census), `when-to-relax` (the guardrail), `duplication` (the dedup sweep) | `auditing` and `when-to-relax` in **every** reading |
| `references/modes/` | modes a pass can run in — `campaign` (measured whole-codebase programme), `loop-until-dry` | when the ask names the mode |
| `references/principles/` | `<category>.md` is a category **index** (read first: the stance and the tells); `<category>/<slug>.md` is one principle | the index first, then every file of an assigned group, in full |
| `references/library/` | reference opened when the ask needs it — claim a number, add a principle, build a detector, cite a source, see a worked example | on request |
| `references/lenses.json` | the principle partition, the indexes each group reads, and the trigger for each stage/mode/library file | by the scripts, and by anyone planning |

**This file is the manifest.** No harness builds one: only `SKILL.md` loads when the skill activates, and every
other file is read on demand *by path* — so a reference nothing here leads to (directly, or through an index that
does) is a file nobody opens. Three checks enforce that, and they run in CI on every push and pull request
(`.github/workflows/skill-checks.yml`):

```bash
python3 scripts/check_reachability.py     # every markdown reachable by following links from this file
python3 scripts/swarm_lenses.py --check   # every principle in exactly one group; no unclassified markdown
python3 -m py_compile scripts/*.py        # the instruments still load
```

Add, rename or move a file and CI names the orphan and which index should link it — so reorganising the library
cannot silently leave a principle behind. Moving a file between roles is `scripts/taxonomy_move.py`, which
rewrites every cross-link by resolving each target from its old location and re-emitting it from the new one.

## Plan the pass before you audit

**A pass is planned, not merely started.** Slop is found when a reader is looking at a specific piece of code
with a specific set of principles in mind, and much less when it is told to "audit this directory" — so the unit
of work is a **cell**: one group of principles × one slice of code × one reading, whose report is merged with the
others afterwards. Survey the shape, design the slices (modules, role archetypes, cross-folder concept clusters,
the schema and its queries, flows, a diff), group the principles into reading stances, write the permutation
list, rank it under a budget, rotate the rounds so a second pass is the complement of the first, and choose the
execution mechanism you actually have — subagents, a harness fan-out, model tiers, or this context one cell at a
time.

The protocol, with the rules that make each step checkable, is
[references/stages/planning.md](references/stages/planning.md). The bookkeeping is optional and scripted:

```bash
python3 scripts/swarm_plan.py --repo <root> --target <dir> --out /tmp/plan --budget 24 [--ledger <jsonl> --round N]
python3 scripts/swarm_lenses.py --emit /tmp/cells --target <slice> --only <group>
```

For a **specific ask** — *"look at separation of concerns in the provider adapters"* — skip the plan and read one
cell: emit the `boundaries` group against that module, or simply open those principle files and read the module
whole. A general pass cannot satisfy that request, because it decides for itself what to open.

## Aggregate, consolidate, then report

A pass always finds more than anyone should act on at once, and a flat list is not a triage. Three stages follow
the readings, each read at its own moment: [aggregation](references/stages/aggregation.md) (merge on locus +
principle; a cell that quotes nothing is a *failed reading*), [consolidation](references/stages/consolidation.md)
(verify at the source line, apply the guardrail, bucket now / next / wait-or-drop, one issue per concern), and
[reporting](references/stages/reporting.md) (the answer first, the short fix-first list, what was left out, then
stop).

## Principle references (indexes)

Each index is a short table of principles with their one-line essences, linking to self-contained files under
`references/principles/<category>/`. **Scope bounds the code you read, not the principles you apply.** A scoped
pass still gets assigned readings — one or two groups, chosen by what the code is (see [recipes](references/stages/recipes.md)) — because reading the indexes and
opening a principle only when a finding "implicates" it is the mechanism that leaves Separation of Concerns
unopened forever. Index-only reconnaissance is a legitimate mode, but name it as one, and never let it be the
default.

Know its cost: a pass can only open a principle it has already suspected, so the ones that need a boundary held
in mind — above all **Separation of Concerns** — are routinely never read. When the ask is coverage rather than
speed, plan the pass instead ([references/stages/planning.md](references/stages/planning.md)): it assigns each
group its files, forces each reading to open them, and merges the reports.

| File | Contents |
|------|----------|
| [references/principles/clean-code.md](references/principles/clean-code.md) | **Clean Code** — KISS, YAGNI, Small Functions, Guard Clauses, Decide Don't Cope, Cognitive Load, Cyclomatic Complexity, SLAP, Self-Documenting Code, Documentation Discipline, Elegance, Legibility, Least Surprise, Patchwork, An Unclaimed Guarantee |
| [references/principles/architecture.md](references/principles/architecture.md) | **Architecture** — DRY, Single Source of Truth, Separation of Concerns, Modularity, One Logical Unit One Home, Encapsulation, Law of Demeter, Orthogonality, DI, Composition Over Inheritance, SOLID, Convention Over Configuration, CQS, Reusability, Parse Don't Validate, A Helper That Must Exist Is an Architecture Finding, Immutability, Idempotency |
| [references/principles/reliability.md](references/principles/reliability.md) | **Reliability** — Fail-Fast, No Silent Defaults, Design by Contract, Postel's Law, Resilience & Graceful Degradation, Least Privilege, Boy Scout Rule, Observability |

---

*Run `/deslop [file-or-directory]` to analyze your code against these principles and let the agent fix any slop it detects.*
