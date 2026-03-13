---
name: report-writing
description: Structure and write comprehensive research reports with proper citations. Use when finalizing research findings into a formal report.
---

# Report Writing Skill

This skill provides structured guidance for transforming research findings into well-organized, professional reports. It ensures consistency, clarity, and completeness across all research outputs.

## When to Use This Skill

Invoke this skill when:

- **Finalizing Research**: Converting raw research notes and findings into a formal deliverable
- **Creating Documentation**: Producing technical documentation, white papers, or analysis reports
- **Synthesizing Multiple Sources**: Combining insights from various sub-agent research tasks into a unified narrative
- **Stakeholder Communication**: Preparing reports for executive review, technical teams, or external audiences
- **Knowledge Preservation**: Documenting research methodology and findings for future reference

**Do NOT use this skill for**:
- Quick summaries or informal notes (use simple markdown instead)
- Real-time status updates (use TODO lists)
- Raw data dumps (use structured data files)

---

## Report Structure Template

Every research report MUST follow this hierarchical structure. Adapt section depth based on report complexity.

### 1. Executive Summary

**Purpose**: Provide a standalone overview for readers who may not read the full report.

**Contents**:
- Research objective (1-2 sentences)
- Key findings (3-5 bullet points)
- Primary recommendations or conclusions
- Critical limitations or caveats

**Length**: 150-300 words (1 page maximum)

**Writing Tip**: Write this section LAST, after all other sections are complete.

### 2. Introduction/Background

**Purpose**: Establish context and frame the research question.

**Contents**:
- Problem statement or research question
- Why this research matters (business/technical impact)
- Scope boundaries (what IS and IS NOT covered)
- Brief overview of approach taken

**Length**: 200-500 words

### 3. Methodology

**Purpose**: Enable reproducibility and establish credibility.

**Contents**:
- Data sources consulted (with dates accessed)
- Search strategies and queries used
- Selection criteria for sources
- Tools and techniques employed
- Limitations of the methodology

**Example Format**:
```markdown
### Data Collection
- Primary sources: [List with access dates]
- Search queries: [Exact queries used]
- Time range: [Date boundaries for research]

### Analysis Approach
- [Describe analytical framework]
- [Note any tools or models used]
```

### 4. Findings

**Purpose**: Present discovered facts objectively, without interpretation.

**Contents**:
- Organized by theme, source type, or chronology
- Each finding clearly attributed to source
- Quantitative data in tables/charts when applicable
- Direct quotes for critical evidence

**Structure Options**:
- **Thematic**: Group by topic or category
- **Comparative**: Side-by-side analysis of alternatives
- **Chronological**: Timeline of developments
- **Source-based**: Organized by information source

### 5. Analysis

**Purpose**: Interpret findings and extract meaning.

**Contents**:
- Patterns and trends identified
- Contradictions or gaps in evidence
- Implications of findings
- Comparison with existing knowledge
- Confidence levels for conclusions

**Analysis Framework**:
```markdown
### Pattern Analysis
[What recurring themes emerge?]

### Gap Analysis
[What questions remain unanswered?]

### Confidence Assessment
- High confidence: [Findings with strong evidence]
- Medium confidence: [Findings with partial evidence]
- Low confidence: [Tentative findings requiring validation]
```

### 6. Conclusions

**Purpose**: Synthesize analysis into actionable insights.

**Contents**:
- Direct answers to research questions
- Prioritized recommendations (if applicable)
- Suggested next steps or future research
- Final assessment of confidence

**Format**:
```markdown
### Key Conclusions
1. [Most important conclusion]
2. [Second conclusion]
3. [Third conclusion]

### Recommendations
1. [Priority 1 action item]
2. [Priority 2 action item]

### Future Research Directions
- [Unanswered questions to explore]
```

### 7. References

**Purpose**: Enable verification and further exploration.

**Contents**:
- All sources cited in the report
- URLs with access dates
- Proper attribution for all quoted material

---

## Citation Formatting Guidelines

### In-Text Citations

Use numbered references in square brackets for inline citations:

```markdown
Recent studies indicate a 40% improvement in efficiency [1]. This aligns with
earlier findings on automation benefits [2, 3].
```

For direct quotes, include page numbers or section identifiers:

```markdown
According to the official documentation, "the system supports up to 10,000
concurrent connections" [4, Section 3.2].
```

### Reference List Format

Use a consistent format for all references:

**Web Sources**:
```markdown
[1] Author/Organization. "Article Title." Website Name. URL. Accessed: YYYY-MM-DD.
```

**Academic Papers**:
```markdown
[2] Author(s). "Paper Title." Journal/Conference Name, Year. DOI/URL.
```

**Documentation**:
```markdown
[3] "Document Title." Product Name Documentation, Version X.X. URL. Accessed: YYYY-MM-DD.
```

**News Articles**:
```markdown
[4] Author. "Headline." Publication Name, Date Published. URL.
```

### Citation Best Practices

