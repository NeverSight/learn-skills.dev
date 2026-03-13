---
name: Feedback Analyzer
slug: feedback-analyzer
description: Analyze customer feedback to extract actionable insights, identify patterns, and prioritize improvements
category: customer-support
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "feedback analysis"
  - "customer feedback"
  - "sentiment analysis"
  - "voice of customer"
  - "feature requests"
  - "user feedback"
tags:
  - feedback
  - analytics
  - sentiment
  - voice-of-customer
  - customer-insights
---

# Feedback Analyzer

Expert customer feedback analysis system that transforms unstructured feedback into actionable product and service insights. This skill provides structured workflows for collecting, categorizing, analyzing, and acting on customer feedback from multiple sources.

Customer feedback is the most direct signal of what's working and what isn't. But raw feedback is noisy, contradictory, and overwhelming. This skill helps you extract patterns, prioritize themes, and close the feedback loop effectively.

Built on voice-of-customer best practices and qualitative research methods, this skill combines text analysis, pattern recognition, and stakeholder communication to turn feedback into action.

## Core Workflows

### Workflow 1: Feedback Collection & Aggregation
**Gather feedback from all sources into unified view**

1. **Feedback Sources**
   - **Direct Surveys**: NPS, CSAT, CES, custom surveys
   - **Support Channels**: Tickets, chat transcripts, calls
   - **In-App Feedback**: Feature requests, bug reports, ratings
   - **Social Media**: Mentions, reviews, comments
   - **Sales Conversations**: Objections, lost deal reasons
   - **User Research**: Interviews, usability tests
   - **Community**: Forums, Slack, Discord

2. **Data Standardization**
   | Field | Description |
   |-------|-------------|
   | Source | Where feedback came from |
   | Date | When received |
   | Customer ID | Link to customer record |
   | Segment | Customer type/tier |
   | Raw Text | Original feedback |
   | Category | Topic classification |
   | Sentiment | Positive/neutral/negative |
   | Priority | Urgency/impact level |

3. **Collection Automation**
   - API integrations with feedback tools
   - Automatic ticket tagging
   - Survey response routing
   - Social listening alerts
   - Scheduled data syncs

4. **Quality Filters**
   - Remove spam and duplicates
   - Flag potentially inaccurate data
   - Note context (e.g., during outage)
   - Weight by customer segment
   - Identify feedback loops (same issue, multiple channels)

### Workflow 2: Categorization & Tagging
**Organize feedback into meaningful categories**

1. **Category Taxonomy**
   - **Product Features**: Specific functionality feedback
   - **Usability/UX**: Interface and experience issues
   - **Performance**: Speed, reliability, bugs
   - **Pricing/Value**: Cost concerns and value perception
   - **Support Experience**: Service quality feedback
   - **Onboarding**: Getting started experience
   - **Documentation**: Help content feedback
   - **Integration**: Third-party connection issues

2. **Subcategory Examples**
   ```
   Product Features
   ├── Feature Requests
   │   ├── New feature ideas
   │   └── Feature enhancements
   ├── Missing Features
   │   ├── Competitor comparisons
   │   └── Workflow gaps
   └── Feature Feedback
       ├── What works well
       └── What doesn't work
   ```

3. **Tagging Best Practices**
   - Use consistent, specific tags
   - Allow multiple tags per feedback
   - Create tag hierarchy (parent/child)
   - Review and consolidate tags quarterly
   - Train team on tagging standards

4. **Automated Classification**
   - Keyword-based routing rules
   - ML-based topic classification
   - Sentiment detection
   - Priority scoring algorithms
   - Entity extraction (features, pages, actions)

### Workflow 3: Sentiment & Urgency Analysis
**Understand emotional context and priority**

1. **Sentiment Classification**
   | Sentiment | Indicators | Action Level |
   |-----------|------------|--------------|
   | Very Negative | Anger, threats to leave | Urgent escalation |
   | Negative | Frustration, complaints | Address in sprint |
   | Neutral | Suggestions, questions | Standard review |
   | Positive | Praise, appreciation | Share with team |
   | Very Positive | Advocacy, testimonial | Request case study |

2. **Urgency Scoring Factors**
   - Customer tier (enterprise = higher weight)
   - Revenue at risk
   - Frequency of same issue
   - Time sensitivity mentioned
   - Escalation history
   - Regulatory/compliance implications

3. **Trend Detection**
   - Volume spikes (sudden increase in topic)
   - Sentiment shifts (getting worse/better)
   - New issues emerging
   - Seasonal patterns
   - Release-correlated feedback

4. **Alert Triggers**
   - High-value customer escalation
   - Sentiment score below threshold
   - Issue volume exceeds normal
   - Churn-risk keywords detected
   - Security/privacy concerns

### Workflow 4: Pattern Recognition & Insights
**Extract actionable patterns from feedback mass**

1. **Quantitative Analysis**
   - Frequency by category
   - Trend over time
   - Segment distribution
   - Correlation with churn
   - Impact on NPS/CSAT

2. **Qualitative Analysis**
   - Representative quote extraction
   - Use case pattern identification
   - User journey mapping
   - Pain point articulation
   - Unmet need discovery

3. **Insight Synthesis**
   ```
   Insight Template:

   FINDING: [What the data shows]
   EVIDENCE: [Supporting data points and quotes]
   IMPACT: [Business/customer impact if unaddressed]
   RECOMMENDATION: [Suggested action]
   PRIORITY: [High/Medium/Low with rationale]
   ```

4. **Root Cause Analysis**
   - Group related feedback
   - Identify underlying causes
   - Map to user journey stages
   - Connect to product/process gaps
   - Distinguish symptoms from causes

