---
name: git-pr
description: Write, review, or improve Pull Request titles and descriptions following best practices — clear title format, structured description (What/Why/How/Testing), linked issues, and a reviewer-friendly checklist. Use whenever the user asks to write a PR, open a PR, draft a PR description, review PR quality, or prep a branch for merge. Also trigger on phrases like "เขียน PR", "PR description", "commit message for PR", or "ready to merge?".
---

# PR Best Practices

A skill for writing high-quality Pull Requests that are easy to review, easy to
revert, and easy to trace back to a reason later.

## When to use this

- User asks to write/draft a PR title or description
- User asks "PR นี้โอเคไหม" / "PR นี้พร้อม merge หรือยัง"
- User is about to open a PR and wants a checklist first
- User wants to turn a diff, issue, or changelog into a PR description

## Core principles

1. **One PR = one logical change.** If the diff mixes unrelated changes (e.g. a
   bug fix + a refactor + a new feature), flag it and suggest splitting.
2. **Title says *what*, description says *why* and *how*.** The title should be
   readable on its own in a git log, six months from now, with no other context.
3. **Optimize for the reviewer's time**, not the author's. Small, focused PRs
   get reviewed faster and get better reviews.
4. **Every PR should be revertible on its own.** If it depends on another
   unmerged PR, say so explicitly.

## PR Title Format

Use Conventional Commits style — plain text, no emoji:

```
<type>(<scope>): <short summary, imperative mood>
```

| type       | use for |
|------------|---------|
| feat       | new feature |
| fix        | bug fix |
| refactor   | code change, no behavior change |
| security   | security hardening (auth, rate limiting, secrets, etc.) |
| chore      | tooling, CI/CD, deps, config |
| docs       | documentation only |
| test       | adding/fixing tests |

Examples:
- `feat(booking): send confirmation email with calendar invite`
- `fix(orders): correct leftover slot count after cancellation`
- `chore(ci): add e2e-test job after deploy`

Keep the title under ~70 characters. Imperative mood ("add", "fix", "remove"),
not past tense ("added", "fixed").

## PR Description Template

```markdown
## What
<1–3 sentences: what changed, at a glance>

## Why
<the problem or need this solves — link the issue: Closes #123>

## How
<key implementation decisions worth flagging for the reviewer —
not a line-by-line narration of the diff>

## Testing
- [ ] Tested locally how?
- [ ] New/updated tests added?
- [ ] Ran e2e suite? (link report if CI produces one)

## Screenshots / Logs
<if UI or output changed>

## Rollback / Risk
<anything the reviewer should know before approving — migrations,
config changes, feature flags, whether this is safe to revert>
```

Adapt sections as needed — a one-line `chore` PR doesn't need all of them, but
`feat`/`fix` touching production behavior should keep What/Why/Testing at minimum.

## Reviewer-Facing Checklist (include or self-check before requesting review)

- [ ] PR is scoped to one logical change
- [ ] Title follows `type(scope): summary` format
- [ ] Linked to an issue (`Closes #N` / `Refs #N`)
- [ ] Secrets/credentials are not touched or exposed in the diff
- [ ] CI passes (build, tests, e2e if applicable)
- [ ] No debug code, commented-out blocks, or stray console/print logs left in
- [ ] Breaking changes or migrations are called out explicitly

## Working with the user

- If given a diff or list of changes, draft the title + description directly —
  don't just describe what a good PR looks like in the abstract.
- If given a vague request ("PR สำหรับ booking feature"), ask what changed and
  why, rather than guessing.
- If the diff looks like it mixes concerns (e.g. a CI change bundled with a
  feature), say so and suggest splitting before writing the description.
- Match the user's language (Thai or English) in the actual PR text, since
  that's what teammates will read.
- Don't invent testing steps, rollback notes, or issue links that weren't
  provided — leave a placeholder and ask, rather than fabricating specifics.