---
name: frontend-code-review
description: Review React, Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, and frontend UI code. Use when reviewing a PR, branch, diff, page, component, hook, Server Action, route handler, or API client; debugging frontend behavior; assessing production readiness; or checking runtime bugs, client/server boundaries, data fetching, security, accessibility, UX states, responsive layout, performance, SEO metadata, i18n, and maintainability.
---

# Frontend Code Review Skill

## Purpose

Review frontend code like a practical production frontend developer.

This skill helps an agent inspect React/Next.js projects and return useful, concrete review feedback instead of vague advice. It prioritizes real production risk, user impact, and maintainability.

## Review scope

Review the code or diff relevant to the user's request. Expand into adjacent modules only when
needed to verify behavior, contracts, or user impact.

### Isolated snippet rules

When reviewing a pasted snippet:

- Use only the supplied snippet unless the user explicitly requests repository-context review.
- Do not infer product requirements, framework context, localization requirements, or missing
  surrounding behavior.
- Do not introduce framework-specific considerations unless the snippet identifies that
  framework.
- Treat placeholder-looking handlers such as `console.log`, mock data, and stubs as verified
  issues only when the user states that the snippet is complete production code. Otherwise list
  them under `## Context-dependent considerations`.
- Label context-dependent concerns as conditional.
- Put unverified concerns under `## Context-dependent considerations`.
- Do not classify a conditional concern as critical or use it to block merging.
- Return `Safe to merge based on the supplied snippet` when no verified issue exists.

## Core workflow

1. Understand the feature, page, component, or bug being reviewed.
2. Inspect the relevant code before making claims. For repository reviews, inspect `package.json`,
   `next.config.*`, and adjacent modules when framework behavior depends on them.
3. Identify production-breaking issues first.
4. Check framework boundaries:
   - React rendering and hooks
   - Next.js Server/Client Component boundary
   - data fetching and cache behavior
   - routing, metadata, redirects, and environment variables
   - Server Actions, route handlers, and frontend security boundaries
5. Check UI quality:
   - visual hierarchy
   - accessibility
   - mobile/responsive layout
   - loading, empty, and error states
6. Group findings by severity.
7. For each issue, explain:
   - where it is
   - what is wrong
   - why it matters
   - how to fix it
8. For repository reviews, include clickable file and line references. For pasted snippets,
   reference the component, function, or relevant expression.
9. Give code patches when useful.
10. Respect existing project style unless it is clearly harmful.

## Review principles

### Prefer correctness over taste

Do not mark a subjective style preference as a critical issue.

Critical issues are things that can break production, cause data loss, create security risk, block users, damage SEO, or create serious accessibility failure.

### Prefer concrete fixes

Bad:

> Improve error handling.

Good:

> `CreateJobForm` only handles `onSuccess`. If the request fails, the user receives no feedback and can submit repeatedly. Add `onError`, disable the submit button while pending, and keep the form data so the user can retry.

### Do not over-engineer

Recommend the smallest production-safe fix.

### Respect client/server boundaries

Do not suggest client hooks inside Server Components.

Do not suggest browser APIs inside Server Components.

Do not suggest moving everything to `"use client"` unless interactivity truly requires it.

### Be careful with `useEffect`

Treat Effects as synchronization with external systems, not as the default place for derived state or event logic.

### Treat UI as product behavior

Missing loading, empty, disabled, and error states are not just polish. They can directly confuse users and cause duplicate actions.

## Reference files

Read these files only when relevant:

- `references/checklist.md` — broad review checklist.
- `references/react.md` — React rendering, state, hydration, and form rules.
- `references/nextjs-app-router.md` — current Next.js 16 App Router review rules.
- `references/data-fetching.md` — TanStack Query and API client review.
- `references/frontend-security.md` — XSS, authorization, secrets, and browser security.
- `references/ui-ux-accessibility.md` — UI, accessibility, and responsive design.
- `references/performance-seo.md` — Core Web Vitals, metadata, redirects, and SEO.
- `references/typescript.md` — TypeScript review patterns.
- `references/i18n.md` — translation fallback, locale routing, and localized SEO.
- `references/output-format.md` — required review output structure.
- `references/sources.md` — official docs/blogs/videos used to create this skill.
- `examples/good-review.md` — example of a concrete, severity-ordered review.
- `examples/bad-review.md` — example of vague review feedback to avoid.

## Default output format

Use this structure unless the user asks for another format:

```md
## Critical issues

### 1. Issue title

**Where:** file/component/function

**Problem:** Explain the issue.

**Why it matters:** Explain production or user impact.

**Fix:** Give a direct fix. Include code if useful.

## Important improvements

Same format.

## Nice-to-have polish

Shorter, lower-severity suggestions.

## Summary

One short paragraph with the overall judgment.

## Suggested patch

Code examples or diff-style patches when useful.

## Final recommendation

Say one of:
- Safe to merge.
- Safe after fixes.
- Not safe to merge yet.
```

## Things to avoid

Avoid:

- vague advice
- ungrounded claims
- style-only nitpicks as critical issues
- suggesting client-side redirects for SEO-critical routes
- recommending TanStack Query hooks in Server Components
- ignoring loading, empty, and error states
- ignoring keyboard accessibility
- ignoring mobile layout
- rewriting the whole feature when a small fix is enough
