---
name: NPS Survey Creator
slug: nps-survey-creator
description: Create, deploy, and analyze Net Promoter Score surveys to measure customer loyalty
category: customer-support
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "nps"
  - "net promoter score"
  - "customer loyalty"
  - "promoter survey"
  - "customer satisfaction survey"
  - "loyalty measurement"
tags:
  - nps
  - surveys
  - customer-loyalty
  - metrics
  - customer-success
---

# NPS Survey Creator

Expert Net Promoter Score survey system that helps you measure, analyze, and act on customer loyalty data. This skill provides structured workflows for designing effective NPS programs, analyzing responses, and turning feedback into action.

NPS is the gold standard for measuring customer loyalty and predicting growth. But the score itself is just the beginning - the real value is in understanding the "why" behind the number and taking action. This skill helps you build an NPS program that drives improvement, not just measurement.

Built on customer research best practices and NPS methodology, this skill combines survey design, statistical analysis, and closed-loop processes to maximize the value of every response.

## Core Workflows

### Workflow 1: NPS Program Design
**Set up a comprehensive NPS measurement system**

1. **Survey Type Selection**
   | Type | When to Use | Timing |
   |------|-------------|--------|
   | Relationship NPS | Overall brand loyalty | Quarterly or semi-annually |
   | Transactional NPS | After specific interaction | Post-event (support, purchase) |
   | Product NPS | Product-specific feedback | After usage milestone |

2. **Survey Questions**
   - **Core NPS Question**: "How likely are you to recommend [Company/Product] to a friend or colleague?" (0-10)
   - **Follow-up (Required)**: "What's the primary reason for your score?"
   - **Optional Drivers**: Specific aspects to rate (product, support, value)
   - **Demographics**: Role, tenure, use case (for segmentation)

3. **Survey Design Principles**
   - Keep surveys short (2-4 questions max)
   - Make follow-up question open-ended
   - Don't combine with other surveys
   - Test on mobile devices
   - Use consistent branding

4. **Sample Survey Flow**
   ```
   Screen 1: NPS Question (0-10 scale)
   Screen 2: Open-ended follow-up
   Screen 3: (Optional) One additional question
   Screen 4: Thank you + close loop preview
   ```

### Workflow 2: Targeting & Timing
**Reach the right customers at the right time**

1. **Timing Strategies**
   - **Relationship NPS**:
     - Quarterly cadence (not more frequent)
     - Stagger sends to avoid survey fatigue
     - Avoid holidays and major events
   - **Transactional NPS**:
     - Within 24-48 hours of interaction
     - After meaningful engagement
     - Not after every interaction

2. **Sampling Considerations**
   - Random sample for unbiased results
   - Stratified sample for segment representation
   - Census for small customer bases
   - Exclude recent surveyees (90-day minimum gap)

3. **Audience Targeting**
   | Segment | Frequency | Purpose |
   |---------|-----------|---------|
   | All Customers | Quarterly | Overall trend |
   | Enterprise | Quarterly | High-value focus |
   | New Customers | At 30/90 days | Onboarding health |
   | At-Risk | After intervention | Save effectiveness |
   | Post-Support | After resolution | Service quality |

4. **Channel Selection**
   - Email (most common, highest response for B2B)
   - In-app (contextual, good for product NPS)
   - SMS (high open rates, use sparingly)
   - Post-call IVR (immediate support feedback)

### Workflow 3: Response Analysis
**Extract insights from NPS data**

1. **Score Calculation**
   ```
   NPS = % Promoters (9-10) - % Detractors (0-6)

   Score ranges from -100 to +100
   ```

   | Category | Score Range | Meaning |
   |----------|-------------|---------|
   | Promoters | 9-10 | Loyal enthusiasts |
   | Passives | 7-8 | Satisfied but unenthusiastic |
   | Detractors | 0-6 | Unhappy, risk of churn |

2. **Statistical Validity**
   - Minimum 100 responses for reliable score
   - Calculate confidence intervals
   - Track response rate (aim for 30%+)
   - Note sample size in reporting
   - Compare statistically significant changes only

3. **Segmentation Analysis**
   - By customer segment (size, industry, tier)
   - By tenure (new vs. established)
   - By product/feature usage
   - By geography
   - By use case

4. **Trend Analysis**
   - Track score over time (quarterly minimum)
   - Identify seasonal patterns
   - Correlate with product changes
   - Compare to industry benchmarks
   - Monitor category shifts (Detractor → Passive)

### Workflow 4: Text Analysis
**Understand the "why" behind the score**

1. **Comment Categorization**
   - **Product**: Features, functionality, reliability
   - **Service**: Support, responsiveness, expertise
   - **Value**: Pricing, ROI, worth
   - **Experience**: UX, ease of use, design
   - **Company**: Brand, trust, relationship

2. **Sentiment Mapping**
   | Score | Typical Themes |
   |-------|----------------|
   | 9-10 | What they love most |
   | 7-8 | What would make them promoters |
   | 4-6 | Key frustrations to address |
   | 0-3 | Critical issues driving away |

3. **Quote Extraction**
   - Identify representative quotes per theme
   - Capture specific, actionable feedback
   - Note emotional intensity
   - Flag verbatims for stakeholders

4. **Driver Analysis**
   - Correlate themes with scores
   - Identify strongest positive drivers
   - Find detractor common causes
   - Prioritize by frequency and impact

### Workflow 5: Close the Loop
**Turn feedback into action and follow-up**

