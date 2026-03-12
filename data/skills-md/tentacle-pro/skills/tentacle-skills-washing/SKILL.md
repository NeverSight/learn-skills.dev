---
name: tentacle-skills-washing
description: |
  Adapt, repair, and environment-proof Agent Skills so they run correctly in this vault. Use this skill when: (1) A downloaded or third-party skill needs to be installed/adapted to this vault's runtime (uv/bun), folder conventions, and path rules. (2) An existing skill fails or errors at runtime due to environment issues—wrong Python/TS runner, broken paths, missing inline dependencies, incorrect execution commands, or artefacts written to the wrong location. (3) A skill's shipped docs (AGENTS.md / SKILL.md) conflict with this vault's standards and need to be reconciled. 
  Triggers: "wash this skill", "fix this skill", "this skill is broken", "adapt skill from", "install skill", "skill throws an error", "skill can't find", "update skill to work here".
---

# Skill: tentacle-skills-washing

## Purpose

Adapt a downloaded third-party Agent Skill so it runs correctly in **this vault's** runtime environment and respects its folder conventions.

## When to Invoke

User says something like:
- "wash this skill"
- "install/adapt this skill from [source/path]"
- "I downloaded a skill, make it work here"

---

## Required Reading Before Acting

Always read these files first — do not proceed without them:

1. `AGENTS.md` (vault root) — folder rules, naming, artefact boundaries
2. `.agents/skills/AGENTS.md` — Python/TS runtime standards, execution commands

---

## Inputs

| Input | Description |
|-------|-------------|
| `skill_path` | Path to the downloaded skill directory, relative to vault root (e.g. `.agents/skills/my-downloaded-skill/`) |

---

## Washing Protocol

Work through each step in order. Check off items as you verify or fix them.

### Step 1 — Inventory

- [ ] List all files in the skill directory
- [ ] Identify primary entry point (`main.py`, `main.ts`, or equivalent)
- [ ] Note language(s) used (Python / TypeScript / shell)

### Step 2 — Python scripts

- [ ] Remove `requirements.txt`, `setup.py`, `.venv/` if present
- [ ] Add PEP 723 inline metadata to every standalone `.py` file (see `.agents/skills/AGENTS.md`)
- [ ] Replace any `python main.py` / `pip install` execution instructions with `uv run .agents/skills/<skill-name>/main.py [args]`

### Step 3 — TypeScript scripts

- [ ] Ensure `package.json` exists inside the skill directory
- [ ] Verify dependencies are installed locally (`bun add` inside the skill dir)
- [ ] Replace execution instructions with `bun .agents/skills/<skill-name>/main.ts [args]`

### Step 4 — Path references

- [ ] Replace all absolute paths or author-machine-specific paths with vault-root-relative paths
- [ ] Any file I/O that reads vault notes must target the correct folders per root `AGENTS.md`
- [ ] Any file I/O that writes logs/temp files must stay inside `.agents/skills/<skill-name>/`

### Step 5 — Shipped docs (AGENTS.md / README / SKILL.md)

- [ ] If the skill ships its own `AGENTS.md`: review for conflicts with our standards; remove duplicates; keep only skill-specific overrides
- [ ] If the skill ships a `SKILL.md`: update execution commands and paths to match local standards; preserve the original's purpose description and parameter contracts
- [ ] If the skill ships neither: create a minimal `SKILL.md` describing what it does and how to invoke it

### Step 6 — Obsidian data integrity

- [ ] If the skill reads `.md` files: confirm it preserves YAML frontmatter
- [ ] If the skill writes `.md` files: confirm it uses wikilink syntax `[[Page Name]]` for cross-references
- [ ] Confirm it does NOT write `.log`, `.tmp` artefacts outside its own directory

### Step 7 — Smoke test

Instruct the user to run the adapted skill with a minimal input and verify it executes without errors.

---

## Output Contract

A skill directory at `.agents/skills/<skill-name>/` that:

- Runs via `uv run` or `bun` without any extra setup
- Contains a `SKILL.md` summarising purpose, inputs, and invocation command
- Leaves no artefacts outside its own directory
- Does not conflict with vault-wide rules in root `AGENTS.md`

---

## Reference Artefacts in This Directory

| File | Purpose |
|------|---------|
| `AGENTS-template.md` | Template for generating vault-level `AGENTS.md` when bootstrapping a new vault |
