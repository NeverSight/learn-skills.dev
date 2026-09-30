---
name: analysis-qa
description: Quality-check data analysis for joins, metrics, denominators, date ranges, leakage, and statistical pitfalls.
---

## Review Checklist

Work through every section below before presenting findings to stakeholders.

### Data Foundation

- [ ] **Correct sources**: Confirmed that the tables and datasets used are the appropriate ones for this question
- [ ] **Freshness**: Data recency is sufficient; the "data as of" date is noted
- [ ] **Coverage**: No unexpected time gaps or missing segments in the dataset
- [ ] **Null treatment**: Null rates in critical columns have been reviewed; nulls are excluded, filled, or explicitly flagged
- [ ] **Duplicate control**: Row counts confirm no double-counting from faulty joins or repeated source records
- [ ] **Filter accuracy**: Every WHERE clause and filter condition has been verified; nothing is accidentally excluded or included

### Computation Integrity

- [ ] **GROUP BY correctness**: All non-aggregated columns appear in GROUP BY; the aggregation grain matches the analytical question
- [ ] **Denominator validity**: Rates and percentages use the intended base population; division by zero is prevented
- [ ] **Temporal alignment**: Compared periods span equal durations; partial periods are either excluded or called out
- [ ] **Join behavior**: JOIN types are intentional (INNER vs. LEFT); many-to-many relationships have not silently inflated totals
- [ ] **Metric fidelity**: Calculated metrics align with how the business defines them; any deviations are documented
- [ ] **Additive consistency**: Sub-totals sum to the reported total where expected; non-additive cases (overlap, double-counting) are explained

### Plausibility Assessment

- [ ] **Order of magnitude**: Key figures fall within a believable range; revenue is non-negative; percentages stay within 0-100%
- [ ] **Trend coherence**: Time series show no unexplained jumps or drops
- [ ] **External agreement**: Headline numbers align with dashboards, finance reports, or earlier analyses
- [ ] **Ballpark math**: Total revenue roughly equals per-user revenue times user count, etc.
- [ ] **Boundary behavior**: Results make sense for edge cases — a single day, a single user, a single category

### Presentation Quality

- [ ] **Accurate visuals**: Bar charts begin at zero; axes have labels; scales are consistent across panels
- [ ] **Clean formatting**: Numbers use appropriate precision, consistent currency/percent notation, and thousands separators
- [ ] **Descriptive titles**: Headings convey the insight, not just the metric name; date ranges are included
- [ ] **Transparent caveats**: Limitations and assumptions are stated up front
- [ ] **Reproducibility**: Another analyst could recreate the work from the provided documentation

## Recognizing Common Mistakes

### Inflated Counts from Many-to-Many Joins

**What goes wrong**: Joining two tables with a many-to-many relationship silently multiplies rows, blowing up counts and sums.

**Detection method**:
```sql
-- Compare row counts before and after the join
SELECT COUNT(*) FROM orders;          -- 1,000
SELECT COUNT(*) FROM orders o
JOIN line_items li ON o.id = li.order_id;  -- 3,500 (unexpected inflation)
```

**Prevention**:
- Always compare pre-join and post-join row counts
- Verify the actual cardinality of the join relationship
- Use `COUNT(DISTINCT o.id)` to count entities accurately through multi-row joins

### Survivorship Bias

**What goes wrong**: The analysis only covers entities that still exist, ignoring those that were removed, churned, or failed.

**Typical scenarios**:
- Studying behavior of "active users" while ignoring everyone who left
- Benchmarking against "companies on our platform" while skipping those who evaluated and moved on
- Analyzing traits of "successful" cases without any "unsuccessful" comparison group

**Prevention**: Before drawing conclusions, ask: "Who is absent from this dataset, and would their presence change the story?"

### Partial Period Comparisons

**What goes wrong**: A month, week, or quarter that is still in progress gets compared to a completed one.

**Typical scenarios**:
- "January revenue is $500K vs. December's $800K" when January is only half over
- "Signups are down this week" when checked on Tuesday against a full prior week

**Prevention**: Restrict comparisons to completed periods, or normalize by matching the same number of elapsed days.

### Shifting Denominators

**What goes wrong**: The population used as a denominator changes between periods, making rate comparisons invalid.

**Typical scenarios**:
- Conversion rate appears to improve because the definition of "eligible visitor" was narrowed
- Churn rate shifts because "active user" was redefined mid-analysis

**Prevention**: Lock in consistent definitions across every period being compared. Flag any definition changes.

### Averaging Pre-Computed Averages

