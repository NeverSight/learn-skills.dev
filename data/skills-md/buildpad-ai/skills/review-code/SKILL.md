---
name: review-code
description: Perform a comprehensive code review checking for quality, security, performance, accessibility, and DaaS/Buildpad compliance. Generates actionable feedback with severity levels. Use when the user says review-code, review this, check code quality, or wants a PR review.
argument-hint: "[file path or feature name to review]"
---

# Review Code

Perform multi-dimensional code review for DaaS platform applications.

> **Delegate for isolated review.** For a thorough pass that doesn't bloat the main conversation, hand the change to the `code-reviewer` subagent (and `security-auditor` for auth, CORS, access-rule (RLS on a Supabase project) and secret concerns) — see `subagent-delegation`. Treat findings as advisory and verify fixes on the main thread.

## Review Dimensions

### 1. Correctness & Logic

- Does it do what it's supposed to?
- Edge cases handled?
- Error states covered?
- TypeScript types correct and strict?

### 2. Security

- [ ] No secrets in code (check `.env.local` usage); on an Engine project any service-role key reference is a finding, because an Engine project has none
- [ ] Auth checks on all API routes
- [ ] Input validation with Zod on all POST/PATCH handlers
- [ ] No direct Supabase calls from client (must use proxy routes); on an Engine project any Supabase client call other than sign-in (password sign-in, session refresh, reading the signed-in user, sign-out) is a finding, because it has no server there
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] CSRF protection on mutations

### 3. DaaS & Buildpad Compliance

- [ ] **Buildpad-First Rule**: No raw Mantine form/input components when Buildpad provides them
- [ ] **Proxy Pattern**: All API calls go through `/api/*` routes, never direct to DaaS backend (the Engine_URL on an Engine project)
- [ ] **Auth Proxy**: Login/logout via `/api/auth/*`, never direct `supabase.auth.*` (on an Engine project the routes use the Supabase client for sign-in only)
- [ ] **Backend-First**: Business logic uses DaaS extensions/workflows, not Next.js API routes (on an Engine project: stored hooks, cron jobs and custom services in the Engine's runtime, and its workflows)
- [ ] Components imported from `@/components/ui/` or `@/lib/buildpad/`
- [ ] No manually created files in `components/ui/` or `lib/buildpad/` (CLI only)

### 4. Performance

- [ ] No unstable useEffect dependencies (new objects every render)
- [ ] API calls not in render loops
- [ ] Large lists virtualized or paginated
- [ ] Images optimized with next/image
- [ ] Server Components used where possible

### 5. Accessibility

- [ ] Semantic HTML elements
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation works
- [ ] Color contrast sufficient
- [ ] Focus management in modals/dialogs

### 6. Testing

- [ ] Tests exist for the feature
- [ ] Happy path, error cases, and edge cases covered
- [ ] Test file in correct `tests/` subdirectory

## Output Format

For each finding:

```
[SEVERITY] Category — Description
File: path/to/file.ts:L42
Fix: Specific recommendation
```

Severity levels: 🔴 CRITICAL (must fix), 🟡 WARNING (should fix), 🔵 INFO (consider)

## References

- [Playwright testing guide](../create-tests/references/playwright-testing.instructions.md)
