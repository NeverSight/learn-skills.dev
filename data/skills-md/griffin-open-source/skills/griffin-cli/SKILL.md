---
name: griffin-cli
description: Use Griffin CLI non-interactively with --json to validate/test monitors, plan/apply/destroy hub changes, manage env vars/secrets, and run two-step auth login. Trigger when users ask to run griffin commands or automate monitor workflows.
---

# Griffin CLI

This skill teaches you how to use **griffin-cli** to support Griffin API monitors: local runs, validation, deploying to the hub, and managing configuration. The CLI is the main way to execute monitors locally, preview and apply changes, and operate on environments and secrets.

---

## 1. When to use this skill

- User asks to run monitors locally, validate monitor files, or run Griffin tests.
- User wants to preview or apply monitor changes to the hub, or destroy monitors.
- User needs to set up a project (init), manage environments, or manage variables/secrets.
- User wants to check status, view runs, trigger a run, or view metrics.
- User mentions griffin-cli, `griffin` commands, or workflows that support Griffin monitors.

---

## 2. Agent execution contract (--json)

When acting as an agent, follow these rules:

- **MUST** run commands with `--json` (prefer global form: `griffin --json <command> ...`).
- **MUST** parse exactly one JSON object from stdout on success and exactly one JSON object from stderr on error.
- **MUST** include non-interactive bypass flags for commands that would otherwise prompt.
- **MUST** use the auth two-step flow (`auth login --no-poll` then `auth login --poll`) in JSON mode.
- **NEVER** run interactive `griffin auth login` (without `--no-poll` or `--poll`) in agent JSON workflows.

All commands support a **global `--json`** flag. In JSON mode the CLI returns a **single JSON object** and disables prompts/spinners/human formatting.

**How to pass --json:** Use the global option before the subcommand, e.g. `griffin --json status` or `griffin --json plan --env production`. Some commands also accept a local `--json`; either form enables JSON output.

### 2.1 JSON envelope

- **Success:** One JSON object on **stdout**, exit code 0.
  ```json
  { "ok": true, "command": "<command-name>", "data": { ... }, "messages": [{ "level": "info", "message": "..." }] }
  ```
  Parse `data` for the result. `messages` is optional (informational lines).

- **Error:** One JSON object on **stderr**, exit code 1.
  ```json
  { "ok": false, "command": "<command-name>", "error": { "code": "ERROR_CODE", "message": "...", "details": ..., "hint": "..." } }
  ```
  Use `error.code` for programmatic handling. Common codes: `AUTH_FAILED`, `NOT_FOUND`, `INTERACTIVE_REQUIRED`, `NO_PENDING_AUTH`, `UNKNOWN_ERROR`.

### 2.2 Non-interactive behavior

In JSON mode, **prompts are disabled**. If a command would prompt (e.g. confirm apply, enter secret value), it returns `INTERACTIVE_REQUIRED`. You **MUST** supply the bypass flag:

| Command / action | Bypass flag |
|------------------|-------------|
| `apply`          | `--auto-approve` |
| `destroy`        | `--auto-approve` |
| `secrets delete` | `--force` |
| `secrets set`    | `--value <value>` (provide value on the command line; avoid for highly sensitive data) |
| `integrations remove` | `--force` |
| `notifications test`  | Provide `--integration` (and e.g. `--channel` or `--to-addresses` as needed) |

Example (agent-safe apply):
```bash
griffin --json apply --env production --auto-approve
```

### 2.3 Auth login: two-step flow for agents

`auth login` uses a **device authorization flow**. In an agent context you cannot open a browser or wait interactively in one process. Use the **two-step** flow:

1. **Step 1 — Get auth URL and instruct the user:**  
   Run:
   ```bash
   griffin --json auth login --no-poll
   ```
   - **Stdout** (success): `data` contains `authUrl`, `userCode`, and `message` (e.g. "Complete authorization in the browser, then run: griffin auth login --poll").
   - The CLI does **not** open the browser in JSON mode. Present `authUrl` (or `userCode`) to the user and ask them to complete sign-in in their browser.

2. **Step 2 — Complete login after user authorized:**  
   After the user has finished authorizing in the browser, run:
   ```bash
   griffin --json auth login --poll
   ```
   - **Stdout** (success): `data` is `{ "success": true }`; credentials are saved to `~/.griffin/credentials.json`.
   - If no pending auth exists: **stderr** error with code `NO_PENDING_AUTH` and a hint to run `griffin auth login --no-poll` first, then have the user authorize, then run `griffin auth login --poll`.

