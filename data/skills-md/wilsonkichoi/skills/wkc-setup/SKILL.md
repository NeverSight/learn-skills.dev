---
name: wkc-setup
description: Configure this project to use skills for AI-SDLC. Scaffolds the project layout, selects the tracker backend, and writes docs/dev-agents/config.md. Use when adopting these skills in a repository, switching its issue tracker, or updating an older config.
disable-model-invocation: true
---

# wkc-setup

- **What it does:** interviews the user about this repository, scaffolds `docs/dev-agents/`, and
  writes `docs/dev-agents/config.md`, which `wkc-tracker` reads.
- **When to use it:** once per repository, before `wkc-tracker`. Re-run it to change
  the tracker or bring an older config up to the current fields.
- **Dependencies:** `git`. `gh` for the GitHub tracker, the Linear MCP server for the Linear
  tracker, neither for the local tracker.
- **Input:** no invocation arguments. Context comes from the current repository and existing config,
  plus the user's answers to the interview. Invoke it without arguments to start or resume setup.
- **Output:** `docs/dev-agents/config.md`, `docs/dev-agents/rules/`, one reference line in the
  project's context file, and any one-time tracker setup.

Idempotent: safe to re-run; never overwrite existing files without asking.

## 1. Detect mode

Inspect the current directory to determine the state (read the files, don't assume):

- **Greenfield:** empty or near-empty (no source tree).
- **Brownfield:** existing code (source dirs, package manifests, git history).

Also read, before asking anything:

- An existing `docs/dev-agents/config.md`. It keeps the choices the project already made; the
  interview only fills what is missing.
- `git rev-parse --git-dir`, to know whether this is a git repository at all.
- `git remote -v`, to know whether there is a GitHub remote.
- `AGENTS.md` and `CLAUDE.md` at the root, to know which context file already exists.
- Any product-intent docs already present (`docs/PRD.md`, `docs/product/`, a spec in `AGENTS.md`).
- The project's test command, from its manifest (`package.json` scripts, `pyproject.toml`,
  `Makefile`).

**No git repository is the first thing to settle.** Offer `git init` before the interview starts.
Every backend ends at step 6 offering a commit, and the `github` backend cannot have a remote
without a repository to attach it to, so discovering this three sections later means unwinding the
interview. Ask it on its own, before Section A is on screen and never as one slot in a picker that
also carries the interview: Section A's GitHub check needs the repository to exist already.

## 2. Interview

Summarise what's present and what's missing. Then take the sections in order. One section, one
answer, then the next.

Give a one-line explainer only when the choice genuinely branches, and skip a section entirely when
step 1 already settled it.

**Ask, then stop.** A question is the last thing in its turn: no tool call after it, no work while
it is outstanding. A harness that is still working cannot take a plain reply.

**Make it cheap to answer.** Number the options, put the recommended one first, and say a digit is
enough. Use the harness's own picker where it has one; most have none, and numbered text is the
right answer there rather than a fallback to apologise for. Never ask for a path already on screen:
show it and take a bare yes.

**A multi-question picker does not reorder the interview.** Claude Code's takes four in one call,
which asks one section faster and never puts Sections A to D on screen together. Section A and every
prerequisite in its table are settled before Section B appears, on every harness: that answer
decides whether the backend works at all, and the sections after it are wasted if it does not. Batch
only questions from one section whose answers cannot change each other.

**Section A: Issue tracker.**

> Explainer: where issues live for this repo. Every other skill reads and writes them through
> `wkc-tracker`. Pick the place you actually track work.

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **Linear**: issues live in linear.app (uses the Linear MCP server). Ask for the team key and the
  project name; both go in the config.
- **Local markdown**: issues live as files under `docs/dev-agents/issues/` in this repo (good for
  solo projects or repos without a remote). One session at a time: an assignment made on a branch is
  invisible from `main` until that branch merges.
- **Other** (Jira, GitLab, etc.): ask the user to describe the workflow in one paragraph; record it
  as freeform text in the config body and set `issue_tracker: other`

**Settle the backend's prerequisites here, before Section B.** A missing prerequisite is a question
to ask now, not a fact to report at the end of the run. The user just chose this backend and is
sitting right there; carrying the problem to step 5 means they answer three more sections without
knowing whether the first one will work.

| Backend | Check | When it is missing |
|---|---|---|
| `github` | `gh auth status`, and a GitHub remote in `git remote -v` | Ask which repository, and offer both answers: an existing one is `git remote add origin <url>`, a new one is `gh repo create <name> --private --source=. --remote=origin`. Creating a repository is the user's call, so offer it and wait for an answer. |
| `linear` | the Linear MCP server answers `list_teams`, and the chosen team has the seven statuses below | No server: stop, say how to connect it, and write no Linear fields into the config until it answers. A missing status: see below. |
| `local` | nothing | |

**Linear statuses.** Statuses are per team and shared by every project in it. Read the chosen
team's with `list_issue_statuses`. Seven are required, each with the category shown:

