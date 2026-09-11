---
name: qualification
description: Write AI qualification prompt variables for prospect evaluation. Creates audience_description, disqualification_criteria, and optional qualification_criteria. Use when setting up AI qualification for a campaign. Triggers on "write qualification", "qualification prompt", or when dispatched by campaign-planning.
model: sonnet
thinking: true
---

# Qualification Skill

Write the structured variables for AI prospect qualification. These variables feed any qualification step that scores or filters individual prospects against an ICP.

## Output Contract

`qualification.md` must follow a fixed structure so downstream campaign tooling can parse it reliably. Hard rules this skill must honor:

- Exactly three H2 headings (case-insensitive match): `## Audience Description`, `## Qualification Criteria`, `## Disqualification Criteria`.
- At least 2 of 3 sections must be populated (non-empty). Fewer is a hard parser error.
- No other H2 headings in the file - they'd be silently ignored.

## Required Context

1. **Read `plan.md`** from the plan folder - Broad ICP definition
2. **Read `search-strategy.md`** from the plan folder - Search filters already applied. Never restate any of these dimensions in the prompt.
3. **Read `{workspace}/research.md`** - Client overview, detailed ICP info, competitors (`{workspace}` = the client campaign workspace, default `./cold-email/{slug}/` under the current directory)

## Core Principles

- **Write short, trust the AI** - The qualification AI is smart. Give it a brief, plain-language brief and let it reason. A few high-signal lines beat an exhaustive rulebook. No long enumerations of titles, industries, or product names.
- **Never repeat the search filters** - `search-strategy.md` already bounds the list (headcount, geography, titles, seniority, industries). Do NOT restate any of it - not in the audience description, not as a criterion. If the filter sets a headcount range, the prompt says nothing about headcount. Qualification only catches what the filters can't see.
- **Don't over-qualify** - Keep it loose. Qualification is a safety net, not a precision filter. When data is incomplete or ambiguous, qualify.
- **Disqualification over qualification** - Prefer audience_description + a few disqualification_criteria only. Add qualification_criteria only when there's a real positive signal worth confirming.
- **Always exclude competitors** - The one disqualifier that's always worth including.

See [references/qualification-guide.md](references/qualification-guide.md) for detailed guidelines and examples.

## Workflow

### Step 1: Load Context
- [ ] Read plan.md for the broad ICP
- [ ] Read search-strategy.md for what's already filtered
- [ ] Read client context and research for competitor info and ICP nuances
- [ ] Read references/qualification-guide.md

### Step 2: Write Qualification Variables

Keep the whole thing short. A sentence or two per section is plenty - the AI fills in the judgment.

**Audience Description** (always required):
- One plain sentence on who we're targeting. 5-20 words.
- No headcount, geography, title lists, or industries - those live in the filters.

**Disqualification Criteria** (strongly preferred):
- A few binary deal-breakers the filters can't see (e.g. competitor, wrong business model).
- 2-4 lines. Always include competitor exclusion. Don't pad the list.

**Qualification Criteria** (optional - usually skip):
- Add only when there's a genuine positive signal worth confirming. Most campaigns don't need it.

### Step 3: Write qualification.md

Keep it lean - short lines, no filter dimensions restated:

```markdown
# Qualification Prompt

## Audience Description
[One plain sentence on who we're targeting. No headcount, geography, titles, or industries.]

## Disqualification Criteria
- [Competitor exclusion]
- [One or two more deal-breakers the filters can't catch, e.g. B2C model, agency/consultancy]

## Qualification Criteria
(Optional - usually skip. Only add a real positive signal worth confirming.)
```

## Output Handling

### Workflow mode (plan folder provided):
1. Write `qualification.md` to the plan folder root
2. Confirm: "Qualification prompt saved to {plan_folder}/qualification.md"

### Standalone mode:
1. Return the output inline to the user

## Variable Definitions

The three structured fields used for qualification:

- `audience_description` - short description of who the target audience is
- `disqualification_criteria` - conditions that disqualify a prospect (bullet points)
- `qualification_criteria` - optional conditions that qualify a prospect (bullet points)
