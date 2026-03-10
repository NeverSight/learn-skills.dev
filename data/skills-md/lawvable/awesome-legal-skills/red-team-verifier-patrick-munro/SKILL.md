---
name: red-team-verifier-patrick-munro
description: Adversarial verification for AI-generated legal content with systematic fact-checking, source validation, and quality control. Use when User requests verification of legal documents, fact-checking of regulatory content, red team review, or quality assurance before distribution to clients/stakeholders. Provides structured verification reports with severity-categorized errors, verified sources, and distribution readiness assessment.
metadata:
  author: Patrick Munro
  license: AGPL-3.0
  version: 2026.02.17
---

# Legal Red Team Verifier

## Purpose

This skill provides systematic adversarial verification of AI-generated legal content to ensure factual accuracy, proper legal citations, and appropriate disclaimers before distribution to clients or stakeholders. It addresses the #1 concern about AI in legal practice: "How do I know this is accurate?"

## When to Use This Skill

Use the Legal Red Team Verifier when User requests:
- Verification of AI-generated legal content before client/stakeholder distribution
- Fact-checking of legal snapshots, briefings, or analyses
- Quality control on compliance documents, regulatory summaries, or legal reports
- Red team review of legal outputs (e.g., "verify this", "fact-check this", "red team this document")
- Adversarial testing of legal claims or arguments

**Trigger phrases**: "verify", "fact-check", "red team", "check accuracy", "validate sources", "quality control", "is this correct", "review for errors"

## Core Verification Categories

### 1. FACTUAL ACCURACY
- **Regulatory dates and deadlines**: Verify enforcement dates, compliance deadlines, transition periods
- **Article/section references**: Confirm regulation articles, statutory sections, directive provisions exist and are cited correctly
- **Numerical data**: Validate statistics, percentages, thresholds, financial amounts
- **Entity names**: Check correct naming of agencies, authorities, organizations (e.g., BaFin, ESTI, ENISA, European Commission)
- **Timeline accuracy**: Verify historical events, legislative milestones, implementation schedules

### 2. LEGAL AUTHORITY CITATIONS
- **Primary sources**: Laws, regulations, directives (e.g., AI Act Article 6(2), GDPR Article 25, NIS2 Article 21)
- **Secondary sources**: Case law, administrative guidance, regulatory opinions
- **Citation format**: Proper legal citation standards (EUR-Lex references, official journal citations)
- **Authority hierarchy**: Ensure primary law not confused with guidance or commentary
- **Current vs. superseded**: Verify using current version, not outdated provisions

### 3. ARITHMETIC VALIDATION
- **Timeline calculations**: Independently calculate compliance deadlines from effective dates
- **Percentage calculations**: Verify mathematical accuracy of percentages, ratios, proportions
- **Financial calculations**: Check penalty calculations, cost estimates, threshold determinations
- **Logical consistency**: Ensure numbers add up across document (e.g., if mentioning "3 categories" verify exactly 3 are listed)

### 4. SOURCE VERIFICATION
- **Verifiable claims**: Every factual claim must link to a verifiable source
- **Official sources prioritized**: EUR-Lex, official gazettes, government websites, regulatory authority publications
- **No unsourced statistics**: Flag any statistical claim without attribution
- **No unsourced quotes**: Every quote must have proper attribution
- **Cross-referencing**: Critical claims verified against multiple independent sources

### 5. SPECULATION DETECTION
- **Opinion vs. fact**: Clearly distinguish editorial opinion from factual legal requirements
- **Uncertainty acknowledgment**: Identify areas where legal interpretation is unsettled or debated
- **Predictive claims**: Flag statements about future regulatory developments as speculation
- **"Likely" and "probably"**: Ensure speculative language is clearly labeled as such
- **Editorial framing**: Identify where AI has inserted interpretive framing not present in source material

