---
name: explore
description: "Explore how code works using GitNexus CLI (gitnexus). CLI ONLY - NO MCP server exists, never use readMcpResource with gitnexus:// URIs. TRIGGERS - how does X work, explore symbol, understand function, trace execution, code walkthrough."
allowed-tools: Bash, Read, Grep, Glob
model: haiku
---

# GitNexus Explore

> **CLI ONLY — no MCP server exists. Never use `readMcpResource` with `gitnexus://` URIs.**

Trace execution flows and understand how code works using the GitNexus knowledge graph.

## When to Use

- "How does X work?"
- "What's the execution flow for Y?"
- "Walk me through the Z subsystem"
- Exploring unfamiliar code areas before making changes

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

### Step 2: Find Execution Flows

```bash
$GN query "<concept>" --limit 5 --repo "$REPO_NAME"
```

This returns ranked execution flows (process chains) related to the concept.

### Step 3: Get 360° Symbol View

For each relevant symbol found:

```bash
$GN context "<symbol>" --content --repo "$REPO_NAME"
```

This shows:

- **Callers** — who calls this symbol
- **Callees** — what this symbol calls
- **Processes** — execution flows this symbol participates in
- **Source** — the actual code (with `--content`)

If multiple candidates are returned, disambiguate with:

```bash
$GN context "<symbol>" --uid "<full-uid>" --content --repo "$REPO_NAME"
# or
$GN context "<symbol>" --file "<file-path>" --content --repo "$REPO_NAME"
```

### Step 4: Read Source Files

Use the Read tool to examine source files at the line numbers identified by GitNexus.

### Step 5: Synthesize

Present a clear explanation covering:

- **What it is** — purpose and responsibility
- **Execution flows** — how data moves through the system
- **Dependencies** — what it depends on, what depends on it
- **Key files** — the most important files to understand

## Example

User: "How does the kintsugi gap repair work?"

```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
$GN query "kintsugi gap repair" --limit 5 --repo "$REPO_NAME"
$GN context "KintsugiReconciler" --content --repo "$REPO_NAME"
$GN context "discover_shards" --content --repo "$REPO_NAME"
```

Then read the relevant source files and synthesize the explanation.
