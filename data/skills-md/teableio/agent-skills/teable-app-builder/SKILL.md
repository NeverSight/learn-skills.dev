---
name: teable-app-builder
description: Build, change, run and publish a Teable app (an App Builder app, Next.js on Teable data) from this machine with the `teable` CLI instead of the in-app chat. Use when the user wants to create a Teable app, work on an existing one locally, push a new version, publish it, roll back, or react to table-schema changes and named-query repairs. Covers project (base) resolution, `teable app init|clone|pull|push|publish`, the local dev loop and the platform rules the checkout must follow.
---

# Teable App Builder (local workspace)

A Teable app is a Next.js project that reads and writes a Teable project (base) through the
Teable SDK, hosted and published by Teable. Normally Teable's own agent (Cuppy) builds it in a
sandbox. This skill does the same work on the user's machine: you are the agent, the `teable`
CLI materializes everything the sandbox would have provided, and `teable app push` saves
versions back to Teable.

You run on the user's machine, not in that sandbox. There is no in-app chat around you: no
credential cards, no sandbox paths, no Teable-side preview you control. Where the sandbox would
show a card, ask the user in your own conversation; the `AGENTS.md` a checkout gets is already
the local variant.

Data questions (query records, change rows) go through the Teable MCP tools when they are
available; everything that produces files, touches git or needs the app checkout goes through
the CLI. Do not mix the two for the same job.

This skill covers only the local checkout. Two neighbouring jobs belong to the
`teable-assistant-ops` skill: having Teable's own builder write or change the app from a prompt
(`teable app create|update --prompt`, no checkout involved), and work on the project itself
(creating tables, fields and views, imports, automations). Use it for the tables a new app needs.

## Prerequisites

- Node.js 22+, git and pnpm on PATH.
- The CLI: use `teable` when it is on PATH; otherwise run every command as
  `npx -y @teable/cli@latest <command>` (no install step). The app checkout commands need a CLI
  whose `teable app --help` lists `init`.
- Sign-in happens once and you do it, not the user: when a command answers
  `Authorization is required`, run `teable auth login` — it opens the browser, the user approves,
  done. `teable auth status` shows the account and endpoint. Self-hosted Teable: `--endpoint <url>`
  or `TEABLE_ENDPOINT`.
- The deployment has a git registry for app code (teable.ai does). Without it the CLI says so;
  then the app is built in the in-app App Builder and `teable app get-code` gives a read-only copy.

## 1. Resolve the project (base) first

Every app belongs to one project. First read what the user is asking for:

- **Building on data they already have** ("an app for my inventory table", a pasted URL, a
  project name) → find that project (below).
- **A new system from scratch** ("make me a CRM", "build a booking app") with nothing pointing
  at existing data → usually a new project: `teable base create --space-id spc… --name "<name>"`,
  then create the tables the app needs and `teable link <baseId>`. A request like this is not
  a reason to drop tables into some unrelated project the user happens to have.
- **Unclear** → ask once, offering the close existing projects and "a new project" side by side.

Finding an existing project, most specific first:

1. **Explicit**: a Teable URL (take the `bse…` id from it), an id, or a name
   → `teable base list --search "<name>"`. One hit: use it. Several: ask the user which.
2. **Directory binding**: the current directory (or a parent) holds `.teable/app.json`
   (an app checkout) or `.teable/cli/config.json` (`teable link`). Commands run there need no
   `--base-id`.
3. **Ask**: `teable link` without arguments lists the projects the account can use. Show the
   candidates and ask once; then `teable link <baseId>`.

Creating a project is visible to everyone in that space, so say where it goes before or as you
do it ("creating project *CRM* in space *Sales*"). The space: the one the user named; else the
only one they have (spaces show up in `teable base list`); else the obvious one from context;
otherwise ask, together with any other open question rather than as a separate round. Don't
stop to ask about anything you can reasonably decide and mention instead.

Tables need no choosing: the checkout receives `schema/*.json` for every table of the project.

## 2. Create or clone the checkout

```bash
teable app init --name "<App name>" --dir ./<dir>        # new app, scaffold as version 1
teable app clone --app-id app… --dir ./<dir>             # existing app (ids from `teable app list`)
```

