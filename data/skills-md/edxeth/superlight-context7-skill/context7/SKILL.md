---
name: context7
description: Fetches up-to-date third-party library documentation via the Context7 v2 REST API. Use when working with external packages and needing current API references, code examples, migration guides, or resolving package errors (stack traces, version mismatches, deprecated methods).
---

# Context7 Documentation Lookup

Retrieves current, version-specific documentation for third-party libraries directly from official sources.

## When to Use

**ALWAYS** invoke before writing code for external libraries when:
- Implementing unfamiliar library APIs
- Debugging errors from external packages (stack traces, "method not found")
- Checking version-specific syntax or breaking changes
- Verifying deprecated/removed APIs
- Encountering unfamiliar `import`/`require` statements

## Protocol

### Step 1: Search for Library ID

```bash
scripts/context7.sh search "<library>" "<intent>"
```

**Example:**
```bash
scripts/context7.sh search "tanstack-query" "optimistic updates"
```

**Output:** Library IDs like `/tanstack/query`, `/vercel/next.js`

**Disambiguation:** If multiple similar results appear, ask user which library they meant.

### Step 2: Fetch Documentation

```bash
scripts/context7.sh docs "<library-id>" "<specific-question>"
```

**Examples:**
```bash
scripts/context7.sh docs "/vercel/next.js" "middleware redirect authentication"
scripts/context7.sh docs "/tanstack/query" "useMutation optimistic update pattern v5"
```

### Step 3: Apply Context

Uses returned documentation to generate accurate, version-correct code.

## Critical Rules

1. **Specific queries win** - "useState hook array destructuring" beats "react hooks"
2. **Include version** - Append version to query if user mentions one
3. **No guessing** - If search returns nothing, ask user before proceeding
4. **Only run context7.sh** - Do not run other bash commands with this skill

## Resources

See `reference/troubleshooting.md` for error handling, configuration, and common issues.
