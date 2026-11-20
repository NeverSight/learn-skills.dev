---
name: nutrition-reports
description: Use when the user wants a nutrition or dietitian-style evaluation of a Cooklang recipe (.cook) or meal plan (.menu) - calories, macros, micronutrients, passed/failed checks against targets, exclusions/allergens, a plan's per-day nutrition - or wants to SCREEN recipes that already meet a number ("which of my recipes are over 35% protein?"). Not for changing a recipe or plan to hit targets - that is nutrition-goals.
---

# Skill: Nutrition Reports

**Needs the Cook MCP server** (tools like `render_report` and `read_recipe`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Never estimate nutrition from your own knowledge instead.

Use when the user wants a **nutrition or dietitian-style evaluation** of a recipe or
meal plan — calories/macros/micronutrients, passed/failed checks against targets, exclusions
or allergens, or aggregating nutrition across a `.menu` plan. Backed by the **Cook
nutrition service**, called through the `render_report` tool.

This skill is for *nutrition* specifically. For plain counts, costs (`db()` datastore) and
custom printouts, follow the report-authoring skill; its `aisled()` /
`excluding_pantry()` / `db()` functions work inside nutrition templates too.

## Access

Nutrition data needs a cook.md login and a Cook Basic or Cook Pro plan. If a render
fails with "authentication required", call `login` and show the user the code and link,
then retry. If it fails with "subscription required", show the user the pricing link from
the error. The direct nutrition tools (`get_nutrition`, `aggregate_nutrition`, `lookup_ingredient`, …) return JSON `login_required` (call `login`) or `plan_required` (show the user `checkout_url`) instead. `auth_status` tells you whether the user is logged in and on which plan.

## How rendering works

Nutrition reports are Jinja2 templates rendered with `render_report` (it never edits
files). The template calls nutrition functions (below); the service resolves each
ingredient. `render_report` returns `{ rendered, checks, resolve_failures }`:
`checks` are the passed/failed checks the template recorded, `resolve_failures` the
ingredients the service couldn't resolve, each with an error code, message and
`suggestions`.

- **Reuse first:** saved templates live in `reports/` (CookCLI) or
  `config/reports/` (Cook Editor); `list_recipes` `kind: "template"` lists both. If one answers the question, check its inline
  targets/exclusions match the user's, then render it with `template_path`. If the targets differ, author inline (or offer to update the saved
  template).
- Otherwise draft inline (`template`) and iterate: read `rendered`, fix errors, repeat.
- `input_path` is the `.cook`/`.menu` file as `list_recipes` returned it (e.g.
  `"plans/Week of May 18.menu"`). `scale` defaults to 1 and scales `.cook` recipes only.
- Targets and exclusions: define them **inline** in the template, or point
  `client_profile_path` at a profile YAML in the collection. The profile is then
  available to the template as `client`:

```yaml
name: Sara
exclusions: [peanut, shellfish]
targets:
  energy_kcal: { min: 1800, max: 2200 }
  protein_g: { min: 75 }
  sat_fat_g: { max: 20, tol_pct: 10 }
```

### Fixing resolve failures

- `ingredient_not_found` → try `lookup_ingredient` with the name and retry with a
  suggestion, or fix the ingredient name in the recipe. Do not bake qualifiers into
  names — `fresh garlic` should be `@garlic{}(fresh)`.
- `density_unavailable` / unit errors → probe with `convert_units`; prefer mass units
  in the recipe when density is missing.
- Fixing the recipe itself is an edit: follow the cooklang-editing skill, and ask
  first.

## Screening a shortlist

"Which of my recipes are over 35% protein?", "find three quick dinners with X" —
you are *filtering* existing files, not evaluating one. `render_report` takes ONE
recipe per call, so a careless screen costs one render per candidate and turns a
three-dinner question into a hundred tool calls. Work in three passes:

1. **Narrow before you measure.** `search_recipes` (with `tag` where it helps),
   folder names, and the pantry tools cut the field on the cheap criteria first —
   course, time, ingredients on hand, cuisine. Nutrition is the *last* filter
   applied, never the first.
