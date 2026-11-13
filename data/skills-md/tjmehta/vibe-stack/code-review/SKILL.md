---
name: code-review
description: Review code changes for quality, security, and best practices. Use when reviewing PRs or checking code quality.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Code Review Skill

When reviewing code in this Vibe Stack project, check for:

## Security

- [ ] No secrets or API keys in code (use environment variables)
- [ ] Convex functions use `auth.getUserId(ctx)` before accessing user data
- [ ] User input is validated with Zod schemas
- [ ] No SQL injection in raw queries (use Convex query builders)
- [ ] Stripe webhooks verify signatures

## TypeScript

- [ ] No `any` types without justification
- [ ] Proper null checks for optional values
- [ ] Convex validators match TypeScript types
- [ ] Async functions properly awaited

## React/Next.js

- [ ] "use client" directive only where needed
- [ ] Server components used where possible
- [ ] Loading and error states handled
- [ ] No unnecessary re-renders (check dependency arrays)

## Convex

- [ ] Indexes defined for frequently queried fields
- [ ] Mutations are atomic
- [ ] Queries don't leak data across users
- [ ] Timestamps use ISO format strings

## Styling

- [ ] Tailwind classes use design system colors
- [ ] Responsive breakpoints considered
- [ ] Dark mode support maintained
- [ ] Accessibility attributes present (aria-labels, roles)

## Output Format

Provide feedback as:

1. **Critical Issues** - Security or data integrity problems
2. **Improvements** - Code quality suggestions
3. **Nitpicks** - Minor style or preference items
