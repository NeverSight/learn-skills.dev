---
name: create-briefing
description: Create shareable briefing documents from sessions, research, or learnings.
---

# Create Briefing

Transform work sessions, research, or learnings into shareable briefing documents. Designed for the emerging pattern where documents need to serve both human readers and AI agents that will consume them later.

## Core Philosophy

**Dual-audience documents**: Every briefing has two sections:

1. **Human-readable top**: Clear, scannable, persuasive content for human readers
2. **AI context bottom**: Structured data, research findings, definitions, and source material that AI agents can draw on

This pattern is increasingly important as people use AI to read and summarize documents.

## When to Use

- End of a research or exploration session
- After significant decisions or debates
- When creating proposals for team review
- When synthesizing multiple sources into a single artifact
- When documenting learnings for future reference

## Invocation

`/briefing` — Assess session and recommend format
`/briefing proposal` — Create a proposal document
`/briefing summary` — Quick summary of session learnings
`/briefing research` — Research synthesis document
`/briefing [custom]` — Natural language guidance on format

## Process

### Step 1: Assess the Content

Before writing, understand:

- **What was accomplished**: Decisions, findings, builds, learnings
- **Who will read this**: Team, stakeholders, future-self, future-AI-agents
- **What's the goal**: Persuade, inform, document, propose, request decision
- **What artifacts exist**: Code, data, research, quotes, examples

### Step 2: Determine Format

