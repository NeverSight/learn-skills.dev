---
name: cogworks-encode
description: Use when synthesizing multiple sources into coherent knowledge bases, performing multi-source analysis, or creating topic expertise from URLs and files. Also use when encountering content integration tasks requiring connections across disparate materials.
license: MIT
metadata:
  author: cogworks
  version: v3.2.0
---

# Topic Synthesis Expertise

You have specialized knowledge for synthesizing content from multiple sources into coherent, expert-level knowledge bases. Your job is to perform **true synthesis** - not concatenation or summarization, but deep integration of concepts, patterns, and relationships across sources.

## Core Mission

Transform disparate source materials into a unified knowledge base that:

1. Identifies and defines core concepts clearly
2. Maps relationships between concepts
3. Extracts reusable patterns with context
4. Documents anti-patterns and pitfalls
5. Flags conflicts between sources
6. Provides practical examples with citations
7. Creates a coherent narrative flow

**Critical:** The downstream consumer is an LLM that treats skill content as authoritative instructions. True synthesis creates new understanding that the agent cannot derive on its own - connections between sources, resolved contradictions, and actionable patterns with when/why/how context. Apply the Expert Subtraction Principle throughout.

### Overriding Principles

1. **Never fabricate domain knowledge.** If sources are ambiguous or incomplete, say so explicitly. This rule overrides all others.
2. **Prefer precision over coverage.** A focused, accurate synthesis is better than a broad, shallow one.

### The Expert Subtraction Principle

**Core Philosophy:** Experts are systems thinkers who leverage their extensive knowledge and deep understanding to reduce complexity. Novices add. Experts subtract until nothing superfluous remains.

**The principle in practice:** True expertise manifests as removal, not addition. The expert's value is knowing what to leave out. A novice demonstrates knowledge by showing everything they know; an expert demonstrates understanding by showing only what matters.

## When to Use

- Combining 2+ sources on a single topic
- Creating reference documentation from multiple inputs
- Building expertise skills from URLs/files
- When sources may conflict and need reconciliation
- Multi-document analysis requiring relationship mapping

**Not for:** Single-source summarization, copy-editing, translation

## Knowledge Base Summary

- **8-phase synthesis process**: Content Analysis -> Concept Extraction -> Relationship Mapping -> Pattern Extraction -> Anti-Pattern Documentation -> Conflict Detection -> Example Collection -> Narrative Construction
- **Decision utility over section counts**: include only the sections and entries that improve execution quality
- **Explicit relationships**: Use arrow notation (->) to show how concepts connect
- **Conflict transparency**: Always flag disagreements between sources with both perspectives
- **Citation requirements**: Every example, pattern, and anti-pattern must cite its source
- **Source scope discipline**: Cross-platform sources are contrast-only and never override primary-platform guidance

## The 8-Phase Process (Summary)

1. **Content Analysis** - Map what each source contributes
2. **Concept Extraction** - Identify the smallest set of fundamental building blocks needed for clear decisions
3. **Relationship Mapping** - Show dependencies, hierarchies, contrasts
4. **Pattern Extraction** - Document reusable approaches (when/why/how/boundary conditions)
5. **Anti-Pattern Documentation** - What to avoid and why
6. **Conflict Detection** - Flag and contextualize disagreements
7. **Example Collection** - Concrete demonstrations with citations
8. **Narrative Construction** - Build coherent flow from simple to complex

## Full Methodology

See [reference.md](reference.md) for the complete synthesis methodology including:

- **Detailed phase instructions** - Step-by-step guidance for each phase
- **Output format template** - Required structure for synthesis output
- **Quality standards checklist** - Self-check before completing
- **Synthesis principles** - Practices and common mistakes
- **Good vs bad examples** - Concrete comparisons
- **Edge case handling** - Similar sources, contradictions, sparse info, technical content
- **Success criteria** - How to evaluate synthesis quality

## Output Structure

See the **Synthesis Output Contract** section in [reference.md](reference.md) for the complete template.

Required synthesis sections: TL;DR, Decision Rules, Anti-Patterns, Quick Reference, Sources.

Conditional sections: Core Concepts, Patterns, Practical Examples, Deep Dives (include only when they add unique value).

## Common Mistakes

- **Concatenation disguised as synthesis** - Just putting sources in sequence with headers
- **Missing citations** - Every pattern/example needs a source reference
- **Hidden conflicts** - Silently picking one source over another without flagging disagreement
- **Abstract patterns** - Patterns without when/why/how aren't actionable
- **Missing boundary conditions** - Patterns that only say when to apply, never when not to, create brittle skills that apply rules where they don't belong
- **Assuming knowledge** - Definitions must stand alone, not assume reader context
- **Section quota chasing** - Inflating section counts instead of improving decision quality

See **Examples of Good vs Bad Synthesis** in [reference.md](reference.md) for concrete comparisons.

## Self-Verification (Required Before Output)

After completing synthesis, verify your output against this checklist before presenting it:

**Fidelity:**
- Core concepts from sources are preserved without distortion
- Key distinctions are explicit, not collapsed into generic guidance
- Contradictions between sources are flagged and resolved with rationale, not silently merged

**Operational density:**
- Decision Rules contain operational guidance ("when X, do Y in this context"), not restated source summaries
- A synthesis that only paraphrases is a summary, not an implementation — the gap between these is the primary quality signal

**Citations:**
- Every Decision Rule and Anti-Pattern carries a [Source N] citation
- Minimum 3 citations across the output
- No fabricated or placeholder citations

**Structure:**
- Required sections present: TL;DR, Decision Rules, Anti-Patterns, Quick Reference, Sources
- Optional sections (Core Concepts, Patterns, Examples, Deep Dives) included only when adding unique decision value
- One canonical location per fact — no section quota inflation

**Truthfulness baseline:**
- Do not fabricate facts, sources, metrics, or standard details
- State uncertainty explicitly rather than filling gaps with unsupported inference
- Keep outputs within the declared scope

**Deterministic validation:**
If available, run the portable validation script:
```bash
bash scripts/validate-synthesis.sh {output_path}
```
