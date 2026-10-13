---
name: write-pr
description: >
  Write a concise GitHub pull request body with five headings. The headings
  are Background, Design Decisions, Changes, Verification Performed, and
  Post-Merge Operations. When you create, open, submit, or update a pull
  request, use this skill. Use it for a PR description or for gh pr create.
  Do not use this skill for commit messages alone.
metadata:
  version: "1.0.0"
  internal: true
---

# Write a Pull Request

Fill `PULL_REQUEST_TEMPLATE.md`. Write in Simple English. Keep the body short.

## When this skill applies

When you create, open, submit, or update a pull request, use this skill.
Use it for `gh pr create`, GitHub MCP `create_pull_request`, and body edits.
Do not use a different heading set. Do not add a Summary or a Test Plan.

## Before you write

1. Read the full diff against the base branch.
2. Read the commit subjects on this branch.
3. If linked issues or design docs add facts the diff does not show, read them.

## Hard limits

Use only these headings, in this order:

1. Background
2. Design Decisions
3. Changes
4. Verification Performed
5. Post-Merge Operations

Keep the whole body under 250 words.
If a heading has no content, write `None.` under it.
Do not add a sixth heading.
Do not leave HTML comments in the submitted body.
Do not add a "Made with" or "Generated with" footer.

## Simple English

Apply the `simple-english` skill in pragmatic mode.
If that skill is not in context, apply these rules:

- Descriptive text uses simple present or simple past.
- Descriptive sentences stay under 25 words.
- `Post-Merge Operations` is a procedure. Use the imperative.
- Procedural sentences stay under 20 words.
- One instruction per sentence.
- Put `If` and `When` at the start of the sentence.
- Use only the modals `can`, `will`, and `must`.
- Do not use `should`, `would`, `may`, `might`, or `could`.
- Do not use contractions or semicolons.
- Do not use `e.g.`, `i.e.`, or `etc.`
- Pick one name per thing and keep it.
- Delete filler that adds no fact.

Then run the simple-english self-check on the draft.

## Section rules

### Background (descriptive)

State why the change exists.
Name the problem, the constraint, or the linked issue.
Use two to four sentences.
Put GitHub close keywords on their own line, for example `Closes #123`.
Do not restate the diff.

### Design Decisions (descriptive)

State only the choices a reviewer cannot infer from the diff.
Use a short bullet list.
If you made no such choice, write `None.`
Do not narrate the design history.

### Changes (descriptive)

State what landed, at component level.
Bold the component. Then write one short clause.
Do not list files. Do not paste commit messages.
Three to seven bullets is enough.

### Verification Performed (descriptive, simple past)

State what you ran and the result.
Name the command and the outcome.
If you did not run the test suite, say that.
Do not write an unchecked future checklist.
Do not invent runs.

### Post-Merge Operations (procedural)

State the steps a human must do after merge.
Put a required condition before the command.
If no step is required, write `None.`
Do not tell the reader to merge the pull request.

## Title

Write a conventional title of the form type-colon-what.
Keep the title under 72 characters.
Use the imperative: `Add`, `Fix`, `Pin`, `Remove`.

## How to submit

Write the body to a file. Then pass that file to the create command.
Do not rely on GitHub to fill the template. Your `--body` replaces it.

## Example

**Before:** extra headings, a future checklist, and a generator footer.

**After:**

```markdown
## Background

`codeql.yml` and `dependency-review.yml` did not take the `enabled:` input.
The other PR-time gates already have that input.
A docs-only pull request still ran a full CodeQL job.

This change unblocks lane targeting in `lvlup-sw/hierophant`.
Tracking: lvlup-sw/.github#38.

## Design Decisions

- Add `enabled:` in the same shape as the other four gates.
- Use `if: ${{ inputs.enabled != false }}` so a bad value still runs the job.
- Leave `update-baseline` unchanged. Consumers call it only on the default branch.

## Changes

- **`dependency-review.yml` and `codeql.yml`** — accept `enabled:` (default `true`).
- **`canary-enabled-input.yml`** — cover both new callers.
- **Consumer guide** — name which reusables accept the input.

## Verification Performed

- `actionlint` was clean on the three changed workflows.
- `pytest actions/ci-lanes/tests` — 39 passed, 164 subtests.
- The canary asserts that a skipped inner job still reports the two-part check name.

## Post-Merge Operations

None.
```

## Anti-patterns

- Do not add extra headings such as Summary, Test Plan, Checklist, Docs, Proof, or Related Issues.
- Do not add a bullet for every file.
- Do not repeat the same fact in two sections.
- Do not name classes and methods that the diff already shows.
- Do not write unchecked boxes for work you plan to do later.
- Do not add ritual `N/A` checklists.
- Do not narrate the work phase by phase.