1. **Always include access dates** for web sources (content may change)
2. **Prefer primary sources** over secondary reports
3. **Note version numbers** for software documentation
4. **Archive volatile sources** when possible (use archive.org links)
5. **Verify link validity** before finalizing report

---

## Writing Style Recommendations

### Style Selection Guide

| Audience | Style | Characteristics |
|----------|-------|-----------------|
| Executives | Executive | Concise, outcome-focused, minimal jargon |
| Technical Teams | Technical | Detailed, precise terminology, includes code/data |
| Academic/Research | Academic | Formal, extensive citations, methodological rigor |
| General Stakeholders | Balanced | Clear explanations, moderate detail, accessible |

### Executive Style

**Characteristics**:
- Lead with conclusions and recommendations
- Use bullet points liberally
- Limit technical jargon; define necessary terms
- Focus on business impact and ROI
- Keep paragraphs short (3-4 sentences max)

**Example**:
```markdown
## Key Finding: Cloud Migration Reduces Costs by 35%

**Bottom Line**: Migrating to cloud infrastructure will reduce operational
costs by $2.4M annually while improving system reliability.

**Recommended Action**: Approve Phase 1 migration by Q2 2025.

**Risk Level**: Low - Similar migrations have 94% success rate.
```

### Technical Style

**Characteristics**:
- Include implementation details
- Use precise technical terminology
- Provide code samples, configurations, or specifications
- Document edge cases and limitations
- Include performance metrics and benchmarks

**Example**:
```markdown
## Implementation: Rate Limiting Configuration

The API gateway implements token bucket rate limiting with the following
parameters:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Bucket Size | 1000 | Handles burst traffic |
| Refill Rate | 100/sec | Sustainable throughput |
| Key Strategy | IP + User ID | Prevents abuse while supporting legitimate use |

```python
rate_limiter = TokenBucket(
    capacity=1000,
    refill_rate=100,
    key_func=lambda req: f"{req.ip}:{req.user_id}"
)
```
```

### Academic Style

**Characteristics**:
- Formal third-person voice
- Extensive literature review
- Detailed methodology documentation
- Statistical rigor where applicable
- Acknowledge limitations explicitly

**Example**:
```markdown
## Literature Review

Previous research in automated code review systems has demonstrated
significant potential for defect detection. Smith et al. (2023) reported
a 23% reduction in production defects when implementing static analysis
tools [1]. However, Johnson and Lee (2024) note that these gains are
contingent upon proper configuration and team adoption [2].

The present study extends this work by examining the integration of
large language models into the review pipeline, an approach not
addressed in prior literature.
```

### General Guidelines (All Styles)

1. **Active voice preferred**: "The team implemented" not "It was implemented by the team"
2. **Specific over vague**: "37% increase" not "significant increase"
3. **Present tense for findings**: "The data shows" not "The data showed"
4. **Consistent terminology**: Choose one term and use it throughout
5. **Avoid hedging excess**: Limit "may," "might," "could possibly"

---

## Quality Checklist Before Submission

### Structure Verification

- [ ] All seven standard sections present (or justified omission noted)
- [ ] Executive summary can stand alone
- [ ] Logical flow from introduction to conclusions
- [ ] Section lengths appropriate to content importance
- [ ] Headers and subheaders create clear hierarchy

### Content Quality

- [ ] Research question clearly stated and answered
- [ ] All claims supported by cited evidence
- [ ] Findings and analysis clearly separated
- [ ] Contradictory evidence acknowledged
- [ ] Confidence levels stated for conclusions
- [ ] Limitations explicitly documented

### Citation Integrity

- [ ] All sources cited in reference list
- [ ] All references cited in text
- [ ] URLs verified as accessible
- [ ] Access dates included for web sources
- [ ] No broken or placeholder citations

### Writing Quality

- [ ] Consistent writing style throughout
- [ ] Technical terms defined on first use
- [ ] No unexplained acronyms
- [ ] Spell-check completed
- [ ] Grammar review completed
- [ ] Sentence length varied (not all long or all short)

### Formatting

- [ ] Consistent heading styles
- [ ] Tables and figures numbered and titled
- [ ] Code blocks properly formatted
- [ ] Bullet points parallel in structure
- [ ] Page breaks at logical points (if applicable)

### Final Review

- [ ] Report answers the original research question
- [ ] Recommendations are actionable
- [ ] Nothing critical missing from scope
- [ ] Appropriate length for audience and purpose
- [ ] Ready for intended audience

---

## Examples of Report Sections

### Example: Executive Summary

```markdown
## Executive Summary

This report evaluates three cloud database solutions for the customer
analytics platform migration: AWS Aurora, Google Cloud Spanner, and
Azure Cosmos DB.

**Key Findings**:
- AWS Aurora offers the lowest total cost of ownership ($145K/year)
- Google Cloud Spanner provides superior global consistency guarantees
- Azure Cosmos DB integrates best with existing Microsoft infrastructure
- All three solutions meet performance requirements (< 50ms p99 latency)

**Recommendation**: Proceed with AWS Aurora for Phase 1, with architecture
designed to allow future multi-cloud expansion.

**Timeline**: Implementation achievable within Q2 2025 with existing team.

**Confidence Level**: High - Based on proof-of-concept testing and vendor
consultations.
```

