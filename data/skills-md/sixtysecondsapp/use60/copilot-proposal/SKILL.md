---
name: Copilot Proposal
description: |
  Generate a tailored sales proposal from deal and company context with pricing options.
  Use when a user asks "/proposal", "write a proposal", "generate proposal", "draft a proposal
  for this deal", "create a proposal for [company]", or "put together a proposal".
  Pulls deal data, contact history, company intel, meeting transcript intelligence, competitive
  context, and org templates to produce a complete proposal with pricing table, ROI metrics,
  competitive positioning, and next steps. Requires a deal or company entity in context.
  Do NOT use for SOWs, contracts, or legal documents -- use proposal-generator for those.
metadata:
  author: sixty-ai
  version: "3"
  category: sales-ai
  skill_type: atomic
  is_active: true
  command_centre:
    enabled: true
    label: "/proposal"
    description: "Generate a tailored proposal from deal context"
    icon: "file-text"
  context_profile: sales
  agent_affinity:
    - pipeline
    - outreach
  triggers:
    - pattern: "/proposal"
      intent: "slash_proposal"
      confidence: 0.95
      examples:
        - "/proposal"
        - "/proposal for Acme"
        - "/proposal for this deal"
    - pattern: "write a proposal"
      intent: "create_proposal"
      confidence: 0.90
      examples:
        - "draft a proposal for this deal"
        - "create a proposal for this company"
        - "put together a proposal"
    - pattern: "generate proposal"
      intent: "generate_proposal"
      confidence: 0.90
      examples:
        - "generate a proposal"
        - "make me a proposal"
        - "build a proposal for this client"
  keywords:
    - "proposal"
    - "deal"
    - "pricing"
    - "pitch"
    - "offer"
    - "generate"
    - "quote"
    - "bid"
  requires_context:
    - deal
    - company
  inputs:
    - name: deal_id
      type: string
      description: "The deal identifier to pull context from"
      required: false
    - name: company_name
      type: string
      description: "Company name if no deal is linked"
      required: false
    - name: tone
      type: string
      description: "Tone: confident_partner, professional_advisor, or enterprise"
      required: false
    - name: template
      type: string
      description: "Template override if the user has a preferred format"
      required: false
    - name: proposal_stage
      type: string
      description: "discovery, evaluation, negotiation, or renewal -- selects template from references"
      required: false
  outputs:
    - name: proposal_content
      type: string
      description: "Complete formatted proposal in markdown with all sections"
    - name: pricing_table
      type: object
      description: "Structured pricing table with up to 3 tiers"
    - name: next_steps
      type: array
      description: "Recommended next steps with owners and deadlines"
    - name: pricing_rationale
      type: string
      description: "Why this pricing was chosen based on deal context and historical data"
    - name: competitive_positioning
      type: object
      description: "How proposal addresses competitive threats mentioned in meetings"
    - name: roi_metrics
      type: object
      description: "Quantified ROI estimates based on prospect's stated metrics"
    - name: personalization_signals
      type: array
      description: "Specific details from RAG/CRM used to personalize this proposal"
    - name: confidence_level
      type: string
      description: "high/medium/low -- confidence in proposal quality based on data availability"
  requires_capabilities:
    - crm
    - web_search
  priority: high
  tags:
    - sales
    - proposal
    - deal-closing
    - pipeline
    - pricing
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

## Instructions

You are executing the /proposal skill. Your job is to generate a tailored, persuasive sales proposal grounded in real deal intelligence -- not generic templates. Every claim, every number, every personalization must trace to a data source.

Consult `references/proposal-templates.md` for stage-specific templates (discovery, evaluation, negotiation, renewal) and annotated examples of strong and weak proposals.

Consult `references/pricing-strategy.md` for the 3-tier anchoring framework, discount guidelines, competitive pricing positioning, and objection response frameworks.

## The 5-Layer Intelligence Model

Work through these layers in order. Each layer enriches the next.

### Layer 1: Deal & Company Context

Collect all available CRM intelligence before writing anything:

1. **Fetch deal details**: `execute_action("get_deal", { id: deal_id })` -- stage, amount, contacts, custom fields, notes
2. **Fetch company info**: `execute_action("get_company_status", { company_name })` -- overview, industry, size, relationship health
3. **Fetch contact details**: `execute_action("get_contact", { id: primary_contact_id })` -- name, title, role, previous interactions
4. **Fetch meeting history**: Search for recent meetings with this company to extract pain points, requirements, and commitments
5. **Fetch activity timeline**: Recent emails, calls, and notes for tone and context clues
6. **Check client fact profiles**: Query `client_fact_profiles` for enriched company data (industry, funding, tech stack, competitors) if available

### Layer 2: Enrichment & Research

Expand beyond CRM with external intelligence:

1. **Web search for company context**: `executeWebSearch("{company_name} news funding announcements", 5)` -- recent events, growth signals, market position
2. **Web search for industry benchmarks**: `executeWebSearch("{company_name} industry {product_category} pricing benchmarks", 3)` -- what similar companies pay for similar solutions
3. **Contact enrichment**: If contact data is thin, use AI Ark or Apollo enrichment for deeper stakeholder profiles -- seniority, reporting lines, social presence
4. **Competitive landscape**: `executeWebSearch("{company_name} competitors alternatives to {your_product}", 3)` -- who else they might be evaluating

### Layer 3: Historical Context (via RAG)

Before writing, search meeting transcripts for deal-specific intelligence:

1. `"pricing discussions with {company}"` -- extract any quoted numbers, budget ranges, pricing concerns
2. `"pain points mentioned by {contact}"` -- use their exact words in the Executive Summary
3. `"commitments made to {company}"` -- ensure proposal aligns with promises made
4. `"ROI or business case for {company}"` -- quantify value in their terms
5. `"competitors mentioned by {contact}"` -- address competitive concerns proactively
6. `"timeline or urgency for {company}"` -- match proposal urgency to their stated deadlines

Use RAG results to populate `personalization_signals` output. Every transcript-sourced quote should include the meeting date for credibility.

### Layer 4: Intelligence Signals

Synthesize patterns from the data:

- **Deal health**: Stage velocity vs. average, engagement recency, multi-threading depth
- **Risk signals**: Stalled stage, pushed close date, quiet champion, new stakeholders late
- **Competitive positioning**: Reference Organization Context for competitors, differentiators, and value props that counter specific competitive threats
- **Win/loss patterns**: If org has historical win data for similar deal sizes or industries, reference what worked

### Layer 5: Proposal Strategy

Synthesize all layers into the proposal. Select the template from `references/proposal-templates.md` based on `proposal_stage` or inferred deal stage:
- **Discovery/early stage** -> Lightweight proposal, focused on understanding and next steps
- **Evaluation stage** -> Feature-rich, comparison tables, ROI analysis
- **Negotiation stage** -> Final pricing, SLAs, implementation timeline
- **Renewal/expansion** -> Account health, growth metrics, new opportunities

## Proposal Structure

### 1. Executive Summary (3-5 sentences)
- Lead with the CLIENT's problem using their exact words from meetings (cite RAG source)
- Reference specific pain points from transcripts and CRM notes
- State the proposed outcome in their language, quantified where possible

### 2. The Challenge
- Reflect back what the prospect told you in discovery -- use direct quotes from RAG
- Quantify the cost of inaction using metrics they mentioned
- Connect to industry benchmarks from web research

### 3. Proposed Solution
- Map ${company_name} offerings to their specific needs identified in Layers 1-3
- Break into phases if the engagement is complex
- Include timeline estimates aligned with any deadlines mentioned in meetings

### 4. Why ${company_name}
- 1-2 relevant case studies matching their industry or problem type from Organization Context
- Differentiators that counter the specific competitors they mentioned (Layer 3)
- Social proof: logos, testimonials, metrics from similar customers

### 5. ROI & Business Case
- Quantify value using the metrics THEY stated matter (from RAG or CRM)
- Include before/after projections based on similar customer outcomes
- Present as `roi_metrics` output

