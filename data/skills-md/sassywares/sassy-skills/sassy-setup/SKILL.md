---
name: sassy-setup
description: >-
  Detect a project's topology and wire it for the Sassy Skills suite: write
  .sassywares/config.yaml, check for the suite's skills and the sassy-agents
  subagents and install whichever is missing in user or project scope, and
  install the snapshot tooling in a multi-repo workspace.
  Use when asked to set up or configure a project, or to check an existing
  setup (`mode:check`).
argument-hint: "[path] [mode:init|check]"
disable-model-invocation: true
---

# Sassy Setup

**Outcome:** `.sassywares/config.yaml` at the project root matching the tree it describes, the skills installed in user or project scope and visible to the harness, the sassy-agents roster installed for the running harness, the snapshot tooling installed in `workspace` mode, and every file setup wrote committed — so the project is wired and the user is good to go in one run.

**Read `references/config.md` first.** It is the schema and the resolution rules; this skill only decides and writes.

**Never a repo by force.** Setup records topology, it does not change it. No `git init`, ever.

**Harness.** Loading another skill, dispatching an agent, and any command you hand the user follow `references/harness.md`; the agent wiring in step 5 uses its tables.

## Modes

| Mode | What it does |
|------|--------------|
| `init` (default) | Detect, ask, write, wire, verify, commit, report |
| `check` | Verify an existing setup against the tree and report |

The argument names the mode: `mode:init`, `mode:check` (or `--check`, the older spelling). A run with no mode that finds a `.sassywares/config.yaml` walking up is a **check** run — a folder that is already wired is verified, never rebuilt from detection.

A check run never edits the config and never rewrites the tree: it prints what `detect.sh --check` says, and its only possible write is step 8 committing setup-owned files that were already dirty. A fix is an `init` run, where each change is shown and approved first.

## Steps

1. **Resolve the start and the mode.** The path argument, else the working directory; the mode per above. On `check`, run steps 7 → 8 → 9 and stop.
2. **Detect.** Run `scripts/detect.sh --root <path>`. It prints a proposed config: topology (`repo`, `workspace`, `none`), the remote name, a probed base branch, and nested repos with their bases.
3. **Ask only what detection cannot answer.** Never re-ask what the tree already said.
   - **`workspace`** — the snapshot mirror: create a **private** GitHub repo, or connect an existing one? Creating it needs explicit approval and a named slug first.
   - **`none`** — confirm the intent: this folder is deliberately outside git, so commit, PR, and babysit refuse here.
   - **Artifacts** — offer the detected paths as the default; take overrides.
   - **Knowledge** — `knowledge.read` defaults to the solutions dir plus the concepts file. Ask whether there are extra folders to read (a hand-written `notes/learnings/`, a `docs/adr/`).
   - **Base map** — detection proposes `"*"` from the probed remote default. Ask where ordinary work branches from, and whether the default branch itself releases to another branch (a `staging: main` rung). Never write `main` as a guess. In `workspace` mode, show the `repos` map and get a yes on every row — a probed base is only the remote's default.
   - **`commit.branch`** — default `new`: the run cuts a branch before the first change and never commits on a base branch. Offer `current` for a repo that genuinely wants work committed where it stands, and say plainly that `current` lets a run commit onto its base branch and push it, with no PR (`pr.*` and `hooks.pr` are ignored). Under `mode:auto` with `current` on a base branch, ship pushes to that base with no gate.
   - **`pr.*`** — default `babysit: true`, `merge: false`, `delete_branch: false`. Say plainly that `merge: true` authorizes merging every babysat PR in this project without asking.
   - **Hooks** — offer, do not impose. Ask whether the project wants steps injected at `before_create`, `after_create`, `before_merge`, or `after_merge`, and under which head branch (`"*"` for all). Entries may carry args (`<skill> <args…>`); a hook skill's args are its own vocabulary. Leave them `[]` when there is nothing to add. **Never write a hook skill yourself** — hooks are project skills, and copying one of ours into that role is the fork this mechanism exists to prevent.
