---
name: Copilot Objection
description: |
  Surface past objection handling and draft a response to a sales objection using the ACE framework.
  Use when a user asks "/objection", "handle objection", "objection response", "how do I respond
  to [objection]", "they said [objection]", "overcome this objection", or "counter this pushback".
  Searches meeting transcripts via RAG for past objection patterns, researches competitor claims
  and proof points via web search, and synthesizes a tailored response grounded in real data.
  Requires a contact or deal entity plus the objection text.
  Do NOT use for general competitive analysis -- use competitor-intel for that.
metadata:
  author: sixty-ai
  version: "3"
  category: sales-ai
  skill_type: atomic
  is_active: true
  command_centre:
    enabled: true
    label: "/objection"
    description: "Handle an objection with proof and past responses"
    icon: "shield"
  context_profile: sales
  agent_affinity:
    - pipeline
    - outreach
  triggers:
    - pattern: "/objection"
      intent: "slash_objection"
      confidence: 0.95
      examples:
        - "/objection"
        - "/objection too expensive"
        - "/objection they want to stay with incumbent"
    - pattern: "handle objection"
      intent: "handle_objection"
      confidence: 0.90
      examples:
        - "how do I handle this objection"
        - "help me handle their pushback"
        - "objection handling"
    - pattern: "objection response"
      intent: "objection_response"
      confidence: 0.90
      examples:
        - "how should I respond to this objection"
        - "what do I say when they say it's too expensive"
        - "counter this objection"
  keywords:
    - "objection"
    - "pushback"
    - "concern"
    - "overcome"
    - "counter"
    - "response"
    - "handle"
    - "too expensive"
    - "competitor"
  requires_context:
    - contact
    - deal
  inputs:
    - name: objection_text
      type: string
      description: "The objection or pushback from the prospect, in their words"
      required: true
    - name: deal_id
      type: string
      description: "The deal context for tailoring the response"
      required: false
    - name: contact_id
      type: string
      description: "The contact who raised the objection"
      required: false
    - name: objection_category
      type: string
      description: "Category override: price, timing, competition, authority, need, trust, status_quo"
      required: false
  outputs:
    - name: past_handling
      type: array
      description: "Previous instances of similar objections with how they were handled and outcome"
    - name: suggested_response
      type: string
      description: "Tailored ACE-framework response addressing this specific objection in context"
    - name: proof_points
      type: array
      description: "Supporting evidence: case studies, metrics, testimonials, and data points"
    - name: objection_pattern
      type: object
      description: "Frequency, trend, and correlation with win/loss across all deals for this objection type"
    - name: confidence_level
      type: string
      description: "high/medium/low based on data richness across all 5 layers"
    - name: alternative_responses
      type: array
      description: "2 alternative response approaches for different buyer personas"
    - name: follow_up_strategy
      type: object
      description: "What to do if the initial response doesn't land -- second move, escalation, channel switch"
  requires_capabilities:
    - crm
    - web_search
  priority: high
  tags:
    - sales
    - objection
    - negotiation
    - coaching
    - pipeline
    - rag
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

## Instructions

You are executing the /objection skill. Your job is to help a sales rep handle a prospect objection by surfacing how similar objections were handled in the past, researching proof points, analyzing objection patterns, and drafting a tailored, confident response grounded in real data.

Consult `references/objection-playbooks.md` for the ACE framework deep dive with worked examples across all 7 objection categories, bridge question library, "do not say" library, and multi-turn objection handling strategies.

Consult `references/proof-point-library.md` for the proof point taxonomy, construction frameworks, industry-specific selection guides, ROI calculation frameworks, and guidance on when proof points backfire.

## The 5-Layer Intelligence Model

Work through these layers in order. Each layer enriches the next.

### Layer 1: Contact & Deal Context

Collect core intelligence before anything else:

1. **Parse the objection**: Classify into a category (see Objection Taxonomy below)
2. **Fetch deal context**: `execute_action("get_deal", { id: deal_id })` -- stage, amount, competitive situation, close date
3. **Fetch contact context**: `execute_action("get_contact", { id: contact_id })` -- role, seniority, previous concerns, communication style
4. **Fetch recent activities**: Last 30 days of meetings, emails, calls involving this contact
5. **Fetch organization playbook**: Check Organization Context for objection handling frameworks, approved responses, and case studies

### Layer 2: Enrichment (Web Search)

Expand beyond CRM with external intelligence relevant to the objection category:

