---
name: analyzing-customers
description: Analyzes customer behavior, needs, pain points, and sentiment through review mining, social listening, buyer persona development, and jobs-to-be-done framework. Use when the user requests customer analysis, voice of customer research, buyer personas, pain point analysis, or wants to understand customer needs and motivations.
---

# Analyzing Customers

This skill performs deep customer analysis using voice of customer research, review mining, sentiment analysis, and behavioral insights to understand customer needs, motivations, and pain points.

## When to Use This Skill

Invoke this skill when the user:
- Requests customer analysis or voice of customer research
- Wants to understand customer pain points and needs
- Asks for buyer persona development
- Needs sentiment analysis of customer feedback
- Mentions jobs-to-be-done analysis
- Wants to analyze customer reviews or feedback
- Asks about customer motivations or decision drivers
- Needs to understand customer journey or buying process

## Core Analysis Activities

### Review Mining and Sentiment Analysis

Extract insights from customer reviews:

**Steps:**
1. Identify review sources (G2, Capterra, TrustRadius, app stores, Amazon)
2. Search for product/category reviews using WebSearch
3. Collect reviews across rating spectrum (1-5 stars)
4. Extract common themes and patterns
5. Categorize feedback (features, support, usability, value, etc.)
6. Analyze sentiment (positive, negative, neutral)
7. Identify recurring pain points and praise
8. Quantify frequency of themes

**Output Format:**
```markdown
# Review Analysis: [Product/Category]

## Data Summary
- Reviews analyzed: ~[Number]
- Sources: [G2, Capterra, etc.]
- Date range: [Period]
- Average rating: X.X/5

## Sentiment Distribution
- Positive: XX%
- Neutral: XX%
- Negative: XX%

## Top Themes (by mention frequency)

### Positive Themes
1. **[Theme]** (mentioned in XX% of positive reviews)
   - Key quotes: "[Quote 1]", "[Quote 2]"
   - Insight: [What this tells us]

2. **[Theme]** (mentioned in XX% of positive reviews)
   - Key quotes: "[Quote 1]", "[Quote 2]"
   - Insight: [What this tells us]

### Negative Themes
1. **[Theme]** (mentioned in XX% of negative reviews)
   - Key quotes: "[Quote 1]", "[Quote 2]"
   - Impact: [How this affects customers]
   - Severity: [High/Medium/Low]

2. **[Theme]** (mentioned in XX% of negative reviews)
   - Key quotes: "[Quote 1]", "[Quote 2]"
   - Impact: [How this affects customers]
   - Severity: [High/Medium/Low]

## Feature Requests
Most requested features not yet available:
1. [Feature] - XX mentions
2. [Feature] - XX mentions

## Use Case Patterns
How customers actually use the product:
1. [Use case] - [Description]
2. [Use case] - [Description]

## Customer Segments in Reviews
- [Segment 1]: [What they value/complain about]
- [Segment 2]: [What they value/complain about]

## Actionable Insights
1. [Insight and recommendation]
2. [Insight and recommendation]
```

### Pain Point Analysis

Systematically identify and prioritize customer pain points:

**Steps:**
1. Gather pain point data from multiple sources (reviews, forums, social media, sales calls)
2. Categorize pain points by type (functional, emotional, financial, social)
3. Map pain points to customer journey stages
4. Assess pain severity and frequency
5. Identify unmet needs vs. underserved needs
6. Prioritize by impact and opportunity
7. Connect pain points to solution opportunities

**Output Format:**
```markdown
# Pain Point Analysis

## Critical Pain Points (High Severity × High Frequency)

### Pain Point 1: [Name]
- **Description:** [What the pain is]
- **Customer quote:** "[Direct quote from customer]"
- **Affected segment:** [Who experiences this]
- **Journey stage:** [When they experience it]
- **Current workarounds:** [How customers cope today]
- **Impact:** [Business/productivity/emotional impact]
- **Opportunity:** [How a solution could help]
- **Priority:** High

### Pain Point 2: [Name]
[Same structure]

## Moderate Pain Points (Medium priority)
[List with brief descriptions]

## Pain Point Categories

**Functional Pains:**
- Can't achieve desired outcome
- Solution is too slow/inefficient
- Too complex or error-prone

**Financial Pains:**
- Too expensive
- Hidden costs
- Poor ROI

**Emotional Pains:**
- Frustrating to use
- Anxiety-inducing
- Requires too much effort

**Social Pains:**
- Makes them look bad
- Not trusted by team
- Poor collaboration

## Pain Point Journey Map

```
Awareness → Consideration → Purchase → Onboarding → Usage → Renewal
    ↓            ↓             ↓           ↓          ↓         ↓
 [Pain A]    [Pain B]      [Pain C]    [Pain D]  [Pain E]  [Pain F]
