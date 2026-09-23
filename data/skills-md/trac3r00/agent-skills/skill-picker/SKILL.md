---
name: skill-picker
description: Finds the right skills for your workload from the catalogue. Queries catalogue.json (generated from the actual skills/ directory, never hand-maintained) by persona, family, keyword, or tag, and outputs matching skills with install commands. Use it to answer "what should I install for X" without reading every SKILL.md.
when_to_use: You're setting up a new project or machine and want the right subset of skills for your workload, or you're recommending skills to someone else. NOT a marketplace client — it reads the local catalogue, it does not download anything.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [skills, catalogue, discovery, install, workflow]
---

# Skill Picker

43 skills is a lot. You don't need all of them — you need the ones that match
your workload. This answers "what should I install" in one command.

## Commands

```bash
python3 scripts/skill_picker.py                        # browse all, by family
python3 scripts/skill_picker.py --persona backend      # skills for a workload
python3 scripts/skill_picker.py --family security      # skills in a family
python3 scripts/skill_picker.py --search "token"       # keyword search
python3 scripts/skill_picker.py --tag security         # skills with a tag
python3 scripts/skill_picker.py --install backend      # copy-paste install cmds
```

## Personas

`coding`, `frontend`, `backend`, `devops`, `agentic`, `design`,
`verification`, `career`, `finance`, `macos`, `research`, `qa`

## Catalogue

`catalogue.json` at the repo root is generated from the actual `skills/`
directory by `generate_catalogue.py` — never hand-edited. Run
`generate_catalogue.py --check` in CI to catch stale catalogues.

## Workflow

1. `skill_picker.py --persona backend` → see what matches your work
2. `skill_picker.py --install backend` → get the copy-paste commands
3. Run them, done.

## Pairs with

`skill-sync` (after installing, unify everything into one directory),
`skill-decay` (periodic check: which installed skills are you actually using).
