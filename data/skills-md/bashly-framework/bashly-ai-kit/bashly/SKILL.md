---
name: bashly
description: |
   Build and maintain Bash command-line applications with the Bashly generator.
   Use when users ask to create a Bashly project, design command trees, define
   flags/arguments/options in `bashly.yml`, generate Bash scripts from Bashly
   config, write command/lib partials in the Bashly source folder, or iterate on
   existing Bashly-based CLIs from idea to complete script (for example: "this is
   a bashly project" or "help me build a bash script using bashly").
---

# Bashly Skill

Use this workflow to produce or update Bashly CLIs.

## Follow Workflow

1. Confirm project mode.
   - Detect whether the user has an existing Bashly project or needs a new one.
   - For existing projects, inspect current Bashly settings and source folder layout before editing.
   - Use `references/bashly-workflow.md` to locate the effective `bashly.yml` when defaults are overridden.
   - When users need non-default paths, add or update settings with `bashly add settings`.

2. Define CLI contract before editing files.
   - Capture command groups, subcommands, required args, optional args, and flags.
   - Confirm naming and UX details (short flags, long flags, help text, defaults, required constraints).

3. Author or update `bashly.yml`.
   - For new projects, initialize with `bashly init` or `bashly init --minimal` based on requested scope.
   - Prefer incremental edits to preserve compatibility in existing projects.
   - Keep descriptions concise and user-facing.
   - Keep command trees predictable and avoid unnecessary nesting.

4. Implement command behavior in Bashly partials.
   - Resolve the active source folder first (default `src`, or overridden in settings/env).
   - Create or update command and shared partial files in that source folder.
   - Keep business logic in partials so regeneration remains safe and repeatable.

5. Generate CLI files with Bashly.
   - Run the Bashly generation command from the project root.
   - If generation is unavailable in the environment, still produce valid `bashly.yml` and list the exact generation command for the user.

6. Validate behavior.
   - Check shell syntax for generated scripts when possible.
   - Exercise representative command paths (`--help`, one success path, one argument/flag error path).

7. Document what changed.
   - Summarize command tree changes and any backward-incompatible flag/argument changes.
   - Summarize which partial files were added/updated in the source folder.
   - Provide quick usage examples for the most important commands.

## Use Bundled Resources

- Read `references/bashly-workflow.md` for command design heuristics, common Bashly operations, and troubleshooting.
- Use the icon asset in `assets/` for skill metadata/UI integration when relevant.

## Use Online Sources

- When internet access is available, verify syntax and options against official Bashly docs before finalizing changes.
- Prioritize sources in this order: Bashly docs (`bashly.dev`), official examples, then `bashly-framework/bashly` repository.
- Use online sources especially for settings behavior, advanced features (`bashly add ...`), and version-sensitive commands.
- If internet access is unavailable, continue using local project files and `references/bashly-workflow.md`, then state that online verification could not be performed.

## Output Expectations

- Produce only files needed for the requested CLI behavior.
- Ensure required source partials are present so generated scripts implement the requested behavior.
- Keep generated UX consistent: clear descriptions, stable command names, and practical defaults.
- Prefer explicit examples in final responses (`tool command --flag value`) for each major command.
