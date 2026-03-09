---
name: gather-plan-apply
description: "MANDATORY before starting any task. Enforces the GPA execution loop that prevents tool call sprawl. G: GATHER phase combines discover queries + memory reads + file reads into one phase. P: Plan in text with zero tool calls. A: APPLY all writes/edits/verification in one phase. One call per tool type per phase — batch all same-type operations together. Covers dependency analysis, batch opportunities, scope estimation, and loop-back triggers."
metadata:
  version: 2.0.0
  category: protocol
  tags: [gpa, gather, plan, apply, workflow, token-efficiency, strict-workflow]
---

## Resources
```
scripts/
  validate-gpa-compliance.sh
references/
  examples-and-checklists.md
```

# Gather-Plan-Apply Protocol (GPA Workflow)

The GPA loop enforces a **one-call-per-tool-type-per-phase** workflow that eliminates token waste from excessive tool calls. This is NOT a suggestion — it is a MANDATORY execution pattern for all GoodVibes agents.

## THE EXACT WORKFLOW

```
0. LOAD SKILLS (once, before any GPA cycle)
   - Call get_skill_content for role-relevant skills
   - This is NOT part of the GPA cycle itself

1. G — GATHER (1-2 tool calls)
   - Check .goodvibes/memory/ files FIRST (failures, patterns, decisions)
   - Single `discover` call with ALL queries batched inside
   - Multiple query types (glob, grep, symbols, structural) in one call
   - Can search file content via grep/symbols queries
   - Batch any file reads that need full content alongside discover
   - Output: files_only or locations (minimal verbosity)

2. P — PLAN (0 tool calls, cognitive only)
   - Agent thinks about what it learned from GATHER
   - Plans which files to create/write/edit
   - Plans which commands to run for validation
   - Identifies ALL batch opportunities — same-type ops go in one call
   - Plans the EXACT apply call structure

3. A — APPLY (1-2 tool calls)
   - Writes and edits batched into one precision_write or precision_edit call
   - Validation commands batched into one precision_exec call
   - Key: one call per tool type, everything batched inside it

4. LOOP — Back to G if:
   - Results didn't match expectations
   - Scope changed
   - Validation failed
```

## CALL BUDGET PER CYCLE

| Phase | Tool Calls | Type | Purpose |
|-------|-----------|------|----------|
| **G** (Gather) | 1-2 | `discover` + optional `precision_read` | All discovery + memory reads |
| **P** (Plan) | 0 | Cognitive | Plan apply operations |
| **A** (Apply) | 1-2 | `precision_write`/`precision_edit` + `precision_exec` | All writes/edits + validation |
| **TOTAL** | **2-4** | | |

**Core rule**: One call per tool type per phase. Never make two `precision_read` calls in the same phase — batch both files into the one call.

**Note on sequential calls:** Sequential calls are acceptable when operations depend on each other (e.g., write then verify). Always prefer true batching via internal precision tool arrays (files array, edits array, commands array).

## KEY RULES (NON-NEGOTIABLE)

1. **`discover` batches ALL discovery queries into 1 call** — NEVER use separate `precision_glob`, `precision_grep` for discovery
2. **Plan steps produce ZERO tool calls** — they are cognitive (agent thinks in text)
3. **One call per tool type per phase** — if you need 3 files read, batch them in 1 `precision_read` call
4. **APPLY output = 1-2 calls** — precision_write/edit for files, precision_exec for commands
5. **ToolSearch is NOT part of GPA** — load tools once at start, don't search mid-cycle
6. **Check memory FIRST** — always read .goodvibes/memory/ before implementing

## Phase 1: GATHER (1-2 calls)

### Initial Setup: Check Memory

Before discovering files, check what's already known. Batch memory reads with your discover call or as a separate read:

```yaml
# GOOD: Memory reads batched with file content reads
precision_read:
  files:
    - path: ".goodvibes/memory/failures.json"
    - path: ".goodvibes/memory/patterns.json"
    - path: ".goodvibes/memory/decisions.json"
  verbosity: minimal
```

