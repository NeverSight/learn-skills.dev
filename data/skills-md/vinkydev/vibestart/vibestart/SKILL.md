---
name: vibestart
description: Use the vibestart CLI to create a TypeScript project, choose a stack or recipe, add capabilities such as Knip, Ultracite or Docker, diagnose project state, upgrade templates while preserving business edits, or recover an interrupted operation. Use when the user mentions vibestart, asks to maintain a project with vibestart.jsonc and .vibestart metadata, or needs help with these CLI workflows. Not for ordinary application feature development unrelated to the CLI.
---

# VibeStart CLI

Use the CLI to resolve stacks and maintain generated projects. Let its current help, capability list, and change plan determine what is supported; do not reconstruct templates or hand-edit maintenance metadata.

## Establish the context

1. Identify the target directory and whether the request is creation or maintenance. Read the project's instructions. For an existing project, inspect `vibestart.jsonc`, `package.json`, Git status, and the presence of `.vibestart/state.json` and `.vibestart/base.json`. Preserve unrelated edits.
2. Run the CLI from npm with `npx --yes vibestart-cli` (or `pnpm dlx vibestart-cli`); a global install is not required. Resolve its version with `npx --yes vibestart-cli --version`. For a preview followed by application, append `@` and that exact published version to the package name in both commands so a new release cannot change the target between them.
3. Installing this skill does not install the CLI, Vite+, or project dependencies. If a required tool is unavailable, follow its installation instructions within the user's scope rather than changing the selected stack.
4. Read `npx --yes vibestart-cli --help` for creation or `npx --yes vibestart-cli COMMAND --help` for maintenance. Prefer `--json` for operations executed by an agent; keep stdout separate from stderr. Do not parse a task runner's banner as JSON.

## Choose the workflow

Read the relevant reference before acting. Paths are relative to this skill's directory, not the user's project.

| User intent                               | First action                                       | Reference                                                       |
| ----------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------- |
| Create a project or use a recipe          | `npx --yes vibestart-cli --list --json`            | [Creating projects](references/create.md)                       |
| Add a capability                          | `npx --yes vibestart-cli add --list --json`        | [Maintenance](references/maintenance.md#add-capabilities)       |
| Diagnose an existing project              | `npx --yes vibestart-cli doctor --offline --json`  | [Maintenance](references/maintenance.md#inspect-project-state)  |
| Update a generated project                | `npx --yes vibestart-cli upgrade --dry-run --json` | [Maintenance](references/maintenance.md#upgrade-templates)      |
| Finish or undo an interrupted operation   | Inspect the pending state with `doctor`            | [Maintenance](references/maintenance.md#recover-an-operation)   |
| Establish provenance for an older project | Locate its original snapshot                       | [Maintenance](references/maintenance.md#adopt-an-older-project) |

Run maintenance from the generated project root, or pass `--cwd /actual/project/path`. Creation instead takes a positional destination directory; it has no `--cwd` option.

## Execute within the requested scope

- Preview changes before writing. When the user has requested the operation and the plan meets that scope, proceed without an extra permission loop. Ask only about missing product choices or material changes outside the request. A request to inspect or preview does not authorize applying the plan.
- Creation uses `--json` to disable prompts. Maintenance writes additionally require `--yes`. Do not pass `--yes` to creation.
- The package manager and Hono runtime are separate choices: `--package-manager bun` selects dependency installation; `--runtime bun` selects Hono execution. Neither changes the other or moves the Vite+ test toolchain to Bun. Do not replace `vp test` with `bun test` or force the CLI to run under Bun.
- Existing projects use `add` and `upgrade`. Do not scaffold over them, replace their baseline with current business files, or edit a recipe to simulate a supported migration.
- Respect the environment's installation and service restrictions. Normal creation and maintenance writes run setup/checks. If these are unavailable, use a read-only preview, or explicitly defer installation when file writes are in scope. `--full-check` can start services and browsers.
- Keep `.vibestart/state.json` and `.vibestart/base.json` together in version control. Leave pending-operation records intact until the operation is recovered, aborted, or rolled back through the CLI.

## Report the actual result

State the CLI version, target project, selected changes, returned status, checks actually run, and any remaining action. For machine output, inspect both exit code and JSON fields. A successful preview, `doctor` result, or historical stack verification record is not evidence that this project's tests passed. `needs-install` is an unfinished operation even though its exit code is zero.

Use the project's generated tasks for subsequent work: `vp install`, `vp check`, and the tasks present in `package.json` or `vite.config.ts`. `vp run ready` runs the full project validation chain. Do not assume a task exists when its optional capability is absent. The generator repository's `vp run deps update` is a maintainer command, not the generated project's upgrade command.
