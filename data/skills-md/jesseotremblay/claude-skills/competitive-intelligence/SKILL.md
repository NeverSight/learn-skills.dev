---
name: competitive-intelligence
description: Monitors and analyzes competitors through systematic tracking of products, pricing, strategies, market positioning, and competitive moves. Use when the user requests competitor tracking, competitive analysis, win/loss analysis, feature comparison, or wants to monitor competitive landscape changes.
---

# Competitive Intelligence

This skill performs systematic competitive intelligence gathering and analysis to track competitors, understand their strategies, and identify competitive advantages.

## When to Use This Skill

Invoke this skill when the user:
- Requests competitor monitoring or tracking
- Wants detailed competitive analysis of specific companies
- Asks for feature comparison or product benchmarking
- Needs win/loss analysis insights
- Mentions competitive positioning or differentiation
- Wants to track competitor product launches or changes
- Asks about competitor strategies or tactics

## Core Intelligence Activities

### Competitor Profiling

Create comprehensive competitor profiles:

**Steps:**
1. Identify the competitor and verify company information
2. Research company background (founding, location, size, funding)
3. Analyze product/service portfolio
4. Document pricing and packaging
5. Examine go-to-market strategy (sales model, channels, partnerships)
6. Research key executives and leadership team
7. Identify competitive positioning and messaging
8. Track recent news, announcements, and changes

**Expected Output:**
```markdown
# Competitor Profile: [Company Name]

## Company Overview
- Founded: [Year]
- Headquarters: [Location]
- Size: [Employees, Revenue if public]
- Funding: [Total raised, Latest round]
- Status: [Private/Public, Growth stage]

## Products & Services
- [Product 1]: [Description, Target market]
- [Product 2]: [Description, Target market]

## Pricing Strategy
- Model: [Subscription, Usage-based, etc.]
- Tiers: [Pricing tiers and features]
- Positioning: [Value, Premium, or Budget]

## Go-to-Market
- Sales model: [Self-serve, Sales-led, Hybrid]
- Target customer: [SMB, Mid-market, Enterprise]
- Channels: [Direct, Partners, Resellers]
- Key partnerships: [List]

## Positioning & Messaging
- Core value prop: [Main claim]
- Key differentiators: [What they emphasize]
- Target use cases: [Primary scenarios]

## Recent Activity (Last 6 months)
- [Date]: [Event/announcement]
- [Date]: [Event/announcement]

## Strengths
- [Strength 1]
- [Strength 2]

## Weaknesses
- [Weakness 1]
- [Weakness 2]
```

### Feature Comparison Matrix

Systematic product feature benchmarking:

**Steps:**
1. Define feature categories to compare
2. Research each competitor's feature set
3. Verify features through multiple sources (website, docs, reviews)
4. Note feature depth/quality, not just presence
5. Identify unique features per competitor
6. Assess feature gaps and overlaps
7. Create structured comparison matrix

**Output Format:**
```
FEATURE COMPARISON MATRIX

Feature Category         | Your Product | Comp A | Comp B | Comp C
------------------------|--------------|--------|--------|--------
CORE FEATURES
├─ Feature 1            |      ✓✓      |   ✓    |   ✓✓   |   ✓
├─ Feature 2            |      ✓       |   ✓✓   |   ✗    |   ✓
└─ Feature 3            |      ✓✓      |   ✗    |   ✓    |   ✓

ADVANCED FEATURES
├─ Feature 4            |      ✓       |   ✓    |   ✗    |   ✗
├─ Feature 5            |      ✗       |   ✓✓   |   ✓    |   ✗
└─ Feature 6            |      ✓✓      |   ✗    |   ✗    |   ✗

INTEGRATIONS
├─ Integration 1        |      ✓       |   ✓    |   ✓    |   ✓
└─ Integration 2        |      ✓       |   ✗    |   ✓    |   ✗

Legend:
✓✓ = Full/Advanced implementation
✓  = Basic implementation
✗  = Not available

KEY INSIGHTS:
- Your unique features: [Feature 6]
- Competitor unique features: [Comp A: Feature 5]
- Table stakes: [Feature 1, Integration 1]
- Your gaps: [Feature 5]
- Market gaps: [No one offers X]
```

### Competitive Positioning Analysis

Understand how competitors position themselves:

**Steps:**
1. Collect competitor messaging (website, ads, sales materials)
2. Identify core value propositions for each competitor
3. Analyze target customer definitions
4. Extract key differentiators claimed
5. Review customer testimonials and case studies
6. Compare positioning against actual capabilities
7. Identify positioning patterns and white space

**Expected Output:**
- Positioning statement for each competitor
- Target customer analysis
- Claimed differentiators vs. reality
- Messaging themes and patterns
- Positioning gaps and opportunities

### Win/Loss Analysis Patterns

Analyze competitive dynamics in deals:

**Steps:**
1. Review competitive win/loss scenarios
2. Identify patterns in wins vs. losses
3. Analyze key decision criteria
4. Extract competitor strengths cited by customers
5. Note common objections or weaknesses
6. Document pricing/value considerations
7. Develop competitive battle cards

**Output Format:**
```markdown
# Win/Loss Analysis: [Competitor Name]

## Win Rate Against This Competitor
- Overall: XX%
- By segment: Enterprise XX%, SMB XX%
- By use case: [Use case] XX%

## Common Win Scenarios
**Scenario 1: [Name]**
- Customer profile: [Description]
- Why we won: [Reasons]
- Key differentiators: [What mattered]

## Common Loss Scenarios
**Scenario 1: [Name]**
- Customer profile: [Description]
- Why we lost: [Reasons]
- Competitor advantages: [What they offered]

## Key Decision Criteria
1. [Criterion 1]: We win XX% when this matters
2. [Criterion 2]: They win XX% when this matters
3. [Criterion 3]: Neutral factor

## Competitive Objections to Address
- "[Objection 1]" → Counter: [Response]
- "[Objection 2]" → Counter: [Response]

## Battle Card Recommendations
- Lead with: [Your strengths]
- Avoid competing on: [Their strengths]
- Ask discovery questions about: [Topics that favor you]
```

### Competitive Move Tracking

Monitor and analyze competitor actions:

**Steps:**
1. Set up monitoring for competitor news and updates
2. Track product launches and feature releases
3. Monitor pricing changes
4. Watch for partnership announcements
5. Track funding rounds and M&A activity
6. Analyze strategic pivots or repositioning
7. Assess impact and implications of moves

**Tracking Categories:**
- Product updates
- Pricing changes
- Leadership changes
- Funding/M&A
- Partnerships
- Market expansion
- Strategic pivots

## Intelligence Gathering Methods

**Method 1: Public Sources**
- **Sources:** Company websites, blogs, press releases, social media
- **Tools:** WebSearch, WebFetch
- **Approach:** Systematic monitoring of official channels
- **Frequency:** Weekly or as needed

**Method 2: Customer Feedback**
- **Sources:** Review sites (G2, Capterra, TrustRadius), forums, Reddit
- **Tools:** WebSearch for review aggregation
- **Approach:** Extract strengths/weaknesses from user reviews
- **Focus:** Look for recurring themes in feedback

**Method 3: Product Analysis**
- **Sources:** Product trials, documentation, demo videos
- **Tools:** Hands-on testing when possible
- **Approach:** Feature-by-feature comparison
- **Documentation:** Screenshots, notes, feature inventory

**Method 4: Market Intelligence**
- **Sources:** Industry analysts, reports, news coverage
- **Tools:** WebSearch for analyst mentions
- **Approach:** Third-party validation of positioning
- **Value:** Unbiased perspective on market position

**Method 5: Job Postings Analysis**
- **Sources:** Competitor career pages, LinkedIn jobs
- **Approach:** Infer strategy from roles they're hiring
- **Insights:** New market segments, product directions, tech stack
- **Example:** Hiring enterprise sales in new region = expansion signal

## Competitive Intelligence Patterns

**Pattern 1: New Competitor Deep Dive**
- **When:** New competitor enters your space
- **Approach:**
  1. Complete competitor profile
  2. Feature comparison matrix
  3. Positioning analysis
  4. Threat assessment (head-to-head overlap)
  5. Response strategy recommendations
- **Output:** Full competitive brief

**Pattern 2: Ongoing Competitive Monitoring**
- **When:** Regular competitive tracking
- **Approach:**
  1. Weekly news/updates scan
  2. Monthly product feature checks
  3. Quarterly strategic review
  4. Track changes over time
- **Output:** Competitive intelligence updates

**Pattern 3: Deal-Specific Competitive Analysis**
- **When:** Facing competitor in specific opportunity
- **Approach:**
  1. Pull competitor profile
  2. Review win/loss history
  3. Create battle card
  4. Prep competitive positioning
- **Output:** Sales enablement brief

**Pattern 4: Feature Parity Assessment**
- **When:** Competitor launches new feature
- **Approach:**
  1. Analyze new feature in depth
  2. Compare to your offering
  3. Assess customer impact
  4. Recommend response (build, ignore, counter-position)
- **Output:** Feature gap analysis and recommendation

**Pattern 5: Competitive Moat Analysis**
- **When:** Assessing long-term competitive position
- **Approach:**
  1. Identify each competitor's defensible advantages
  2. Assess switching costs they create
  3. Analyze network effects
  4. Evaluate proprietary assets (data, tech, brand)
  5. Compare to your moats
- **Output:** Competitive moat comparison

## Competitive Battle Card Template

