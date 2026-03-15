---
name: deep-research
description: This skill should be used when the user needs deep, multi-step research using native web tools (WebSearch/WebFetch) without external API keys.
license: MIT
---

# Deep Research (No External API)

## Purpose

Run structured, multi-step research with evidence-first synthesis.

This skill is designed to work **without Google/Gemini API** or any paid provider setup.

## When to Use This Skill

Use this skill when:
- Performing market analysis
- Conducting competitive landscaping
- Building literature or source reviews
- Doing technical due diligence
- Preparing decision memos with citations

## Requirements

- Access to built-in web research tools (`WebSearch`, `WebFetch`)
- Clear research question and scope

No external API key is required.

## Progress Tracking

Display a progress gauge at each research phase:

```
[████░░░░░░░░░░░░░░░░] 20% — Phase 1/5: Defining Objective & Scope
[████████░░░░░░░░░░░░] 40% — Phase 2/5: Collecting Sources
[████████████░░░░░░░░] 60% — Phase 3/5: Deep Analysis & Synthesis
[████████████████░░░░] 80% — Phase 4/5: Drafting Output
[████████████████████] 100% — Phase 5/5: Quality Review & Citations
```

## Workflow

## Research Protocol

1. Define objective and output format
- Clarify the research question, audience, and success criteria.
- Confirm time horizon (e.g., last 12 months, last 5 years).

2. Build search strategy
- Create 5-10 query variants (broad, narrow, comparative, opposing views).
- Prefer primary sources first (official docs, papers, regulatory pages, vendor docs).

3. Collect sources with traceability
- Capture URL, title, date, publisher, and relevance notes.
- Track contradictions and unresolved claims explicitly.

4. Validate and triangulate
- Cross-check key claims with at least 2 independent credible sources.
- Flag weak evidence and avoid overconfident conclusions.

5. Synthesize output
- Produce concise findings with direct citations.
- Separate facts, inferences, and recommendations.

## Output Formats

Choose one based on request:

### 1) Executive Brief
- Objective
- Top findings (5-10)
- Risks / unknowns
- Recommendations
- Sources

### 2) Comparative Analysis
- Criteria matrix
- Option-by-option strengths/weaknesses
- Trade-offs
- Recommendation + rationale
- Sources

### 3) Research Log
- Queries used
- Source inventory
- Evidence quality notes
- Open questions
- Next research steps

## Quality Bar

- Evidence before conclusions
- Date-aware and source-aware claims
- Contradictions surfaced, not hidden
- No uncited critical claims

## Time & Cost

- Time: usually 5-20 minutes depending on scope
- Cost: no external API cost for this skill

## Safety

- Never fabricate sources or citations.
- If evidence is insufficient, state it clearly.
- Distinguish confirmed facts from inference.

## Critical Rules

- Always include citations for material claims.
- Always separate facts from interpretations and recommendations.
- Always mark uncertainty explicitly when evidence is weak or conflicting.

## Error Handling

| Error | Likely Cause | Action |
|-------|-------------|--------|
| WebSearch returns no results | Query too specific, misspelled, or topic very niche | Broaden query, try alternate phrasing, report low-coverage finding |
| WebFetch times out or blocked | Site is down, bot-blocking, or paywalled | Skip that source, note it as inaccessible, continue with other sources |
| Insufficient sources found | Topic has limited public information | Report coverage gaps; recommend user provide domain-specific sources |
| Conflicting information across sources | Different sources cite different facts | Flag the conflict explicitly; present both sides with sources |
| Query too broad | Research question covers too many sub-topics | Ask user to narrow the scope or prioritize specific dimensions |
| Paywalled content | Article requires subscription | Note the source as paywalled; use abstract/preview if available |

## Example Usage

1. "Use deep-research to compare 3 vector databases for enterprise use."
2. "Use deep-research to summarize regulatory updates from the last 12 months."
3. "Use deep-research to produce a source-backed buy-vs-build memo."
