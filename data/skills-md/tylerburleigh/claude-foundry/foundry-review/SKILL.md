---
name: foundry-review
description: Review implementation fidelity against specifications by comparing actual code to spec requirements. Identifies deviations, assesses impact, and generates compliance reports for tasks, phases, or entire specs.
user-invocable: false
---

# Implementation Fidelity Review Skill

## Table of Contents

- [Overview](#overview)
- [Skill Family](#skill-family)
- [When to Use](#when-to-use-this-skill)
- [MCP Tooling](#mcp-tooling)
- [Core Workflow](#core-workflow)
- [LSP Operations Quick Reference](#lsp-operations-quick-reference)
- [Essential Commands](#essential-commands)
- [Review Types](#review-types)
- [Assessment Categories](#fidelity-assessment-categories)
- [Long-Running Operations](#long-running-operations)
- [Example Invocation](#example-invocation)

## Overview

The `foundry-review` skill compares actual implementation against SDD specification requirements. It uses LSP for structural verification and MCP for AI-powered deviation analysis.

## Skill Family

Part of the **Spec-Driven Development** quality assurance family:

```
foundry-spec → foundry-implement → [CODE] → foundry-review (this skill)
```

## When to Use This Skill

**Use when:**
- Verifying implementation matches specification requirements
- Identifying deviations between plan and actual code
- Reviewing pull requests for spec compliance
- Auditing completed phases or tasks

**Do NOT use for:**
- Creating specifications (use `foundry-spec`)
- Finding next tasks or tracking progress (use `foundry-implement`)
- Running tests (run directly via Bash)

### Flow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop · `§`=section ref

```
- **Entry** → [Familiar with code?]
  - [no] → Explore subagent
  - [else] → skip
  - Spec changes → `spec action="diff"` → `spec action="history"`
  - LSP pre-check → `documentSymbol`
    - [structures exist?] → continue
    - [else] → Early exit with findings → **Exit**: Report
  - MCP review → `fidelity action="review"` → Scope: phase or task
    - [deviations found?] → LSP investigate → `goToDefinition` → `findReferences` → `incomingCalls`
  - Assess deviation: Exact, Minor, Major, Missing
  - **Exit** → Report with recommendations
```

## MCP Tooling

This skill uses the Foundry MCP server with router+action pattern: `mcp__plugin_foundry_foundry-mcp__<router>` with `action="<action>"`.

**Critical Rules:**
- **ALWAYS** use MCP tools for spec operations
- **NEVER** use `Read()` on spec JSON files
- **NEVER** use shell commands (`cat`, `grep`, `jq`) on specs

### Router Actions

| Router | Action | Purpose |
|--------|--------|---------|
| `review` | `fidelity` | Run AI-powered fidelity analysis |
| `task` | `query` | List tasks for review scope |
| `task` | `info` | Get task details and acceptance criteria |
| `spec` | `diff` | Compare spec versions to understand changes |
| `spec` | `history` | View spec modification timeline |

### Spec Comparison for Fidelity Context

Use `spec:diff` and `spec:history` to understand what changed before reviewing implementation:

```bash
# See what changed since last review
mcp__plugin_foundry_foundry-mcp__spec action="diff" spec_id="{spec-id}" compare_to="specs/.backups/{spec-id}-previous.json"

# View modification history to understand evolution
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="{spec-id}" limit=5
```

**Why this helps fidelity review:**
- **diff**: Identifies which requirements changed, helping focus review on modified tasks
- **history**: Shows when requirements were added/modified, explaining apparent deviations that were actually spec updates

## Core Workflow

The fidelity review workflow integrates LSP verification with MCP AI analysis:

### Step 1: Gather Context (Optional)

For unfamiliar code, use Explore subagent to find implementation files:
```
Explore agent (medium thoroughness): Find all files in phase-1, related tests, config files
```

### Step 2: Check Spec Changes

Before reviewing, understand what changed in the spec since the last review:

```bash
# Check recent spec modifications
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="{spec-id}" limit=5

# Compare current spec against last backup
mcp__plugin_foundry_foundry-mcp__spec action="diff" spec_id="{spec-id}" compare_to="specs/.backups/{spec-id}-last-review.json"
```

**Deviation assessment using diff:**
```
📊 Spec Diff: user-auth-001

Tasks:
  ~ task-1-2: Acceptance criteria updated (added "support OAuth2")
  + task-1-4: New task added after initial implementation

Use this to:
- Focus review on changed requirements (task-1-2)
- Flag new tasks as "not yet implemented" rather than "deviation" (task-1-4)
- Explain apparent deviations that reflect spec evolution
```

### Step 3: LSP Structural Pre-Check

Before the AI review, verify structural requirements with LSP:

```python
# Get symbols in implementation file
symbols = LSP(operation="documentSymbol", filePath="src/auth/service.py", line=1, character=1)

# Compare against spec: expects AuthService with login(), logout(), refresh_token()
# Identify missing symbols before expensive AI review
```

**Why:** Catches missing implementations in seconds before 5-minute AI review.

### Step 4: MCP Fidelity Review

Run the AI-powered fidelity analysis:

```bash
# Phase review
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id="{spec-id}" phase_id="{phase-id}"

# Task review
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id="{spec-id}" task_id="{task-id}"
```

The MCP tool handles spec loading, implementation analysis, AI consultation, and report generation.

### Step 5: LSP-Assisted Investigation

For deviations found, use LSP to investigate:

```python
# Trace deviation origin
definition = LSP(operation="goToDefinition", filePath="src/auth/service.py", line=45, character=10)

# Find what depends on deviated code
calls = LSP(operation="incomingCalls", filePath="src/auth/service.py", line=45, character=10)

# Assess blast radius
refs = LSP(operation="findReferences", filePath="src/auth/service.py", line=45, character=10)
```

**Why:** Understand deviation impact before recommending fixes.

**CRITICAL:** Read [references/lsp-integration.md](./references/lsp-integration.md) before LSP investigation. Contains required operation patterns.

## LSP Operations Quick Reference

| Operation | When to Use | Purpose |
|-----------|-------------|---------|
| `documentSymbol` | Pre-check | List all symbols in a file for structural verification |
| `workspaceSymbol` | Pre-check | Find symbols across codebase |
| `hover` | During review | Get type info and documentation |
| `goToDefinition` | Investigation | Trace where symbols are defined |
| `findReferences` | Investigation | Find all usages of a symbol |
| `incomingCalls` | Investigation | Find what calls a function |
| `outgoingCalls` | Investigation | Find what a function calls |

## Essential Commands

**Query tasks before review:**
```bash
mcp__plugin_foundry_foundry-mcp__task action="query" spec_id="{spec-id}" parent="{phase-id}"
```

**Phase review:**
```bash
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id="{spec-id}" phase_id="{phase-id}"
```

**Task review:**
```bash
mcp__plugin_foundry_foundry-mcp__review action="fidelity" spec_id="{spec-id}" task_id="{task-id}"
```

> For query patterns and anti-patterns, see `references/querying.md`

## Review Types

| Type | Scope | When to Use |
|------|-------|-------------|
| **Phase Review** | 3-10 tasks | Phase completion checkpoints |
| **Task Review** | 1 file | Critical task validation, high-risk implementations |

> For detailed workflow per review type, see `references/review-types.md`

### Plan-Enhanced Review

When a spec has a linked `plan_path`, fidelity review automatically includes spec-vs-plan comparison. This is **not a separate review type** — it augments the standard phase or task review with additional plan alignment checks.

**Auto-triggered when:** Spec metadata contains `plan_path`
**No user action needed:** The MCP tool detects plan linkage and enhances the review automatically

The response includes a `plan_enhanced` boolean indicating whether plan comparison was performed.

## Fidelity Assessment Categories

| Category | Meaning |
|----------|---------|
| **Exact Match** | Implementation precisely matches specification |
| **Minor Deviation** | Small differences with no functional impact |
| **Major Deviation** | Significant differences affecting functionality |
| **Missing** | Specified features not implemented |

## Long-Running Operations

**This skill may take up to 5 minutes.** The MCP tool handles timeout internally.

**Never** use `run_in_background=True` with frequent polling.

## Example Invocation

```bash
Skill(foundry:foundry-review) "Review phase phase-1 in spec user-auth-001"
```

## Detailed Reference

For comprehensive documentation including:
- Long-running operations guidance → `references/long-running.md`
- Review types → `references/review-types.md`
- LSP integration patterns → `references/lsp-integration.md`
- Querying spec data → `references/querying.md`
- Workflow steps → `references/workflow.md`
- Report structure → `references/report.md`
- SDD workflow integration → `references/integration.md`
- Assessment categories → `references/assessment.md`
- Examples → `references/examples.md`
- Error handling → `references/errors.md`
- Best practices → `references/best-practices.md`
- Subagent patterns → `references/subagent.md`
