---
name: agents-md-refactor
description: Use when refactoring long or conflicting AGENTS.md/CLAUDE.md/COPILOT.md into a minimal root file plus linked, topic-focused docs using progressive disclosure.
---

# AGENTS.md Refactor

## Goal

Restructure agent instruction files into a small, universal root plus linked, self-contained topic docs.

## Guardrails

- Resolve contradictions before reorganizing content.
- Keep root file short (target under ~80 lines).
- Put specifics (language, testing, style) in linked docs, not the root.
- Prefer a hidden folder `.agents/` unless the repo already uses another convention.

## Workflow (short)

1. Scan for contradictions and ask for precedence.
2. Extract root essentials and links only.
3. Group remaining guidance into 3–8 topic docs.
4. Create files and link from root.
5. Prune vague or redundant statements.
6. Verify links, coverage, and self-contained topics.

## References (load when needed)

- `agents-md-refactor/references/templates.md`: root and topic doc templates.
- `agents-md-refactor/references/checklist.md`: execution and verification checklist.
- `agents-md-refactor/references/triage.md`: contradiction patterns and resolution prompts.
