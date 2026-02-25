---
name: ai-personalization-prompts
description: 6 AI personalization prompts (lemlist style) plus 2 email templates - ICP Identification, Company Description, Similar Product, Top 3 Problems, Subject Line, Case Study Reference, and Similar Company Approach. Use when setting up AI-powered personalization, building Clay/lemlist workflows, or automating research.
---

# AI Personalization Prompts (lemlist Style)

Quick reference for AI prompts. For full prompts with rules, see [references/prompts.md](references/prompts.md).

## Prompt Overview

| # | Prompt | Output | Max Words |
|---|--------|--------|-----------|
| 1 | ICP Identification | Top 3 ICPs (job titles) | 3 titles |
| 2 | Company Description | Concise description | 8 words |
| 3 | Similar Product | Product category | 6 words |
| 4 | Top 3 Problems | ICP pain points | 10 words each |
| 5 | Subject Line | Email subject | 2 words |
| 6 | Case Study Reference | Template with variables | N/A |
| 7 | Similar Company Approach | Full email template | N/A |

## Quick Usage

**Inputs needed:** `{{companyDomain}}` or `{{companyDescription}}`

**Prompt 1-5:** Use for variable generation in Clay/lemlist
**Prompt 6-7:** Use as full email templates with AI-generated variables

## Output Examples

| Prompt | Input | Output |
|--------|-------|--------|
| ICP ID | "CRM software" | "Sales leaders, RevOps managers and AEs" |
| Description | "coldiq.com" | "outbound automation (for B2B sales teams)" |
| Similar | "calendly.com" | "scheduling software" |
| Problems | "HR software" | "slow hiring, poor retention, and compliance gaps" |
| Subject | "analytics platform" | "your metrics" |

## Key Rules (All Prompts)

- All lower case output
- No full stops at end
- No sales/buzzwords
- Must fit grammatically in template sentence

---

## Combines with

| Skill | Why |
|-------|-----|
| `clay-enrichment-9step` | Run prompts via Claygent |
| `personalization-6-buckets` | Know what data to feed prompts |
| `cold-email-templates-34` | Use outputs in email templates |
| `coldiq-messaging-templates` | Combine with case study template |

## Example prompts

```
Generate ICP identification and top 3 problems for a cybersecurity company.
```

```
Create a 2-word subject line for a prospect selling HR software.
```

```
Write template #7 (Similar Company Approach) with AI-generated variables for [company].
```
