---
name: sasjs-lint
description: Linting and formatting SAS code with @sasjs/lint - the .sasjslint rules and their defaults, severityLevel and exit codes, per-file @sasjslint overrides, what the formatter fixes, and how the SASjs CLI, VS Code extension and SASjs Server run it. Use when configuring lint rules, resolving a lint warning, or wiring lint into CI, a git hook or an editor.
license: MIT
copyright: Copyright (c) SASjs
spdx-license-identifier: MIT
---

# @sasjs/lint

<!-- SPDX-License-Identifier: MIT -->

`@sasjs/lint` is the linting and formatting engine for SAS code. It is a TypeScript library with no SAS dependency - it reads `.sas` files as text - and it is the single engine behind `sasjs lint`, the SASjs VS Code extension's Problems panel, and the SASjs Server Studio editor.

This skill covers the rules, the `.sasjslint` file, the formatter, and the ways to invoke it. It does not cover the SAS language itself (see `sas`) or the rest of the CLI (see `sasjs-cli`).

## When to use

- Writing or changing a `.sasjslint` file
- A `sasjs lint` run reports a warning and you need to know what it means or how to silence it
- Adding lint to a CI pipeline or a git pre-commit hook
- Running the formatter (`sasjs lint fix`, format-on-save, `formatText`)
- Explaining why a rule does or does not fire in an editor

## Where it runs

| Surface | How it is invoked | Notes |
|---|---|---|
| SASjs CLI | `sasjs lint`, `sasjs lint find`, `sasjs lint fix`, `sasjs lint init` | `find` is the default subcommand. `init` writes a `.sasjslint` at the project root holding the full default config |
| VS Code extension (`sasjs/sasjs-for-vscode`, published on Open VSX) | Problems panel (ctrl+shift+M), Format Document, format-on-save | Config precedence: project `.sasjslint` > setting `sasjs-for-vscode.lintConfig` > `~/.sasjslint` > defaults |
| SASjs Server Studio | `POST /SASjsApi/code/lint` and `POST /SASjsApi/code/format`, body `{ code, filePath }` | Rules come from the nearest `.sasjslint` at or above the file's folder on the SASjs Drive, walking up to the drive root. A drive-root `.sasjslint` is seeded on first start and shows in the file tree as `/.sasjslint` |
| Library | `lintText`, `lintFile`, `formatText`, `formatFile`, and the folder/project variants | See the API section below |

All four call the same rules. The CLI, extension and server each pin a version of `@sasjs/lint`, so a rule added to the library only appears in a surface once that surface bumps its dependency - check the pinned version before telling a user a rule should fire in their editor.

## Config resolution

When no configuration is passed in, the library resolves it in this order:

1. `.sasjslint` at the project root (the library walks up to find the project)
2. `.sasjslint` in the user's home directory
3. `DefaultLintConfiguration` - the built-in defaults

A setting that is absent takes its default, and so does a project with no `.sasjslint` at all. `DefaultLintConfiguration` is exported from `@sasjs/lint/utils/getLintConfig`, and it is what `sasjs lint init` writes out.

## The .sasjslint file

```json
{
  "noTrailingSpaces": true,
  "maxLineLength": 100,
  "noSingleAsteriskComments": true,
  "severityLevel": {
    "hasDoxygenHeader": "warn",
    "noEncodedPasswords": "error"
  }
}
```

## Rules and defaults

Two groups, and the way you switch a rule off depends on which group it is in.

**On by default - switch off with `false`** (except where noted):

