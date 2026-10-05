---
name: suggest
description: >
  Submit structured improvement suggestions for CLI skills — bugs, missing features, inefficiencies, or token waste.
  BLOCKING REQUIREMENT: When you write a workaround for a skill limitation (python one-liner, extra parsing, manual post-processing),
  you MUST submit a /suggest IMMEDIATELY — before continuing the task. Do not batch suggestions for later.
metadata:
  kind: cli
  version: "0.5.0"
  user-invocable: "true"
  argument-hint: <skill-name> [<markdown-text> | -]
---

# suggest — skill improvement suggestions

`suggest` is a standalone CLI on PATH. Invoke via Bash: `Bash(suggest peek "# title ...")`

Skills evolve through use. When a skill falls short — wrong output, missing mode, wasteful tokens, clunky interface — submit a suggestion so it gets better.

## When to suggest

- **You wrote a workaround** — a `python -c` one-liner, extra parsing, post-processing that the skill should have handled
- **Output was wasteful** — verbose, redundant, or burns tokens without adding information
- **Interface friction** — flags that could be merged, wrong defaults for the common case, unnecessary ceremony
- **A skill errored or gave wrong results** on valid input
- **A skill you needed doesn't exist** — and the use case is common enough to justify one

Skip suggestions for user errors or things outside the skill's scope.

## Suggestion format

Each suggestion is a markdown file. Use `#` (h1) for the title and `##` (h2) for sections — standard markdown hierarchy. Be concrete; vague suggestions are noise.

```markdown
# <Short descriptive title of the issue>

## Context
What were you doing when you hit this?

## Gap
What did you try, what happened, what should have happened? Include the command and output.

## Responsibility
Why should the skill handle this, not the caller? If you wrote a workaround, include it — it proves the need.

## Suggestion
What should change? A new flag, different default, leaner output format?

## Impact
One line: how does this fix improve the workflow?
```

## Usage

```text
suggest <skill-name> "<markdown text>"           # inline text
suggest <skill-name> -                           # read from stdin
```

When the suggestion is long or contains complex markdown with backticks/quotes, prefer stdin to avoid shell quoting issues.

## Example

```bash
suggest peek "# peek -c output is too verbose for multi-file scans

## Context
Scanning 12 parquet files to find which ones contain a 'user_id' column.

## Gap
\`peek data/*.parquet -c\` prints full schema for every file. I only needed column names, but got types and row counts too — ~60 lines of output when 12 would do.

## Responsibility
Schema scanning across many files is a core peek use case. The caller shouldn't need to pipe through grep to get a compact answer.

## Suggestion
Add a \`--names-only\` modifier for \`-c\` that prints just column names, one file per line. Or: make \`-c\` output more compact by default and add \`-cv\` for the verbose version.

## Impact
Cuts token usage ~5x for multi-file schema scans — the most common first step when exploring a new dataset directory."
```

## Configuration

Set the `SKILL_SUGGEST_DIR` environment variable to change where suggestions are saved. Defaults to `~/Documents/skill-suggestions/`. The installer (`just i suggest`) auto-configures this from [skills/suggest/env.toml](env.toml).

## Output

```text
saved: $SKILL_SUGGEST_DIR/peek/suggestion_20260403_141523_012345.md
```
