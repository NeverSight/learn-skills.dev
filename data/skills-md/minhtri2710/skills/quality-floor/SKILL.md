---
name: quality-floor
description: Write a project's quality bar as CONSTRAINTS.md with enforced commands, and guard diffs against moves that quietly lower it. Use when the user asks to set up constraints, quality gates, or standards, or when agents keep suppressing checks, skipping tests, or editing thresholds to reach green. Do not use when CONSTRAINTS.md exists and is not being changed; read and follow it.
---

# Quality Floor

Agents take the cheapest road to a green check. A bar that lives only in prose
erodes one suppression at a time, so record this project's bar with the command
that produces each verdict, and check every diff for moves that lower it.
Tightening the bar is silent; loosening it is loud.

## 1. Detect

Read the manifests, test runner, linters and their configs, CI workflows, current
coverage output, and agent instruction files before asking anything. Report what
exists as a short summary the user can scan before the first question.

## 2. Ask four questions

Only with the user present; in a non-interactive run, install the floor alone,
say so, and leave the rest for the user. Ask one round, each question with a
default, so "not sure" is a complete answer:

1. Which dimensions beyond the floor to enforce: coverage of changed lines,
   security scanning, performance budgets, accessibility, architecture boundaries.
   Default: the ones with a tool already installed, plus secrets and dependency
   scanning. Say that performance and accessibility need a running URL and
   boundaries need a rules file. Offer two more dimensions, never as a default,
   because each needs a baseline file and runs only in CI: dead code (functions the
   shipped entry point cannot reach with tests excluded, compared both ways against
   an allow file whose every row carries a reason) and uncovered guards (refusal
   branches no test enters, read from the coverage of every test lane merged,
   compared both ways against a baseline). Either enters the project only when the
   user selects it.
2. Block or report when a check fails mid-task. Default: block on the floor, report
   the rest until each dimension has passed once on the current tree.
3. Target numbers, or measure today and hold. Default: measure and hold.
4. Slowest acceptable check before work is handed back. Default: about 90 seconds
   at task end, unlimited in CI.

## 3. Write CONSTRAINTS.md

Use [references/constraints-template.md](references/constraints-template.md) at the
repository root. Every numbered row names the command that produces its verdict and
a bound written as `>=` or `<=`; a number without a command is an aspiration, not a
constraint. Give each number its reason. Where no target exists, record today's
measured value as the bound and refuse regression; a target the tree fails today
stays out until there is a plan to meet it. When the user agrees, add one line to
the agent instruction file: `Read CONSTRAINTS.md before writing code; change it
only in a commit of its own.`

## 4. Install and wire

For each chosen dimension, install the de facto tool from the template's tool table
rather than a hand-rolled checker (the security-setup skill chooses the Secrets,
Dependencies, and Code-security tools), and mirror the commands in the project's own
scripts at three costs: after an edit (seconds, changed files), at task end (under
the agreed budget, diff-scoped), and in CI (everything). `CONSTRAINTS.md` is the
source of truth; the scripts follow it. Run secret scanners with redaction so a
matched value never reaches a transcript. Scope expensive tools (mutation testing,
static analysis) to changed files, and read the coverage report the suite already
writes instead of running the suite twice. When a dimension cannot run for this
project (no URL for a library or CLI), drop it and say why.

Prove each guard bites before trusting it: run it green, deliberately violate one
rule, confirm it fails naming that rule, revert, and run it green again. A guard
that was never seen red is an assumption.

At least one enforced constraint must be external — a vulnerability database, a
WCAG engine, a real browser measurement — because the project's own tests are the
one check the same agent can write to pass.

## 5. Guard the diff

Run the guard from the target repository at task end and in CI:

```bash
python3 <this-skill>/scripts/floor_guard.py --base origin/main
```

It compares the working tree, including untracked files, with the merge base and
reads Git paths unquoted so non-ASCII and spaced names are matched as written.
`scripts/floor_guard.py` defines every rule it flags and every coverage and lint
config it watches. It prints rule and `path:line` only. Exit `0` is clean, `1` is a
violation, `2` means it could not run and never counts as clean.

Each flag is resolved by fixing the code, or by the user accepting an exception
row `| E<n> | rule or * | path glob | reason | removal condition |`, which
suppresses matching findings from then on. Review also rejects a `CONSTRAINTS.md`
change in the same commit as the feature it would let pass.

Done means `CONSTRAINTS.md` exists with a reason for every number, every enforced
row has a command that runs today, the floor guard exits `0` on the current tree,
and at least one constraint is external.
