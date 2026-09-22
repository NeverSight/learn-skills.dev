---
name: w-ui
description: Build or reshape UI with purpose, existing tokens, accessible interactions, and bounded rendered verification.
disable-model-invocation: true
---

Build or reshape a user-facing surface. Planning a feature without UI work stays on `/w-plan`. Installing a primitive stays on `/w-shadcn`. Do not invent `PRODUCT.md` or `DESIGN.md`. Follow existing tokens and root `DESIGN.md` when present. Do not install animation libraries or design-detector hooks.

Load `frontend-design` for visual direction, `composition-patterns` for reusable APIs, and `web-design-guidelines` for the UI code checklist. Durable jobs live in matching MDX/README/`DESIGN.md`.

1. Name the job, the person, and the surface mode: Operate (app/task), Persuade (marketing), or Read (docs).
2. Use the brief, existing screens, or a stated aesthetic. If the repo has tokens and shared components, inspect those first.
3. Prefer shared primitives. Compose at the second call site. Do not extract a compound API for a one-off route. Do not lift server data into a client provider.
4. Mobile-first layout, visible focus, keyboard path, `prefers-reduced-motion`. Do not add a new motion library.
5. Cover loading, empty, error, success, and overflow as applicable.
6. Implement the smallest slice that completes the job.
7. Inspect desktop and mobile together. Exercise primary interactions and keyboard navigation. Critique screenshots. Fix evidenced issues in one batch. Confirm with at most one more pass, then stop. If browser tools are missing, say so. A type check is not visual QA.
8. Optional: `/w-a11y` against existing a11y docs and tests (do not invent a WCAG level). Playwright E2E only when an existing spec covers the path.
9. Docs: `/w-docs` if behavior or commands changed.
