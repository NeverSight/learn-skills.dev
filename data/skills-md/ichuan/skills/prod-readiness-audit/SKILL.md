---
name: prod-readiness-audit
description: >
  Audit and harden a project before production release, then fix issues found where safe.
  Use when users ask whether a project is ready to deploy, request final pre-launch cleanup,
  or ask to handle responsiveness, light/dark themes, SEO, performance, Lighthouse scores,
  security, tests, deployment readiness, or production smoke validation before going live.
---

# Production Readiness Audit

Run a practical production-readiness pass. The goal is not a theoretical checklist; it is to find and fix issues that would block real users, deployment, or safe operation.

## Operating Rules

1. State assumptions and scope before changing code.
2. Prefer evidence from source, tests, builds, browser checks, logs, and docs.
3. Fix concrete issues; do not add speculative features.
4. Keep changes surgical and aligned with the existing stack.
5. If the user asked for implementation, continue through verification instead of stopping at analysis.
6. If a fix requires product judgment or broad redesign, report it as a decision point instead of guessing.

## Audit Plan

### 1. Establish Baseline

Collect:

- Project stack, package manager, test/build commands.
- Existing deployment docs or scripts.
- Main user-facing routes/pages.
- Current git status.
- Available browser/e2e tooling.

Run the cheapest reliable baseline first, usually lint/typecheck/tests/build. If commands are unknown, infer them from project files.

### 2. User-Facing Completeness

Check whether visible features are production coherent:

- No obvious demo-only pages, placeholders, fake data, debug controls, or broken navigation.
- Empty/loading/error states exist where users can hit them.
- Auth/session flows fail clearly.
- Primary workflows are reachable from navigation.
- Docs or README do not promise missing behavior.

Fix small mismatches. For larger missing features, list them separately as launch blockers or non-blocking gaps.

### 3. Responsive Layout

Inspect key pages at desktop and mobile widths. Verify:

- No horizontal overflow.
- Text does not overlap or escape containers.
- Navigation works on mobile.
- Tables, sidebars, dialogs, and forms remain usable.
- Touch targets are reasonable.

Use browser screenshots when available. Fix layout issues with minimal CSS/component changes.

### 4. Light/Dark Theme

If the app supports themes, check both. Verify:

- Text contrast remains readable.
- Borders, backgrounds, cards, inputs, menus, and disabled states are visible.
- Charts, icons, logos, skeletons, spinners, and code blocks do not disappear.
- System theme or persisted theme behavior is not broken.

Do not introduce a theme system if the project does not already have one unless the user requested it.

### 5. SEO And Shareability

For public web apps or marketing/documentation pages, check:

- Page titles and descriptions.
- Canonical URL if relevant.
- Open Graph/Twitter metadata if pages are shared.
- Semantic headings.
- `robots.txt` and sitemap when the app expects indexing.
- Server/client rendering implications for crawlers.

For private dashboards, keep SEO scope narrow: title, no accidental indexing of private content, and useful metadata.

### 6. Performance

Use the project's available tools first, then browser Lighthouse when practical. Check:

- Production build size and warnings.
- Obvious render waterfalls, repeated network calls, or duplicate data fetching.
- Large images/assets and missing compression/cache headers.
- Lazy loading for heavy non-critical UI.
- Lighthouse performance/accessibility/best-practices/SEO where relevant.

Fix high-confidence issues. Do not chase arbitrary perfect scores if the app type makes them unrealistic; explain residual tradeoffs.

### 7. Security

Run a focused security pass:

- Secrets committed or exposed to client bundles.
- Auth and authorization gaps.
- Unsafe redirects, path traversal, injection, XSS, CSRF, CORS mistakes.
- Sensitive values logged or returned to UI/API.
- Dependency audit if the ecosystem supports it.
- Production config: debug flags, permissive hosts, insecure cookies, missing HTTPS assumptions.

Prioritize exploitable issues over style concerns. If a finding is uncertain, validate before changing code.

### 8. Deployment Readiness

Check:

- Required environment variables are documented without exposing values.
- Build artifacts are generated and ignored/committed correctly.
- Start/deploy scripts match docs.
- Health check or smoke check exists.
- Migration/seed steps are explicit if needed.
- Rollback/restart path is known enough for this project.

If deployment docs are missing or stale, update the smallest relevant doc.

### 9. Verification

After fixes, run the strongest feasible verification set:

- Unit/integration/e2e tests relevant to changed areas.
- Typecheck/lint/build.
- Browser checks for key pages and responsive/theme behavior.
- Lighthouse or equivalent when requested and feasible.
- Security/dependency checks where available.
- Production smoke checks if deployment is in scope.

Do not claim production readiness without saying what was actually verified.

## Final Report

Keep the final report concise:

- Changes made.
- Verification commands/results.
- Remaining launch blockers.
- Non-blocking follow-ups.
- Any checks skipped and why.
