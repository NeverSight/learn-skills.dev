---
name: list-segmentation
description: >
  Take an enriched Extruct table and a hypothesis set, then segment companies
  by hypothesis fit and assign tiers based on data richness and signal strength.
  Outputs a tiered, segmented list ready for email generation. Triggers on:
  "segment", "tier", "segment companies", "tier companies", "prioritize list",
  "segment and tier", "tiering", "which companies first".
---

# Segment and Tier

Take an enriched table + hypothesis set and produce a tiered, segmented list. This decides WHO gets which message and in what order.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Enriched table | Extruct table ID (after `list-enrichment`) | yes |
| Hypothesis set | `claude-code-gtm/context/{vertical-slug}/hypothesis_set.md` or context file | yes |
| Context file | `claude-code-gtm/context/{company}_context.md` | recommended |

## Environment

| Variable | Service |
|----------|---------|
| `EXTRUCT_API_TOKEN` | Extruct API |

Before making API calls, check that `EXTRUCT_API_TOKEN` is set by running `test -n "$EXTRUCT_API_TOKEN" && echo "set" || echo "missing"`. If missing, ask the user to provide their Extruct API token and set it via `export EXTRUCT_API_TOKEN=<value>`. Do not proceed until confirmed.

Base URL: `https://api.extruct.ai/v1`

## Official API Reference

- https://www.extruct.ai/docs

## Workflow

### Step 1: Load data

Fetch enriched table data via `GET /tables/{table_id}/data`. Parse all rows and their enrichment column values.

Read the hypothesis set file. Parse each hypothesis into:
- Number and short name
- Description with data points
- Best-fit company type

### Step 2: Match companies to hypotheses

For each company row, evaluate which hypothesis fits best. Consider:

1. **Enrichment data alignment** — do the enrichment column values match the hypothesis's "best fit" description?
2. **Signal strength** — how many enrichment columns have useful data (not N/A)?
3. **Specificity** — does the company's profile match the hypothesis narrowly or broadly?

Assign each company ONE primary hypothesis. If multiple fit, pick the strongest signal.

**Decision framework:**

```
For each company:
  1. Read all enrichment values
  2. For each hypothesis:
     - Does the company's vertical/industry match the "best fit"?
     - Do enrichment values confirm the hypothesis pain point?
     - Is there a specific data point that makes this hypothesis resonate?
  3. Pick the hypothesis with the strongest evidence
  4. If no hypothesis fits well, mark as "Unmatched"
```

### Step 3: Assign tiers

Three tiers based on fit strength and data richness:

| Tier | Criteria | Action |
|------|----------|--------|
| **Tier 1** | Strong hypothesis fit + data-rich (3+ enrichment fields populated) + clear hook signal | Personalized email via `email-response-simulation` review |
| **Tier 2** | Medium hypothesis fit OR data-rich but no clear hook | Standard templated email via `email-generation` |
| **Tier 3** | Weak fit OR missing data (2+ fields N/A) OR unmatched hypothesis | Hold for re-enrichment or different campaign |

**Tier 1 signals (any of these):**
- CEO/leadership made a public statement related to the hypothesis
- Recent news directly relevant to the pain point
- Hiring for roles that signal the hypothesis pain
- High hypothesis fit score from enrichment (grade 4-5)

**Tier 3 signals (any of these):**
- Most enrichment fields returned N/A
- No hypothesis match above threshold
- Company profile too generic to confidently segment

### Step 4: Generate output

Output a segmented list in two formats:

**Markdown table (for review):**

```markdown
## Segmented List: [Campaign Name]

### Tier 1 — [N] companies (personalized outreach)

| Company | Domain | Hypothesis | Tier Rationale | Hook Signal |
|---------|--------|-----------|----------------|-------------|
| [name] | [domain] | #[N] [name] | [why this tier] | [specific hook] |

### Tier 2 — [N] companies (templated outreach)

| Company | Domain | Hypothesis | Tier Rationale |
|---------|--------|-----------|----------------|
| [name] | [domain] | #[N] [name] | [why this tier] |

### Tier 3 — [N] companies (hold/re-enrich)

| Company | Domain | Issue |
|---------|--------|-------|
| [name] | [domain] | [what's missing] |
```

**CSV (for email-generation):**

Save to `claude-code-gtm/csv/input/{campaign-slug}/segmented_list.csv` with columns:
- `company_name`, `domain`, `tier`, `hypothesis_number`, `hypothesis_name`, `tier_rationale`, `hook_signal`

### Step 5: Review with user

Present summary stats:
- Total companies: N
- Tier 1: N (X%)
- Tier 2: N (X%)
- Tier 3: N (X%)
- Unmatched: N

Ask:
- "Does the tier distribution look right? (Typical: 10-20% Tier 1, 50-60% Tier 2, 20-30% Tier 3)"
- "Any companies that should move tiers?"
- "Ready to proceed to `email-generation`?"

## Reference

See [references/tiering-framework.md](references/tiering-framework.md) for the detailed tiering decision matrix.
