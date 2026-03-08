---
name: parallel-docs-simplify-sync
description: >-
  Runs synapse-docs, /simplify, sync-plugin-skills, and github-pages-sync
  in parallel for synapse-a2a development workflows. Use when you need doc
  updates, code simplification, plugin skill sync, and site-docs sync at the
  same time.
commands:
  - /parallel-docs-simplify-sync
---

# Parallel Docs Simplify Sync

Coordinate four independent skills in parallel using the **Task tool**.

> **Dev-focused orchestration skill.** The canonical source lives in
> `plugins/synapse-a2a/skills/` and is synced to `.agents/skills/` and
> `.claude/skills/`.

- `synapse-docs` — documentation updates
- `/simplify` — Claude Code built-in code simplification (replaces custom code-simplifier)
- `sync-plugin-skills` — plugin skill synchronization
- `github-pages-sync` — GitHub Pages site synchronization

## When To Use

- Code and documentation were changed in the same task.
- Simplification or refactor cleanup is needed while keeping docs in sync.
- Plugin-skill synchronization should happen in the same run.
- GitHub Pages site (`site-docs/`) needs to reflect code or doc changes.

## Parallel Execution Workflow

### Step 1: Split into four independent sub-tasks

Define one clear objective and divide it:

| Track | Skill | Typical Scope |
|-------|-------|---------------|
| Docs | `synapse-docs` | README.md, guides/, CLAUDE.md |
| Simplify | `/simplify` (built-in) | Recently changed `.py` files |
| Sync | `sync-plugin-skills` | plugins/synapse-a2a/skills/ |
| Pages | `github-pages-sync` | site-docs/ |

### Step 2: Launch four Task tool calls in a single message

Use the **Task tool** with four parallel invocations in one response.
Each Task call should use the prompt template below.

```text
# Example: four parallel calls (3 Task agents + 1 Skill)
Task(subagent_type="general-purpose", prompt="[synapse-docs prompt]")
Skill("simplify")
Task(subagent_type="general-purpose", prompt="[sync-plugin-skills prompt]")
Task(subagent_type="general-purpose", prompt="[github-pages-sync prompt]")
```

### Step 3: Wait for all four outputs

All four tasks return independently. Collect results before merging.

### Step 4: Merge and resolve conflicts

Apply changes from each track. If conflicts arise, follow the
**Conflict Resolution Rules** below. Run tests after merging.

### Step 5: Retry failed tracks only

If any track fails, rerun only that track. Do not re-execute all four.

## Task Prompt Template

Use this for each parallel track:

```text
Goal: <shared task goal>
Track: <synapse-docs | simplify | sync-plugin-skills | github-pages-sync>
Scope: <files/areas>
Constraints:
- Keep behavior unchanged unless explicitly requested
- Keep style consistent with repository conventions
- Do NOT touch files outside your track's scope
Deliverable:
- Concise change summary and touched files
```

## Conflict Resolution Rules

`synapse-docs` and `sync-plugin-skills` can both modify files under
`plugins/synapse-a2a/skills/`. When this happens:

1. **sync-plugin-skills wins** for skill SKILL.md content.
2. **synapse-docs wins** for README.md, guides/, and non-skill documentation.
3. If both modified the same SKILL.md, take `sync-plugin-skills` output and
   verify it against the doc changes from `synapse-docs`. Manually reconcile
   if descriptions diverge.
4. `/simplify` should never conflict because it only touches `.py` files.
5. `github-pages-sync` only modifies `site-docs/` and `mkdocs.yml`. If both
   `synapse-docs` and `github-pages-sync` modify `mkdocs.yml`,
   `github-pages-sync` takes priority because it owns the site build config.

## Completion Checklist

- [ ] All four tracks completed: `synapse-docs`, `/simplify`, `sync-plugin-skills`, `github-pages-sync`
- [ ] Conflicts resolved per rules above
- [ ] `pytest` passes
- [ ] `uv run mkdocs build --strict` passes (if Pages track ran)
- [ ] Final diff is coherent and reviewable
