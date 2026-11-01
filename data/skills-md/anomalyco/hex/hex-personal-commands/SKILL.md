---
name: hex-personal-commands
description: Configure Hex personal deterministic transcript transformations in `~/.config/hex/hex.config.ts`. Use when the user wants to add or change custom text transformations for the Hex voice app.
license: MIT
---

# Hex Personal Transformations

This skill targets current Hex (dev builds now, and the next stable release).
Hex 2.3.1 uses an older runtime; its matching skill installs with
`npx skills add anomalyco/hex#app-v2.3.1 --skill hex-personal-commands`.

Hex runs `~/.config/hex/hex.config.ts` itself, in an embedded JavaScript
engine. There is no package to install and no build step.

1. Check for `~/.config/hex/hex.config.ts` (or `hex.config.js`). If it is
   missing, ask the user to open Hex's Modes pane and choose Create Config,
   or run `hex commands init` if the `hex` CLI is available.
2. Read `~/.config/hex/AGENTS.md` for the current API and limits, and
   `hex.d.ts` for exact types. Hex owns both and rewrites them; do not edit
   them.
3. Edit only the config and files it imports. Scripts are plain TypeScript or
   JavaScript: they can import `@hex/commands` and files in the folder, not
   npm packages, Effect, or Node APIs, and they have no filesystem, network,
   or timer access. Enums, namespaces, and constructor parameter properties are
   rejected.
4. Use `defineHexConfig` from `@hex/commands` and declare pure `transformations`
   entries (`{ id, name, description?, transform(text, context) }`).
5. Transformations must be selected in the mode's Transformations section.
   They run after mode corrections and optional AI rewriting, not for meetings.
6. Run `hex commands check` (macOS) after editing. It loads the config as Hex
   does and prints what it registers or the error with file, line, and column.
   Optionally type-check with `npx -y -p typescript tsc` in `~/.config/hex`. A
   running Hex reloads the config on save and shows load errors in Modes'
   Transformations section.
   If `hex` reports `commands check` as an unrecognized subcommand, stop: the
   user is on an older Hex (such as 2.3.1). Tell them to install the matching
   skill with `npx skills add anomalyco/hex#app-v2.3.1 --skill hex-personal-commands`,
   or to switch to the dev build (https://github.com/anomalyco/hex#install-hex).

Completion criterion: the requested behavior is represented in the config,
`hex commands check` succeeds (or, without the CLI, the reload succeeded in
Hex), and any verification gap is reported.
