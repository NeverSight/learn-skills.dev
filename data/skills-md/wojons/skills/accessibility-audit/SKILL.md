---
name: accessibility-audit
description: Use when you need comprehensive accessibility auditing including WCAG compliance, legal requirements mapping, and user testing with disabilities
license: MIT
compatibility: opencode
metadata:
  audience: accessibility-specialists, developers, designers
  category: accessibility
---

# Accessibility Audit

Perform comprehensive accessibility audits that go beyond automated testing to include WCAG compliance verification, legal requirements mapping, user testing with disabilities, and actionable remediation guidance. This skill provides holistic accessibility assessment for digital products.

## When to use me

Use this skill when:
- You need a comprehensive accessibility audit beyond automated testing
- You're preparing for legal compliance (ADA, Section 508, AODA, EN 301 549)
- You need to map accessibility issues to specific WCAG success criteria
- You want to conduct user testing with people with disabilities
- You need to create accessibility statements and VPAT (Voluntary Product Accessibility Template) reports
- You're developing accessibility training and remediation plans
- You need to assess accessibility across multiple platforms (web, mobile, desktop)
- You want to establish accessibility benchmarks and maturity models

## What I do

- **WCAG compliance auditing**: Comprehensive auditing against WCAG 2.1/2.2 A, AA, AAA success criteria
- **Legal requirements mapping**: Map accessibility issues to legal requirements (ADA, Section 508, AODA, EU Web Accessibility Directive)
- **User testing coordination**: Plan and coordinate user testing with people with disabilities
- **Assistive technology testing**: Test with screen readers (NVDA, JAWS, VoiceOver), screen magnifiers, switch devices
- **Mobile accessibility auditing**: Audit mobile applications for accessibility (iOS, Android)
- **PDF/document accessibility**: Audit PDFs and documents for accessibility
- **VPAT report generation**: Generate Voluntary Product Accessibility Template reports
- **Remediation planning**: Create detailed remediation plans with priority and effort estimation
- **Accessibility maturity assessment**: Assess organizational accessibility maturity and capability
- **Training needs analysis**: Analyze accessibility training needs for development teams

## Examples

```bash
# Perform comprehensive WCAG audit
./scripts/analyze-accessibility.sh --wcag --level aa --output audit-report.json

# Generate VPAT report
./scripts/analyze-accessibility.sh --vpat --standard section508 --output vpat.docx

# Map issues to legal requirements
./scripts/analyze-accessibility.sh --legal-mapping --regulations ada section508

# Plan user testing with disabilities
./scripts/analyze-accessibility.sh --user-testing-plan --participants 5 --output plan.md

# Assess accessibility maturity
./scripts/analyze-accessibility.sh --maturity-assessment --output maturity-score.json
```

## Output format

