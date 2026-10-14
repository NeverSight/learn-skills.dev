---
name: repo-skills
description: >-
  Select and install a small, reputable set of agent skills for a repository.
  Use when setting up repo skills or auditing skill fit, duplication, and
  conflicts. Inspect the actual stack and existing installations, recommend
  ponytail and git-commit as the baseline, and add specialists only for
  demonstrated needs. Install only within an explicitly approved scope.
---

# Repo Skills

Equip the repo, not every possible future task. This skill selects capability;
it does not choose product architecture, run development, or replace Harness.

## Inspect

1. Read applicable instructions, git status, manifests/lockfiles, workspace
   packages, and relevant tool configuration. Identify stack versions and the
   requested work; do not infer React, Expo, or Supabase from incidental text.
2. Inventory repo-local and global skills, including native agent locations,
   symlinks, bundled skills, and `skills-lock.json` when present. The CLI lists
   project skills by default; `npx skills list -g` lists global skills.
3. Reuse an adequate existing skill, regardless of install scope. Do not create
   another copy just to make every repo look alike. Check names AND behavior:
   different names can still prescribe the same workflow.

Read the [curated sources](references/curated-skills.md) for stack candidates.
Do not read every external skill or run a broad ecosystem search on each setup.

## Select

- Baseline: `ponytail` for smallest-complete-change discipline and `git-commit`
  for user-requested commits. Existing copies satisfy this baseline. Installation
  does not activate a session mode or authorize committing.
- Add domain guidance only for an observed stack or concrete upcoming task.
  React web and React Native are separate targets; monorepos may need both.
- Inspect the candidate's current `SKILL.md` and relevant referenced workflows.
  Check source ownership, exact name, compatible versions, dependencies,
  instruction precedence, broad triggers, hooks, and side effects.
- Prefer official maintainers and established sources with credible adoption.
  Use current skills.sh installs and GitHub maintenance/reputation as supporting
  signals, not a security guarantee. Do not invent counts or rely on rank alone.
- For a demonstrated gap outside the catalog, use a bounded
  `npx skills find "<capability>" --owner <known-owner>` search, then inspect the
  source. If trust or network evidence is unavailable, label it unverified;
  do not substitute an unknown mirror or silently install it.
- Harness owns task state, documentation routes, handoff, and verification.
  Specialists advise within that scope. Do not add competing intake, planning,
  docs-writing, commit, review, or orchestration bundles by default.
- Preserve repository rules and accepted decisions. A rule that demands a new
  dependency, experimental runtime, wider refactor, or unsafe command is not
  permission to make that change. Report conflicts; do not silently rewrite
  installed skills or repository policy to hide them.
- Choose one primary browser automation workflow. `agent-browser` is a candidate
  for real browser work, not a reason to replace an adequate existing tool.
- `caveman` is explicit opt-in voice only, not a baseline or a docs style.

## Propose and install

Report inline: evidence for the stack, reused baseline, each selected skill's
source and purpose, skipped duplicates/conflicts, commands, and prerequisites.
Do not create a skill registry, report file, setup script, or mandatory task.

When installation is requested, use the Skills CLI defaults in the current repo.
Do not ask the user to choose an agent/CLI or add `--agent`; default skill
directories can be shared across agents, not agent-exclusive. Do not add `-g`,
`--all`, or wildcards unless requested. A recommendation-only request still
does not authorize installation, and CLI prompts are not a safety boundary.

1. In the current repo, run `npx skills add <source> --list` to confirm names
   without installing. Search indexes and curated names may be stale.
2. Read and review the selected source before installation. Pause on unexpected
   changes, incompatible prerequisites, or conflicts. If a name disappeared,
   propose its verified replacement rather than guessing an alias.
3. Run `npx skills add <source> --skill <exact-name>` for the requested selection,
   using default installation behavior; no extra agent-selection approval.
   Never execute unresolved placeholders. No automatic bundle updates/removals.
4. Verify the installed path and git/lockfile changes; report what changed.
   Do not overwrite a customized skill without approval or delete unrelated
   installations.

Skill instructions and runtime tools are different installations. Installing
`agent-browser` guidance does not authorize browser binaries; Expo/Supabase
skills do not authorize SDK upgrades, credentials, MCP setup, telemetry, database
writes, builds, deployment, or submissions. Obtain separate approval for those
operations. Never put skill installation in `init.sh` or verification commands.

If only advice was requested, stop after the proposal. If installation fails,
report the failure and partial state; do not claim setup succeeded or escalate
to another source/global scope automatically.
