---
name: react-feature-composition
description: Guide React or Next.js feature composition before implementation and during reshaping. Use when designing feature structure, route/runtime boundaries, services, selectors, controller hooks, presentation models, layout/view ownership, typed view variants, focused effects, or large UI surfaces with prop soup and hidden dependencies.
---

# React Feature Composition

Shape React features around explicit ownership and small renderable models.

Core contract:

- Controllers derive models. Views render models.
- Services transform. Selectors query. Controllers coordinate.
- Preserve behavior unless the task explicitly includes UX change.

## Read First

Always read `LANGUAGE.md`. It is the vocabulary contract.

Load focused refs by need:

- `references/refactor-candidates.md` for smells, candidate output, and deepening checks.
- `references/model-interface-design.md` for large controller/model design choices.
- `references/validation.md` before calling implementation done.

## Related Skills

Select a related skill when its concern appears in the task. If a selected skill is missing, ask the user before running its install command.

- `vercel-react-best-practices`
  ```sh
  npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
  ```
- `vercel-composition-patterns`
  ```sh
  npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-composition-patterns
  ```
- `next-best-practices` (optional review checklist; install only when explicitly requested)
  ```sh
  npx skills add https://github.com/vercel-labs/openreview --skill next-best-practices
  ```
- `web-design-guidelines`
  ```sh
  npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
  ```

Use local `ui-text` when semantic text, copy, typography, or token hygiene matter:

```text
/Users/cflack/Repos/callumflack/ds-kit/skills/ui-text
```

## Target Shape

Many features do not need a Controller. Static lists, one-submit forms, obvious leaf extractions, and already-separated behavior may only need a rename, a leaf split, or no refactor.

The tree below is an upper-bound shape, not a checklist.

When a feature has route gating, host chrome, and multiple runtime views, prefer:

```text
feature/
  page.tsx
  controller.tsx
  feature.tsx
  feature/
    feature-layout.tsx
    feature-view.tsx
    types.ts
    hooks/
      use-feature-controller.ts
      use-embed-presentation.ts
      use-completion.ts
    lib/
      density.ts
      completion.ts
    views/
      intro-view.tsx
      input-view.tsx
      success-view.tsx
```

Ownership rules:

- `page.tsx`: Route Entry only.
- `controller.tsx`: Route Controller only.
- `feature.tsx`: Feature Entry only.
- `use-*-controller.ts`: Controller and Presentation Model derivation.
- `types.ts` or `*-model.ts`: Model types and pure model shape.
- `*-layout.tsx`: Layout View.
- `*-view.tsx`: View Switch only.
- `views/*`: Runtime Views.
- `lib/*`: Services, Selectors, and Pure Helpers.
- `hooks/*`: Effect Hooks and focused subscriptions.

## Workflow

1. Explore the feature and name the current ownership shape using `LANGUAGE.md`.
2. Load `references/refactor-candidates.md`, then identify the dominant smell.
3. Apply the deletion test: if deleting the extraction just moves equal complexity back into callers, it is shallow.
4. Use this recommendation ladder:
   1. Rename for ownership if behavior is already separated.
   2. Extract a Controller when behavior and rendering are mixed.
   3. Extract Services or Selectors when pure logic is repeated, hard to name, or worth testing through a stable seam.
   4. Extract Effect Hooks only when external synchronization has a clear single concern.
   5. Introduce context only when data is ambient and deeply shared.
5. Present candidates using the output contract below. Do not jump straight to file moves when the model interface is still unclear.
6. Choose the smallest shape that gives better locality. Explicitly say when the correct outcome is no Controller.
7. For large model choices, run `references/model-interface-design.md` before editing.
8. Implement in small behavior-preserving steps.
9. Validate with `references/validation.md` and use its done checklist.

## Output Contract

For planning or review, present each candidate as:

- **Files**: current files/modules involved.
- **Problem**: the ownership or locality problem.
- **Proposed shape**: route/controller/model/view/service/selector split.
- **Why**: how this reduces caller knowledge, prop threading, or effect coupling.
- **Test seam**: where behavior should be verified.
- **Risks**: behavior, routing, rendering, or type risks.

For implementation, report:

- changed files
- final ownership shape
- validation run
- remaining risk

## Patterns

Controller output should be a Presentation Model, usually:

```ts
type PresentationModel = {
  layout: LayoutModel;
  view: ViewModel;
};
```

`ViewModel` should be a discriminated union. Each view kind carries only the data and actions that view can use.

Effects are for external synchronization only. Derive renderable model state during render.

Context is for ambient, deeply shared data. Do not use context to hide prop soup that should be solved by a better model.

## Finish

Before calling implementation done, load `references/validation.md` and use its done checklist.
