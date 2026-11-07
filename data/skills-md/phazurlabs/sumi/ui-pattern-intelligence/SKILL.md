---
name: ui-pattern-intelligence
description: "200+ UI patterns across 10 categories, benchmark DNA from 50+ world-class products, sector pattern matrices, a matcher for code and screenshots, and a 100+ entry anti-pattern encyclopedia. Use when detecting AI slop, judging whether a pattern is standard, or matching how a known product feels."
---

# UI Pattern Intelligence

## Mental model

Most interface problems are solved problems. The skill is recognising which
solved problem you have, and noticing when what you have built is a known
mistake wearing a new coat of paint.

- **Convention is a budget.** Jakob's Law says people spend most of their time
  on other products. Every deviation from convention spends some of the goodwill
  you need for the deviation that actually matters. Spend it once, deliberately.
- **AI-generated UI has a signature.** Purple-to-blue gradients, uniform 8px
  radius on everything, a single font weight, no hover states, no empty states,
  perfectly even spacing with no hierarchy. Recognising the signature is faster
  than evaluating the design.
- **An anti-pattern is a pattern that tested well once.** Carousels, hamburger
  menus on desktop, and infinite scroll on a shopping grid all had a reason.
  Know the reason before you deploy the fix.
- **Match the paradigm, not the pixels.** Copying Linear's colours gets you
  nothing. Copying its commitment to sub-50ms response gets you Linear.

## Index

| Need | Reference |
|---|---|
| Find a pattern by category | `pattern-quick-lookup.md` |
| Choose between candidate patterns | `pattern-decision-engine.md` |
| The full taxonomy, 200+ patterns | `pattern-taxonomy-complete.md` |
| Detect AI slop in code or a screenshot | `anti-pattern-encyclopedia.md` |
| 100+ anti-patterns with the fix | `anti-pattern-encyclopedia.md` |
| Match how Linear, Stripe, Notion feel | `world-class-pattern-dna.md` |
| What is arriving: AI-native, spatial, voice, ambient | `emerging-patterns-2025-2026.md` |
| What died recently and why | `pattern-evolution-2024-2026.md` |
| Score an existing UI against known patterns | `pattern-matching-engine.md` |
| Which patterns a sector expects | `sector-pattern-matrix.md` |
| Benchmark DNA by product tier | `designer-benchmark-dna.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/pattern-quick-lookup.md` | indexed lookup, all categories | 2481 |
| `references/pattern-taxonomy-complete.md` | 200+ patterns, 10 categories | 1878 |
| `references/emerging-patterns-2025-2026.md` | what is arriving | 914 |
| `references/pattern-decision-engine.md` | decision trees | 905 |
| `references/world-class-pattern-dna.md` | 50+ products deconstructed | 618 |
| `references/anti-pattern-encyclopedia.md` | 100+ anti-patterns | 328 |
| `references/pattern-evolution-2024-2026.md` | what died and why | — |
| `references/sector-pattern-matrix.md` | pattern expectations per sector | 417 |
| `references/pattern-matching-engine.md` | identify, benchmark, sector-fit | 412 |
| `references/designer-benchmark-dna.md` | products and designers by tier | 369 |

`pattern-quick-lookup.md` is the largest file in the plugin. Read a section, not
the file.

## What every reference file contains

1. The pattern's name, and the other names it goes by
2. When it applies and the condition that rules it out
3. What a correct implementation includes
4. The failure mode, and the anti-pattern it degrades into
5. Products that do it well, named

## Routing

For **finding a pattern fast** — the complete indexed lookup across navigation,
content display, data entry, feedback and social patterns: read
`references/pattern-quick-lookup.md`.

For **choosing between candidates** — decision trees for lists, navigation
systems, and the other recurring "which of these five" questions: read
`references/pattern-decision-engine.md`.

For **matching a product's feel** — Linear, Stripe, Notion and the rest
deconstructed into the paradigm each is built on: read
`references/world-class-pattern-dna.md`.

For **what is arriving** — AI-native, spatial/AR, voice and multimodal,
collaborative and ambient patterns: read `references/emerging-patterns-2025-2026.md`.

For **the full taxonomy and the anti-patterns**: read
`references/pattern-taxonomy-complete.md` and
`references/anti-pattern-encyclopedia.md`.

For **auditing an existing interface** — the three-stage identify, benchmark and
sector-fit process that turns a screenshot or a codebase into scored findings:
read `references/pattern-matching-engine.md`, with
`references/sector-pattern-matrix.md` for what the sector expects and
`references/designer-benchmark-dna.md` for the tier the product is aiming at.

## Cross-References

This skill is the connective tissue that links analysis to action:

- **`sector-style-intelligence`** — Provides visual direction (colors, typography, tone) per sector. This skill provides pattern direction per sector. Together they define what a product in sector X should look like AND how it should work.
- **`screen-flow-patterns`** — Provides screen type and flow catalogs. This skill provides the broader pattern taxonomy that screen types are composed of.
- **`component-patterns-code`** — Provides React, SwiftUI, and CSS code for individual components. This skill identifies which components are needed; component-patterns-code provides the implementation.
- **`cognitive-psychology-ux`** — Provides the cognitive science (Fitts, Hick, Miller, Gestalt) that explains why patterns work or fail. This skill applies those principles to pattern evaluation.
- **`nng-ux-heuristics`** — Provides Nielsen's 10 heuristics for evaluation. This skill uses heuristics to score pattern execution.
- **`accessibility-inclusive-design`** — Provides WCAG compliance details. This skill flags accessibility gaps in pattern execution.
- **`design-systems-architecture`** — Provides token architecture. This skill assesses whether patterns consume tokens consistently (coherence).
- **`design-critique-case-studies`** — Provides deep product case studies. This skill provides broader pattern-level benchmarking.
- **`interaction-motion-design`** — Provides animation and motion patterns. This skill assesses whether patterns have appropriate motion.
- **`performance-states-patterns`** — Provides loading, error, and empty state patterns. This skill flags missing states as pattern gaps.

## Commands Powered by This Skill

| Command | How This Skill Is Used |
|---------|----------------------|
| `/audit` | Primary command — runs the full 5-stage analysis pipeline |
| `/component` | Consumes pattern taxonomy for component building, benchmark DNA for quality targeting |
| `/screen` | Consumes screen patterns from taxonomy, sector expectations from matrix |
| `/audit` | Cross-references pattern quality during heuristic evaluation |
| `/benchmark` | Uses designer benchmark DNA for competitive comparison |
| `/style` | Uses pattern taxonomy and benchmark DNA for inspiration references |
| `/roast` | References anti-pattern encyclopedia during design critique |
| `/remix` | Uses prescriptions from pattern analysis to drive redesign |
| `/grade` | Pattern quality contributes to overall design score |

## How to Use This Skill

When Claude Code activates this skill, it draws from:

1. **Pattern Taxonomy** to identify and classify what is present in the user's code/screenshots
2. **Designer Benchmark DNA** to know what world-class execution looks like for each pattern
3. **Sector Pattern Matrix** to know which patterns are critical for the user's industry
4. **Pattern Matching Engine** to run the systematic 5-stage analysis pipeline
5. **Pattern Evolution** to ensure recommendations are temporally current
6. **Anti-Pattern Encyclopedia** to identify and explain what is wrong

The combination of these six reference files gives Sumi deep pattern intelligence — not by listing every possible UI, but by providing a taxonomy deep enough to classify any UI, benchmarks comprehensive enough to score any execution, and prescriptions specific enough to upgrade any pattern to world-class.
