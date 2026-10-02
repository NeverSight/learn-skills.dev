---
name: red-team-verifier-patrick-munro
description: Adversarial verification of AI-generated legal content with systematic fact-checking, source validation, and quality control. Use when a user asks to verify, fact-check, red-team, validate sources, or quality-control a legal document, briefing, compliance summary, or regulatory analysis before it is distributed to clients, stakeholders, or published. Trigger phrases include "verify", "fact-check", "red team", "red-flag", "check accuracy", "validate sources", "quality control", "is this correct", and "review for errors". Produces a structured verification report with severity-categorized errors, verified sources, unsupported claim list, missing disclaimers, and an explicit distribution-readiness assessment.
metadata:
  author: "Patrick Munro"
  license: "agpl-3.0"
  version: "2026-04-25"
---

# Red Team Verifier

## Purpose

This skill provides systematic adversarial verification of AI-generated legal content to establish factual accuracy, proper legal citation, and appropriate disclaimers before the content is distributed to clients or stakeholders. It addresses the core concern about AI in legal practice: *how do I know this is accurate?*

The output is a structured verification report, not a reassurance. Where a claim cannot be confirmed against an official source, the skill reports it as unsupported rather than as true.

## When to use

- Verification of AI-generated legal content before client or stakeholder distribution
- Fact-checking of legal snapshots, briefings, or analyses
- Quality control on compliance documents, regulatory summaries, or legal reports
- Red-team review of legal outputs before publication
- Adversarial testing of legal claims or arguments in draft materials

**Trigger phrases**: verify, fact-check, red team, red-flag, check accuracy, validate sources, quality control, is this correct, review for errors.

## Verification stance

Every factual claim, citation, date, and number in the input document is treated as unverified until an official source confirms it. Independent verification is the product of this skill, not a safeguard layered on top of it. A claim that cannot be matched to a primary or official source is reported as unsupported rather than as true. This stance applies uniformly across legal citations, numerical data, timelines, attributions, and interpretations; each requires its own verification step.

This is an adversarial stance by design. The goal is not to confirm what the input document says, but to independently test it. The verifier actively searches for contradictory evidence, questions every number, demands sources, tests logical consistency, and challenges interpretations against authoritative sources.

## Core verification categories

### 1. Factual accuracy

- **Regulatory dates and deadlines**: enforcement dates, compliance deadlines, transition periods
- **Article and section references**: confirm that regulation articles, statutory sections, directive provisions exist and are cited correctly
- **Numerical data**: statistics, percentages, thresholds, financial amounts
- **Entity names**: correct naming of agencies and authorities (regulatory bodies, supervisory authorities, courts, standards bodies)
- **Timeline accuracy**: historical events, legislative milestones, implementation schedules

### 2. Legal authority citations

- **Primary sources**: laws, regulations, directives (e.g., AI Act Article 6(2), GDPR Article 25, NIS2 Article 21)
- **Secondary sources**: case law, administrative guidance, regulatory opinions
- **Citation format**: EUR-Lex references, official journal citations, national citation conventions
- **Authority hierarchy**: primary law distinguished from guidance or commentary
- **Currency**: cited version is current, not superseded

### 3. Arithmetic validation

- **Timeline calculations**: independently compute compliance deadlines from effective dates
- **Percentage calculations**: verify mathematical accuracy of percentages, ratios, proportions
- **Financial calculations**: penalty calculations, cost estimates, threshold determinations
- **Logical consistency**: numbers add up across the document; if the text mentions "three categories", exactly three are listed

### 4. Source verification

- Every factual claim links to a verifiable source
- Official sources take precedence: EUR-Lex, official gazettes, government websites, regulatory authority publications
- Statistical claims include attribution
- Quotes include proper attribution and match the source character-by-character
- Critical claims cross-referenced across multiple independent sources

### 5. Speculation detection

