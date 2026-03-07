---
name: impact
description: "Blast radius analysis via GitNexus CLI (gitnexus). CLI ONLY - NO MCP server exists, never use readMcpResource with gitnexus:// URIs. TRIGGERS - what breaks if I change, blast radius, impact analysis, safe to modify."
allowed-tools: Bash, Read, Grep, Glob
model: haiku
---

# GitNexus Impact Analysis

> **CLI ONLY — no MCP server exists. Never use `readMcpResource` with `gitnexus://` URIs.**

Analyze the blast radius of changing a symbol — who calls it, what processes it participates in, and what tests cover it.

## When to Use

- Before modifying a function with many callers
- "What breaks if I change X?"
- "Is it safe to modify Y?"
- "What's the blast radius of changing Z?"

## Workflow

### Step 0: Resolve CLI and Repo Name

Resolve the CLI command (bare `gitnexus` may fail if the project's mise node version differs from where it was installed):

```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
GN=$(command -v gitnexus >/dev/null 2>&1 && echo "gitnexus" || echo "npx gitnexus")
```

Use `$GN --repo "$REPO_NAME"` on all commands below.

### Step 1: Auto-Reindex If Stale

```bash
$GN status --repo "$REPO_NAME"
```

If stale (indexed commit ≠ HEAD), **automatically reindex before proceeding** — do not ask the user:

```bash
$GN analyze --repo "$REPO_NAME"
```

Then re-check status to confirm index is current.

### Step 2: Upstream Blast Radius

```bash
$GN impact "<symbol>" --depth 3 --repo "$REPO_NAME"
```

This shows everything that depends on the symbol (callers, transitive callers up to depth 3).

If multiple candidates are returned, disambiguate:

```bash
$GN impact "<symbol>" --uid "<full-uid>" --depth 3 --repo "$REPO_NAME"
# or
$GN impact "<symbol>" --file "<file-path>" --depth 3 --repo "$REPO_NAME"
```

### Step 3: Downstream Dependencies (Optional)

```bash
$GN impact "<symbol>" --direction downstream --depth 3 --repo "$REPO_NAME"
```

Shows what the symbol depends on — useful for understanding if dependencies might change.

### Step 4: Test Coverage

```bash
$GN impact "<symbol>" --include-tests --repo "$REPO_NAME"
```

Shows which test files exercise this symbol.

### Step 5: Risk Assessment

Based on the number of direct dependents:

| Dependents | Risk Level   | Recommendation                                      |
| ---------- | ------------ | --------------------------------------------------- |
| < 5        | **LOW**      | Safe to modify with basic testing                   |
| 5–20       | **MEDIUM**   | Review all callers, run related tests               |
| 20–50      | **HIGH**     | Consider backward-compatible API, extensive testing |
| 50+        | **CRITICAL** | Needs deprecation strategy, phased migration        |

### Step 6: Structured Report

Present:

- **Risk level** with dependent count
- **Top affected processes** — execution flows that include this symbol
- **Direct callers** — functions/methods that call this directly
- **Test coverage** — tests that exercise this symbol (or gaps)
- **Recommendation** — safe to modify, needs tests, needs migration plan

## Example

User: "What breaks if I change RangeBarProcessor?"

```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
$GN impact "RangeBarProcessor" --depth 3 --repo "$REPO_NAME"
$GN impact "RangeBarProcessor" --include-tests --repo "$REPO_NAME"
```

Output: "CRITICAL risk — 73 dependents across 12 processes. 8 test files cover it. Recommend backward-compatible changes only."
