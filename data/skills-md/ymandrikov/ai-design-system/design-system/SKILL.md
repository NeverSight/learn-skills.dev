---
name: design-system
description: Organise and maintain a consistent design system through contracts, discovery, reuse and verification. Handles locally added external components, design-only component and consumer changes, initial setup, adoption and migration, analysis, gaps and triage; component internals and business logic remain project-owned.
---

# Design system

One entrypoint, two workflows with separate responsibilities. The framework governs
design-system work and its checks; implementation and engineering test methods follow
the project's procedures. Read
[the shared model](reference/model.md) once, then the procedure for the request.
Load supporting references only when their stated condition applies.
Within a project workflow, act as its design-system specialist under the
[shared responsibility boundary](reference/model.md#authority-and-task-scope).

## Choose the workflow

Accept explicit `design-system craft <request>` and `design-system use <request>`, or infer
the workflow from the requested result. An explicit mode sets the scope; a missing
capability does not expand it.

| Requested result | Read and follow |
| --- | --- |
| Add external component sources to the project, or document a manual addition | [craft external-component adoption](reference/craft.md#adopt-locally-added-external-components) in the same task |
| Survey and improve design-system consistency, including related consumer presentation while preserving logic | [improve](reference/improve.md); read-only survey, then one choice to document or implement |
| Create or maintain components' design, layouts, patterns, contracts, tokens, rules or availability; fix a design-system gap | [craft](reference/craft.md) |
| Build or change a product interface by selecting and composing the system's public capabilities | [use](reference/use.md) |

`craft` delivers reusable system capabilities and evidence for their promises.
`use` delivers a product interface and evidence for its composition and behaviour.
A page request authorises product work and suitable local fallbacks; shared component
development and system rule changes require craft scope. Record a reusable shortfall
as a gap and hand it off to craft. Recording it does not authorise the repair.

An authorised external-component addition includes its bounded contract and index
work through craft, even when another project skill owns installation. Direct
library imports are outside this route; a page request alone does not authorise
installing new components.

When both workflows are authorised, identify their separate stages and results.
Follow **craft → checks → use → checks**: verify the shared capability before using
it, then verify its actual composition, subject to explicit migration exceptions.
Existing authorisation counts; crossing the boundary is not an automatic response to
failed discovery. Keep unrelated system work outside the task.

## Standalone procedures

Explicit `design-system improve`, `analyze`, `setup`, `migrate`, `discovery`, `verify`, `gaps` or `triage`, and equivalent natural
language requests, reach the matching procedure directly. These are internal Markdown
instructions, not additional skills. End at that procedure's result; standalone
selection or review does not start implementation. Improve presents its survey before offering documentation or bounded
system changes; its stricter scope remains in force when calling craft.

| Request or workflow condition | Read and follow |
| --- | --- |
| Improve the existing system, or resume saved improvements, preserving logic and allowing scoped consumer design changes | [improve](reference/improve.md); one read-only survey pass, then document or implement and verify |
| Analyze the codebase for component, layout or pattern extraction, consolidation or reuse candidates | [analyze](reference/analyze.md); saved recommendations, with readiness determined by design-system artifacts and indexes |
| Select components, layouts, patterns or tokens; advise how to organise or adapt a composition; assess system coverage | [discovery](reference/discovery.md), read/search only; return the recommendation without writing files |
| Explicitly request project connection or its continuation | [setup](reference/setup.md) |
| Automatically migrate a connected project, or resume a saved automatic migration | [migrate](reference/migrate.md); owns migration modes, batches and completion |
| Check an interface or component against its contracts and design sources | [verify](reference/verify.md) |
| Record or assess a systemic shortfall | [gaps](reference/gaps.md); resolving a system gap belongs to craft |
| Review open gaps, clean the journal or archive and recommend next work | [triage](reference/triage.md); journal/archive maintenance and recommendations |

## Follow links by purpose

- **Read a rule:** consult the named section when its condition applies; this does
  not execute its containing procedure. Reuse already-read unchanged rules.
- **Run a procedure:** perform the named step within the caller's scope and return
  its result to that caller. A called section does not start the rest of its workflow.
- **Hand off work:** return the result, missing inputs or required next stage.
  Execute that stage only under existing authority or a new authorised request.

Read-only discovery keeps its own scope when called by a writable workflow.
Missing context and handoffs do not expand authority; useful calls with returns
remain valid, without recursively restarting their callers.
