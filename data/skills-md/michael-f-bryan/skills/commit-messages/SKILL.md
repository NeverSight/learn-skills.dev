---
name: commit-messages
description: When suggesting or writing commit messages for this repo, follow these rules.
---
# Commit messages

When suggesting or writing commit messages for this repo, follow these rules.

## Format

- **Use Conventional Commits.** Prefer the form `type(scope): description` or `type: description`. Keep the type to a set that tools like Release Please recognise: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`. Scope is optional; use it when it helps (e.g. `feat(graphql):`, `fix(data-sourcing):`).
- **Subject line:** Imperative mood, lowercase after the colon. Write it so it would make sense in a changelog on its own (e.g. `feat: add whitelisting_rules query` not `feat: added whitelisting_rules query` or `feat: Adding the whitelisting rules query`).
- **Jira/ticket refs:** Only reference a ticket (e.g. `SIM-652`) in the subject or body if this commit **fully resolves** that ticket. Otherwise omit.
- **Merge commits:** Leave merge commit messages as-is; do not rewrite them.

## Body

- **When to add a body:** Only for non-trivial commits. Small, obvious changes do not need a body.
- **Style:** Prefer short, concise bullet points. Focus on what matters to the end user or to the project’s architecture; avoid narrating every file or line changed.
- **Length:** Keep the message reasonable. Nobody wants to read an essay.

## Examples

**Good (subject only):**
- `feat(graphql): add whitelisting_rules query`
- `fix: upgrade OpenSSL in Docker images to fix CVE-2025-69421`
- `chore: add dependency on ddtrace`

**Good (with body for non-trivial change):**
```
refactor(graphql): split schema into domain modules

- common.py: GlobalID, Blob, PageInfo, Connection, decode_id
- culling.py: CulledDocument, get_culled_documents, WhitelistingQuery
- documents.py: Document, Filters, DocumentsQuery
- schema.py: composes Query, schema, graphql_app

Public API unchanged.
```

**Avoid:**
- Past tense or sentence case in subject: `Added foo`, `Updates the bar`
- Ticket ref when the commit doesn’t close the ticket
- Long, story-style bodies for trivial changes
- Capitalised word after the colon (except proper nouns)
- Do not mention that a commit was co-authored by Cursor in the commit message or trailer.
