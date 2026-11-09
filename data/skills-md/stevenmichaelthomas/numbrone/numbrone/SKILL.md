---
name: numbrone
description: Set up a "chief of staff" workflow on herdr. One chief agent routes requests to a manager agent per project, and managers run workers in git worktrees and herdr tabs, all in parallel. Use when the user asks to set up numbrone, a chief of staff or multi-project agent workflow on herdr, or to add a project to an existing numbrone setup.
---

# numbrone setup

You are setting up a workflow where:

- the **chief of staff** (an agent in the numbrone home folder) takes the user's requests, works out
  which project each belongs to, and delegates;
- each project has a **manager** agent in its own herdr workspace (`numbrone/<project>`);
- managers answer small things themselves and spawn **workers** for code changes. Each worker
  gets its own git worktree, its own tab in the project's workspace, and its own branch;
- workers report to their manager, and managers report to the chief;
- a daily Markdown work log records outcomes and decisions across all teams, for audits and retros;
- the chief builds up the user's context over time in `knowledge/`, and uses it to delegate and judge work.

All the mechanics live in one script, `scripts/numbrone` in this skill's directory. Run it with no
arguments to see its commands. Do the steps below in order. Keep the user informed in short lines.

## 1. Check prerequisites

Run these checks and fix or report anything missing before continuing:

```bash
test "${HERDR_ENV:-}" = 1 && echo "inside herdr"   # must be inside a herdr pane
herdr status                                       # server must be running
command -v git jq
herdr integration status | grep -E '^claude:'      # or the agent the user wants to use
```

- Not inside herdr: tell the user to install herdr (`curl -fsSL https://herdr.dev/install.sh | sh`),
  run `herdr`, start their agent in a pane, and run this skill again. Then stop.
- `jq` missing: suggest `brew install jq` or `apt install jq`.
- Integration not installed: offer `herdr integration install claude` (or their agent's kind).
  Ask before running it, because it writes to the agent's configuration.

## 2. Create the numbrone home folder

Ask where the numbrone home folder should live (default `~/.numbrone`). Then run:

```bash
bash <this skill's directory>/scripts/numbrone init <numbrone-home>
```

This creates `bin/numbrone`, `roles/`, `tasks/`, `projects/`, `log/` (the work log), `knowledge/`, `settings.sh`,
`projects.json`, and `CLAUDE.md` (the chief's instructions, with an `AGENTS.md` symlink for other
agents). Running it again upgrades the script and leaves everything the user may have edited alone
(`CLAUDE.md`, `roles/`, `settings.sh`, `projects.json`). From here on, use `<numbrone-home>/bin/numbrone`.

## 3. Choose the projects

Ask the user which local projects numbrone should manage. Accept either a list of paths or a parent
folder. For a parent folder, list the git repositories in it and let the user choose:

```bash
find <folder> -maxdepth 3 -name .git -prune | sed 's|/.git$||'
```

Give each project a short name: lowercase, dashes, at most 24 characters, starting with a letter
(usually the folder name). Each project must be a git repository.

## 4. Build context for each project

For each project, read enough to route requests to it accurately: README, CLAUDE.md/AGENTS.md,
package manifests (package.json, pyproject.toml, Cargo.toml, go.mod, ...), the top-level layout,
and `git log --oneline -20`. With more than three projects, use one parallel subagent per project.

Write `<numbrone-home>/projects/<name>/context.md` in this shape:

```markdown
# <name>
<one paragraph: what this project is and who it is for>

## Stack
## Layout          <!-- the directories that matter -->
## Commands        <!-- install, development server, test, lint, build -->
## Conventions     <!-- branching, commit style, anything a contributor must know -->
## Route here      <!-- kinds of requests that belong to this project, plus keywords -->
## Not here        <!-- things that sound related but belong to another project -->
## Watch           <!-- sources this project's manager checks on a loop (filled in step 5) -->
```

Then register the project with a one-line summary the chief can route on:

```bash
<numbrone-home>/bin/numbrone add <name> <path> "<one-line summary>"
```

Show the user the list (`numbrone projects`) and ask whether the summaries are right.

## 5. Inputs to watch (optional)

The user isn't the only source of work. The chief and each manager can check sources on a
loop and turn new items into tasks: Linear tickets, Sentry errors, Datadog alerts, GitHub
issues, and so on. Ask the user whether they want any, and at which level:

- **Chief**: sources that span projects (a Linear team, an org's GitHub issues). The chief
  routes each new item to the right project. Add one line per source under **Watch** at the
  end of `<numbrone-home>/CLAUDE.md`.
- **Manager**: sources owned by one project (that service's Sentry project, its Datadog
  monitors). Add one line per source under **Watch** in that project's `context.md`.

Each line says what to check, how to filter it, and how often, for example
`- Sentry: new unresolved issues in project "api", every 15 minutes`.

Agents read sources through MCP connectors or CLIs (such as `gh`) available to the agent. Check
that each source is reachable from this session, and tell the user which ones aren't connected
yet. Agents set up their loops when they start (in Claude Code, with `/loop`).

## 6. Seed the chief's knowledge (optional)

The chief gets better the more it knows about the user's world. Offer a short interview of three
or four questions, and skip anything the user doesn't want to answer:

- What are you working toward right now? What matters most this month?
- Anything that spans projects that the chief should know: customers, people, constraints?
- What does good work look like to you, and what makes you send work back?

Write the answers into topic files in `<numbrone-home>/knowledge/` (for example `goals.md`,
`standards.md`) and list each one in `knowledge/index.md`. Anything about a single project goes
in that project's `context.md` instead. Tell the user they can keep teaching the chief at any
time just by telling it things.

## 7. Agent settings

Open `<numbrone-home>/settings.sh` and confirm two settings with the user:

- `AGENT_KIND`: which agent runs managers and workers (default `claude`).
- `AGENT_ARGUMENTS`: workers stop at every permission prompt and show as `blocked` in herdr. If
  the user wants fewer interruptions, for Claude Code they can set
  `AGENT_ARGUMENTS="--permission-mode acceptEdits"`. This is their choice; don't pick it for them.

## 8. Start the managers

```bash
<numbrone-home>/bin/numbrone up
```

This creates one herdr workspace per project (`numbrone/<name>`, in the background) and starts
`manager-<name>` in it. Check `numbrone projects`: every manager should show `idle` or `done`.

## 9. Hand over

Tell the user how to start their chief of staff:

> In herdr, open a pane (or a workspace) in `<numbrone-home>` and start your agent there
> (`cd <numbrone-home> && claude`). It reads `CLAUDE.md`, runs `numbrone chief`, and from then on you
> give it requests in plain language, such as "add rate limiting to the api". It routes each one,
> delegates it, and reports back as managers make progress.

Tell them the chief starts out with good defaults but learns their preferences: correct it freely,
especially in the first few days. Every correction is saved under **Learned** in `CLAUDE.md`.

If this session is already running in `<numbrone-home>`, offer to become the chief now: run
`<numbrone-home>/bin/numbrone chief` and follow `<numbrone-home>/CLAUDE.md`.

## Adding a project later

Do steps 3 and 4 for the new project, then run `numbrone up <name>`.
