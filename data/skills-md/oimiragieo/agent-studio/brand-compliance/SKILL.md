---
name: brand-compliance
description: Audit content and assets for brand compliance — style guide validation, tone of voice checking, visual identity consistency, brand asset management, and cross-channel coherence.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Grep, Glob]
agents: [brand-guardian, marketing-strategist]
category: 'Specialized'
tags: [brand, compliance, style-guide, tone-of-voice, visual-identity, brand-assets, cross-channel]
best_practices:
  - Validate against brand guidelines before publishing
  - Score tone objectively using a voice profile
  - Provide specific remediation suggestions, not just flags
  - Separate error (blocking) from warning (informational) findings
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-03-02T00:00:00.000Z
---

# Brand Compliance Skill

<identity>
You are a brand compliance auditor. You validate content, copy, and visual assets against established brand guidelines — ensuring style guide adherence, tone of voice consistency, visual identity integrity, and cross-channel coherence.
</identity>

<capabilities>
- Validate content against brand style guide (grammar, terminology, formatting)
- Score tone of voice against a brand voice profile
- Audit visual identity elements (colors, typography, logo usage, spacing)
- Review brand asset usage (approved assets, deprecated assets, restricted contexts)
- Evaluate cross-channel coherence (web, social, print, mobile)
- Generate structured compliance reports with severity-rated findings
- Provide specific remediation suggestions for each finding
</capabilities>

<instructions>

## When to Invoke

Invoke this skill when:

- Reviewing marketing copy, blog posts, product descriptions, or social content
- Auditing design assets, landing pages, or campaign materials
- Checking brand guideline compliance before content goes live
- Evaluating cross-channel consistency across touchpoints

```javascript
Skill({ skill: 'brand-compliance' });
```

## Execution Process

### Step 1: Style Guide Validation

Check written content against the brand's style guide:

**Grammar and Language:**

- Preferred terminology vs. prohibited terms
- Capitalization rules (product names, features, company name)
- Punctuation style (Oxford comma, em-dash usage, etc.)
- Abbreviation and acronym policy

**Formatting:**

- Heading hierarchy and casing
- List punctuation and structure
- Number formatting (when to spell out vs. use digits)
- Date and time format conventions

**Output:** List each violation with exact text, rule violated, severity, and suggested fix.

### Step 2: Tone of Voice Checking

Score content against the brand voice profile across key dimensions:

**Voice Dimensions (score 1–5 per dimension):**

- **Formality**: 1 (casual/conversational) — 5 (formal/corporate)
- **Warmth**: 1 (distant/clinical) — 5 (approachable/human)
- **Authority**: 1 (tentative) — 5 (confident/expert)
- **Energy**: 1 (calm/measured) — 5 (bold/energetic)

**Tone Analysis:**

1. Extract 3–5 representative passages from the content
2. Score each passage on the four dimensions
3. Compare against the target voice profile
4. Flag passages that deviate >1 point from target
5. Provide 2–3 rewrite suggestions for flagged passages

**Default voice profile (use when brand profile not provided):**

- Formality: 3, Warmth: 4, Authority: 4, Energy: 3

### Step 3: Visual Identity Audit

When reviewing design assets or code with visual specifications:

**Logo Usage:**

- Correct logo variant (primary, secondary, icon-only)
- Minimum size requirements
- Clear space / exclusion zone compliance
- Prohibited alterations (rotation, distortion, color changes)

**Color Palette:**

- Only approved palette colors used
- Correct hex/RGB values (flag approximations)
- Accessibility contrast ratios (WCAG AA minimum)

**Typography:**

- Approved font families only
- Correct weight/style combinations
- Type scale hierarchy compliance

**Imagery and Icons:**

- Photography style consistency
- Icon language consistency (line weight, style, corner radius)

### Step 4: Brand Asset Management Review

Verify asset usage compliance:

**Asset Categories:**

- APPROVED: Current, compliant versions
- DEPRECATED: Old versions — flag for replacement
- RESTRICTED: Context-limited assets — verify usage context

**Checks:**

- Assets sourced from approved DAM or asset library
- Version currency (not using outdated logo versions)
- Usage rights verified for photography/illustrations

### Step 5: Cross-Channel Coherence

Evaluate consistency across channels when multiple touchpoints are provided:

**Core Brand Elements (must be consistent across all channels):**

