---
name: tech-lead-setups
description: 'Scaffold a new project as the Tech Lead would in Sprint 0, after the task breakdown and before coding standards are written. Grills on folder structure, architectural patterns, commit hooks, tooling, the test harness, and stubs, then executes the scaffold: directory layout, local tooling config, pre-commit hooks, a test harness with one e2e smoke flow, and endpoint/page stubs that return mock responses so frontend and backend can build in parallel from day one. On a running project it audits first and adds only what is missing. Use when the user wants to set up, bootstrap, or scaffold a project, add a test or e2e harness, stand up the repo skeleton, do Sprint 0, or asks to "set up the project".'
---

# Tech Lead Setup

Stand up the project skeleton so every developer can start their first card without blocking anyone. This is the Sprint 0 scaffold: structure, tooling, hooks, and stubs, executed from the decisions already made upstream.

This runs **after** `task-breakdown` (the cards, including any Sprint 0 scaffold cards, exist) and **before** `coding-standard` (the standards describe the skeleton this skill creates). Two phases: **grill to lock the setup, then execute it.**

CI workflows are not written here. `github-project-init` owns `.github/`, and its CI runs the aggregate check command this skill defines.

**Running project (adopt mode).** If the repository already has code, do not scaffold. Audit what exists against the list in Phase 1, show the gaps, and add only the missing pieces, most often the test harness. Never restructure existing folders.

## Phase 1: Grill

**Read `docs/technical-specs/` first; it is the source of truth for this scaffold.** The repository structure, tech stack, module definitions, and environment configuration are already decided there: read the repository-structure spec for the directory tree, the tech-stack spec for the runtime, tooling, and versions, the module-definitions spec for the per-module surface, and the environment-configuration spec for the env vars. In the current layout these are `03-`, `04-`, `05-`, and `11-`; in an older layout, match them by topic name. Also read the Sprint 0 cards in `docs/task-breakdown/sprint-0.md` (or `docs/TASK_BREAKDOWN.md` in an older project), the endpoint contracts in `docs/api-specs/`, and any conventions in `CLAUDE.md`. Pull every decision you can from these and confirm it rather than re-deciding; the grill only fills genuine gaps. If `docs/technical-specs/` does not exist, say so and run `technical-spec` first, because scaffolding without it means inventing architecture the rest of the pipeline has not agreed to.

Interview the user one question at a time, recommending an answer each, until the setup is fully pinned. This is a grill, not a form: ask the live question, give your recommendation and the one reason it wins, wait, then walk the branch that answer opens before starting the next topic. Don't paste the list below as a questionnaire.