4. **Write the config.** Build the file from the proposal plus the answers. It is written **fully commented**: every key keeps a description and its allowed values, exactly as the detector emits them. Never strip those comments to save lines — for a teammate opening the file, the comments are the documentation. If a config already exists, show what changes and ask before writing — never silently overwrite. Keep every key; an unset key falls back to its documented default, so a short file is legal when nothing deviates.
5. **Wire the skills and the agents.** Both install the same way: if they are already there in either scope, report which and move on; if not, ask once where to install, recommending user scope.

   - **Skills.** The suite comes from upstream with the open `skills` CLI. Never copy skill files in by hand, never add the suite as a dependency.

     **Installed** means the `sassy-*` skills exist in the project scope (`.agents/skills/sassy-*`, pinned in `skills-lock.json`) or the user scope (`~/.agents/skills/`, plus `~/.claude/skills/` for Claude Code). If they do, report which scope and move on. If not, ask once where to install, recommending user scope:

     - **User scope** — every project on this machine, nothing committed, updated with `npx skills update -g`. Run `npx -y skills add sassywares/sassy-skills -g -y`, which writes `~/.agents/skills/sassy-*`, the `~/.claude/skills/sassy-*` links, and `~/.agents/.skill-lock.json`.
     - **Project scope** — only this project, pinned with it. Run `npx -y skills add sassywares/sassy-skills -y`, which writes `.agents/skills/sassy-*` (real files), per-agent links such as `.claude/skills/sassy-*`, and `skills-lock.json`. The vendored folders and the lock are the pin and join step 8's commit list, so a clone needs no network. Ignore `.claude/skills` only — it is a link created at install time. Create `.gitignore` only when there is none, and in `workspace` topology never touch the project's root `.gitignore` at all.

     A project that wants its own pin on a machine that already has the user-scope suite can install in project scope too — say that Claude Code prefers the user-scope copy, so the project's pin does not decide what Claude Code runs there.

     **Do not wire updates.** How and when the suite is refreshed is the user's or the project's decision, not setup's: no `skills:*` scripts, no `postinstall` edit. Mention the update command for the chosen scope and stop there. Note for yourself that `npx skills check` is an alias of `update` — it is not a validator, and running it here would silently move the pin.

   - **Write `.sassywares/README.md`** from `assets/sassywares-readme.md` when absent. Never overwrite it — it may carry project notes.
   - **Agents.** The skills dispatch four subagents by name — `scout`, `worker`, `reviewer`, `validator` — from [`sassy-agents`](https://github.com/sassywares/sassy-agents), which keeps one folder per harness. Use the row for the harness you are running in:

     | Harness | sassy-agents folder | User scope | Project scope |
     |---|---|---|---|
     | pi | `pi/` | `~/.pi/agent/agents/` | `.pi/agents/` |
     | Claude Code | `claude/` | `~/.claude/agents/` | `.claude/agents/` |

     A harness with no row has no folder in sassy-agents: say so, skip the agents, and name it in the report. Never translate another harness's folder by hand.

     **Installed** means all four `<name>.md` files exist in the user scope or the project scope. If they do, report which scope and move on. If any are missing, ask once where to install, recommending user scope:

     - **User scope** — every project on this machine, updated by `git pull`. Reuse the user's sassy-agents checkout if they have one; otherwise ask where to clone it (`git clone https://github.com/sassywares/sassy-agents.git <dir>`). Then run `<dir>/scripts/install.sh <folder>`, which symlinks the folder into the user scope and never overwrites a differing file.
     - **Project scope** — only this project, pinned with it. Shallow-clone into `/tmp/sassywares/<harness>/scratch/` (per `references/harness.md`), copy `<folder>/*.md` into the project scope directory, delete the clone. Never overwrite an existing agent file that differs: show it and ask. The copies join step 8's commit list.

   - **Tell the user to `/reload`** (or restart the harness). The skills and agents are invisible to the harness until it rescans.

6. **Install the workspace tooling, `workspace` only.** The snapshot plus the `branches` / `pull` / `checkout-bases` git helpers, and one `workspace:<script>` alias per script in the project's own manifest. Read `references/workspace.md` and follow it.
7. **Verify.** Run `scripts/detect.sh --root <path> --check`. It validates the config against the tree — topology and remotes, `base_map` shape and cycles, `repos` against each nested repo, hooks, artifacts paths, `knowledge`, `pr.*` booleans, `commit.branch`, any unknown key, and in `workspace` mode the installed snapshot's version — plus, for a project-scope install, the pin: every `.agents/skills/sassy-*` folder hashed against `skills-lock.json`, the lock's coverage both ways, and whether git carries the lock. A user-scope install has no pin here; the check notes the scope it found. Report every `drift:` line verbatim, or that the config matches the tree. Drift blocks step 8.

   Then check the skills and the agents exactly as step 5's **Installed** rules say, and report the scope each was found in or what is missing. A check run never installs them; a missing suite or roster is reported with the fix (`mode:init`), and it does not block step 8.
8. **Commit what setup owns.** `repo` topology only, and only when step 7 is clean. The file list is exactly what setup wrote or found unwritten:

   `.sassywares/config.yaml`, `.sassywares/README.md`, `.agents/skills/sassy-*` and `skills-lock.json` when the suite is in project scope, the project-scope agent files when step 5 copied them, and `.gitignore` when step 5 created it. Named files only — never `git add -A`, never `git add .`.

   Dispatch `sassy-commit` with that list and `branch:current`. The token is explicit, not this skill's default: wiring is a one-time bootstrap commit, and cutting a branch would leave the project configured but uncommitted until someone ships it. Name the branch it landed on, base branch included.

   **Nothing else** unless the user asks: a plan, a doc, a source file, or anything already dirty in the tree stays uncommitted, because setup's commit is not a place to launder work in progress. A user who says "commit my plan too" widens the list with the file they named — never with a sweep for it. On a `check` run this fires only when something setup owns is dirty: an uncommitted pin, a config edited since the last commit. Nothing dirty, nothing to commit.

   - **`workspace`** — nothing to commit: the root is not a repo, and `references/workspace.md` forbids running the snapshot here. Say the root config and the pin land with the project's next snapshot.
   - **`none`** — nothing to commit, deliberately.

9. **Report.** The config path, the topology, the resolved artifact and knowledge paths, where the skills are installed (scope) and where the agents are (scope and harness), or why either is not, the commit (hash and branch) or why there is none, and in `workspace` mode what was installed, with versions (`snapshot vN`, `workspace-git vN`), and the manifest the `workspace:*` aliases went into — naming it as created when there was no script surface to begin with. Remind: `/reload` so the harness rescans. Close with what is left over — at most dirt setup deliberately did not commit — and nothing else: a clean setup leaves the user good to go.

## Hard rules

| Rule | Requirement |
|------|-------------|
| No `git init` | Setup never turns a folder into a repo, and never does remote or ref surgery. The step 8 commit is its only git write. |
| Commit only what setup owns | The config, the setup README, the vendored `sassy-*` folders and `skills-lock.json` (project scope), the project-scope agent files, and a `.gitignore` setup created. Never a file the user wrote or the repo already had, unless they name it. |
| Verify before commit | A config that fails `--check` is reported, never committed. |
| Approval to create a remote | Creating the mirror repo needs an explicit yes and a named slug first. |
| No silent overwrite | An existing config or an existing `.sassywares/workspace/snapshot` is shown and asked about, never replaced blind. |
| Version is reported | Setup names the snapshot and `workspace-git` versions it installed; `--check` flags an installed copy older than the skill's. |
| Skills come from upstream | Install with `npx skills add`, `-g` for user scope; never hand-copy skill files or maintain the links yourself. |
| Agents come from sassy-agents | Only the running harness's folder, as-is: linked by `install.sh` (user scope) or copied verbatim (project scope). Never edit, merge, or overwrite a differing agent file without asking. |
| Never edit the manifest | No dependencies, no `postinstall`, no `skills:*` scripts. The one exception is step 6's `workspace:*` aliases in `workspace` topology: appended or corrected, never removed, and nothing else in the file touched. Setup installs the suite; the user or project decides how it updates. |
| Write boundary | Only `.sassywares/`, the skills and agent files step 5 installed in the scope the user chose, `skills-lock.json` (project scope), and one `.gitignore` line — and the project-scope part of that list is step 8's commit. Never `package.json` outside step 6's `workspace:*` aliases, never a root `.gitignore` in a workspace. Workspace git helpers land in `.sassywares/workspace/`, never in a project's `bin/`. |
| Detect, don't guess | An unknown base branch stays unknown and gets asked about. A probed value is reported as probed. |
| Comments are part of the file | Every key keeps its description and allowed values. A stripped config is an incomplete config. |
| Hooks are named, not written | Setup records hook skill names. Creating those skills is the project's work. |
| Repair is `check` | Run against an existing config, setup reports drift — it does not rewrite the file without approval. |

## What setup is not

Not a migration tool. A project already using another convention keeps its files; setup records where they already are. There is no rename step, and no fallback to `docs/` behind a configured path.

Not an updater. `check` reports a project pin that is stale or edited; it never moves it. Updating the suite is `npx skills update` (`-g` for user scope), which is the user's or project's decision and not setup's.
