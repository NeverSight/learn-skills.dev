---
name: enrichment-design
description: >
  Design enrichment columns that bridge research hypotheses to list enrichment.
  Two modes: segmentation (columns that score hypothesis fit per company) and
  personalization (columns for company-specific hooks). Interactive column
  design with the user. Outputs ready-to-run column_configs for
  list-enrichment. Triggers on: "data points", "enrichment columns", "column
  design", "what to research", "data point builder", "build columns",
  "segmentation columns", "personalization columns".
---

# Data Points Builder

Bridge the gap between research hypotheses and table enrichment. Define WHAT to research about each company before running enrichment.

## When to Use

- After `market-research` has produced a hypothesis set
- Before `list-enrichment` — this skill designs the columns, that skill runs them
- When the user says "what should we research about these companies?"

## Two Modes

### Mode 1: Segmentation

**Goal:** Design columns that score or confirm hypothesis fit per company.

**Input:** Hypothesis set (from `market-research` or context file)

**Process:**
1. Read the hypothesis set
2. For each hypothesis, propose 1-2 columns that would confirm or deny fit
3. Discuss with user — refine, add, remove
4. Output final `column_configs`

**Example:** If hypothesis is "Database blind spot — 80-90% of targets invisible to standard tools":
- Column: "Data Infrastructure Maturity" (select: ["No CRM", "Basic CRM", "Full stack"])
- Column: "Digital Footprint Score" (grade: 1-5)

### Mode 2: Personalization

**Goal:** Design columns that capture company-specific hooks for email personalization.

**Input:** Target list + what the user wants to personalize on

**Process:**
1. Ask what hooks matter for this campaign (leadership quotes, recent launches, hiring signals, tech stack, etc.)
2. Propose 2-4 columns with prompts
3. Discuss with user — refine
4. Output final `column_configs`

**Example:** For personalization hooks:
- Column: "Recent Product Launch" (text: describe any product launched in last 6 months)
- Column: "Leadership Public Statement" (text: find a public quote from CEO/CTO about [topic])

## Interactive Column Design

Do NOT just generate columns silently. Walk through this with the user:

**Step 1: Present the framework**

Show the user the two modes and ask which applies (or both).

**Step 2: Propose initial columns**

Based on hypotheses or user input, propose 3-5 columns. For each, show:

```
Column: [name]
Type: [output_format]
Agent: [research_pro | llm]
Prompt: [the actual prompt text]
Why: [what this tells us for segmentation/personalization]
```

**Step 3: Refine together**

Ask:
- "Any columns to add?"
- "Any to remove or merge?"
- "Should any prompts be more specific?"

**Step 4: Confirm column budget**

Guidance:
- 3-5 columns is the sweet spot
- 6-7 is acceptable if each serves a clear purpose
- 8+ adds noise — push back and suggest merging

**Step 5: Output column_configs**

Generate the final column configs as a JSON array ready for `list-enrichment`:

```json
[
  {
    "kind": "agent",
    "name": "Column Display Name",
    "key": "column_key_snake_case",
    "value": {
      "agent_type": "research_pro",
      "prompt": "Research prompt using {input} for domain...",
      "output_format": "text"
    }
  }
]
```

## Column Design Guidelines

### Agent Type Selection

| Data point type | Agent type | Why |
|----------------|-----------|-----|
| Factual data from the web (funding, launches, news) | `research_pro` | Needs web research |
| Classification from company profile | `llm` | Profile data is enough |
| Nuanced judgment (maturity, fit score) | `research_reasoning` | Needs chain-of-thought |
| People/org structure | `linkedin` | LinkedIn-specific |

### Output Format Selection

| Data point type | Format | When |
|----------------|--------|------|
| Free-form research | `text` | Open-ended questions |
| Score/rating | `grade` | 1-5 scale assessments |
| Category | `select` | Mutually exclusive buckets |
| Multiple tags | `multiselect` | Non-exclusive tags |
| Structured data | `json` | Multiple related fields |
| Yes/no with evidence | `json` | `{"match": bool, "evidence": str}` |

### Prompt Writing Tips

- Always include `{input}` for the company domain
- Be specific about output format in the prompt itself
- Include fallback: "If not found, return N/A" or "If unclear, return 'Unknown'"
- For `select`/`multiselect`: list the labels in the prompt too
- For hypothesis scoring: reference the specific hypothesis in the prompt
- Keep prompts under 200 words

## Reference Library

See [references/data-point-library.md](references/data-point-library.md) for ~20 pre-built column configs organized by use case.

## Output Handoff

After column design is complete:
1. Present the final `column_configs` JSON to the user
2. Tell the user: "These configs are ready for `list-enrichment`. Run that skill with your table ID and these columns."
3. If the user wants to run immediately, hand off to `list-enrichment` workflow
