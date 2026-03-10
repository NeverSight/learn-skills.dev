---
name: review-research
description: >
  Conduct a peer review of research methodology, experimental design, and
  manuscript quality. Covers methodology evaluation, statistical appropriateness,
  reproducibility assessment, bias identification, and constructive feedback.
  Use when reviewing a manuscript, preprint, or internal research report,
  evaluating a research proposal or study protocol, assessing evidence quality
  behind a claim, or reviewing a thesis chapter or dissertation section.
license: MIT
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: review
  complexity: advanced
  language: natural
  tags: peer-review, methodology, research, reproducibility, bias, manuscript
---

# Review Research

Perform a structured peer review of research work, evaluating methodology, statistical choices, reproducibility, and overall scientific rigour.

## When to Use

- Reviewing a manuscript, preprint, or internal research report
- Evaluating a research proposal or study protocol
- Assessing the quality of evidence behind a claim or recommendation
- Providing feedback on a colleague's research design before data collection
- Reviewing a thesis chapter or dissertation section

## Inputs

- **Required**: Research document (manuscript, report, proposal, or protocol)
- **Required**: Field/discipline context (affects methodology standards)
- **Optional**: Journal or venue guidelines (if reviewing for publication)
- **Optional**: Supplementary materials (data, code, appendices)
- **Optional**: Prior reviewer comments (if reviewing a revision)

## Procedure

### Step 1: First Pass — Scope and Structure

Read the entire document once to understand:
1. **Research question**: Is it clearly stated and specific?
2. **Contribution claim**: What is novel or new?
3. **Overall structure**: Does it follow the expected format (IMRaD, or venue-specific)?
4. **Scope match**: Is the work appropriate for the target audience/venue?

```markdown
## First Pass Assessment
- **Research question**: [Clear / Vague / Missing]
- **Novelty claim**: [Stated and supported / Overstated / Unclear]
- **Structure**: [Complete / Missing sections: ___]
- **Scope fit**: [Appropriate / Marginal / Not appropriate]
- **Recommendation after first pass**: [Continue review / Major concerns to flag early]
```

**Expected:** Clear understanding of the paper's claims and contribution.
**On failure:** If the research question is unclear after a full read, note this as a major concern and proceed.

### Step 2: Evaluate Methodology

Assess the research design against standards for the field:

#### Quantitative Research
- [ ] Study design appropriate for the research question (experimental, quasi-experimental, observational, survey)
- [ ] Sample size justified (power analysis or practical rationale)
- [ ] Sampling method described and appropriate (random, stratified, convenience)
- [ ] Variables clearly defined (independent, dependent, control, confounding)
- [ ] Measurement instruments validated and reliability reported
- [ ] Data collection procedure reproducible from the description
- [ ] Ethical considerations addressed (IRB/ethics approval, consent)

#### Qualitative Research
- [ ] Methodology explicit (grounded theory, phenomenology, case study, ethnography)
- [ ] Participant selection criteria and saturation discussed
- [ ] Data collection methods described (interviews, observations, documents)
- [ ] Researcher positionality acknowledged
- [ ] Trustworthiness strategies reported (triangulation, member checking, audit trail)
- [ ] Ethical considerations addressed

#### Mixed Methods
- [ ] Rationale for mixed design explained
- [ ] Integration strategy described (convergent, explanatory sequential, exploratory sequential)
- [ ] Both quantitative and qualitative components meet their respective standards

**Expected:** Methodology checklist completed with specific observations for each item.
**On failure:** If critical methodology information is missing, flag as a major concern rather than assuming.

### Step 3: Assess Statistical and Analytical Choices

- [ ] Statistical methods appropriate for the data type and research question
- [ ] Assumptions of statistical tests checked and reported (normality, homoscedasticity, independence)
- [ ] Effect sizes reported alongside p-values
- [ ] Confidence intervals provided where appropriate
- [ ] Multiple comparison corrections applied when needed (Bonferroni, FDR, etc.)
- [ ] Missing data handling described and appropriate
- [ ] Sensitivity analyses conducted for key assumptions
- [ ] Results interpretation consistent with the analysis (not overstating findings)