**Summary for agents:** You **MUST** use `--no-poll` then `--poll` with `--json`. Never run `griffin auth login` without one of these flags in JSON mode; that path is interactive-only. For self-hosted hubs, use `griffin auth connect --url <url> --token <token>` instead (no browser).

### 2.4 Troubleshooting (JSON mode)

| Error code | Meaning | Required recovery |
|------------|---------|-------------------|
| `INTERACTIVE_REQUIRED` | Command requires prompt input | Re-run with the required non-interactive bypass flag (`--auto-approve`, `--force`, `--value`, etc.) |
| `NO_PENDING_AUTH` | Tried `auth login --poll` with no prior device flow | Run `griffin --json auth login --no-poll`, have the user complete browser auth, then run `griffin --json auth login --poll` |
| `AUTH_FAILED` | Credentials invalid/expired or auth context mismatch | Re-auth (`auth login` two-step) or reconnect with `auth connect --url ... --token ...`; verify target hub URL/token |
| `NOT_FOUND` | Referenced monitor/resource/environment does not exist | Verify identifiers (`--monitor`, `--env`, integration/secret names) and retry. For missing monitor name, error details may include `available: string[]` listing valid monitor names. |

---

## 3. Command overview

Commands are either **top-level** or under a **group**. The default environment is `default` unless overridden with `--env <name>` where supported. **All commands support `--json`** (global flag) for a single JSON blob on stdout/stderr.

| Area | Commands | Purpose |
|------|----------|--------|
| **Project** | `init`, `validate`, `status` | Bootstrap, validate monitors, show status |
| **Local run** | `test` | Run monitors locally |
| **Hub sync** | `plan`, `apply`, `destroy` | Preview changes, push to hub, remove from hub |
| **Hub runs** | `runs`, `run`, `metrics` | List runs, trigger run, view metrics |
| **Auth** | `auth login`, `auth logout`, `auth connect`, `auth generate-key` | Cloud or self‑hosted auth |
| **Environments** | `env list`, `env add`, `env remove` | Manage environments |
| **Variables** | `variables list`, `variables add`, `variables remove` | Per-environment variables (in state) |
| **Secrets** | `secrets list`, `secrets set`, `secrets get`, `secrets delete` | Per-environment secrets (stored on hub) |
| **Integrations** | `integrations list`, `integrations show`, `integrations connect`, `integrations update`, `integrations remove` | Slack, email, webhooks, etc. |
| **Notifications** | `notifications list`, `notifications test` | Notification rules and test sends |

---

## 4. Core workflows

### 4.1 Project setup

1. **Initialize** (once per project):
   ```bash
   griffin init
   griffin init --project my-service   # override project ID
   ```
   Creates `.griffin/state.json` with project ID, default environment, and hub config. Add `.griffin/` to `.gitignore`.

2. **Optional: add environments and variables**
   ```bash
   griffin env add staging
   griffin env add production
   griffin variables add API_BASE=https://staging.example.com --env staging
   griffin variables add API_BASE=https://api.example.com --env production
   ```

3. **Connect to hub** (for plan/apply/runs/run/metrics):
   - **Griffin Cloud**: Use the two-step flow: `griffin --json auth login --no-poll` (get `authUrl`, have user authorize), then `griffin --json auth login --poll` (complete; token stored in `~/.griffin/credentials.json`). See section 2.3 above.
   - **Self‑hosted**: `griffin auth connect --url https://hub.example.com --token <api-key>` (no browser).

### 4.2 Local development and validation

- **Validate** monitor files (no run, no hub). Optional `--monitor <name>` validates only that monitor:
  ```bash
  griffin validate
  griffin validate --monitor health-check
  ```

- **Run monitors locally** against an environment (uses variables from state for that env). Optional `--monitor <name>` runs only that monitor:
  ```bash
  griffin test
  griffin test --env staging
  griffin test --env staging --monitor health-check
  ```

- **Check status** (project, hub connection):
  ```bash
  griffin status
  ```

### 4.3 Preview and deploy to hub

- **Preview** what would be created/updated/deleted (exit code 2 if there are changes). Optional `--monitor <name>` plans only that monitor:
  ```bash
  griffin plan
  griffin plan --env production --json
  griffin plan --env production --monitor health-check
  ```

- **Apply** changes to the hub (creates/updates monitors; optionally prune). Optional `--monitor <name>` applies only that monitor:
  ```bash
  griffin apply --env production
  griffin apply --env production --monitor health-check
  griffin apply --env production --auto-approve
  griffin apply --env production --dry-run
  griffin apply --env production --prune    # delete hub monitors not present locally
  ```

