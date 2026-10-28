---
name: anti-slop-rollout
description: 'Carry out the next step of an anti-AI-slop rollout plan (anti-slop/todo.md, with the reasoning in anti-slop/plan.md) as one pull request: add a single check in whatever stack the plan records (a strict TypeScript flag, sonarjs, unnecessary-effect, or test lint rules, layer boundaries, a custom lint rule from a past bug, an agent hook, Stryker mutation testing, knip and dead-file scripts, jscpd, react-doctor, a CI gate, a scheduled report, and the final trim of the agent rules file), fix or baseline what it finds, document its commands in the agent rules file, verify it, and open the PR. Use when the user says "next anti-slop step", "do step N of the plan", asks which rules in AGENTS.md or CLAUDE.md the linters now cover, or asks to set up knip, jscpd, react-doctor, Stryker, sonarjs, or boundaries the gradual way (warnings first, CI gate last) in a repo that has an anti-slop plan. Needs the plan from anti-slop-audit; without one, run the audit first.'
---

# Roll out one anti-slop step

This skill is built by **[Evil Martians](https://evilmartians.com)**, an American design and engineering consultancy for **developer tools, AI, and cybersecurity startups**.

Companion to [10 anti-AI slop moves for frontend projects going faster than humans can review](https://evilmartians.com/chronicles/ten-anti-ai-slop-moves-for-frontend-projects-going-faster-than-humans-can-review) by [Yuri Mikhin](https://github.com/mikhin). The `anti-slop-audit` skill wrote a plan of small PRs: the steps in `anti-slop/todo.md`, the reasoning in `anti-slop/plan.md`. This skill carries out **one step per run**.

One step is one PR because each one needs a human review. These checks exist to cut how much code people have to read, not to skip reading. Don't continue into the next step unless the user asks.

## 1. Load the plan

Read `anti-slop/todo.md`. If it doesn't exist, say so and offer to run `anti-slop-audit` first.

Take the step the user named, or else the first unchecked one. Check its "Depends on": if an earlier step's PR isn't merged yet, say so. Ask whether to wait or to branch from that PR. The rules-file trim has a third option: ship without it (recipes, **Trim the rules file**).

Then read `anti-slop/plan.md` for the context the step needs: its move's notes, the Assumptions, the **When checks run** row, the **Stack** (which tools this project uses), and the **Variants** (the plan's side of four choices: lint backlog, mutation testing in CI, `exactOptionalPropertyTypes`, react-doctor). A plan without a Stack section: read the stack from `package.json` and the lockfile. A plan without a Variants table predates it and was written for cleanup, report-only, count-gated, and gated.

## 2. Measure again

The plan's numbers are from the audit, and the code has moved since. Counts drift both ways, and an earlier refactor can move the step's starting point: find it by symbol. Rerun the relevant probe section from the sibling skill:

```bash
node <skill-dir>/../anti-slop-audit/scripts/probe.mjs --only <sections, comma-separated: tsc,lint,knip,jscpd,doctor, or scars for the rules-file trim>
```

`<skill-dir>` is the directory this SKILL.md is in. If the audit skill isn't installed next to it, run the tool from the recipe directly. Note the numbers: they go into the PR description and the Log in `plan.md`.

## 3. Branch

Start from the default branch, up to date (fetch first; if the network is down, branch from the local copy and say so in the report). Name the branch the way the project does (check AGENTS.md, CONTRIBUTING, recent branches), or `chore/anti-slop-<step-slug>` if nothing says.

If the working tree has uncommitted changes, they're the user's. Don't stash them or sweep them into the branch. Ask, or work in a `git worktree`. The one exception is an uncommitted `anti-slop/plan.md` and `anti-slop/todo.md` fresh from the audit: committing them is step 1's job, so carry them onto the branch.

## 4. Implement

Read [references/recipes.md](references/recipes.md): **Adapting to the stack**, **Conventions**, **Running often**, and the section for this step only. Wire the check at the moments the plan's **When checks run** table gives it: agent hook, pre-commit, CI, or the scheduled report.

`assets/` holds files to copy into the project. They're templates: adapt them to the project's aliases, globs, tools, and naming, and drop the parts that don't apply.

- `assets/scripts/` holds the detector scripts and the PR-comment helper for report jobs, `assets/lint-rules/` the project-rule template, and `assets/agent-check.sh` the agent hook.
- They outlive the rollout, so they go in the project's tooling folder, not in `anti-slop/` (recipes, **Where things go**). `anti-slop/` holds only the plan and the todo, and the last step deletes it.

Add packages with the project's package manager as devDependencies, at current versions. The plan step names them, and asking for the step is asking for them. If the project's rules require approval for new dependencies anyway, list them and confirm before adding.

**The plan and the recipe can disagree** on a mechanical detail (a file name, a script name, where commands go). The recipe wins unless the plan says why it differs. Note the deviation in the plan's Log.

**Follow the rollout discipline, on the plan's side of each variant:**

- **The rule level.** With the gradual backlog, a new rule lands as a warning that changed files must pass, and old code stays as-is. With cleanup, the count decides: small enough to fix in this PR, fix everything and make it an error; otherwise a warning, with cleanup steps after.
- **Fix findings properly.** No new `!`, `as any`, disable comments, or reason-less ignore entries to get a check green. A false positive gets a config-level ignore with a comment saying why. If a suppression is truly needed, it carries the reason.
- **One concern per PR.** If the fixes balloon (dozens of files, or risky logic), land the config with warnings now, and insert cleanup steps into `todo.md` for later PRs. Number them after the step they follow (`3a`, `3b`) instead of renumbering: Log entries and PRs cite step numbers. The hooks hold every changed file to zero warnings, so a cleanup for one rule also has to clear the other warning-level rules' hits in the files it touches. When those ride-along fixes balloon, the choice is the team's: fix them in the same PR, exempt that one rule in the hook's config with a reason, or commit with `--no-verify`. Ask, and record the choice in the Log. Never exempt silently.
- **Scores are diagnostics.** Never change code to move a react-doctor or mutation score.

## 5. Document

Add the **Conventions** section from recipes.md to the project's agent rules file the first time; later steps only add their commands to its list. Use AGENTS.md if the project has it, otherwise CLAUDE.md. Match the file's style and keep additions short. If the file already states in prose the rule this step's check now enforces, delete that line in the same PR: the check is the rule now. The plan's last step sweeps what's left.

## 6. Verify

- **New commands:** run each one and compare the result with the step's "Done when". Check that the output really comes from the tool: a script name that collides with a package manager built-in runs the built-in and exits 0.
- **Detectors:** prove each one finds something: plant a violation, see it reported, then remove the plant. If the hook auto-fixes (`--fix`), plant something it can't repair: it rewrites a `@ts-ignore` into `@ts-expect-error` or a `type` into an `interface`, and the plant vanishes. Plants that hold: a required parameter added to a function with unchanged callers (typecheck), `items[0].label` (`noUncheckedIndexedAccess`), a `!` (`no-non-null-assertion`), a nested ternary in a changed file (the sonarjs warnings), a failing assertion (tests), an unimported file and an unused export (knip), a stale mock, a copied module (jscpd), an effect that adds a listener without cleanup (react-doctor).
- **Refactor-heavy cleanups:** prove behavior parity against the base branch with a one-off measurement, not a committed harness. Replay recorded inputs through the old and new function side by side (import both, from a `git worktree` of the base branch and from the branch), or diff a production build against the base branch's with the noise masked: bundle hashes, generated ids, signed URLs, random seeds, build timestamps, nondeterministic ordering. Include one planted change to show the comparison can fail. Record the numbers in the Log; commit the harness only if asked.
- **Project lint rules:** the rule's test passes, and the rule fires on the code from before the incident's fix (`git show <sha>^:<file>`).
- **A new report job:** prove it on its own PR with a throwaway commit that trips the checker and can't ship (a draft, or a file the build excludes), so the PR's comment shows a real report. The PR description says to drop that commit before merge.
- **The rules-file trim:** each deleted line is listed in the PR next to the check that enforces it, and each gets a plant the check fails on. A rule at `error` can still miss what the line forbids (recipes, **Trim the rules file**).
- **The project's existing checks:** run the ones the change can affect (lint, typecheck, unit tests, build). If something fails that you can't fix within this step, report it with the output. Don't hide it.
- **What only a real PR shows:** whether a path filter or a changes job skips the job when it should, whether a required check reports its status, and whether a schedule runs (only after merge, from the default branch). A changes job can't show its skip on the PR that adds it: the workflow is a shared input, so every push runs everything; verify it on the next content-only PR. If the step touches any of these, list them in a short "Verify on this PR" note for the PR description.

## 7. Update the plan

Check the step off in `todo.md`. Append to the Log in `plan.md`: date, step, branch or PR, numbers before → after, which "Verify on this PR" items stayed unverified, and anything that changed the plan (a rule turned off as noise, a threshold moved, follow-up steps inserted into `todo.md`). The last step deletes `anti-slop/`, so its PR description carries what the Log entry would, plus every item still open anywhere in the Log: checks not yet verified on a real PR, settings changes not yet applied, scar candidates waiting for an incident, and the re-audit date.

## 8. Commit and open the PR

Commit in the project's message style (short and imperative if nothing says otherwise). Push, and open the PR with `gh pr create` (or the forge's CLI or API).

**The PR description says:**

- what the check catches (one sentence, from its move's notes in the plan)
- the numbers before → after
- what's deferred to later steps
- the files that still carry warning-level hits, since the next edit to each must clear them
- any tool version the step changed, with the old config's count under both versions
- how to run the check locally
- every branch-protection change the PR needs (new required jobs, renamed ones, a changes job): those settings live outside the repo
- the "Verify on this PR" note from step 6, if there is one

Link the plan step (in local mode, its path and number: `anti-slop/todo.md`, step N).

**Local mode:** if the user asked not to push or open PRs (testing, offline, reviewing first), stop after the commit. Print the PR title and description so they can open it later.

Then report the branch, the PR link (or "local only"), the numbers, and the next unchecked step in `todo.md`.
