---
name: pr-review
description: "PR Review: Comprehensive code review based on project standards"
disable-model-invocation: true
---

# PR Review: Comprehensive code review based on project standards

When the user types `/pr-review`, perform a comprehensive pull request code review.

## 1) Collect required inputs (ask before doing anything)

Before proceeding, ask the user for:

- **Base branch**: the branch being merged INTO (e.g., `master`, `env/staging`, `env/sandbox`)
- **Compare branch**: the branch being reviewed (e.g., `feature/my-feature`)

Do NOT proceed until both branches are provided.

## 2) Load the current project rules

Read ALL rules in the `.cursor/rules/` directory to ensure the review reflects the most up-to-date project standards:

```
@.cursor/rules/
```

Pay special attention to:
- `@.cursor/rules/ai-programming-assistant.mdc` — general code quality expectations
- `@.cursor/rules/ruby-no-default-params.mdc` — Ruby method signature rules
- `@.cursor/rules/ui-code-naming-conventions.mdc` — UI vs code naming mismatches
- Any domain-specific rules that apply to the changed files

## 3) Analyze the diff

Run the following shell command to get the full changeset:

```bash
git diff <base-branch>...<compare-branch>
```

**Important**: Use three dots (`...`) not two. This shows all changes on `<compare-branch>` since it diverged from `<base-branch>`, which is what we want for PR review. Two dots would include changes on both branches.

For each changed file, identify:
- File type (Ruby, TypeScript, GraphQL, ERB, spec, etc.)
- Which cursor rules apply to that file type
- The nature of the change (new feature, bug fix, refactor, test, etc.)

## 4) Perform the code review

Evaluate the changes against ALL applicable rules. Organize findings by severity:

### Critical (must fix before merge)
- Security vulnerabilities
- Data integrity issues
- Breaking changes without migration path
- Violations of `@.cursor/rules/` that could cause bugs

### Important (should fix)
- Rule violations that affect maintainability
- Missing tests for new functionality
- Performance concerns
- Accessibility issues (for UI changes)

### Suggestions (nice to have)
- Code style improvements
- Refactoring opportunities
- Documentation gaps

### Positive observations
- Well-structured code worth highlighting
- Good test coverage
- Clever solutions or patterns worth noting

## 5) Check against specific rule categories

### Ruby code (`*.rb`)
- [ ] No default parameters in method definitions (`ruby-no-default-params.mdc`)
- [ ] Sorbet types are correct and strict where required
- [ ] RuboCop violations addressed (run `bundle exec rubocop` on changed files)
- [ ] Packwerk boundaries respected (`bin/packwerk check`)
- [ ] No TODOs, placeholders, or incomplete implementations

### GraphQL (`app/graphql/**`)
- [ ] UUIDv7 identifiers at boundaries (not integer IDs)
- [ ] No `me` field usage
- [ ] Proper pagination with bounds
- [ ] Unions preferred over interfaces
- [ ] Auth checked at resolver level

### React/TypeScript (`*.ts`, `*.tsx`)
- [ ] Functional components with hooks only
- [ ] No unnecessary effects
- [ ] No premature memoization
- [ ] Proper TanStack Query patterns (no double mutations)
- [ ] SquareKit components used where applicable
- [ ] Accessibility guidelines followed

### Tests (`*_spec.rb`, `*.test.ts`)
- [ ] Tests written FIRST (TDD)
- [ ] Verified doubles with constant classes (not plain doubles)
- [ ] Integration tests preferred over mocks
- [ ] Coverage for both happy path and edge cases

### Migrations (`db/migrate/**`)
- [ ] Safe migration patterns (no data loss)
- [ ] Indexes added for foreign keys and query patterns
- [ ] UUIDv7 for new ID columns

## 6) Output format

Structure the review as:

```markdown
# PR Review: [compare-branch] → [base-branch]

## Summary
[1-2 sentence overview of what this PR does]

## Rule Compliance
[Which cursor rules were checked and their status]

## Findings

### Critical
[List or "None"]

### Important
[List or "None"]

### Suggestions
[List or "None"]

### Positive Observations
[List or "None"]

## Files Reviewed
[List of files with brief notes on each]

## Recommendation
[ ] Ready to merge
[ ] Ready after addressing Critical issues
[ ] Needs significant rework
```

## 7) Interactive follow-up

After presenting the review, offer to:
- Explain any finding in more detail
- Suggest specific code fixes for any issue
- Re-review after changes are made
