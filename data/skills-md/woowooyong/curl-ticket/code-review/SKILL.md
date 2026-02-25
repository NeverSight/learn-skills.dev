---
name: code-review
description: Review code changes for correctness, security, and adherence to project conventions. Use when asked to "review code", "review PR", "review my changes", "check this code", or when reviewing diffs, new features, bug fixes, or refactors in this Nuxt 4 / Vue 3 / Drizzle ORM / Supabase project.
---

# Code Review

Perform thorough code reviews for the Curl Ticket project (Nuxt 4 + Vue 3 + Drizzle ORM + Supabase Auth + Zod).

## Review Process

1. **Identify scope** — determine which files changed and their categories (API route, component, schema, shared code)
2. **Read changed files** — read each file fully before reviewing
3. **Apply category checklist** — use the relevant sections from [references/checklist.md](references/checklist.md)
4. **Report findings** — output structured review with severity levels

## Review Categories

Based on the changed files, apply the matching checks:

| File path pattern | Checklist sections to apply |
|---|---|
| `server/api/**` | API Route, Security, Error Handling |
| `app/components/**`, `app/pages/**` | Vue Component, Security (XSS) |
| `server/database/schema/**` | Database & Schema |
| `shared/schemas/**`, `shared/constants.ts` | Validation & Types |
| `app/composables/**` | Vue Component (data fetching), Performance |
| `server/utils/**`, `server/middleware/**` | API Route (auth), Security, Error Handling |

Always apply **Security Review** regardless of file type.

For the full checklist, read [references/checklist.md](references/checklist.md).

## Critical Project Rules

These are the most common mistakes — flag immediately:

- **Missing project access check**: Any `server/api/projects/[projectId]/**` route MUST call `getAccessibleProject()` or `buildProjectAccessCondition()`
- **Raw string enums**: Use `IssueStatus.Open`, `HttpMethod.GET`, etc. from `shared/constants.ts` — never raw strings
- **Raw fetch in components**: Must use `useFetch` or project composables for SSR compatibility
- **Options API usage**: All components must use `<script setup lang="ts">`
- **Missing Zod validation**: All API request bodies must be validated with shared Zod schemas
- **Error helpers**: Use `notFound()`, `forbidden()`, `badRequest()`, `unauthorized()` from `server/utils/errors.ts`
- **v-html with user input**: Flag as high-severity security issue

## Output Format

Structure review output as:

```
## Code Review: [brief description]

### Summary
[1-2 sentence overview of changes and overall assessment]

### Findings

#### 🔴 Critical
- **[file:line]**: [description and fix]

#### 🟡 Suggestions
- **[file:line]**: [description and suggestion]

#### 🟢 Good Patterns
- [note positive patterns worth highlighting]

### Verdict
[APPROVE / REQUEST_CHANGES / COMMENT — with brief rationale]
```

Omit empty severity sections. If no issues found, state the code looks good with brief justification.