1. **Response Triage**
   | Score | Response | Timeline |
   |-------|----------|----------|
   | 0-3 | Personal outreach by CSM/manager | 24-48 hours |
   | 4-6 | CSM follow-up email | Within 1 week |
   | 7-8 | Thank you + what would make it better | Automated |
   | 9-10 | Thank you + advocacy ask | Automated |

2. **Detractor Recovery**
   - Personal call from appropriate level
   - Listen without defending
   - Acknowledge the issue
   - Commit to specific action
   - Follow up on resolution
   - Re-survey after resolution

3. **Promoter Activation**
   - Thank for positive feedback
   - Ask for specific advocacy actions:
     - Review on G2/Capterra
     - Case study participation
     - Reference call availability
     - Social media mention
   - Offer exclusive benefits (beta access, etc.)

4. **Organizational Action**
   - Share insights with product/engineering
   - Create improvement initiatives
   - Track issue → action → impact
   - Communicate changes to customers
   - Measure NPS impact of changes

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create NPS survey | "Create NPS survey for [audience]" |
| Calculate NPS score | "Calculate NPS from responses" |
| Analyze comments | "Analyze NPS comments" |
| Generate report | "Create NPS report for [period]" |
| Segment analysis | "Break down NPS by [segment]" |
| Design follow-up | "Create NPS follow-up workflow" |
| Benchmark comparison | "Compare NPS to industry" |
| Trend analysis | "Show NPS trend over time" |
| Identify drivers | "Find NPS drivers from feedback" |
| Recovery playbook | "Create detractor recovery process" |

## Best Practices

### Survey Design
- Use standard 0-10 NPS scale (never modify)
- Keep survey to 2-3 questions maximum
- Make follow-up question required but open-ended
- Don't ask leading questions
- Test mobile experience

### Timing & Frequency
- Don't survey more than quarterly (relationship NPS)
- Wait 90 days before resurveying same customer
- Avoid surveying during known issues
- Time around customer lifecycle moments
- Respect opt-outs

### Response Rates
- Keep surveys short (2-3 minutes max)
- Send from recognizable sender
- Personalize subject line
- Send at optimal times (Tue-Thu, 10am-2pm)
- Follow up non-responders once

### Analysis
- Focus on trend, not single score
- Segment to find actionable insights
- Read every comment
- Look for patterns, not outliers
- Compare scores statistically

### Closing the Loop
- Respond to detractors within 48 hours
- Thank all respondents
- Share what you're doing with feedback
- Track feedback → action → outcome
- Measure recovery effectiveness

## NPS Benchmarks

### Industry Benchmarks
| Industry | Good | Great | World-Class |
|----------|------|-------|-------------|
| SaaS B2B | 30+ | 50+ | 70+ |
| E-commerce | 40+ | 60+ | 80+ |
| Financial Services | 20+ | 40+ | 60+ |
| Telecom | 0+ | 20+ | 40+ |
| Healthcare | 20+ | 40+ | 60+ |

### Score Interpretation
| Score Range | Interpretation |
|-------------|----------------|
| Below 0 | Serious problems - more detractors than promoters |
| 0-30 | Room for improvement |
| 30-50 | Good - solid foundation |
| 50-70 | Excellent - strong loyalty |
| 70+ | World-class - exceptional |

## Survey Templates

### Relationship NPS Email
```
Subject: [Name], we'd love your feedback (30 seconds)

Hi [Name],

As a valued [Company] customer, your opinion matters to us.

One quick question: How likely are you to recommend [Company] to a friend or colleague?

[0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]
Not at all likely          Extremely likely

Click a number to share your response.

Thank you for your time!

[Company] Team
```

### Follow-Up Question
```
Thanks for your feedback!

What's the primary reason for your score?

[Open text field - required]

[Submit]
```

### Thank You Screen (Promoter)
```
Thank you for your feedback! 🙏

We're thrilled you'd recommend us.

Would you be willing to:
[ ] Write a brief review on G2/Capterra
[ ] Be a reference for future customers
[ ] Share your experience in a case study

[Submit] [Not right now]
```

### Detractor Follow-Up Email
```
Subject: Following up on your feedback

Hi [Name],

I saw your recent feedback about [Company], and I wanted to reach out personally.

I'm sorry we haven't met your expectations. I'd love to understand more about your experience and see how we can make things right.

Would you have 15 minutes this week for a call?

I'm committed to addressing your concerns.

Best,
[Name]
[Title]
[Direct line]
```

## Red Flags

- **Low response rate**: Below 15% suggests survey fatigue or poor targeting
- **Score volatility**: Large swings indicate inconsistent experience
- **Comment mismatch**: Score doesn't align with sentiment
- **Passive majority**: Large passive segment is stalled growth
- **No action**: Collecting data without acting on it
- **Survey fatigue**: Response rates declining over time
- **Score gaming**: Internal pressure to inflate scores
- **Missing segments**: Not hearing from key customer groups

## Metrics to Track

| Metric | What It Tells You | Target |
|--------|-------------------|--------|
| Overall NPS | Customer loyalty level | Industry benchmark + 10 |
| Response Rate | Survey engagement | 30%+ |
| Promoter % | Advocacy potential | 50%+ |
| Detractor % | Churn risk pool | < 15% |
| Comment Rate | Feedback quality | 70%+ of responses |
| Close Rate | Follow-up effectiveness | 100% of detractors |
| Recovery Rate | Detractor win-back | 20%+ to passive/promoter |
