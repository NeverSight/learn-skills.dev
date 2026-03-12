---
name: context-building
description: >
  Build and maintain a global company context file that all other GTM skills
  read from. Captures product info, voice rules, ICP, win cases, proof
  library, campaign history, hypotheses, and DNC lists. Supports four modes:
  create (new context), update (append to existing), call recording capture
  (extract signals from transcripts), and feedback loop (import campaign
  results). Triggers on: "company context", "update context", "build context",
  "ICP", "win cases", "campaign history", "call recording", "feedback loop",
  "DNC list".
---

# Company Context Builder

One global context file per company. Every other GTM skill reads from this file for voice, value prop, ICP, win cases, proof points, and campaign learnings.

## Context File Location

```
claude-code-gtm/context/{company}_context.md
```

Single file per company, not per-campaign. All skills reference this path.

## Modes

### Mode 1: Create

Use when no context file exists yet. Walk the user through each section.

**Step 1:** Check if `claude-code-gtm/context/{company}_context.md` exists.

**Step 2:** If not, ask the user for each section (one at a time or in bulk):

| Section | What to ask | Example |
|---------|------------|---------|
| What We Do | Product one-liner, core value prop, email-safe value prop, key lingo, key numbers | Product description + quantifiable claims |
| ICP | Customer profiles, company sizes, roles, geographies | Target profiles with size ranges and regions |
| Win Cases | Past customers, why they bought, what worked | Concrete outcomes with metrics |
| Proof Library | Pre-written PS sentences for emails, mapped to audience and hypothesis | Ready-to-paste proof points |
| Campaign History | Past campaigns: vertical, list size, reply rate, learnings | (empty on first run) |
| Active Hypotheses | Current working hypotheses about what resonates | Pain points validated by campaign data |

**Step 3:** Write the file using the schema from [references/context-schema.md](references/context-schema.md).

**Key sections to get right:**

**What We Do** — must include:
- Product one-liner
- Core value prop (internal version, can use any language)
- Email-safe value prop (outreach-friendly version of the value prop)
- Key numbers (quantifiable claims — database size, speed benchmarks, coverage stats)
- Key lingo (internal terms and definitions)

**Proof Library** — must include:
- Full PS sentences ready to paste into emails
- Each mapped to: best audience, best hypothesis, source win case
- Every proof point must trace back to a real win case
- Write the sentence as it would appear in the email (including "PS.")

### Mode 2: Update

Use when context file exists and user wants to add or modify a section.

**Step 1:** Read existing context file.

**Step 2:** Ask what to update. Common updates:
- Add a new win case
- Add a campaign result
- Update ICP based on new learnings
- Add domains to DNC
- Revise or add hypotheses
- Add or update proof points in the Proof Library
- Update voice rules
- Update key numbers (e.g., database size grew)

**Step 3:** Append to the relevant section. Never overwrite existing entries — add new rows to tables, new bullets to lists.

### Mode 3: Call Recording Capture

Use when the user pastes a call transcript or meeting notes.

**Step 1:** Read the transcript.

**Step 2:** Extract and categorize signals:
- **ICP signals** — who was on the call, their role, company size, what they care about
- **Win case data** — what resonated, what they said about their current workflow, pain points confirmed
- **Proof point candidates** — specific results or quotes that could become Proof Library entries
- **DNC signals** — any companies or domains mentioned as off-limits
- **Hypothesis validation** — which existing hypotheses were confirmed or refuted
- **Voice feedback** — any reaction to tone, language, or positioning that should update Voice rules

**Step 3:** Present extracted signals to the user for confirmation.

**Step 4:** Update the context file with confirmed signals.

### Mode 4: Feedback Loop

Use when importing campaign results from your email sequencer (e.g. Instantly) or manual tracking.

**Step 1:** Read campaign results (CSV, pasted data, or email sequencer export e.g. Instantly).

**Step 2:** Extract metrics:
- Campaign name, vertical, list size
- Open rate, reply rate, positive reply rate
- Top-performing hypotheses (which P1 angles got replies)
- Patterns in positive vs negative replies

**Step 3:** Add a new row to the `## Campaign History` table.

**Step 4:** Update `## Active Hypotheses` based on results:
- Promote hypotheses with high reply rates to Validated
- Demote hypotheses that didn't resonate to Retired
- Note any new hypotheses suggested by reply patterns

**Step 5:** Update `## Proof Library` if campaign results surfaced new proof points:
- New win cases → write new PS sentences
- Existing proof points that didn't resonate → add notes or remove

## Cross-Skill References

This context file is consumed by:
- `hypothesis-building` — reads ICP, Win Cases, and product value prop to generate pain hypotheses
- `email-prompt-building` — reads Voice, What We Do, Proof Library, and Active Hypotheses to build prompt templates
- `email-generation` — reads the prompt template (which was built from this file)
- `list-building` — reads ICP and Win Cases for seed companies
- `market-research` — reads ICP and hypotheses for research scope
- `enrichment-design` — reads hypotheses for segmentation column design
- `list-segmentation` — reads hypotheses for tiering logic
- `email-response-simulation` — reads Voice rules to constrain rewrites
- `campaign-sending` — reads DNC list for exclusions

## Reference

See [references/context-schema.md](references/context-schema.md) for the full file schema with all sections and field definitions.
