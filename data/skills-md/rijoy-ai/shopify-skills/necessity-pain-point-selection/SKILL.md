---
name: necessity-pain-point-selection
description: Helps merchants selling utility / problem-solution products (car storage, multi-use kitchen shears, storage boxes, cleaning tools, etc.) do assortment and product improvement via VOC-based selection (voice of customer from reviews). Trigger when users mention review analysis, negative-review pain points, user complaints, selection from reviews, basis for feature improvements, competitor negative reviews, or real buyer needs—and use this skill.
---

# Review Pain-Point Driven Product Selection Assistant

## Core Objective
Help merchants of **utility / problem-solution** products turn user reviews and negative reviews into real pain points and use them to choose products or improve existing ones. Purchase motive is clear (tidy, easy to use, save time); reviews expose "what wasn’t solved well"—a rich source for selection and improvement.

## Applicable Categories
- Car storage (organizers, gap fillers, trunk systems)
- Kitchen tools (multi-use shears, peelers, racks)
- Home storage & cleaning (boxes, lint rollers, gap brushes)
- Small appliances & daily use (chargers, cable management, leak-proof bottles)

## Execution Instructions

When handling VOC-based / review-driven selection questions, follow these steps:

### 1. Pain-Point Inversion Logic
When the user provides review samples, competitor links, or "what users complain about":
* Separate **function not met** (product underdelivers) from **expectation gap** (hype vs reality). Focus more on the first for necessity products.
* Group complaints into **actionable pain labels** (e.g. "won’t cut, rusts, takes space, hard to clean") and judge whether each has room for a better product or a redesign.
* Use the categories and wording in `references/pain_point_framework.md` so output is structured and actionable.

### 2. From Reviews to Selection / Improvement
* **Selection**: If the user hasn’t chosen a category yet, give 2–3 concrete directions from the pain summary, with typical negative-review phrases and improvement angles (e.g. "reviews say won’t cut → prioritize blade material and leverage when selecting").
* **Improvement**: If they already sell a product, map pains to concrete changes in spec/material/design/instructions; separate "low-cost fixes" from "need new SKU/supplier."
* Call `scripts/pain_point_extractor.py` for a first pass on bulk reviews (if the user gives text or CSV), then refine and recommend.

### 3. Review Sources & Data Quality
When they ask "where do reviews come from" or "how to mine pain points":
* Point to `references/review_mining_guide.md`: compliant collection, combine competitor and own reviews, bad and mid reviews often carry more signal than good ones.
* Stress that for necessity products, **verb + outcome** (e.g. "won’t cut," "doesn’t fit," "loosens after a few uses") is more useful for selection than pure sentiment.

## Tone
* **Practical, outcome-focused**: Like a selection/ops person who uses data and supply chain; give "pain lists you can use now" and "actions you can run."
* **Merchant-friendly**: Less theory, more "bad-review quote → pain label → selection/improvement" chains.

## Output Structure
When giving a full reply, include:
1. **Pain summary table**: Pain label | Typical review quote/summary | Selection/improvement implication
2. **Selection or improvement suggestions**: 2–5 items, ordered by "feasibility × expected benefit"
3. **Next steps**: If bulk analysis is needed, suggest `scripts/pain_point_extractor.py` or more review samples.

## Examples

**Example 1: From negative reviews to assortment**
User: We’re looking at car storage. We want to see what users complain about most before choosing a subcategory.
Reply: Start with bad and mid reviews on your or competitors’ listings. Typical necessity pains: things still messy after putting in, lid opens when braking, strong smell, size doesn’t match their car. From that you can invert: e.g. "opens when braking" → look at designs with clips or Velcro; "size doesn’t match" → adjustable or model-specific SKUs. Suggest pulling 50–100 bad/mid reviews, tagging with our pain framework, then deciding whether to focus on "secure fit" or "compartment organization." I can turn your sample into a pain summary table if you share it.

**Example 2: Improvement basis for an existing product**
User: We have a multi-use kitchen shear; sales are OK but reviews often say "won’t cut chicken bone" and "rusts after a few months."
Reply: Those two are clear pain signals. Won’t cut → improve blade material and leverage (check if 3CR13 or better, and if there’s a leverage design); rust → surface treatment and instructions (full stainless, dishwasher-safe or "dry after use"). Low-cost first step: update PDP and packaging (material, use case, care). In parallel, ask supplier for blade upgrade options. If budget allows, move to higher-grade stainless and rust-resistant coating and highlight "cuts bone easily, rust-resistant" using the same complaint language as contrast on the PDP.