### Workflow 5: Reporting & Action
**Communicate insights and drive improvements**

1. **Stakeholder Reports**
   | Audience | Focus | Frequency |
   |----------|-------|-----------|
   | Product | Feature requests, usability | Weekly |
   | Support | Training needs, process issues | Weekly |
   | Executive | Strategic themes, churn drivers | Monthly |
   | Engineering | Bugs, performance issues | Real-time |
   | Marketing | Positioning, messaging gaps | Monthly |

2. **Report Components**
   - Executive summary
   - Key metrics and trends
   - Top themes with supporting data
   - Representative customer quotes
   - Recommended actions
   - Open questions

3. **Feedback Loop Closure**
   - Track feedback → action connection
   - Communicate changes to customers
   - Measure impact of changes
   - Update customers on feature requests
   - Publish "You Asked, We Built" updates

4. **Action Prioritization**
   - Impact on retention/growth
   - Effort to address
   - Customer segment affected
   - Strategic alignment
   - Quick wins vs. long-term investments

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Import feedback | "Import feedback from [source]" |
| Categorize feedback | "Categorize feedback batch" |
| Analyze sentiment | "Run sentiment analysis on [data]" |
| Find patterns | "Identify patterns in feedback" |
| Generate report | "Create feedback report for [audience]" |
| Extract quotes | "Find quotes about [topic]" |
| Trend analysis | "Analyze feedback trends" |
| Segment analysis | "Compare feedback by segment" |
| Priority scoring | "Score feedback by priority" |
| Action tracking | "Track feedback to action" |

## Best Practices

### Collection
- Capture feedback at moments of truth
- Use consistent rating scales
- Include open-ended questions
- Don't over-survey (survey fatigue)
- Thank customers for feedback

### Categorization
- Create mutually exclusive categories
- Allow multi-tagging for complex feedback
- Review taxonomy quarterly
- Train team on consistent tagging
- Use automation for high-volume

### Analysis
- Look for patterns, not anecdotes
- Weight by customer segment value
- Consider feedback context
- Triangulate across sources
- Separate signal from noise

### Reporting
- Lead with insights, not data
- Use customer quotes strategically
- Connect to business impact
- Recommend specific actions
- Track what gets done

### Closing the Loop
- Communicate what you've heard
- Update on progress
- Thank specific contributors
- Measure impact of changes
- Celebrate wins publicly

## Analysis Frameworks

### Framework 1: Jobs-to-be-Done Lens
Analyze feedback through customer goals:
- What job is the customer trying to do?
- What's preventing success?
- What would "done" look like for them?
- How does our product help or hinder?

### Framework 2: Kano Model
Categorize feature feedback:
- **Basic**: Expected, causes dissatisfaction if missing
- **Performance**: More is better, linear satisfaction
- **Delighters**: Unexpected, causes delight if present
- **Indifferent**: No impact on satisfaction

### Framework 3: Impact/Effort Matrix
Prioritize actions:
```
High Impact
    │   Quick Wins    │   Major Projects
    │   (Do Now)      │   (Plan Carefully)
────┼─────────────────┼───────────────────
    │   Fill-ins      │   Thankless Tasks
    │   (Do If Time)  │   (Reconsider)
Low │                 │                  High
    └─────────────────┴───────────────────
                    Effort
```

### Framework 4: Customer Journey Mapping
Map feedback to journey stages:
1. Awareness & Discovery
2. Evaluation & Decision
3. Onboarding & Activation
4. Regular Usage
5. Growth & Expansion
6. Support & Recovery
7. Renewal & Advocacy

## Report Templates

### Weekly Product Feedback Summary
```markdown
# Feedback Summary: [Week]

## Key Numbers
- Total feedback received: [X]
- Sentiment breakdown: [+/neutral/-]
- Top category: [Category] ([%])

## This Week's Themes

### Theme 1: [Title]
[Brief description of pattern]
- Volume: [X] mentions
- Segments affected: [List]
- Representative quote: "[Quote]"
- Recommendation: [Action]

### Theme 2: [Title]
[Same format]

## Emerging Issues
- [New issue to watch]

## Positive Highlights
- "[Positive quote]" - [Customer]

## Actions from Last Week
- [Action taken] → [Result]
```

### Monthly Executive Report
```markdown
# Voice of Customer: [Month]

## Executive Summary
[2-3 sentences on key findings and business impact]

## Metrics
| Metric | This Month | Last Month | Trend |
|--------|------------|------------|-------|
| NPS | [Score] | [Score] | [↑↓] |
| CSAT | [Score] | [Score] | [↑↓] |
| Feedback Volume | [X] | [X] | [↑↓] |

## Strategic Themes

### 1. [Theme Name]
**Impact**: [Business impact if unaddressed]
**Evidence**: [Data summary]
**Recommendation**: [Strategic action]

### 2. [Theme Name]
[Same format]

## Competitive Intelligence
[What customers are saying about competitors]

## Customer Quotes
[3-5 impactful quotes with context]

## Recommended Actions
1. [Priority action with owner]
2. [Priority action with owner]

## Appendix
[Detailed data tables]
```

## Red Flags

- **Echo chamber**: Only hearing from vocal minority
- **Recency bias**: Overweighting recent feedback
- **Volume bias**: Prioritizing loudest over important
- **Missing segments**: Not hearing from key customers
- **Action gap**: Collecting but not acting
- **No closure**: Customers don't know they were heard
- **Stale categories**: Taxonomy doesn't match current product
- **Sentiment-only**: Missing nuance in analysis
