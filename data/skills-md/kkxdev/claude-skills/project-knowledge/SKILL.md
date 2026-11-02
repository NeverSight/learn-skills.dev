---
name: project-knowledge
description: "Generate project knowledge for any git repo: code graph, knowledge graph, code wiki, and AI-written domain docs under .ai/. Use when onboarding to a repo, asked to document a codebase, or to refresh stale .ai/ knowledge."
trigger: /project-knowledge
---

# /project-knowledge

Deterministic facts first (code graph, knowledge graph, code wiki), then narrative docs written from those facts.

## Usage

```
/project-knowledge            # current repo
/project-knowledge <path>     # another repo
```

## Step 1: deterministic artifacts (no model, stdlib Python 3.9+)

```
python3 ~/.claude/skills/project-knowledge/scripts/build_knowledge.py <repo> [--rules rules.json] [--name NAME]
```

Writes (all derived from the code, nothing invented; capped in size):

- `.ai/graph/code-graph.json`: files, symbols, import edges (Python, JS/TS, PHP, Java)
- `.ai/graph/knowledge-graph.json`: modules, hub files, optional rules linked to the modules they govern
- `.ai/wiki/code-wiki.md`: most-imported hub files + module map with top symbols
- `.ai/wiki/knowledge-wiki.md`: optional rules grouped by kind

`rules.json` is optional: `[{"id","kind","text","scope_paths","source"}]`, kind one of convention/decision/constraint/gotcha/other. Only include rules the user has confirmed.

## Step 2: narrative docs (you write these)

Read `.ai/wiki/code-wiki.md` and the hub files first; do not re-explore the whole tree. Then write:

- `.ai/domain/*.md`: one file per business domain/module cluster: purpose, key entry points, invariants, gotchas. Cite real paths.
- `.ai/danger-zones.yaml`: hub files and fragile areas (use the hub list as the starting evidence).
- `CLAUDE.md`: minimal; point to `.ai/wiki/code-wiki.md` and `.ai/domain/`. Do not overwrite an existing CLAUDE.md; append a short "Project knowledge" section instead.

Rules: state only what you verified in code; mark anything inferred as such; keep files short, they are read on demand.

## Step 3: report

Summarise files written and graph stats. Do not commit; leave the diff for the user to review. Suggest adding `.ai/graph/*.json` to `.gitignore` if the repo is large.