1. **Competitor claims** (for competition objections): `executeWebSearch("{competitor_name} vs {your_product} reviews comparison", 5)` -- find real claims to counter
2. **Industry benchmarks** (for price objections): `executeWebSearch("{prospect_industry} {product_category} pricing benchmarks ROI", 3)` -- market-rate validation
3. **Proof points** (all categories): `executeWebSearch("{your_product} customer results {prospect_industry}", 3)` -- case studies and testimonials
4. **Market context** (for timing/need objections): `executeWebSearch("{prospect_industry} trends challenges 2025 2026", 3)` -- urgency signals

Only run searches relevant to the objection category. Price objections need benchmarks. Competition objections need competitor intel. Do not run all four for every objection.

### Layer 3: Historical Context (via RAG)

Before drafting, search meeting transcripts for objection-specific intelligence:

1. `"objections raised by {contact}"` -- past objections from this specific person
2. `"objection about {category} from {company}"` -- similar objections from the same account
3. `"how {category} objection was handled"` -- successful responses across all deals
4. `"{competitor_name} mentioned by"` -- competitor claims surfaced in meetings (for competition objections)
5. `"pricing concerns in {prospect_industry}"` -- industry-specific objection patterns

Use RAG results to:
- Surface how this exact contact has objected before (recurring patterns)
- Find responses that led to won deals vs. lost deals
- Quote specific language from past successful rebuttals
- Identify whether this objection correlates with deal outcomes

If RAG returns no results, proceed with CRM + web data and note the gap in `confidence_level`.

### Layer 4: Intelligence Signals

Analyze patterns across the data to detect:

- **Objection frequency**: How often does this objection type appear across all deals? Is it trending up?
- **Win/loss correlation**: Do deals with this objection type close at a higher or lower rate? What differentiates wins from losses?
- **Contact pattern**: Has this contact raised this objection before? Is it a habitual concern or a new signal?
- **Deal health context**: Is this objection appearing in a healthy deal (buying signal) or a stalling deal (exit signal)?
- **Competitive signal**: If competition-related, is this a real evaluation or a negotiation tactic?

Populate `objection_pattern` output with these findings.

### Layer 5: Response Strategy (Synthesis)

Synthesize all layers into the ACE response. Select the response approach from `references/objection-playbooks.md` based on:
- Objection category (Layer 1)
- External proof points available (Layer 2)
- Past handling success/failure (Layer 3)
- Pattern intelligence (Layer 4)

## Objection Taxonomy

Classify every objection into one of these categories:

| Category | Signal Phrases | Core Concern |
|----------|---------------|--------------|
| **Price** | "too expensive", "over budget", "cheaper alternative", "can't justify the cost" | Value not demonstrated relative to cost |
| **Timing** | "not the right time", "next quarter", "too busy", "other priorities" | Urgency not established |
| **Competition** | "we're looking at [competitor]", "incumbent does this", "why switch" | Differentiation unclear |
| **Authority** | "need to check with my boss", "not my decision", "need board approval" | Decision process unknown or unnavigated |
| **Need** | "we're fine as is", "don't see the need", "not a priority" | Pain not sufficiently uncovered |
| **Trust** | "we've been burned before", "too risky", "unproven", "what if it fails" | Risk not mitigated |
| **Status Quo** | "we've always done it this way", "change is hard", "team won't adopt" | Change management concerns |

## Output Structure

### 1. Objection Pattern Analysis

Populate `objection_pattern`:
```json
{
  "category": "price | timing | competition | authority | need | trust | status_quo",
  "frequency": "How often this objection appears across all deals (e.g., '23% of deals')",
  "trend": "increasing | stable | decreasing over last 90 days",
  "win_rate_with_objection": "Win rate for deals where this objection was raised",
  "win_rate_without": "Win rate for deals without this objection (comparison)",
  "top_winning_response": "Summary of the response pattern that correlates with wins"
}
```

### 2. Past Handling

Search across meeting transcripts and CRM notes for similar objections. For each match:
```json
{
  "date": "When the objection was raised",
  "deal_name": "Which deal",
  "objection_verbatim": "What the prospect said",
  "rep_response": "How the rep responded",
  "outcome": "won | lost | pending",
  "effectiveness": "high | medium | low",
  "lesson": "What worked or didn't work"
}
```

If no past handling is found, note: "No similar objections found in your meeting history. The response below is based on sales best practices, web research, and your Organization Context."

### 3. Suggested Response (ACE Framework)

Draft using the ACE framework. See `references/objection-playbooks.md` for category-specific worked examples.

**A - Acknowledge** (1-2 sentences): Validate the concern without agreeing with it. Show empathy. Never dismiss.

**C - Contextualize** (2-3 sentences): Reframe using their stated goals and data from Layers 1-3. Reference their own words from transcripts. Include ROI calculations or comparative analysis from web research (Layer 2).

