---
name: nocobase-install-start
description: Select an installation method, install NocoBase, and start it locally or on a server. Use when users ask how to install NocoBase, initialize a project, or start a running instance.
argument-hint: "[docker|create-nocobase-app|git] [install-dir]"
allowed-tools: Bash, Read, WebFetch
---

# Goal

Install NocoBase with clear branching and minimal questioning.

# Workflow

1. Ask quick mode first.
2. Quick mode (`Docker + install together + PostgreSQL`):
- Ask only release channel and installation directory.
- Execute install and startup.
3. Non-quick mode:
- Ask installation method (`docker`, `create-nocobase-app`, `git`), release channel, and installation directory.
- If method is Docker, ask database mode (`install together` or `connect existing`).
- If Docker + `install together`, ask database type (`PostgreSQL`, `MySQL`, `MariaDB`).
- If `connect existing` (Docker/non-Docker), confirm connection info readiness and require config/env edits before startup.
- Execute install only; provide startup commands and verification steps (do not execute startup).
4. Always read `references/install-methods.md` and include the chosen method doc link before running commands.

# Method Rule

- Docker is the default recommended method.
- Use `create-nocobase-app` when user wants the fastest local bootstrap.
- Use Git installation only when user needs source-level customization.

# Mandatory Clarification Gate

- Do not run install/start commands before all required confirmations are collected.
- Quick mode: release channel + installation directory.
- Non-quick mode: installation method + release channel + installation directory.
- Docker extra: database mode; and database type if `install together`.
- Existing DB: connection info readiness confirmation.
- If user says "you decide" in non-quick mode, choose Docker.

# Mandatory Doc-Read Gate

- Do not run install/start commands before reading `references/install-methods.md`.
- Do not run install/start commands unless the chosen method matches one method in `references/install-methods.md`, or quick mode preset is selected.
- Include the exact method doc link from `references/install-methods.md` before running commands.
- If method mapping is unclear, stop and ask a clarification question.

# Question Template

- Quick mode question: "Do you want quick mode (`Docker + PostgreSQL + install together`) so I execute install and startup directly?"
- Method question: "Which NocoBase installation method do you want: Docker (recommended), create-nocobase-app, or Git?"
- Version question: "Which release channel do you want to install: latest (stable), beta, or alpha?"
- Directory question: "Please provide the target installation directory (for example `./my-nocobase` or `/opt/nocobase`)."
- Docker database mode question: "For Docker installation, do you want to install database together in Docker, or connect to an existing database?"
- Docker bundled DB type question: "For Docker + install together, which database type do you want to install: PostgreSQL, MySQL, or MariaDB?"
- Existing DB readiness question: "Please confirm your existing database connection info is ready (host, port, database, username, password), and you can edit NocoBase config/env before startup."

# Resources

- Must read `references/install-methods.md` before generating commands.
