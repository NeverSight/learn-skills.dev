---
name: Survey Analyzer
slug: survey-analyzer
description: Process and analyze survey data to extract insights, identify patterns, and generate actionable recommendations
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "analyze survey"
  - "survey results"
  - "survey analysis"
  - "process survey data"
tags:
  - survey-analysis
  - quantitative-research
  - sentiment-analysis
  - response-analysis
---

# Survey Analyzer

Expert survey research agent that processes survey data, analyzes responses, identifies patterns, and generates actionable insights. Specializes in quantitative analysis, qualitative coding, sentiment analysis, cross-tabulation, and recommendation generation from survey feedback.

This skill applies rigorous survey methodology, statistical analysis, and data visualization to transform raw survey responses into clear insights. Perfect for customer feedback, employee engagement, market research, and user experience studies.

## Core Workflows

### Workflow 1: Comprehensive Survey Analysis

**Objective:** Full analysis of survey data from raw responses to final insights

**Steps:**
1. **Survey Overview & Setup**
   - Survey objectives and research questions
   - Population and sample characteristics
   - Response rate and representativeness
   - Survey design evaluation (question types, flow, biases)
   - Data format and structure assessment

2. **Data Cleaning & Preparation**
   - Remove duplicate responses
   - Handle incomplete responses (criteria for inclusion/exclusion)
   - Standardize data formats
   - Code open-ended responses
   - Create derived variables (e.g., aggregate scores, categories)
   - Validate data quality

3. **Descriptive Statistics**
   - Response rate and completion rate
   - Sample demographics and characteristics
   - Response distribution for each question
   - Central tendency (mean, median, mode)
   - Dispersion (standard deviation, range)
   - Frequency tables and percentages

4. **Question-Level Analysis**
   - **Closed-ended questions:**
     - Frequency distributions
     - Top box/bottom box analysis
     - Net Promoter Score (if applicable)
     - Likert scale aggregation
   - **Open-ended questions:**
     - Thematic coding
     - Sentiment analysis
     - Word frequency and clouds
     - Representative quotes

5. **Cross-Tabulation Analysis**
   - Compare responses across segments (demographics, behaviors, etc.)
   - Identify statistically significant differences
   - Chi-square tests for categorical variables
   - T-tests or ANOVA for continuous variables
   - Effect size calculations

6. **Correlation & Pattern Analysis**
   - Identify relationships between variables
   - Correlation matrices
   - Driver analysis (what predicts key outcomes)
   - Segment profiling
   - Cluster identification

7. **Insight Synthesis**
   - Key findings with supporting data
   - Unexpected or surprising results
   - Actionable insights by theme
   - Prioritized recommendations
   - Data storytelling with visualizations

**Deliverable:** Comprehensive survey report with analysis, visualizations, and recommendations

### Workflow 2: Net Promoter Score (NPS) Analysis

**Objective:** Analyze NPS data and drivers of promoter/detractor status

**Steps:**
1. **NPS Calculation**
   - Categorize responses:
     - Promoters: 9-10
     - Passives: 7-8
     - Detractors: 0-6
   - Calculate NPS: % Promoters - % Detractors
   - Compare to benchmarks (industry, historical)

2. **Segment-Level NPS**
   - NPS by customer segment
   - NPS by product/service
   - NPS by geography or time period
   - Identify high and low NPS segments

3. **Driver Analysis**
   - Correlate other survey questions with NPS
   - Identify what promoters value most
   - Identify what frustrates detractors
   - Key driver analysis (what moves NPS most)

4. **Verbatim Analysis**
   - Code "Why?" responses from NPS question
   - Theme analysis by promoter/passive/detractor
   - Sentiment analysis of comments
   - Extract representative quotes

5. **Action Planning**
   - Quick wins to convert passives to promoters
   - Critical issues driving detractors
   - Segment-specific interventions
   - NPS improvement roadmap

**Deliverable:** NPS analysis report with drivers, verbatim insights, and improvement plan

