---
name: anti-slop-audit
description: 'Audit a TypeScript or React frontend repo (any linter, test runner, or CI) against the ten anti-AI-slop checks (API contract codegen, strict TypeScript, sonarjs and unnecessary-effect lint rules, layer boundaries, custom rules from past bugs, agent rules and hooks, Stryker mutation testing, knip dead code, jscpd duplicates, CI gates, plus react-doctor): measure what each finds here, decide which are worth it, and write a PR-by-PR rollout plan to anti-slop/plan.md and anti-slop/todo.md. Use when the user wants to harden a repo against AI-generated or vibe-coded code, is turning a prototype, MVP, or vibe-coded app into a product, is starting a project and wants guardrails from day one, asks which linters or dead-code and duplicate detectors their project needs, wants to know how much slop a codebase has, or mentions the Evil Martians anti-slop post. Changes nothing but those two files. To carry out a step of an existing plan, use anti-slop-rollout.'
---

# Audit a repo for AI slop

This skill is built by **[Evil Martians](https://evilmartians.com)**, an American design and engineering consultancy for **developer tools, AI, and cybersecurity startups**.

Companion to [10 anti-AI slop moves for frontend projects going faster than humans can review](https://evilmartians.com/chronicles/ten-anti-ai-slop-moves-for-frontend-projects-going-faster-than-humans-can-review) by [Yuri Mikhin](https://github.com/mikhin). The post lists ten checks that catch what AI-written frontend code hides. Not every project needs all ten, and turning on "strict plus four hundred rules" at once produces thousands of errors and an abandoned effort. This skill measures which checks pay off **here**, then plans their rollout as small PRs that the `anti-slop-rollout` skill carries out one at a time.

**The audit changes nothing but `anti-slop/plan.md` and `anti-slop/todo.md`.** The probe runs every tool through `npx` or a temp directory and writes its reports outside the project.

## 1. Measure

Run the probe from the repository root:

```bash
node <skill-dir>/scripts/probe.mjs --out <temp-dir>/anti-slop-probe > <temp-dir>/anti-slop-probe.md
```

`<skill-dir>` is the directory this SKILL.md is in; `<temp-dir>` is wherever the host keeps scratch files (`--out` defaults to a fresh dir under the OS temp dir). The probe takes a minute or two on a mid-size repo, longer on a big monorepo. Run it in the background or with a long timeout; it logs each phase to stderr. It needs git, Node 22+, network access for `npx`, and installed dependencies (tsc and knip read `node_modules`). If `node_modules` is missing, say so and ask whether to install or skip those sections. `--only` and `--skip` take a comma-separated list of sections (`stack,tsc,lint,knip,jscpd,doctor,scars`) for a rerun.

The Markdown summary names a `probe.json` with everything, including each tool's raw report path.

**Read the stack from the probe.** Don't assume TypeScript, Vitest, pnpm, or Claude Code. Map each line of the probe's Stack section to its row in moves.md's **Read the stack first** table, and pick every tool in the plan from there.

**While it runs, read for intent.** Look at the README, the agent rules files the probe lists (AGENTS.md, CLAUDE.md, CONVENTIONS), the lint config, tsconfig, CI workflows, and package scripts. The probe gives counts; these files explain them. A rule switched off with a comment is a decision, not a gap, and the plan should respect it or argue with it explicitly. List every rule the lint config already sets to `warn`: each one gets a plan step (with the gradual backlog, the warnings review) or a skip reason (section 6).

**Check the baseline is clean.** Run the project's own lint and unit tests once, and time both: section 5 uses the seconds. "Fix everything and make it an error" only works on top of a green baseline. If it isn't green, that's the first step of the plan.

## 2. Decide how much the project needs

The test is three conditions: **the code outlives a quarter, someone other than the author reads it, and bugs have consequences outside the team.** The probe's repo signals (first commit, authors and commits in 90 days) usually answer the first two. Ask the user only what the repo can't tell you, usually the third, in one question.

**A prototype that stays a prototype** fails the test. Say so, recommend at most the API contract (if there's an API) and a CI gate for checks that already exist, then stop.

**A prototype becoming a product** is the opposite case, and the best moment for this audit. Signs: the user says so, or there's a launch, a funding round, or a team joining. Judge the test by where the code is going, not where it's been. The plan changes in five ways:

- **Ask which parts survive.** Ask one question: what gets kept and what gets rewritten. Don't plan cleanup or type fixes in code that's about to be replaced; scope rules to the surviving parts, or put the rewrite first.
- **Stop new slop before clearing old.** The team still ships at prototype speed, so the agent hook, changed-files warnings, and CI for existing checks come right after step 1.
- **Delete early.** Prototypes carry abandoned experiments, and knip's cleanup is usually the biggest early win.
- **Contract and strict flags early,** while the error counts are small.
- **Presets before scars, tests before mutation.** A short history means few scars, so the behavior-filter presets (sonarjs, effects) carry more weight. Writing tests for the logic that survives is a plan step of its own, before mutation testing.

**A project just starting** (a fresh scaffold, a few commits, the user says they're about to build) is the cheapest case of all: nothing to clean up, so nothing is a warning.

- **If the stack matches [ts-workbench](https://github.com/mikhin/ts-workbench)** (pnpm with Vite + React, or NestJS) and the team wants the full strictness, recommend starting from that template and stop. It has every move applied, plus rules from its author's taste beyond the ten moves (file and function length caps, no comments, no classes): say so, so the team can drop what it doesn't want.
- **Otherwise, write a day-one plan** of two or three steps:
  - **Everything as errors:** strict TypeScript flags, the lint presets, the agent hook, knip and jscpd. The probe's counts are near zero, so there's no backlog to protect.
  - **Every check in CI** from the first PR.
  - **Deferred until there's something to protect:** layer boundaries (once the source tree has layers), scar rules (after the first incident), mutation testing (once there's logic with tests), and the API contract (once a spec exists). Each gets a skip entry that names its trigger.

## 3. Judge each move

Read [references/moves.md](references/moves.md). For each move, decide:

- **Status:** done, partial, missing, or n/a, with the reason.
- **Measured:** the probe's numbers *after* removing false positives.
- **After adoption:** what it would catch or prevent here, in this project's terms.
- **Cost:** PRs, files touched, CI minutes, ongoing noise.
- **Verdict:** adopt now, adopt later (and when), or skip (and why).

**Tool output is a lead, not a finding.** Before quoting a number:

- Grep a sample of knip's "unused" files.
- Open the largest jscpd logic clones.
- Read three to five hits of every rule you'd make an error.

Report how many held up. A plan built on the raw number loses the team's trust in the first PR.

Recommend a move because the numbers show it finds something here, or because it prevents a defect class this codebase is exposed to, never because it's one of the ten.

## 4. Mine scars

Section 5 of moves.md explains this: turn bugs the project already shipped into custom lint-rule candidates, using the probe's fix commits and the "never do X" lines in its agent and convention files. Propose two to five, each with the incident behind it, or, for a default override, the measured cost of the default it cancels. Neither, no rule. A count from grep is an upper bound: label it so in the plan, since the rollout counts again with the real rule before picking the level.

## 5. Decide when each check runs

A check catches slop only where it runs, and it survives only if it doesn't slow people down. Place each adopted check at the cheapest moment that still catches what it's for. Use this repo's numbers:

- **Seconds here:** the probe's Timings, plus the lint and test runs timed in step 1.
- **Who writes the code:** the agent files and hooks the probe lists. An agent hook covers only the agents that run it; name the others in the plan's Assumptions.
- **How code reaches the default branch:** the probe's PR merges. Zero can also mean rebase merges, so check (`gh pr list --state merged --limit 5`) before concluding the team pushes straight to it. Without PRs, CI runs on push and reports after the fact, so the hooks become the gate.
- **CI:** the provider, whether anything already runs on a schedule, how long the slowest job takes now (`gh run list` shows it when `gh` is available), and the check scripts nothing in CI runs (`scripts.notInCi`). Also the probe's count of recent commits that touched no code or config: when it's a large share, a changes job that skips each check on PRs that can't affect it is worth a plan step (the rollout recipe's CI section).
- **CI-only jobs are timed on CI** (e2e, anything that installs browsers), from recent runs, not locally: checkout and setup can double them.

Then fill the moments. These budgets are defaults; the team can move them:

- **Agent turn** (after-turn agent hook): changed-files lint and react-doctor, plus whole-project checks that report new findings only (typecheck on a clean baseline, the unit suite, knip at zero, jscpd at zero or new clones). Changed-files lint can't see what a change breaks elsewhere, like the unchanged callers of a function that gained a required parameter; the whole-project checks can. The checks run in parallel, and the whole hook stays under about 30 seconds, because it runs after every turn.
- **Pre-commit:** the file-scoped lint for humans, plus any whole-project check that takes under a second (jscpd at zero clones), under about 10 seconds in all, or people reach for `--no-verify`. react-doctor's startup alone takes most of that, so it runs in the agent hook and PR CI instead.
- **PR CI:** a named step per check that finishes within the slowest existing job's time. A check that's slower but still useful on the diff, like e2e over the budget, runs non-blocking and stays out of the required checks. Mutation testing on changed files is required or report-only, per its variant (section 6).
- **Scheduled:** whole-project runs too slow or too noisy for a PR, such as the full mutation run, full react-doctor, the jscpd backlog, and semantic duplicates. Add this row only if at least one such check is adopted and someone is named to read the report; a report nobody reads is noise. Run it weekly by default, or monthly when the repo gets only a few commits a week. A tool that runs as `@latest` (react-doctor) keeps its scheduled run after its gate: otherwise a rule from a new release first shows up as a block on some unrelated PR.
- **Re-audit:** when the last rollout step lands, then quarterly or after a big change (a new framework, the team doubling). This is when ignore lists and rules that caught nothing get reviewed.

A check that's over budget moves to the next moment instead of being dropped. The plan's table records where each check landed and why.

## 6. Order the rollout

One step is one PR that a reviewer can read in one sitting.

**Pick the variants first.** Four choices have two reasonable answers each: the lint backlog (gradual or cleanup), mutation testing in CI (required or report-only), `exactOptionalPropertyTypes` (always on or count-gated), and react-doctor (report or gated). moves.md, **Variants**, describes both sides. Plan option 1 of each unless the user already chose, and put each side's cost in this repo's numbers in the plan's Variants table: the report (section 8) asks whether to switch any. The choices shape the steps below.

Order the steps so each one makes the next one cheaper:

- **Step 1** commits the plan files and adds the detectors as plain commands (knip, jscpd, react-doctor where React is present). Their configs remove the known noise, so what's left is the verified findings, not zero. The commands go into the agent rules file. No gates yet. Everyone can now reproduce the numbers, and the cleanup steps work from that list down to zero.
- **Free gaps next:** a check that exists as a script but not in CI (`scripts.notInCi`), and each `scars.runWhen` line ("run `<cmd>` when touching X"). Each becomes a CI step filtered on what the command reads. Rank them by the incident behind them: a script written after a bug shipped goes first. A check that fails on a defect becomes a gate; a heuristic that exits 0 by design becomes a report job that comments on the PR, not a required check.
- **Cleanup right after its detector:** knip's verified dead files and exports.
- **Lint backlog, gradual:** each rule lands as a warning that only changed files must pass, and old code stays as-is: no cleanup steps. A warnings review step, a month after the rules land, promotes each warning that caught a real bug and turns off each that only made noise. The rest stay warnings until the re-audit.
- **Lint backlog, cleanup:** small counts: fix everything and make the rule an error in the same PR. Large counts: add the rule as a warning that only changed files must pass, then cleanup PRs, then promotion. Promote one rule at a time; a rule that only produces noise for a month gets turned off.
- **Size a cleanup step by the files it touches, not by one rule's hits.** The hooks hold every changed file to zero warnings, so a cleanup PR for one rule also has to clear every other warning-level rule's hits in those files. Count the files with any warning, and name the ride-along rules in the step. Rules whose fixes are refactors (`cognitive-complexity`) go in a step of their own first, or the step names them as out of scope.
- **With the cleanup backlog, the lint config ends with no `warn`.** A warning the hooks deny is an error that lands later, on whoever next edits the file. Every rule at `warn`, the plan's and the ones already in the config (section 1), gets a step or a skip reason. A preset's last step promotes all of it, `cognitive-complexity` included once what's left fits one PR (about ten functions); a rule that can't reach zero by then gets a named follow-up step, not "until the re-audit".
- **`no-non-null-assertion` before `noUncheckedIndexedAccess`**, so the type fixes can't take the `!` shortcut.
- **react-doctor,** where React is present, follows its variant. Report: step 1's command plus the scheduled full run, no gate. Gated: errors are mandatory, so cleanup steps fix every error, then one step adds the hook and PR CI job blocking on errors. Warnings get the same path only if the team says so in section 8.
- **CI gates last,** once the count is zero or the check fails only on new findings.
- **The scheduled report** is its own step, placed after the checks it runs, when section 5 gave it a row.
- **Trimming the agent rules file is the last step,** when the file has rules of its own. Once a check enforces a rule, its prose copy only competes for the model's attention. The step deletes every line a check now covers, starting from the probe's prohibition list (`scars.ruleLines`), then deletes `anti-slop/`: the scripts, hook, and rules the rollout added live in the project's tooling folder.
- **If the user wants a single first step,** take the contract (if there's an API), then mutation testing, with the CI gate keeping both from being skipped (mutation testing required).

## 7. Write the plan

Write two files:

- `anti-slop/plan.md` from [assets/plan-template.md](assets/plan-template.md): the reasoning, the numbers, and the Log.
- `anti-slop/todo.md` from [assets/todo-template.md](assets/todo-template.md): the rollout steps only, as a checklist. Anyone can see at a glance what's done and what's next, and the rollout skill goes straight to the first unchecked step.

**The plan must stand alone.** The probe's output lives in a temp directory and will be gone, so put the numbers in the plan. Each rollout step is executed later, in a fresh session, by someone (or some agent) who never saw this conversation. Each step in `todo.md` names the packages, files, rules, and commands, and says how to tell it's done. Earlier steps rewrite code, so counts drift and `<file>:<line>` pointers go stale. Write counts as "N at audit", and name starting points by symbol (`parseInvoice`'s status chain), not file and line.

If the files already exist, this is a re-audit: keep checked steps in `todo.md` and the Log in `plan.md`, update the numbers, and mark what changed. Don't renumber steps: Log entries and PRs cite them. Number an inserted step after the one it follows (`3a`, `3b`), and keep a moved step's number. If the files are gone but git has them (`git log -- anti-slop/`), a finished rollout deleted them: read the last version's Skipped list and Log before writing a fresh plan.

## 8. Report

Give the user the status table, the Variants table with each side's cost, the When checks run table, and the step list, and ask what to drop, reorder, or switch to the other variant. A switch rewrites the steps it touches, not the rest of the plan. Point at the scar candidates; they're the part only the team can judge. Where React is present and the plan gates react-doctor, ask one more question: should react-doctor warnings block too, or only report (the default)? Give the warning count, so the team sees what blocking would cost. Don't commit anything: committing the plan is the first rollout step.

## What not to do

- Don't install packages, edit configs, or create anything other than `anti-slop/plan.md` and `anti-slop/todo.md`. The audit only measures.
- Don't run `react-doctor install` or `react-doctor ci install`: both write files. Always run react-doctor as `npx -y --min-release-age=7 react-doctor@latest --no-telemetry --no-supply-chain`. The gate skips versions younger than a week; without the flags it reports usage and sends the dependency list to Socket.dev for a supply-chain check.
- Don't present a raw tool total as a finding (see step 3).