**E - Evidence** (1-2 proof points): Select from `references/proof-point-library.md`. Prioritize proof points from their industry, matching their concern, with specific numbers.

Close with a **bridge question** from `references/objection-playbooks.md` that moves the conversation forward.

### 4. Alternative Responses

Populate `alternative_responses` with 2 alternatives:
- **For analytical buyers**: Data-heavy, ROI-focused, comparison tables
- **For relationship buyers**: Story-driven, peer testimonials, risk-reduction framing

### 5. Follow-up Strategy

Populate `follow_up_strategy`:
```json
{
  "if_response_lands": "Next step to advance the deal",
  "if_objection_persists": "Second-move strategy from references/objection-playbooks.md",
  "escalation_trigger": "When to involve manager, reference customer, or technical expert",
  "channel_switch": "When to move from email to call, or bring in a different stakeholder"
}
```

### 6. Proof Points

For each proof point, structure per `references/proof-point-library.md`:
```json
{
  "type": "case_study | metric | testimonial | data_point | comparison | analyst_quote",
  "content": "The proof point content",
  "source": "Where this comes from (Organization Context, CRM, web search, public data)",
  "relevance": "Why this matters for THIS specific objection",
  "strength": "high | medium | low -- based on specificity and source credibility"
}
```

## Response Tone Guidelines

- **Never be defensive.** Objections are buying signals -- the prospect is engaged enough to push back.
- **Never dismiss.** "That's not really a concern" kills trust instantly.
- **Never oversell.** Overpromising to overcome an objection leads to churn.
- **Be direct.** If the objection is valid (e.g., you genuinely lack a feature), acknowledge it honestly and position it.
- **Be curious.** Follow up with questions that uncover the real concern behind the stated objection. The first objection is rarely the real one.

## Confidence Level

Set `confidence_level` based on data richness:

| Level | Criteria |
|-------|----------|
| **high** | CRM data + RAG transcript results + web research proof points + past handling with outcomes |
| **medium** | CRM data present but RAG returned sparse results, or web search added context but no past handling found |
| **low** | Sparse CRM data, no transcripts, no web research results. Response based on playbook templates only |

Always report honestly. A low-confidence response with clear disclaimers is better than a fabricated high-confidence one.

## Quality Checklist

Before returning:
- [ ] Objection is correctly categorized with signal phrases identified
- [ ] Response uses the full ACE framework (Acknowledge, Contextualize, Evidence)
- [ ] Response references the prospect's specific situation, not generic handling
- [ ] Proof points are relevant to their industry and concern, with source cited
- [ ] Response ends with a bridge question that moves the conversation forward
- [ ] Tone is empathetic and confident, not defensive
- [ ] Past handling examples include outcomes (won/lost) for credibility
- [ ] No competitor bashing -- only differentiation
- [ ] Objection pattern analysis populated with frequency and trend data
- [ ] Confidence level reflects actual data quality across all layers

## Graceful Degradation

When data is missing, degrade gracefully -- never block the response:

| Missing Data | Fallback |
|-------------|----------|
| No RAG results | Use CRM notes + web research; set confidence to medium; note "first interaction or data gap" |
| No deal linked | General category response; omit deal-specific framing; ask user to link a deal for tailored version |
| No contact context | Skip persona-matching for alternatives; use category defaults from playbooks |
| Web search fails | Proceed with CRM + RAG data only; note in output: "External research unavailable" |
| No past handling found | Use playbook templates from references/; note "no historical data for this objection type" |
| Objection is ambiguous | Ask user for the prospect's exact words before generating response |
| Multiple categories detected | Classify primary and secondary; address primary in main response, secondary in alternatives |

## Error Handling

### Objection text is vague
If the objection is too vague to classify (e.g., "they're not interested"), ask: "Can you share what the prospect actually said? The exact words help me find the best response."

### No deal or contact context
Generate a general response based on the objection category. Note: "Without deal context, this is a general response. Link a deal or contact for a tailored version that references their specific situation."

### Objection is actually a rejection
If the objection signals a hard no (e.g., "We've signed with [competitor]" or "We're canceling the evaluation"), acknowledge it honestly. Do not try to overcome a closed decision. Suggest a graceful exit strategy that preserves the relationship for future opportunities.

### Conflicting data
If RAG transcripts contradict CRM data (e.g., different competitor mentioned), surface both with timestamps and let the rep decide. Example: "CRM shows competitor is Vendor A (updated Jan 15) but Sarah mentioned evaluating Vendor B in the Dec 12 call. Verify which is the active threat."
