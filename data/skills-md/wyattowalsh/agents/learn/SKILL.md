---
name: learn
description: >-
  Capture corrections, insights, and patterns as reusable project knowledge.
  Routes learnings to the right instruction file. Applies kaizen: small
  improvements, error-proofing, standards work. Auto-invoked when a correction
  pattern is detected 3+ times. Also use manually when Claude makes a
  repeated mistake, discovers a non-obvious gotcha, or when you want to
  persist a workflow preference.
argument-hint: "[correction or insight to capture]"
user-invocable: true
disable-model-invocation: false
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Learn — Capture and Route Project Knowledge

Record corrections, insights, and patterns. Route them to the correct instruction file. Apply kaizen principles to keep instructions lean and effective.

## Dispatch

| `$ARGUMENTS` | Action |
|---|---|
| `"<correction text>"` | Route correction to appropriate instruction file |
| `review` | Show pending learnings and their frequency |
| `promote` | Promote high-frequency learnings (3+ occurrences) to instruction files |
| `audit` | Check for stale, contradictory, or duplicate learnings |
| Empty | Display usage summary |

## References

| File | Purpose |
|------|---------|
| `references/routing-rules.md` | Decision tree for where to route instruction changes |
| `references/kaizen-principles.md` | Error-proofing patterns, when to use hooks vs prose vs rules |

## Routing Protocol

Route proposed updates to the correct target:

| Scope | Target |
|-------|--------|
| Cross-project conventions | `instructions/global.md` |
| Language-specific tooling | Convention skill (`python-conventions`, etc.) |
| Orchestration/parallelism | `orchestrator` skill body |
| Project-specific standards | Project's `AGENTS.md` |
| File-scoped enforcement | `.claude/rules/<topic>.md` |
| Skill behavior | The skill's own `SKILL.md` |

### Routing Decision Steps

1. Determine the scope: does this apply to all projects or just one?
2. If cross-project, does it relate to a specific language or tool?
3. If language-specific, route to the corresponding convention skill
4. If general, route to `instructions/global.md`
5. If project-only, route to the project's `AGENTS.md`
6. If file-scoped enforcement only, create a `.claude/rules/` entry

## Kaizen Principles

1. **Incremental > revolutionary** — Smallest viable change, verify before next
2. **Poka-yoke** — Prefer hooks/tooling over prose instructions (error-proof by design)
3. **Standards work** — Follow existing patterns, document what works
4. **JIT** — Build only what is needed, optimize when measured

## Verification Checklist

1. Verify against actual practice — confirm the pattern reflects real usage
2. Check for contradictions with existing instructions
3. Assess token impact — keep always-loaded content minimal
4. Get user approval — never modify instruction files without consent
5. Test the change — run `wagents validate` after any instruction file edit

## Critical Rules

1. Never modify instruction files without explicit user approval
2. Require 3+ corrections across 2+ sessions before promoting
3. Check for contradictions with existing instructions
4. Route to narrowest applicable scope (rule before skill, skill before global)
5. Keep always-loaded content under token budget
6. Run `wagents validate` after every instruction file modification
7. Prefer hooks/rules over prose (poka-yoke principle)

## Canonical Terms

- `instruction file` — any file that provides agent instructions (global.md, AGENTS.md, SKILL.md)
- `routing` — the process of choosing the correct target file for a change
- `correction pattern` — a repeated fix that indicates a missing or wrong instruction
- `token budget` — the limit on always-loaded instruction content
- `scope` — cross-project, language-specific, orchestration, project-specific, or file-scoped
