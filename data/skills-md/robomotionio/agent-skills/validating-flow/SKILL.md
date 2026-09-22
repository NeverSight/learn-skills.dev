---
name: validating-flow
description: Validates a compiled Robomotion flow against pspec schemas via `robomotion validate <flow-dir>`. Exits 0 on clean, 1 on error with node-by-node report on stderr; no stdout output (composes in shell pipelines). Use when the user says "validate this flow", "check the flow", "is this correct", or before running. Does NOT run the flow — for behavioral tests use testing-flow.
---

# Validating a Robomotion Flow

Build + validate a flow against pspec schemas, including all subflows.

## When to use

- After writing or editing a flow with the TypeScript SDK
- Before running or committing a flow
- In a tight validate-then-fix loop while iterating

## Usage

```bash
robomotion validate <flow-dir>           # e.g. robomotion validate write-to-clipboard
robomotion validate                       # defaults to main.ts in cwd
robomotion validate path/to/main.ts       # also accepts a file
```

On success, exits 0 with `✔ <name> validated` on stderr and **no stdout** — composes cleanly:

```bash
robomotion validate write-to-clipboard/ && robomotion run write-to-clipboard/
```

On failure, exits 1 and prints structured node-by-node errors on stderr. Designer side files (`*.designer.ts`) are NOT regenerated on validate — use `robomotion build` when you want JSON output or designer refresh.

## What it checks

- Node property names against pspec schemas (catches typos, wrong casing, invented properties)
- Port numbers (exceeding a node's output count)
- Node types exist in their package's pspec

## What it does NOT check

- Loop wiring patterns (Goto→Label) — manual review
- Missing required properties — manual review
- Variable references (`Message('varName')` matching upstream writes) — manual review
- Business logic correctness

## Validate-then-fix loop

```bash
robomotion validate write-to-clipboard/    # exit 1, error report on stderr
# read the error, edit main.ts to fix, then:
robomotion validate write-to-clipboard/    # exit 0
```

## Common errors and fixes

| Error fragment | Fix |
|----------------|-----|
| `Unknown property 'inCode'` | Use `robomotion describe node <type>` to see the real property list. |
| `Node type X not found in pspec` | Use `robomotion get nodes <keyword>` to find the correct name. |
| `Invalid output port N` | Check node's output count with `robomotion describe node <type>`. |
| `Could not load pspec for Package` | Verify namespace spelling; use `robomotion get packages <keyword>`. |

## Pre-run checklist

- [ ] `robomotion validate` exits 0
- [ ] Loops have Goto→Label wiring (manual check)
- [ ] Required properties set (manual check)
- [ ] Port numbers correct for multi-output nodes

## Related Skills

- `creating-flow` — generate a flow
- `running-flow` — execute after validation
- `searching-packages` — find correct node types / packages