- Opinion is distinguished from factual legal requirement
- Unsettled or debated interpretations are labeled as such
- Predictive statements about future regulatory developments are flagged as speculation
- Hedging terms ("likely", "probably", "expected to") are recognized and labeled
- Editorial framing not present in the source material is flagged

### 6. Disclaimer adequacy

- Legal advice disclaimer ("This is not legal advice") where appropriate
- Jurisdiction clearly stated
- Date or version of regulations cited
- Recommendation to consult qualified legal professionals for specific situations
- Disclosure where regulation is pending, in draft, or interpretation is unclear

## Verification methodology

Execute the following steps in order. Each step produces evidence that feeds the final report.

### Step 1: Initial content review

Read the entire document to understand scope and claims. List all factual claims, legal citations, numerical data, and authoritative statements. Note missing sources, vague language, and unsupported assertions.

### Step 2: Source verification

For every factual claim, legal citation, and statistical assertion, run a web search against official sources in this priority order:

1. Primary legal databases (EUR-Lex for EU law; national equivalents for domestic law)
2. Official government websites (.gov, .gov.uk, .bund.de, .europa.eu, etc.)
3. Regulatory authority publications (supervisory authorities, standards bodies)
4. Official gazettes and consolidated text repositories

Cross-reference critical claims across multiple sources. Record the source URL for each verified fact.

### Step 3: Arithmetic verification

Independently calculate all timelines, deadlines, and dates. Recompute all percentages, ratios, and financial figures. Check internal consistency between stated counts and enumerated items.

### Step 4: Citation validation

Confirm that cited article and section numbers exist in the referenced regulation. Check that citations match the current consolidated version. Verify citation format against jurisdiction standards. Confirm quoted text matches the source exactly.

### Step 5: Speculation identification

Flag predictive statements, editorial opinions presented as facts, and areas of legal uncertainty. Confirm speculative content is clearly labeled in the source document.

### Step 6: Disclaimer review

Verify presence of legal advice disclaimer, jurisdiction statement, regulation date or version, and recommendation for professional consultation.

## Source hierarchy

Apply this hierarchy when evaluating source quality:

1. **Primary legal sources**: official legislation (EUR-Lex, national official gazettes)
2. **Official guidance**: regulatory authority publications (supervisory authorities, European Commission, national data protection authorities, financial regulators, cybersecurity agencies, standards bodies)
3. **Secondary legal sources**: court decisions, published legal commentary, peer-reviewed academic analysis
4. **Tertiary sources**: news articles and blog posts. Use only when primary or official guidance sources are unavailable, and label the lower source quality explicitly in the report.

## Transparency requirements

- Every verified fact includes its source URL
- Claims that could not be verified are listed explicitly under "Unsupported Claims"
- Areas of legal uncertainty or active debate are disclosed
- Speculation from the source document is reported as speculation, not fact

## Output structure

Produce the verification report in this format:

