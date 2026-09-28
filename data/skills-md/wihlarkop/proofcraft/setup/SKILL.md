---
name: setup
description: >-
  Initialize or reconcile workspace operating context for coding agents. Use for a fresh workspace
  or repository, first-time project onboarding, a materially changed project structure, or an
  explicit request to create/reconcile AGENTS.md and project context. Preserve existing human
  instructions; do not invent undecided architecture or mutate a project merely because the suite
  was updated.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.2"
---


# Setup

Establish the minimum durable context an agent needs to work safely in a project workspace.

## Trigger

Use for greenfield workspace/repository initialization, first-time onboarding after this suite is installed, explicit AGENTS/project-context reconciliation, or a material project/tooling reorganization.

Do not use for normal feature work.

## Workflow

1. Read the relevant shared constitution and run a focused reality check.
2. Detect workspace capabilities before using them. Determine whether the folder is a Git repository from project-local evidence before running Git commands; treat Git as optional rather than assuming it exists.
3. Classify the project as greenfield or existing based on meaningful project content. Installed agent-skill directories and skill lockfiles are tooling context, not application source.
4. Inspect existing `AGENTS.md`, project layout, manifests, task runners, docs, ADR/product/design artifacts, CI configuration, and obvious optional specialist capabilities. Do not exhaustively inventory the workspace when a pointer is enough.
5. Use capability-aware probes: an empty search/no-match is normal evidence, not a workflow failure. Avoid bundling expected no-match or unavailable-tool probes into commands whose non-zero exit obscures successful inspection.
6. For greenfield projects, create only minimum navigation/context. Leave undecided architecture explicitly undecided.
7. For existing projects, preserve established conventions and human-authored instructions. Manage only the marked block in `AGENTS.md` when one is created.
8. Keep `AGENTS.md` thin, but ensure its managed block contains the bootstrap guards from the shared AGENTS guidance: project-local context is authoritative before task-specific skill loading; unrelated global/harness memory is not project authority; Git is optional and must not be probed until repository presence is established; unrelated work must be preserved.
9. Record the workflow schema and suite-major compatibility in project context when this project adopts the suite.
10. When setup is explicitly rerun after Proofcraft guidance changes, reconcile only the managed AGENTS block and stale project orientation needed to adopt compatible bootstrap rules; do not mutate application/product/architecture artifacts merely because the suite changed.

## Outputs

Normally:
- a thin `AGENTS.md` managed block;
- `docs/agents/project.md` or the project's established equivalent;
- an ADR directory/convention only when one does not exist and architecture decisions are expected.

Do not initialize Git/source control unless requested or already established. Do not create fake product, design, or architecture decisions just to populate files.

## Stop

Stop when the project is navigable, bootstrap context guards are durable, human content is preserved, canonical sources are discoverable, and no invented decision has been introduced.
## Reference Guide

Load only the references needed for the current task:

- [existing project](references/existing-project.md)
- [greenfield](references/greenfield.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [artifact model](references/_shared/artifacts/artifact-model.md)
- [agents md](references/_shared/artifacts/agents-md.md)
- [project context](references/_shared/artifacts/project-context.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [diff discipline](references/_shared/engineering/diff-discipline.md)
