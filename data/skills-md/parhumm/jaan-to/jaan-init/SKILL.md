---
name: jaan-init
description: Initialize jaan-to for the current project with directory setup and seed files. Use when setting up jaan-to in a new project.
allowed-tools: Read, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh), Edit(.gitignore)
argument-hint: (no arguments)
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# jaan-init

> Activate jaan-to for the current project.

## Context Files

- `${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh` - Bootstrap script that creates directories and seeds files
- `$JAAN_LEARN_DIR/jaan-to-jaan-init.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Arguments**: $ARGUMENTS

No arguments required. This skill initializes jaan-to in the current project directory.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `jaan-init`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_jaan-init`

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Check Current State

Check if `jaan-to/` directory already exists in the project root.

**If `jaan-to/` exists:**
Tell the user: "jaan-to is already initialized for this project. Bootstrap runs automatically on each session."
Stop here — do not proceed.

**If `jaan-to/` does NOT exist:**
Continue to Step 2.

## Step 2: Explain What Will Be Created

Show the user what initialization will create:

```
jaan-to/
  config/settings.yaml    — Project configuration
  context/                 — Project context files (tech.md, team.md, etc.)
  templates/               — Custom template overrides (initially empty; read from plugin at runtime)
  outputs/                 — Generated outputs from skills
  learn/                   — Project-specific lessons (initially empty; created via /jaan-to:learn-add)
  docs/                    — Reference docs (STYLE.md, create-skill.md)
```

Also mention: `jaan-to/` will be added to `.gitignore`.

---

# HARD STOP - Human Review Gate

Ask the user:

```
Initialize jaan-to for this project?

This will create the jaan-to/ directory with config, context, templates,
outputs, learn, and docs subdirectories.

Proceed? [y/n]
```

**Do NOT proceed without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 3: Run Bootstrap

Execute the bootstrap script to create directories and seed all files:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh
```

Note: The bootstrap script creates the `jaan-to/` directory and all subdirectories internally. It handles:
1. Creating all subdirectories (outputs, learn, context, templates, config, docs)
2. Copying seed context files (tech.md, team.md, integrations.md, etc.)
3. Copying reference docs
4. Initializing settings.yaml
5. Adding `jaan-to/` to `.gitignore`

Templates and learn files are loaded from the plugin at runtime (lazy loading).
Customize templates by copying them to `jaan-to/templates/`.
Add project lessons via `/jaan-to:learn-add`.

## Step 4: Report Result

Show the user the bootstrap output and summarize:

```
jaan-to initialized successfully.

Next steps:
- Edit jaan-to/context/tech.md with your project's tech stack
- Run /jaan-to:detect-pack for a full project analysis
- Run any skill: /jaan-to:pm-prd-write "feature name"
```

## Step 5: Capture Feedback

Ask the user:
```
Have feedback to improve future initializations?
Use: /jaan-to:learn-add "jaan-init" "lesson"
```

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] `jaan-to/` directory exists with subdirectories: outputs/, learn/, context/, templates/, config/, docs/
- [ ] `jaan-to/config/settings.yaml` exists
- [ ] Context seed files copied to `jaan-to/context/`
- [ ] `.gitignore` contains `jaan-to/` entry
- [ ] User informed of next steps
- [ ] User has approved final result

---

## Error Handling

### Permission Error
> "Could not create jaan-to/ directory. Check file permissions for the project root."

### Bootstrap Script Missing
> "Bootstrap script not found at ${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap.sh. Plugin may be corrupted — try reinstalling."

---

## Trust Rules

1. **NEVER** create directories without user confirmation
2. **ALWAYS** show what will be created before proceeding
3. **ALWAYS** check if already initialized before acting