```
Comprehensive Accessibility Audit Report
─────────────────────────────────────
Audit Date: 2025-01-15T10:30:00Z
Application: https://app.example.com
WCAG Version: 2.1
Compliance Level: AA

EXECUTIVE SUMMARY:
──────────────────
Overall Compliance Score: 68/100
Critical Issues: 42
Serious Issues: 89
Moderate Issues: 156
Minor Issues: 234

Legal Compliance Status:
• ADA Title III: Partially Compliant (High Risk)
• Section 508: Partially Compliant (Remediation Required)
• AODA: Not Compliant (Major Issues)
• EU Web Accessibility Directive: Partially Compliant

WCAG 2.1 AA COMPLIANCE BREAKDOWN:
─────────────────────────────────
Perceivable (Principle 1): 45% compliant
• 1.1 Text Alternatives: 12 failures
• 1.2 Time-based Media: 8 failures
• 1.3 Adaptable: 23 failures
• 1.4 Distinguishable: 18 failures

Operable (Principle 2): 62% compliant
• 2.1 Keyboard Accessible: 9 failures
• 2.2 Enough Time: 5 failures
• 2.3 Seizures and Physical Reactions: 1 failure
• 2.4 Navigable: 27 failures
• 2.5 Input Modalities: 15 failures

Understandable (Principle 3): 78% compliant
• 3.1 Readable: 8 failures
• 3.2 Predictable: 12 failures
• 3.3 Input Assistance: 9 failures

Robust (Principle 4): 85% compliant
• 4.1 Compatible: 7 failures

CRITICAL ISSUES BY IMPACT:
──────────────────────────
Screen Reader Users (High Impact):
• 18 images missing alt text (critical)
• 7 form fields missing labels (critical)
• 3 ARIA landmarks missing (serious)
• 5 dynamic content updates not announced (serious)

Keyboard Users (High Impact):
• 2 keyboard traps in modal dialogs (critical)
• 5 focus order inconsistencies (serious)
• 9 missing focus indicators (serious)

Low Vision Users (High Impact):
• 23 elements with insufficient color contrast (< 4.5:1) (critical)
• 8 text resize issues (serious)
• 12 spacing and line height issues (moderate)

Cognitive Disability Users (Medium Impact):
• 7 complex navigation structures (serious)
• 12 inconsistent labeling patterns (moderate)
• 9 missing error prevention (moderate)

Motor Disability Users (Medium Impact):
• 5 small touch targets (< 44x44px) (serious)
• 8 timing issues (moderate)
• 3 complex gestures required (moderate)

ASSISTIVE TECHNOLOGY TESTING RESULTS:
─────────────────────────────────────
Screen Readers:
• NVDA (Windows): 42 issues
• JAWS (Windows): 38 issues
• VoiceOver (macOS/iOS): 35 issues
• TalkBack (Android): 31 issues

Screen Magnifiers:
• ZoomText: 18 issues
• Windows Magnifier: 12 issues

Switch Devices:
• Single switch scanning: 8 issues
• Multiple switch scanning: 5 issues

Voice Control:
• Dragon NaturallySpeaking: 7 issues
• Windows Speech Recognition: 9 issues

MOBILE ACCESSIBILITY AUDIT:
───────────────────────────
iOS Application:
• VoiceOver compatibility: 65% compliant
• Dynamic Type support: 70% compliant
• Switch Control compatibility: 60% compliant

Android Application:
• TalkBack compatibility: 62% compliant
• Display size adjustment: 68% compliant
• Switch Access compatibility: 58% compliant

USER TESTING FINDINGS:
──────────────────────
Testing with 5 participants with disabilities:
• Participant 1 (Screen reader user): Completed 4/7 tasks successfully
• Participant 2 (Keyboard-only user): Completed 5/7 tasks successfully
• Participant 3 (Low vision user): Completed 3/7 tasks successfully
• Participant 4 (Motor disability user): Completed 4/7 tasks successfully
• Participant 5 (Cognitive disability user): Completed 2/7 tasks successfully

Key Usability Issues:
• Complex checkout process caused confusion for cognitive disability users
• Inconsistent navigation frustrated screen reader users
• Small touch targets caused errors for motor disability users
• Low contrast text reduced readability for low vision users

REMEDIATION ROADMAP:
────────────────────
Phase 1: Critical Fixes (1-2 weeks):
• Add alt text to 18 images
• Fix 2 keyboard traps in modal dialogs
• Improve color contrast for 23 elements
• Add labels to 7 form fields

Phase 2: Serious Issues (3-6 weeks):
• Fix focus order for 5 elements
• Add ARIA landmarks for 3 regions
• Increase touch target size for 5 elements
• Fix 8 dynamic content announcement issues

Phase 3: Moderate Issues (7-12 weeks):
• Simplify navigation structure
• Consistent labeling patterns
• Improve error prevention
• Enhance timing and gesture alternatives

Phase 4: Continuous Improvement (Ongoing):
• Establish accessibility training program
• Implement accessibility in CI/CD pipeline
• Regular user testing with disabilities
• Accessibility monitoring and reporting

ACCESSIBILITY MATURITY ASSESSMENT:
──────────────────────────────────
Current Maturity Level: 2/5 (Reactive)
• Policy: Basic accessibility policy exists
• Process: Ad-hoc accessibility testing
• Technology: Limited automated testing
• People: Limited accessibility expertise
• Culture: Accessibility seen as compliance requirement

Target Maturity Level: 4/5 (Proactive)
• Policy: Comprehensive accessibility policy with enforcement
• Process: Integrated accessibility in development lifecycle
• Technology: Comprehensive automated testing suite
• People: Dedicated accessibility team and training
• Culture: Accessibility embraced as core value

VPAT (SECTION 508) COMPLIANCE:
───────────────────────────────
Revised Section 508 Standards:
• 501 (Software) - Partially Supports
• 502 (Web) - Partially Supports
• 503 (Documentation) - Supports
• 504 (Support Services) - Supports with Exceptions

Estimated Remediation Cost: $45,000 - $65,000
Estimated Timeline: 3-6 months
Return on Investment: Improved usability, reduced legal risk, expanded market reach
```

## Notes

- Automated tools catch only 30-40% of accessibility issues; manual testing is essential
- Legal requirements vary by jurisdiction; consult legal counsel for compliance
- User testing with people with disabilities provides invaluable insights
- Accessibility is not a one-time project but an ongoing commitment
- Consider the full spectrum of disabilities: visual, auditory, motor, cognitive, speech
- Mobile accessibility requires platform-specific testing and considerations
- Document accessibility (PDF, Word, Excel) often requires separate tools and expertise
- VPAT reports require careful documentation and accuracy for procurement purposes
- Accessibility maturity models help organizations progress from reactive to proactive approaches