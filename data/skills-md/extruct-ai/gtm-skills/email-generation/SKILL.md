---
name: email-generation
description: >
  Generate cold outreach emails from a contact CSV and a self-contained prompt
  template. Campaign-agnostic — no hardcoded product or voice. The prompt
  template (from email-prompt-building skill) contains all voice rules, research data,
  value prop, proof points, and personalization rules. This skill just runs it.
  Triggers on: "generate emails", "email generation", "run emails", "create
  emails", "email pipeline", "generate outreach", "write emails for campaign".
---

# Email Generation

Generate cold outreach emails from a contact CSV + prompt template. The prompt template is self-contained — it has all voice, research, value prop, proof points, and personalization rules baked in. This skill just runs it per row.

## Architectural Principle

**This skill is a runner, not a reasoner.** All strategic reasoning (voice, value angles, proof points, research data) was done by the `email-prompt-building` skill at prompt-build time and embedded in the prompt template. This skill reads the prompt + CSV and generates emails. It does NOT read the context file, hypothesis set, or research files.

```
prompt template (.md) ─┐
                       ├──▶ generate email per row ──▶ emails CSV
contact CSV ───────────┘
```

## Inputs Required

| Input | Source | Required |
|-------|--------|----------|
| Contact CSV | File with recipient data + enrichment columns | yes |
| Prompt template | `.md` file from `email-prompt-building` skill | yes |

That's it. No context file, no hypothesis set, no research files.

### Contact CSV Columns

The prompt template specifies which columns it needs. Check the prompt's "Enrichment data fields" section for the expected column names. Common columns:

**Required (always):**
- `first_name`, `last_name`, `company_name`, `job_title`

**Enrichment (campaign-specific):**
Listed in the prompt template. If the prompt references a field that's not in the CSV, the email quality degrades. Check column alignment before running.

## Running the Generator

### Option A: In-chat generation (< 30 contacts)

1. Read the prompt template
2. Read the contact CSV
3. For each row, apply the prompt with the row's data and generate the email
4. Output as JSON per row, accumulate results
5. Save to output CSV

### Option B: Batch generation (30+ contacts)

Process in batches of 10-20 rows within the conversation:

1. Load the prompt template and contact CSV
2. Process contacts in batches
3. For each row, apply the prompt and generate the email JSON
4. Accumulate results and save to output CSV

**Output path:** `claude-code-gtm/csv/output/{campaign-slug}/emails.csv`

## Quality Checks

After generating, verify:
- [ ] Every email is within the word limit specified in the prompt
- [ ] No banned phrases from the prompt template appear
- [ ] Enrichment data was actually used — not just generic text
- [ ] Example queries in P2 are specific to each recipient's verticals
- [ ] Proof points vary across emails (not the same PS for everyone)
- [ ] Subject lines meet the prompt's length constraints

## Segmentation-Aware Generation

When the contact CSV includes segmentation data (from `list-segmentation`):

**Tier 1 companies:**
- Generate individually with full attention to enrichment data
- Route through `email-response-simulation` for review before sending

**Tier 2 companies:**
- Group by `hypothesis_number`
- Generate in batches within each hypothesis group
- Spot-check 2-3 from each group

**Tier 3 companies:**
- Do not generate emails
- Route back to `list-enrichment` or `list-building`

## In-Chat Refinement Loop

After generating, the user can refine:

1. User identifies emails they don't like
2. User says what to change
3. **Update the prompt template** (not just the individual email) — the fix should be systemic
4. Re-run the generator with updated prompt
5. Repeat until satisfied

Track changes made to the prompt so the user can see the evolution.

## Building a New Prompt Template

If no prompt template exists for this campaign, use the `email-prompt-building` skill to build one. That skill reads the context file and research, then synthesizes a self-contained prompt. Do not build prompts ad hoc in this skill.
