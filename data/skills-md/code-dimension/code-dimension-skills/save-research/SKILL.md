---
name: save-research
description: Save a complete research record from an AI-agent discussion into docs/researchs/. Use when the user asks to save, register, document, persist, or consolidate research, investigation, discovery, decisions, alternatives, or context after discussing a topic with AI agents, especially when the saved research will later feed OpenSpec/spec creation.
metadata:
  author: code-dimension
  version: 1.0
---

# Save Research

## Purpose

Create a durable Markdown research document under `docs/researchs/` that preserves the full useful context from the current AI-agent discussion so it can be used later to create specs.

## Workflow

1. Stay inside the current repository.
2. Inspect `docs/researchs/` before writing:
   - Create the directory if it does not exist.
   - Reuse any established naming or formatting pattern already present.
   - Avoid overwriting an existing research file unless the user explicitly asks to update that file.
3. Choose a file name:
   - Use `YYYY-MM-DD-short-topic-slug.md`.
   - Keep the slug lowercase, ASCII, and hyphen-separated.
   - If a file already exists, append a short differentiator such as `-2` or a narrower topic.
4. Reconstruct the research from the current conversation and any artifacts already inspected in the session.
5. Include concrete evidence from files, commands, specs, docs, payloads, errors, links, or decisions that were discussed.
6. Write only the research document unless the user explicitly asks for additional changes.
7. Verify the file exists and review the diff before reporting completion.

## Completeness Rules

- Capture the conversation faithfully, including corrections, rejected ideas, uncertainty, tradeoffs, and changes in direction.
- Prefer exact names, paths, fields, commands, payload keys, errors, dates, and identifiers over vague summaries.
- Distinguish confirmed facts from assumptions, hypotheses, and unverified memory.
- Preserve the user's intent and constraints in their practical form, not just as a high-level summary.
- Record what was not done and why, especially if implementation, validation, or spec creation was intentionally deferred.
- Do not invent details to make the research look complete. If context is missing, add it under "Gaps / Missing Context".
- Redact secrets, credentials, private tokens, and sensitive personal data. Keep enough structure to make the evidence useful.

## Research Document Structure

Use this structure unless an existing `docs/researchs/` pattern clearly says otherwise:

```markdown
# <Research Title>

Date: YYYY-MM-DD
Status: Research captured
Source: AI-agent discussion
Related specs: <existing spec/change ids, or "None yet">

## Objective

<What the user wanted to understand, decide, or prepare for.>

## Context

<Relevant background, repository/module boundaries, business/domain facts, and prior constraints discussed.>

## Discussion Timeline

- <Important step, correction, or discovery in order.>

## Findings

- <Concrete finding with supporting evidence.>

## Decisions

- <Decision made, with rationale.>

## Alternatives Considered

- <Alternative, why it was considered, and why it was accepted/rejected/deferred.>

## Requirements Candidates

- <Potential requirement that could later become spec text.>

## Implementation Notes

- <Potential code/data/docs locations, integration points, commands, migration notes, or validation notes.>

## Risks And Open Questions

- <Known risks, unresolved questions, missing inputs, or validation gaps.>

## Evidence

- <Files, commands, outputs, payload snippets, links, or other source material discussed.>

## Spec Follow-Up

- <Recommended next steps for creating OpenSpec/spec artifacts later.>
```

## Writing Guidelines

- Write in the same language the user used in the research discussion; default to Portuguese for Portuguese conversations.
- Be exhaustive about the useful context, but keep wording factual and structured.
- Use Markdown headings and bullets for scanning.
- Use code blocks for payloads, command snippets, schemas, errors, or exact examples.
- Link repository files with relative paths in the document unless the local convention uses absolute links.
- Keep the document as research, not as an implementation plan pretending to be approved spec work.

## Boundaries

- Do not create or modify OpenSpec specs unless the user explicitly asks.
- Do not edit application code while saving research.
- Do not rerun broad investigations unless the research cannot be saved honestly from available context. If extra verification is needed, do the smallest targeted lookup first.