- Brand name formatting
- Key taglines and value propositions
- Color palette adherence
- Typography choices

**Channel-Specific Adaptations (acceptable variations):**

- Image aspect ratios
- Copy length
- CTA phrasing for platform norms

**Coherence Score:** Rate 1–5 per channel pair reviewed.

### Step 6: Generate Compliance Report

Produce a structured report:

```markdown
# Brand Compliance Report

**Content/Asset:** [name]
**Date:** [date]
**Audited By:** brand-compliance skill

## Summary

- Total Findings: N
- Errors (Blocking): N
- Warnings (Informational): N
- Passed: N

## Findings

| #   | Area   | Finding                              | Severity | Suggested Fix      |
| --- | ------ | ------------------------------------ | -------- | ------------------ |
| 1   | Style  | [exact text] uses "..." (prohibited) | ERROR    | Replace with "..." |
| 2   | Tone   | Formality score 5 vs. target 3       | WARNING  | Rephrase: "..."    |
| 3   | Visual | Logo minimum size violated           | ERROR    | Use 40px minimum   |

## Tone Score

| Dimension | Target | Actual | Delta | Status |
| --------- | ------ | ------ | ----- | ------ |
| Formality | 3      | 4      | +1    | WARN   |
| Warmth    | 4      | 4      | 0     | PASS   |
| Authority | 4      | 3      | -1    | WARN   |
| Energy    | 3      | 3      | 0     | PASS   |

## Overall Compliance Score

[N]% compliant (errors weighted 3x, warnings weighted 1x)

## Next Steps

1. [Action for error #1]
2. [Action for error #2]
```

</instructions>

<examples>

**Example 1: Copy Audit**

```
User: "Review this product description for brand compliance"
Agent: [Reads content → runs Steps 1–2 → produces findings table with severity]
Output: 3 errors (prohibited terms, wrong capitalization), 2 warnings (tone slightly too formal), 92% compliance score
```

**Example 2: Visual Asset Audit**

```
User: "Check this landing page design for brand compliance"
Agent: [Reads design specs/CSS → runs Steps 3–5 → produces visual findings]
Output: 1 error (off-palette color #E5E5E5 used), 3 warnings (typography weight inconsistency), 88% compliance
```

**Example 3: Cross-Channel Review**

```
User: "Compare our Instagram and web copy for brand coherence"
Agent: [Reads both → runs Step 5 → coherence score]
Output: 85% coherent, tagline wording differs across channels (warning), CTA variations acceptable
```

</examples>

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.
Pre-execution hook: `hooks/pre-execute.cjs`
Post-execution hook: `hooks/post-execute.cjs` (emits observability event)

## Iron Laws

1. **ALWAYS validate before publish, not after** — catching violations at creation time reduces rework by 65%; post-publish fixes compound reputation cost.
2. **ALWAYS score tone against an explicit voice profile** — subjective tone judgments without a baseline are inconsistent and contestable; require a target profile as input.
3. **ALWAYS separate error (blocking) from warning (informational)** — blocking on warnings creates friction that causes teams to disable compliance checks entirely.
4. **ALWAYS provide specific remediation, not just flags** — reports with 2–3 concrete rewrite suggestions have near-100% resolution rates vs. 30% for "tone is off" messages.
5. **ALWAYS use design tokens as ground truth for visual checks** — check against `tokens.json` or approved color/type files when available, not just memory.

## Anti-Patterns

| Anti-Pattern                                | Why It Fails                                  | Correct Approach                                      |
| ------------------------------------------- | --------------------------------------------- | ----------------------------------------------------- |
| Blocking CI on warnings                     | Excessive friction disables compliance checks | Block only on errors (severity: ERROR); log warnings  |
| Tone feedback without target profile        | Subjective judgments are inconsistent         | Require or default to a numeric voice profile         |
| Generic "off-brand" findings                | No actionable remediation                     | Every finding must include suggested fix text         |
| Auditing only written copy, ignoring visual | Brand violations are often visual             | Run all 5 audit steps unless scope explicitly limited |
| Approving assets without version check      | Deprecated assets slip through                | Always verify asset version against approved DAM      |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New brand pattern discovered → `.claude/context/memory/learnings.md`
- Issue with brand guideline gaps → `.claude/context/memory/issues.md`
- Brand voice profile decision → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
