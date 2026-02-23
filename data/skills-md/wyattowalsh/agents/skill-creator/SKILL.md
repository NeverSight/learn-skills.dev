---
name: skill-creator
description: >-
  Create, improve, and audit AI agent skills. Applies 14 proven structural
  patterns, scores quality with deterministic audit, manages full lifecycle.
  Use when building, refactoring, or reviewing skills.
  NOT for agents, MCP servers, or running existing skills.
argument-hint: "<mode> [name]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "2.0.0"
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - command: "echo 'skill-creator: Bash access granted for script execution'"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "jq -r '.tool_input.file_path // empty' | grep -q 'skills/.*/SKILL.md' && wagents validate 2>/dev/null || true"
---

# Skill Creator

Create, improve, and audit AI agent skills. Every skill follows 14 proven structural patterns.

**Scope:** Skills only. NOT for creating agents (`wagents new agent`), building MCP servers (`/mcp-creator`), or running existing skills. This repo uses raw `SKILL.md` format committed directly to `skills/`.

## Dispatch

| $ARGUMENTS | Action | Example |
|------------|--------|---------|
| `create <name>` / `new <name>` | Develop (new) | `/skill-creator create my-analyzer` |
| `create <name> --from <source>` | Develop (new, from exemplar) | `/skill-creator create my-analyzer --from wargame` |
| `improve <name>` / `improve <path>` | Develop (existing) | `/skill-creator improve add-badges` |
| `audit <name>` | Audit | `/skill-creator audit honest-review` |
| `audit --all` | Audit All | `/skill-creator audit --all` |
| `dashboard` | Dashboard | `/skill-creator dashboard` |
| `package <name>` / `package --all` | Package | `/skill-creator package wargame` |
| Natural language skill idea | Auto: Develop (new) | `"tool that audits Python type safety"` |
| Skill name + modification verb | Auto: Develop (existing) | `"refactor the wargame skill"` |
| Path to SKILL.md | Auto: Develop (existing) | `skills/wargame/SKILL.md` |
| "MCP server" / "agent" / "run" | Refuse + redirect | — |
| Empty | Gallery | `/skill-creator` |

### Auto-Detection Heuristic

If no explicit mode keyword is provided:

1. Path ending in `SKILL.md` or directory under `skills/` → **Develop (existing)**
2. Existing skill name + modification verb (improve, refactor, enhance, update, fix, rewrite, optimize, polish, revise, change) → **Develop (existing)**
3. `--from <source>` in arguments → **Develop (new, from exemplar)**
4. New capability description ("I want to build...", "tool that...", "skill for...") → **Develop (new)** — derive name, confirm before scaffolding
5. "MCP server", "agent", "run" → refuse gracefully and redirect
6. Ambiguous → ask the user which mode they want

## Quick Start

```bash
wagents new skill <name>           # Scaffold from template
wagents validate                   # Check all skills
uv run python skills/skill-creator/scripts/audit.py skills/<name>/  # Score quality
wagents package <name>             # Package as portable ZIP
```

## Skill Development

Unified process for creating new skills and improving existing ones. Load `references/workflow.md` for the full procedure.

| Step | New Skill | Existing Skill |
|------|-----------|----------------|
| 1. Understand | Define use cases, scope, patterns | Audit + understand user's intent |
| 2. Plan | Structure, description, frontmatter | Gap analysis + improvement plan (approval gate) |
| 3. Scaffold | `wagents new skill <name>` | Skip |
| 4. Build | Write/edit body, references, scripts, templates, evals | Same |
| 5. Validate | `wagents validate` + `audit.py` | Same |
| 6. Iterate | Test, identify issues, loop to Step 4 | Same |

## Audit

Score a skill using deterministic analysis + AI review. Load `references/audit-guide.md`.

## Audit All

Comparative ranking of all repository skills. Load `references/audit-guide.md` § Audit All.

## Dashboard

Render visual creation process monitor or audit quality dashboard. Load `references/audit-guide.md` § Dashboard.

Auto-detects mode from data: `phases` field → process monitor; `skills` array → audit overview.

## Gallery (Empty Arguments)

Present skill inventory with scores and available actions.
Run `uv run python skills/skill-creator/scripts/audit.py --all --format table`, display results, offer mode menu.

## Package

