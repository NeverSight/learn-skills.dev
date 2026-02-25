---
name: ddd-guide
description: Document-Driven Development workflow for existing codebases. Provides systematic planning, documentation-first design, and implementation verification.
version: 1.0.0
license: MIT
metadata:
  category: workflow
  complexity: high
  original_source: https://github.com/robotdad/amplifier-collection-ddd
---

# Document-Driven Development (DDD) Guide

## Core Principle

**Documentation IS the specification. Code implements what documentation describes.**

DDD inverts traditional development: update documentation first, then implement code to match.

## Why DDD?

- **Catches design flaws early** - Before expensive code changes
- **Prevents documentation drift** - Docs and code stay synchronized
- **Enables human review** - Humans approve specs, not code
- **AI-friendly** - Clear specifications reduce hallucination

## Six-Phase Workflow

| Phase | Name | Command | Deliverable |
|-------|------|---------|-------------|
| 0-1 | Planning | /ddd 1-plan | plan.md |
| 2 | Documentation | /ddd 2-docs | Updated docs |
| 3 | Code Planning | /ddd 3-code-plan | code_plan.md |
| 4 | Implementation | /ddd 4-code | Working code |
| 5-6 | Finalization | /ddd 5-finish | Tested, committed |

## Core Techniques

### Retcon Writing

Document features as if they already exist. No future tense.

- Bad: "This feature will add..."
- Good: "This feature provides..."

### File Crawling

Process files one at a time to avoid context overflow:

1. Generate index with `[ ]` checkboxes
2. Process one file per iteration
3. Mark `[x]` when complete

### Context Poisoning Prevention

Eliminate contradictions:

- One authoritative location per concept
- Delete duplicates, don't update
- Resolve conflicts before proceeding

## When to Use DDD

**Use DDD for:**
- Multi-file changes
- New features in existing codebases
- Complex integrations

**Skip DDD for:**
- Typo fixes
- Single-file changes
- Emergency hotfixes

## References

See `@skills/ddd-guide/references/` for detailed documentation:

- `core-concepts/` - Techniques and methodologies
- `phases/` - Step-by-step phase guides
- `philosophy/` - Underlying principles

## Remember

**Documentation first.** If it's not documented, it doesn't exist.

**Retcon, don't predict.** Write as if the feature already exists.

**One source of truth.** Delete duplicates, don't update them.
