---
name: react-build-lens
description: "Meta skill for React build work when multiple React/framework/data skills or evidence oracles could apply. For Next.js, read the installed bundled docs first for runtime claims, then still select ownership and other lenses that apply. Use to classify diff-scoped findings as PR risk/follow-up/noise and choose the proof oracle. Do not use for obvious single-oracle React tasks, React Native, or Expo."
---

# React Build Lens

Choose the smallest useful React build lens for the current task.

## Rule

Pick the smallest lens set that fits the touched React surface. Do not run every React skill by default. Do not fix all warnings by default.

Framework knowledge comes from the installed framework, not a generic skill. When the installed Next.js package includes `node_modules/next/dist/docs/`, read the relevant guide there first for runtime claims, then choose any additional lens whose smell still applies. Resolve the package from the owning app when working in a monorepo. Use Next DevTools MCP when the repo configures it.

Use this only when more than one React skill or evidence oracle could apply. For obvious single-skill work, use that skill directly. Do not use this for React Native or Expo.

Cold-agent guardrails:

- Name the owner surface before choosing lenses.
- If the owner is a Next.js app, resolve its installed `next` package and read the relevant bundled docs first for runtime claims: `use client`, RSC, routing, data fetching, metadata, rendering. `react-feature-composition` is the ownership lens in any React app, including Next: feature folders, controllers, models, views, services, selectors. Load both when both apply, Next docs first. `next-best-practices` and training knowledge are not the Next runtime owner.
- Before loading a lens, name the touched file or observed smell that makes it relevant.
- If only one lens applies, use that skill directly and stop.
- If no React surface changed, do not use this skill.
- If a selected lens is missing, ask the user before installing it. If install is declined or unavailable, keep working from local files and available oracles, and name the missing lens as a limitation.

Definitions:

- `Owner surface`: the route, package, component, hook, service, or module that owns the behavior being changed.
- `Browser truth`: inspected rendered DOM, CSS, interaction, or runtime behavior.
- `Smell`: a concrete observed problem in the touched code or rendered UI.

## Risk Rubric

- `PR risk`: issue introduced or exposed by this branch that is likely to break shipped behavior, build, types, route/runtime boundaries, data flow, hydration, accessibility, acceptance criteria, or reviewed user-visible UI.
- `Follow-up`: a real issue outside branch scope, pre-existing, cross-cutting, or requiring product/design choice.
- `Noise`: preference, score-only warning, unreproduced issue, unrelated file, or repo-nonstandard advice.

## Framework Check

Before selecting a lens, inspect the owning package.

- If `next/package.json` resolves and its `dist/docs/` directory exists, read the relevant bundled guide and heed the repo's Next-managed `AGENTS.md` block. Next docs own the framework runtime: `use client`, RSC, route files, data fetching, metadata, rendering. Stop there for those claims. Keep going when the smell is feature ownership, file naming, controller/model/view boundaries, or a large UI surface: that is `react-feature-composition`, including in Next apps.
- `next-best-practices` is an optional review checklist, not the normal Next.js setup path or a substitute for version-matched bundled docs. Do not install or load it by default for framework knowledge.
- The former `vercel-labs/next-skills` install route is deprecated. If the user explicitly asks for the optional skill, use the current OpenReview route listed under Related Skills.

## Lens Selector

This is a selector, not a sequence. Pick only lenses with an observed trigger, then stop.

1. `react-feature-composition` (React and Next.js)
   - Use for ownership, file naming, controller/model/view boundaries, effects, selectors, services, and large UI surfaces. This is the ownership lens in Next apps too; Next runtime docs answer a different question.
   - Read `LANGUAGE.md` from that skill when naming ownership is part of the task.

2. `vercel-react-best-practices`
   - Use for observed or plausible React performance/data-flow risk: waterfalls, server/client data boundaries, bundle size, render churn, effect misuse that changes behavior or performance, hydration mismatch, or JavaScript payload.
   - Prefer the specific rule file that matches the smell.

3. `tanstack-start`
   - Use only after repo evidence confirms a TanStack Start codebase.
   - Use when the branch touches SSR, streaming, server functions, API routes, middleware, Start config, route/runtime boundaries, or Start-specific Router/Query integration.
   - Treat it as a TanStack Start framework lens, not as a general TanStack ecosystem trigger. TanStack Router or Query alone is not enough.

