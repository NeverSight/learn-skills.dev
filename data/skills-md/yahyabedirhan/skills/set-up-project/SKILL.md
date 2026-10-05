---
name: set-up-project
description: Set up or audit a project for coding agents - the machine checked first with set-up-machine, AGENTS.md as the one rules file with CLAUDE.md pointing at it, the issue tracker, triage labels and domain docs, the folder standard's .gitignore, and project harness files kept allow-only. Use for a new or existing project, to audit a project's agent setup, or when a skill finds no issue tracker configured.
---

# Set up project

Scaffold and audit the per-repo configuration the skills assume:

- **Rules file**: `AGENTS.md`, which every harness reads. `CLAUDE.md` is either the single line `@AGENTS.md` or a symlink to `AGENTS.md`. Claude Code skips a project's `AGENTS.md` when a `CLAUDE.md` exists, and both of those forms give it the same text.
- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them
- **Folder standard**: the `.gitignore` lines of [orchestrating/folder-standard.md](../orchestrating/folder-standard.md)
- **Allow-only project permissions**: the global rules are the machine's safety rails, and a project's own harness files only add convenience. The **audit** flags every project file that weakens a global rule.

You explore, present what you found, confirm with the user, then write. Running it again is the **audit**.

## Process

### 1. Check the machine

Run **set-up-machine**'s verify script, `python3 <set-up-machine skill>/scripts/verify.py` (the skill is installed beside this one). A pass is exit code 0. That means the `rules` line says `ok` and no `hook` line says `FAIL`. A `codex` line that says `differs`, `same`, `stricter`, or `skipped` is not a failure. `differs` is what the script prints for a row Codex can't express, and it still exits 0 with `rules ok`. When the exit code is not 0, run the **set-up-machine** skill first, then come back. Done when verify exits 0.

### 2. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` or `## Environment defaults` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root, and any `CONTEXT.md` or `CONTEXT-MAP.md` in the repo: the domain docs' old names, which the skills no longer read
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.efforts/`: a sign that a local-markdown issue tracker is already in use
- `docs/assets/`: the folder standard's old image folder
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.
- A tool the project's own docs require for a role skills name (a worktree tool in a `docs/worktrees.md`, a session host its scripts assume). This decides whether Section D runs.

### 3. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo and no old `CONTEXT.md` or `CONTEXT-MAP.md`, Section D when the project names no tool for a role).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.efforts/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.efforts/<effort>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

When exploration found an old `CONTEXT.md` or `CONTEXT-MAP.md`, propose renaming each with `git mv`, so its history follows it: `git mv CONTEXT.md GLOSSARY.md`, `git mv CONTEXT-MAP.md GLOSSARY-MAP.md`, and the same for each per-context `CONTEXT.md`. Where the new name already exists, `git mv` refuses: propose merging the old file into the new one instead, and ask which wins where they disagree. Also propose updating the map's links and any other file that names the old files; the drafts of `AGENTS.md` and `docs/agents/domain.md` already use the new names.

When exploration found a `docs/assets/` folder, propose moving each topic with `git mv`, as the folder standard's *Migration from older layouts* says: images the project ships or shows to `assets/images/<topic>/`, screenshots to `assets/screenshots/<topic>/`, and each relative link to them updated.

**Section D: Project environment defaults.** Recommend **none**. Ask only when exploration found a tool the project requires for a role: then propose an `## Environment defaults` row for it, which overrides the user's global row for this project. [agents-md.md](agents-md.md), *Environment defaults*, says what may go there.

### 4. Confirm and write

Show the user a draft of:

- `AGENTS.md`: new from [agents-md.md](agents-md.md), or the existing one with the `## Agent skills` block and any `## Environment defaults` rows added, and each line of an existing `CLAUDE.md` moved into it
- `CLAUDE.md`: the single line `@AGENTS.md`, or an existing symlink to `AGENTS.md` left as it is. Claude Code skips a project's `AGENTS.md` when a `CLAUDE.md` exists, and both forms give it the same text.
- `.gitignore`: `.scratch/` and `.claude/worktrees/`, each only where it's missing
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)
- Each rename or merge of an old `CONTEXT.md` or `CONTEXT-MAP.md`, and the edits to the files that name them, when Section C proposed them
- Each move out of `docs/assets/`, and the links it updates, when proposed

Let them edit, then take one approval for all of it. Then write:

1. Edit `AGENTS.md`, never `CLAUDE.md`. If an `## Agent skills` block already exists, update its contents in place rather than appending a duplicate, and keep the user's edits around it. Include the `### Triage labels` sub-block only when `triage` is installed and Section B ran.
2. Leave `CLAUDE.md` holding `@AGENTS.md` alone (a `CLAUDE.md` that is a symlink to `AGENTS.md` is fine as it is), and add the missing `.gitignore` lines.
3. Write the docs files using the seed templates in this skill folder as a starting point:
   - [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
   - [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
   - [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
   - [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
   - [domain.md](./domain.md): domain doc consumer rules + layout

   For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

   Give every `docs/agents/issue-tracker.md` the templates' `## Title prefixes` section, so each skill that creates an issue titles it the same way. Seed its semantic list from the areas the project's open issue titles already name, one line each with what the area covers.
4. Run each approved rename or merge of an old `CONTEXT.md` or `CONTEXT-MAP.md`, then update the files that named it.
5. Run each approved move out of `docs/assets/`, then update the links to it.

Done when every approved change is made.

### 5. Audit

Read every harness file the project holds, from the root down, against **set-up-machine**'s `rules.json`, whether or not that harness is set up on this machine: `.claude/settings.json` and `settings.local.json`, `.cursor/cli.json`, `opencode.json(c)` and `.opencode/`, `.codex/config.toml`. [references/project-files.md](references/project-files.md) says what each harness lets a project file do to a global rule, and how to judge an entry. Report each finding as:

- `weakens`: a global rule no longer holds as the machine sets it, in some harness. Explain which and why, and propose the fix: remove the entry, or narrow it to the project's own commands. The file is the project's, so change it only on the user's approval.
- `overlaps`: an allow that covers a rule's command while the rule still holds. Propose narrowing it.
- `extra` (a project deny or ask) and `gap` (what you can't judge): name each.

Also report each old `CONTEXT.md` or `CONTEXT-MAP.md` still in the repo, with the rename Section C proposes for it. Report a `docs/agents/issue-tracker.md` that has no `## Title prefixes` section, and propose the section step 3 writes.

The audit passes with no `weakens`. Done when it passes, or the user has chosen to keep a `weakens` entry: then it stays failed, and the report names that entry.

### 6. Done

Tell the user the setup is complete, what the audit found, and which skills will now read from these files. Mention they can edit `AGENTS.md` and `docs/agents/*.md` directly later; re-running this skill audits the project again, and switches issue trackers when they want to. Leave the commit to the user or the skill that called this one.