Which app: the one the user named or linked. Otherwise run `teable app list` first. Several
apps and no name → ask which one. A request for a new app when a similar one already exists →
ask once whether to change that one or start a new one; do not pick silently.

Both leave a git checkout whose remote `teable` is the app repository, plus:

| File | Purpose |
| --- | --- |
| `CLAUDE.md` → `AGENTS.md` | The platform's instructions for this app: stack, scaffold map, locked files, data rules, credential rules. Read it before writing code. |
| `.env` | Platform variables (API URL, app token, app and project ids, AI gateway). Never edit or commit; `teable app pull` refreshes it. |
| `teable.md`, `schema/*.json` | SDK usage and the current table schemas. Regenerated by `teable app pull`. |
| `.teable/app.json` | Workspace marker (app, project, endpoint). Gitignored; do not edit. |

Then `cd <dir>`, `pnpm install`, `pnpm dev` (port 3000) and build. `AGENTS.md` is authoritative
for conventions; this skill only covers the workflow around it.

## 3. Work, then push

```bash
teable app pull                        # start of a session, or when tables/app may have changed
# ... edit, verify with curl -s http://127.0.0.1:3000 ...
teable app push -m "<what changed>"    # commit (if needed), pre-check, push, record a Teable version
```

`push` refuses when platform-owned files changed, when a `.env` file is tracked, when
`teable/queries.yaml` is invalid, or when the app repository moved ahead (then `teable app pull`,
resolve, push again). On success Teable records the version under the user's name, refreshes a
running preview and notes the push in the app chat. A plain `git push` does not create a version.

`clone` and `pull` also bring the checkout to what the Teable sandbox would run: they rewrite the
platform's own files and apply pending template upgrades to an older app (Next 16 `proxy.ts`,
`pnpm-workspace.yaml`, …). On a clean tree that lands as its own commit ("Upgrade app template" or
"Sync platform files"), pushed with your next `teable app push`; check `notes` in the output for
anything left to do by hand.

`pull` reports table-schema changes since the last sync ("field added", "type changed", …) and
pending named-query repairs. Adjust code for the changes; review repairs with
`teable query repairs` and `teable query repair-apply --repair-id <id>` (details in
`references/workflow.md`).

## 4. Publish, inspect, roll back

```bash
teable app publish --wait              # only when the user asks; streams build steps, prints the URL
teable app versions --app-id app…      # history
teable app rollback --app-id app… --to <n>   # restores as a new version; then `teable app pull`
```

## Rules that keep the checkout valid

- Never edit the locked files `AGENTS.md` lists (`lib/teable.ts`, `lib/credentials.ts`,
  `next.config.mjs`, reporters, beacon route, …): the platform rewrites them.
- Never ask the user to paste a secret into the chat, and never pass `--value` yourself. The user
  runs `teable secret set --key <KEY> --grant app:<appId> --dev-env` in a terminal window of their
  own (not via `!` in Claude Code: no TTY there): it
  prompts for the value without echo, stores it as their personal secret granted to the app, and
  writes the same key to the checkout's `.env.local` for `pnpm dev`.
- An app that reads a third-party service (Stripe, HubSpot, Gmail…) gets a connection, not an
  API key, whenever one exists: `teable integration search --query "<task>"` finds it,
  `teable integration connect --toolkit <slug> --wait` opens the consent screen, then
  `teable secret grant --type connection --id <connectionId> --resource app:<appId> --alias <ALIAS>`.
  A toolkit that takes an API key prompts for it in the terminal, so the user runs that command
  themselves in a terminal window of their own — not via Claude Code's `!` prefix, which has no
  TTY, so the prompt cannot read the value. AGENTS.md has the
  runtime helpers (`getConnectionToken`, `callConnection`); both work under `pnpm dev`.
- Login flows redirect to the Teable preview origin, not localhost: verify them after a push in
  the app's Preview panel in Teable.
- Keep commits user-facing: one commit per completed request, subject under 72 characters, no
  `feat:`/`fix:` prefixes.
- Codex: the first `git push` and CLI network calls need network approval.

See `references/workflow.md` for the end-to-end script and `references/pitfalls.md` for what
goes wrong and how to recover.
