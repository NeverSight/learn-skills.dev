---
name: gap-trap
description: Use when asked to set up, install, or refine an agent quality framework in a repository (rules with gates, architecture contracts, proven-red tests, ratchets, playbooks), or when the user says "gap-trap", "gap-trap setup", "gap-trap refine", "gate the rules", or "make the agents' code match the rules".
---

# gap-trap

Sets up a quality framework for repositories where agents write most of
the code. Every rule the agents follow has a gate that fails a commit, a
push, or a CI run when the rule breaks. A rule a script could check but
that names no gate is a defect. The framework is the one described in
`reference/framework.md`; read it before either mode.

Two modes: `setup` builds the framework in a repo that has none.
`refine` audits a repo that has it and proposes the next rules and gates
from what broke. Bare `gap-trap` with no keyword means `setup` when the
repo has no `AGENTS.project.md`, otherwise `refine`. A hand-written
`AGENTS.md` or `CLAUDE.md` on its own is input to setup, not a sign the
framework exists.

## Model gate

This skill runs on Opus or a more capable model (Opus 4.8 or newer, Opus
5, Fable, Mythos). Discovery decides which parts of a codebase get a
contract, and a wrong contract costs every later session. Your system
prompt names your model.

If it is Sonnet, Haiku, or anything below Opus, stop. Read nothing,
write nothing. Say exactly this and end the turn:

> gap-trap runs on Opus or a more capable model. You are on
> <model name>. Switch with `/model`, then run gap-trap again.

Do not dispatch Opus subagents from a smaller orchestrator, start "the
easy parts", or offer a lighter version.

## setup

1. **Discover.** Follow `reference/discovery.md`. It produces a plan
   file in your scratch directory: stack, commands, CI provider,
   contract candidates with real symbol names, the first domain facts
   from history (the revert probe runs at any commit count), and one
   row per rule found in an existing instruction file with where it
   goes and what gates it.
2. **Confirm once.** Show the plan as a short list: the contracts you
   will write (at most six), the gates you will add, the test and lint
   commands you found, the migrated-rules table, and where slop-mop
   goes. A build, type check, or
   lint that is already red is the first item: setup fixes only what
   its own gate files need (a missing type package, a lockfile) and
   records the rest as a ratchet count or an out-of-scope entry. Ask one
   round of questions, only about what discovery could not settle. Then
   proceed.
3. **Install slop-mop.** `git clone https://github.com/pliablepixels/slop-mop.git`
   into your scratch directory and copy `slop-mop/slop-mop` to
   `~/.claude/skills/slop-mop` (skip if present). It is not vendored into
   the repo; the project rule in `AGENTS.project.md` requires it.
4. **Write the instruction files** from `templates/`. `AGENTS.md` and
   `agents/generic/claude-workflows.md` are copied unchanged, with one
   exception: a rule whose gate cannot exist in this repo (I3's
   accessibility lint and C3's locales in a repo with no UI) gets its
   `Gate:` clause replaced by `Gate: n/a, no <thing> in this repo`.
   Nothing else in `AGENTS.md` changes. `AGENTS.project.md`,
   `CLAUDE.md`, and `agents/project/` are filled from the plan; drop the
   UI and end-to-end lines and `{{E2E_CMD}}` when the repo has no UI, and
   delete every placeholder you cannot fill with a verified value.
   Contracts name real symbols only. Existing instruction files
   (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`,
   `.github/copilot-instructions.md`, `CONTRIBUTING.md`) are migrated
   from the plan's migrated-rules table, one row at a time: a contract
   row becomes a contract block, a rule row becomes a project rule with
   its gate name or `Gate: review`, a playbook row goes verbatim into
   the named `agents/project/` file, a command row fills the
   verification block, and a duplicate or dropped row is left out. No
   rule is dropped silently; the confirm step showed the table. The
   old file is replaced by the template that owns its name, and
   `CONTRIBUTING.md` stays where it is. The user sees the diff.
5. **Write the gates** from `reference/gates.md`, in the repo's own test
   runner and CI provider: the instruction gate, proven red, the PR body
   check, the ratchet (always, seeded with the counters the repo
   supports: files over the C2 length, lint problems per rule when a
   linter runs, each contract Never clause that has violations today),
   and the mutation smoke when discovery named a risky module (auth, a
   parser, the API client); otherwise refine adds it after the first
   fix chain. The stack table there picks the reference: native ports
   for Node and Python, shell references that need only git, grep, and
   awk for every other language. Set the instruction gate's word budget
   at the current count plus half, rounded up to the next 500.
6. **Prove each gate red** with a scratch violation, remove the
   violation, run the repo's full test command, and commit one logical
   change per commit. Do not push unless asked.
7. **Report** what was written, the instruction word count against the
   budget, which contracts say `Gate: review` and why, and the one
   next step: run `gap-trap refine` after the first incident or in a
   month.

Instruction files are read by agents. Write them as terse statements
with IDs and gate names. Human-voice prose belongs in the repo's docs,
not in `AGENTS*.md` or `agents/`.

## refine

Follow `reference/refine.md`. It audits rules without gates, contract
names that no longer exist, and the commit history since the last
refine, and it proposes edits through the self-improvement protocol as
one PR. It removes rules with no incident behind them as readily as it
adds gates.

## Common mistakes

| Mistake | Fix |
|---|---|
| A contract with a guessed symbol name | Every name in a `Path:` line is greppable in the tree; the instruction gate fails otherwise |
| Writing ten contracts on day one | Start with the places that have one sanctioned path and a violation today; add the rest through refine |
| A gate that passed on first run | Prove it red with a scratch violation first; a gate that never failed proves nothing |
| Vendoring slop-mop into the repo | It installs per agent from its repo; the project rule requires it |
| Instruction prose polished for people | Agents read it. Statement, one-clause why, gate name |
| Skipping the model gate because the repo is small | Discovery quality is the deliverable; the gate is first for a reason |
