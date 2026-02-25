---
name: literature-review-planner
description: Structured literature review planning with systematic methodology, source evaluation, and synthesis frameworks. Use when planning academic literature reviews, research surveys, systematic reviews, or scoping reviews.
---

# Literature Review Planner

Comprehensive frameworks for planning, conducting, and synthesizing literature reviews across academic and professional research contexts.

## Review Types

| Type | Purpose | Scope | Methodology Rigor | Best For |
|------|---------|-------|-------------------|----------|
| **Narrative** | Broad overview of a topic | Wide, flexible | Low-Medium | Background sections, introductions |
| **Systematic** | Answer a specific research question | Narrow, predefined | High | Evidence-based decisions, clinical practice |
| **Scoping** | Map available evidence on a topic | Wide, structured | Medium | Emerging fields, identifying gaps |
| **Meta-Analysis** | Quantitative synthesis of findings | Narrow, statistical | Highest | Combining effect sizes, treatment efficacy |
| **Rapid** | Timely evidence synthesis | Focused, abbreviated | Medium | Policy decisions, time-constrained contexts |
| **Umbrella** | Review of existing reviews | Reviews only | High | Overarching evidence synthesis |
| **Integrative** | Synthesize diverse methodologies | Wide, mixed methods | Medium | Combining qualitative and quantitative |

### Choosing the Right Review Type

```
Do you need to answer a specific, focused question?
  YES --> Is quantitative synthesis of effect sizes needed?
    YES --> Meta-Analysis
    NO  --> Systematic Review
  NO --> Do you need to map the breadth of evidence?
    YES --> Is the field well-established?
      YES --> Umbrella Review (review of reviews)
      NO  --> Scoping Review
    NO --> Do you need to combine qualitative and quantitative?
      YES --> Integrative Review
      NO --> Is time constrained (< 3 months)?
        YES --> Rapid Review
        NO  --> Narrative Review
```

## Search Strategy Development

### PICO/PEO Framework

Use structured frameworks to define your research question:

| Framework | Element | Description | Example |
|-----------|---------|-------------|---------|
| **PICO** | Population | Who is being studied | Adults with Type 2 diabetes |
| | Intervention | What treatment/exposure | Telemedicine consultations |
| | Comparison | Alternative to intervention | In-person consultations |
| | Outcome | What is measured | HbA1c levels, patient satisfaction |
| **PEO** | Population | Who is being studied | Software engineering teams |
| | Exposure | Phenomenon of interest | Agile methodology adoption |
| | Outcome | What is measured | Productivity, code quality |

### Database Selection

| Database | Coverage | Best For |
|----------|----------|----------|
| **PubMed/MEDLINE** | Biomedical, life sciences | Clinical, medical, health research |
| **Scopus** | Multidisciplinary, broadest | Cross-disciplinary reviews |
| **Web of Science** | Multidisciplinary, citation data | Citation analysis, impact tracking |
| **IEEE Xplore** | Engineering, computer science | Technical and computing research |
| **PsycINFO** | Psychology, behavioral science | Mental health, cognition research |
| **ERIC** | Education | Teaching, learning, education policy |
| **CINAHL** | Nursing, allied health | Nursing and health professions |
| **Cochrane Library** | Systematic reviews, trials | Clinical intervention evidence |
| **Google Scholar** | Broad, grey literature | Supplementary searching, snowballing |
| **Preprint servers** | arXiv, bioRxiv, SSRN | Cutting-edge, unpublished work |

### Keyword and Boolean Strategy

```
BUILDING A SEARCH STRING:

Step 1: Identify key concepts from PICO/PEO
  Concept 1: "telemedicine" OR "telehealth" OR "remote consultation" OR "virtual care"
  Concept 2: "diabetes" OR "type 2 diabetes" OR "T2DM" OR "diabetes mellitus"
  Concept 3: "glycemic control" OR "HbA1c" OR "blood glucose" OR "patient outcomes"

Step 2: Combine with Boolean operators
  (Concept 1) AND (Concept 2) AND (Concept 3)

Step 3: Apply filters
  - Date range: 2015-2025
  - Language: English
  - Study type: RCT, cohort, systematic review
  - Peer-reviewed only

ADVANCED OPERATORS:
  "exact phrase"      - Exact match
  *                   - Truncation (therap* = therapy, therapies, therapeutic)
  MeSH terms          - Controlled vocabulary (PubMed)
  NEAR/3              - Proximity (terms within 3 words)
  ti,ab               - Title and abstract search
```

### Search Documentation Template

```
SEARCH LOG:

Database: [Name]
Date Searched: [Date]
Search String: [Full query]
Filters Applied: [Date, language, study type]
Results Retrieved: [Count]
Results After Deduplication: [Count]
Notes: [Any issues, modifications needed]
```

## PRISMA Flow Diagram

```
IDENTIFICATION
  Records identified through database searching: n = ___
  Records identified through other sources: n = ___
  |
  v
  Records after duplicates removed: n = ___
  |
SCREENING
  v
  Records screened (title/abstract): n = ___
  Records excluded: n = ___
  |
  v
  Full-text articles assessed for eligibility: n = ___
  Full-text articles excluded (with reasons): n = ___
    - Reason 1: n = ___
    - Reason 2: n = ___
    - Reason 3: n = ___
  |
INCLUDED
  v
  Studies included in qualitative synthesis: n = ___
  Studies included in quantitative synthesis (meta-analysis): n = ___
```

