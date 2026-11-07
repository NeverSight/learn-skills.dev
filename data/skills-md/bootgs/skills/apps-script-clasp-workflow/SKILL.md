---
name: apps-script-clasp-workflow
description: Documents the clasp CLI workflow for Google Apps Script projects — login, project creation/cloning, push vs deploy, versioning, and multi-environment (dev/staging/prod) setups. Use when setting up CI/CD for an Apps Script project, publishing a new version, or switching between multiple script IDs. Framework-agnostic — applies with or without bootgs. Not for Marketplace listing and review (`apps-script-marketplace-publish`), nor for why a trigger isn't firing (`apps-script-triggers`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
---

# Apps Script clasp Workflow

## Auth

```bash
clasp login             # interactive, opens a browser
clasp login --no-localhost   # headless/CI — prints a URL to visit, then paste the resulting code back
```

Produces `~/.clasprc.json`. In CI, inject this file from a secret — never commit it; it's a live OAuth credential.

## Project setup

```bash
clasp create --type standalone --title "My Project"   # new project
clasp clone <scriptId>                                  # existing project
```

`.clasp.json` fields that matter:

| Field | Purpose |
|---|---|
| `scriptId` | Target Apps Script project — the single most important field to get right per environment (see Multi-environment below) |
| `rootDir` | Directory clasp pushes from, e.g. `"./dist/appsscript"` — point it at your **build output**, not source, if you bundle |
| `filePushOrder` | Files pushed first, before the rest — `appsscript.json` is commonly listed here since manifest changes should land before code that depends on new scopes/services |

## Push vs. deploy — the distinction that causes silent "my fix isn't live" bugs

- `clasp push` updates the project's **HEAD** (the editor/dev version). Anyone opening the script editor sees it immediately. It does **not** affect any existing versioned deployment.
- `clasp deploy` creates or updates a **versioned deployment** with a stable URL/ID. A web app or add-on installed by end users runs whatever version its deployment points at — pushing new code does nothing for them until you deploy.

```bash
clasp push -f                          # force push, skip the interactive diff/overwrite prompt — needed for CI
clasp push --watch                     # dev loop: push on every local file change
clasp deploy -i <deploymentId> -d "Fix widget sorting"   # update an existing deployment
clasp deployments                      # list deployment IDs
clasp versions                         # list version history
```

Forgetting the deploy step after a push is the single most common "I fixed it but users still see the bug" report — always pair a fix with a deploy when the project has a live deployment.

## Multi-environment (dev/staging/prod)

clasp has no native named-environment concept — one `.clasp.json` points at one `scriptId`. The standard workaround is one config file per environment, copied into place before pushing:

```
.clasp.dev.json
.clasp.staging.json
.clasp.prod.json
```

```json
{
  "scripts": {
    "push:dev": "cp .clasp.dev.json .clasp.json && clasp push -f",
    "push:staging": "cp .clasp.staging.json .clasp.json && clasp push -f",
    "deploy:prod": "cp .clasp.prod.json .clasp.json && clasp push -f && clasp deploy -d \"$npm_config_message\""
  }
}
```

Never commit the active `.clasp.json` if it varies per developer machine/environment — commit the per-environment copies instead and gitignore the working one, or keep `.clasp.json` itself checked in only for single-environment projects.

## Manifest essentials worth setting explicitly

Don't leave `appsscript.json` at its scaffolded defaults:

- `runtimeVersion: "V8"` — required for modern syntax and decorators (see the `bootgs-quickstart` skill if the project uses bootgs).
- `oauthScopes` — list only what's actually called. GAS shows the full list on the consent screen; an over-broad list (a common copy-paste mistake) increases user friction and review scrutiny for public add-ons without adding capability.
- `webapp.executeAs`/`webapp.access` — only relevant if `doGet`/`doPost` are deployed as a web app.
- `exceptionLogging: "STACKDRIVER"` — otherwise uncaught errors only appear in the legacy execution log tied to the script's lifetime.

## Verification

- [ ] `clasp push -f` used in CI (interactive prompts hang non-interactively without `-f`).
- [ ] A deploy step (`clasp deploy`) runs after push whenever the project has a live deployment end users depend on — push alone is not a release.
- [ ] `.clasprc.json` is never committed; CI injects it from a secret.
- [ ] `oauthScopes` reviewed against what the code actually calls before each release.
