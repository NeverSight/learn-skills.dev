---
name: engineer-review
description: Comprehensive multi-agent code review with parallel specialist reviewers. Use when the user says "review this", "code review", "review my PR", provides a PR number or branch, or after completing a /engineer-work cycle.
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Task", "Write"]
argument-hint: "[pr-number or files]"
---

# /engineer-review — Multi-Agent Code Review

Launch parallel specialist reviewer agents to comprehensively review code changes. Each reviewer focuses on one domain and reports findings independently.

## When to Use

- User says "review this", "code review", "review my PR"
- After completing `/engineer-work`
- Before merging a feature branch

## Process

### Step 1: Scope the Review

Determine what to review:
- If a PR number is provided: `gh pr diff [number]`
- If on a feature branch: `git diff main...HEAD`
- If `$ARGUMENTS` specifies files: review those files

Get the diff and list of changed files.

### Step 2: Detect Tech Stack

Read project config files to determine which conditional reviewers to launch:
- `tsconfig.json` → TypeScript reviewer
- `next.config.*` → Next.js reviewer
- `app.json` or `expo` in package.json → Expo/RN reviewer
- `supabase/` directory → Supabase reviewer
- `docs/prds/` or `docs/tech-specs/` → Spec compliance reviewer

### Step 3: Launch Parallel Reviewers

Spawn ALL selected reviewers IN PARALLEL using the Task tool. Send all Task calls in a single message.

**Always launch these 4 core reviewers:**

#### Security Reviewer
```
prompt: Review these code changes for security vulnerabilities.
  Focus on: auth bypass, injection (SQL/XSS/command), data exposure,
  hardcoded secrets, insecure defaults, missing input validation.
  Return: file, line, severity (P1-P4), description, fix suggestion.
```

#### Performance Reviewer
```
prompt: Review these code changes for performance issues.
  Focus on: N+1 queries, missing indexes, unnecessary re-renders,
  bundle size impact, request waterfalls, missing caching, large payloads.
  Return: file, line, severity (P1-P4), description, fix suggestion.
```

#### Architecture Reviewer
```
prompt: Review these code changes for architectural issues.
  Focus on: component boundaries, module dependencies, state management
  choices, data flow patterns, separation of concerns, SOLID principles.
  Return: file, line, severity (P1-P4), description, fix suggestion.
```

#### Patterns Reviewer
```
prompt: Review these code changes for consistency with codebase patterns.
  First read existing files to understand conventions, then check:
  naming conventions, import patterns, error handling patterns,
  duplication, anti-patterns, TypeScript usage.
  Return: file, line, severity (P1-P4), description, fix suggestion.
```

**Conditionally launch based on Step 2 detection:**

#### TypeScript Reviewer (if tsconfig.json)
```
prompt: Review for TypeScript quality. Focus on: type safety, proper generics,
  Zod schema integration, avoiding any/as assertions, discriminated unions.
```

#### Next.js Reviewer (if next.config.*)
```
prompt: Review for Next.js App Router best practices. Focus on: server/client
  component boundaries, data fetching patterns, caching, middleware, server actions.
```

#### Expo/RN Reviewer (if app.json/expo)
```
prompt: Review for Expo/React Native patterns. Focus on: Expo Router conventions,
  NativeWind styling, platform handling, native module usage, mobile performance.
```

#### Supabase Reviewer (if supabase/ directory)
```
prompt: Review Supabase usage. Focus on: RLS policy completeness, auth patterns,
  client selection (browser vs server), storage policies, realtime security.
```

#### Spec Compliance Reviewer (if docs/prds/ or docs/tech-specs/)
```
prompt: Compare implementation against the spec. Read the latest PRD/tech-spec
  in docs/. Check: requirements met, deviations justified, nothing over-built.
```

See [references/reviewer-catalog.md](references/reviewer-catalog.md) for full reviewer focus areas.

### Step 4: Synthesize Results

Collect all reviewer findings and produce a unified summary:

```markdown
## Code Review Summary

### P1 — Critical (must fix before merge)
| # | File | Line | Issue | Reviewer |
|---|------|------|-------|----------|

### P2 — Important (should fix)
| # | File | Line | Issue | Reviewer |

### P3 — Suggestion (consider fixing)
| # | File | Line | Issue | Reviewer |

### P4 — Nitpick (optional)
| # | File | Line | Issue | Reviewer |

### Positive Patterns
[Good patterns worth noting]

### Reviewers Run
[List which reviewers were launched and why]
```

Deduplicate findings across reviewers. If two reviewers flag the same issue, keep the more specific one.

## Output

Review summary presented inline. Optionally save to `docs/reviews/` if requested.

## Next Steps

- Issues found? Fix them and re-run `/engineer-review`
- All clear? Merge the PR
- Want to capture learnings? → `/knowledge-compound`
