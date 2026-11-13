---
name: ux-typography
description: Design or critique a product's typography — typeface selection and pairing, type scale, hierarchy, and readability settings (size, line length, line height, spacing, alignment). Trigger when choosing a typeface or font pairing, setting up a type scale, fixing typographic hierarchy, improving text readability, or reviewing a UI layout for typography issues.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Typography Skill


## How this skill behaves (read first)

This is a **generative** skill. Typography has two default failure modes: **bland** (pick one safe font, no real scale or hierarchy) and **over-expressive** (multiple display faces, many weights/colors/cases stacked → cluttered and illegible). So this skill gates:

1. **Establish brand personality, content types, and medium** — these drive the *expressive* choices worth making.
2. **Apply the always-true core** — legibility, a clear scale/hierarchy, and restraint hold for any product.
3. **Make the typeface/pairing/scale choices deliberately** — surface them as gated decisions tied to brand, not defaults.

Then **hand off to the audits**: `accessibility` (size, contrast, spacing), `aesthetics` (hierarchy, balance).

---

## Step 0 — Establish context before choosing type

- **Brand personality & expected aesthetics** — what impression should it make, and what does the audience expect (a kids' app vs. a banking app demand opposite tone)?
- **Content types** — what kinds of text exist (display, headings, body, captions, labels)? This sizes the hierarchy.
- **Medium** — long-form reading vs. dense UI vs. marketing — changes the legibility/expressiveness balance.
- **Language direction** — LTR vs. RTL (drives default alignment).

State assumptions if proceeding without answers.

---

## The always-apply core (true for any typography)

**Readability & legibility (body text)**

- **Body ≥ 16px.** Start the scale from body size (it occupies the most space), then size up/down.
- **Line length 50–75 characters.** Longer is hard to track; too short forces choppy eye movement.
- **Line height ~150%** of font size for body; larger sizes/widths need more.
- **Paragraph spacing ≥ 1.5× line spacing** (WCAG); separate ideas into digestible blocks.
- **Left-align body text in LTR** (right for RTL). Reserve center alignment for short elements (headlines, quotes, CTAs) — it slows reading and hurts users with cognitive/visual impairments.
- Design for **scannability** — ~79% of users scan, ~3% read word-by-word; hierarchy + spacing make scanning work.

**Hierarchy & restraint**

- **Limit to ≤3 typefaces** — often one superfamily with good weight/style variety is enough.
- **Build a type scale** (size, weight, style) covering the content types; keep levels distinct.
- **Use ≤3 hierarchy instruments** (size, weight, style, color, case) per level and **2–3 heading levels**; stacking all of them is clutter (a huge, bold, colored, all-caps headline shouts).
- **Emphasis is soft and singular** — italics (softest) or bold, not several at once; color in type sparingly.
- **Group with white space & proximity** — related text close, unrelated separated.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0. **Stacking display faces, weights, and decoration is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Typeface personality / mood** | A display/character face fits the brand and appears only in headings | Using an expressive face for body text (kills readability) | Character in display, high-legibility for body |
| **One vs. two typefaces** | A heading/body pairing adds useful contrast | A third face, or pairing that lacks clear contrast | One superfamily by default; add a second only with clear contrast + role |
| **Number of weights** | A few weights to build hierarchy | A weight for every whim | The minimum that makes the scale legible |
| **Type-scale ratio** | Dramatic ratio for marketing/editorial impact | Dramatic ratio in dense UI (wastes space) | Modest ratio for product UI; bolder for marketing |
| **Serif vs. sans** | Match medium/brand (serif long-form/editorial trust; sans UI clarity) | Choosing by taste against the medium | Fit the medium and audience expectation |
| **Decorative touches** (drop caps, pull/block quotes) | Editorial/long-form layouts | Product UI, forms, dense screens | Editorial only |

**Always avoid** (regardless of context): typographic **clichés** (Papyrus for "ancient", Comic Sans for "fun"), **anachronisms** (period-mismatched faces), and **appropriateness** failures (a casual script on a banking app). Explore beyond the obvious; prioritize fit over novelty.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After choosing or revising type, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`microcopy` is Tier A (auto-run); `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — body ≥16px, contrast of text on its background, line length/height and paragraph spacing, alignment, and that hierarchy doesn't rely on color alone.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — typographic hierarchy effectiveness, balance, white space, and whether the type treatment tipped into clutter (>3 instruments, too many faces).
- **`ux-microcopy-audit`** *(Tier A)* — the words themselves (this skill sets how text *looks*, not what it *says*).

If accessibility flags readability or aesthetics flags clutter, return to the core: fewer faces, fewer instruments, a cleaner scale.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| One safe font, no scale or hierarchy | A deliberate type scale with 2–3 distinct levels |
| 3+ typefaces / a display face for body | ≤3 faces; often one superfamily; display only in headings |
| Big + bold + colored + ALL-CAPS headline | ≤3 hierarchy instruments per level |
| Body text < 16px | Body ≥16px, scale built up from there |
| Full-width lines of text | 50–75 characters per line |
| Tight, cramped line spacing | ~150% line height; paragraph spacing ≥1.5× |
| Center-aligned body paragraphs | Left-align body (LTR); center only short elements |
| Papyrus/Comic Sans clichés; anachronistic faces | Appropriate, considered faces explored beyond the obvious |
| Ship without checking | Hand off to accessibility + aesthetics |

---

## Source lessons (Uxcel)

- [Selecting Typefaces](https://uxcel.com/lessons/selecting-typefaces-611)
- [Typographic Principles](https://uxcel.com/lessons/typographic-principles-438)
- [Paragraphs in Typography](https://uxcel.com/lessons/paragraphs-200)
- [Typographic Hierarchy](https://uxcel.com/lessons/typographic-hierarchy-107)
