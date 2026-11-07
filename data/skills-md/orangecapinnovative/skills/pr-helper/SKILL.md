---
name: pr-helper
description: Open a new PR or update an open PR with a clear change log and description, in any repo. Follows the repo PR template, bumps semantic versions from the latest GitHub tags, and keeps backticks out of the body. Use whenever the user asks to open, create, update, or manage a pull request.
---

Use the `gh` CLI for GitHub operations. Use plain `git` for local history.

## 0. Preconditions

1. `gh --version` and `gh auth status` both succeed. Otherwise tell the user to install gh (`brew install gh` on macOS, https://cli.github.com elsewhere) and run `gh auth login`, then stop.
2. Current branch is not the default branch, and is pushed (`git push -u origin <branch>`). Ask before pushing commits the user has not reviewed.
3. Base branch is the repo default (`gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`). Use another base only when the user names it.

## 1. Pick mode

```bash
gh pr list --head <current-branch> --json number,url,title,body,baseRefName
```

- Empty → **create mode**.
- Non-empty → **update mode**. Use the PR's own `baseRefName` as base.

## 2. Gather changes

```bash
git log <base>..HEAD --oneline
git diff <base>...HEAD --stat
```

Read the actual diff where the stat is not enough. Every statement in the body must come from the commits and diff, not from guesses.

Group changes by area (app, package, module, docs, infra), using whatever top-level structure the repo has. Do not assume a particular framework, language, or folder layout.

## 3. Choose the body layout

If `.github/pull_request_template.md` exists, it is the PR template. Always use it:

- Keep every heading, in the original order. Do not delete or rename sections.
- Fill each field with real content from the diff. Answer what the field asks, not something nearby.
- Checkboxes: tick only what is true and verified. Leave others unticked.
- Section does not apply → write "N/A" with a short reason. Never leave placeholder text or HTML comment hints.

No template → use this layout:

```
## Summary
1-3 sentences: what and why.

## Changes
Bullets grouped by area.

## Test plan
What ran, and what a reviewer should check.
```

Title: one imperative line in the style of recent `git log` subjects.

## 4. Versions

Only when the body or template has a section that mentions version (release, version, changelog, bump). Otherwise skip.

1. Find the apps this PR touches. Single-project repo → one app. Monorepo (workspaces, `apps/*`, `packages/*`, services) → every app with changed files in the diff, plus apps that depend on a changed shared package when that is clear from the repo.
2. Find the latest tag on GitHub for each app. Read the remote, not local tags, which may be stale:

```bash
git ls-remote --tags --refs origin | sed 's#.*refs/tags/##' | sort -V
```

   Tag style decides the match. Plain tags like `v1.4.2` → one shared version. Prefixed tags like `api-v1.4.2` or `api/v1.4.2` → one version per app, matched by prefix. Also check `gh release list --limit 5` when the repo publishes releases.
3. Compute the new version from the latest tag, following semantic versioning:
   - Breaking change → major.
   - New feature, backward compatible → minor.
   - Fix, refactor, docs, chore → patch.
   - Several kinds of change in one app → highest level wins.
4. Fill the body with the new version only, as plain text in the tag style (va.b.c), for example "v1.5.0". Monorepo → one line per app, for example "api: v1.5.0". No old → new arrow and no explanation of the bump. An app with no changes in the diff gets no bump; omit it, or keep its current version if the template has a field for it.
5. Always compute from the remote tag, never from a version already in the body. Update mode must not bump twice.
6. No tag found for an app → ask the user for the starting version. Do not invent one.

This skill only reports versions in the body. It does not create tags, releases, or edit version files.

## 5. Body rules

- **No backtick character in the title or body.** Backticks can break CI pipelines that read the PR text. This covers inline code, fenced code blocks, and any backticks copied from the template. Write names plainly (api, package.json) or in quotes, and use plain indented text instead of fenced blocks.
- Keep secrets, `.env` values, tokens, and personal data (names, emails, phone numbers) out of the title and body.
- Content comes from the real diff.

Write the body to a file in the scratchpad or temp dir, then check it before use:

```bash
grep -c '`' <body-file>   # must print 0
```

Any hit → remove the backticks and check again.

## 6. Apply

**Create mode:**

```bash
gh pr create --base <base> --head <current-branch> --title "<title>" --body-file <body-file>
```

**Update mode:** refresh the body only. Change the title only when the user asks.

1. Re-run steps 2-5 against the PR's base, so the body covers every commit pushed since the PR opened.
2. Keep accurate content the user added by hand, such as ticked checkboxes and manual notes. Drop what the diff no longer supports.
3. Apply:

```bash
gh pr edit <number> --body-file <body-file>
```

## 7. Report

- Create mode → PR URL.
- Update mode → PR URL plus a short list of what changed in the body (new bullets, version changes).
- Version section filled → list each app with its new version.

## Notes

- This skill creates and edits PRs only. Force-push, close, and merge stay with the user.
