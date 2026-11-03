---
name: pr
description: Create clear, concise, reviewer-friendly pull request titles and descriptions. Use when preparing, writing, or improving a pull request.
---

## Instructions

Before writing:

1. Inspect the Git diff, including staged and unstaged changes.
2. Understand the purpose of the changes.
3. Identify the main functionality, bug fixes, or refactoring.
4. Identify relevant tests and their actual results.
5. Check for breaking changes, migrations, configuration changes, or deployment requirements.
6. If the purpose is unclear, ask for clarification rather than inventing intent.

## Title guidelines

- Use Conventional Commit prefixes where appropriate:
  - `feat:` — New functionality.
  - `fix:` — Bug fixes.
  - `refactor:` — Internal restructuring without behavior changes.
  - `perf:` — Performance improvements.
  - `test:` — Test-related changes.
  - `docs:` — Documentation changes.
  - `chore:` — Maintenance tasks.
- Keep titles concise and descriptive.
- Use imperative or direct wording.
- Focus on the outcome, not implementation details.
- Avoid vague titles such as "Updates", "Improvements", or "Various fixes".

Examples:
- `feat: add phone number verification`
- `fix: prevent duplicate order submissions`
- `refactor: simplify payment processing`
- `perf: reduce unnecessary conversation queries`

## Description guidelines

Use the following structure when appropriate:

### Summary
Briefly explain what the PR accomplishes and why it is needed.

### Changes
List the important changes in concise bullet points.

Focus on meaningful behavior and functionality rather than listing every modified file.

### Testing
Mention relevant tests that were actually executed and their results.

Never claim tests passed unless verified.

### Additional Notes
Include only when relevant:
- Breaking changes.
- Database migrations.
- Environment variable changes.
- Deployment requirements.
- API changes.
- Important implementation decisions.

Omit sections that have no meaningful content.

## Quality standards

- Be concise. Do not repeat the same information across sections.
- Do not describe obvious implementation details.
- Do not invent requirements, motivations, or testing results.
- Do not exaggerate the scope of changes.
- Use terminology consistent with the codebase.
- Make the description understandable without requiring the reviewer to inspect every changed file.
- Highlight important behavioral changes and potential review considerations.
- Never include unrelated changes in the description.

## Output

Use the Github CLI to file the pull request.