---
name: pm-requirements
description: >-
  Write market-driven, prioritized product requirements (a Market Requirements
  Document / MRD) the Pragmatic Institute way. Use when the PM asks for
  "requirements", "an MRD", "what should we build", "prioritize features", "market
  requirements", or wants development to stop saying "requirements aren't specific
  enough". Articulates each requirement as a persona's problem, prioritizes with
  Market Evidence × Impact, and groups them for delivery. Produces a Market
  Requirements Document as a Markdown or Word .docx artifact.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Market Requirements (Pragmatic Framework: Planning → Requirements)

**Rule:** *market problems drive requirements that work.* A requirement articulates a
**problem**, not a solution — the *what* (owned by the PM), never the *how* (owned by
the team). Write every requirement as:

> **[persona]** has **[problem, described in a use scenario]** with **[frequency]**.

If personas or use scenarios aren't ready, run `pm-personas` and `pm-use-scenarios` first.
See `../pm-copilot/references/framework.md`.

## Prioritize objectively (never High/Med/Low or voting)
**Priority = Market Evidence × Impact.**
- **Market Evidence** — a tally of documented occurrences across inputs (discovery
  interviews, surveys, sales calls, support tickets, win/loss, analyst reports,
  reviews, usage data). "How many times have we seen it? What % experience it?"
- **Impact** — an objective 1–5 scale (adapt to your strategy) plus a **99999**
  contractual override:

| Impact | Definition |
| ---: | :--- |
| **99999** | Contractual obligation |
| **5** | Minimum purchase criteria (evaluator) |
| **4** | Potentials lose time or money due to the problem |
| **3** | Difficult for customers to achieve a primary goal |
| **2** | Customers have difficulty with a non-primary goal |
| **1** | Not in the target market segment |

**Advanced — the Four Forces (BUVC):**
> Priority = Evidence × Impact × (B + U + C + V)
Buying (what the buyer needs to make the sale), Using (what the user needs to solve
their problem), Vision (long-term strategic goals), Competitive (stay competitive).
Apply as per-criterion multipliers (example weights B=2, U=1, C=1, V=1).

**Group & Group Order:** a *Group* is two or more requirements that make sense to solve
together; *Group Order* + Priority set the sequence handed to development. "Deliver 100%
of something, not 70% of everything."

## Interview the user (batch questions)
1. The target release goal and what market forces / content is driving it.
2. The personas involved (link or summarize).
3. The list of problems (persona's first person) + the evidence count for each.
4. Impact rating per problem (use the scale) and any contractual must-haves (99999).
5. Which problems naturally group together.

## Artifact template — Market Requirements Document (MRD)
```markdown
# <Product Name> — Market Requirements Document

*This document is confidential and subject to change. For internal use only. No external
commitments can be made based on this document since it is in early planning stages.
Content and timing are very likely to change.*

**Company:** <company>  ·  **Feature / Product:** <product name>
**Author:** <author>  ·  **Contact:** <email>  ·  **Date created:** <date>  ·  **Date last updated:** <date>

## Overview of Target Release
<What is the goal for this release? What market forces are driving this project? What
other artifacts have been created? Are we driven primarily by content or by a target date?>

## Requirements

### GROUP #1 — <Group Name>
<Short description of the group.>

**Requirement #1 — <problem>**
<Persona> has <problem, described in a use scenario> with <frequency>.
**Priority:** 25 (inputs) × 4 (impact) = 100

**Requirement #2 — <problem>**
<Persona> has <problem> with <frequency>.
**Priority:** <evidence> × <impact> = <priority>

### GROUP #2 — <Group Name>
…

## Persona Details
<Full personas, one per page or linked.>

## Requirements Summary
| Name | Market Evidence | Impact | Priority (Evidence × Impact) | Group Name | Group Order |
| :--- | ---: | ---: | ---: | :--- | ---: |
| <req> | 25 | 4 | 100 | <group> | 1 |
<!-- Sort by Group Order ascending, then Priority descending. -->

## Approvals
| Name | Title | Date | Signature |
| :--- | :--- | :--- | :--- |
| | Systems Architect | | |
| | Interaction Designer | | |
| | Product Manager | | |
| | Development Manager | | |
| | Quality Assurance Lead | | |
| | Project Manager | | |

## Change Tracking
| Version | Date | Changes | Reason |
| :--- | :--- | :--- | :--- |
| 1.0 | <date> | Initial draft | — |
```

## Deliver the artifact
Follow `../pm-copilot/references/artifact-output.md`: confirm inputs, **ask Markdown
or .docx**, write the `.md`, convert to `.docx` on request via your environment's native document-creation capability. Then offer the next stages: add context with `pm-use-scenarios`,
assemble a full `pm-prd`, or commit an increment with `pm-release-plan`.