### Inclusion/Exclusion Criteria

| Criterion | Include | Exclude |
|-----------|---------|---------|
| **Population** | [Define target population] | [Define excluded populations] |
| **Intervention/Exposure** | [Define relevant interventions] | [Define excluded interventions] |
| **Outcome** | [Define relevant outcomes] | [Outcomes not of interest] |
| **Study Design** | [Accepted study types] | [Excluded study types] |
| **Date Range** | [Start year] to [End year] | Outside date range |
| **Language** | [Accepted languages] | Other languages |
| **Publication Type** | Peer-reviewed journals | Editorials, letters, conference abstracts |

## Source Evaluation

### Critical Appraisal Tools by Study Design

| Study Design | Appraisal Tool | Key Domains |
|-------------|---------------|-------------|
| **RCTs** | Cochrane Risk of Bias (RoB 2) | Randomization, blinding, attrition, reporting |
| **Cohort Studies** | Newcastle-Ottawa Scale (NOS) | Selection, comparability, outcome assessment |
| **Case-Control** | Newcastle-Ottawa Scale (NOS) | Selection, comparability, exposure assessment |
| **Qualitative** | CASP Qualitative Checklist | Aims, methodology, recruitment, data, analysis, ethics |
| **Cross-Sectional** | JBI Critical Appraisal | Inclusion, measurement, confounders, analysis |
| **Diagnostic** | QUADAS-2 | Patient selection, index test, reference standard, flow |
| **Mixed Methods** | MMAT | Qualitative, quantitative, mixed methods criteria |

### Source Quality Assessment Framework

```
QUALITY SCORING (rate each 1-5):

RELEVANCE:
  - Directly addresses research question? ___
  - Population matches target? ___
  - Outcomes align with review objectives? ___

METHODOLOGICAL RIGOR:
  - Study design appropriate? ___
  - Sample size adequate? ___
  - Bias minimized? ___
  - Statistical analysis appropriate? ___

CREDIBILITY:
  - Published in peer-reviewed journal? ___
  - Authors have relevant expertise? ___
  - Funding sources declared? ___
  - Conflicts of interest addressed? ___

RECENCY:
  - Published within target date range? ___
  - Findings still applicable? ___
  - Not superseded by newer evidence? ___

TOTAL SCORE: ___ / 60
  High quality: 48-60
  Medium quality: 36-47
  Low quality: < 36
```

### Hierarchy of Evidence

```
EVIDENCE PYRAMID (highest to lowest):

Level 1: Systematic Reviews & Meta-Analyses
Level 2: Randomized Controlled Trials (RCTs)
Level 3: Cohort Studies (prospective)
Level 4: Case-Control Studies
Level 5: Cross-Sectional Studies / Case Series
Level 6: Expert Opinion / Editorials
Level 7: Anecdotal / Narrative Reports
```

## Citation Management

### Workflow

```
CITATION MANAGEMENT PROCESS:

1. COLLECT
   - Export references from databases (RIS, BibTeX, EndNote XML)
   - Import into reference manager (Zotero, Mendeley, EndNote)
   - Attach PDFs where available

2. ORGANIZE
   - Create folder structure mirroring review themes
   - Tag with inclusion/exclusion status
   - Tag with quality rating
   - Add notes and annotations

3. DEDUPLICATE
   - Run automatic deduplication
   - Manual review of near-duplicates
   - Document count removed

4. SCREEN
   - Title/abstract screening (tag: include/exclude/maybe)
   - Full-text screening (tag: include/exclude with reason)
   - Track screening decisions

5. EXTRACT
   - Populate data extraction form
   - Link to source reference
   - Note discrepancies
```

### Data Extraction Template

```
EXTRACTION FORM:

Study ID: ___
Authors: ___
Year: ___
Title: ___
Journal: ___
Study Design: ___
Country/Setting: ___

Population:
  - Sample size: ___
  - Demographics: ___
  - Inclusion criteria: ___

Intervention/Exposure: ___
Comparison/Control: ___

Outcomes:
  - Primary: ___
  - Secondary: ___
  - Measurement tools: ___

Key Findings: ___
Effect Size (if applicable): ___
Confidence Interval: ___
Quality Rating: ___
Reviewer Notes: ___
```

## Synthesis Frameworks

### Thematic Synthesis

```
THEMATIC SYNTHESIS STEPS:

1. CODE: Read included studies and assign descriptive codes
2. ORGANIZE: Group related codes into descriptive themes
3. DEVELOP: Generate analytical themes that go beyond the primary studies
4. MAP: Create a thematic map showing relationships between themes
5. WRITE: Narrate findings organized by analytical themes

THEMATIC MAP STRUCTURE:
  Overarching Theme
  |-- Sub-theme 1
  |   |-- Code A (Studies 1, 3, 7)
  |   |-- Code B (Studies 2, 5)
  |-- Sub-theme 2
  |   |-- Code C (Studies 1, 4, 6)
  |   |-- Code D (Studies 3, 8)
```