2. **Cap the candidates at about six**, chosen from that shortlist. If six is not
   enough, say so and screen a second batch — do not pre-emptively measure twenty
   files.
3. **Render, do not read.** A render already resolves the recipe's ingredients and
   macros; reading a file you are about to render buys nothing. Read a recipe only
   when you need its prose — method, equipment, wording you will quote. Send the
   same small template for each candidate (in parallel if your client allows).

Emit one machine-readable line per candidate (`NAME | kcal | protein_g |
pct_protein | OK/FAILED`) so each output is a single line. Present the survivors,
then hand off — meal-planning to build a `.menu` from them, nutrition-goals only
if a chosen recipe has to be *changed* to clear the bar.

## Presenting results

The rendered report **is** the answer: show it to the user as it came back, then add
at most three lines — the verdict, blockers (FAILED or low-confidence ingredients),
the next step. Do not retype or recompute its numbers. For `.menu` plans the per-day
table (each day vs. its targets) lives in the report; the summary names the days that
miss which targets. When the user supplied targets earlier in the conversation, use
them — do not ask again; with no user targets, frame against daily values
(`dv_percent`) rather than inventing thresholds. A single-number question may be
answered in one line from the render. If the user wants the recipe or plan *changed*
to hit the targets, follow nutrition-goals.

## Incomplete coverage — never fail the report

The nutrition database does not resolve every ingredient (regional names,
brands, unusual units). A report must still render for the ingredients it
*can* resolve, skip the rest, and list them at the end:

- Build per-ingredient tables and totals from `aggregate_nutrition(ingredients)`.
  Its `items` are the resolved ingredients (`.ingredient`, `.amount.value` /
  `.amount.unit`, `.macros.kcal|protein_g|fat_g|carb_g|fiber_g|sat_fat_g|sugar_g`,
  `.confidence`) and its `failures` the unresolved ones (`.ingredient`,
  `.error.message`, `.error.suggestions`). `totals` — and the `macros()` /
  `total_calories()` shortcuts — already exclude failures; `totals.is_partial`,
  `totals.included_count` and `totals.failed_count` tell you whether they are complete.
- Do **not** call `nutrition_for(ingredient)` in a loop over `ingredients`: it
  raises a template error on the first unresolved ingredient or non-numeric
  quantity ("some", "1–2") and aborts the whole render. Iterate `agg.items`.
- Do not add your own "coverage must be 100 %" checks or `{% raise %}`-style
  guards; partial data is reported, not refused.
- End every nutrition report with a "Not included" section listing each failure
  and its reason, and say in your summary how many ingredients were skipped.
  Never present partial totals as complete.

```jinja2
{% set agg = aggregate_nutrition(ingredients) %}
{% set servings = metadata.servings | default(1) | int %}
# Nutrition — {{ metadata.title | default("Recipe") }}

| Ingredient | Amount | kcal | Protein | Carbs | Fat |
|---|---|---|---|---|---|
{% for it in agg.items -%}
| {{ it.ingredient }} | {{ it.amount.value }} {{ it.amount.unit }} | {{ it.macros.kcal | round }} | {{ it.macros.protein_g | round(1) }} g | {{ it.macros.carb_g | round(1) }} g | {{ it.macros.fat_g | round(1) }} g |
{% endfor %}
**Per serving ({{ servings }}):** {{ (agg.totals.macros.kcal / servings) | round }} kcal ·
{{ (agg.totals.macros.protein_g / servings) | round(1) }} g protein ·
{{ (agg.totals.macros.carb_g / servings) | round(1) }} g carbs ·
{{ (agg.totals.macros.fat_g / servings) | round(1) }} g fat
{% if agg.totals.is_partial %}
*Totals cover {{ agg.totals.included_count }} of {{ agg.totals.included_count + agg.totals.failed_count }} ingredients.*

### Not included ({{ agg.failures | length }})
{% for f in agg.failures -%}
- {{ f.ingredient }} — {{ f.error.message }}{% if f.error.suggestions %} (try: {{ f.error.suggestions | join(", ") }}){% endif %}
{% endfor %}
{% endif %}
```

### Meal plans (.menu)