### Workflow 3: Customer Satisfaction (CSAT) Analysis

**Objective:** Analyze customer satisfaction scores and improvement opportunities

**Steps:**
1. **CSAT Metrics**
   - Overall satisfaction score (typically 1-5 or 1-7 scale)
   - % satisfied (top 2 boxes)
   - % dissatisfied (bottom 2 boxes)
   - Mean and distribution
   - Trend over time

2. **Touchpoint Analysis**
   - Satisfaction at each customer journey touchpoint
   - Identify pain points and moments of delight
   - Compare across journey stages

3. **Attribute Importance**
   - Rate importance vs. satisfaction for key attributes
   - Importance-Performance Matrix:
     - High importance, high satisfaction: Strengths (maintain)
     - High importance, low satisfaction: Critical priorities (fix now)
     - Low importance, high satisfaction: Nice-to-haves (maintain if easy)
     - Low importance, low satisfaction: Low priority (de-prioritize)

4. **Root Cause Analysis**
   - What drives satisfaction vs. dissatisfaction
   - Statistical correlation with satisfaction
   - Open-ended feedback thematic analysis
   - Segment-specific drivers

5. **Improvement Prioritization**
   - Rank opportunities by impact and feasibility
   - Quick wins vs. strategic initiatives
   - Resource requirements
   - Expected satisfaction lift

**Deliverable:** CSAT analysis with prioritized improvement roadmap

### Workflow 4: Employee Engagement Survey Analysis

**Objective:** Analyze employee engagement and organizational health

**Steps:**
1. **Engagement Metrics**
   - Overall engagement score
   - Benchmark against industry/historical data
   - Response rate and non-response analysis
   - Engagement distribution (highly engaged, neutral, disengaged)

2. **Dimension Analysis**
   - Common dimensions:
     - Leadership and management
     - Career development
     - Compensation and benefits
     - Work environment
     - Work-life balance
     - Recognition and rewards
     - Company vision and values
   - Score by dimension
   - Identify strengths and weaknesses

3. **Demographic Analysis**
   - Engagement by department, location, tenure, role
   - Identify pockets of high and low engagement
   - Manager-level analysis (team engagement scores)
   - Highlight significant differences

4. **Driver Analysis**
   - What predicts overall engagement
   - Key factors for retention
   - Flight risk indicators
   - Correlation with performance data (if available)

5. **Verbatim Analysis**
   - Code open-ended comments
   - Sentiment by theme
   - Representative employee voices
   - Issues that don't show in quantitative data

6. **Action Planning**
   - Company-wide initiatives
   - Department-specific actions
   - Manager enablement
   - Communication plan for results
   - Follow-up survey timeline

**Deliverable:** Engagement analysis with action plan and communication strategy

### Workflow 5: Open-Ended Response Analysis

**Objective:** Extract insights from qualitative survey responses

**Steps:**
1. **Initial Review**
   - Read a sample of responses for context
   - Identify broad themes emerging
   - Note response quality and depth
   - Assess coding complexity

2. **Codebook Development**
   - Create coding framework:
     - Deductive codes (based on survey objectives)
     - Inductive codes (emerging from responses)
   - Define each code clearly
   - Create hierarchy (themes → sub-themes)
   - Include examples for each code

3. **Response Coding**
   - Apply codes to each response
   - Responses can have multiple codes
   - Track frequency of each code
   - Note sentiment (positive, negative, neutral) per code
   - Flag particularly insightful or representative quotes

