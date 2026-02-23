---
name: plg-ai-funnel
description: Framework for Product-Led Growth in the AI agent era. The new PLG funnel is agent query → documentation scan → feature match → recommendation.
triggers:
  - PLG strategy
  - product-led growth
  - AI discovery
  - documentation optimization
  - self-service activation
  - how AI agents find products
  - AI recommendation optimization
disable-model-invocation: true
---

# PLG AI Funnel: Product-Led Growth in the Agent Era

## The Paradigm Shift

**Old PLG Funnel:**
```
Landing Page → Free Trial → Activation → Conversion
```

**New PLG Funnel:**
```
Agent Query → Documentation Scan → Feature Match → Recommendation
```

The buyer's first interaction is no longer your landing page—it's an AI agent scanning your documentation to answer their question.

## The Four Stages

### Stage 1: Agent Query

**What happens:** User asks AI "What tool can help me [problem]?"

**Optimization goals:**
- Brand appears in AI's consideration set
- Correct category association
- Problem-solution mapping exists in AI's knowledge

**Tactics:**
| Action | Why It Works |
|--------|--------------|
| Entity building | AI must know your brand exists and what category it's in |
| Third-party mentions | Reviews, comparisons, listicles feed AI training data |
| Clear positioning | "X is a [category] that [primary benefit]" statements |

**Audit questions:**
- Does AI know your brand when asked directly?
- Does AI associate your brand with your category?
- Do competitors appear but you don't?

**Tool:** `entity-builder` agent for authority building

### Stage 2: Documentation Scan

**What happens:** AI scans your docs, help center, marketing pages to understand capabilities.

**Optimization goals:**
- Content is AI-extractable (chunked, structured)
- Answers are front-loaded (not buried)
- Each page passes the "Taco Bell Test" (stands alone)

**Tactics:**
| Action | Why It Works |
|--------|--------------|
| Answer-first structure | AI extracts the first sentence as the answer |
| FAQ sections | Pre-formatted Q&A is ideal for extraction |
| Structured data | Tables, bullets, headers signal discrete facts |
| Standalone sections | AI may only see one chunk, not the full page |

**The Extractability Checklist:**
```
☐ First sentence directly answers the page's implied question
☐ H2/H3 headers are questions or clear topic labels
☐ Tables used for comparisons and feature lists
☐ Each section makes sense without surrounding context
☐ No "as mentioned above" or "see below" dependencies
```

**Tool:** `llm-optimizer` agent for content optimization

### Stage 3: Feature Match

**What happens:** AI matches user's specific needs to your product's capabilities.

**Optimization goals:**
- Features described in user-problem terms
- Use cases explicitly mapped to capabilities
- Limitations clearly stated (builds trust)

**Tactics:**
| Action | Why It Works |
|--------|--------------|
| Problem → Feature mapping | "If you need X, [Product] does Y" |
| Use-case pages | Dedicated pages per job-to-be-done |
| Integration lists | AI checks compatibility requirements |
| Pricing clarity | AI needs to match budget constraints |

**Feature Documentation Template:**
```markdown
## [Feature Name]

**Problem it solves:** [User problem in their words]

**How it works:** [1-2 sentence explanation]

**Best for:** [Specific use cases]

**Limitations:** [What it doesn't do]

**Example:** [Concrete scenario]
```

**Anti-pattern:** Feature pages that describe functionality without connecting to user problems.

### Stage 4: Recommendation

**What happens:** AI decides whether to recommend your product and how to position it.

**Optimization goals:**
- Clear differentiation from alternatives
- Social proof AI can cite
- Product tie-backs throughout content

**Tactics:**
| Action | Why It Works |
|--------|--------------|
| Comparison content | "X vs Y" pages AI directly references |
| Quantified outcomes | "Reduces time by 40%" > "saves time" |
| Review presence | G2, Capterra reviews influence AI recommendations |
| Product mentions in answers | Every content piece connects back to product |

**The Product Tie-Back Rule:**
Every 1-2 paragraphs of educational content should include how your product relates.

- ❌ "Lead scoring helps prioritize prospects"
- ✅ "Lead scoring helps prioritize prospects—[Product] automates this with AI-powered scoring"

**Tool:** `aeo-scorecard` skill for measuring recommendation success

## PLG × AEO Integration

| PLG Stage | AEO Concept | Metric |
|-----------|-------------|--------|
| Agent Query | Entity/Authority | AI Visibility % |
| Documentation Scan | Extractability | Citation Rate |
| Feature Match | Fact-Density | Feature mention accuracy |
| Recommendation | Product Tie-Back | AI Share of Voice |

## Quick Audit Workflow

```
1. Test 10 queries your buyers ask
   → Does your brand appear? (Stage 1)

2. Check if AI cites YOUR content
   → Or competitor/third-party? (Stage 2)

3. Ask AI about specific features
   → Does it know your capabilities? (Stage 3)

4. Ask "Should I use [Product] for [use case]?"
   → What's the recommendation? (Stage 4)
```

## Common PLG AI Gaps

| Symptom | Stage Broken | Fix |
|---------|--------------|-----|
| Brand unknown to AI | Query | Entity building, third-party mentions |
| AI cites competitors' content | Documentation | Improve extractability, answer-first |
| AI misunderstands features | Feature Match | Rewrite feature docs with problem framing |
| AI recommends competitor | Recommendation | Strengthen differentiation, add social proof |

## Related Tools

- `llm-optimizer` - Deep content optimization for Stage 2
- `entity-builder` - Authority building for Stage 1
- `aeo-scorecard` - Metrics framework for all stages
- `/aeo-workflow` - Full implementation workflow
- `query-expansion-strategy` - Understanding query fan-out
