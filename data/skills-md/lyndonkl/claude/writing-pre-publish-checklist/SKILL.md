---
name: writing-pre-publish-checklist
description: Use when performing final quality checks before sharing or publishing writing. Invoke when user mentions pre-publish, final check, ready to publish, last review, quality check before sending, about to share, or wants a comprehensive checklist run on a finished piece.
---

# Writing Pre-Publishing Checklist

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Check Details](#check-details)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill runs a comprehensive six-section quality checklist before writing is shared or published. It covers content accuracy, structural integrity, clarity, style consistency, polish, and final read-aloud tests. This is the last gate before publishing - it catches issues that revision and stickiness enhancement might miss.

## When to Use

Use this skill when:

- **About to publish**: User is ready to share or publish a piece
- **Final review**: Writing has been revised and user wants a last check
- **Quality gate**: User wants systematic verification before sending
- **Second opinion**: User wants another set of eyes on finished work
- **Submission prep**: About to submit to editor, client, or publication

Trigger phrases: "ready to publish", "final check", "pre-publish", "before I send this", "last review", "is this ready?", "quality check", "submission ready", "about to share"

**Do NOT use for:**
- Planning structure (use `writing-structure-planner`)
- Deep revision of prose (use `writing-revision`)
- Making messages memorable (use `writing-stickiness`)

## Core Principles

1. **Systematic, not subjective**: Follow the checklist completely, don't skip sections
2. **Fresh eyes perspective**: Read as if seeing the piece for the first time
3. **Binary decisions**: Each check item is pass/fail, not "sort of"
4. **Flag, don't fix**: Identify issues and present to user rather than silently fixing
5. **Final gate, not revision**: This catches remaining issues, not does deep rewriting

## Workflow

Copy this checklist and track your progress:

```
Pre-Publishing Checklist:
- [ ] Section 1: Content check
- [ ] Section 2: Structure check
- [ ] Section 3: Clarity check
- [ ] Section 4: Style check
- [ ] Section 5: Polish check
- [ ] Section 6: Final tests
```

**Before starting:** This is a systematic pass through the complete piece. Read the ENTIRE document first to understand context, then work through each section.

### Section 1: Content Check

Step 1.1: Read the entire piece. Identify the core message. Verify core message is crystal clear - could a reader state it back in one sentence?

Step 1.2: Check all facts for accuracy. Flag any claims that need verification. Note any statistics, dates, names, or specific details that should be double-checked with the user.

Step 1.3: Evaluate examples and evidence. Are examples relevant and appropriate for the audience? Are arguments sound and complete? Is there any missing information that would leave readers with unanswered questions?

Present Content Check results:
```
Content Check:
- [ ] Core message crystal clear
- [ ] All facts checked for accuracy
- [ ] Examples relevant and appropriate
- [ ] Arguments sound and complete
- [ ] No missing information
Issues found: [list any issues]
```

### Section 2: Structure Check

Step 2.1: Evaluate the opening. Does it hook readers? Would someone continue reading after the first paragraph?

Step 2.2: Check flow and transitions. Is the logical flow smooth throughout? Do transitions between sections work? Are there any jarring jumps?

Step 2.3: Examine the middle and ending. Does the middle section have gold-coin moments (rewards for the reader)? Does the conclusion satisfy - does it deliver on the promise of the opening?

Present Structure Check results:
```
Structure Check:
- [ ] Opening hooks readers
- [ ] Flow is logical and smooth
- [ ] Transitions work smoothly
- [ ] Middle section has gold coins
- [ ] Conclusion satisfies
Issues found: [list any issues]
```

### Section 3: Clarity Check

Step 3.1: Scan for jargon. Is all jargon either removed or explained? Is it appropriate for the target audience?

Step 3.2: Check for ambiguity. Are there ambiguous pronouns? Garden-path sentences that require re-reading? Any sentences where meaning is unclear?

Step 3.3: Verify audience fit. Is technical accuracy maintained? Is the level of detail appropriate for the target audience?

Present Clarity Check results:
```
Clarity Check:
- [ ] No jargon (or all jargon explained)
- [ ] No ambiguous pronouns
- [ ] No garden-path sentences
- [ ] Technical accuracy maintained
- [ ] Appropriate for target audience
Issues found: [list any issues]
```

### Section 4: Style Check

Step 4.1: Verify tone consistency. Is the tone consistent throughout? Does it shift inappropriately between sections?

Step 4.2: Check voice and sentence variety. Is the voice appropriate for the audience and purpose? Is there good sentence variety (mix of short, medium, long)? Rate sentence variety on a 1-10 scale (target 7+).

Step 4.3: Scan for remaining clutter. Is there any clutter that should have been caught in revision? Does active voice predominate?

Present Style Check results:
```
Style Check:
- [ ] Tone is consistent
- [ ] Voice is appropriate
- [ ] Sentence variety is good (score: X/10)
- [ ] No clutter remains
- [ ] Active voice predominates
Issues found: [list any issues]
```

### Section 5: Polish Check

Step 5.1: Check mechanics. Scan for spelling errors, grammar issues, and punctuation problems.

Step 5.2: Verify formatting. Is formatting consistent throughout (headings, lists, emphasis, spacing)? Do links work (if applicable)?

Present Polish Check results:
```
Polish Check:
- [ ] Spelling checked
- [ ] Grammar correct
- [ ] Punctuation proper
- [ ] Formatting consistent
- [ ] Links work (if applicable)
Issues found: [list any issues]
```

### Section 6: Final Tests

Step 6.1: Read-aloud test. Read the piece aloud (or simulate reading aloud). Flag any sections that sound awkward, trip over themselves, or lose momentum.

Step 6.2: Intent test. Does the piece achieve its stated intent? Does it satisfy the target audience's needs?

Step 6.3: Pride test. Present the overall assessment - is this piece ready for its intended audience? Note any remaining concerns.

Present Final Tests results:
```
Final Tests:
- [ ] Read aloud - sounds good
- [ ] Achieves stated intent
- [ ] Satisfies target audience needs
- [ ] Ready for publication
Overall assessment: [PASS / PASS WITH NOTES / NEEDS REVISION]
```

### Final Summary

Present the complete checklist results in a single summary:

```
Pre-Publishing Checklist Summary:
================================
Content:   [PASS/FAIL] - [brief note]
Structure: [PASS/FAIL] - [brief note]
Clarity:   [PASS/FAIL] - [brief note]
Style:     [PASS/FAIL] - [brief note]
Polish:    [PASS/FAIL] - [brief note]
Final:     [PASS/FAIL] - [brief note]

Overall:   [READY TO PUBLISH / NEEDS ATTENTION]

Issues requiring action:
1. [issue]
2. [issue]
```

Validate using [resources/evaluators/rubric_pre_publish.json](resources/evaluators/rubric_pre_publish.json). **Minimum standard**: Average score >= 3.5.

## Check Details

| Section | Focus | Key Questions |
|---------|-------|---------------|
| Content | Accuracy & completeness | Is the core message clear? Facts correct? |
| Structure | Organization & flow | Does it hook, flow, and satisfy? |
| Clarity | Readability | Can audience understand without re-reading? |
| Style | Consistency & voice | Is tone consistent? Voice appropriate? |
| Polish | Mechanics | Spelling, grammar, punctuation, formatting? |
| Final | Overall quality | Read-aloud test? Achieves intent? |

## Guardrails

**Critical requirements:**

1. **Complete all 6 sections**: Don't skip sections even if the writing seems good
2. **Binary pass/fail**: Each checklist item gets a clear pass or fail, not "maybe"
3. **Flag to user**: Present issues for the user to address rather than silently fixing
4. **Context-aware**: Adjust standards to context (blog post vs. academic paper vs. email)
5. **Honest assessment**: Give genuine feedback even if it means more work is needed

**Common pitfalls:**
- Rubber-stamping everything as "pass" without careful review
- Skipping the read-aloud test (it catches issues nothing else does)
- Not adjusting standards for the specific publication context
- Trying to do deep revision instead of flagging issues
- Missing formatting inconsistencies in longer pieces

## Quick Reference

**Key resources:**
- **[resources/evaluators/rubric_pre_publish.json](resources/evaluators/rubric_pre_publish.json)**: Quality scoring criteria

**Inputs required:**
- Finished or near-finished piece of writing
- Target audience and publication context
- Stated intent or core message

**Outputs produced:**
- Complete 6-section checklist with pass/fail for each item
- List of issues requiring attention
- Overall publication readiness assessment