- **Folder structure.** Monorepo vs polyrepo, workspace layout, where app code, shared code, modules/features, tests, scripts, and docs live. The exact tree to create. Recommend grouping by feature: each feature folder holds its handler, service, repository, and tests. Group by layer only when the platform sets the structure.
- **Patterns.** The per-module / per-feature file pattern the scaffold must reproduce (e.g. backend module = route + service + repository + schema + test per endpoint; frontend feature = model + presenter + view). This is the architecture-pattern decision the whole scaffold repeats, so pin it concretely, not abstractly: propose the pattern derived from `05-module-definitions.md`, **write out the actual file tree for one real module as a worked example**, and get the user's sign-off on that example before generalizing it across every module. A new file should be obvious to place. The pattern is where the project's **seams** get placed (terms in [../technical-spec/references/module-design.md](../technical-spec/references/module-design.md#vocabulary)): the split should keep the deep logic in one place (the service) with the swappable parts (repository, external clients) behind injectable seams, so tests run against the service's interface and adapters can vary. A pattern that scatters one module's logic across many shallow files is the smell to avoid.
- **Commit hooks.** Pre-commit runs the format check, the linter, and the type-checker on staged files; the full check runs before hand-off. Use the `setup-pre-commit` skill for the mechanics; it wires the project's own commands. If that skill is not available, install the hooks directly with the same three steps. On Claude Code, offer the `git-guardrails-claude-code` hook for destructive-command protection.
- **Tooling.** Package manager and lockfile, type-checker, linter, formatter, build. Take the linter, formatter, and complexity rule from the tooling table in `coding-standard`'s `references/baseline-rules.md`: for JS/TS that is oxlint with the anti-slop plugin, oxfmt, and a cyclomatic complexity limit of 10. [references/anti-slop.md](references/anti-slop.md) gives the plugin's install steps. The exact `scripts` entries and an aggregate check command (e.g. `complete-check`) that CI will run.
- **Test harness.** The unit and integration runner, a test database or in-memory stand-in with fixtures, the e2e tool from the tech-stack spec, and the contract-test pattern if the project uses mocks. `task-breakdown`'s wiring cards prove their AC with an e2e flow, so the e2e tool must exist before the first wiring card.
- **Stubs.** Which endpoints and pages to scaffold and the mock-response shape. The point of stubs: a stub returns a contract-valid hardcoded response (matching `docs/api-specs/` where present) so frontend integrates against it from day one and no one is blocked. Confirm the stub depth (mock response only, vs real health probes, etc.).

Surface contradictions against the specs ("the tech-stack doc says Bun but there's a `package-lock.json` here, which wins?") and flag anything underspecified before creating files. When the setup is locked, summarize what you will create and confirm before executing.

## Phase 2: Execute

Create the scaffold for real. Group the work and report what you create.

1. **Initialize** the project with the chosen package manager; write the manifest, lockfile, and `scripts` entries.
2. **Create the directory tree** exactly as agreed, with a placeholder or index file in each directory so the structure is committable and navigable.
3. **Write tooling config** for the type-checker, linter (with the complexity rule), and formatter. Pin versions.
4. **Set up the test harness**:
   - the unit runner, with one passing example test per layer (for example service and handler), in the project's test layout;
   - a test database or an in-memory stand-in, with a fixture loader and a reset between tests;
   - the e2e tool, with one smoke flow that loads the app and hits one stub end to end;
   - e2e settings that keep local runs light: a capped worker count read from an env var, one headless browser locally (the full browser matrix in CI), reuse of a running dev server, traces and video only on failure, a tag for heavy scenarios that local runs skip, and a global teardown that stops every process the suite started;
   - the contract-test pattern if the project mocks external services: a mock must parse against its schema, and a deliberately broken copy must fail;
   - `scripts` entries for each. Wire the unit and integration tests into the aggregate check command. Keep e2e as its own script (for example `test:e2e`) that CI runs, so the local gate needs no browser and no live services. Add `test:e2e:full`, which also runs the heavy-tagged scenarios, and `check:fast`: type-check, lint, and the unit tests that need no database. `github-project-init` runs `check:fast` on pushes to the long-lived branches and the full set before each build.
5. **Install commit hooks** via the `setup-pre-commit` skill, so the format check, the linter, and the type-checker run on staged files, and the commit-msg and branch checks read the coding standard's `pr-hygiene` block. Add the guardrail hook if requested.
   If the team uses Claude Code, add `.claude/settings.json` with `{"attribution": {"commit": "", "pr": ""}}`. It stops the agent from adding a co-author trailer and a "Generated with" line. The commit-msg hook and CI catch both in any harness.
6. **Scaffold stubs**: one stub per endpoint following the module pattern, each returning a contract-valid mock response (typed mock constants, matching `docs/api-specs/`), plus page/route placeholders that link the relevant pages per role. Real probe code only where it must be live (e.g. health checks). Mark each stubbed operation `SCAFFOLD` in the Operation Status Tracker of `docs/api-specs/_index.md`.
7. **Generate shared types/constants** if the structure has a shared package.

## Verify

Run the project's own gate end to end and confirm a clean baseline before handing off:

```
<type-check> && <lint> && <format-check> && <test> && <build>
```

Use the exact commands established in the grill. The scaffold must pass green on an empty project: stubs compile, mock responses satisfy their contracts, the example tests and the e2e smoke flow pass, and hooks fire. Report the result. If a gate cannot run here (missing runtime), say so explicitly rather than claiming a pass.

## Notes

- Composes with `setup-pre-commit` (hooks) and `git-guardrails-claude-code` (destructive-command protection); invoke them rather than re-implementing.
- The scaffold is the thing `coding-standard` then describes and `lead-review` enforces, so keep the patterns consistent with what those skills will document.

## Writing conventions (enforced in all output)

- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- If a document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