```

## Opportunity Sizing
1. [Pain point] → Affects XX% of customers → $XXM opportunity
2. [Pain point] → Affects XX% of customers → $XXM opportunity
```

### Buyer Persona Development

Create detailed, research-backed buyer personas:

**Steps:**
1. Identify distinct customer segments
2. Research demographic and firmographic data
3. Analyze behavioral patterns and psychographics
4. Document goals, motivations, and success criteria
5. Map pain points and challenges
6. Identify information sources and influences
7. Understand decision-making process
8. Create narrative persona profiles

**Persona Template:**
```markdown
# Persona: [Persona Name]

## Profile Snapshot
- **Title/Role:** [Job title]
- **Industry:** [Primary industries]
- **Company Size:** [Employee count/revenue]
- **Experience Level:** [Years in role/field]
- **Age Range:** [If relevant]
- **Location:** [If relevant]

## Goals & Motivations
**Professional Goals:**
- [Goal 1]: [Why it matters]
- [Goal 2]: [Why it matters]

**Personal Motivations:**
- [Motivation 1]
- [Motivation 2]

**Success Metrics:**
- [How they measure success]
- [KPIs they care about]

## Pain Points & Challenges
**Top Challenges:**
1. [Challenge 1]: [Description and impact]
2. [Challenge 2]: [Description and impact]
3. [Challenge 3]: [Description and impact]

**Daily Frustrations:**
- [Frustration 1]
- [Frustration 2]

## Buying Behavior

**Decision Criteria:**
1. [Criterion 1] - [Priority level]
2. [Criterion 2] - [Priority level]
3. [Criterion 3] - [Priority level]

**Information Sources:**
- [Source 1: e.g., peer recommendations]
- [Source 2: e.g., industry blogs]
- [Source 3: e.g., analyst reports]

**Decision Process:**
- Decision-maker or influencer: [Role in decision]
- Typical buying cycle: [Duration]
- Key stakeholders involved: [List]
- Budget authority: [Yes/No/Shared]

**Objections & Concerns:**
- [Common objection 1]
- [Common objection 2]

## Technology & Tools
**Current Stack:**
- [Tool 1]
- [Tool 2]

**Tech Savviness:** [Low/Medium/High]

## Communication Preferences
- **Preferred channels:** [Email, phone, Slack, etc.]
- **Content preferences:** [Case studies, demos, technical docs]
- **Tone:** [Formal/casual, technical/business-focused]

## Quote
"[Representative quote that captures their perspective]"

## How to Reach Them
- Marketing channels: [Where they spend time]
- Messaging that resonates: [Key themes]
- Content to create: [Types and topics]

## Red Flags (Anti-Persona Indicators)
- [Indicator that this is NOT a good fit]
- [Indicator that this is NOT a good fit]
```

### Jobs-to-be-Done (JTBD) Analysis

Understand what customers are trying to accomplish:

**Steps:**
1. Identify the core "job" customers hire your product to do
2. Map functional, emotional, and social jobs
3. Document job context and triggers
4. Identify job steps and desired outcomes
5. Assess current solutions and alternatives
6. Find unmet needs in job execution
7. Prioritize job outcomes by importance and satisfaction

