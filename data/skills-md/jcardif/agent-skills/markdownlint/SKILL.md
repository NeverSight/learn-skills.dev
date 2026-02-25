---
name: markdownlint
description: Ensures style consistency and correctness in Markdown files using markdownlint-cli2. Use whenever creating, updating, editing, or reviewing any Markdown (.md) file. Triggers on any task that creates or modifies .md files, including README.md, CHANGELOG.md, documentation, or any file with a .md extension. Also triggers when the user mentions markdown, linting, markdown formatting, markdown style, or markdownlint. Always run the linter after writing or editing markdown content — do not skip this step.
---

# Markdownlint

Lint Markdown files for style and consistency
using [markdownlint][ml] via the `markdownlint-cli2` CLI.

[ml]: https://github.com/DavidAnson/markdownlint

## Running the linter

Lint specific files or directories:

```bash
npx markdownlint-cli2 "docs/**/*.md"
```

Lint and auto-fix fixable issues:

```bash
npx markdownlint-cli2 --fix "docs/**/*.md"
```

Lint multiple paths:

```bash
npx markdownlint-cli2 "docs/**/*.md" "README.md" "CHANGELOG.md"
```

Exclude paths with `#` (negation):

```bash
npx markdownlint-cli2 "**/*.md" "#node_modules"
```

### Exit codes

- `0`: No errors (warnings may exist)
- `1`: Linting errors found
- `2`: Linting failed (e.g., bad config)

## Interpreting output

Output format: `filepath:line rule/alias description`

Example:

```text
docs/guide.md:15 MD022/blanks-around-headings [Expected: 1; Actual: 0; Below]
docs/guide.md:42 MD034/no-bare-urls Bare URL used [Context: "..."]
```

## Configuration

### Project config file `.markdownlint.json`

```json
{
  "default": true,
  "MD013": false,
  "MD033": { "allowed_elements": ["details", "summary", "br"] },
  "MD024": { "siblings_only": true }
}
```

Rules can be set to:

- `true` or `"error"` — enable as error
- `"warning"` — enable as warning
- `false` — disable
- `{ ... }` — enable with parameters

### CLI config file `.markdownlint-cli2.jsonc`

Controls both rules and CLI behavior:

```jsonc
{
  "config": {
    "default": true,
    "MD013": false
  },
  "globs": ["**/*.md"],
  "ignores": ["node_modules/**", "build/**"],
  "fix": false
}
```

### Configuration precedence

1. `.markdownlint-cli2.jsonc` / `.markdownlint-cli2.yaml` (full CLI config)
2. `.markdownlint.jsonc` / `.markdownlint.json` / `.markdownlint.yaml` (rules only)
3. Inline HTML comment directives in the file itself

## Inline directives

Control rules within a file using HTML comments:

```markdown
<!-- markdownlint-disable MD013 -->
This long line won't trigger a warning because MD013 is disabled for this section of the file.
<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable-line MD034 -->
https://bare-url-allowed-on-this-line.com

<!-- markdownlint-disable-next-line MD041 -->
Not a heading on line 1

<!-- markdownlint-configure-file { "MD013": { "line_length": 120 } } -->
```

State capture/restore:

```markdown
<!-- markdownlint-capture -->
<!-- markdownlint-disable MD013 -->
Long content here...
<!-- markdownlint-restore -->
```

## Common rules quick reference

| Rule | Alias | What it checks | Fixable |
| --- | --- | --- | --- |
| MD001 | heading-increment | Heading levels increment by one | No |
| MD003 | heading-style | Consistent heading style (atx vs setext) | No |
| MD004 | ul-style | Consistent unordered list markers | Yes |
| MD005 | list-indent | Consistent list indentation | Yes |
| MD007 | ul-indent | Unordered list indentation depth | Yes |
| MD009 | no-trailing-spaces | No trailing whitespace | Yes |
| MD010 | no-hard-tabs | No hard tab characters | Yes |
| MD012 | no-multiple-blanks | No consecutive blank lines | Yes |
| MD013 | line-length | Line length limit (default 80) | No |
| MD022 | blanks-around-headings | Blank lines around headings | Yes |
| MD023 | heading-start-left | Headings must start at line beginning | Yes |
| MD025 | single-h1 | Only one top-level heading per file | No |
| MD031 | blanks-around-fences | Blank lines around fenced code blocks | Yes |
| MD032 | blanks-around-lists | Blank lines around lists | Yes |
| MD033 | no-inline-html | No inline HTML | No |
| MD034 | no-bare-urls | No bare URLs | No |
| MD040 | fenced-code-language | Fenced code blocks need a language | No |
| MD041 | first-line-h1 | First line should be a top-level heading | No |
| MD047 | single-trailing-newline | Files end with a single newline | Yes |

For a complete reference of all 47 rules with parameters, see [references/rules.md](./references/rules.md).

## Workflow

When creating or editing markdown files:

1. Write or edit the markdown content
2. Run the linter: `npx markdownlint-cli2 "path/to/file.md"`
3. If errors are found:
   - Try auto-fix first: `npx markdownlint-cli2 --fix "path/to/file.md"`
   - Manually fix any remaining non-fixable issues
   - Re-run the linter to confirm zero errors
4. If a rule should be permanently disabled, update `.markdownlint.json`
5. For one-off exceptions, use inline directives

## Tips

- Run `--fix` before manual fixes to save effort — about half the rules are auto-fixable
- Use rule aliases (e.g., `no-trailing-spaces`) instead of codes (e.g., `MD009`) in inline directives for readability
- The `MD013` line-length rule is commonly disabled in projects (this project disables it in `.markdownlint.json`)
- Use `<!-- markdownlint-disable-next-line -->` for single-line exceptions rather than disable/enable blocks
- Configuration in `.markdownlint.json` applies to the directory and all subdirectories
