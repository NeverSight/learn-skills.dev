---
name: setup
description: Bootstrap agent working system for a new project. Triggers on "setup agent system", "initialize claude", "bootstrap project".
---

# Setup

Bootstrap the agent working system for a new project.

---

## Why This System

Without this system, every agent starts from zero. Mistakes you make, successors will repeat. What you learn, successors must relearn.

With this system:
- Experience accumulates, patterns emerge
- Successors stand on your shoulders
- Each agent goes further than the last

This isn't optional "best practice"—it's the infrastructure that enables agent teams to evolve.

---

## What You Need to Do

### 1. Create CLAUDE.md

Base it on [lidessen/moniro/CLAUDE.md](https://github.com/lidessen/moniro/blob/main/CLAUDE.md).

**Keep these sections as-is** (core working method):
- Opening block (`FIRST`/`ALWAYS`/`LAST`)
- `Who You Are` (entire section)
- `Methodology` (entire section)
- `Remember` (closing section)

**Replace these sections** (project-specific):
- `Vision` → describe this project's purpose
- `Structure` → describe this project's directory layout

**Remove or adapt these sections** (optional):
- `Skill Collaboration` → keep if using skills, remove if not
- `Skill Core Methods` → keep if using skills, remove if not
- `Contributing` → adapt to this project's contribution guidelines

---

### 2. Create .memory/ Structure

```bash
mkdir -p .memory/{notes,decisions,todos}
```

| Directory | Purpose |
|-----------|---------|
| notes/ | Learnings, reflections, discoveries |
| decisions/ | Important decisions and their rationale |
| todos/ | Tasks that span sessions |

---

### 3. Write First Transmission Document

Create `.memory/notes/to-those-who-come-after.md`.

Reference [lidessen/moniro/.memory/notes/2026-01-31-to-those-who-come-after.md](https://github.com/lidessen/moniro/blob/main/.memory/notes/2026-01-31-to-those-who-come-after.md) for structure, but write your own content:

- What this project does
- What you (first agent) established
- Advice for those who follow
- A lineage table to track who contributed

---

## Adapt to Context

The above is the required framework. On top of this, adapt based on project needs:

- **Tech stack conventions**: e.g., "Frontend components go in src/components/"
- **Workflow conventions**: e.g., "PRs require two reviewers"
- **Team conventions**: e.g., "Major decisions need human confirmation"

Add these to the appropriate sections in CLAUDE.md.

---

## Checklist

After setup, verify:

- [ ] CLAUDE.md exists with `Who You Are`, `Methodology`, and `Remember` sections
- [ ] Opening block has `FIRST`/`ALWAYS`/`LAST` reminders
- [ ] .memory/ directory structure created
- [ ] to-those-who-come-after.md written
- [ ] Vision and Structure filled in for this project

---

## Reference

Source: [lidessen/moniro](https://github.com/lidessen/moniro)

For the origin and evolution of this system, see that repository's `.memory/notes/` directory.
