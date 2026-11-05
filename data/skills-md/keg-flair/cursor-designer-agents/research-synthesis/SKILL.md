---
name: research-synthesis
description: Synthesizes raw research notes into themes → insights → opportunities, with evidence snippets and falsifiable hypotheses + success signals. Use when the user has interview/usability notes, support themes, or feedback snippets and needs a structured synthesis.
---

# Research Synthesis

See shared conventions in `docs/HOUSE_STYLE.md` (confidence, fallbacks, evidence labels).

## Defaults

- **Evidence-backed**: themes and insights cite verbatim snippets.
- **Traceable**: keep a line of sight from notes → themes → insights → opportunities.
- **Decision-supporting**: end with hypotheses and success signals (and what to validate next).

## Constraints

- **Do not invent** participant counts, segments, or quotes.
- **Ask at most 3 clarifying questions**; if missing, proceed with low-confidence clusters + what’s needed next.

## Clarifying questions (ask max 3)

1. What was the study goal / decision this synthesis should inform?
2. Who are the participants/segment(s) and sample size (if known)?
3. What’s the product area / flow steps covered by the notes?

## Inputs to request (only if missing)

- Study goal + method (interviews/usability/support themes/etc.)
- Participant segment(s) + count (even rough)
- Raw notes/snippets labeled with participant ID and (ideally) task/step

## Fallback behavior (when notes are too thin)

If notes are fragments without context, produce:
- Provisional themes labeled **Low confidence**
- The **minimum additional inputs** needed (goal, segment, 5–10 verbatim snippets with IDs)
- A suggested **note format** the user can paste next

## Output template

```markdown
#### Study context
- **Study goal**:
- **Participants / segment**:
- **Method**:
- **Key constraints**:

#### Themes (clusters)
##### Theme 1: <name>
- **What we heard**:
- **Evidence snippets**:
  - “...”

#### Insights (so what)
- **Insight**:
  - **Why it matters**:
  - **Who it affects**:
  - **Supporting evidence**:

#### Opportunities (now what)
- **Opportunity**:
  - **Approach**:
  - **Risks / trade-offs**:

#### Hypotheses + success signals
- **Hypothesis**:
  - **Success signals**:

#### Open questions / follow-ups
- …

#### Test plan / validation
- …
```

