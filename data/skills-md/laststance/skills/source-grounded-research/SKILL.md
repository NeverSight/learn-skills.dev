---
name: source-grounded-research
description: Cited research briefs
disable-model-invocation: true
---

# Source-Grounded Research

## Purpose

Use this skill for research-only tasks that should end in a cited brief rather
than code changes.

This skill is for:

- web research
- library and framework documentation lookup
- open-source repository investigation
- comparison and decision support
- recent changes and release-note checks

Do not use this skill for:

- implementation work
- code editing
- speculative answers without sources

## Quick Start

1. Restate the question and classify it into one primary lane.
2. Start from the lane's highest-authority source.
3. Corroborate major claims with a second source.
4. Check for contradictions or recent changes.
5. Produce a cited report with a query log and sources section.

## Research Lanes

### `library-framework`

- Start with official docs via `Context7` when available.
- Use `get_code_context_exa` for examples and practical usage.
- Use `Perplexity` or `WebSearch` only for contradiction checks or recent
  changes.

### `oss-repository`

- Start with `DeepWiki` when available.
- Read repo structure before asking detailed questions.
- Corroborate key claims with GitHub docs, repo pages, Exa, or official docs.

### `recent-changes`

- Start with `Perplexity Search` or standard `WebSearch`.
- Verify final claims with official release notes, changelogs, or docs.

### `local-plus-external`

- Start with local repo evidence tools first.
- Bridge to external docs only after the local behavior is understood.

### `comparison-decision`

- Start with breadth discovery.
- Run an authority pass.
- Run a contradiction pass before recommending.

## Tool Priority

Prefer tools by role, not habit:

- `Sequential Thinking`: scope, sub-questions, assumptions
- `Context7`: official library/framework docs
- `DeepWiki`: OSS repository architecture and topic map
- `Exa`: breadth discovery and code/doc context
- `Perplexity`: recent web-grounded synthesis and contradiction checks
- `WebSearch` / `WebFetch`: standard web fallback or direct page retrieval
- local repo tools: first-class evidence when the question touches local code

## Output Contract

Always include:

1. Executive Summary
2. Evidence Map
3. What We Know
4. What We Infer
5. Contradictions and Unknowns
6. Confidence
7. Actionable Next Steps
8. Query Log
9. Sources

## Citation Rules

- Every material factual claim must have an inline citation.
- Prefer direct URLs to primary sources.
- If only secondary evidence exists, say so explicitly.
- Keep facts and inference separate.

## Failure Rules

- If a tool is unavailable, switch to another tool with the same role.
- If evidence is thin, say `insufficient evidence`.
- If there is no primary source, lower confidence and state the limitation.
- If evidence conflicts, preserve both sides with citations.

## Report Template

Use this structure:

```markdown
## Executive Summary
- Key takeaway with citation

## Evidence Map
- Primary: why this source is authoritative
- Supporting: what it adds
- Counter: what challenges the main claim

## What We Know
- Fact with citation

## What We Infer
- Inference linked back to evidence

## Contradictions and Unknowns
- Open disagreement or missing source

## Confidence
- high | medium | low

## Actionable Next Steps
- Specific follow-up

## Query Log
| Tool | Query/Prompt | Filters | Why Used | Outcome |
| --- | --- | --- | --- | --- |

## Sources
- [Title](https://example.com) - Publisher, date
```

## Additional Guidance

- For the detailed lane matrix and DeepWiki workflow, see [reference.md](reference.md).
- For concrete example prompts and output shapes, see [examples.md](examples.md).