```
# LEGAL RED TEAM VERIFICATION REPORT

## Document Analyzed
[Title/description of content verified]

## Overall Assessment
Quality Score: [1-5 scale, 5 = distribution-ready]
Distribution Readiness: [READY / NEEDS REVISION / MAJOR CORRECTIONS REQUIRED]
Critical Issues Found: [Number]
Verification Completed: [Date/time]

---

## Verified Facts
[List all factual claims successfully verified with sources]
- Claim: [statement]
  Source: [official source URL]
  Status: Verified

---

## Errors Requiring Correction

### Critical (immediate correction required)
- Error: [Description of factual error, legal misstatement, or arithmetic mistake]
  Location: [Where in document]
  Correction: [What it should say]
  Source: [Correct source URL]

### High (correction strongly recommended)
- Issue: [Missing critical disclaimer, regulatory uncertainty not disclosed]
  Impact: [Why this matters]
  Recommendation: [Suggested addition or revision]

### Moderate (should be addressed)
- Issue: [Unsourced statistics, editorial framing as fact]
  Impact: [Credibility or accuracy concern]
  Recommendation: [How to improve]

### Low (minor improvements)
- Issue: [Minor inconsistencies, stylistic issues]
  Recommendation: [Optional enhancement]

---

## Unsupported Claims
[Claims requiring verification or removal]
- Claim: [Statement made without source]
  Status: Could not verify through official sources
  Action Required: Provide source or remove claim

---

## Missing Disclaimers
[Recommended disclaimer additions]
- Location: [Where to add]
  Type: [Legal advice / Jurisdiction / Date-version / Professional consultation]
  Suggested Language: [Specific disclaimer text]

---

## Detailed Findings

### Factual Accuracy
[Detailed analysis of factual claims]

### Legal Citations
[Analysis of legal authority citations]

### Arithmetic Validation
[Analysis of numerical accuracy]

### Source Quality
[Assessment of sources used]

### Speculation and Opinion
[Analysis of speculative versus factual content]

### Disclaimer Adequacy
[Assessment of disclaimers and qualifications]

---

## Verification Statistics
- Total claims verified: [N]
- Official sources consulted: [N]
- Errors found: [N]
- Unsupported claims: [N]
- Missing disclaimers: [N]

---

## Distribution Recommendation

- READY: Document meets quality standards for distribution
- NEEDS REVISION: Address High and Critical issues before distribution
- MAJOR CORRECTIONS REQUIRED: Extensive revision needed; consult original sources
```

## Severity taxonomy

### Critical

- **Factual errors**: incorrect dates, wrong article numbers, false statements
- **Arithmetic mistakes**: calculation errors, timeline mistakes, wrong percentages
- **Legal misstatements**: misrepresenting legal requirements or obligations
- **Attribution errors**: quotes or claims attributed to the wrong source

Action: correct before distribution.

### High

- **Missing critical disclaimers**: no legal advice disclaimer where needed
- **Regulatory uncertainty not disclosed**: unsettled law presented as certain
- **Jurisdiction ambiguity**: unclear which legal system applies
- **Outdated legal references**: citing superseded provisions

Action: correct before distribution.

### Moderate

- **Unsourced statistics**: numbers without attribution
- **Editorial framing as fact**: opinion presented as objective requirement
- **Vague language**: ambiguous terms that could mislead
- **Incomplete citations**: missing EUR-Lex references or official journal citations

Action: address to improve quality and credibility.

### Low

- **Minor inconsistencies**: small formatting or style issues
- **Optional enhancements**: additional context that would improve clarity
- **Stylistic preferences**: wording choices that could be improved

Action: optional improvement.

## Quality scoring

**5/5 Distribution Ready**
All factual claims verified with official sources. All legal citations confirmed accurate. All arithmetic independently validated. Appropriate disclaimers present. No Critical or High issues. Professional quality suitable for client or stakeholder distribution.

**4/5 Minor Revisions**
Factual claims verified but some Moderate issues found. May have unsourced statistics that should be added. Disclaimers adequate but could be enhanced. No Critical issues, only Moderate or Low severity.

**3/5 Needs Revision**
Some factual errors or unsupported claims found. Missing important disclaimers. High-severity issues present. Requires revision before distribution.

**2/5 Major Corrections Required**
Multiple factual errors identified. Significant legal citation problems. Critical issues present. Extensive revision needed.

**1/5 Not Distribution Ready**
Fundamental errors in core legal statements. Pervasive unsupported claims. Multiple Critical issues. Requires complete rework.

## Jurisdiction adaptation

The verifier is jurisdiction-agnostic. Adapt the source hierarchy and citation format to the relevant jurisdiction.

### EU and national EU Member State law

- Prioritize EUR-Lex and the relevant national official gazette
- Verify regulatory authority guidance (supervisory authorities, standards bodies, European institutions)
- Check national statutory citations using the jurisdiction's convention
- Verify transposition status for directives where national implementation is relevant

### Common law jurisdictions (UK, Ireland, US, Canada, Australia, etc.)