**JTBD Framework:**
```markdown
# Jobs-to-be-Done Analysis

## Core Job Statement
"When [situation], I want to [motivation], so I can [expected outcome]."

**Example:**
"When I need to share project updates with stakeholders, I want to quickly create visual reports, so I can keep everyone aligned without spending hours on formatting."

## Job Type Breakdown

### Functional Job (What task needs to be done)
- **Main job:** [Primary functional goal]
- **Related jobs:** [Connected tasks]
- **Success criteria:** [How they know it's done well]

### Emotional Job (How they want to feel)
- **Desired feelings:** [Confident, in control, respected]
- **Feelings to avoid:** [Anxious, incompetent, overlooked]

### Social Job (How they want to be perceived)
- **Desired perception:** [Competent, innovative, reliable]
- **Social context:** [Team, management, clients]

## Job Context

**When does this job arise?**
- Trigger: [What causes the need]
- Frequency: [How often]
- Duration: [How long it takes currently]
- Urgency: [Time sensitivity]

**Constraints:**
- Time: [Limitations]
- Resources: [Available tools/budget]
- Skills: [Required expertise]

## Job Steps & Outcomes

**Desired Outcomes at Each Step:**

1. **[Step name]**
   - Outcome: [What they want to achieve]
   - Current satisfaction: Low/Medium/High
   - Importance: Low/Medium/High
   - Opportunity: [Gap between importance and satisfaction]

2. **[Step name]**
   [Same structure]

## Current Solutions

**What do they use today?**
1. **[Solution 1]**
   - What it does well: [Strengths]
   - What it lacks: [Weaknesses]
   - Switching cost: [Barriers to change]

2. **[Solution 2]**
   [Same structure]

**Non-consumption:**
- % doing nothing: [XX%]
- Why: [Reasons for non-consumption]

## Unmet Needs

**Underserved Outcomes:**
(High importance, low satisfaction)
1. [Outcome]: [Description and opportunity]
2. [Outcome]: [Description and opportunity]

**Overserved Outcomes:**
(Low importance, high satisfaction - potential to simplify)
1. [Outcome]: [Description]

## Solution Implications

**Must-haves:**
- [Critical capability 1]
- [Critical capability 2]

**Differentiators:**
- [Unique approach to job outcome 1]
- [Unique approach to job outcome 2]

**Avoid:**
- [Overserving low-importance outcomes]
```

### Customer Journey Mapping

Map the end-to-end customer experience:

**Steps:**
1. Define journey scope (which journey to map)
2. Identify journey stages
3. Map customer actions at each stage
4. Document thoughts and emotions
5. Identify pain points and moments of delight
6. Note touchpoints and channels
7. Assess opportunities for improvement

**Journey Map Format:**
```markdown
# Customer Journey Map: [Journey Name]

## Journey Scope
- Persona: [Which customer type]
- Scenario: [Specific use case or goal]
- Timeframe: [Duration of journey]

## Stage 1: [Stage Name]

**Customer Actions:**
- [Action 1]
- [Action 2]

**Thoughts:**
- "[What they're thinking]"
- "[Concern or question]"

**Emotions:** [Happy/Neutral/Frustrated/Anxious]

**Touchpoints:**
- [Website, sales call, email, etc.]

**Pain Points:**
- [Pain 1]: Severity [High/Med/Low]
- [Pain 2]: Severity [High/Med/Low]

**Opportunities:**
- [Improvement opportunity]

---

## Stage 2: [Stage Name]
[Repeat structure]

---

## Journey Insights

**Moments of Truth:**
(Critical moments that make/break the experience)
1. [Moment]: [Why it's critical]
2. [Moment]: [Why it's critical]

**Drop-off Points:**
- [Stage]: XX% abandon → Why: [Reason]

**Delight Opportunities:**
- [Opportunity to exceed expectations]

**Quick Wins:**
- [Easy improvement with high impact]
```

## Research Methods

**Method 1: Review Platform Analysis**
- **Platforms:** G2, Capterra, TrustRadius, App Store, Google Play, Amazon
- **Approach:** Search and analyze recent reviews
- **Focus:** Themes, sentiment, feature requests
- **Tools:** WebSearch for review content

**Method 2: Social Listening**
- **Platforms:** Reddit, Twitter, LinkedIn, industry forums
- **Approach:** Search for product mentions and category discussions
- **Focus:** Unfiltered feedback, use cases, workarounds
- **Tools:** WebSearch with site-specific queries

**Method 3: Community Analysis**
- **Sources:** Product forums, Slack communities, Discord servers
- **Approach:** Identify common questions and issues
- **Focus:** Real-world usage patterns and problems
- **Value:** Authentic user voice

**Method 4: Sales/Support Conversation Mining**
- **Sources:** CRM notes, support tickets, call transcripts (if available)
- **Approach:** Extract patterns from customer conversations
- **Focus:** Objections, questions, use cases
- **Note:** May require user to provide this data

