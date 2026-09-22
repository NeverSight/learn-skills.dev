---
name: baselinedocs-extract-wiki
description: Extract reusable implementation guidance from a baseline pack or completed code change into a concise project wiki article. Use automatically when task-specific history is obscuring a repeatable migration, integration, conversion, or engineering pattern needed elsewhere.
---

# Baseline Docs Extract Wiki

Turn reusable knowledge into a task-independent article.

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Workflow

1. Identify a pattern that can be applied outside the originating task.
2. Verify the pattern against current code and explicit decisions.
3. Remove task chronology, attempt history, phase status, and one-off ownership details.
4. Write or update `docs/wiki/<topic>.md`.
5. Use this frontmatter:

```yaml
---
wiki_schema: "1.0"
topic: "<kebab-case-topic>"
status: "verified"
updated: "YYYY-MM-DD"
code_ref: "<commit|uncommitted|unknown>"
applies_to:
  - "<scope or glob>"
---
```

6. Structure the article around:
   - intent and applicability
   - prerequisites
   - canonical implementation pattern
   - migration or usage steps
   - verification
   - limitations
7. Replace duplicated guidance in baseline packs with a direct wiki link when safe.

## Boundaries

- Keep baseline packs as task state and the wiki as reusable guidance.
- Do not publish assumptions as a verified pattern.
- Do not copy the full pack into the wiki.
- Preserve exceptions that materially limit reuse.
