---
name: briefing-document
description: Generates comprehensive briefing documents that synthesize sources into executive-ready reports. Produces an Executive Summary with critical takeaways, detailed thematic analysis with evidence, and objective conclusions. Use when creating a briefing, summarizing research, synthesizing sources, writing an executive summary, or asking "create a briefing document."
---

# Briefing Document

Synthesize source materials into a structured, executive-ready briefing.

## Workflow

```text
Briefing document progress:
- [ ] Step 1: Gather sources
- [ ] Step 2: Analyze and extract themes
- [ ] Step 3: Write briefing document
- [ ] Step 4: Validate quality
```

### Step 1: Gather sources

Read files, fetch URLs, or accept pasted text. Ask the user for sources if none are provided. Read every source completely before writing anything.

### Step 2: Analyze and extract themes

- Identify 3-7 major themes or arguments across all sources.
- Track direct quotes with attribution (author, source title, page/section if available).
- Note areas of agreement, tension, or contradiction between sources.
- Distinguish claims from evidence — report what sources say, do not add unsupported conclusions.
- When sources conflict, prepare to present both positions.

### Step 3: Write briefing document

Follow this structure exactly:

```markdown
# [Report Title]: Briefing Document

## Executive Summary

[2-3 paragraphs: the critical takeaways a busy reader needs. A reader
who reads only this section should understand the core findings.]

## [Theme 1 Name]

- [Key point with supporting evidence]
- "[Exact quote]" ([Source Author/Title])
- [Implication or significance]

## [Theme 2 Name]

[Continue for each major theme identified in Step 2]

## Points of Tension

[Where sources disagree or present competing views. Present both sides
without taking a position.]

## Conclusions and Implications

[Synthesis of what the evidence collectively suggests. Forward-looking
implications where supported by the sources.]

## Sources

1. [Author]. [Title]. [Date/Publication if available].
```

### Step 4: Validate quality

```text
Before finalizing, verify:
- [ ] Every claim traces to a specific source (no fabricated content)
- [ ] All major themes from sources are represented
- [ ] Direct quotes are exact and attributed
- [ ] Executive Summary stands alone as a complete overview
- [ ] Analysis is organized by theme, not by source
- [ ] Tone is objective throughout — no editorializing
- [ ] Markdown renders correctly (headings, lists, blockquotes)
```

## Tone and voice

- Objective and analytical — present findings, not opinions.
- Incisive — cut to what matters, do not pad.
- Use "The sources indicate..." or "According to [Author]..." not "I found..." or "We see..."
- Prefer active voice. Avoid hedging unless uncertainty is genuine.
- Match the depth of analysis to the complexity of the sources.

## Context adjustments

- **Single source**: deeper analysis, more granular themes, extended quotes.
- **Multiple sources**: comparative analysis, synthesis across sources, highlight agreements and tensions.
- **Technical sources**: preserve technical terminology, include code references where relevant.
- **Non-English sources**: translate key quotes, note original language.

## Anti-patterns

- Summarizing each source sequentially instead of synthesizing by theme.
- Burying the key finding in the middle of the document.
- Including every detail instead of the most significant findings.
- Editorializing beyond what sources support.
- Writing an Executive Summary that requires reading the full document to understand.

## Skill handoffs

| When | Run |
|------|-----|
| After briefing is written, audit prose quality | `docs-writing` |
| If briefing needs to become a presentation | `creating-presentations` |
