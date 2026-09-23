---
name: github-issue-pr
description: >-
  Draft and file well-structured GitHub issues AND pull requests via the `gh` CLI. Use whenever the
  user wants to create, file, open, draft, raise, or log a GitHub issue/ticket/bug/feature-request/task,
  OR to open/draft/create a pull request (PR) — phrasings like "create an issue", "file a gh issue",
  "open a github ticket", "log this bug", "raise an issue", "open a PR", "draft a pull request", "create
  the PR", or when they hand you a chat/diff/piece of work and ask to capture it as a GitHub issue or PR.
  Also use it to write an issue or PR body to a file for review before filing. It distinguishes bug
  reports (reproduction + root cause + file:line) from feature/task issues (outcome + acceptance
  criteria, NOT implementation), and issues (describe behaviour, NO code internals) from PRs (the
  Changes section DOES carry code internals). This is for GitHub via `gh` — for Jira/Linear/Asana use
  the dedicated ticket skill instead.
---

# GitHub Issue & PR

Turn a request — a bug you found, a feature to build, a chunk of work to ship — into a clear GitHub
**issue** or **pull request**, then file it with `gh`. A good issue/PR is read by people who weren't in
the room: it should stand on its own and say why it matters.

The single most important rule: **issues describe behaviour, PRs describe the change.** An issue leaves
*how* to the implementer and carries no code internals; a PR's `## Changes` section is exactly where
code internals (files, functions, endpoints, models) belong.

## Match the repo's house style first

Templates below are a starting shape, not a straitjacket. Repos rarely ship a `.github` template file —
the real convention is set by example. **Before drafting, skim a couple of recent issues/PRs**
(`gh issue list`, `gh pr list`, then `gh issue view <n>` / `gh pr view <n> --json title,body`) and match
their section layout. Drop sections that don't apply.

## Issues

### Pick the type first: bug vs. everything else

- **Bug** — something is broken. Specifics are the point: pin down reproduction, expected-vs-actual,
  and — when known — the root cause with `file:line`. Concrete internals are a feature here, not a leak.
- **Feature / task / enhancement / chore** — work to be done. Describe the *outcome and behaviour*, not
  the code. Do **not** prescribe file paths, function/class names, or module structure — that's the
  implementer's job and it goes stale the moment the code moves.

If the type is ambiguous, ask the user rather than guessing.

### Issue template — Bug

```markdown
## Summary
<one or two sentences: what's broken and the visible effect>

## Steps to reproduce
1. …
2. …

## Expected vs actual
- Expected: …
- Actual: …

## Root cause  (include only if known)
<the mechanism, with file:line references, e.g. `foo/bar.py:42`>

## Impact
<who/what is affected, severity, how often>
```

### Issue template — Feature / task

```markdown
## Summary
<what capability this delivers and WHY it's worth doing>

## Behaviour
<observable behaviour as bullets — what the system should do, from the outside>

## Acceptance criteria
<checklist of objectively verifiable outcomes that mean "done">

## Out of scope
<explicitly what this issue does not cover, to prevent scope creep>

Jira: PROJ-1234 — https://<org>.atlassian.net/browse/PROJ-1234   (drop if no tracker)
```

Interface-level facts are fine in a feature issue (an endpoint path, which external service is called,
"stored and available to the X pipeline") — those describe behaviour and contracts. Code internals
(this file, that function) are **not** — save those for the PR.

## Pull requests

A PR restates the delivered work: *what & why*, then the concrete changes. Unlike an issue, the
`## Changes` section is expected to name files, functions, endpoints, and models — that's the review
surface.

### PR template

```markdown
## What & why
<what the change delivers and WHY — a sentence or two>

Closes #<issue-number>.

## Jira
https://<org>.atlassian.net/browse/PROJ-1234

## Changes
- **<area / symbol>** (`path/to/file.py`) — what changed and the resulting behaviour.
- <one bullet per meaningful change; code internals ARE expected here>

## Out of scope
<what this PR deliberately does not cover>
```

- `Closes #<n>.` in the body auto-closes the linked issue on merge — file the issue first, then paste
  its number in.
- Add `## Deploy notes` **only** when the change needs an out-of-band step (a migration, a new index,
  a config/env change); omit it otherwise.
- Keep the PR title in the repo's commit style (e.g. `fix: …` / `feat: …`) if it uses one.

## Filing with `gh`

Draft the body first. For anything non-trivial, **write it to a file and show the user before filing** —
issues and PRs are outward-facing and awkward to undo, so confirm unless they've said "just file it".

1. **Target repo.** Inside the repo's checkout, `gh` infers it. Otherwise pass `--repo owner/name`.
2. **Write the body to a file** (`gh` markdown is easiest via a file, not inline `--body`): e.g.
   `ISSUE.md` / `PR.md` or a temp file.
3. **Create the issue:**
   ```bash
   gh issue create \
     --title "<concise, specific title>" \
     --body-file /path/to/ISSUE.md \
     --assignee @me        # @me = the authenticated user; or a github login
   ```
4. **Create the PR** (branch must be pushed first; the user drives version control unless they've asked
   you to push):
   ```bash
   gh pr create \
     --base <default-branch> \
     --head <feature-branch> \
     --title "<concise title>" \
     --body-file /path/to/PR.md \
     --assignee @me
   ```
   - Before creating a PR, check the branch isn't already open: `gh pr list --head <feature-branch>`.
   - `--label bug` / `--label enhancement` only if the label exists (`gh label list`); a missing label
     fails the command. Many repos label nothing — match what recent issues/PRs do.
5. **Report the URL** `gh` prints.

## Titles

Concise and specific — someone scanning the list should get the gist. Prefer
"KR-Type1 stops regenerating after a correction" over "KR-Type1 bug". No trailing period. For PRs,
follow the repo's commit-prefix convention when it has one.

## Capturing work from the current session

If the user says "turn this into an issue/PR" about work already discussed, mine the conversation for
the what/why, the acceptance criteria, and (for a bug) the root cause — then confirm the gaps with the
user rather than inventing detail. Keep it one issue per distinct concern; split if a thread covers two.
