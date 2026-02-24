---
name: user-story-creator
description: Synthesize completed work into structured User Stories with intelligent subtask grouping. Use when you want to document development activities as a formal User Story (HU) with subtasks, acceptance criteria, and technical narrative. Triggered by user request "/user-story" or when suggesting story creation after completing work.
license: MIT
metadata:
  author: aroldolanderos
  version: "1.0.0"
---

# User Story Creator

## Overview

Convert session context into well-structured User Stories (Historias de Usuario). After completing development activities, use this skill to synthesize work into a formal narrative that:

- Summarizes high-level benefits (who, what, why)
- Groups changes into logical, atomic subtasks
- Documents technical actions in future tense
- Includes acceptance criteria and technical validation

**Key principle**: The story documents "what will be done" not "what was done" — written in future tense as if planning the implementation.

## When to Use This Skill

- After resolving one or more issues and want to document as a formal User Story
- When you've completed features, bug fixes, or refactoring and need to synthesize the narrative
- When you need to group technical changes (file modifications, API updates, schema changes) into logical subtasks
- To create audit-ready documentation for stakeholders unfamiliar with implementation details

**Not automatic**: Always request explicitly or confirm when suggested. Never generate unsolicited.

## Workflow

### 1. Provide Context

When you request the skill, give me:

- Summary of what was completed (or I'll infer from conversation history)
- Key modules/files affected (optional — I can analyze from git context)
- The main goal or benefit delivered

### 2. I Generate the Structure

I will:

1. **Extract commit labels** from your recent commits (feat, fix, refactor, etc.)
2. **Group changes logically** using these heuristics:
   - **<12 files/changes** → One subtask per logical grouping (module-based, component-based)
   - **≥12 files/changes** → Group by module, feature area, or architectural layer (avoid both overly generic and overly specific)
3. **Auto-generate title** with "HU - " prefix
4. **Create subtasks** with appropriate prefix (Feature:, Fix:, Refactor:, etc.)
5. **Propose acceptance criteria** based on changes made

### 3. Review & Approve

I'll present the story in **plain text format** (easy to copy) and ask for approval before finalizing.

## Output Format

See [references/template.md](references/template.md) for the exact structure.

**Key characteristics**:

- **Historia de Usuario** header with descriptive title
- **Cómo/Quiero/Para** format (always "Cómo: Desarrollador")
- **Subtareas** with prefixes: `Feature:`, `Fix:`, `Refactor:`, `Chore:`, `Docs:`, `Test:`, `Perf:`, `Style:`, `Build:`, `CI:`, `Env:`
- **Future tense** throughout (Implementar, Refactorizar, Validar, etc.)
- **Descripción** for each subtask (1-2 lines explaining the "why" and scope)
- **Acciones a Realizar** (atomic, concrete actions—2-5 bullets per subtask)
- **Criterios de Aceptación** (system behavior verification, regression prevention)

## Grouping Logic

See [references/grouping-guide.md](references/grouping-guide.md) for detailed heuristics.

**Quick rules**:

- Related changes → same subtask (e.g., model update + schema update for one feature)
- Module-based grouping when many changes across multiple modules
- Independent changes → separate subtasks
- Balance: Aim for 3-8 subtasks per story (fewer if simple, more only if substantially complex)

## Commit Label Mapping

See [references/commit-labels.md](references/commit-labels.md) for how commit messages map to subtask prefixes.

**Common mappings**:

- `feat:` → `Feature:`
- `fix:` → `Fix:`
- `refactor:` → `Refactor:`
- `test:` → `Test:`
- `docs:` → `Docs:`

## Example

See [references/examples.md](references/examples.md) for 2-3 realistic examples from actual development sessions.

---

**Ready?** Just say "Create a user story" or share what you want to document!
