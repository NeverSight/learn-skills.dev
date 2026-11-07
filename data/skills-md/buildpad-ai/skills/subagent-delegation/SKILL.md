---
name: subagent-delegation
description: Delegates focused work to Kiro subagents that run in isolated context. Use when work can run in parallel, when a specialized agent fits (code review, testing, security, research), or when a long task would otherwise bloat the main conversation. Trigger with "run subagents to ...".
---

# Subagent Delegation

## Overview

A subagent is a focused task handed to an agent that runs in its **own isolated context**. Kiro launches subagents automatically when a request matches an agent's `description`, or on demand when you say "Run subagents to ...". Use them to keep the main conversation lean, run independent tracks in parallel, or chain specialists into a pipeline.

Subagents are Markdown files in `.kiro/agents/` (workspace) or `~/.kiro/agents/` (user). This starter ships three, mirrored from `.github/agents/`:

| Subagent | Delegate when you need… |
|---|---|
| `code-reviewer` | Five-axis review (correctness, readability, architecture, security, performance) + Buildpad/DaaS compliance, after writing or changing code |
| `test-engineer` | Test-suite design, coverage-gap analysis, or writing Playwright/Vitest tests |
| `security-auditor` | Security review of auth, CORS, access rules (RLS on a Supabase project), input handling, secrets |

## When to Delegate

- **Parallel, independent work** — several read-only research tracks, or reviewing multiple modules at once.
- **Specialized review** — hand a finished slice to `code-reviewer` / `security-auditor` instead of self-reviewing inline.
- **Context isolation** — a large exploration (e.g., "map how auth flows through the app") would flood the main context; a subagent returns just the summary.
- **Pipelines** — implement → `code-reviewer` → `security-auditor`, each stage building on the last.

## When NOT to Delegate

- The task is trivial or you need tight, iterative back-and-forth.
- Steps share mutable state or must run in strict order (collection definitions or DB migrations, a single edit sequence).
- The subagent would need most of your current context to make progress — the hand-off cost outweighs the benefit.

Delegation adds coordination overhead. If a task is small and sequential, just do it on the main thread.

## How to Delegate

1. **Write a self-contained brief.** Subagents do NOT see your conversation. State the goal, the exact files/paths, constraints, and the output you want back.
2. **Launch.** Let Kiro auto-match by description, or be explicit: "Run subagents to review `app/items/` with code-reviewer and audit `app/api/auth/` with security-auditor."
3. **Parallelize only independent work.** For work that shares an interface, define the contract first (see `planning-and-task-breakdown`), then fan out.
4. **Integrate on the main thread.** Treat subagent output as advisory. Apply fixes, resolve conflicts, and run the build/tests yourself before declaring done.

## Patterns

```
Fan-out (research):    main ─┬─ subagent: "map data model in src/collections"
                             ├─ subagent: "list all /api routes + auth guards"
                             └─ subagent: "inventory Buildpad components used"
                        main merges the three summaries.

Pipeline (quality):    implement slice → code-reviewer → security-auditor → fix → verify

Map (review at scale):  one code-reviewer subagent per changed module, in parallel
```

## DaaS / Buildpad Notes

- Route Buildpad-First and proxy-pattern compliance checks to `code-reviewer`.
- Route CORS, access-rule (RLS on a Supabase project) and secret-handling checks to `security-auditor`, and OAuth checks on a Supabase project; on an Engine project the only OAuth sign-in is XAppHub, so the OAuth review there covers XAppHub sign-in only.
- Route Playwright coverage and RBAC test design to `test-engineer`.
- Give research subagents the MCP context they need (project detail, collection schemas) in the brief — they start with a clean context.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Delegating is always faster" | Only for independent or isolatable work. Sequential, shared-state work is slower split up. |
| "The subagent knows what I know" | It starts fresh. An underspecified brief produces a useless result. |
| "I'll skip the main-thread verification" | Subagent output is advisory. Nothing is done until the build and tests pass on the main thread. |

## Red Flags

- Delegating a task that needs your live context to make sense.
- Parallelizing work that shares an API contract without defining it first.
- Accepting subagent results without integrating and verifying them.
- Spawning subagents for a one-file change.

## Verification

- [ ] Each delegated task had a self-contained brief (goal, files, constraints, expected output).
- [ ] Only independent work was parallelized; shared contracts were defined first.
- [ ] Subagent results were integrated on the main thread.
- [ ] Build and tests pass after integration.
