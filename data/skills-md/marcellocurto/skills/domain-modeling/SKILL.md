---
name: domain-modeling
description: Define and maintain the codebase's shared domain terms and architectural decisions.
---

# Domain Modeling

Clarify the project's domain concepts and the decisions that shape them. Use this skill when defining or revising those meanings; merely reading an existing glossary does not require a modeling session.

## Choose the working mode

- **Discussion or proposed edits:** For discussion, review, or read-only requests, keep definitions, decisions, and proposed document changes in the conversation. Do not create or edit files.
- **Documentation updates:** When the user asks to create or maintain domain documentation, or requests a workflow that includes recording it, write settled terms and qualifying decisions within that scope. Honor authorization already given without asking again for each entry. If writes are limited to particular documents, keep other proposed records in the conversation.

Loading this skill alone does not authorize documentation writes. When the request does not establish write intent, continue in discussion mode. Recording a model does not authorize implementing it or renaming code.

## Find the existing documentation

Inspect repository guidance and relevant documentation for the current glossary, context map, ADR location, and document formats. Follow existing names, links, context ownership, and numbering before creating anything. A glossary or ADR directory with a different name is not missing documentation.

If no convention exists, use `CONTEXT.md` for domain terms and `docs/adr/` for architectural decisions. Create them only in documentation-update mode when there is agreed content to record. Use an existing context map, whatever its filename, to locate domain-specific records; do not infer that the whole project has one context merely because a root `CONTEXT.md` exists.

## During the session

### Challenge against the glossary

Compare the intended meaning with the glossary. Ask about a conflict when it changes a domain distinction, behavior, ownership, or contract. Ordinary synonyms or wording variations that clearly refer to the same concept do not need an interruption; use the established term in your response.

### Sharpen fuzzy language

Use context and available evidence to interpret an overloaded term. If materially different meanings remain plausible, explain the distinction and ask a focused question. Recommend a canonical term when useful, but do not treat that recommendation as an agreed change or police wording for consistency alone.

### Discuss concrete scenarios

Use concrete scenarios when they distinguish plausible meanings or expose an unresolved domain rule. Focus on cases that could change the current decision; do not generate edge cases merely to prolong the discussion.

### Cross-reference with code

Check relevant code when it can establish current behavior or clarify a material distinction. Keep implemented behavior separate from the user's intended model. If they differ, establish whether the user is describing a planned change, correcting stale documentation, or resolving an inconsistency; do not reopen an explicit decision merely because the code has not caught up.

### Record settled meanings

In documentation-update mode, record a resolved term in the existing glossary as its meaning settles. In discussion mode, retain the agreed definition or proposed text in the response. Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) only when the project has no established format.

Keep glossary entries focused on domain meaning. Put implementation decisions in the appropriate architectural record rather than a definition. Preserve unrelated sections of existing documents; do not reshape a multipurpose `CONTEXT.md` into a glossary-only file. Keep unresolved proposals and assumptions distinct from agreed content.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the unsolicited ADR. When documentation updates are already authorized, record qualifying settled decisions without requesting approval again. Otherwise propose the record in the conversation. Follow the project's ADR format; use [ADR-FORMAT.md](./ADR-FORMAT.md) when no convention exists.

## Finish

Summarize the resolved meanings and decisions, material open questions, and documents updated or proposed. Read back written changes to confirm they express the agreed meaning and preserve existing context. Do not claim proposed text was saved in discussion mode.
