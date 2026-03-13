---
name: devlaunch
description: Configure a repository for devlaunch by generating manifest and state files that match the strict runtime contract.
---

# Devlaunch Skill

Use this skill when a repository must be initialized or updated for `devlaunch`.

## Source Of Truth

The only normative references are:

- `references/manifest.v1.schema.json`
- `references/state.v1.schema.json`

Templates and examples are only helpers. They are not the contract.

Every generated or edited `.devlaunch/manifest.json` and `.devlaunch/state.local.json` must match the strict v1 schemas exactly.

If a field is unknown, unsupported, or missing, treat the document as invalid and say so before proceeding.

## Existing Repository Rule

If the skill is called again on a repository that already contains `.devlaunch` files, do not guess.

Ask which of these three actions the developer wants:

1. Recreate from scratch
2. Adapt the existing files to the latest supported manifest/state contract
3. Do nothing

Do not silently overwrite an existing manifest or state file.

## Workflow

Order is mandatory:

1. Ask the developer which tools they use to work on the project.
2. Ask how they usually launch the project day to day.
3. Ask which tools should stay open or be treated as optional.
4. If `.devlaunch` already exists, ask whether to recreate, adapt, or leave it unchanged.
5. Inspect the repository to confirm and complete the picture.
6. If the repo is not initialized yet, run `devlaunch init` first so the baseline files are created safely.
7. Adapt `.devlaunch/manifest.json`.
8. Adapt `.devlaunch/state.local.json` only when needed.
9. Validate both files against the strict v1 schema before considering the task complete.
10. Register the project through `devlaunch init` or the runtime.

## Questions To Ask First

Ask explicitly:

1. Which developer tools do you need open for this project?
2. Which commands do you usually run, and in what order?
3. Which commands are interactive long-running services?
4. Which external apps are required on your machine?
5. Which items should be optional rather than auto-started?

Do not skip these questions unless the developer already answered them in the current conversation.

## Use The Local Assets

Use these assets intentionally:

1. `references/`
   Read the strict schema references first.

2. `assets/templates/`
   Use them only as a starting shape for new files.

3. `assets/examples/`
   Use them only as examples of valid files.

## Constraints

- The manifest may only contain `apps` and `services`.
- `docker compose up -d` must be modeled as a `service`.
- The target platform is Windows.
- The shell is PowerShell.
- `startPolicy` and `stopPolicy` are explicit per resource.
- `checks.start` and `checks.status` are explicit per resource.
- `checks.*.mode` must always be present.
- `devlaunch init` must be safe on existing projects.
- Never produce fields outside the supported v1 schema.
