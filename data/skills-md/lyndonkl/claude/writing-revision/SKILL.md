---
name: writing-revision
description: Use when revising, editing, or polishing an existing draft. Invoke when user mentions revision, editing, cutting clutter, tightening prose, improving readability, fixing rhythm, reducing word count, or improving an existing piece of writing.
---

# Writing Revision (Three-Pass System)

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Pass Overview](#pass-overview)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill applies a systematic three-pass revision system drawn from Zinsser, King, Pinker, and Clark. Each pass has a single focus: Pass 1 cuts clutter (make it lean), Pass 2 reduces cognitive load (make it readable), Pass 3 improves rhythm (make it flow). Multiple focused passes produce better results than one comprehensive revision.

## When to Use

Use this skill when:

- **Revising a draft**: User has written content that needs improvement
- **Tightening prose**: User wants to cut word count or eliminate clutter
- **Improving readability**: Text is hard to follow or requires re-reading
- **Enhancing flow**: Writing feels choppy, monotonous, or lacks rhythm
- **Polishing before publishing**: Final quality improvement pass on prose

Trigger phrases: "revise", "edit my draft", "tighten this", "cut clutter", "too wordy", "improve readability", "fix the flow", "polish", "make it better", "reduce word count", "too long"

**Do NOT use for:**
- Planning structure from scratch (use `writing-structure-planner`)
- Making messages memorable (use `writing-stickiness`)
- Final publishing checklist (use `writing-pre-publish-checklist`)

## Core Principles

1. **One focus per pass**: Don't try to fix everything at once - each pass targets one dimension
2. **Cut 10-25%**: King's formula - second draft equals first draft minus 10-25%
3. **Every word earns its place**: If a word doesn't contribute, remove it
4. **First reading is correct reading**: Readers shouldn't need to re-read sentences (Pinker)
5. **Rhythm creates engagement**: Varied sentence lengths and strong endings keep readers moving

## Workflow

Copy this checklist and track your progress:

```
Three-Pass Revision:
- [ ] Pass 1: Cut clutter (analyze -> improve)
- [ ] Pass 2: Reduce cognitive load (analyze -> improve)
- [ ] Pass 3: Improve rhythm (analyze -> improve)
```

**Before starting:** Review [resources/revision-guide.md](resources/revision-guide.md) for the complete three-pass system with examples and the full transformation demonstration.

**IMPORTANT:** For each pass, analyze the ENTIRE draft first and output findings to an analysis file in the current directory, then read that file to make improvements. This ensures complete coverage.

### Pass 1: Cut Clutter (Zinsser/King)

**Goal:** Cut 10-25% of word count. Make every word earn its place.

Step 1.1 - Analysis: Read ENTIRE draft. Create analysis file `writer-pass1-clutter-analysis.md` identifying ALL instances of: adverbs (-ly words), qualifiers (very, really, quite, somewhat), passive voice, weak verbs (is, are, was, were, has/have/had), throat-clearing phrases, and cliches. Calculate word count and set target for 10-25% reduction.

Step 1.2 - Improvement: Read analysis file. Work through ENTIRE draft making improvements: remove 70% of adverbs, delete qualifiers, convert passive to active voice, replace weak verbs with action verbs, eliminate throat-clearing, remove cliches. Verify word count reduction meets 10-25% target. Ensure every remaining word earns its place.

See [resources/revision-guide.md - Pass 1](resources/revision-guide.md#pass-1-cut-clutter-zinsserking) for detailed examples.

### Pass 2: Reduce Cognitive Load (Pinker)

**Goal:** Make reading effortless. First reading should be correct reading.

Step 2.1 - Analysis: Read ENTIRE draft. Create analysis file `writer-pass2-cognitive-load-analysis.md` identifying ALL issues: garden-path sentences (temporarily mislead readers), buried topics, subject-verb-object separated by more than 7 words, ambiguous pronouns, broken topic chains, sentences requiring re-reading.

Step 2.2 - Improvement: Read analysis file. Work through ENTIRE draft: fix garden-path sentences, signal topic at start of each sentence, keep subject-verb-object close, clarify pronouns, repair topic chains, break overly complex sentences. Read aloud to verify no stumbles.

See [resources/revision-guide.md - Pass 2](resources/revision-guide.md#pass-2-reduce-cognitive-load-pinker) for detailed examples.

### Pass 3: Improve Rhythm (Clark)

**Goal:** Create engaging flow through sentence variety and strong endings.

Step 3.1 - Analysis: Read ENTIRE draft. Create analysis file `writer-pass3-rhythm-analysis.md` analyzing: sentence lengths for each paragraph (list actual lengths), monotonous patterns (5+ similar-length sentences in a row), last word of each sentence (mark weak endings), gold-coin placement (identify gaps), opportunities for ladder of abstraction (concrete -> general -> concrete), sections lacking variety.

Step 3.2 - Improvement: Read analysis file. Work through ENTIRE draft: add short sentences for emphasis after longer ones, replace weak sentence endings with strong words, distribute gold-coin moments throughout (especially middle), apply ladder of abstraction, vary sentence lengths deliberately. Read aloud to verify flow. Confirm good mix of short, medium, and long sentences.

See [resources/revision-guide.md - Pass 3](resources/revision-guide.md#pass-3-improve-rhythm-clark) for detailed examples.

Validate using [resources/evaluators/rubric_revision.json](resources/evaluators/rubric_revision.json). **Minimum standard**: Average score >= 3.5.

## Pass Overview

| Pass | Focus | Method | Target |
|------|-------|--------|--------|
| Pass 1 | Clutter | Zinsser/King | Cut 10-25% word count |
| Pass 2 | Cognitive Load | Pinker | No re-reading needed |
| Pass 3 | Rhythm | Clark | Varied lengths, strong endings |

## Guardrails

**Critical requirements:**

1. **Preserve meaning**: Never change the author's intended meaning while cutting or restructuring
2. **Analyze before improving**: Always create the analysis file first, then make improvements based on findings
3. **Complete coverage**: Analyze the ENTIRE draft in each pass, not just the first few paragraphs
4. **Measure reduction**: Track actual word count reduction in Pass 1 (target 10-25%)
5. **Read aloud**: After Passes 2 and 3, verify by reading aloud for stumbles and rhythm

**Common pitfalls:**
- Trying to fix everything in one pass (stick to one focus per pass)
- Only revising the opening paragraphs and losing steam
- Cutting so aggressively that voice is lost
- Not tracking actual word count reduction
- Skipping the analysis phase and jumping straight to editing

## Quick Reference

**Key resources:**
- **[resources/revision-guide.md](resources/revision-guide.md)**: Complete three-pass system with before/after examples
- **[resources/evaluators/rubric_revision.json](resources/evaluators/rubric_revision.json)**: Quality scoring criteria

**Inputs required:**
- Draft text to revise (any stage)
- User's intent or core message (if known)
- Any constraints (word count target, tone preferences)

**Outputs produced:**
- Analysis files for each pass (clutter, cognitive load, rhythm)
- Revised draft with tracked word count reduction
- Summary of changes made in each pass
