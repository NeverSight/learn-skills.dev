---
name: project-safety
description: "Set up safety rules and folder structures for research projects. Prevent accidental data loss when Claude reorganizes files. Triggers: 'protect my data', 'set up project safety rules'. Not for auditing structure — use /audit-project-research."
argument-hint: [project-path]
---

# Project Safety Skill

**CRITICAL RULE: Never delete data or code files. Never.** Use legacy/ folder for originals. Copy, don't move.

> Establish safety rules and structures before Claude makes changes to research projects.

## Purpose

Based on Scott Cunningham's workflow: prevent accidental data loss by establishing rules and using legacy folders before Claude reorganizes or modifies project files.

## When to Use

- Starting a new research project folder
- Before asking Claude to reorganize files
- When Claude will be running code or modifying data
- Setting up a project for collaborative work

---

## Safety Rules Template

Add this to any project's CLAUDE.md file:

```markdown
## Safety Rules

1. **Never delete data files** — No .csv, .dta, .xlsx, .parquet, or any data format
2. **Never delete code files** — No .py, .R, .do, .tex, .md or scripts
3. **Use legacy/ folder** — If reorganizing, move originals to legacy/ first
4. **Copy from legacy, don't move** — Always preserve the original

### If you need to reorganize:
1. Create a legacy/ folder if it doesn't exist
2. Move ALL original files into legacy/
3. Copy (not move) needed files into new structure
4. Never modify anything in legacy/
```

---

## Directory Structure

After safety setup:

```
project/
├── CLAUDE.md           ← Safety rules + project context
├── README.md           ← Project documentation
├── legacy/             ← PROTECTED: original files
│   └── [all originals]
├── code/
│   ├── R/
│   ├── python/
│   └── stata/
├── data/
│   ├── raw/            ← Copied from legacy, never modified
│   └── processed/
├── output/
│   ├── figures/
│   └── tables/
├── docs/
│   └── manuscript/
└── log/                ← Progress logs
```

---

## Dry Run Pattern

Before Claude executes potentially destructive operations, ask for a preview:

> "Tell me what commands you would run to reorganize this folder, but don't execute them yet."

> "Show me what files would be affected by this change before you make it."

> "Walk me through your plan for cleaning this data before you run any code."

**When to use dry runs:**
- File operations (move, delete, rename)
- Git operations (reset, clean, force push)
- Database operations
- Batch processing
- Any operation affecting multiple files

**After reviewing:**
- If correct: "Go ahead"
- If wrong: "Wait — don't do X, instead Y"

---

## Workflow

1. **Create CLAUDE.md** with safety rules
2. **Create legacy/ folder**
3. **Move all originals to legacy/**
4. **Copy needed files** into new structure
5. **Verify** legacy/ contains everything
6. **Proceed** with project work

---

## Prompt Template

```
I'm starting work on [PROJECT]. Before we do anything:

1. Create a CLAUDE.md with safety rules (never delete data/code, use legacy folder)
2. Create a legacy/ folder
3. Move all existing files into legacy/
4. Show me the proposed new directory structure before creating it

Do a dry run first — tell me what you would do before doing it.
```

---

## Why This Matters

- Claude operates at speed — mistakes happen fast
- You can't always verify what Claude will do before it does it
- Version control (git, Dropbox) helps but prevention is better
- The legacy/ folder is your safety net
- Dry runs give you a chance to catch mistakes

---

## Example Use

"Set up my new Carbon Markets project with proper safety rules. Create the CLAUDE.md, legacy folder, and recommended directory structure. Show me your plan before executing."