### 6. Pricing Table
- Present up to 3 tiers using anchoring -- highest first (see `references/pricing-strategy.md`)
- Each tier has clear deliverables and differentiation
- Pricing aligns with any budget ranges discussed in meetings (Layer 3)
- Include payment terms appropriate for their company type and deal size
- Document reasoning in `pricing_rationale` output

### 7. Next Steps
- 2-3 concrete actions with owners and deadlines
- Single clear CTA (schedule review, sign, reply YES)
- Urgency element based on real constraints from meetings (not manufactured)

## Pricing Table Format

Structure the `pricing_table` output as:
```json
{
  "tiers": [
    {
      "name": "Scale",
      "price": "$X",
      "includes": ["item1", "item2"],
      "best_for": "scenario description",
      "highlighted": false
    },
    {
      "name": "Growth",
      "price": "$Y",
      "includes": ["item1", "item2"],
      "best_for": "scenario description",
      "highlighted": true
    },
    {
      "name": "Starter",
      "price": "$Z",
      "includes": ["item1", "item2"],
      "best_for": "scenario description",
      "highlighted": false
    }
  ],
  "currency": "USD",
  "payment_terms": "50/50 or milestone-based",
  "rationale": "Why these tiers and prices were chosen"
}
```

## Tone Calibration

- **confident_partner**: Direct, first-person, treats client as an equal. For founders and business owners.
- **professional_advisor**: Warm but clear, uses analogies, avoids jargon. For non-technical buyers.
- **enterprise**: Formal, comprehensive, risk-aware. Includes compliance and SLA language. For procurement.

Default to the tone that matches the prospect's communication style from emails and meeting transcripts (Layer 3).

## Confidence Level Assessment

Set `confidence_level` based on data availability:
- **high**: RAG transcript data + CRM deal data + enrichment/web research all available. 3+ personalization signals sourced from meetings.
- **medium**: CRM deal data available but no RAG transcripts (or transcripts are sparse). Personalization based on CRM notes only.
- **low**: Minimal CRM data, no transcripts, no enrichment. Proposal relies heavily on templates and placeholders.

## Quality Checklist

Before returning:
- [ ] Opens with the CLIENT's problem using their exact words from meetings (cite RAG source)
- [ ] ROI/value quantified using metrics the prospect mentioned
- [ ] Competitive concerns addressed proactively (if competitor was mentioned in meetings)
- [ ] Pricing aligns with any budget ranges discussed in meetings
- [ ] At least 3 personalization signals from RAG/CRM data sourced in `personalization_signals`
- [ ] Social proof matches their industry or problem type
- [ ] Every next step has an owner and deadline
- [ ] Single clear CTA at the end
- [ ] No dead language ("synergies", "leverage", "streamline", "cutting-edge", "best-in-class")
- [ ] Confidence level reflects data quality (high if RAG + CRM, medium if CRM only, low if sparse)

## Error Handling

### No deal found
If no deal is linked, ask: "Which company or deal should I generate a proposal for?" Do not fabricate deal details.

### No pricing available
Use `[PRICE]` placeholders and recommend three tiers using the anchoring framework from `references/pricing-strategy.md`. Note: "Pricing placeholders included -- fill in your rates before sending."

### Missing RAG context
Proceed with CRM data only. Set `confidence_level` to "medium". Add to `personalization_signals`: "No meeting transcripts available -- recommend conducting discovery before sending."

### Missing competitive context
Generate proposal without competitive section. Add note: "No competitor mentions found in meetings -- consider adding competitive positioning if relevant."

### Conflicting data
If RAG transcripts contradict CRM data (e.g., different budget range), surface both with timestamps in the `pricing_rationale` and let the rep decide. Example: "CRM shows budget $50K (updated Jan 15) but Sarah mentioned $30-40K in the Dec 12 call. Verify before sending."

### Minimal context
If CRM data is sparse, ask the user to provide: the client's main pain points, what was discussed, their timeline, and budget range. Set `confidence_level` to "low". These are the minimum inputs for a strong proposal.

### Web search fails
Proceed without enrichment data. Note in output: "External research unavailable -- proposal based on CRM data only."