Package skills into portable ZIP files for Claude Code Desktop import. Load `references/packaging-guide.md` for ZIP structure, manifest schema, portability checks, and cross-agent compatibility.

```bash
wagents package <name>            # Single skill → <name>-v<version>.skill.zip
wagents package --all             # All skills → dist/ with manifest.json
wagents package --all --dry-run   # Check portability without creating ZIPs
```

## Hooks

PreToolUse hooks intercept tool calls during skill execution. The `hooks:` frontmatter field scopes hooks to this skill only — they activate when the skill is loaded and deactivate when it completes.

## State Management

Creation progress persists at `~/.claude/skill-progress/<name>.json`. Read/write via `scripts/progress.py`. Survives session restarts. Use `--state-dir` to override the default location.

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/workflow.md` | Unified 6-step skill development process for new and existing skills | Develop (new), Develop (existing) |
| `references/audit-guide.md` | Audit procedure, Audit All, Dashboard rendering, Gallery, grade thresholds | Audit, Audit All, Dashboard, Gallery |
| `references/proven-patterns.md` | 14 structural patterns with examples from repo skills | Step 4 (Build), gap analysis |
| `references/best-practices.md` | Anthropic guide + superpowers methodology + cross-agent awareness | Step 2 (Plan), Step 4 (Build), description writing |
| `references/frontmatter-spec.md` | Full field catalog, invocation matrix, decision tree | Step 3 (Scaffold), frontmatter configuration |
| `references/packaging-guide.md` | ZIP structure, manifest schema, portability checks, import instructions | Package |
| `references/evaluation-rubric.md` | 11 scoring dimensions, grade thresholds, pressure testing | Audit (pressure testing), scoring targets |

Read reference files as indicated by the "Read When" column above. Do not rely on memory or prior knowledge of their contents.

## Core Principles

**Conciseness is respect** — The context window is shared. Every line competes with the agent's working memory. Earn every line or delete it.

**Progressive disclosure** — Frontmatter for discovery (~100 tokens), body for dispatch (<5K tokens), references for deep knowledge (on demand), scripts/templates for execution (never loaded).

**Self-exemplar** — This skill follows every pattern it teaches. When in doubt, look at how skill-creator applies it.

## Critical Rules

1. Run `uv run wagents validate` before declaring any skill complete
2. Run `uv run python skills/skill-creator/scripts/audit.py` after every significant SKILL.md change
3. Never create a skill without a dispatch table — it is the routing contract
4. Never create a dispatch table without an empty-args handler — unrouted input is a bug
5. Every reference file must appear in the Reference File Index — orphan refs are invisible
6. Every indexed reference must exist on disk — phantom refs cause agent errors
7. Body must stay under 500 lines (below frontmatter) — move detail to references
8. Description must include "Use when" trigger phrases AND "NOT for" exclusions
9. Names must be kebab-case, 2-64 chars, no consecutive hyphens, no reserved words
10. Scripts use argparse + JSON to stdout — no custom output formats
11. Templates are self-contained HTML with no external dependencies
12. Do NOT call `wagents docs generate` — delegate to docs-steward
13. Do NOT create agents or MCP servers — refuse gracefully and redirect
14. Improving existing skills requires presenting an improvement plan and getting user approval before implementing changes
15. Audit mode is read-only — never modify the skill being audited
16. Update evals when dispatch behavior or modes change — stale evals are invisible bugs

**Canonical terms** (use these exactly throughout):
- Modes: "Develop (new)", "Develop (existing)", "Audit", "Audit All", "Dashboard", "Package", "Gallery"
- Steps (Development): "Understand", "Plan", "Scaffold", "Build", "Validate", "Iterate"
- Grade scale: "A" (90+), "B" (75-89), "C" (60-74), "D" (40-59), "F" (<40)
- Patterns: "dispatch-table", "reference-file-index", "critical-rules", "canonical-vocabulary", "scope-boundaries", "classification-gating", "scaling-strategy", "state-management", "scripts", "templates", "hooks", "progressive-disclosure", "body-substitutions", "stop-hooks"
- Audit dimensions: "frontmatter", "description", "dispatch-table", "body-structure", "pattern-coverage", "reference-quality", "critical-rules", "script-quality", "portability", "conciseness", "canonical-vocabulary"