- Use government legislative databases (legislation.gov.uk, UK; congress.gov, US federal; etc.)
- Verify case law against authoritative reporters and databases
- Follow jurisdiction-specific citation conventions (OSCOLA, Bluebook, etc.)

### Other civil law jurisdictions

- Use national official legislative databases
- Verify court decisions against authoritative collections
- Follow the jurisdiction's citation conventions

## Known AI hallucination patterns

### Pattern 1: Plausible but wrong article numbers

Problem: AI generates realistic-sounding article citations that do not exist.
Example: "AI Act Article 42(5)" when AI Act Article 42 only has paragraphs (1) to (4).
Verification: check official source for exact article structure.

### Pattern 2: Confident but incorrect dates

Problem: AI states dates with confidence but gets them wrong.
Example: "NIS2 applies from October 2024" when the actual Member State transposition deadline was 17 October 2024 and national implementation dates vary.
Verification: independently verify all dates against official sources; distinguish between directive deadlines and national implementation dates.

### Pattern 3: Mixing guidance and legal requirements

Problem: AI presents regulatory guidance as legal obligation.
Example: Treating a standards body recommendation as a binding regulatory requirement.
Verification: distinguish between binding legal text and non-binding guidance.

### Pattern 4: Outdated legal references

Problem: AI cites superseded or amended provisions.
Example: Citing original text when the provision has been amended or authoritatively interpreted.
Verification: check for amendments, implementing acts, and authoritative interpretations.

### Pattern 5: Arithmetic errors in timeline calculation

Problem: AI makes mistakes calculating deadlines from effective dates.
Example: Claiming "18 months from October 2024 is March 2026" when the correct result is April 2026.
Verification: independently calculate all timelines.

### Pattern 6: Paraphrase presented as quote

Problem: AI reproduces a close paraphrase of regulatory text but wraps it in quotation marks, suggesting verbatim citation.
Example: Quoting "AI systems must be transparent" when the regulation says "AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent".
Verification: match quoted text character-by-character against the official source.

## Use case examples

### Example 1: In-house legal briefing

**Input**: AI-generated compliance briefing on NIS2 implementation timeline for entities operating in a specific Member State.
**Verification focus**:

- Verify all national implementing statute article references
- Check supervisory authority guidance citations and URLs
- Validate compliance deadlines and calculation from directive effective date
- Confirm entity categorization thresholds
- Verify authority statements

**Output**: Corrected briefing with verified sources, ready for stakeholder distribution.

### Example 2: Law firm client snapshot

**Input**: AI-drafted legal snapshot on Data Act Article 5 data portability requirements.
**Verification focus**:

- Verify Data Act article citations against EUR-Lex
- Confirm enforcement date calculation
- Validate technical requirements and specifications
- Check for appropriate "pending implementation" disclaimers where relevant
- Verify cross-references to other regulations (GDPR, AI Act, CRA)

**Output**: Client-ready snapshot with verified sources and appropriate legal disclaimers.

### Example 3: Regulatory update for stakeholders

**Input**: AI-generated summary of recent regulatory guidance publication.
**Verification focus**:

- Verify the publication exists and the date is correct
- Check all quoted guidance language against the original
- Validate interpretation of non-binding guidance versus legal requirements
- Ensure clear labeling of "recommendations" versus "obligations"
- Verify URLs to official publications

**Output**: Verified update with clear source attribution and regulatory status.

## Continuous improvement

As this skill is used, document new hallucination patterns encountered, refine the verification methodology based on findings, build a library of reliable sources for different legal areas, and track error types to identify systematic AI weaknesses.

---

## Process summary

This skill exists to verify, not to confirm. Every claim in the input document is treated as unverified until an official source backs it. Verified claims are reported with their source URL. Unverified claims are listed as unsupported. The final report categorizes issues by severity and gives an explicit distribution-readiness recommendation. When in doubt, the verifier errs toward flagging rather than passing.