| Required status | Category |
|---|---|
| Backlog | `backlog` |
| Todo | `unstarted` |
| In Progress | `started` |
| In Review | `started` |
| Done | `completed` |
| Canceled | `canceled` |
| Duplicate | `duplicate` |

**Expect In Review to be missing.** A team created from Linear's default template has six
statuses and no In Review, so this is the ordinary first run rather than an edge case. Say so
plainly instead of treating it as the user having done something wrong.

**A missing status is a question now.** There is no MCP tool that creates or renames a status, so
name exactly what to add in the team's settings, under which category, and end the turn asking the
user to reply once it is there. Read the statuses again on the reply. Section B waits until all
seven exist, and no Linear field goes into the config before then. Do not invent a mapping onto
whatever the team happens to have: a ticket written to the wrong status lands where nobody is looking.

**An extra status is a warning, not a stop.** Report it loudly, by name and category, and say that
tickets parked there are invisible to the frontier and will be reported as unmapped. Then write it
into the config body under **Tracker notes**, so it is a decision the user can come back to with
the AI rather than something they have to remember.

Write the resolved `OWNER/REPO`, or the resolved team and project, into the config. Never record an
intention to set one up later.

**Section B: Product-intent documents.** Where the requirements, the spec, and the roadmap live,
so later skills read the right files. Defaults are `docs/dev-agents/PRD.md`, `docs/dev-agents/SPEC.md`, and
`docs/dev-agents/ROADMAP.md`. Where `AGENTS.md` or `CLAUDE.md` is already the doc, point the field at it.

**Section C: Context file.** The project's entry point for coding agents. Default `AGENTS.md`,
or `CLAUDE.md` for a deliberately Claude-Code-only project. A project with a convention keeps it:
point `context_file` at the file every harness ultimately reaches, and never invert that.

**Section D: Test command.** Confirm the command inferred in step 1, or ask for it. It is what
later skills run before handing work back. A project with no tests leaves `test_command` out.

## 3. Scaffold

Everything the dev skills own lives under `docs/dev-agents/`; the project owns everything else.
Create only what is missing:

```
docs/dev-agents/
docs/dev-agents/config.md             # entry point on how to use these skills for AI-SDLC
docs/dev-agents/rules/                # promoted learnings, one file per rule
docs/dev-agents/issues/               # only when issue_tracker: local
```

Add `docs/dev-agents/rules/.gitkeep` so git tracks the directory before the first rule lands.

Do not create empty `PRD.md`, `SPEC.md`, or `ROADMAP.md`, and do not reverse-engineer a spec from
existing code. Their paths are recorded in the config; `wkc-research`, `wkc-architect`, and
`wkc-plan` write them when the work needs them.

**Template:** write `docs/dev-agents/config.md` from
[config-template.md](./config-template.md), dropping the fields that do not apply. Every value comes
from the interview or from step 1. Never guess a path into configuration.

**Existing projects:** an existing `config.md` keeps the choices the project already made. Add the
fields it is missing and report what changed; do not rewrite the body.

**Ownership rule:** the project owns `AGENTS.md` and `CLAUDE.md`. `wkc-setup` adds at most the step 4
reference line and never moves, consolidates, or rewrites what is already there. `rules_dir`
defaults to `docs/dev-agents/rules/`, and a project with its own convention may point it elsewhere,
such as `.claude/rules/`, which Claude Code auto-loads. Never migrate rule files uninvited.

## 4. Add the reference line

Add one line to the configured `context_file` so every session loads the dev config:

```
Read dev workflow for AI-SDLC from docs/dev-agents/config.md
```

Skip this step when the line is already there; a re-run must not add a second copy. Brownfield:
append it and touch nothing else. Greenfield with no context file at all: create a lean
one (under 50 lines) naming the project, the tracker backend, and the product-doc paths, with the
reference line at the end.

Claude Code does not auto-load `AGENTS.md`. When `context_file: AGENTS.md` and Claude Code is or
may be in use, also ensure `CLAUDE.md` contains an `@AGENTS.md` import line: create a one-line
`CLAUDE.md` when none exists, append the line when one exists, and never replace an existing body.

## 5. Tracker setup

One-time work for the chosen backend. Report what you did; do not treat a failure here as a reason
to abandon the rest of setup.

- **github:** the remote and `gh auth status` were settled in Section A. Create the four status
  labels with `gh label create`, skipping any that already exist: `backlog`, `ready`,
  `in-progress`, `in-review`. There is no label for `done`, `cancel`, or `duplicate`; those three
  are GitHub close reasons, which is what `wkc-tracker` reads and writes. If the authenticated user
  cannot write to the repository, create nothing and report the exact commands a maintainer needs
  to run.
- **linear:** the MCP connection and the team's statuses were settled in Section A. Nothing else
  to set up.
- **local:** create `docs/dev-agents/issues/.gitkeep`.
- **other:** nothing to set up. The workflow the user described is the contract.

## 6. Report

Offer to commit the scaffold and config. In a fresh repo this creates the root commit that later
task branches need.

Then summarize: mode, tracker backend, files created, one-time tracker setup performed, and
anything the user still has to do themselves.

Next step: confirm the backend responds with `wkc-tracker list`.