### Example: Methodology Section

```markdown
## Methodology

### Research Approach

This analysis employed a mixed-methods approach combining:
1. Vendor documentation review
2. Technical proof-of-concept testing
3. Industry analyst report analysis
4. Peer organization interviews

### Data Sources

| Source Type | Sources Consulted | Date Range |
|-------------|-------------------|------------|
| Vendor Docs | AWS, GCP, Azure official documentation | Dec 2024 |
| Analyst Reports | Gartner, Forrester database evaluations | 2024 |
| Technical Tests | Internal POC environment | Dec 15-22, 2024 |
| Interviews | 3 peer organizations (anonymized) | Dec 2024 |

### Evaluation Criteria

Solutions were evaluated against weighted criteria:
- Performance (30%): Latency, throughput, scalability
- Cost (25%): TCO over 3 years including migration
- Reliability (20%): SLA guarantees, disaster recovery
- Integration (15%): Compatibility with existing stack
- Vendor Support (10%): Documentation, support quality

### Limitations

- POC testing limited to 72-hour duration
- Cost projections based on current pricing (subject to change)
- Interview sample size limits generalizability
```

### Example: Findings Section

```markdown
## Findings

### Performance Comparison

All three solutions demonstrated acceptable performance for the target
workload of 10,000 queries per second:

| Solution | Avg Latency | P99 Latency | Max Throughput |
|----------|-------------|-------------|----------------|
| AWS Aurora | 12ms | 45ms | 15,000 QPS |
| Cloud Spanner | 15ms | 42ms | 18,000 QPS |
| Cosmos DB | 18ms | 48ms | 12,000 QPS |

*Source: Internal POC testing, December 2024 [1]*

### Cost Analysis

Three-year total cost of ownership analysis:

**AWS Aurora**: $435,000
- Compute: $180,000
- Storage: $95,000
- Data transfer: $85,000
- Support: $75,000

**Google Cloud Spanner**: $520,000
- [Detailed breakdown...]

**Azure Cosmos DB**: $485,000
- [Detailed breakdown...]

*Source: Vendor pricing calculators and enterprise discount estimates [2, 3, 4]*
```

### Example: Analysis Section

```markdown
## Analysis

### Cost-Performance Trade-offs

While AWS Aurora offers the lowest TCO, Cloud Spanner's 20% higher cost
delivers measurably better global consistency. For applications requiring
strong consistency across regions, this premium may be justified.

The cost difference primarily stems from:
1. Cloud Spanner's TrueTime infrastructure overhead
2. AWS Aurora's more aggressive reserved instance discounts
3. Different approaches to cross-region replication

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Vendor lock-in | High | Medium | Abstract data layer |
| Price increases | Medium | Medium | 3-year commitment |
| Service outage | Low | High | Multi-region deployment |

### Confidence Assessment

**High Confidence**:
- Performance meets requirements (validated via POC)
- AWS Aurora is most cost-effective option

**Medium Confidence**:
- 3-year cost projections (pricing may change)
- Integration complexity estimates

**Low Confidence**:
- Long-term vendor roadmap alignment
```

### Example: References Section

```markdown
## References

[1] Internal Engineering Team. "Database POC Test Results." Internal
    Documentation. December 22, 2024.

[2] Amazon Web Services. "Amazon Aurora Pricing." AWS Documentation.
    https://aws.amazon.com/aurora/pricing/. Accessed: December 20, 2024.

[3] Google Cloud. "Cloud Spanner Pricing." Google Cloud Documentation.
    https://cloud.google.com/spanner/pricing. Accessed: December 20, 2024.

[4] Microsoft Azure. "Azure Cosmos DB Pricing." Azure Documentation.
    https://azure.microsoft.com/pricing/details/cosmos-db/.
    Accessed: December 20, 2024.

[5] Gartner. "Magic Quadrant for Cloud Database Management Systems."
    Gartner Research, November 2024. (Subscription required)

[6] Smith, J. and Chen, L. "Comparative Analysis of Distributed Databases."
    Proceedings of VLDB 2024. DOI: 10.14778/example.
```

---

## Integration with Research Workflow

This skill integrates with the broader research workflow as follows:

```
Research Request → Data Collection → Analysis → [REPORT WRITING] → Verification → Delivery
                                                      ↑
                                                 This Skill
```

**Inputs Expected**:
- Completed research findings (from sub-agents or direct research)
- Original research request/questions
- Source materials and citations
- Any constraints (length, audience, format)

**Outputs Produced**:
- Formatted report following structure template
- Complete reference list
- Executive summary for quick consumption

**Quality Gates**:
- Report must pass quality checklist before marking complete
- All citations must be verifiable
- Conclusions must trace back to evidence in findings
