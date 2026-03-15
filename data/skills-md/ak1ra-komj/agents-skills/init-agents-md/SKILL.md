---
name: init-agents-md
description: Use when writing, reviewing, or refactoring AGENTS.md, writing an agent guide, documenting the project for AI agents, or orienting AI coding tools to a new repository.
---

# init-agents-md

Analyze the repository and write (or overwrite) an `AGENTS.md` file in the project
root. The file is a concise, prescriptive orientation guide for AI coding agents.
It must not duplicate `README.md` — link there for anything already covered.

## Workflow

1. Read `README.md`, `pyproject.toml` / `package.json` / equivalent manifest,
   and any existing config files to infer the tech stack and tooling.
2. Identify the environment manager, test runner, linter, and build tool in use.
3. Write `AGENTS.md` following the structure below.
4. Aim for **under 80 lines** total.

## Required sections

### 1. What This Project Does (2–4 sentences)

State the project's purpose and technology stack category. Add a pointer to
`README.md` for full details.

### 2. Environment & Tooling — CRITICAL

Identify the exact tool that manages the environment and write explicit
**DO / DO NOT** rules covering:

- The exact command to run the test suite
- How to install/sync dependencies
- How to lint and format
- Which alternatives are explicitly forbidden

Mark this section `— CRITICAL` so agents cannot miss it.

### 3. Conventions (non-obvious only)

Cover naming patterns and the canonical source-of-truth files agents must
respect when adding new parameters or configuration keys.

### 4. Testing Guidelines

- Where tests live and how they map to source modules
- Whether external I/O must be mocked
- Rules about keeping tests in sync when function signatures change

### 5. Common Operations

One shell code block with one-liner comments for the 4–6 most frequent tasks
(test, lint, build, deploy, docs preview, etc.).

## Style rules

- Write in **English**.
- Be prescriptive ("ALWAYS", "NEVER", "Do NOT"), not descriptive.
- Omit content already in `README.md` — link there instead.
- Prefer bullet lists and short paragraphs over prose.
