---
name: pr-gen
description: Use when the user asks to generate, write, draft, refresh, retitle, or align a GitHub Pull Request title or description for the current branch — including phrasings like "write the PR description", "update the PR", "summarize this branch for review", "match our PR template", or "regenerate the body". Analyzes `git diff` against the base branch (final state, not commit history) so added-then-removed work is omitted and fabrication is avoided. Skip for changelogs, release notes, issue comment summaries, or open-ended code review.
compatibility: Requires git and the GitHub CLI (`gh`) authenticated to the repo.
license: MIT
---

# pr-gen

Generate or update a GitHub PR title and description from the **final state** of
the current branch (`git diff "$base"...HEAD`), not from commit history.

## Principles

1. **Document `HEAD`, not history.** If a change was added then removed, it does
   not exist — do not mention it.
2. **Verify before citing.** Run `git show HEAD:<path> | grep …` for every
   feature, file, symbol, or test you plan to reference.
3. **Be concise.** 15–30 lines is typical; ≤ 50 for genuinely complex PRs.
4. **Respect project conventions.** If `.github/PULL_REQUEST_TEMPLATE.md` or
   `CONTRIBUTING.md` exist, follow them exactly — they win over this skill's
   templates.
5. **Refuse rather than fabricate.** If the branch cannot satisfy the chosen
   template's required sections, stop and tell the user what is missing. Do not
   silently downgrade to a looser template, and never list a file, symbol, or
   test that is not in `HEAD`.

## Workflow

### 1. Locate the PR and base branch

```bash
branch=$(git branch --show-current)
base=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null || echo main)
pr=$(gh pr view --json number,state 2>/dev/null)
```

If a PR exists and its state is not `OPEN`, stop and ask the user whether to
(1) create a new PR, (2) edit the closed/merged one anyway, or (3) cancel.
Re-check the state again immediately before `gh pr edit` (TOCTOU window).

### 2. Inspect the final-state diff

```bash
git diff "$base"...HEAD --stat
git diff "$base"...HEAD --name-only | cut -d/ -f1 | sort -u
git log "$base"..HEAD --oneline   # context only — not the source of truth
```

For every feature, file, or symbol you plan to mention:

```bash
git show HEAD:<path> | grep -n '<symbol-or-feature>'
```

### 3. Check project requirements

```bash
for f in .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md \
         PULL_REQUEST_TEMPLATE.md CONTRIBUTING.md; do
  [ -f "$f" ] && { echo "# $f"; cat "$f"; }
done
```

A repo template wins on structure. `CONTRIBUTING.md` may add required sections
(performance repro steps, spec updates, security statements, …).

### 4. Classify the change

Pick exactly one: **bugfix**, **feature**, **refactor**, **infra**, **docs**.

If classified **bugfix**, the branch MUST contain all of:

- An articulable invariant (or expected behavior) that the fix restores.
- Non-test code implementing the fix (or an explicit "test-only" confirmation
  from the user).
- At least one test per invariant, wired into the project's test runner.

```bash
git diff "$base"...HEAD -- '**/*test*' '**/tests/**' '**/*_test.*' '**/*.spec.*'
```

If anything required is missing, stop and list the gaps. Do not generate.

### 5. Pick a template

| Classification    | Template                                                          |
| ----------------- | ----------------------------------------------------------------- |
| bugfix            | [assets/templates/bugfix.md](assets/templates/bugfix.md)          |
| feature, refactor, docs | [assets/templates/feature.md](assets/templates/feature.md)  |
| large infra only  | [assets/templates/infrastructure.md](assets/templates/infrastructure.md) |

Read only the template you picked. The bugfix template is **prescriptive**
(four required sections, in order); the feature and infrastructure templates
are **defaults** — drop sections that don't apply rather than padding them.

### 6. Write the title

Default shape: `<type>(<scope>): <imperative summary>` (e.g.
`fix(auth): restore retry-safe WOTS keypair generation`,
`feat(api): add idempotent webhook delivery`).

Under 72 characters; imperative mood; describes the outcome, not the process.

If the repo's existing PRs and `CONTRIBUTING.md` use a different convention
(plain prose, ticket-prefix, etc.), match it. Load
[references/title-patterns.md](references/title-patterns.md) only when the
repo lacks an established convention and you need fallback shapes.

### 7. Write the description

- Bullets over paragraphs; one idea per bullet.
- Repo-relative file links: `[file.ts](src/file.ts)` or
  `[file.ts:42](src/file.ts#L42)`.
- Cite only what `git show HEAD:…` confirmed.
- Present tense ("Adds X", "Removes Y").
- Skip `## Background` / `## Implementation Details` unless something is
  genuinely non-obvious — link the issue or design doc instead.
- Do **not** append "Generated with Claude" / `Co-Authored-By:` footers; that
  belongs in commit metadata, not PR bodies.

If you need worked examples of how to verify scope and link
files, load [references/analysis-workflow.md](references/analysis-workflow.md).

### 8. Push the update

Re-check PR state, then:

```bash
gh pr edit "$pr_number" \
  --title "$title" \
  --body "$(cat <<'EOF'
<description>
EOF
)"
gh pr view "$pr_number"
```

If no PR exists, use `gh pr create --base "$base"` with the same `--title` and
`--body`.

## Gotchas

- `git log $base..HEAD` shows commits, including ones whose changes were later
  reverted. Use `git diff $base...HEAD` for what's actually shipping.
- `gh pr view` outside a PR-linked branch exits non-zero — capture stderr or
  `|| echo …` so the script keeps going.
- `.github/PULL_REQUEST_TEMPLATE.md` may be lowercase, uppercase, plural
  (`pull_request_template/`), or live in `docs/`. Check all four.
- A bugfix branch with only test additions is a "test-only" PR, not a bugfix —
  ask the user before classifying.

## Final checklist

- [ ] Every feature, file, symbol, and test cited is present in `HEAD`.
- [ ] No mention of added-then-removed work.
- [ ] File links are repo-relative.
- [ ] Repo PR template (if any) is followed exactly.
- [ ] Length 15–30 lines (≤ 50 for complex PRs).
- [ ] Bugfix PRs use the four-section invariants+tests structure.
- [ ] No "Generated with Claude" / `Co-Authored-By:` footers in the body.
