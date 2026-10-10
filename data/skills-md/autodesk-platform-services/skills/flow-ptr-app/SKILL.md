---
name: flow-ptr-app
description: "Guide for developing a new Flow Production Tracking (FPTR) / ShotGrid Toolkit (sgtk) app following a Spec-driven approach. Triggers on: create a new FPTR app, new Flow Production Tracking app, new Toolkit app, tk-multi-starterapp, sgtk app development, tank install_app, tank switch_app, dev sandbox pipeline configuration, ShotGrid Toolkit app."
---

# Create a Flow Production Tracking (FPTR) Toolkit App

This skill guides developers and pipeline engineers through building an FPTR app, following a
**spec-driven** way — capture intent, check for reuse, write and validate a spec, plan, then
implement, verify, release, and maintain against that spec. Tell the user which phase (below)
you're starting before acting in it, so they can track progress and step in between phases.

Reference guide: [Developing a Toolkit App](https://help.autodesk.com/view/SGDEV/ENU/?guid=SGD_pg_developer_pg_sgtk_developer_app_html)
Default app template repo: https://github.com/shotgunsoftware/tk-multi-starterapp

## App spec-driven lifecycle

Each step below that has mechanical how-to links to a `references/*.md` guide — read it while
executing that step, not before; keep the skill itself light and pull in detail only when it's
actually needed. Phases 2, 7, and 9 have no dedicated guide — they're about the spec and process
rather than a tool/config action.

- **Phase 1 — Requirements/Intent capture**
   - Step 1.1 — Ask for the business need, and capture it in a short spec (one paragraph or a few
     bullet points) — what the app should do, on which context and environment it will run,
     whether it needs a UI, whether it needs toolkit hooks, constraints and acceptance criteria.
   - Step 1.2 — Find if an existing app / project setting / hook cover fully or partially the
     requirements, and confirm with the user whether later we will fork/extend from that tool or
     scaffold a new app from the starter template. Read
     [references/existing-functionality.md](references/existing-functionality.md) while executing
     this step.
- **Phase 2 — Specification** — before cloning anything, write down what the app does:
   - Step 2.1 — Clarify the goal, the app name, dependencies on Flow PTR frameworks/engines, the
     environment the tool runs in (e.g. Sequence/Shot/Episode-specific), the entities involved, the
     settings schema, which hooks the tool may need to expose and why, whether it needs a UI, and
     its acceptance criteria.
   - Step 2.2 — Validate the spec before planning: check it for internal contradictions, missing
     edge cases (no-UI/headless path, permissions, multi-engine support), and security/data-privacy
     concerns (e.g. what PTR fields/entities the app reads or writes). Flag gaps to the user instead
     of assuming an answer; only move to Phase 3 once the spec is complete and consistent.
- **Phase 3 — Plan/Design**
   - Step 3.1 — Locate the project's pipeline configuration and figure out how it's set up
     (centralized vs. distributed). Read
     [references/locating-config.md](references/locating-config.md) while executing this step.
   - Step 3.2 — Find or create a sandbox or a dev configuration if it doesn't exist. Read
     [references/sandbox-dev-configuration.md](references/sandbox-dev-configuration.md) while
     executing this step.
   - Step 3.3 — Clarify where the app's source code should live, and how it will be installed into
     the target configuration (dev path vs. install_app + switch_app). Read
     [references/cloning-template.md](references/cloning-template.md) and
     [references/install-app.md](references/install-app.md) while executing this step.
   - Step 3.4 — Break the spec into a technical plan: architecture decisions, file/module
     breakdown, sequencing of work, identification of risks or open questions. Where practical,
     decide to keep core logic separate from UI code (e.g. `app.py`/a logic module stays
     UI-agnostic, with `dialog.py` calling into it) — this is what lets Phase 6 exercise the tool
     as a headless command in `tk-shell` before wiring up the dialog. Read
     [references/implement-app.md](references/implement-app.md) while executing this step for how
     that split plays out in code.
   - Step 3.5 — Split the plan into discrete, independently verifiable tasks/tickets, each with
     clear inputs/outputs and acceptance criteria, so that the work can be parallelized and
     tracked.
- **Phase 4 — Scaffold**
   - Step 4.1 — Clone the reference tool — `tk-multi-starterapp` by default, or whichever existing
     app Phase 1 found as a better fit. Read
     [references/cloning-template.md](references/cloning-template.md) while executing this step.
- **Phase 5 — Implement against spec**
   - Step 5.1 — Fill in `info.yml` and implement code with main logic starting in `app.py` and UI
     starting in `python/app/dialog.py`. Declare and implement hooks if applicable. Read
     [references/app-manifest.md](references/app-manifest.md),
     [references/app-hooks.md](references/app-hooks.md), and
     [references/implement-app.md](references/implement-app.md) while executing this step.
- **Phase 6 — Verify against spec**
   - Step 6.1 — Test and iterate using Toolkit's "Reload and Restart" menu item, checked against
     acceptance criteria, not just "does it run". If possible and it has a dependency on UI, test
     first in `tk-shell` or a batch context, then in tk-desktop and then in the target DCC engine,
     if applicable. If app is a Menu Action Item, test it in the FPTR Desktop and then in the web
     UI. Read [references/test-app.md](references/test-app.md) while executing this step.
- **Phase 7 — Change management**
   - Step 7.1 — Commit in git, pushing changes only to the sandbox configuration, not
     production.
   - Step 7.2 — Future feature changes update the spec first (Phase 2, re-validating it per Step
     2.2), then cascade forward through Phases 3-6 — the spec stays the source of truth, not the
     code.
- **Phase 8 — Release to production**
   - Step 8.1 — Once ready for release, warn the user about the implications of bringing to
     production the new changes. Analyse possible side effects or interruptions to workflow.
   - Step 8.2 — Tag a release and push the sandbox config changes to the production pipeline
     configuration. Read [references/release.md](references/release.md) while executing this
     step.
- **Phase 9 — Maintenance**
   - Step 9.1 — Treat post-release bug reports or new asks as spec changes, not code patches: update
     the spec first (back to Phase 2), validate it again, then re-enter Phase 3 and cascade forward
     through Phases 4-8 — the spec stays the source of truth for the life of the app, not just
     during initial development.

## Reference guides — skip the phases

The phases above are one way to work through building an app — spec-driven, with an explicit
plan/verify loop. If you're following a different process instead (your own tickets, a different
planning method, or you're just experienced enough with Toolkit not to need the scaffolding), use
this table to jump straight to the how-to you need. Each guide is self-contained and doesn't assume
you've read the phases above.

| Guide | What it covers |
|---|---|
| [references/existing-functionality.md](references/existing-functionality.md) | Toolkit's customization ladder, GitHub org search for reuse, and reference apps to study for architecture patterns |
| [references/locating-config.md](references/locating-config.md) | Finding the project's `PipelineConfiguration` and detecting centralized vs. distributed setup |
| [references/sandbox-dev-configuration.md](references/sandbox-dev-configuration.md) | Finding or creating a dev sandbox instead of developing against production |
| [references/cloning-template.md](references/cloning-template.md) | Naming convention and where/how to clone the starter template (or another existing app) |
| [references/install-app.md](references/install-app.md) | Wiring the app into an engine/environment via a `dev` descriptor or `install_app`/`switch_app` |
| [references/app-manifest.md](references/app-manifest.md) | `info.yml` manifest fields — engines, settings schema, frameworks, version requirements |
| [references/app-hooks.md](references/app-hooks.md) | When and how to add a hook, and how studios override it per-project |
| [references/implement-app.md](references/implement-app.md) | `app.py`/`dialog.py` structure, UI vs. no-UI paths, web menu actions, custom events |
| [references/test-app.md](references/test-app.md) | Reload-and-Restart loop, `tk-shell`-first testing, granting testers sandbox access |
| [references/release.md](references/release.md) | Versioning, tagging a release, and pushing config changes to production |
| [references/centralized-config.md](references/centralized-config.md) | Access checks and on-disk layout for centralized (classic) pipeline configurations |
| [references/distributed-config.md](references/distributed-config.md) | Descriptor types and what to do for each, for distributed pipeline configurations |
| [references/python-api-best-practices.md](references/python-api-best-practices.md) | Performance, API-key hygiene, and design guidance for `sg.find`/`sg.create` calls |

## Flow PTR documentation

- **User documentation** — getting-started guides and know-how articles by production role:
  https://help.autodesk.com/view/SGSUB/ENU/
- **Developer documentation** — technical guides for pipeline leads/devs: Toolkit, tools,
  configurations, APIs, integrations, troubleshooting:
  https://help.autodesk.com/view/SGDEV/ENU/