```markdown
# Battle Card: [Competitor Name]

## Quick Reference
- **Primary Overlap:** [Where you compete most]
- **Their Strength:** [What they do best]
- **Our Advantage:** [How we win]
- **Win Rate:** XX%

## Company Overview
- Size: [Employees, funding, stage]
- Target market: [Who they focus on]
- Pricing: $X - $Y [per month/user/etc.]

## Head-to-Head Comparison

### Where We Win
1. **[Capability/Feature]**
   - Why it matters: [Customer impact]
   - Proof point: [Customer quote, metric]

2. **[Capability/Feature]**
   - Why it matters: [Customer impact]
   - Proof point: [Customer quote, metric]

### Where They Win
1. **[Capability/Feature]**
   - Why it matters: [Customer impact]
   - How to counter: [Positioning response]

2. **[Capability/Feature]**
   - Why it matters: [Customer impact]
   - How to counter: [Positioning response]

## Discovery Questions
Ask these to uncover fit issues with competitor:
- "[Question that reveals their weakness]"
- "[Question that highlights our strength]"

## Common Objections
**"They have [feature/capability we lack]"**
→ Response: [How to handle]

**"They're cheaper"**
→ Response: [How to handle]

## Pricing Comparison
| Tier | Competitor | Us | Notes |
|------|------------|-----|-------|
| Entry | $X | $Y | [Details] |
| Mid | $X | $Y | [Details] |
| Enterprise | $X | $Y | [Details] |

## Landmine Questions
Questions to ask that expose their weaknesses:
- "[Question]" → Likely reveals [issue]
- "[Question]" → Likely reveals [issue]

## Win Stories
**Recent win against them:**
"[Customer quote or story about why they chose you]"
- Customer: [Company name/industry]
- Key factor: [What made the difference]

## Key Takeaway
[One sentence on how to beat this competitor]
```

## Analysis Frameworks

**Framework 1: SWOT on Competitor**
- Strengths: What they do well
- Weaknesses: Where they fall short
- Opportunities: What they could do to improve
- Threats: What could hurt them (from your actions or market changes)

**Framework 2: 4 Ps Analysis**
- Product: Feature set and quality
- Price: Pricing strategy and positioning
- Place: Distribution channels and market coverage
- Promotion: Marketing and messaging strategy

**Framework 3: Value Chain Analysis**
- Where do they add most value?
- What activities do they excel at?
- Where are inefficiencies?
- Vertical integration vs. partnerships

## Information Sources Checklist

- [ ] Company website and product pages
- [ ] Pricing page (screenshot for historical tracking)
- [ ] Blog and announcement feeds
- [ ] Social media (LinkedIn, Twitter)
- [ ] Review sites (G2, Capterra, TrustRadius)
- [ ] Customer case studies and testimonials
- [ ] Press releases and news coverage
- [ ] Product documentation (if public)
- [ ] Demo videos or trial accounts
- [ ] Job postings
- [ ] Analyst reports (Gartner, Forrester)
- [ ] SEC filings (if public company)
- [ ] Patent filings
- [ ] Conference presentations

## Validation Checklist

Before completing competitive intelligence:

- [ ] Competitor information verified from multiple sources
- [ ] Recent activity captured (last 3-6 months)
- [ ] Feature comparison based on current product state
- [ ] Pricing information is current
- [ ] Strengths and weaknesses balanced and fair
- [ ] Sources cited and credible
- [ ] Actionable insights identified
- [ ] Competitive response options outlined
- [ ] Information organized for easy reference
- [ ] Battle cards created for key competitors

## Ethical Guidelines

**Do:**
- Use publicly available information
- Try competitors' products legitimately
- Analyze public reviews and feedback
- Attend public events and webinars
- Review published analyst reports

**Don't:**
- Misrepresent yourself to gain information
- Violate terms of service
- Engage in industrial espionage
- Share confidential information obtained improperly
- Spread misinformation about competitors

## Examples

**Example 1: Competitive Feature Gap Analysis**

Input: "Competitor just launched an AI-powered feature. How does it compare to ours?"

Process:
1. Search for competitor's announcement and documentation
2. Analyze feature capabilities and limitations
3. Compare to our existing offering
4. Test if possible or review demos
5. Assess customer impact and demand
6. Evaluate technical implementation
7. Recommend response (build, counter-position, ignore)

Output: Feature analysis with comparison matrix, customer impact assessment, and strategic recommendation

**Example 2: New Market Entrant Analysis**

Input: "New startup just raised $50M in our space. What's their strategy?"

Process:
1. Research company background and founding team
2. Analyze funding announcement and investor thesis
3. Review product positioning and features
4. Identify target market and GTM strategy
5. Compare to our offering and positioning
6. Assess competitive threat level
7. Recommend monitoring or response strategy

Output: Competitor profile with threat assessment and recommended actions

## Additional Notes

- Competitive intelligence is ongoing, not one-time
- Update competitor profiles quarterly at minimum
- Track changes over time to spot strategic shifts
- Combine with market-mapping skill to visualize competitive landscape
- Use researching-markets skill for broader industry context
- Focus on actionable insights, not just information collection
- Keep battle cards updated based on win/loss learnings
- Share insights cross-functionally (sales, product, marketing)