Choose format based on **purpose** (what you're trying to accomplish):

#### Inform & Update

| Format                | Best For                                | Length        | When to Use                              |
| --------------------- | --------------------------------------- | ------------- | ---------------------------------------- |
| **Status Update**     | Regular progress reports                | 200-400 words | Weekly/periodic updates to stakeholders  |
| **Executive Summary** | High-level overview for busy readers    | 300-500 words | When execs need the gist without details |
| **Session Notes**     | Capturing learnings from a work session | 200-500 words | End of research/exploration sessions     |

#### Propose & Decide

| Format                     | Best For                              | Length          | When to Use                                          |
| -------------------------- | ------------------------------------- | --------------- | ---------------------------------------------------- |
| **Proposal**               | Pitching an idea, requesting approval | 800-2000 words  | New initiatives, budget requests, strategy changes   |
| **Decision Doc**           | Structured decision with options      | 500-1500 words  | When multiple stakeholders need to align on a choice |
| **One-Pager**              | Concise pitch or summary              | 400-600 words   | Quick executive read, meeting pre-read               |
| **6-Pager** (Amazon-style) | Comprehensive narrative memo          | 1500-2500 words | Major initiatives requiring deep thinking            |

#### Technical & Engineering

| Format                                 | Best For                                  | Length          | When to Use                                        |
| -------------------------------------- | ----------------------------------------- | --------------- | -------------------------------------------------- |
| **RFC / Design Doc**                   | Technical proposals seeking feedback      | 1000-3000 words | Architecture decisions, new systems, major changes |
| **Technical Briefing**                 | Explaining implementation approach        | 500-1500 words  | Onboarding, handoffs, knowledge transfer           |
| **ADR** (Architecture Decision Record) | Documenting a specific technical decision | 300-600 words   | Recording why a particular approach was chosen     |

#### Learn & Reflect

| Format                          | Best For                                | Length         | When to Use                                   |
| ------------------------------- | --------------------------------------- | -------------- | --------------------------------------------- |
| **Research Synthesis**          | Consolidating investigation findings    | 500-1500 words | After research phase, before action           |
| **Post-Mortem / Retrospective** | Learning from incidents or projects     | 500-1200 words | After incidents, project completion, failures |
| **Lessons Learned**             | Capturing insights for future reference | 300-800 words  | End of project phase, after experiments       |

If format isn't clear from invocation, present 2-3 relevant options:

> "This could be a **[format A]** (if goal is X) or **[format B]** (if goal is Y). Which fits better?"

### Step 3: Extract Core Elements

Identify before drafting:

1. **The headline**: What's the single most important thing?
2. **The "so what"**: Why should the reader care?
3. **The evidence**: What supports the conclusions?
4. **The ask** (if any): What decision or action is needed?
5. **The open questions**: What's unresolved?

### Step 4: Draft the Document

Follow the dual-audience structure:

```markdown
# [Title]

## Summary

[2-4 sentences capturing the essence. A reader should understand the core message from this alone.]

---

## [Human-Readable Sections]

[Main content organized by format type - see Format Templates below]

---

## Additional Context (For AIs and Deep Dives)

This section documents the research, analysis, and reasoning that informed this briefing.
Useful for humans wanting to verify claims or AIs needing context for future work.

### [Structured subsections]

[Research findings, source material, definitions, detailed analysis, data dumps]

### Key Definitions

[Terms and concepts that might be ambiguous]

### Referenced Sources

[Links, citations, data sources]
```

### Step 5: Write to File

**Ask for location** if not specified:

> "Where should I save this? Default: `docs/briefings/[date]-[slug].md`"

**File naming**: `YYYY-MM-DD-descriptive-slug.md`

## Format Templates

### Status Update

```markdown
# [Project/Work] Status Update — [Date/Week]

## TL;DR

[One sentence: What's the headline?]

---

## Progress This Period

- **Completed**: [What shipped or finished]
- **In Progress**: [What's actively being worked on]
- **Blocked**: [What's stuck and why]

## Key Metrics / Milestones

| Milestone     | Status                                | Notes        |
| ------------- | ------------------------------------- | ------------ |
| [Milestone 1] | ✅ Done / 🟡 In Progress / 🔴 Blocked | [Brief note] |

## Risks & Issues

[Any concerns stakeholders should know about]

## Next Period Focus

[What's planned next]

## Decisions Needed

[Any blockers requiring stakeholder input]

---

## Additional Context (For AIs)

[Detailed progress notes, links to artifacts, raw data]
```

### Session Notes / Quick Summary

```markdown
# [Topic] — Session Notes

## Key Takeaways

- [Most important point]
- [Second point]
- [Third point]

## What Happened

[Brief narrative, 2-3 paragraphs]

## Open Questions

- [Unresolved item 1]
- [Unresolved item 2]

## Next Steps

- [ ] [Action 1]
- [ ] [Action 2]

---

## Additional Context (For AIs)

[Session details, raw notes, source material]
```

### One-Pager / Executive Summary

```markdown
# [Title]

## The Headline

[One sentence capturing the essence]

## The Situation

[2-3 sentences on context/problem]

## The Proposal / Finding

[2-3 sentences on what you're recommending or what you found]

## Key Points

- [Point 1]
- [Point 2]
- [Point 3]

## The Ask

[What you need from the reader — decision, feedback, awareness]

---

## Additional Context (For AIs)

[Supporting details, data, sources]
```

### Decision Doc

```markdown
# Decision: [Question We're Answering]

## Summary

[What decision is needed and recommended option, 2-3 sentences]

---

## Background

[Context needed to understand the decision]

## Options Considered

### Option A: [Name]

- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Effort**: [High/Medium/Low]

### Option B: [Name]

- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Effort**: [High/Medium/Low]

### Option C: [Name] (if applicable)

- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Effort**: [High/Medium/Low]

## Recommendation

[Which option and why]

## Decision Roles (DACI)

- **Driver**: [Who's driving this to resolution]
- **Approver**: [Who makes the final call]
- **Contributors**: [Who has input]
- **Informed**: [Who needs to know]

## Decision Needed By

[Date/deadline]

---

## Additional Context (For AIs)

### Analysis Details

[Deeper comparison, data, research]

### Stakeholder Input

[Feedback received, concerns raised]

### References

[Related decisions, prior art]
```

### Proposal

```markdown
# [Proposal Title]

## Summary

[What we're proposing and why, in 2-4 sentences]

---

## The Proposal

[Detailed description of what's being proposed]

## Why This / Why Now

[Motivation, context, urgency]

## How It Works

[Implementation approach, phases, details]

## Bull Case / Bear Case

### Why This Could Work

[Arguments in favor, evidence]

### Why This Could Fail

[Risks, challenges, mitigations]

## Resource Requirements

[What's needed: time, people, money, tools]

## Decision Requested

[Specific ask: approve, reject, modify, discuss]

---

## Additional Context (For AIs and Deep Dives)

### Background Research

[Full research, analysis, data that informed proposal]

### Alternatives Considered

[What else was evaluated and why rejected]

### Key Definitions

[Terms that might be ambiguous]

### References

[Sources, prior art, related work]
```

### RFC / Design Doc

```markdown
# RFC: [Title]

**Status**: Draft | Under Review | Approved | Implemented
**Author(s)**: [Names]
**Reviewers**: [Names]
**Last Updated**: [Date]

## Summary

[2-4 sentence overview of the proposal]

---

## Background & Motivation

[Why is this change needed? What problem does it solve?]

## Goals

- [Goal 1]
- [Goal 2]

## Non-Goals

- [What this RFC explicitly does NOT address]

## Proposed Solution

### Overview

[High-level description]

### Detailed Design

[Technical specifics, architecture, interfaces]

### Alternatives Considered

[Other approaches evaluated and why rejected]

## Migration / Rollout Plan

[How to implement incrementally, rollback strategy]

## Risks & Open Questions

- [Risk 1]
- [Open question 1]

## Success Metrics

[How we'll know this worked]

---

## Additional Context (For AIs and Deep Dives)

### Technical Appendix

[Code examples, schemas, detailed specs]

### Research & Prior Art

[Related systems, papers, prior RFCs]

### Glossary

[Technical terms defined]
```

### Post-Mortem / Retrospective

```markdown
# Post-Mortem: [Incident/Project Name]

**Date**: [Date of incident/completion]
**Author**: [Name]
**Status**: Draft | Final

## Summary

[What happened in 2-3 sentences]

---

## Timeline

| Time   | Event           |
| ------ | --------------- |
| [Time] | [What happened] |
| [Time] | [What happened] |

## Impact

- **Duration**: [How long]
- **Affected**: [Who/what was impacted]
- **Severity**: [High/Medium/Low]

## Root Cause Analysis

[What actually caused this? Use "5 Whys" if helpful]

## What Went Well

- [Thing 1]
- [Thing 2]

## What Didn't Go Well

- [Thing 1]
- [Thing 2]

## Lessons Learned

- [Lesson 1]
- [Lesson 2]

## Action Items

| Action   | Owner  | Due Date | Status    |
| -------- | ------ | -------- | --------- |
| [Action] | [Name] | [Date]   | Open/Done |

---

## Additional Context (For AIs)

### Detailed Timeline

[Minute-by-minute if needed]

### Raw Data / Logs

[Supporting evidence]

### Related Incidents

[Links to similar past issues]
```

### Research Synthesis

```markdown
# [Topic]: Research Synthesis

## Summary

[2-4 sentence executive summary]

---

## Key Findings

### Finding 1: [Title]

[Evidence and analysis]

### Finding 2: [Title]

[Evidence and analysis]

## Implications

[What this means for decisions/actions]

## Confidence Assessment

| Finding     | Confidence      | Reasoning |
| ----------- | --------------- | --------- |
| [Finding 1] | High/Medium/Low | [Why]     |

## Open Questions

[What we still don't know]

---

## Additional Context (For AIs and Deep Dives)

### Research Methodology

[How findings were gathered]

### Detailed Findings

[Full analysis, data, quotes]

### Sources

[Links, citations]
```

### ADR (Architecture Decision Record)

```markdown
# ADR-[Number]: [Title]

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: [Date]
**Decision Makers**: [Names]

## Context

[What is the issue that we're seeing that is motivating this decision?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

[What becomes easier or more difficult to do because of this change?]

---

## Additional Context (For AIs)

[Technical details, alternatives rejected, related ADRs]
```

## Writing Principles

### For Human Readers

- **Lead with the headline**: Most important thing first
- **Make it scannable**: Headers, bullets, tables
- **Be direct**: State conclusions, then support them
- **Show, don't tell**: Use examples, data, artifacts
- **End with clarity**: Clear ask or next step

### For AI Consumers

The "Additional Context" section should:

- **Be structured**: Use consistent headers and formats
- **Include raw data**: Quotes, numbers, source material
- **Define terms**: Avoid ambiguity
- **Cite sources**: Links, references, attribution
- **Preserve reasoning**: How conclusions were reached

### General Quality

- **Honest**: Acknowledge uncertainty, present counterarguments
- **Concise**: Say it once clearly, not three times vaguely
- **Actionable**: Reader knows what to do after reading
- **Complete**: All context needed to understand and act

## Quality Checklist

Before delivering:

- [ ] Summary captures the essence in 2-4 sentences
- [ ] Human section is scannable and clear
- [ ] AI section has structured, consumable context
- [ ] Any ask or decision request is explicit
- [ ] Open questions are acknowledged
- [ ] File saved to appropriate location

## Example: What We Just Did

The proposal document we created earlier (`Time Delay Arbitrate - Asian news POC.md`) follows this pattern:

- **Human sections**: Summary, Sprint Plan, Bull/Bear Case
- **AI section**: "Additional Context (For AIs and Deep Dives)" with research findings, definitions, sources
- **Clear ask**: Decision requested with resource requirements

This dual-audience structure makes the document useful both for team review and for future AI agents who need to understand the context.