### Chronological Synthesis

Best for showing how understanding of a topic has evolved over time.

```
CHRONOLOGICAL STRUCTURE:

Era 1 (e.g., 2000-2010): Foundational Work
  - Key studies and their contributions
  - Prevailing theories and methods

Era 2 (e.g., 2010-2018): Methodological Advances
  - New approaches introduced
  - Challenges to earlier findings

Era 3 (e.g., 2018-Present): Current State
  - Latest findings and debates
  - Emerging directions
```

### Methodological Synthesis

Group studies by methodology to compare how different approaches yield different insights.

| Methodology | Studies | Key Findings | Strengths | Limitations |
|-------------|---------|-------------|-----------|-------------|
| **RCTs** | [list] | [summary] | Causal inference | Generalizability |
| **Qualitative** | [list] | [summary] | Rich context | Subjectivity |
| **Mixed Methods** | [list] | [summary] | Comprehensive | Complexity |
| **Observational** | [list] | [summary] | Real-world validity | Confounding |

## Gap Identification

### Gap Analysis Framework

```
GAP CATEGORIES:

KNOWLEDGE GAPS:
  - What questions remain unanswered?
  - Where do findings conflict?
  - What populations are understudied?

METHODOLOGICAL GAPS:
  - What study designs are missing?
  - Are sample sizes consistently too small?
  - Are measurement tools validated?

CONTEXTUAL GAPS:
  - What geographic regions are underrepresented?
  - What settings haven't been studied?
  - Are there temporal gaps in the literature?

PRACTICAL GAPS:
  - What interventions haven't been tested?
  - Where does evidence fail to translate to practice?
  - What implementation barriers are unaddressed?
```

### Gap Documentation Template

```
GAP: [Brief description]
EVIDENCE: [What the current literature shows / doesn't show]
SIGNIFICANCE: [Why this gap matters]
SUGGESTED RESEARCH: [What future studies could address this]
PRIORITY: [High / Medium / Low]
```

## Writing Structure

### Literature Review Sections

```
STRUCTURE:

1. INTRODUCTION (10-15% of word count)
   - Context and importance of the topic
   - Scope and objectives of the review
   - Research question(s)
   - Brief overview of structure

2. METHODOLOGY (15-20% for systematic; shorter for narrative)
   - Search strategy and databases
   - Inclusion/exclusion criteria
   - Screening process (PRISMA for systematic)
   - Quality assessment approach
   - Data extraction method
   - Synthesis approach

3. FINDINGS / RESULTS (40-50%)
   - Organized by themes, chronology, or methodology
   - Summary tables of included studies
   - Critical analysis (not just description)
   - Comparison and contrast across studies
   - Quality assessment results

4. DISCUSSION (15-20%)
   - Synthesis of key findings
   - Comparison with existing reviews
   - Implications for theory and practice
   - Strengths and limitations of the review

5. GAPS AND FUTURE DIRECTIONS (5-10%)
   - Identified gaps in knowledge
   - Recommended research priorities
   - Methodological recommendations

6. CONCLUSION (5%)
   - Summary of main findings
   - Answer to research question
   - Key implications
```

## Common Pitfalls

| Pitfall | Description | Prevention |
|---------|-------------|------------|
| **Cherry-picking** | Selecting only studies that support a hypothesis | Pre-register protocol, follow PRISMA |
| **Narrative bias** | Describing studies without critical analysis | Use appraisal tools, compare across studies |
| **Scope creep** | Expanding focus beyond original question | Stick to predefined inclusion criteria |
| **Recency bias** | Over-weighting recent studies | Include full date range, weight by quality |
| **Publication bias** | Missing grey literature and null results | Search preprints, dissertations, trial registries |
| **Inadequate search** | Too few databases or narrow search terms | Minimum 3 databases, iterative search refinement |
| **Poor synthesis** | Listing studies instead of integrating findings | Use synthesis frameworks, identify patterns |
| **Missing protocol** | No pre-registered review protocol | Register on PROSPERO or OSF before starting |

## Review Protocol Template

```
PROTOCOL:

Title: [Review title]
Registration: [PROSPERO/OSF ID]
Authors: [Names and roles]
Date: [Protocol date]

Background: [Why this review is needed]
Objectives: [What the review aims to achieve]
Research Question: [PICO/PEO formatted question]

Eligibility Criteria:
  Inclusion: [List]
  Exclusion: [List]

Information Sources: [Databases and other sources]
Search Strategy: [Full search string per database]

Study Selection:
  - Stage 1: Title/abstract screening (2 independent reviewers)
  - Stage 2: Full-text screening (2 independent reviewers)
  - Disagreement resolution: [Process]

Data Extraction: [What data will be extracted]
Quality Assessment: [Which tool(s) will be used]
Synthesis Method: [Narrative, thematic, meta-analysis]
Timeline: [Planned completion date]
```

## See Also

- [Data Science](../data-science/SKILL.md)
- [Grant Proposal Builder](../grant-proposal-builder/SKILL.md)