### The `discover` Tool

The `discover` tool runs multiple grep/glob/symbols/structural queries **in parallel**, returning results keyed by query ID. This is your primary discovery mechanism.

**Pattern: Batch ALL discovery queries**

```yaml
# GOOD: 1 discover call with everything
discover:
  queries:
    - id: existing_files
      type: glob
      patterns: ["src/features/auth/**/*.ts"]
    - id: existing_patterns
      type: grep
      pattern: "export (function|const|class)"
      glob: "src/features/**/*.ts"
    - id: exported_hooks
      type: symbols
      query: "use"
      kinds: ["function"]
    - id: console_logs
      type: structural
      structural_pattern: "console.log($$$ARGS)"
  verbosity: files_only
```

**Query types:**
- **glob** - Find files by path patterns
- **grep** - Find files containing patterns
- **symbols** - Find exported functions/types/classes
- **structural** - Find AST patterns (e.g., function calls)

**Output modes:**
- `count_only` - Just counts (scope estimation)
- `files_only` - File paths only (building target lists) ← **USE THIS**
- `locations` - File paths + line numbers (when you need exact locations)

### Reading Full File Contents

For reading full file contents, use `precision_read` in the GATHER phase, batched with memory reads or as a second call if discover results are needed first.

### [BAD] vs [GOOD] Gather Patterns

**[BAD] — Sequential discovery queries (multiple tool calls)**

```yaml
# BAD: 4 separate tool calls for discovery
precision_glob:
  patterns: ["src/**/*.ts"]

precision_grep:
  queries:
    - id: exports
      pattern: "export function"

precision_read:
  files:
    - path: ".goodvibes/memory/failures.json"

precision_grep:
  queries:
    - id: imports
      pattern: "import.*from"
```

**[GOOD] — Single discover call + batched memory reads (2 tool calls)**

```yaml
# GOOD: 1 discover call with all queries
discover:
  queries:
    - id: files
      type: glob
      patterns: ["src/**/*.ts"]
    - id: exports
      type: grep
      pattern: "export function"
      glob: "src/**/*.ts"
    - id: imports
      type: grep
      pattern: "import.*from"
      glob: "src/**/*.ts"
  verbosity: files_only

# GOOD: Memory reads in one batched call
precision_read:
  files:
    - path: ".goodvibes/memory/failures.json"
    - path: ".goodvibes/memory/patterns.json"
    - path: ".goodvibes/memory/decisions.json"
  verbosity: minimal
```

## Phase 2: PLAN (0 calls, cognitive only)

### Purpose

Planning is **cognitive work**, not tool calls. You think in text about:

- Which files to create/write
- Which files to edit (with exact find/replace)
- Which commands to run for validation
- ALL batch opportunities — same-type ops must be batched

**Output: A written plan with NO tool calls**

### Plan Structure

```
Plan:
1. Create the following files:
   - src/features/auth/types.ts — User interface
   - src/features/auth/hooks.ts — useAuth hook
   - src/features/auth/index.ts — barrel export

2. Edit the following files:
   - src/app/layout.tsx — wrap App with AuthProvider

3. Validate:
   - npm run typecheck (expect exit 0)
   - npm run lint (expect exit 0)

4. Batch plan:
   - Call 1 (Apply): precision_write with 3 files + precision_edit with 1 edit
   - Call 2 (Apply): precision_exec with 2 commands
```

### [BAD] vs [GOOD] Planning

**[BAD] — Vague plan that leads to sequential calls**

```
Plan:
- Create some files
- Maybe edit layout
- Run typecheck
```

This leads to:
```yaml
precision_write: ...   # 1st call
precision_write: ...   # 2nd call! (should be batched)
precision_edit: ...    # 3rd call! (could combine with above pattern)
```