A `.menu` is read through `plan`, not `ingredients`: `plan.days` (each with `.name`,
`.date`, `.meals` and the day's scaled `.ingredients`), `plan.all_ingredients`,
`plan.servings` (people eating, from the menu's frontmatter) and
`plan.missing_recipes` (references that didn't resolve — report them). Per-day totals:

```jinja2
{% set people = plan.servings | default(1) %}
| Day | kcal / person | Protein / person |
|---|---|---|
{% for day in plan.days -%}
{% set t = aggregate_nutrition(day.ingredients).totals.macros %}
| {{ day.name or day.date }} | {{ (t.kcal / people) | round }} | {{ (t.protein_g / people) | round(1) }} g |
{% endfor %}
```

### Non-English recipes

The nutrition database currently resolves **English** ingredient names; other
languages are not translated yet. When the failures are mostly non-English names
(e.g. Dutch `havermout`, `volkorenbrood`), still render the report as above and
tell the user in your summary, once:

> Nutrition lookups currently understand English ingredient names — <language>
> isn't supported yet, so those ingredients are listed under "Not included". If
> you'd like your language added sooner, email support@cook.md.

You may offer to re-run with English equivalents (`nutrition_for_amount("rolled
oats", 40, "g")`) for the skipped rows, clearly marked as translated by you —
it errors too if the English name is unknown, so drop that row rather than retry.

## Function cheatsheet

Nutrition functions (full reference at
https://nutrition.cook.md/docs/guides/functions):

| Function | Returns |
|---|---|
| `nutrition_for(ingredient)` | macros for one ingredient: `kcal`, `protein_g`, `fat_g`, `carb_g`, `fiber_g` |
| `nutrition_for_amount(name, amount, unit, prep, standard?)` | full item incl. micros + vitamins (no ingredient object needed); `standard?` (`"fda"`/`"eu"`/`"uk"`) controls which RDA standard the response's `reference_intakes` table uses |
| `aggregate_nutrition(ingredients)` | `{ items, failures, totals, confidence_breakdown }` for a whole list — resolved rows, skipped rows, and totals that exclude the skipped ones |
| `macros(ingredients)` | totals `{kcal, protein_g, fat_g, sat_fat_g, carb_g, fiber_g, …}` |
| `total_calories(ingredients)` | number |
| `vitamins(ingredients)` | vitamins object |
| `nutrient_total(ingredients, key)` | number; looks in micros then vitamins (`"iron_mg"`, `"vit_d_iu"`) |
| `reference_intake(name, standard?)` | daily reference intake (RDA/DV) for a nutrient key, e.g. `reference_intake("sodium_mg")` → `2300`; `undefined` if the nutrient has no DV. `standard?` defaults to `"fda"` (`"eu"`/`"uk"` also) |
| `dv_percent(name, amount, standard?)` | `amount` as a % of that nutrient's daily reference, e.g. `dv_percent("sodium_mg", 230)` → `10`; `undefined` if no DV. `standard?` defaults to `"fda"` |
| `is_in_category(ingredient, slug)` | bool, tree-aware (`oily_fish` ⇒ `fish_and_shellfish`) |
| `category_servings(plan, slug)` | int — meals containing ≥1 ingredient in the category |
| `convert(amount, from, to, ingredient?)` | unit conversion (ingredient needed for volume/count) |
| `compare(actual, target, op)` | bool — `op` is `gte`/`lte`/`eq` |
| `within_tol(actual, target, tol_pct)` | bool — within `tol_pct` % of target |
| `record_check(label, ok)` / `all_checks()` / `failed_checks()` | record and read passed/failed checks |
| `matched_exclusions(ingredients, exclusions)` / `unresolved_exclusions(...)` | exclusion resolution |

Check macros — `{% import "ck" as ck %}`, then each macro records a check and renders a line:

| Macro | Asserts |
|---|---|
| `ck.min(value, target, label)` | value ≥ `target.min` |
| `ck.max(value, target, label)` | value ≤ `target.max` |
| `ck.range(value, target, label)` | `target.min` ≤ value ≤ `target.max` |
| `ck.within(value, target, label)` | value within `target.tol_pct` % of `target.max` |
| `ck.between(value, lo, hi, label)` | lo ≤ value ≤ hi (scalar bounds) |
| `ck.absent(ingredient)` | the excluded ingredient is not present |

`ck.min/max/range/within` take a `target` *object* (`{min, max, tol_pct}`); `ck.between`
takes scalar bounds. Recorded checks also come back in `render_report`'s `checks`.
`category_servings` and plan-wide aggregation are covered at
https://nutrition.cook.md/docs/guides/plan; provenance/estimate quality at
https://nutrition.cook.md/docs/guides/confidence.

For a quick single-ingredient question ("how much protein in 200 g tofu?") you do not
need a template: `get_nutrition` answers it directly, and `aggregate_nutrition` the
tool sums a hand-made list.

## Worked template (inline targets)

```jinja2
{% import "ck" as ck %}
{# Targets inline; or set client_profile_path and use client.targets. #}
{% set targets = {
  "energy_kcal": {"min": 1800, "max": 2200},
  "protein_g":   {"min": 75},
  "sat_fat_g":   {"max": 20},
  "fiber_g":     {"min": 25}
} %}
{% set exclusions = ["peanut", "shellfish"] %}

# Nutrition check — {{ metadata.title | default("Recipe") }}

{% set t = macros(ingredients) %}
- Energy: {{ t.kcal | round }} kcal
- Protein: {{ t.protein_g | round }} g
- Saturated fat: {{ t.sat_fat_g | round(1) }} g
- Fiber: {{ t.fiber_g | round(1) }} g

## Checks
{{ ck.range(t.kcal, targets.energy_kcal, "Daily kcal") }}
{{ ck.min(t.protein_g, targets.protein_g, "Protein (g)") }}
{{ ck.max(t.sat_fat_g, targets.sat_fat_g, "Saturated fat (g)") }}
{{ ck.min(t.fiber_g, targets.fiber_g, "Fiber (g)") }}
{% for ex in exclusions %}{{ ck.absent(ex) }}
{% endfor %}

{% set checks = all_checks() %}
**Summary:** {{ checks | selectattr("ok") | list | length }} of {{ checks | length }} checks passed.
```

## Showing % daily value

When the user wants nutrients framed against a daily target, use `dv_percent` (or
`reference_intake` for the raw figure) instead of inventing reference numbers. The
standard defaults to `"fda"`; use `"eu"`/`"uk"` for European labels. A nutrient with
no published DV returns `undefined` — pre-assign the result and guard with `is defined`
so the row is skipped (piping `undefined` through `| round` raises a template error):

```jinja2
{% set t = macros(ingredients) %}
{% set sodium = nutrient_total(ingredients, "sodium_mg") %}
{% set sodium_dv = dv_percent("sodium_mg", sodium) %}
{% set fiber_dv = dv_percent("fiber_g", t.fiber_g) %}
{% if sodium_dv is defined %}
- Sodium: {{ sodium | round }} mg ({{ sodium_dv | round }}% DV)
{% endif %}
{% if fiber_dv is defined %}
- Fiber: {{ t.fiber_g | round(1) }} g ({{ fiber_dv | round }}% DV)
{% endif %}
```

Workflow: reuse a saved template by `template_path` if one fits → else draft inline →
`render_report` → read `rendered` / `resolve_failures` / fix errors → repeat → show the
report once → ≤3-line summary.

## When the render errors

`render_report` returns an error result on failure. Read it:

- **"authentication required"**: call `login`, show the user the code and link, retry
  once they've approved.
- **"subscription required"**: nutrition data needs Cook Basic or Cook Pro — show the
  user the pricing link from the error. Do not keep retrying.
- **Template error** (minijinja reports the line): fix the template and render again.

## Saving a reusable template

When the user wants to keep the report, save it as a `.jinja` file:

- Save it where the collection already keeps templates (`reports/` for CookCLI,
  `config/reports/` for Cook Editor); default `reports/`.
- Encode the output format in the inner extension: `nutrition.md.jinja` → markdown.
- Save it with `write_config` (`path` e.g. `reports/nutrition.md.jinja`) and tell the
  user where.
- From then on, render it with `template_path` rather than re-sending the source.

Render inline for one-off questions; offer once to save a template, and save only
if the user accepts.
