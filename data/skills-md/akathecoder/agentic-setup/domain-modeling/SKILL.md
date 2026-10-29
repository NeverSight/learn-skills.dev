---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when terminology, project facts, or durable design decisions must be clarified and recorded, or when another skill needs to maintain them.
---

# Domain Modeling

Actively build and sharpen the active project's domain model while designing. This
is the discipline of challenging terms, testing relationships with concrete cases,
and capturing settled knowledge when it crystallizes.

## Project Artifacts

Use `<workspace-root>/.agents/projects/<project>/` for all project artifacts. Resolve
the opened workspace root from session context before reading or writing. In a
single-repository workspace, use the repository root. Keep this root fixed when
changing directories; never use sub-repositories or global agent-installation
directories. Create only the files that have content to hold:

- `CONTEXT.md` holds a concise project description, confirmed facts, tracker choice,
  reusable non-secret configuration references, relevant links, and domain language.
- `LINKS.md` holds Jira, GitHub, Confluence, repository, and other external links.
- `adr/NNNN-slug.md` holds a durable architectural decision.

Keep `CONTEXT.md` factual and concise. It is neither a specification nor a scratch
pad. A glossary entry defines a project-specific term in one or two sentences and
may name near-synonyms under `_Avoid_`.

## During The Session

1. Read the active project's context and links before proposing terminology or a
   decision. If a user statement conflicts with them or with the codebase, surface
   the contradiction for resolution.

   Done when the current discussion starts from the existing project facts.

2. Challenge vague or overloaded terms. Propose one canonical term, then stress-test
   relationships with concrete edge-case scenarios before recording them.

   Done when each resolved domain concept has an unambiguous definition.

3. Update `CONTEXT.md` and `LINKS.md` inline as facts, terminology, tracker details,
   configuration references, and links become confirmed. Never store secret values;
   record only a variable name, owner, purpose, or retrieval location.

   Done when reusable knowledge is recorded without duplicating implementation plans.

4. Offer an ADR only when the decision is hard to reverse, surprising without
   context, and the result of a real trade-off. Number it after the highest existing
   project ADR and state the context, decision, and reason concisely.

   Done when every qualifying decision is preserved under `.agents/projects/<project>/adr/`.
