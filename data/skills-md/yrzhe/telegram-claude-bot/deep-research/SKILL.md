---
name: deep-research
description: Deep research skill for systematic exploration. Auto-triggered for research, analysis, investigation tasks. Ensures data accuracy and research depth.
triggers:
  - research
  - analyze
  - investigate
  - deep dive
  - study
  - evaluate
  - compare
  - industry
  - market
  - trend
  - outlook
  - 研究
  - 分析
  - 调研
  - 深入
---

# Deep Research Skill

## Core Principles

**Every research task MUST follow**:
1. Plan first, execute later - Don't start collecting data immediately
2. Multi-dimensional exploration - Go deep, don't stay shallow
3. Verify data - Sources must be cited, important data cross-verified
4. Dig into anomalies - Unusual points are often the most valuable
5. Maintain explorer's mindset - Curiosity-driven, always ask "why"

## Auto-Trigger Conditions

MUST use this skill when user message involves:

- Any "research X", "analyze X", "investigate X" requests
- Questions about a topic/industry/company/technology/person
- Data-driven decision making
- Comparison and evaluation tasks
- Deep understanding of a field
- Trends, outlook, development direction topics

## Research Execution Flow

### Phase 1: Research Planning (REQUIRED)

Before any actual research, MUST complete these steps:

#### 1.1 Clarify Research Objectives

Ask yourself:
- What does the user really want to know? (beyond the surface question)
- What is the ultimate value of this research?
- What form should the output be? (report/data/recommendations)

#### 1.2 Brainstorm Research Dimensions (MUST list at least 5)

Think systematically about these aspects:

| Dimension Type | Example Questions |
|---------------|-------------------|
| Core Direct | What data is needed to directly answer the user's question? |
| Background Context | What's the history? What's the development timeline? |
| Related Factors | What are the influencing factors? What are the relationships? |
| Different Perspectives | How do different viewpoints see this issue? |
| Risks & Limitations | What are the risks? What are the limitations? |
| **Unique Angles** | What unusual points are worth exploring deeply? |

**Important**: The 6th "Unique Angles" dimension is key to creating differentiated value - don't skip it.

#### 1.3 Determine Priorities

Categorize:
- **Must Have**: Core questions that must be answered
- **Should Have**: Value-adding supplementary analysis
- **Nice to Have**: Unique insights and extended thinking

#### 1.4 Define Quality Criteria

Auto-generate review_criteria for subsequent review, including:
- Which dimensions must be covered for completeness
- What data quality standards to meet
- What depth of analysis is expected
- What sections the report must contain

### Phase 2: Data Collection & Verification

#### Universal Verification Rules

1. **Prioritize reliable data sources**
   - Professional tools (e.g., akshare-stocks, akshare-a-shares)
   - Official websites and documentation
   - Authoritative media and institutions

2. **Cross-verify important data**
   - At least 2 sources for confirmation
   - If conflicts exist, analyze reasons

3. **MUST cite data sources and timestamps**
   - Source: Where the data came from
   - Time: Data timeliness
   - If historical data, clearly mark it

#### Domain-Specific Rules

| Domain | Recommended Sources | Verification Method |
|--------|--------------------|--------------------|
| Finance/Stocks | akshare-stocks + akshare-a-shares + web-research | Dual-source comparison, note trading day |
| Tech/Products | Official docs + tech blogs + community discussions | Version number verification, release date |
| News/Events | Multiple media + official statements | Timeline comparison, source tracing |
| Academic/Professional | Papers + authoritative institution reports | Cite original sources |
| Companies/Organizations | Official site + financial reports + news | Multi-dimensional cross-reference |

### Phase 3: Deep Exploration (Core Value Phase)

For each research dimension, execute this flow:

```
┌─────────────────────────────────────┐
│  1. Basic Information Collection    │
│     - Gather fundamental data/facts │
└─────────────┬───────────────────────┘
              ▼
┌─────────────────────────────────────┐
│  2. Anomaly Identification (KEY)    │
│     - What data looks unusual?      │
│     - What trends deserve attention?│
│     - What's commonly overlooked?   │
└─────────────┬───────────────────────┘
              ▼
┌─────────────────────────────────────┐
│  3. Deep Investigation (anomalies)  │
│     - Why is this happening?        │
│     - What's the underlying cause?  │
│     - What impacts/chain effects?   │
└─────────────┬───────────────────────┘
              ▼
┌─────────────────────────────────────┐
│  4. Form Insights                   │
│     - What does this mean?          │
│     - What value for the user?      │
│     - What actionable suggestions?  │
└─────────────────────────────────────┘
```

### Phase 4: Comprehensive Report

#### Report Structure (MUST include)

1. **Executive Summary**
   - 2-3 sentences summarizing core conclusions
   - Let readers quickly grasp key points

2. **Key Findings**
   - Each finding must have data support
   - Cite data sources and timestamps
   - Distinguish facts from inferences

3. **Deep Analysis**
   - In-depth exploration of anomalies
   - Analysis from different angles
   - Unique insights and observations

4. **Data Appendix**
   - Sources of all cited data
   - Retrieval timestamps
   - Data limitations explained

5. **Risk Alerts/Limitations**
   - Data limitations
   - Analysis assumptions
   - Possible biases

6. **Conclusions & Recommendations**
   - Clear recommendations based on research
   - Directions for further exploration
   - Points requiring ongoing attention

## Review Guidelines (For Main Agent)

When reviewing research results, check these dimensions:

### Coverage Check
- [ ] Does it answer the user's core question?
- [ ] Does it cover all planned dimensions?
- [ ] Are there obvious missing important aspects?

### Depth Check
- [ ] Does analysis stay at surface-level data?
- [ ] Are anomalies/interesting points explored deeply?
- [ ] Are there unique insights and observations?
- [ ] Does it ask "why"?

### Data Quality Check
- [ ] Are data sources cited?
- [ ] Is important data cross-verified?
- [ ] Are timestamps clear?
- [ ] Is historical data clearly marked?

### Logic Check
- [ ] Are conclusions supported by data?
- [ ] Is the reasoning sound?
- [ ] Does it distinguish facts from inferences?

### When Rejecting, MUST Provide

If deciding to reject, must give:
1. **Specific Issue**: Which dimension is insufficient/inaccurate
2. **Missing Content**: What else should be analyzed
3. **Exploration Directions**: 2-3 specific improvement directions
4. **Improvement Guidance**: Tell Sub Agent exactly how to improve

Example rejection feedback:
```
REJECT

Issue: Analysis stays at surface level, only lists data without analyzing reasons.

Missing dimensions:
- No comparison with industry averages
- No analysis of historical trend changes
- No exploration of reasons for anomalous data points

Improvement directions:
1. Compare with data from other companies in the same industry
2. Analyze trends over the past 3 years
3. Deeply explore why XXX metric is abnormally high

Specific suggestion: XXX data is significantly higher than industry average,
this is worth exploring from market positioning, cost structure,
and competitive advantage perspectives.
```

## Quality Criteria Template

When using delegate_and_review, reference this quality criteria template:

```
Research report must satisfy:

1. Structural Completeness
   - Contains summary, findings, analysis, data appendix, conclusions
   - Each section has substantial content, not empty

2. Data Quality
   - All data has cited sources
   - Key data verified from at least 2 sources
   - Data timeliness is clear

3. Analysis Depth
   - Not just listing data, must have analysis
   - Anomalies are explored in depth
   - Has unique insights, not generic statements

4. Practical Value
   - Conclusions are clear and actionable
   - Recommendations are specific and implementable
   - Risk alerts are explicit
```
