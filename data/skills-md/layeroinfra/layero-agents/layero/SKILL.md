---
name: layero
description: Deploy, publish or ship a site to Layero and operate it afterwards — hosting with build servers in Russia. Use when the user asks to deploy/publish/ship and mentions Layero, when the directory contains .layero/project.json or layero.json, when asked to configure a Layero build (layero.json), or for any question about a site hosted on Layero (status, logs, rollback, domains, env, analytics, Data API).
---

# Layero

Layero is a hosting and deployment platform (like Vercel) with build servers
and delivery inside Russia. A project is connected to a repository or uploaded
from a folder; the platform builds it and serves it at `<project>.layero.app`.
There are custom domains, preview branches, runtime apps, environment
variables, analytics and Postgres databases with a Data API. Dashboard —
`https://app.layero.ru`, documentation — `https://docs.layero.ru`.

## Three paths — pick by situation

| Situation | Path |
|---|---|
| (a) There is a repository on GitHub, GitVerse, GitLab, GitFlic or SourceCraft | Connect it: `npx layero@latest projects create --repo <provider>:<owner/repo> --json` (a token-based provider — `npx layero@latest sources connect <provider> --token-stdin`; GitHub — by installing the App in the dashboard), or in the dashboard **Создать проект → Импорт из репозитория**. After that a push to a branch = preview, a push to `main` = production. Details — [references/git-providers.md](references/git-providers.md). |
| (b) There is a folder with code, and no repository (or none is wanted) | `npx layero@latest deploy --json` — the CLI packs the folder, the platform builds it. Ready-made static files can also be published through MCP `publish_site`. |
| (c) The site is already on Layero | Diagnostics (`diagnose_deploy` in MCP / `npx layero@latest diagnose`), logs, rollback, environments (`envs list`), domains, env, analytics, Data API — through MCP or the CLI. |

How to tell: the user works with a repository — (a); asks to "put this folder
online" («выложи вот эту папку») — (b); asks about a site that is already
live — (c). Do not turn (b) into (a): `git init` is not needed for a deploy.

## CLI

```bash
npx layero@latest deploy --dry-run --json   # the build plan; uploads nothing, no login
npx layero@latest deploy --json
```

`--json` switches on JSON-lines: one object per stdout line. Route on the
`event` field; do not parse the human-readable text. Inside an agent and with
a non-TTY stdout the mode switches on by itself.

`--dry-run` prints how the platform will build the folder: framework, build
command, output folder, where each value comes from (`layero.json`, project
settings, `package.json`, a framework default) and whether the deploy replaces
the live site. If its `confident` is `false`, do what `next_action` says before
the first deploy (details in the `layero.json` section). `npx layero@latest
init` is optional: it adds a rules block to `AGENTS.md`; it records no
settings, and `deploy` links the folder by itself.

With a token the whole deploy is one non-interactive command:
`LAYERO_TOKEN=… npx layero@latest deploy --name <name> --yes --json`.
No account, no token, or the person is away from the keyboard:
`npx layero@latest deploy --claim --yes --json` — no login at all (details
below, "No Layero account at all").

Main events:

- `auth_required` — `url` and `user_code`. Show `url` as a clickable link; the
  CLI waits for the login by itself (polling every 2 s, the token is cached in
  `~/.layero/config.json`). There is no localhost callback — the browser may
  be on another machine; it works from SSH, Docker and sandboxes.
- `detected` — how the CLI sees the folder: framework, build command, output
  folder, `sources`, `confident`. It is advice — the platform decides from the
  uploaded files, and the guess is never saved to the project. `confident:
  false` comes with `hint` and `next_action`: follow them.
- `build_log` — raw log; forward only the lines with errors.
- `ready` — `url` = the live address of the site, already answering: the CLI
  waits (up to 90 s) until the address serves the site instead of a platform
  page. Show it **as is**, never assemble the host from a template.
  `dashboard_url` is the dashboard, not the site. `edge_ready: false` means the
  app never came up — read `npx layero@latest logs --runtime`.
- `error` — a stable `code` and `next_action`. Follow `next_action` (for a
  failed build it is `npx layero@latest diagnose --deploy <id>`, which also
  works without an account).