| Setting | Default | Severity | What it checks |
|---|---|---|---|
| `hasDoxygenHeader` | true | WARNING | the file begins with a `/**` Doxygen header |
| `hasMacroNameInMend` | true | WARNING | `%mend` carries the macro name |
| `hasMacroParentheses` | true | WARNING | macros are defined with parentheses, and no space before the `(` |
| `noNestedMacros` | true | WARNING | no `%macro` defined inside another macro |
| `strictMacroDefinition` | true | WARNING | no space in a parameter name (`%macro m(my var);`), no unrecognised option (`%macro m()/nonsense;`) |
| `noUndeclaredMacros` | true | WARNING | every macro a file calls is declared in the file or its header |
| `noUnusedMacros` | true | WARNING | every macro in `<h4> SAS Macros </h4>` is actually called |
| `noTrailingSpaces` | true | WARNING | no line ends in whitespace |
| `noTabs` | true | WARNING | no tab characters. Alias: `noTabIndentation` (deprecated) |
| `noGremlins` | true | WARNING | no zero-width or otherwise non-standard characters |
| `indentationMultiple` | 2 | WARNING | leading spaces divide cleanly by this number |
| `lowerCaseFileNames` | true | WARNING | filenames are lowercase (autocall on `*nix` requires it) |
| `noSpacesInFileNames` | true | WARNING | filenames contain no spaces |
| `noEncodedPasswords` | true | ERROR | no `{sas00X}` or `{sasenc}` encoded password |
| `maxLineLength` | 80 | WARNING | line length. Off with `0` |

**Off by default - switch on with `true`**:

| Setting | Default | Severity | What it checks |
|---|---|---|---|
| `noSingleAsteriskComments` | false | WARNING | comment statements of the form `* text;` |
| `noUnusedLibnames` | false | WARNING | a libref the file assigns and never uses |
| `hasRequiredMacroOptions` | false | WARNING | macros carry the options in `requiredMacroOptions` |
| `lineEndings` | `"off"` | WARNING | line endings conform to `lf` or `crlf` |

**Supporting settings** (not rules):

| Setting | Default | Purpose |
|---|---|---|
| `ignoreList` | `[]` | paths to skip. Files in `.gitignore` are skipped too |
| `allowedGremlins` | `[]` | 4-hex-digit strings such as `"0x0080"` |
| `defaultHeader` | see below | header template applied to a file with no `/**` header |
| `severityLevel` | `{}` | per-rule override of `"warn"` / `"error"` |
| `maxHeaderLineLength` | 80 | line limit inside the header |
| `maxDataLineLength` | 80 | line limit inside `datalines` / `cards` / `parmcards` records |
| `requiredMacroOptions` | `[]` | options required by `hasRequiredMacroOptions` |
| `ignoredLibnames` | `[]` | librefs `noUnusedLibnames` leaves alone |

## Severity and exit codes

Every rule has three states: off, WARNING, or ERROR. `sasjs lint` returns a non-zero exit code **only when an ERROR is reported** - warnings leave the exit code at 0, so a hook or pipeline keyed on the exit code passes a file that only warns. `noEncodedPasswords` is the only rule that ships as ERROR.

`severityLevel` promotes or demotes a rule by name, and accepts only `"warn"` and `"error"`; any other value is ignored without complaint:

```json
{
  "severityLevel": {
    "maxLineLength": "error",
    "hasDoxygenHeader": "warn"
  }
}
```

## Per-file overrides

A file adjusts the rules that apply to itself with a `@sasjslint` block in its Doxygen header:

```sas
/**
  @file
  @brief Calls the settlement API

  @sasjslint {"maxHeaderLineLength": 200, "noUndeclaredMacros": false}

  <h4> SAS Macros </h4>
  @li mf_trim.sas

**/
```

- Scalars replace, arrays are additive (`allowedGremlins`, `requiredMacroOptions`, `ignoredLibnames` gain entries rather than replacing), objects merge key by key (`severityLevel`).
- The override applies to the formatter as well, so `sasjs lint fix` honours it - a file that switches `noUnusedMacros` off keeps the header entries it would otherwise lose.
- Only the header is read, and only a line that starts with the tag followed immediately by `{`. A malformed or unterminated block is ignored rather than raised.
- The header wins over the configuration the caller passes.
- `ignoreList` is the one setting a header cannot use: it is evaluated before the file is read.
- Place the block **outside** the `<h4> SAS Macros </h4>` section, which the formatter rewrites.

## The formatter

The formatter applies the fixable rules on save. Implemented today:

- add the macro name to `%mend`
- add a Doxygen header template when the file has none
- add macros a file uses to `<h4> SAS Macros </h4>`, de-duplicated and sorted
- remove macros from that section that the file does not use
- remove trailing spaces

