---
name: elementor-feature-lookup
description: Answer "is this Elementor feature/widget free or Pro?" Use when the user asks whether something (a widget, theme builder, popups, forms, dynamic tags, loop, WooCommerce builder, motion FX, etc.) requires Elementor Pro or ships in free.
---

# elementor-feature-lookup

Read `resources/free-vs-pro.md` and answer from it. Do not guess.

Steps:
1. Read the matrix file in this skill's `resources/`.
2. Match the user's term against the `widget_name | tier | module` rows AND the "Pro feature gates" section.
3. Reply with: tier (free / Pro / Pro+WooCommerce), module path, and one-line caveat if any (deprecated variant, experiment-gated, license feature flag).
4. If not in the matrix, say so — do not invent. Suggest grepping `modules/*/widgets/` in the source roots the user gave.

Do not paraphrase the table into the response. Quote the row.

To check what's *actually* registered on a specific live install (free vs Pro, experiments on/off) instead of relying on the static matrix, use the live-inventory snippet in `elementor-deploy-verify`.