**[GOOD] — Specific plan with exact batch structure**

```
Plan:
1. Write 3 files in 1 precision_write call:
   - src/features/auth/types.ts (symbols)
   - src/features/auth/hooks.ts (content)
   - src/features/auth/index.ts (content)

2. Edit 1 file in 1 precision_edit call:
   - src/app/layout.tsx — wrap with AuthProvider

3. Validate in 1 precision_exec call:
   - npm run typecheck
   - npm run lint
```

## Phase 3: APPLY (1-2 calls)

### Pattern: Batch All Writes/Edits

**Single precision_write with multiple files:**

```yaml
precision_write:
  files:
    - path: "src/features/auth/types.ts"
      content: |
        export interface User {
          id: string;
          email: string;
        }
    - path: "src/features/auth/hooks.ts"
      content: |
        import type { User } from './types';
        export function useAuth(): User | null { /*...*/ }
    - path: "src/features/auth/index.ts"
      content: |
        export * from './types';
        export * from './hooks';
  verbosity: count_only
```

**OR single precision_edit with multiple edits:**

```yaml
precision_edit:
  edits:
    - path: "src/app/layout.tsx"
      find: "<App />"
      replace: "<AuthProvider><App /></AuthProvider>"
    - path: "src/middleware.ts"
      find: "export const config = {}"
      replace: "export const config = { matcher: ['/dashboard/:path*'] }"
    - path: "src/lib/api.ts"
      find: "headers: {}"
      replace: "headers: { Authorization: `Bearer ${token}` }"
  verbosity: minimal
```

**Validation via precision_exec (second Apply call):**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
    - cmd: "npm run lint"
      expect:
        exit_code: 0
  verbosity: minimal
```

### [BAD] vs [GOOD] Apply Batching

**[BAD] — 3 separate precision_write calls**

```yaml
precision_write:
  files:
    - path: "file1.ts"
      content: "..."

precision_write:  # Second call!
  files:
    - path: "file2.ts"
      content: "..."

precision_write:  # Third call!
  files:
    - path: "file3.ts"
      content: "..."
```

**[GOOD] — 1 precision_write call with 3 files**

```yaml
precision_write:
  files:
    - path: "file1.ts"
      content: "..."
    - path: "file2.ts"
      content: "..."
    - path: "file3.ts"
      content: "..."
  verbosity: count_only
```

## Phase 4: LOOP (When to Return to Gather)

### Loop Triggers

1. **Results don't match expectations** — Typecheck fails, tests fail, unexpected behavior
2. **Scope changed** — Discovery revealed different situation than expected
3. **New information** — Task requirements clarified during execution

### Loop Pattern

```yaml
# Initial GPA cycle
discover: ...          # Gather call 1
precision_read: ...    # Gather call 2 (memory + key files)
precision_write: ...   # Apply call 1
precision_exec: ...    # Apply call 2 — FAILS typecheck

# LOOP: Start new GPA cycle with refined discovery
discover:              # Gather call 1 (new cycle)
  queries:
    - id: find_missing_import
      type: grep
      pattern: "export.*User"
      glob: "src/**/*.ts"
  verbosity: locations  # Need exact location

precision_edit: ...    # Apply call 1 (new cycle) - fix the issue
precision_exec: ...    # Apply call 2 (new cycle) - re-validate
```

## Complete Example: Implementing Auth Feature

### Cycle 1: Initial Implementation

**Step 1 — GATHER (2 calls)**

```yaml
# Call 1: Check memory
precision_read:
  files:
    - path: ".goodvibes/memory/failures.json"
    - path: ".goodvibes/memory/decisions.json"
  verbosity: minimal

# Call 2: Discover landscape
discover:
  queries:
    - id: existing_auth
      type: glob
      patterns: ["src/features/auth/**/*.ts", "src/**/auth*.ts"]
    - id: auth_patterns
      type: grep
      pattern: "(useAuth|getSession|AuthProvider)"
      glob: "src/**/*.{ts,tsx}"
    - id: user_types
      type: symbols
      query: "User"
      kinds: ["interface", "type"]
  verbosity: files_only
