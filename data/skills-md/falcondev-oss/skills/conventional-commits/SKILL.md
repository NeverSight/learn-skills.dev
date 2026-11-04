---
name: conventional-commits
description: Format commit messages, branch names, PR titles, and issue titles to the Conventional Commits 1.0.0 spec. Use BEFORE running `git commit`, `git checkout -b`/`git branch`, `gh pr create`, or `gh issue create`; before writing any commit message, branch name, PR title, or issue title; and whenever staging changes to commit or asked to "commit", "make a PR", "open an issue", or "create a branch" — or when another skill needs a spec-compliant commit message.
---

# Conventional Commits

Every commit, branch, PR, and issue you name follows the Conventional Commits 1.0.0 spec exactly. Two rules override anything else: each commit is **atomic** (one logical change), and you **verify** the message against the spec and the actual diff before it lands.

**Exception — keep tool-generated default messages.** Merges and similar auto-generated commits keep their default message (`Merge branch ...`, `Merge pull request ...`, `Revert ...`), never rewritten into a Conventional Commits subject. Many tools identify and filter these by their default prefix, so the prefix must stay intact.

## The format

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

**Types** — pick the one that matches what the diff _actually does_:

| type        | use for                                                         | SemVer |
| ----------- | --------------------------------------------------------------- | ------ |
| `feat`      | a new feature                                                   | MINOR  |
| `fix`       | a bug fix                                                       | PATCH  |
| `docs`      | documentation only                                              | —      |
| `style`     | whitespace, formatting, semicolons; never CSS or visual changes | —      |
| `refactor`  | code change that neither fixes a bug nor adds a feature         | —      |
| `perf`      | a performance improvement                                       | —      |
| `test`      | adding or correcting tests                                      | —      |
| `build`     | build system or dependencies                                    | —      |
| `ci`        | CI configuration                                                | —      |
| `chore`     | anything else with no production-code effect                    | —      |
| `wayfinder` | a wayfinder map ticket/issue                                    | —      |
| `spec`      | a spec (e.g. from a wayfinder map via `/to-spec`)               | —      |

CSS, Tailwind classes, and other visual changes are code, never `style`: use `feat` for a new look, `fix` for a visual bug, and `refactor` for restructured styles with no visible change.

A wayfinder map ticket/issue is always `wayfinder`, and a spec is always `spec` — the artifact decides the type, overriding what the change itself does (`feat`, `fix`, etc.).

**Subject-line rules:**

- `type` is required, lowercase, from the table above.
- `scope` is optional: a noun in parentheses naming the affected section — `fix(parser):`.
- `!` immediately before the colon marks a breaking change (MAJOR) — `feat(api)!:`.
- Exactly one colon and one space, then the description.
- `description`: a concise, imperative summary on the same line as the type, **led by substance**. The type already carries the verb, so cut any leading verb that only echoes it (`feat: add…`, `fix: fix…`) or fills space (`give…`, `make…`, `update…`); keep a verb only when it names _how_ the change happens in a way the type can't (`refactor(auth): extract token parser`).
  - `feat(time-tracking): add shift-derived automatic blocking` → `feat(time-tracking): shift-derived automatic blocking`
  - `refactor(seeder): give duty-plan departments unique shifts` → `refactor(seeder): unique shifts per duty-plan department`

**Body & footers** (only when the change needs them):

- Body: one blank line after the description, then free-form paragraphs.
- Footers: one blank line after the body. Each footer is `Token: value` or `Token #value`. The token replaces spaces with `-` (e.g. `Reviewed-by`, `Refs`), **except** `BREAKING CHANGE`.
- Breaking change: either `!` in the prefix, or a footer `BREAKING CHANGE: <description>` — the token must be uppercase (`BREAKING-CHANGE` is synonymous).

**Language:**

- Always use american english.

## Common presets

Reach for these exact messages when the diff matches — they keep recurring commits consistent:

- **`style: lint`** — the commit contains _only_ linting/formatting changes (no change to code meaning).
- **`build(deps): upgrade deps`** — a broad dependency update touching multiple packages.
- **`build(deps): upgrade <package>`** — a dependency update scoped to one package, e.g. `build(deps): upgrade vitest`.

A preset applies only when the staged diff is genuinely just that change; if anything else is bundled in, split it out (see step 2 below) rather than stretching the preset.

## Making a commit

1. **Survey the whole diff.** Run `git status` and `git diff` (staged and unstaged). Understand every hunk before writing anything.

2. **Split into atomic commits.** Group the hunks so each planned commit is a _single_ type + scope + intent. A diff that mixes features, fixes, refactors, or unrelated scopes is **not** atomic — plan one commit per unit. Done when every hunk is assigned to exactly one planned commit and each planned commit is one type/scope/intent.

3. **Stage and draft, one commit at a time.** Stage only that commit's hunks (`git add <paths>`, or `git add -p` for partial files), then draft its message in the format above.

4. **Verify** (below) before committing. Do not run `git commit` until every check passes.

5. **Commit** with the verified message, then return to step 3 for the next planned commit.

## Verify

The feedback run. Re-read the drafted message against both the spec and the _staged_ diff. Every item must pass; if one fails, revise the message (or re-split the commit) and run the checklist again.

- **Format**: matches `<type>[scope][!]: <description>` — lowercase type from the table, one colon + one space.
- **Type matches reality**: the type describes what the staged diff does — not `feat` for a refactor, not `fix` for a new capability, not `style` for CSS or UI changes.
- **Atomic**: the staged diff is one logical change; nothing unrelated is bundled in.
- **Description**: imperative, concise, true to the change, and led by substance — no leading verb that merely echoes the type or fills space.
- **Body/footers** (if any): blank-line separated; footer tokens well-formed; any breaking change flagged with `!` or an uppercase `BREAKING CHANGE:` footer.
- **Authorship**: the attribution footer is exactly the one the Authorship section below asks for, and nothing follows it.

## Branches, PRs, and issues

The same `type` vocabulary and the subject-line rules apply, and each is verified the same way:

- **Branch**: `<type>/<kebab-case-summary>` — `feat/user-export`, `fix/parser-crash`.
- **PR title**: an exact Conventional Commits subject line (`<type>[scope][!]: <description>`), because it becomes the squash-merge commit.
- **Issue title**: `<type>[scope]: <description>` naming the desired change or the bug.

## Authorship

Add exactly the attribution footer the harness or user instructions specify.

### Commit-message formatting

When committing from a shell, pass each paragraph as a separate `-m` argument. Ordinary quoted `\n` remains literal text.

```sh
git commit \
  -m 'type(scope): summary' \
  -m 'Body paragraph.' \
  -m 'Closes #123'
```

For exact formatting, use `git commit -F <message-file>` with real line breaks.

Before pushing, verify:

```sh
git show -s --format=%B HEAD | sed -n l
```

Completion criterion: every intended line appears separately, with no literal `\n`.
