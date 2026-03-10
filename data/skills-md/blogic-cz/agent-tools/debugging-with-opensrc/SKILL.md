---
name: debugging-with-opensrc
description: "ALWAYS LOAD THIS SKILL when: something doesn't work as expected, documentation is unclear, need to understand library internals, debugging integration issues, or before making assumptions about how a library works. Contains opensrc repo paths, debugging workflows, and examples for Effect, TanStack, TRPC, Drizzle, Better Auth, OpenCode."
---

# Debugging with OpenSrc

## Overview

**CRITICAL: Never guess how a library works. Always verify by reading the actual source code.**

OpenSrc provides access to the exact version of external libraries installed in this project. Use it BEFORE making assumptions.

## When to Use This Skill

- Something doesn't work as expected
- Documentation is unclear or missing
- Need to understand library internals
- Debugging integration issues
- Before implementing patterns with external libraries
- When error messages are cryptic

## OpenSrc Commands

```bash
# Sync all repos (run after git clone)
bun run opensrc:sync

# Fetch new package
bun run opensrc:use <package>        # npm package
bun run opensrc:use owner/repo       # GitHub repo
```

## Available Repos (opensrc/repos/github.com/)

| Library             | Path                                                | What to look for                   |
| ------------------- | --------------------------------------------------- | ---------------------------------- |
| **Effect**          | `Effect-TS/effect/packages/effect/src/`             | Schema, Effect.gen, Layer, Context |
| **TanStack Router** | `TanStack/router/packages/react-router/src/`        | createFileRoute, loader, useParams |
| **TanStack Query**  | `TanStack/query/packages/react-query/src/`          | useSuspenseQuery, queryOptions     |
| **TanStack Form**   | `TanStack/form/packages/react-form/src/`            | useForm, validation                |
| **TanStack Start**  | `TanStack/router/packages/start/src/`               | SSR, server functions              |
| **TRPC**            | `trpc/trpc/packages/server/src/`                    | procedures, middleware, routers    |
| **Drizzle ORM**     | `drizzle-team/drizzle-orm/drizzle-orm/src/`         | pgTable, relations, queries        |
| **Better Auth**     | `better-auth/better-auth/packages/better-auth/src/` | auth config, plugins, sessions     |
| **OpenCode**        | `sst/opencode/packages/opencode/src/`               | skills, commands, plugins          |
| **Pino**            | `pinojs/pino/lib/`                                  | logger, transports                 |
| **Sentry**          | `getsentry/sentry-javascript/packages/`             | SDK, integrations, tracing         |

## Debugging Workflow

### Step 1: Identify the Problem

```
Error: "X is not a function" or "Cannot read property Y"
→ Find where X/Y is defined in source code
```

### Step 2: Locate Relevant Source

```bash
# Use CK semantic search to find in opensrc
mcp_ck_semantic_search(
  query="useSuspenseQuery implementation",
  path="opensrc/repos/github.com/TanStack/"
)

# Or grep for specific function
mcp_grep(
  pattern="export function useSuspenseQuery",
  path="opensrc/repos/github.com/TanStack/"
)
```

### Step 3: Read the Implementation

```bash
# Read the actual source file
mcp_read(filePath="opensrc/repos/github.com/TanStack/query/packages/react-query/src/useSuspenseQuery.ts")
```

### Step 4: Understand the Expected Behavior

Look for:

- Function signatures and return types
- Default values and optional parameters
- Error handling and edge cases
- Internal state management

## Common Debugging Scenarios

### Scenario: TanStack Form Validation Not Working

```
BAD: Search web for "TanStack Form validation issue"
GOOD:
1. Read opensrc/repos/github.com/TanStack/form/packages/react-form/src/useForm.ts
2. Find validator interface and expected return type
3. Check how Standard Schema integration works
4. Fix based on actual implementation
```

### Scenario: TRPC Procedure Not Receiving Context

```
1. Read opensrc/repos/github.com/trpc/trpc/packages/server/src/core/middleware.ts
2. Understand how context flows through middleware chain
3. Check if .use() returns opts.next() correctly
```

### Scenario: Effect Layer Not Providing Service

```
1. Read opensrc/repos/github.com/Effect-TS/effect/packages/effect/src/Layer.ts
2. Understand Layer.effect vs Layer.succeed
3. Check Context.Tag usage patterns
```

