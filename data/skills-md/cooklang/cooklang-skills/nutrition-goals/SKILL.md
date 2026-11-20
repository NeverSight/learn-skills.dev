---
name: nutrition-goals
description: Use when the user wants to change AN EXISTING Cooklang recipe (.cook) or meal plan (.menu) so it hits numeric nutrition targets ("make this 600 kcal per serving", "get my week to 150 g protein a day", "more protein, same calories"). Measures with the Cook nutrition service, edits, and verifies. Not for evaluation-only questions (nutrition-reports), and not for picking or screening recipes that already meet a number (nutrition-reports screening, then meal-planning).
---

# Skill: Nutrition Goals

**Needs the Cook MCP server** (tools like `render_report` and `validate`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Never estimate nutrition from your own knowledge instead.

Use when the user wants to **change** a recipe or meal plan so it hits numeric
nutrition targets — "make this 600 kcal per serving", "get my week to 150 g
protein per day", "more protein, same calories". You measure with the **Cook
nutrition service** (through `render_report`), choose edits, verify them
*before* saving, save, and confirm.

Nutrition data needs a cook.md login and Cook Basic or Cook Pro. On
"authentication required" call `login`; on "subscription required" show the
user the pricing link from the error. The direct nutrition tools (`get_nutrition`, `aggregate_nutrition`, `lookup_ingredient`, …) return JSON `login_required` (call `login`) or `plan_required` (show the user `checkout_url`) instead.

This skill changes food to reach numbers. For evaluation-only questions where
no change is wanted ("is this healthy?", "how much protein is in this?"), follow
the nutrition-reports skill instead.

**Not for selection.** "Find me three dinners over 35% protein", "which of my
recipes are high protein", "plan a week that averages 150 g protein from what I
already have" are *screening* requests: nothing gets edited, and the number is
a filter over existing files. Running this skill's per-file measure-and-edit
loop over a candidate list is how a three-dinner question turns into a hundred
tool calls. Follow nutrition-reports (its "Screening a shortlist" section) and,
if a `.menu` is wanted at the end, meal-planning. Come back here only once a
specific file has been chosen and has to *change* to hit the number.

## The loop

1. Pin down the target (nutrient, value, basis, tolerance).
2. Measure the baseline and per-ingredient contributions.
3. Choose edits — tiered, minimally invasive.
4. Verify the edited text BEFORE saving.
5. Save the edit and present current → new vs target.
6. Re-measure the saved file to confirm.
7. Offer to save the targets as a reusable checks template.

## 1. Pin down the target

- Nutrient keys: macro keys are `kcal`, `protein_g`, `fat_g`, `sat_fat_g`,
  `carb_g`, `sugar_g`, `fiber_g`; micros/vitamins by key via `nutrient_total`
  (e.g. `"sodium_mg"`, `"iron_mg"`). `nutrient_total` returns 0 for an unknown
  key — if a micro baseline reads 0 for an ingredient list that plainly
  contains it, suspect the key, not the food.
- **Basis:** per serving, whole recipe, or per day (for `.menu` plans). If the
  recipe declares `servings` and the user just says "600 kcal", per-serving vs
  total is genuinely ambiguous — ask. Otherwise don't ask; state your reading.
- **Tolerance:** default ±5 % (`within_tol(value, target, 5)`); use the user's
  figure when given. For "keep X the same", hold X within ±5 % of its current
  value.
- **Already given:** targets, restrictions or servings the user stated earlier
  in the conversation (including in a prompt they ran) count as provided. Do
  not ask for them again — restate your reading and proceed.

## 2. Measure the baseline

Read the file with `read_recipe` (you need its source to edit it), then render
it with `render_report` (`input_path` = the file). Emit machine-readable lines —
the ITEM lines are your lever map (which ingredients dominate which nutrient):

```jinja2
{% set t = macros(ingredients) %}
{% set servings = metadata.servings | default(1) | int %}
TOTAL kcal={{ t.kcal | round(1) }} protein={{ t.protein_g | round(1) }} fat={{ t.fat_g | round(1) }} carb={{ t.carb_g | round(1) }} fiber={{ t.fiber_g | round(1) }}
PER_SERVING ({{ servings }}) kcal={{ (t.kcal / servings) | round(1) }} protein={{ (t.protein_g / servings) | round(1) }}
{% set agg = aggregate_nutrition(ingredients) %}
{% for it in agg.items -%}
ITEM {{ it.ingredient }} | {{ it.amount.value }} {{ it.amount.unit }} | kcal={{ it.macros.kcal | round(1) }} protein={{ it.macros.protein_g | round(1) }} | {{ it.confidence }}
{% endfor -%}
{% for f in agg.failures -%}
FAILED {{ f.ingredient }} — {{ f.error.message }}
{% endfor -%}
```

FAILED ingredients contribute **nothing** to the totals — tell the user the
numbers exclude them rather than silently trusting the total. Flag `estimated`
confidence items when they dominate a target nutrient.

For `.menu` plans the template reads `plan.days` (each day's scaled
`.ingredients`) instead of `ingredients`; see the "Meal plans" section of
nutrition-reports and https://nutrition.cook.md/docs/guides/plan.

## 3. Choose edits — tiered

Prefer the least invasive tier that can reach the target; move down only when
the current tier cannot:

1. **Quantities & servings** — scale ingredient amounts, or plan servings.
2. **Swaps** that preserve the dish — yogurt → Greek yogurt, half the oil plus
   broth, white rice → lentils. `lookup_ingredient` finds catalog names,
   `check_category` keeps a swap in its category (e.g. oily fish), and
   `get_nutrition` compares per-amount profiles before you commit.
3. **Add/remove** ingredients — or recipes in a plan — last.

Keep the dish's character: a few decisive changes beat many tiny ones. Round
to practical cooking amounts and keep the recipe's existing unit style. The
`cooklang://syntax` resource covers the edit mechanics for `.cook` and
`.menu` files.

## 4. Verify BEFORE saving

Write the full edited file text, then render it with `render_report` using
`input` (the edited text) and `kind` (`"cook"` or `"menu"`) instead of
`input_path` — the same measuring template, so numbers are comparable. Nothing
is saved yet. Refine at most ~3 rounds; if the targets stay unreachable within
the allowed tiers, stop and present the closest achievable numbers with a
plain explanation of the gap (e.g. "without swapping the rice, 40 g protein
forces ~750 kcal").

To compare a few alternatives quickly without writing each one out, sum
`nutrition_for_amount` over a candidate list (item shape — macros live under
`.macros`); it raises a template error when an ingredient can't be resolved,
so fix the name/unit and re-render:

```jinja2
{% set candidate = [
  {"name": "chicken breast", "amount": 300, "unit": "g"},
  {"name": "olive oil", "amount": 1, "unit": "tbsp"},
  {"name": "basmati rice", "amount": 150, "unit": "g"}
] %}
{% set servings = 2 %}
{% set ns = namespace(kcal=0.0, protein=0.0) %}
{% for c in candidate %}
{% set n = nutrition_for_amount(c.name, c.amount, c.unit) %}
{% set ns.kcal = ns.kcal + n.macros.kcal %}
{% set ns.protein = ns.protein + n.macros.protein_g %}
{% endfor %}
CANDIDATE total kcal={{ ns.kcal | round(1) }} protein={{ ns.protein | round(1) }}
CANDIDATE per-serving kcal={{ (ns.kcal / servings) | round(1) }}
KCAL_OK={{ within_tol(ns.kcal / servings, 600, 5) }}
```

## 5. Save the edit

- Run `validate` on the edited text, then save with `write_recipe` (`.cook`) or
  `write_menu` (`.menu`), always the full file content. This overwrites the
  user's file: if they asked to see options first, or the change is large (tier
  3), confirm before saving.
- Tell the user what you changed in one or two lines per ingredient
  (`olive oil 3 tbsp → 1 tbsp`), not a full diff, and where you saved it.
- Present current → new vs target (per serving/day and total, from steps 2 and
  4) as a small table.

## 6. Confirm on the saved file

Re-render the saved file with `input_path` and the same measuring template. If
the numbers differ from step 4, say so and fix — the saved file is what the
user will cook from.

## 7. Offer to persist the goals

Offer (don't push) to save the targets as a reusable checks template so future
edits can be re-validated (the nutrition-reports flow), at
`reports/goals.<recipe-slug>.md.jinja` (or under `config/reports/` if that is
where the collection keeps its templates — Cook Editor does), with `write_config`:

```jinja2
{% import "ck" as ck %}
{% set t = macros(ingredients) %}
{% set servings = metadata.servings | default(1) | int %}
# Goals — {{ metadata.title | default("Recipe") }}

- Energy: {{ (t.kcal / servings) | round }} kcal per serving
- Protein: {{ (t.protein_g / servings) | round(1) }} g per serving

{{ ck.between(t.kcal / servings, 570, 630, "kcal per serving") }}
{{ ck.min(t.protein_g / servings, {"min": 40}, "Protein per serving (g)") }}

{% set checks = all_checks() %}
**{{ checks | selectattr("ok") | list | length }} of {{ checks | length }} checks passed.**
```

Render it later with `template_path: "reports/goals.<recipe-slug>.md.jinja"`.

(`ck.min`/`ck.max`/`ck.range` take a target *object* like `{"min": 40}`;
`ck.between` takes scalar bounds.)

## Function cheatsheet (condensed)

Full reference at https://nutrition.cook.md/docs/guides/functions.

| Function | Returns |
|---|---|
| `macros(ingredients)` | flattened totals `{kcal, protein_g, fat_g, sat_fat_g, carb_g, sugar_g, fiber_g}` |
| `aggregate_nutrition(ingredients)` | `{items, failures, totals, confidence_breakdown}`; each item has `.ingredient`, `.amount.value/.unit/.mass_g`, `.macros.*`, `.confidence` |
| `nutrition_for_amount(name, amount, unit, prep?, standard?)` | one full item (same shape as `items[]`) for an arbitrary hypothetical amount |
| `nutrient_total(ingredients, key)` | number; micros then vitamins (`"sodium_mg"`, `"vit_d_iu"`) |
| `within_tol(actual, target, tol_pct)` | bool — within `tol_pct` % of target |
| `compare(actual, target, op)` | bool — `op` is `gte`/`lte`/`eq` |
| `convert(amount, from, to, ingredient?)` | unit conversion (ingredient needed for volume/count) |
| `record_check(label, ok)` / `all_checks()` | record and read passed/failed checks (used by `ck` macros) |

## Guardrails

- **Every number comes from the service.** Never estimate nutrition from your
  own knowledge — not for baselines, not for candidate verification.
- Surface FAILED and low-confidence ingredients; never present totals that
  silently exclude them. Measure with `aggregate_nutrition` / `macros` (both skip
  unresolved ingredients; `aggregate_nutrition` lists them under `failures`), never with
  `nutrition_for(ingredient)` in a loop — that aborts on the first miss.
- Non-English recipes: the nutrition database resolves English ingredient names
  only. When the FAILED list is mostly non-English names, tell the user once —
  "Nutrition lookups currently understand English ingredient names — <language>
  isn't supported yet; email support@cook.md if you'd like it added sooner" —
  and offer to proceed with English equivalents via `nutrition_for_amount`,
  clearly marked as translated by you.
- Keep proposed quantities practical (no "137 g chicken"; prefer 140 g).

## When the render errors

`render_report` returns an error result on failure:

- **"authentication required"**: call `login`, show the user the code and link,
  retry once they've approved.
- **"subscription required"**: nutrition math needs Cook Basic or Cook Pro — show
  the pricing link from the error. You may still make a qualitative edit if the
  user wants, clearly labelled as unverified. Do not keep retrying.
- **Template error** (minijinja reports the line): fix the template, render again.
