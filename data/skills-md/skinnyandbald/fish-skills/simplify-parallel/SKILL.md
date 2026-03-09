---
name: simplify-parallel
description: "Run code simplification across entire codebase using parallel agents with automatic segmentation and coordination"
---

# Parallel Codebase Simplification

Execute code simplification across a large codebase by automatically segmenting it into logical chunks and processing them concurrently with proper dependency ordering.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/simplify-parallel` | Analyze and simplify entire codebase |
| `/simplify-parallel --dry-run` | Analyze only, show plan without executing |
| `/simplify-parallel --focus=lib` | Limit to specific area |
| `/simplify-parallel --segments=4` | Set max parallel agents |

## Usage

```
/simplify-parallel [options]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` | false | Analyze only, don't modify files |
| `--focus=AREA` | all | Limit to area: `api`, `lib`, `components`, `hooks`, `pages` |
| `--segments=N` | 3 | Maximum parallel agents |
| `--max-files=N` | 20 | Max files per segment |
| `--verbose` | false | Show detailed progress |

---

## CRITICAL: What NOT to Change

> **This section is the #1 priority.** Violations here negate the value of simplification.
> Workers MUST read this section before making any changes.

### Never Remove Comments

Workers must **NEVER** remove any of the following:

| DO NOT REMOVE | Example |
|---------------|---------|
| **Section separators** | `// ===== Types =====`, `// ===== Helpers =====`, `// ===== Component =====` |
| **JSDoc/TSDoc docstrings** | `/** Computes the current project step... */` |
| **File header comments** | Block comments at top of files explaining purpose |
| **"Why" comments** | `// Only truly block when mutation is actively in flight` |
| **Business logic comments** | `// While any query is loading, trust the server-provided step` |
| **Error handling rationale** | `// Check if error is retryable based on status code` |
| **TODO/FIXME/NOTE comments** | These track technical debt |
| **Biome ignore directives** | `// biome-ignore lint/style/useNamingConvention: reason` |
| **Re-export annotations** | `// Re-export types for convenience`, `// Production hooks use tRPC` |
| **Phase/section markers** | `// Phase 14.16`, `// Step 1: Fetch and validate` |

### Never Remove These Code Patterns

| DO NOT REMOVE | Reason |
|---------------|--------|
| **Explicit intent patterns** | `if (x) { return x; } return undefined;` shows intent vs implicit `return x;` |
| **Named intermediate variables** | `const isMutationPending = mutation.isPending` is clearer than inlining |
| **Error handling structure** | Don't collapse try/catch blocks that handle different error types |
| **Manual test output** | `console.log` in `*.integration.ts` or `manual.*.ts` files is intentional |

### The Rule

**If removing a comment or simplification changes the clarity of _intent_, don't do it.**

Simplification means removing _unnecessary complexity_, not removing _documentation_.

---

## How It Works

### Phase 1: Codebase Analysis

The orchestrator analyzes the codebase structure:

```
1. Directory Tree Scan     -> Identify top-level modules
2. File Metrics Collection -> Count files, LOC, complexity per directory
3. Dependency Graph        -> Parse imports to build file->file dependency map
4. Cluster Formation       -> Group tightly-coupled files into processing units
```

### Phase 2: Segment Formation

Files are grouped into segments based on:
- **Natural boundaries**: `src/app/api/`, `src/lib/`, `src/components/`
- **Dependency coupling**: Files that import each other stay together
- **Size limits**: Target 10-25 files per segment

### Phase 3: Parallel Execution

```
Orchestrator (Main Agent)
  |-- Worker Agent (Segment A)
  |-- Worker Agent (Segment B)
  |-- Worker Agent (Segment C)
```

### Phase 4: Verification & Consolidation

After all segments complete:
1. Run type-check (`npm run typecheck`)
2. Run linting (`npm run lint`)
3. Run unit tests (`npm run test:run`)
4. **Verify no comments were removed** (MANDATORY)
5. Create consolidated commit

## Workflow Steps

### Step 1: Run Analysis

```bash
npx tsx scripts/analyze-codebase.ts --verbose
```

**Note:** The analysis script automatically excludes `.github/worktrees/` directories.

### Step 2: Review Parallel Groups

The analysis output shows which segments can run concurrently.

**Key principle**: Groups are processed sequentially, but segments within a group run in parallel.

### Step 3: Execute Simplification

For each parallel group:

1. **Launch worker agents** using the Task tool
2. **Each worker receives** an exclusive list of files to modify
3. **Workers run simultaneously** with no overlap
4. **Wait for all workers** before proceeding to next group

### Step 4: Verify & Commit

After all groups complete, run full verification suite:

```bash
npm run typecheck
npm run lint
npx vitest run --exclude='.github/worktrees/**'
npm run build
```

### Step 5: Comment Preservation Check (MANDATORY)

Before committing, verify that comments were NOT removed:

```bash
# Check diff for removed comments
git diff HEAD -- '*.ts' '*.tsx' | grep -E '^\-\s*//' | grep -v '^\-\s*//\s*$'
```

If any helpful comments were removed, **restore them before committing**.

**Manual verification checklist:**
- [ ] Section separators (`// ===...`) still present in modified files
- [ ] JSDoc/TSDoc blocks above functions are preserved
- [ ] Inline "why" comments are preserved
- [ ] Biome ignore directives are preserved

## Simplification Patterns Applied

Workers apply these transformations:

| Pattern | Before | After |
|---------|--------|-------|
| Nested ternaries | `a ? b ? c : d : e` | Helper function |
| Debug logs | `console.log('debug')` | Removed (production code only) |
| Repeated patterns | Same code 3+ times | Extracted function |
| Complex conditions | `if (a && b \|\| c && d)` | Named boolean |
| Long functions | 100+ lines | Split into smaller functions |

## Conflict Prevention

| Strategy | Implementation |
|----------|---------------|
| **File Ownership** | Each segment has exclusive file list - no overlaps |
| **Dependency Order** | Foundation modules processed before dependents |
| **Sequential Groups** | Groups run one at a time, segments within parallel |
| **Verification Gates** | Type-check between groups catches issues early |

## Failure Handling

- Failed segments are retried up to 3 times with smaller batches
- Other segments continue processing
- Final report shows partial completion if needed