### 6. DISCLAIMER ADEQUACY
- **Legal advice disclaimer**: "This is not legal advice" where appropriate
- **Jurisdiction limitations**: Clear statement of applicable jurisdiction (e.g., "Based on German/EU law")
- **Date/version disclaimer**: Document version/date of regulations cited
- **Professional consultation**: Recommendation to consult qualified legal professionals for specific situations
- **Regulatory uncertainty**: Disclosure where regulation is pending, in draft, or interpretation unclear

## Verification Methodology

### STEP 1: Initial Content Review
- Read entire document to understand scope and claims
- Identify all factual claims, legal citations, numerical data, and authoritative statements
- Note any missing sources, vague language, or unsupported assertions

### STEP 2: Source Verification (ALWAYS ONLINE)
- **MANDATORY**: Use web_search for EVERY factual claim, legal citation, and statistical assertion
- Prioritize official sources:
  - EUR-Lex (https://eur-lex.europa.eu) for EU legislation
  - Official government websites (.gov, .gov.uk, .bund.de, .europa.eu)
  - Regulatory authority sites (BaFin, ESTI, ENISA, BSI)
  - Official gazettes and legal databases
- Cross-reference critical claims across multiple sources
- Document source URLs for all verified facts

### STEP 3: Arithmetic Verification
- Independently calculate all timelines, deadlines, and dates
- Verify all percentages, ratios, and financial figures
- Check internal consistency (e.g., if document says "3 types" verify exactly 3 are listed)
- Flag any mathematical errors or inconsistencies

### STEP 4: Citation Validation
- Verify article/section numbers exist in cited regulations
- Check that citations match current versions (not superseded provisions)
- Ensure proper legal citation format
- Confirm quotes are accurate (not paraphrased but presented as quotes)

### STEP 5: Speculation Identification
- Flag any predictive statements about regulatory developments
- Identify editorial opinions presented as facts
- Note areas of legal uncertainty or debate
- Ensure speculative content is clearly labeled

### STEP 6: Disclaimer Review
- Check for legal advice disclaimers
- Verify jurisdiction is clearly stated
- Ensure date/version of regulations is specified
- Confirm recommendation for professional consultation where appropriate

## Output Structure

Provide verification results in the following structured format:

```
# LEGAL RED TEAM VERIFICATION REPORT

## Document Analyzed
[Title/description of content verified]

## Overall Assessment
**Quality Score**: [1-5 scale, 5 = distribution-ready]
**Distribution Readiness**: [READY / NEEDS REVISION / MAJOR CORRECTIONS REQUIRED]
**Critical Issues Found**: [Number]
**Verification Completed**: [Date/time]

---

## ✅ VERIFIED FACTS
[List all factual claims successfully verified with sources]
- Claim: [statement]
  Source: [official source URL]
  Status: ✅ VERIFIED

---

## ❌ ERRORS REQUIRING CORRECTION

### CRITICAL (Immediate correction required)
- **Error**: [Description of factual error, legal misstatement, or arithmetic mistake]
  **Location**: [Where in document]
  **Correction**: [What should it say]
  **Source**: [Correct source URL]

### HIGH (Correction strongly recommended)
- **Issue**: [Missing critical disclaimer, regulatory uncertainty not disclosed]
  **Impact**: [Why this matters]
  **Recommendation**: [Suggested addition/revision]

### MODERATE (Should be addressed)
- **Issue**: [Unsourced statistics, editorial framing as fact]
  **Impact**: [Credibility/accuracy concern]
  **Recommendation**: [How to improve]

### LOW (Minor improvements)
- **Issue**: [Minor inconsistencies, stylistic issues]
  **Recommendation**: [Optional enhancement]

---

## ⚠️ UNSUPPORTED CLAIMS
[Claims requiring verification or removal]
- **Claim**: [Statement made without source]
  **Status**: Could not verify through official sources
  **Action Required**: Either provide source or remove claim

---

## 📋 MISSING DISCLAIMERS
[Recommended disclaimer additions]
- **Location**: [Where to add]
  **Type**: [Legal advice / Jurisdiction / Date-version / Professional consultation]
  **Suggested Language**: [Specific disclaimer text]

---

## 🎯 DETAILED FINDINGS

### Factual Accuracy
[Detailed analysis of factual claims]

### Legal Citations
[Analysis of legal authority citations]

### Arithmetic Validation
[Analysis of numerical accuracy]

### Source Quality
[Assessment of sources used]

### Speculation & Opinion
[Analysis of speculative vs. factual content]

### Disclaimer Adequacy
[Assessment of disclaimers and qualifications]

---

## 📊 VERIFICATION STATISTICS
- Total claims verified: [N]
- Official sources consulted: [N]
- Errors found: [N]
- Unsupported claims: [N]
- Missing disclaimers: [N]

---

## RECOMMENDATIONS FOR DISTRIBUTION

**If READY**: Document meets quality standards for distribution
**If NEEDS REVISION**: Address HIGH and CRITICAL issues before distribution
**If MAJOR CORRECTIONS REQUIRED**: Extensive revision needed; consult original sources
```

## Severity Taxonomy

### CRITICAL
- **Factual errors**: Incorrect dates, wrong article numbers, false statements
- **Arithmetic mistakes**: Calculation errors, timeline mistakes, wrong percentages
- **Legal misstatements**: Misrepresenting legal requirements or obligations
- **Attribution errors**: Quotes or claims attributed to wrong source

**Action**: MUST correct before distribution

### HIGH
- **Missing critical disclaimers**: No legal advice disclaimer where needed
- **Regulatory uncertainty not disclosed**: Presenting unsettled law as certain
- **Jurisdiction ambiguity**: Not clear what legal system applies
- **Outdated legal references**: Citing superseded provisions

**Action**: STRONGLY RECOMMEND correction before distribution

### MODERATE
- **Unsourced statistics**: Numbers without attribution
- **Editorial framing as fact**: Opinion presented as objective requirement
- **Vague language**: Ambiguous terms that could mislead
- **Incomplete citations**: Missing EUR-Lex references or official journal citations

**Action**: SHOULD address to improve quality and credibility

### LOW
- **Minor inconsistencies**: Small formatting or style issues
- **Optional enhancements**: Additional context that would improve clarity
- **Stylistic preferences**: Wording choices that could be improved

**Action**: OPTIONAL improvement

## Use Case Examples

**Output**: Client-ready snapshot with verified sources and appropriate legal disclaimers

### Example 3: Regulatory Update for Stakeholders
**Input**: AI-generated summary of recent ENISA NIS2 guidelines
**Verification Focus**:
- Verify ENISA publication exists and date is correct
- Check all quoted guidance language against original
- Validate interpretation of non-binding guidance vs. legal requirements
- Ensure clear labeling of "recommendations" vs. "obligations"
- Verify URLs to official ENISA publications

**Output**: Verified update with clear source attribution and regulatory status

## Critical Requirements

### ALWAYS Verify Online
- NEVER rely solely on AI-generated content or memory
- ALWAYS use web_search to verify factual claims against official sources
- NEVER assume dates, article numbers, or legal citations are correct without verification
- ALWAYS cross-reference critical claims across multiple sources

### Source Hierarchy
1. **Primary legal sources**: Official legislation (EUR-Lex, official gazettes)
2. **Official guidance**: Regulatory authority publications (BaFin, ENISA, BSI, European Commission)
3. **Secondary legal sources**: Court decisions, legal commentary
4. **Tertiary sources**: News articles, blog posts (use with extreme caution)

### Transparency Requirements
- ALWAYS provide source URLs for verified facts
- ALWAYS acknowledge when claims cannot be verified
- ALWAYS disclose areas of legal uncertainty or debate
- NEVER present speculation as fact

## Adversarial Mindset

When performing verification, adopt an adversarial stance:
- **Assume error until proven correct**: Don't trust AI-generated content
- **Seek contradictory evidence**: Actively look for information that contradicts claims
- **Question every number**: Independently verify all calculations
- **Demand sources**: Every factual claim must have verifiable attribution
- **Test logical consistency**: Look for internal contradictions
- **Challenge interpretations**: Where AI presents legal interpretation, verify against authoritative sources

## Quality Standards

**5/5 - Distribution Ready**
- All factual claims verified with official sources
- All legal citations confirmed accurate
- All arithmetic independently validated
- Appropriate disclaimers present
- No critical or high-severity issues
- Professional quality suitable for client/stakeholder distribution

**4/5 - Minor Revisions**
- Factual claims verified but some moderate issues found
- May have unsourced statistics that should be added
- Disclaimers adequate but could be enhanced
- No critical issues, only moderate or low severity

**3/5 - Needs Revision**
- Some factual errors or unsupported claims found
- Missing important disclaimers
- High-severity issues present
- Requires revision before distribution

**2/5 - Major Corrections Required**
- Multiple factual errors identified
- Significant legal citation problems
- Critical issues present
- Extensive revision needed

**1/5 - Not Distribution Ready**
- Fundamental errors in core legal statements
- Pervasive unsupported claims
- Multiple critical issues
- Requires complete rework

## Customization by Jurisdiction

### EU/German Law Focus
- Prioritize EUR-Lex, German official gazettes (BGBl)
- Verify BaFin, BSI, ENISA guidance
- Check German statutory citations (BGB, BDSG, GeschGehG, etc.)
- Verify EU directive transposition status for Germany

### General Legal Verification
- Adapt source hierarchy to relevant jurisdiction
- Use appropriate official sources (gov websites, legal databases)
- Adjust citation formats to jurisdiction standards
- Modify disclaimer language as appropriate

## Examples of Known AI Hallucination Patterns

### Pattern 1: Plausible but Wrong Article Numbers
**Problem**: AI generates realistic-sounding article citations that don't exist
**Example**: "AI Act Article 42(5)" when AI Act only has Article 42(1)-(4)
**Verification**: Always check official EUR-Lex text for exact article structure

### Pattern 2: Confident but Incorrect Dates
**Problem**: AI states dates with confidence but gets them wrong
**Example**: "NIS2 applies from October 2024" when actual date is October 17, 2024
**Verification**: Independently verify all dates against official sources

### Pattern 3: Mixing Guidance and Legal Requirements
**Problem**: AI presents regulatory guidance as legal obligation
**Example**: Treating ENISA recommendations as binding NIS2 requirements
**Verification**: Distinguish between binding legal text and non-binding guidance

### Pattern 4: Outdated Legal References
**Problem**: AI cites superseded or amended provisions
**Example**: Citing original GDPR text when regulation has been practically interpreted by CJEU
**Verification**: Check for amendments, implementing acts, and authoritative interpretations

### Pattern 5: Arithmetic Errors in Timeline Calculation
**Problem**: AI makes mistakes calculating deadlines from effective dates
**Example**: Claiming "18 months from October 2024 is March 2026" (actually April 2026)
**Verification**: Independently calculate all timelines

## Continuous Improvement

As you use this skill:
- **Document new hallucination patterns** encountered
- **Refine verification methodology** based on findings
- **Build library of reliable sources** for different legal areas
- **Track error types** to identify systematic AI weaknesses
- **Share learnings** to improve legal AI verification practices

---

## Critical Reminder

**The purpose of this skill is adversarial verification**. Approach every AI-generated legal claim with skepticism. Your role is not to confirm what the AI said, but to independently verify whether it's accurate, properly sourced, and appropriately disclaimed. When in doubt, verify. When you can't verify, flag it. Better to over-verify than to distribute inaccurate legal information.
