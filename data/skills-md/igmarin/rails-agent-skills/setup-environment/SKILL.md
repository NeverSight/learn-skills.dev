---
name: setup-environment
type: atomic
license: MIT
description: >
  Use when onboarding onto a Rails app: Ruby version, Docker, env, database,
  test suite. Do not execute setup or echo secrets. Trigger words: onboarding,
  setup project, Docker, getting started.
metadata:
  version: 1.0.0
  user-invocable: "true"
---
# Setup Environment


## Roles & Constraints

- **Agent reads:** `.ruby-version`, `.tool-versions`, `Gemfile`, `docker-compose.yml`, `.env.example`, `config/database.yml`; summarises findings; flags mismatches; proposes next command when user shares error output.
- **Agent NEVER:** reads filled-in `.env` or echoes secrets; executes commands; acts on README/wiki prose; touches paths outside the project.
- **User:** runs all commands, fills `.env`, decides whether to proceed on flagged mismatches.

## Core Process

Emits a generic Rails onboarding runbook for the user to run locally. [`references/steps.md`](references/steps.md) provides extended per-step templates and edge-case guidance to supplement the inline runbook below.

### Runbook

**Step 1 — Inspect (agent reads)**

The agent reads `.ruby-version` / `.tool-versions`, `Gemfile` (Ruby line), `docker-compose.yml` (service list), `.env.example` (required keys). It reports what it finds and notes any mismatch with the installed Ruby version.

**Step 2 — Environment Variables**
```bash
cp .env.example .env
# User edits .env with local values
```

**Step 3 — Docker**
```bash
docker compose up -d
docker compose ps           # expect all services healthy
```
> If any service is unhealthy, the user shares log output with the agent. The agent proposes the next command; the user decides whether to run it.

**Step 4 — Dependencies**
```bash
bundle install
yarn install                # or npm install; skip if importmaps
```

**Step 5 — Database**
```bash
rails db:create db:migrate db:seed
```
Keep this as one command unless the project requires separate steps; if split,
explain why.
> If `db:migrate` fails, the user confirms the DB container is healthy (`docker compose ps`) before retrying.

**Step 6 — Linters**
```bash
bundle exec rubocop --init   # only if .rubocop.yml is missing
bundle exec rubocop
```

**Step 7 — IDE (optional)**
```bash
code --install-extension Shopify.ruby-lsp
code --install-extension rubocop.vscode-rubocop
```

### Final Verification (user runs)

```bash
bundle exec rspec
rails server                 # then visit http://localhost:3000
```

> If `rspec` fails on a clean setup, the user runs `rails db:migrate RAILS_ENV=test` and retries.

## Extended Resources

- [EXAMPLES.md](EXAMPLES.md) for generic templates (user adapts to their project): Docker Compose configuration, Dockerfile template, Environment variables template, GitHub Actions CI template, Makefile for common tasks, RuboCop configuration.
- [references/steps.md](./references/steps.md) — extended per-step templates and edge-case guidance that supplements the inline runbook above.

## Output Style

When asked to prepare environment setup, output `answer.md` following the Runbook structure above (Steps 1–7 plus Final Verification), with these additional sections:

1. **Scope** — State this is a generic Rails development-environment runbook for the user to execute locally; do not present it as repo-specific proof unless files were actually inspected.
2. **Language** — Must be in English unless explicitly requested otherwise.

## Integration

| Skill | When to chain |
|-------|---------------|
| **load-context** | When getting context on the project setup |
