---
name: deep-dive-research-orchestrator
description: Conduct comprehensive multi-dimensional research on any subject using coordinated AI research specialists
category: research
tags:
  - research
  - analysis
  - competitive-intelligence
  - market-analysis
  - data-synthesis
  - investigation
  - orchestration
author: Claude Code
version: 1.1.0
risk-level: low
context: fork
agent: Explore
allowed-tools:
  - Bash(curl *)
  - Bash(grep *)
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
dependencies:
  - financial-deep-research
  - competitor-intel
  - app-store-optimization
  - agent-control-metalayer-skill
  - harness-engineering-skill
ai-requirements:
  - web-search
  - data-synthesis
  - report-generation
  - coordination
estimated-time: 2-3 hours
output-format: markdown
outputs:
  - executive-summary
  - deep-dives
  - analysis
  - synthesis
---

# Deep-Dive Research Orchestrator

## Overview

Conduct comprehensive, multi-faceted research on any subject (companies, products, markets, technologies, etc.) using coordinated AI research specialists. This skill synthesizes data from multiple specialized research agents to produce professional analysis reports with full source documentation.

## What This Skill Does

### Core Research Capabilities

1. **Financial & Funding Analysis**
   - Revenue and profitability metrics
   - Funding rounds and investor details
   - Valuation and comparable analysis
   - Unit economics and financial projections
   - Capital efficiency and burn rate

2. **Competitive & Strategic Intelligence**
   - Market positioning and differentiation
   - Competitive landscape and threats
   - Organization and team information
   - Technology stack and infrastructure
   - Business metrics and growth signals

3. **Product & Market Analysis**
   - Product performance metrics
   - User engagement and satisfaction
   - Market size and growth rates
   - Competitive benchmarking
   - Monetization and pricing strategy

4. **Synthesis & Professional Reporting**
   - Executive summaries with key findings
   - Deep-dive analysis documents
   - Citation-backed claims with sources
   - Data quality and information gap assessment
   - Professional formatting for stakeholders

## How to Use

### Basic Research Request

```
Conduct comprehensive research on [SUBJECT].

Include analysis of:
- [Key dimension 1]
- [Key dimension 2]
- [Key dimension 3]

Generate professional reports with full citations.
```

### Detailed Research with Parameters

```
Research [SUBJECT] for [PURPOSE].

Scope: [lightweight/standard/comprehensive]
Focus: [investment/competitive/market/technical/partnership]
Timeline: [urgent/standard/deep]
Format: [markdown/html/json]

Key research questions:
- [Question 1]
- [Question 2]
- [Question 3]
```

### Example Research Scenarios

**Investment Due Diligence:**
```
Conduct due diligence research on [Subject] for investment evaluation.

Analyze:
1. Financial performance and funding
2. Market opportunity and growth trajectory
3. Product traction and user metrics
4. Competitive positioning and advantages
5. Team capability and track record
6. Key risks and mitigation
```

**Competitive Threat Assessment:**
```
Competitive analysis: How does [Subject] compare to alternatives?

Provide:
1. Market position and differentiation
2. Technology and capabilities
3. Pricing and business model
4. User satisfaction and retention
5. Competitive advantages vs. [alternatives]
6. Likely strategic response
```

**Market & Opportunity Analysis:**
```
Market research on [Subject/Market]:

Evaluate:
1. Total market size and growth rate
2. Current competitors and leaders
3. Customer segments and needs
4. Technology requirements
5. Barriers to entry
6. Partnership and distribution channels
```

**Technology Deep-Dive:**
```
Technical analysis of [Subject]:

Research:
1. Technology stack and architecture
2. Infrastructure and scalability
3. Development practices
4. Security and compliance
5. Performance metrics
6. Technical roadmap
```

**Strategic Partnership Evaluation:**
```
Partnership assessment for [Subject]:

Analyze:
1. Strategic fit and synergies
2. Capability alignment
3. Financial health and stability
4. Cultural compatibility
5. Growth stage and trajectory
6. Risk factors and mitigation
```

## What You Get

### Comprehensive Analysis Package

1. **Executive Summary** (~4,000-5,000 words)
   - Overview and key metrics
   - Strategic findings
   - Conclusions and recommendations

2. **Deep-Dive Analysis** (Multiple files, 10,000-15,000+ words total)
   - Financial analysis
   - Market and competitive positioning
   - Product and performance metrics
   - Technical capabilities
   - Organization and team
   - Strategic assessments

3. **Supporting Documentation**
   - Navigation guide
   - Methodology explanation
   - Source citations
   - Data freshness notes
   - Information gaps identified

### Quality Assurance

- ✅ Minimum 3+ verified sources per major claim
- ✅ All metrics include source attribution
- ✅ Data freshness and research date documented
- ✅ Information limitations explicitly noted
- ✅ Professional formatting with citations
- ✅ Methodology transparency

### Typical Deliverables

- **Word Count:** 15,000-20,000+ words
- **Files:** 5-7 markdown documents
- **Sources:** 20+ verified references
- **Research Time:** 2-3 hours
- **Cost:** $0 (uses pre-installed skills)

## Use Cases

Perfect for:

✅ **Investment Analysis**
- Due diligence for portfolio decisions
- Series A/B/C evaluation
- Competitive landscape for investments

✅ **Competitive Intelligence**
- Monitor market competitors
- Benchmark market positioning
- Identify differentiation opportunities

✅ **Market Research**
- Evaluate market opportunities
- Size markets and TAM
- Understand customer needs

✅ **Strategic Planning**
- Partnership evaluation
- Technology assessment
- Acquisition analysis