**Method 5: Survey Data Analysis**
- **Sources:** NPS surveys, customer satisfaction surveys
- **Approach:** Analyze quantitative scores and qualitative comments
- **Focus:** Satisfaction drivers and detractors
- **Note:** User may need to provide survey data

## Analysis Patterns

**Pattern 1: New Market Customer Research**
- **When:** Entering new market or launching new product
- **Approach:**
  1. Define target customer hypotheses
  2. Mine reviews of competitor/alternative products
  3. Analyze community discussions
  4. Develop initial personas
  5. Create JTBD framework
  6. Identify top pain points
- **Output:** Customer research brief with personas and JTBD

**Pattern 2: Product-Market Fit Assessment**
- **When:** Validating product-market fit
- **Approach:**
  1. Analyze review sentiment and themes
  2. Identify must-have vs. nice-to-have features
  3. Map pain points to product capabilities
  4. Assess job outcome satisfaction
  5. Calculate NPS/satisfaction proxies from reviews
- **Output:** PMF assessment with recommendations

**Pattern 3: Feature Prioritization Research**
- **When:** Deciding what to build next
- **Approach:**
  1. Mine feature requests from reviews
  2. Analyze pain points by frequency and severity
  3. Map to JTBD outcomes (importance vs. satisfaction)
  4. Assess competitive feature gaps
  5. Prioritize by customer impact
- **Output:** Prioritized feature opportunity list

**Pattern 4: Churn Risk Analysis**
- **When:** Understanding why customers leave
- **Approach:**
  1. Analyze negative reviews for churn signals
  2. Identify switching triggers
  3. Map to customer journey stages
  4. Assess competitive alternatives mentioned
  5. Recommend retention strategies
- **Output:** Churn driver analysis and mitigation plan

**Pattern 5: Segment-Specific Analysis**
- **When:** Understanding differences between customer segments
- **Approach:**
  1. Filter feedback by segment (enterprise vs. SMB, industry, etc.)
  2. Compare pain points across segments
  3. Analyze differing needs and priorities
  4. Create segment-specific personas
  5. Recommend segment strategies
- **Output:** Segment comparison and strategy recommendations

## Validation Checklist

Before completing customer analysis:

- [ ] Multiple data sources consulted
- [ ] Sufficient volume of feedback analyzed (50+ reviews/data points)
- [ ] Themes validated across sources
- [ ] Quantitative data (frequency, percentages) included
- [ ] Direct customer quotes included
- [ ] Personas based on real patterns, not assumptions
- [ ] JTBD statements validated against customer language
- [ ] Pain points prioritized by impact
- [ ] Actionable insights and recommendations provided
- [ ] Segment differences identified
- [ ] Journey map reflects actual customer experience

## Examples

**Example 1: Review Mining for SaaS Product**

Input: "Analyze customer reviews for project management software to understand pain points"

Process:
1. Search G2, Capterra for "project management software" reviews
2. Collect 100+ recent reviews across top products
3. Categorize feedback themes (ease of use, features, pricing, support)
4. Extract specific pain points and praise
5. Calculate theme frequency and sentiment
6. Identify feature gaps and requests
7. Develop actionable insights

Output: Comprehensive review analysis with top pain points, feature requests, sentiment breakdown, and product recommendations

**Example 2: Buyer Persona Development**

Input: "Create buyer personas for our DevOps monitoring tool"

Process:
1. Analyze reviews to identify distinct user types
2. Research job titles and roles in DevOps
3. Extract goals and challenges from feedback
4. Identify decision criteria and buying process
5. Map typical tech stack and environment
6. Document communication preferences
7. Create 2-3 distinct personas

Output: Detailed buyer personas with goals, pain points, buying behavior, and how to reach them

## Additional Notes

- Voice of customer research is ongoing, not one-time
- Review platforms may require filtering out fake/incentivized reviews
- Look for both stated needs (explicit) and latent needs (implicit)
- Combine quantitative data (ratings, frequency) with qualitative insights (quotes)
- Validate assumptions against real customer data
- Update personas regularly as market evolves
- Use direct customer language in insights and personas
- Combine with competitive-intelligence to understand why customers choose alternatives
- Link to analyzing-pricing to understand willingness to pay