A repeat deploy is the same command: the first run creates the project, the
next ones reuse it; no commit is needed between runs. The full list of events,
fields, error codes and exit codes — [references/json-events.md](references/json-events.md).
Every command prints events in `--json`; the exit code tells the class:
2 — login needed, 3 — not found, 4 — invalid input, 5 — remote error.

**No Layero account at all** — `npx layero@latest deploy --claim --json`:
the platform creates a temporary site for 1 hour, and the CLI prints a
`claimable` event with `claim_url` **before** `ready`. Static sites and SPAs
only: a server app (SSR, fullstack, container) is refused with
`claim_static_only` before anything is uploaded — it needs an account. The
address is random and closed to search engines. Hand the person
`ready.url` and `claim_url`: only they can take the site into an account, in
the dashboard. The mode turns on ONLY with `--claim`: without it and without
a token `deploy` asks for a login (`auth_required`) — show the person `url`
and `user_code` and wait. Publishing without an account is the person's
decision, not yours: use `--claim` when they asked for it or agreed. The
sandbox only creates a new project: `--claim` together with `--project` is the
`claim_with_project` error. Taking the site into an account clears the
environment variables, deploy hooks and build settings set up without one.

### CI

Browser login is impossible in a runner — a token is needed:
`npx layero@latest token create` or `https://app.layero.ru/settings/cli`.

```bash
LAYERO_TOKEN=… npx layero@latest deploy --project <slug> --json --yes
```

`LAYERO_TOKEN` overrides the cached local login. `--yes` skips the
confirmation that would otherwise wait forever. `--project`, not `--name`:
`--name` only names the project at creation, and a pipeline running from a
clean checkout without `.layero/project.json` would create a new project on
every run.

## MCP

Server `https://mcp.layero.ru/mcp` (Streamable HTTP), name in the client
config — `layero`. To connect: `npx -y add-mcp https://mcp.layero.ru/mcp` or
the Claude Code / Cursor plugin from `LayeroInfra/layero-agents`. Available
without login: `search_docs`, `check_copy`, `refactor_site`; everything else
needs OAuth login (the client opens a browser on the first call of an account
tool) or the `Authorization: Bearer $LAYERO_TOKEN` header for CI.

Tool groups:

- **account and projects** — `whoami`, `my_projects`, `list_sources`
  (providers and connections), `import_repo` (a project from a repository —
  path (a) without the dashboard; it finishes the setup wizard and starts
  the first build by itself, without pinning the detected framework, build
  command or output folder (the builder detects them from the repository on
  every build) — field `setup`: `applied` / `pending` / `failed`;
  `deploy=false` leaves the project in the setup wizard; the provider token
  is connected by the person in the dashboard, not by the agent),
  `project_create` (an empty project for a later `publish_site`),
  `list_environments` (branches with addresses and latest builds),
  `project_settings` (read or change the app folder, commands, output folder
  and project type — the way out when detection was wrong; an app in a
  monorepo subfolder is imported with `import_repo(root_directory=…)`);
- **site** — `site_status` (`wait_s` waits for a running build, `path` checks
  a route of an API server), `env_vars`, `read_site`, `site_screenshot`,
  `site_issues`, `refactor_site`, `check_copy`, `check_performance`;
- **deploys** — `list_deploys`, `deploy_logs`, `diagnose_deploy`,
  (`build_facts`: what the build really used), `retry_deploy`
  (`redeploy=true` rebuilds the latest commit without a push),
  `cancel_deploy`, `rollback`, `publish_site`
  (the old name `publish_landing` is a deprecated alias);
- **domains and analytics** — `connect_domain`, `check_domain`,
  `list_domains`, `connect_analytics`, `site_analytics`;
- **Data API** — `data_api_status`, `data_api_methods`, `data_api_grant`,
  `data_api_keys`, `data_api_origins`, `data_api_probe`.

These require the person's explicit consent: `rollback` (changes what
visitors see), `data_api_grant` (opens access to data), `data_api_keys` with
`issue`/`revoke`, `data_api_origins`. A client with forms gets the question
from the server; without forms — ask in the chat and only then pass
`confirmed`. Never pass `confirmed` in place of the person's answer.