4. `vercel-composition-patterns`
   - Use when the problem is reusable component API shape, not feature file ownership: boolean prop proliferation, slotting, compound components, render props, controlled/uncontrolled APIs, context/provider interfaces, or explicit variant components.
   - This is the lens for preventing prop-matrix and caller-ergonomics dead ends. Do not replace it with `react-feature-composition` when consumer API shape is the risk.
   - Do not apply it to every route-local component.

5. `web-design-guidelines`
   - Use when the user asks for UI/design review, or when the branch's main risk is visible layout, interaction, accessibility, visual hierarchy, or copy presentation.
   - Do not use it for routine JSX/CSS touches, headless logic, data plumbing, or invisible refactors.

## Related Skills

If a selected lens is missing, ask the user before installing it. Use the exact command shown only after approval. These commands install optional lenses; they are not the setup path for Next.js framework knowledge, which comes from the owning app's installed docs. If the target install scope is unclear, ask first. If a repo contains multiple skills, keep the `--skill` selector. For project installs, run the command from the target project root. For global installs, add `--global`.

- `next-best-practices` (optional review checklist)
  - Current listing: <https://www.skills.sh/vercel-labs/openreview/next-best-practices>
  - Install only when explicitly requested:
    ```sh
    npx skills add https://github.com/vercel-labs/openreview --skill next-best-practices
    ```
  - Do not use the deprecated source: `npx skills add vercel-labs/next-skills --skill next-best-practices`.

- `react-feature-composition`
  ```sh
  npx skills@latest add callumflack/skills --skill react-feature-composition
  ```
- `vercel-react-best-practices`
  ```sh
  npx skills@latest add vercel-labs/agent-skills --skill vercel-react-best-practices
  ```
- `tanstack-start`
  ```sh
  npx skills@latest add tanstack-skills/tanstack-skills --skill tanstack-start
  ```
- `vercel-composition-patterns`
  ```sh
  npx skills@latest add vercel-labs/agent-skills --skill vercel-composition-patterns
  ```
- `web-design-guidelines`
  ```sh
  npx skills@latest add vercel-labs/agent-skills --skill web-design-guidelines
  ```

## Evidence Oracles

Use the narrowest real oracle that matches the touched surface:

- typecheck for types and build-time contracts;
- lint for repo lint rules;
- focused tests for behavior;
- browser truth for rendered UI and interaction;
- exact file inspection for documentation or config-only changes;
- React Doctor for high-signal React diff evidence and prioritization.

React Doctor is advisory evidence, not the owner surface. Use it seriously: run the diff scan when it can cheaply inspect the branch, inspect or reproduce high-signal findings against the touched files, and fix branch-caused PR risks. Do not chase score-only findings, but do not dismiss warnings without classifying them with the risk rubric.

React Doctor can be the best discovery oracle. It is not a replacement for the repo's typecheck, lint, focused tests, or browser truth when those are the real proof for the changed surface.

Prefer diff-scoped runs:

```sh
npx react-doctor@latest . --diff <base> --offline --fail-on none --json
```

Add `--project <workspace-or-app>` only after inspecting the repo's package or workspace shape. Use `--no-lint` when React Doctor's bundled lint backend is blocked locally; the repo's own lint command remains the lint oracle.

## Workflow

1. Inspect the touched files or diff and name the owner surface.
2. Run the framework check. For Next.js, read the installed bundled docs before making framework runtime claims. Then choose any additional lens whose smell still applies, including `react-feature-composition` for ownership.
3. If only one lens or oracle applies, use it directly and exit this skill.
4. Choose the relevant lenses and say why each applies.
5. Read only the focused skill refs needed for the observed smells. Skip lens docs when file inspection already answers the question.
6. Classify findings into `PR risk`, `Follow-up`, and `Noise`.
7. Recommend the smallest fix set for this branch.
8. If implementing, patch only that agreed or requested fix set.
9. Prove done with the narrowest real oracle: typecheck, lint, focused test, React Doctor-backed inspection, browser truth, or exact file inspection.

## Prompt Templates

Review mode:

```text
Use the React build lens on the current React diff only if multiple lenses
or evidence oracles could apply. Pick only the relevant skills, classify
findings as PR risk / follow-up / noise, and recommend the smallest
branch-specific fix set. Do not fix all warnings.
```

Implementation mode:

```text
Use the React build lens. Patch only the agreed fix set, preserve behavior, and
prove it with the narrowest real oracle for each touched surface.
```

Closeout:

```text
Name the lenses used, changed files, validation run, and remaining risk.
```
