---
name: i18n-validate
description: "Use when checking translation/locale files for consistency — missing keys, extra keys, placeholder mismatches, malformed or CLDR-incomplete plurals, parse errors, empty or untranslated values — across 32 file formats. Also use in CI (JUnit/JSON output, meaningful exit codes). Wraps the i18n-validate CLI."
---

# i18n-validate: translation file consistency checker

Validates a locales directory (or single file) against a reference language.
Zero-config: auto-detects layout, formats, and languages.

## Setup check

```bash
command -v i18n-validate || npm install -g @i18n-agent/i18n-validate
```

## Usage

```bash
i18n-validate [OPTIONS] <path-to-locales-dir-or-file>
```

| Flag | Meaning | Default |
|------|---------|---------|
| `--ref <LANG>` | Reference language | `en` |
| `--expect <LANGS>` | Expected languages (comma-separated) | auto-discover |
| `--layout <TYPE>` | `flat`, `directory`, `single-file` | auto-detect |
| `--include` / `--exclude <PATTERN>` | Glob filters (repeatable) | all / none |
| `--format <FORMAT>` | `terminal`, `json`, `junit` | `terminal` |
| `-o, --output <FILE>` | Write report to file | stdout |
| `--strict` | Warnings count as errors | off |
| `--no-warnings` | Suppress warnings | off |
| `--skip <CHECKS>` | Skip named checks | none |
| `--quiet` | Exit code only | off |
| `--config <PATH>` | Config file | auto-detect |

**Checks** — errors: `missing-languages`, `orphaned-languages`, `missing-keys`,
`extra-keys`, `placeholders`, `plural-structure`, `plural-requirements`,
`parse-errors`. Warnings: `empty-values`, `untranslated`.

**Exit codes**: `0` pass · `1` errors (or warnings with `--strict`) · `2` bad args/config.

## Examples

```bash
i18n-validate ./locales                                    # zero-config
i18n-validate ./locales --format junit -o i18n-report.xml --strict   # CI
i18n-validate ./locales --format json                      # for scripting
i18n-validate ./locales --skip untranslated,empty-values   # onboarding a new language
```

## Agent guidance

- Run after ANY edit to locale files — it's the cheapest regression gate.
- Use `--format json` when you need to parse findings and fix them
  programmatically; fix `missing-keys` and `placeholders` errors first.
- In CI, prefer `--strict --format junit -o report.xml` so warnings fail the
  build and reporters render the results.