**What goes wrong**: Taking the mean of group-level averages ignores differences in group size, producing an incorrect overall figure.

**Illustration**:
- Segment A: 100 customers, $50 average order
- Segment B: 10 customers, $200 average order
- Incorrect overall average: ($50 + $200) / 2 = $125
- Correct weighted average: (100 * $50 + 10 * $200) / 110 = $63.64

**Prevention**: Always compute averages from individual records. Never take the mean of already-aggregated means.

### Timezone Inconsistencies

**What goes wrong**: Different source systems record timestamps in different zones, causing misaligned daily rollups and join mismatches.

**Typical scenarios**:
- Backend events logged in UTC while the reporting layer uses US Pacific
- Two tables that define "today" with different cutoff hours

**Prevention**: Convert all timestamps to a single reference zone (UTC is the safest default) before any analysis. State the timezone in the deliverable.

### Circular Segmentation

**What goes wrong**: Segments are defined using the very outcome being measured, creating tautological findings.

**Typical scenarios**:
- "Users who finished onboarding retain better" — finishing onboarding is itself a retention signal
- "Power users drive more revenue" — revenue generation is what made them power users

**Prevention**: Base segment definitions on characteristics measured before the outcome period, not on the outcome itself.

## Sanity-Checking Results

### Quick Magnitude Tests

| Metric Category | Validation Approach |
|---|---|
| User counts | Cross-reference against known DAU/MAU benchmarks |
| Revenue totals | Compare to known ARR or recent financial reports |
| Conversion rates | Must be 0-100%; compare to dashboard baselines |
| Growth rates | Is 50%+ month-over-month realistic, or does it signal a data problem? |
| Averages | Given the distribution, does this number feel right? |
| Segment shares | Do percentage breakdowns sum to approximately 100%? |

### Cross-Validation Approaches

1. **Dual calculation**: Derive the same metric via two independent query paths and confirm they match
2. **Record-level spot checks**: Select a handful of specific entities and manually trace their numbers end to end
3. **Benchmark comparison**: Verify against published dashboards, finance systems, or prior analysis outputs
4. **Arithmetic reversal**: If total revenue is X and there are N users, does X / N approximate the reported per-user figure?
5. **Micro-slice testing**: Filter to a single day, user, or category and confirm the micro-result is sensible

### Signals That Demand Investigation

- Any metric swinging more than 50% period-over-period without a clear explanation
- Totals or sums that land on suspiciously round numbers (possible filter or default-value artifact)
- Rates pegged at exactly 0% or 100% (may indicate missing data rather than perfect outcomes)
- Results that confirm the hypothesis too neatly (real data is almost always messy)
- Identical values appearing across different time periods or segments (suggests a dimension is being ignored)

## Ensuring Reproducibility

### Analysis Write-Up Template

Every substantial analysis should ship with this documentation:

```markdown

## Analysis: [Title]

### Business Question
[The precise question this work answers]

### Sources
- Table: [schema.table_name] (snapshot date: [date])
- Table: [schema.other_table] (snapshot date: [date])
- External file: [filename] (origin: [description])

### Metric and Segment Definitions
- [Metric A]: [Precise calculation formula]
- [Segment X]: [Exact inclusion/exclusion criteria]
- [Time window]: [Start] through [end], [timezone]

### Analytical Approach
1. [First step and its purpose]
2. [Second step]
3. [Third step]

### Assumptions and Known Limitations
- [Assumption and why it holds]
- [Limitation and its potential effect on conclusions]

### Results
1. [Finding with supporting evidence]
2. [Finding with supporting evidence]

### Queries
[All SQL and code used, annotated with comments]

### Warnings for the Reader
- [Anything the audience should weigh before acting on these results]
```

### Annotating Analytical Code

For SQL or Python that others may reuse:

```python
"""
Title: Monthly Cohort Retention
Author: [Name]
Created: [Date]
Sources: events, users
Last cross-checked: [Date] — matched dashboard within 2%

Objective:
    Build monthly retention cohorts anchored on each user's first event date.

Assumptions:
    - "Active" = at least one recorded event in the calendar month
    - Internal and test accounts excluded (user_type != 'internal')
    - All timestamps normalized to UTC

Output:
    Retention grid: rows are cohort months, columns are months since first event.
    Cell values are retention percentages (0-100).
"""
```

### Maintaining an Audit Trail

- Store all queries and scripts in version control or a shared knowledge base
- Record the exact data snapshot date used for each analysis run
- When refreshing a recurring analysis, document what changed and why
- Link current results to prior versions so trends in the analysis itself are traceable