- **Destroy** monitors on the hub:
  ```bash
  griffin destroy --env production
  griffin destroy --env production --monitor health-check --dry-run
  griffin destroy --env production --auto-approve
  ```

### 4.4 Runs and metrics

- **List recent runs**:
  ```bash
  griffin runs
  griffin runs --env production --monitor health-check --limit 20
  ```

- **Trigger a run**:
  ```bash
  griffin run --env production --monitor health-check
  griffin run --env production --monitor health-check --wait
  griffin run --env production --monitor health-check --force   # even if local differs from hub
  ```

- **Metrics summary**:
  ```bash
  griffin metrics --env production
  griffin metrics --env production --period 7d --json
  ```

### 4.5 Variables and secrets

Variables are stored in `.griffin/state.json` per environment and used when running monitors (e.g. for `variable("api-service")` in monitor DSL). Secrets are stored on the hub per environment and referenced in monitors via `secret("REF")`.

- **Variables** (in state; not sensitive):
  ```bash
  griffin variables list --env default
  griffin variables add API_BASE=https://localhost:3000 --env default
  griffin variables remove API_BASE --env default
  ```

- **Secrets** (on hub; use for tokens, API keys):
  ```bash
  griffin secrets list --env production
  griffin secrets set API_TOKEN --env production
  griffin secrets set API_TOKEN --env production --value "sk-..."
  griffin secrets get API_TOKEN --env production
  griffin secrets delete API_TOKEN --env production --force
  ```

---

## 5. File and config locations

- **State**: `.griffin/state.json` (project root). Holds `projectId`, `environments` (with optional `variables` per env), `hub`, `cloud`, and optional `discovery` (pattern/ignore). Do not commit if it contains local-only overrides; add `.griffin/` to `.gitignore` if desired.
- **Credentials**: `~/.griffin/credentials.json` (user-level). Used by `auth login` and `auth connect --token`. Do not commit.
- **Monitors**: Discovered from `__griffin__` directories; pattern is configurable in state under `discovery.pattern` (default `**/__griffin__/*.{ts,js}`), with `discovery.ignore` (e.g. `["node_modules/**", "dist/**"]`).

---

## 6. Environment and defaults

- Most hub-related and run commands accept `--env <name>`. Default is `default`.
- Set default env for the shell: `export GRIFFIN_ENV=production` (if the CLI respects it; otherwise pass `--env` explicitly).
- Variables and secrets are scoped per environment; ensure the right `--env` when adding or listing.

---

## 7. Checklist for common tasks

**First-time setup**
- [ ] Run `griffin init` (and optionally `griffin env add` for extra environments).
- [ ] Add variables with `griffin variables add KEY=value --env <env>` as needed for monitor `variable("...")` refs.
- [ ] Use `griffin auth login` (two-step: `--no-poll` then user authorizes then `--poll`) or `griffin auth connect` if you will use plan/apply/runs/run/metrics.

**Before deploying**
- [ ] Run `griffin validate` to ensure monitor files are valid.
- [ ] Run `griffin test --env <env>` to confirm monitors pass locally.
- [ ] Run `griffin plan --env <env>` to preview hub changes; then `griffin apply --env <env>` (use `--dry-run` or `--auto-approve` as appropriate).

**After changing monitors**
- [ ] `griffin validate` then `griffin test`; then `griffin plan` and `griffin apply` for the target environment.

**Secrets used in monitors**
- [ ] Create/update with `griffin secrets set REF --env <env>`; ensure secret ref names match monitor DSL (e.g. `API_TOKEN`, not `api-token`).

---

## Summary

1. **Agents:** Follow the execution contract in section 2: use `--json`, parse stdout/stderr JSON envelopes, provide required bypass flags, and use auth two-step only (`--no-poll` then `--poll`).
2. **Setup**: `griffin init`; optionally `env add`, `variables add`, and `auth login` (two-step) or `auth connect`.
3. **Local**: `griffin validate` and `griffin test --env <env>`.
4. **Hub**: `griffin plan` to preview; `griffin apply` to sync; `griffin runs` / `griffin run` / `griffin metrics` to observe.
5. **Config**: Variables in state via `griffin variables`; secrets on hub via `griffin secrets`; both are per-environment.
6. Use `--env` consistently when targeting a non-default environment; use `griffin status` to verify project and connection.
