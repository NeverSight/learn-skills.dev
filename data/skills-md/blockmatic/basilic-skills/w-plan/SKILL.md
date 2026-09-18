---
name: w-plan
description: Write an ordered plan without changing implementation.
disable-model-invocation: true
---

Planning does not implement, branch, or commit. A single already-clear change uses `/w-build`. A blocking product gap uses `/w-clarify`.

1. **Goals**: 3–7 bullets for scope, success, constraints, non-goals.
2. **Context**: matching glob rule and skill, then topic MDX (or this repo’s docs path). Rules override skills. Inspect affected packages, README, scripts. Durable product/architecture: `PRODUCT.md` and matching MDX/ADR. Generated outputs name an owning source; commands come from inspected scripts.
3. **Assumptions**: 3–5 bullets. Defer product scope, secrets, and destructive ops.
4. **Tasks**: ordered work with likely files and dependencies. Uncertain work first. Diagram only if relationships need one.
5. **Output**: user’s path, else the repo’s existing plan file, else chat. Sections: Goals, Assumptions, Tasks, Risks, **References** (plain paths to each rule, skill, and MDX used — no `@`). Do not create another backlog or overwrite another unfinished plan.