## `layero.json`

**The file is an answer to one specific problem — one symptom, one field —
never a questionnaire.** Look at the folder first: an ordinary single app
deploys with no file at all; the shapes below are configured before the
first deploy. Every field you write
stops being auto-detected and is locked in the dashboard, and an unknown key
is skipped silently — so never write the file "just in case".

**Before you create or edit `layero.json`, you MUST read
[references/layero-json.md](references/layero-json.md)** — the complete key
list, the symptom → field table and the log lines that prove a value was
applied. Do not write the file from memory.

When a build or launch fails:

1. Get the real error from the log (`diagnose_deploy` → `deploy_logs`, or
   `npx layero@latest diagnose` / `logs`) — never act on the card text alone.
2. Look at the failed stage: `detect` → app shape (root, type, `runtime`), not
   code; `install` → lockfile; `build` → the quoted error line; `verify` /
   `upload` → `outputDirectory`; `launch` → `startCommand`, `port`, env.
3. Find the symptom in the reference table and change exactly one thing.
4. Verify in the build log that the value was applied (`(from layero.json)`)
   and that the file produced no warnings.
5. The same failure twice in a row — stop and tell the person; no third deploy.

Before the first deploy, run `npx layero@latest deploy --dry-run --json`. When
it cannot recognise the folder it says so (`confident: false`) and names the
shape in `hint` and the fix in `next_action`: an app in a subfolder →
`--root <dir>`; a workspace app that imports a neighbour package → a
`layero.json` at the workspace root with `"framework": "generic"` +
`buildCommand` + `outputDirectory`; a custom build script with no framework →
`"framework": "generic"` (`static` never runs a build); a server →
`-t node_web` / `-t python_web`; `frontend/` + `backend/` → the full-stack
blocks. The shapes and their files are in the reference.

`--dry-run` does not read your code. For any server open the entry file first:
it must listen on `0.0.0.0` (not `127.0.0.1`) and on `$PORT`, and the start
command must run a file that exists after the build (`node dist/index.js`, not
a `.ts` source) — the launch error does not name these causes.

Not fixed by the file: monorepo root → `--root`; deploy from the wrong folder → `cd` or `--root`; Next.js server/export mode → `next.config`; code errors → the code; secrets and env → project variables (`env set`); platform failures → retry once.

No secrets, tokens, domains or ids in the file — it lives in git.

## Git providers

GitHub, GitVerse, GitLab, GitFlic, SourceCraft — all are connected in the
dashboard through «Импорт из репозитория». A push to a branch is a preview
environment, a push to `main` is production. Differences between providers —
[references/git-providers.md](references/git-providers.md).

## Never

- `git init` or a push to a repository for the sake of a deploy — the unit of
  a CLI deploy is a folder.
- `npm install -g layero` — a global install fails in agent sandboxes.
  Only `npx layero@latest …` or `npm install -D layero`.
- Opening the dashboard to "finish the setup": the CLI does everything itself,
  there has been no browser wizard since v0.5.0.
- `layero login --provider` — the flag is gone since v0.5.x; the provider is
  chosen in the browser.
- Treating `layero deploy` as a safe preview: for a CLI project a direct
  upload is auto-promoted and replaces what visitors see at `ready.url`.
  `--prod` only makes sense for projects with a connected repository.
- Offering `--branch` as an isolated publication: `deploy` rejects the flag
  with the `branch_unsupported` code — direct uploads land in the `cli`
  environment. An isolated preview is only a push to a branch of a connected
  repository (`projects create --repo`).
- Accepting a claimable request or deleting a project on the person's behalf:
  `claim accept` only opens the link, `projects delete` requires the `admin`
  scope and an explicit `--yes` from the person.
- Assembling the site address from a template — only `ready.url`.
- Deploying to production silently, or rolling back without asking.
- Inventing `layero.json` keys — only the names listed in the reference exist.
- Filling `layero.json` as a questionnaire — one symptom, one field.
- A third deploy after two identical failures; `--confirm-repeated-failure`
  is for the person, not for you.
- Editing code on a `detect`-stage failure — the fix is the app shape (root,
  type, `runtime`), not the code.