4. **Thematic Analysis**
   - Identify most frequent themes
   - Cross-tabulate themes with respondent characteristics
   - Sentiment by theme
   - Co-occurrence of themes (what's mentioned together)

5. **Insight Extraction**
   - Key themes with evidence (frequency + quotes)
   - Surprising or unexpected themes
   - Differences across segments
   - Themes not captured in closed-ended questions
   - Actionable insights from verbatims

6. **Quote Selection**
   - Representative quotes for each theme
   - Powerful or emotional quotes
   - Actionable suggestions
   - Balance positive and negative feedback

**Deliverable:** Qualitative analysis report with themes, sentiment, and curated quotes

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Full survey analysis | "Analyze this survey data comprehensively" |
| NPS analysis | "Calculate and analyze NPS from this survey" |
| CSAT analysis | "Analyze customer satisfaction scores" |
| Open-ended coding | "Code and analyze open-ended responses" |
| Segment comparison | "Compare survey results across [segments]" |
| Driver analysis | "What drives [outcome] in this survey?" |

## Survey Analysis Best Practices

### Data Quality Checks
- [ ] Response rate is adequate (>30% for email surveys)
- [ ] Sample is representative of population
- [ ] No significant non-response bias
- [ ] Straight-lining detected and handled (same answer to all questions)
- [ ] Speeders identified (completed too fast to be genuine)
- [ ] Duplicate responses removed
- [ ] Incomplete responses treated consistently

### Statistical Rigor
- [ ] Appropriate statistical tests selected
- [ ] Sample size adequate for analysis (n>30 for most tests)
- [ ] Assumptions of tests verified
- [ ] Significance levels stated (typically p<0.05)
- [ ] Effect sizes calculated and reported
- [ ] Confidence intervals included
- [ ] Multiple comparison corrections if needed

### Reporting Standards
- [ ] Methodology clearly documented
- [ ] Sample characteristics described
- [ ] Limitations acknowledged
- [ ] Margin of error stated
- [ ] Visualizations are clear and accurate
- [ ] Insights are actionable
- [ ] Recommendations are prioritized
- [ ] Source data or raw counts provided

## Common Survey Question Types

### Closed-Ended Questions

**Rating Scales (Likert)**
- Strongly Disagree → Strongly Agree (1-5 or 1-7)
- Analysis: Mean, distribution, top-2-box %

**Multiple Choice (Single Select)**
- One answer from list
- Analysis: Frequency distribution, mode

**Multiple Choice (Multi-Select)**
- Multiple answers allowed
- Analysis: % selecting each option (denominator = respondents, not responses)

**Ranking Questions**
- Rank items in order
- Analysis: Average rank, % ranked #1

**Matrix/Grid Questions**
- Multiple items, same scale
- Analysis: Item-level scores, comparison across items

### Open-Ended Questions

**Short Text**
- Brief responses (1-2 sentences)
- Analysis: Thematic coding, word frequency

**Long Text**
- Extended responses (paragraphs)
- Analysis: Deep thematic coding, case studies

**Why/Why Not**
- Follow-up to rating question
- Analysis: Reason coding, sentiment

## Key Metrics & Calculations

### Net Promoter Score (NPS)
```
NPS = % Promoters (9-10) - % Detractors (0-6)
Range: -100 to +100
```

### Customer Satisfaction Score (CSAT)
```
CSAT = (Number of satisfied customers / Total responses) × 100
Usually "satisfied" = top 2 boxes on 5-point scale
```

### Top Box Score
```
Top Box % = (Responses in highest category / Total responses) × 100
Example: % "Strongly Agree" on 5-point Likert
```

### Net Sentiment Score
```
Net Sentiment = % Positive - % Negative
(Similar to NPS but for sentiment)
```

### Response Rate
```
Response Rate = (Completed surveys / Invitations sent) × 100
```

### Completion Rate
```
Completion Rate = (Completed surveys / Started surveys) × 100
```

## Visualization Guidelines

### For Closed-Ended Data
- **Single question:** Bar chart (horizontal if many categories)
- **Trends over time:** Line chart or area chart
- **Ratings/Likert:** Diverging stacked bar chart (show positive/negative split)
- **Proportions:** Pie chart (only if <6 categories) or donut chart
- **Comparison across groups:** Grouped bar chart
- **Many variables:** Heatmap or small multiples

### For Open-Ended Data
- **Theme frequency:** Bar chart (themes on Y-axis, frequency on X-axis)
- **Word frequency:** Word cloud (use sparingly, hard to read precisely)
- **Sentiment:** Stacked bar by theme showing positive/neutral/negative
- **Quotes:** Pull quote boxes with attribution

### Best Practices
- Keep it simple: One insight per chart
- Use color intentionally: Consistent meaning (green=positive, red=negative)
- Label clearly: Title, axes, data labels, source
- Show context: Benchmarks, targets, previous periods
- Accessible: Color-blind friendly palettes

## Survey Analysis Report Template

```markdown
# Survey Analysis Report: [Survey Name]

**Date:** [Report Date]
**Survey Period:** [Dates]
**Analyst:** Claude Survey Analyzer

## Executive Summary
- Survey objective
- Response rate and sample size
- Top 3 findings
- Key recommendations

## Methodology
- Survey design and distribution
- Sample characteristics
- Response rate
- Data cleaning and preparation
- Analysis approach

## Key Findings

### Finding 1: [Insight Title]
**Data:** [Metric/statistic]
**Visualization:** [Chart]
**Insight:** [What this means]
**Supporting Evidence:** [Additional data or quotes]

[Repeat for each finding]

## Detailed Analysis

### Overall Results
- Response distribution
- Key metrics (NPS, CSAT, etc.)
- Trends vs. previous period

### Question-by-Question Analysis
[For each key question]
- Response distribution
- Segment breakdown
- Correlation with other variables

### Segment Analysis
[For each key segment]
- How this segment differs
- Unique insights for this segment

### Verbatim Analysis
**Key Themes:**
1. Theme 1 (mentioned by X%)
   - Sentiment: [Positive/Neutral/Negative]
   - Representative quote: "..."

[Repeat for each theme]

## Recommendations
1. **[Priority 1 Recommendation]**
   - Rationale: [Why this matters]
   - Impact: [Expected benefit]
   - Effort: [Low/Medium/High]
   - Timeline: [When to implement]

[Repeat for each recommendation]

## Appendix
- Full question text
- Detailed data tables
- Methodology notes
- Statistical test results
```

## Integration with Other Skills

- **Use with `data-analyzer`:** Advanced statistical analysis of survey data
- **Use with `user-research`:** Complement qualitative research with survey data
- **Use with `sentiment-analysis`:** Deep sentiment analysis of open-ended responses
- **Use with `market-research-analyst`:** Survey-based market validation
- **Use with `trend-spotter`:** Identify emerging preferences and behaviors

## Common Pitfalls to Avoid

- **Ignoring non-response bias:** Those who respond may differ from those who don't
- **Over-interpreting small differences:** Check statistical significance
- **Cherry-picking data:** Report full story, not just favorable results
- **Ignoring open-ended insights:** Numbers tell part of the story
- **Poor question design:** Leading, double-barreled, or ambiguous questions
- **Sample size issues:** Too small for meaningful segment analysis
- **Forgetting margin of error:** All surveys have uncertainty
- **Analysis without action:** Insights are worthless without follow-through
- **Confusing correlation with causation:** Survey data is correlational
- **Failing to close the loop:** Not sharing results or actions with respondents

## Advanced Analysis Techniques

### Driver Analysis
Identify which survey items most influence key outcome (e.g., overall satisfaction)
- Correlation analysis
- Regression analysis (if sufficient sample)
- Relative importance analysis

### Gap Analysis
Compare importance ratings vs. satisfaction ratings
- Identify high-importance, low-satisfaction gaps (priorities)
- Identify low-importance, high-satisfaction areas (potential over-investment)

### Trend Analysis
Compare survey waves over time
- Statistical tests for significant changes
- Identify improving and declining metrics
- Seasonality or event-driven changes

### Text Analytics
Advanced open-ended analysis
- Sentiment scoring
- Entity extraction (brands, products mentioned)
- Topic modeling for large text datasets
- Word co-occurrence networks
