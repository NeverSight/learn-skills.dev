---
name: dan-koe-validator
description: Validates and edits articles to match Dan Koe's writing style. Use when reviewing content for Koe-style voice, structure, or philosophy alignment. Triggers on requests to "validate article," "edit in Dan Koe style," "check if this sounds like Koe," "review my newsletter," or any content review against the Koe framework.
---

# Dan Koe Article Validator

Validates articles against Dan Koe's writing style, providing specific edits and scoring.

## Validation Workflow

1. **Read the style guide** → Load `references/style-guide.md` for comprehensive style rules
2. **Analyze the article** → Score against 7 dimensions
3. **Provide specific edits** → Line-by-line rewrites, not vague suggestions
4. **Deliver verdict** → Pass/Fail with actionable next steps

## Quick Reference: The Koe Voice

**Core traits:**
- Direct second-person address ("You" is the most common word)
- Declarative assertions, zero hedging (no "I think," "perhaps," "maybe")
- Reframes mainstream concepts through new definitions
- Warm but uncompromising — challenges without condescension
- Anti-guru positioning — earned confidence, not credential-based authority

**Structural signatures:**
- Problem → Amplification → Reframe → Framework → (Soft CTA)
- Roman numerals or numbered sections for major breaks
- Short paragraphs (1-3 sentences typical)
- Single-line sentences for emphasis
- Questions as transitions between sections

**What Koe never does:**
- Uses emojis
- Hedges with qualifiers
- Cites academic studies or statistics
- Uses passive voice
- Entertains for entertainment's sake (no jokes, no banter)
- Writes bullet points without development (each point = paragraph)

## Scoring Dimensions

Rate each 1-10, then average for overall score:

| Dimension | What to evaluate |
|-----------|------------------|
| **Voice** | Second-person, declarative, zero hedging |
| **Structure** | Problem-amplify-reframe pattern, clear sections |
| **Conviction** | Assertions stated as facts, not opinions |
| **Conceptual depth** | Redefines terms, introduces frameworks |
| **Rhythm** | Short paragraphs, white space, sentence variety |
| **Philosophy alignment** | Agency, anti-conformity, entrepreneurship-as-nature |
| **Practical utility** | Frameworks readers can apply, not just ideas |

**Passing threshold:** 7.0+ overall

## Output Format

```markdown
## DAN KOE STYLE VALIDATION

### Overall Score: X.X/10 — [PASS/FAIL]

### Dimension Scores
- Voice: X/10 — [one-line rationale]
- Structure: X/10 — [one-line rationale]
- Conviction: X/10 — [one-line rationale]
- Conceptual Depth: X/10 — [one-line rationale]
- Rhythm: X/10 — [one-line rationale]
- Philosophy Alignment: X/10 — [one-line rationale]
- Practical Utility: X/10 — [one-line rationale]

### Critical Issues (if any)
[List dealbreakers that must be fixed]

### Specific Edits

**Line X:** [Original text]
→ [Rewritten in Koe voice]
Rationale: [Why this change]

[Repeat for each edit]

### Verdict
[2-3 sentences on whether to publish, major changes needed, or pass]
```

## Detailed Style Reference

For comprehensive rules, examples, and anti-patterns, read:
- `references/style-guide.md` — Full voice and structure breakdown
- `references/validation-examples.md` — Before/after edit examples

Always load the style guide before validating. It contains the complete definition derived from Koe's books and newsletters.