```

**Step 2 — PLAN (0 calls, cognitive)**

```
Gather results:
- No memory failures for auth
- No existing auth files
- No auth patterns in use
- User type exists in src/types/user.ts

Plan:
Apply Call 1 (precision_write): Create 3 auth files
Apply Call 2 (precision_exec): typecheck + lint
```

**Step 3 — APPLY (2 calls)**

```yaml
# Call 1: Create files
precision_write:
  files:
    - path: "src/features/auth/provider.tsx"
      content: |
        import { ClerkProvider } from '@clerk/nextjs';
        export function AuthProvider({ children }: { children: React.ReactNode }) {
          return <ClerkProvider>{children}</ClerkProvider>;
        }
    - path: "src/features/auth/hooks.ts"
      content: |
        import { useUser } from '@clerk/nextjs';
        import type { User } from '@/types/user';
        export function useAuth(): User | null {
          const { user } = useUser();
          if (!user) return null;
          return { id: user.id, email: user.emailAddresses[0].emailAddress, name: user.fullName };
        }
    - path: "src/features/auth/index.ts"
      content: |
        export { AuthProvider } from './provider';
        export { useAuth } from './hooks';
  verbosity: count_only

# Call 2: Validate
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
    - cmd: "npm run lint"
      expect:
        exit_code: 0
  verbosity: minimal

# Result: typecheck FAILS — missing @clerk/nextjs
```

**Total calls in Cycle 1: 4** (precision_read + discover + precision_write + precision_exec)

### Cycle 2: Fix Missing Dependency

**Step 1 — GATHER (1 call)**

```yaml
discover:
  queries:
    - id: package_json
      type: glob
      patterns: ["package.json"]
    - id: clerk_usage
      type: grep
      pattern: "@clerk/nextjs"
      glob: "src/**/*.{ts,tsx}"
  verbosity: files_only
```

**Step 2 — PLAN (0 calls, cognitive)**

```
Discovery: @clerk/nextjs not in package.json
Plan:
Apply Call 1 (precision_exec): npm install @clerk/nextjs, then typecheck
```

**Step 3 — APPLY (1 call)**

```yaml
precision_exec:
  commands:
    - cmd: "npm install @clerk/nextjs"
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
  verbosity: minimal

# Result: PASSES
```

**Total calls in Cycle 2: 2** (discover + precision_exec)

## Common Violations and Fixes

| Violation | Tool Calls | Fix |
|-----------|-----------|-----|
| Sequential precision_read calls | 5+ | Batch all files into 1 precision_read call |
| Sequential precision_write calls | 5+ | Batch all files into 1 precision_write call |
| Using precision_glob + precision_grep separately | 2+ | Use 1 discover call with both query types |
| Reading outline, then content | 2 | Read content once if you'll need it |
| Planning via tool calls | 1+ | Plan in text (cognitive work = 0 calls) |
| Memory reads skipped | - | Always check .goodvibes/memory/ in Gather phase |

## Enforcement

If you find yourself making the same tool type twice in a phase, you are violating the protocol. Stop and restructure:

1. Identify which calls are discovery → batch into 1 `discover` call
2. Identify which calls are memory/file reads → batch into 1 `precision_read` call
3. Identify which calls are writes/edits → batch into same-type calls (writes together, edits together)
4. Ensure planning happens in text, not via tools

Target: **one call per tool type per phase**.

## Summary

- **G** (Gather): check memory + `discover` + optional `precision_read` for key files
- **P** (Plan): 0 calls (cognitive)
- **A** (Apply): `precision_write`/`precision_edit` + `precision_exec` for validation
- **LOOP**: Start new cycle if needed

**Rule: One call per tool type per phase. Maximize batching within each call.**

Make this your default mode of operation.