Not implemented (do not promise these): tabs to spaces, gremlin removal, line-ending correction, converting single-asterisk comments to block comments.

`defaultHeader` uses `{lineEnding}` as the newline placeholder - a literal `\n` does not work:

```json
{
  "defaultHeader": "/**{lineEnding}  @file{lineEnding}  @brief Our Company Brief{lineEnding}**/"
}
```

## Library API

```ts
import { lintText, lintFile, formatText, formatFile, LintConfig, Severity } from '@sasjs/lint'

const diagnostics = await lintText(code, config)   // config optional
const fixed = await formatText(code, config)       // config optional
```

- `lintText(text, configuration?)`, `lintFile(path, configuration?)`, `lintFolder`, `lintProject`
- `formatText(text, configuration?)`, `formatFile`, `formatFolder`, `formatProject`
- `new LintConfig(json)` builds a config from a plain object; `config.override(json)` returns a new config with an override merged in
- `Diagnostic` carries `message`, `lineNumber`, `startColumnNumber`, `endColumnNumber` and `severity`
- `Severity` is `Info` (0), `Warning` (1), `Error` (2)

Passing an explicit `LintConfig` matters when the caller knows the rules - a server or editor linting a buffer with no path on disk cannot rely on the working-directory walk.

## Pitfalls

- **Off means something different per rule.** The on-by-default rules switch off with `false`; `maxLineLength` switches off with `0`; `lineEndings` switches off with `"off"`; the off-by-default rules ignore `false` (it is the same as leaving them out) and need `true`. Getting this wrong is the most common reason a rule "does not work".
- **`maxHeaderLineLength` and `maxDataLineLength` are inert when `maxLineLength` is off**, because they are scoped to it. The effective limit is the *higher* of the two values, so setting one lower than `maxLineLength` is silently ignored.
- **`noUnusedMacros` plus the formatter removes `@li` dependencies.** Those entries are consumed by the compiler, so a macro referenced only indirectly - through a dynamic `%&name` call, or supplied by an `%include`d program - loses its declaration and the job can fail to assemble. Switch the rule off for the project or the file when that applies.
- **`noUndeclaredMacros` does not see `SASAUTOS`.** Macros that ship with SAS are always treated as declared (the list is generated from `@sasjs/sas-language`), but macros made available through `SASAUTOS` are invisible to the linter and are reported. Declare them in the header or switch the rule off.
- **`noUnusedLibnames` is deliberately generous.** A libref counts as used if it appears anywhere outside a `LIBNAME` statement - including inside a double-quoted string, as in `pathname("outData", "L")`. It is off by default because a file is not a complete job, and it has no formatter fix.
- **An empty `.sasjslint` is not the same as no `.sasjslint`** only for settings whose default was previously applied conditionally. Since 4.0.0 an absent `maxLineLength` or `hasMacroNameInMend` falls back to its documented default (80, and `true`), so a project that relied on omitting them to disable those rules must now set `"maxLineLength": 0` or `"hasMacroNameInMend": false`.
- **`allowedGremlins` entries are strings, not numbers**: `"0x0080"`, exactly four hex digits.
- **The CLI output is a box-drawn table.** It is meant for a terminal; do not paste it into a plain-text or ASCII-only document without expecting the border glyphs to be a problem.
- **`sasjs lint` with no subcommand behaves as `sasjs lint find`**, linting every `.sas` file in the project.

## Verification

- Confirm a rule fires: put the offending construct in a `.sas` file and run `terminal(command="npx sasjs lint")`. A hit prints a row with the message and a `[line, column]` position; no row means the rule is off or the construct is excluded (check the config first, then the rule's exclusions).
- Confirm a config change took effect: run `npx sasjs lint` before and after editing `.sasjslint`, and compare the rows. A rule that is off by default needs `true`, not `false`.
- Confirm the formatter's effect: run `npx sasjs lint fix` and inspect the diff - the `<h4> SAS Macros </h4>` section and `%mend` lines are the ones it rewrites.
- Confirm a per-file override: add the `@sasjslint` block, run `sasjs lint`, and check that the rule it switches off no longer reports for that file while still reporting for its neighbours.
