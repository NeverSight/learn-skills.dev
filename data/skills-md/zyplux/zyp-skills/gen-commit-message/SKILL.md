---
name: gen-commit-message
description: >
  Draft a commit message for the current project by inspecting git state
  (status, staged diff, recent log) and emitting a message that follows the
  Conventional Commits v1.0.0 specification. Use this whenever the user runs
  /gen-commit-message, asks for a commit message or PR title, or is about to
  commit and has not written one. Produce only the message — do not run
  `git commit` or stage files.
metadata:
  kind: prompt
  version: "0.1.2"
  user-invocable: "true"
---

# gen-commit-message — Conventional Commits message for current changes

Invoked as the slash command `/gen-commit-message` (no arguments). This is a
prompt-driven skill with no CLI binary: read the git state directly with Bash
and produce a message that conforms to the Conventional Commits v1.0.0 spec
bundled at `references/conventional-commits-v1.0.0.md`.

## When to use

- User runs `/gen-commit-message`.
- User asks "what should this commit say", "draft a commit message", or
  wants a PR title for the current branch.
- User is about to commit and has not supplied a message.

Do **not** auto-commit, auto-stage, push, or amend. The skill only drafts
the message — the user decides when and how to commit.

## Workflow

1. **Read git state in parallel.** Three commands together:
   - `git status --porcelain=v1` — what's modified/staged/untracked
   - `git diff --cached` — the staged changes (source of truth for the message)
   - `git log -n 10 --pretty=format:'%h %s'` — recent commits, to match
     prevailing type/scope conventions in this repo

   If `git diff --cached` is empty, fall back to `git diff` (unstaged
   working-tree changes). If both are empty and there are no untracked
   files, say "nothing to commit" and stop.

2. **Pick the scope.** Look at which area the change touches and match the
   recent log's style. In repos that scope by component (e.g. `feat(h2md):`,
   `fix(peek):`), use the component name. Omit the scope when the change
   spans many areas or touches project-wide tooling, rather than inventing
   `repo` or `misc`.

3. **Pick the type.** Consult `references/conventional-commits-v1.0.0.md`
   for the authoritative rules. Quick guide:

   | Type | Use when |
   |------|----------|
   | `feat` | A new feature — user-visible capability |
   | `fix` | A bug fix |
   | `docs` | Documentation-only change |
   | `refactor` | Code change that is neither a feature nor a fix |
   | `test` | Tests only, no production code change |
   | `perf` | Performance improvement |
   | `build` | Build system / dependency changes |
   | `ci` | CI configuration |
   | `chore` | Housekeeping / tooling with no src or test impact |
   | `style` | Formatting, whitespace, no behavior change |
   | `revert` | Revert of a previous commit |

   If the change is incompatible with prior behavior, mark it breaking by
   adding `!` before the colon **and** (optionally) a `BREAKING CHANGE:`
   footer that explains the migration.

4. **Write the description.** One line, imperative mood, lowercase start,
   no trailing period, aim for ≤72 characters. Describe *what* changed.
   Prefer concrete verbs (`add`, `remove`, `rename`, `inline`, `expose`)
   over vague ones (`update`, `improve`, `tweak`).

5. **Body (optional).** Add a body only when the subject cannot carry the
   full picture — for example when multiple related changes need to be
   tied together, or when the rationale is non-obvious. Separate from the
   subject by one blank line. Wrap around 72 characters. Explain *why*,
   not *what* (the diff shows what).

6. **Footers (optional).** One blank line after the body. Use git trailer
   format: `Token: value`, with `-` in place of spaces inside the token.
   Common footers: `Refs: #123`, `Closes: #456`, `Reviewed-by: Name`,
   `BREAKING CHANGE: <migration note>`.

7. **Emit the message.** Print the draft inside a fenced code block so the
   user can copy it verbatim. If multiple reasonable messages exist (e.g.
   the staged changes bundle unrelated work), print the best single
   message and note briefly that the user may want to split the commit.

## Output shape

Always return the draft wrapped in a fenced block using the `text`
language tag so it renders cleanly and is easy to copy:

````text
<type>[(scope)][!]: <description>

<optional body paragraph(s)>

<optional footer(s)>
````

## Examples

Given staged changes that add a new `--copy-to` flag to the `h2md` skill:

````text
feat(h2md): add --copy-to flag for writing article.md to an external path
````

Given a staged diff that fixes a crash when a parquet file has zero rows:

````text
fix(peek): handle empty parquet files in describe mode

Previously `peek -d` raised ZeroDivisionError when computing per-column
stats on an empty file. Short-circuit to a zero-row describe result.

Refs: #42
````

Given a change that renames a public CLI flag, breaking existing callers:

````text
feat(suggest)!: rename --dir flag to --out

BREAKING CHANGE: `suggest --dir` is removed. Use `--out <path>` instead,
or set the SKILL_SUGGEST_DIR env var.
````

## Notes

- **Match the repo's voice.** Scan `git log` output for the project's
  prevailing style (scope granularity, tense, sentence length) and match
  it. Consistency is more valuable than rigid rule-following.
- **Don't pad.** A one-line subject is correct for most commits. Bodies
  and footers exist when they add information — omit them otherwise.
- **Don't claim credit.** Do not add `Co-Authored-By` or agent-attribution
  footers unless the user explicitly asks for them.