### Scenario: OpenCode Skill Not Loading

```
1. Read opensrc/repos/github.com/sst/opencode/packages/opencode/src/
2. Find skill loading logic
3. Check frontmatter parsing and description matching
4. Run `opencode debug skill` to verify
```

### Scenario: Better Auth Session Not Persisting

```
1. Read opensrc/repos/github.com/better-auth/better-auth/packages/better-auth/src/
2. Find session handling logic
3. Check cookie configuration and storage
```

## Key Principle

**Source code is the truth.**

- Documentation can be outdated
- Stack Overflow answers may not apply to your version
- Blog posts may use different configurations
- Only the source code shows exactly what happens

## Example: Full Debugging Session

```
Problem: useSuspenseQuery returns undefined even though data is in cache

Step 1: Check TanStack Query source
→ Read opensrc/repos/github.com/TanStack/query/packages/react-query/src/useSuspenseQuery.ts

Step 2: Find the issue
→ Discover that useSuspenseQuery requires queryOptions() wrapper, not raw object

Step 3: Verify in project
→ Check how other components use it successfully

Step 4: Fix
→ Change from trpc.x.useQuery() to useSuspenseQuery(trpc.x.queryOptions())
```

## OpenCode Agent Infrastructure

### Testing Skills and CLAUDE.md Changes

After modifying skills or CLAUDE.md, test in a NEW session:

```bash
# Test with specific model (use perl timeout for non-interactive)
perl -e 'alarm 120; exec @ARGV' opencode run -m anthropic/claude-sonnet-4-5 --format json "your test prompt" 2>&1

# Examples:
# Test database skill autoloading
perl -e 'alarm 120; exec @ARGV' opencode run -m anthropic/claude-sonnet-4-5 --format json "potrebujem vytvorit novu tabulku v databaze" 2>&1

# Test auth skill
perl -e 'alarm 120; exec @ARGV' opencode run -m anthropic/claude-sonnet-4-5 --format json "ako pridam protected procedure pre admin" 2>&1
```

### OpenCode Debug Commands

```bash
# List all available skills (verify skill is registered)
opencode debug skill

# Check OpenCode version
opencode --version

# Run with different models
opencode run -m anthropic/claude-sonnet-4-5 "message"
opencode run -m anthropic/claude-opus-4 "message"
```

### Skill File Structure

```
.opencode/skill/<skill-name>/
├── SKILL.md              # Main skill file with frontmatter
└── references/           # Optional additional docs
    ├── examples.md
    └── patterns.md
```

### SKILL.md Frontmatter Format

```yaml
---
name: skill-name
description: "ALWAYS LOAD THIS SKILL when: keyword1, keyword2, keyword3. Contains X, Y, Z."
---
# Skill Title

## Content...
```

**Key insight:** The `description` field determines when the model loads the skill automatically. Use:

- `"ALWAYS LOAD THIS SKILL when: ..."` for critical skills
- `"LOAD THIS SKILL when: ..."` for optional skills
- Include relevant keywords the user might mention

### Testing Skill Autoloading

1. Make changes to skill or CLAUDE.md
2. Run test in NEW session (skills load at session start)
3. Check JSON output for `"tool":"skill"` call
4. Verify skill content was used in response

```bash
# Look for skill loading in output
perl -e 'alarm 120; exec @ARGV' opencode run -m anthropic/claude-sonnet-4-5 --format json "test prompt" 2>&1 | grep -A5 '"tool":"skill"'
```

### OpenCode Source Code Locations

For debugging OpenCode itself:

```
opensrc/repos/github.com/sst/opencode/packages/opencode/src/
├── skill/          # Skill loading and management
├── command/        # Custom commands
├── plugin/         # Plugin system
├── session/        # Session management
└── provider/       # Model providers
```

## Remember

1. **Read source FIRST** - before asking, before web searching
2. **Exact version matters** - opensrc has YOUR installed version
3. **Follow the code path** - trace from entry point to implementation
4. **Check types** - TypeScript types often reveal expected usage
5. **Look at tests** - library tests show correct usage patterns
6. **Test in NEW session** - skills and CLAUDE.md load at session start