Common statistical red flags:
- p-hacking indicators (many comparisons, selective reporting, "marginally significant")
- Inappropriate tests (t-test on non-normal data without justification, parametric tests on ordinal data)
- Confusing statistical significance with practical significance
- No effect size reporting
- Post-hoc hypotheses presented as a priori

**Expected:** Statistical choices evaluated with specific concerns documented.
**On failure:** If the reviewer lacks expertise in a specific method, acknowledge this and recommend a specialist reviewer.

### Step 4: Evaluate Reproducibility

- [ ] Data availability stated (open data, repository link, available on request)
- [ ] Analysis code availability stated
- [ ] Software versions and environments documented
- [ ] Random seeds or reproducibility mechanisms described
- [ ] Key parameters and hyperparameters reported
- [ ] Computational environment described (hardware, OS, dependencies)

Reproducibility tiers:
| Tier | Description | Evidence |
|------|-------------|----------|
| Gold | Fully reproducible | Open data + open code + containerized environment |
| Silver | Substantially reproducible | Data available, analysis described in detail |
| Bronze | Potentially reproducible | Methods described but no data/code sharing |
| Opaque | Not reproducible | Insufficient method detail or proprietary data |

**Expected:** Reproducibility tier assigned with justification.
**On failure:** If data cannot be shared (privacy, proprietary), synthetic data or detailed pseudocode is an acceptable alternative — note whether this is provided.

### Step 5: Identify Potential Biases

- [ ] Selection bias: Were participants representative of the target population?
- [ ] Measurement bias: Could the measurement process have systematically distorted results?
- [ ] Reporting bias: Are all outcomes reported, including non-significant ones?
- [ ] Confirmation bias: Did the authors only look for evidence supporting their hypothesis?
- [ ] Survivorship bias: Were dropouts, excluded data, or failed experiments accounted for?
- [ ] Funding bias: Is the funding source disclosed and could it influence the findings?
- [ ] Publication bias: Is this a complete picture or might negative results be missing?

**Expected:** Potential biases identified with specific examples from the manuscript.
**On failure:** If biases cannot be assessed from the available information, recommend that the authors address this explicitly.

### Step 6: Write the Review

Structure the review constructively:

```markdown
## Summary
[2-3 sentences summarizing the paper's contribution and your overall assessment]

## Major Concerns
[Issues that must be addressed before the work can be considered sound]

1. **[Concern title]**: [Specific description with reference to section/page/figure]
   - *Suggestion*: [How the authors might address this]

2. ...

## Minor Concerns
[Issues that improve quality but are not fundamental]

1. **[Concern title]**: [Specific description]
   - *Suggestion*: [Recommended change]

## Questions for the Authors
[Clarifications needed to complete the evaluation]

1. ...

## Positive Observations
[Specific strengths worth acknowledging]

1. ...

## Recommendation
[Accept / Minor revision / Major revision / Reject]
[Brief rationale for the recommendation]
```

**Expected:** Review is specific, constructive, and references exact locations in the manuscript.
**On failure:** If the review is running long, prioritize major concerns and note minor issues in a summary list.

## Validation

- [ ] Every major concern references a specific section, figure, or claim
- [ ] Feedback is constructive — problems are paired with suggestions
- [ ] Positive aspects acknowledged alongside concerns
- [ ] Statistical assessment matches the analysis methods used
- [ ] Reproducibility is explicitly evaluated
- [ ] The recommendation is consistent with the severity of concerns raised
- [ ] The tone is professional, respectful, and collegial

## Common Pitfalls

- **Vague criticism**: "The methodology is weak" is unhelpful. Specify what is weak and why.
- **Demanding a different study**: Review the research that was done, not the research you would have done.
- **Ignoring scope**: A conference paper has different expectations than a journal article.
- **Ad hominem**: Review the work, not the authors. Never reference author identity.
- **Perfectionism**: No study is perfect. Focus on concerns that would change the conclusions.

## Related Skills

- `review-data-analysis` — deeper focus on data quality and model validation
- `format-apa-report` — APA formatting standards for research reports
- `generate-statistical-tables` — publication-ready statistical tables
- `validate-statistical-output` — statistical output verification
