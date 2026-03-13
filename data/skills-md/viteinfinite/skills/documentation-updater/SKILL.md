---
name: documentation-updater
description: Use when implementing features, refactors, or fixes that affect core functionality, configuration, infrastructure, or integrations. Ensures documentation stays accurate by updating README, operational guides, and reference docs, and verifying links/commands remain correct.
---

# Documentation Updater

Maintain project documentation (README, operational guides, reference docs) as a first-class part of shipping changes. Keep documentation accurate and executable as code evolves.

## When to use

Activate this Skill when:

- A change alters **how to run/test locally** (development environment setup, containerization, bootstrapping).
- You add/remove/change **environment variables**, secrets, or configuration files.
- You change **environment/deployment assumptions** used by scripts or tools.
- You add/modify **operational scripts** (deployment, data seeding, logging, maintenance tasks).
- You update **integrations** with external services or APIs.
- You modify **infrastructure** setup or deployment processes.

## Principles

1. **Prefer updating existing docs over adding new ones.** Add a new doc only when it clearly reduces confusion.
2. **Keep docs executable.** Commands must match actual scripts/tools; paths must match the project structure.
3. **Respect environment requirements.** When docs tell users to run commands/tests, include the correct environment setup steps (e.g., sourcing environment files, activating virtual environments, loading configuration).
4. **Document "what & why", not internal trivia.** Focus on user outcomes and maintenance workflows.
5. **Cross-link instead of duplicating.** Use references to maintain a single source of truth.

## Workflow

### 1) Determine doc impact from the change

Identify what category the change falls into and what docs it likely affects.

### 2) Update the smallest set of docs that restores accuracy

- Update only the relevant sections; avoid broad rewrites.
- Keep headings and tone consistent with the existing file.
- Prefer adding links from main documentation to detailed reference docs for deep dives, instead of duplicating instructions.

### 3) Add "quick verification" steps

When documenting new or changed workflows, include:

- The exact command(s) to run (use project-standard task runners or scripts).
- The expected output/behavior at a high level (1–2 bullets).
- Any common failure mode and how to fix it (1 short subsection max).

### 4) Check for drift and broken references

- Confirm referenced scripts/commands exist in the project.
- Confirm file paths and directory references exist in the repository.
- Verify external links are still valid and accessible.
