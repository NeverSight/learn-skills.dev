---
name: hrt-mr-brief
description: "Writes mr-brief.md for tempa-spec's apply phase: a three-section brief (Summary, Evidence, Merge Danger) that helps a reviewer understand an implemented change, written so its content can be pasted as a merge/pull request comment after the user commits. Built from the change's own artifacts and real test runs, never invented. Adapted from mattpocock/skills `pr`, itself credited to Dex Horthy's `show-me`. Use at the end of the tempa-spec `apply` phase, after the review loop."
---

# hrt-mr-brief

Adapted from the `pr` skill in `mattpocock/skills` (MIT), which credits Dex Horthy's `show-me` skill (humanlayer). The three-section shape is theirs. What changes here: the output is a file in the change directory, not a PR body, and every section is sourced from this change's artifacts instead of the agent's memory.

## Why this exists

A reviewer of a merge request sees the diff. The reasoning behind it lives in `proposal.md`, `design.md`, `align.md`, and `specs/**/*.md`, which the reviewer may never open. `mr-brief.md` is the one file that tells the reviewer what changed, proves it works, and says what it costs to be wrong.

This skill only writes the file. The user commits it with the code and posts its content wherever their review happens. The skill never posts anything and never runs git.

## When to run

Once, at the end of `apply`, after `hrt-apply-code-review` has finished. Write `mr-brief.md` next to `tasks.md` in the change directory. If it already exists, rewrite it from the current state, do not append. Write the final version once, before the user commits, and tell the user to include the file in that commit.

If the review loop ended with unresolved HIGH findings (RELEASE BLOCKER), still write the file. The blocker goes first under Merge Danger, stated plainly.

## Inputs

Read only these. Anything you cannot find in them, you do not write.

- `tasks.md`, `specs/**/*.md`, `design.md` (Shape / Seams, Decisions, Risks / Trade-offs).
- `align.md`, only the decision entries that changed behaviour.
- The diff of the working tree.
- Test output: the RED output `apply` Phase 1 wrote to `red-log.md` (next to `tasks.md`), and a fresh run of the suite now.
- The floor-guard flags the user approved in `hrt-apply-code-review` (rule, file, the user's reason).

## Output

Use this template. Keep the three headings as written. Write the prose under them in the language of `proposal.md`. Keep technical terms (test names, paths, identifiers) as they are.

```markdown
## Summary

<one visual, plus at most two sentences>

## Evidence

- **Before:** <failing test name and its failure line, from the Phase 1 RED run>
  **After:** <the same test passing, from a run now>

## Merge Danger

**Door:** <one-way or two-way>

<one or two sentences: why>

**Blast Radius:** <one word>

<one or two sentences: who or what breaks if this is wrong>

**Approved floor-guard flags:** <one line each: rule, file, reason; or "none">
```

### Summary

Pick the smallest view that makes the key point clear, and use one. Choose by what changed:

- Logic or an algorithm: pseudocode.
- Runtime control flow: a call tree.
- Components or modules: a shallow tree, with `diff` markers (`+`/`-`) when the shape already existed.
- Interaction between parts: a Mermaid `sequenceDiagram`.
- File or responsibility split: a shallow file tree.

Take the structure from `design.md`'s Shape / Seams section and the real diff. Name things with the terms the specs use. Do not draw anything the diff does not contain.

### Evidence

Show a before and after for the behaviour that matters most, not for every task. Pick the scenarios the specs treat as critical, plus any negative or `[security]` scenario.

- Execution evidence only: a test name with its real failure line, then the same test passing. Use the output you have. Do not retype it from memory.
- If the Phase 1 RED output is not in `red-log.md`, write `Before: not recorded` for that item. Never reconstruct a failure.
- Screenshots count as stronger evidence when the change is visual and the environment can take them. They cannot go into a text file, so name where the user should attach them. Do not fake one.
- Include the final result of the full suite on one line (pass count, fail count).
- Name the security scanners `apply` ran and their result in one line, or write `no scanner configured`. Never imply a scan happened that did not. If opengrep ran, give how many candidates it raised and how many were kept, and say that the bundled rules cover only Python, JavaScript/TypeScript, and Odoo. If the diff touched none of those files, write `opengrep not needed: no covered file changed`. A required scan that did not run never reaches this brief, because it blocks Phase 2.

### Merge Danger

**Door.** A two-way door can be walked back with a revert. A one-way door cannot. Mark one-way when the diff contains any of: a data migration or destructive schema change, deletion of stored data, a change to a published API or event contract, a config or flag removal that other code reads, or a step that has to be undone by hand. Otherwise two-way. Check the specs' `MODIFIED` and `REMOVED` deltas, since a breaking spec change is a contract change.

**Blast Radius.** One word (for example `module`, `consumers`, `data`, `tenant`, `release`), then one or two sentences on who or what breaks if the change is wrong. Draw this from `design.md` Risks / Trade-offs and the diff. If `design.md` lists a `[Threat] -> Mitigation` entry, say whether a passing test covers the mitigation. Do not contradict a failure-consequence statement already approved in the design. Say what the Blast Radius rests on (the suite result, a design Risk, or the diff alone). If it rests on the diff alone, write "not checked beyond the diff".

**Approved floor-guard flags.** Each suppression, skip, deleted test, assertion drop, or stub that the user approved during the review stays in the diff. List each one on one line: the rule, the file, and the user's reason, without the line text. Write `none` if there were none. A security suppression goes first.

## Rules

1. Facts only. Each claim traces to an artifact, the diff, or a test run in this session. A claim with no source is cut.
2. The brief is read once by a reviewer who may not have followed the work. Prose follows the `plain-language-writing` skill's ARTIFACT rules, with these changes: sentences stay short, one idea each, and nothing is named by a pronoun when two things could be meant.
3. The file ends up in a shared place. Keep out of it, including from pasted test output: tokens and keys, passwords, URLs with credentials, email addresses, phone numbers, and national identity numbers. Cut or mask them.
4. Never write `Closes`, `Fixes`, or `Resolves` (or variants) next to an issue reference, including inside pasted output. Posting it could close the issue early. Write "Related to #N" if a reference is needed.
5. Trackers run a comment line that starts with `/` as a command (for example `/label`, `/close`). Never start a line of prose with `/`. Paths and commands go inside code fences.
6. No relative links to files in the change directory. The reader may see a comment, not a file next to `design.md`. Name files by path as text.
7. Keep it short enough to read in a minute or two. If the Summary needs more than one visual, the change is probably too large to review as one unit, so say so under Blast Radius.
8. Never run `git commit`, `git push`, or any command that talks to the review system. The user does that.