✅ **Business Development**
- Capability assessment
- Synergy identification
- Risk evaluation

✅ **Product Strategy**
- Competitive benchmarking
- Feature prioritization
- Pricing research

## Limitations

Not ideal for:

❌ **Private/Bootstrapped Subjects** - Limited public data
❌ **Very Early Stage** - Minimal public information
❌ **Secretive/Stealth Mode** - By design restricted information
❌ **Specialized Domains** - May need domain-specific skills
❌ **Real-Time Data** - Research completes in 2-3 hours

## Agents

This skill includes 5 specialized agents in `.claude/agents/`:

### research-orchestrator (opus)
The lead coordinator that manages the full research workflow. Deploys specialist agents in parallel, cross-references findings, and synthesizes final reports.
- **Skills:** financial-deep-research, competitor-intel, app-store-optimization, agent-control-metalayer-skill, harness-engineering-skill
- **Tools:** Read, Glob, Grep, WebFetch, WebSearch, Task, Write

### financial-researcher (sonnet)
Financial and funding analysis specialist. Revenue metrics, funding rounds, valuations, unit economics, and projections.
- **Skills:** financial-deep-research
- **Tools:** Read, Glob, Grep, WebFetch, WebSearch

### competitive-analyst (sonnet)
Competitive landscape and strategic positioning analyst. Market share, team analysis, technology stack, and competitive threats.
- **Skills:** competitor-intel
- **Tools:** Read, Glob, Grep, WebFetch, WebSearch

### market-product-analyst (sonnet)
Product metrics and market opportunity analyst. App store performance, user engagement, market sizing, and monetization.
- **Skills:** app-store-optimization
- **Tools:** Read, Glob, Grep, WebFetch, WebSearch

### governance-auditor (haiku)
Quality and compliance auditor. Validates source verification, data quality, compliance, and report standards.
- **Skills:** agent-control-metalayer-skill
- **Tools:** Read, Glob, Grep

## Workflow

### Phase 1: Research Planning (15 min)
- Define research objectives
- Identify key questions
- Determine scope and focus

### Phase 2: Specialist Deployment (30 min)
- Activate financial analysis agent
- Deploy competitive intelligence
- Execute product/market research

### Phase 3: Parallel Research (45 min)
- Multiple agents research simultaneously
- Cross-reference findings
- Verify key metrics

### Phase 4: Synthesis & Analysis (30 min)
- Compile findings
- Create cohesive narrative
- Validate conclusions

### Phase 5: Report Generation & Delivery (15 min)
- Generate professional reports
- Verify quality
- Package for stakeholders

**Total Time: 2-2.5 hours**

## Security & Privacy

- ✅ No sensitive data storage
- ✅ Public information sources only
- ✅ No credential requirements
- ✅ No external dependencies
- ✅ Local execution only
- ✅ GDPR/CCPA compliant

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|-----------|
| Data Accuracy | Low | Multiple sources required |
| Information Gaps | Low | Gaps explicitly noted |
| Research Bias | Low | Multiple research angles |
| Data Privacy | Low | Public information only |
| Data Staleness | Low | Research date documented |

## Customization Options

### By Scope
- **Lightweight:** 1 hour (summary + 2 areas)
- **Standard:** 2 hours (summary + 4 areas)
- **Comprehensive:** 3 hours (all areas + analysis)

### By Focus Area
- Financial & Investment
- Competitive & Market Position
- Product & User Traction
- Technical & Infrastructure
- Strategic & Partnership
- Organization & Team

### By Output Format
- **Markdown:** Default (shareable, version-controllable)
- **HTML:** Presentation-ready
- **JSON:** For data integration

## Success Metrics

✅ Complete, accurate information
✅ Professional, organized reporting
✅ All claims supported by sources
✅ Stakeholders can make decisions
✅ Technical teams understand capabilities
✅ Ready for sharing with stakeholders

## Best Practices

### Before Research
- ✅ Define specific research objectives
- ✅ Identify subject clearly
- ✅ List information gaps to fill
- ✅ Determine output format
- ✅ Set scope and timeline

### During Research
- ✅ Document all sources
- ✅ Flag unverified claims
- ✅ Cross-reference metrics
- ✅ Note data freshness
- ✅ Track information gaps

### After Research
- ✅ Review for accuracy
- ✅ Validate key claims
- ✅ Get stakeholder feedback
- ✅ Archive documentation
- ✅ Update knowledge base

## Next Steps After Research

### For Decision Making
→ Use executive summary for overview
→ Deep-dive into relevant sections
→ Reference for key decisions

### For Strategy
→ Identify opportunities and threats
→ Benchmark against alternatives
→ Plan next actions

### For Action
→ Use findings for roadmapping
→ Prioritize based on insights
→ Track competitive developments

## Skill Statistics

| Metric | Value |
|--------|-------|
| **Estimated Time** | 2-3 hours |
| **Report Length** | 15,000-20,000+ words |
| **Number of Files** | 5-7 documents |
| **Source References** | 20+ verified |
| **Cost** | $0 (local execution) |
| **Reusability** | 100% (fully customizable) |

## Version History

- **v1.1** (Feb 2025): Agent orchestration with Explore agent, context isolation, and tool restrictions
- **v1.0** (Feb 2025): Initial release with three research specialist coordination

## Support

For issues, questions, or improvements:
- Check documentation in GitHub repository
- Review examples for usage patterns
- Adapt to your specific use case

---

**Created:** February 24, 2025
**Status:** Production Ready
**Maintenance:** Community-maintained
