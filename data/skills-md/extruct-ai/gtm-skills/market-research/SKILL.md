---
name: market-research
description: >
  Research a target vertical's pain points using deep research APIs and distill
  findings into a numbered hypothesis set. Pure industry education tool —
  decoupled from email generation. Use when the user wants to understand a
  market before outreach, form hypotheses about a vertical, or build an
  industry knowledge base. Triggers on: "deep research", "hypothesis set",
  "research pain points", "research vertical", "sourcing research", "pain
  mapping", "industry problems", "market research", "educate me on".
---

# Market Problems Deep Research

Research a target vertical's pain points using deep research APIs. Distill findings into a numbered hypothesis set. Output is pure industry education — no email generation, no company matching.

## Environment

Provider selection and credentials are handled in Step 0 of the workflow.

## Workflow

### Step 0: Confirm provider and learn API

1. Ask the user which deep research provider they want to use. If they're unsure, Perplexity is a common choice — see workflow below for query design patterns.
2. Fetch or read the provider's API documentation and identify:
   - Chat/completions or search endpoint
   - Available models (pick the one with web search / citations)
   - Authentication method and credentials
   - Rate limits
3. Ask for their API credentials and confirm access before proceeding

### Step 1: Define the research scope

Read the company context file if it exists (`claude-code-gtm/context/{company}_context.md`) for ICP and existing hypotheses.

Ask the user for:

| Input | Required | Example |
|-------|----------|---------|
| Target vertical | yes | "Mid-market logistics companies" |
| Specific sub-verticals | yes | "3PL, freight brokerage, cold chain" |
| What we solve for them | yes | "Find potential partners and customers in fragmented markets" |
| Existing hypotheses to test | no | From context file or user input |

### Step 2: Run hypothesis-driven research

Do NOT run generic research. Run 3-4 focused queries, each targeting a different angle of the same problem. The queries should be specific enough to return actionable data points, not overviews.

**Query design principles:**
- Each query should target ONE specific aspect of the pain
- Ask for concrete data points, numbers, timelines, tool names
- Ask for workflow descriptions, not abstractions
- Ask for failure modes and workarounds
- Keep queries vertical-agnostic in structure — the vertical comes from Step 1

Run each query through the chosen provider's API (from Step 0).

**Standard 3-query framework:**

Query 1 — **Workflow pain**: "What is the specific day-to-day workflow for [role] at [company type] when they [task we solve]? What tools do they use? Where do those tools fail? How long does each step take? Give concrete examples and data points."

Query 2 — **Tool/database gaps**: "How well do [existing tools] cover [target segment]? What percentage of the market do they miss? Why do [target companies] fall through the cracks? What data is wrong or stale? Give specific numbers."

Query 3 — **Scaling problems**: "What happens when [company type] tries to scale [process] beyond the initial [easy phase]? What breaks? What are the real-world failure stories? How do they work around it? What does it cost?"

**Optional Query 4 — Industry leaders and public statements**: "Who are the recognized thought leaders in [vertical]? What have they said publicly about [pain area] in the last 12 months? Include quotes, conference talks, blog posts, LinkedIn posts. Focus on practitioners, not analysts."

### Step 3: Distill into numbered hypothesis set

Read all research responses and extract distinct, non-overlapping pain points. Each hypothesis should be:

- **Specific**: tied to a concrete workflow step, tool failure, or scaling problem
- **Quantified**: includes at least one data point (hours, percentages, dollar amounts)
- **Verifiable**: the recipient can confirm it from their own experience
- **Non-obvious**: teaches them something they may not have measured

Format:

```markdown
## Hypothesis Set: [Vertical]

### #1 [Short name]
[2-3 sentence description with data points]
Best fit: [what type of company this applies to most]

### #2 [Short name]
...
```

Target: 5-7 hypotheses per vertical.

### Step 4 (optional): Industry Leaders

If Query 4 was run, compile an industry leaders section:

```markdown
## Industry Leaders: [Vertical]

### [Leader Name] — [Title, Company]
- **Public stance on [pain area]:** [summary of their position]
- **Key quote:** "[direct quote]" — [source, date]
- **Relevance:** [why this matters for outreach or positioning]
```

This section helps with:
- Email personalization (referencing what a leader said)
- Positioning (aligning with or contrasting industry voices)
- Content creation (informed takes on industry problems)

### Step 5: Save outputs

Save to the vertical context directory:

```
claude-code-gtm/context/{vertical-slug}/sourcing_research.md   — full research output
claude-code-gtm/context/{vertical-slug}/hypothesis_set.md      — distilled hypotheses
claude-code-gtm/context/{vertical-slug}/industry_leaders.md    — leaders section (if Query 4 ran)
```

Create the directory if it doesn't exist.

## Output Consumers

The hypothesis set is consumed by:
- `enrichment-design` — to design enrichment columns that score/confirm hypotheses
- `list-segmentation` — to match companies to hypotheses and assign tiers
- `email-generation` — to personalize P1 openers per hypothesis
- `email-response-simulation` — to evaluate whether email copy aligns with research

## Relationship to hypothesis-building

`hypothesis-building` generates hypotheses from your own knowledge (context file + user input) — fast, no API. This skill validates and enriches those hypotheses with external research. If a hypothesis set already exists at `claude-code-gtm/context/{vertical-slug}/hypothesis_set.md`, use it to focus research queries instead of starting from scratch.

Typical flow: `hypothesis-building` first (define what you think) → `market-research` (validate with data). Or skip this skill entirely if you know the vertical well.

## When NOT to Use This Skill

- If you already have a hypothesis set for the vertical — update it, don't recreate
- If you just need quick hypotheses from existing knowledge — use `hypothesis-building`
- If the user just wants to write emails — use `email-generation` skill
- If the user wants to find companies — use `list-building` skill
- If the user wants to enrich a table — use `list-enrichment` skill
- If the user wants to match companies to hypotheses — use `list-segmentation` skill
