---
name: athlisis-diet-plans
description: Use when creating or editing a client's diet plan in the Athlisis dietitian app — building meal options from a questionnaire, computing food quantities against calorie targets, or writing ingredient-substitution notes.
---

# Athlisis diet plans

## Overview
Athlisis diet plans use an **options layout**: no days of the week, just interchangeable meal choices per category (Πρωινό, Δεκατιανό, Μεσημεριανό, Απογευματινό, Βραδινό). Every choice within a category must land on the same calorie target (±30 kcal), computed from the client's own questionnaire wording — not invented. Get this wrong and the dietitian has to manually fix quantities across every meal.

## When to use
- Building a brand-new plan for a client from their questionnaire answers
- Adding/changing meals in an existing plan
- Computing substitution quantities ("X ή Y" alternatives) for meal notes
- Any `search_foods` / `update_diet_plan` / `get_diet_plan` MCP call against Athlisis

## Workflow

1. **Read this skill's reference files first** (see below) — don't start from scratch.
2. **Fetch in parallel**: `search_clients`, `get_client_questionnaire`, `get_client_measurements`, `list_client_diet_plans`.
3. **Fetch plan structure**: `get_diet_plan` to see existing `meal_type`/`day` layout and the equation-suggested `required_kcal`.
4. **Ask if unclear**: total daily kcal (unless the dietitian already gave it), or meal-count/structure questions. Never invent a target.
5. **Propose the full per-meal kcal breakdown** (all categories, sums to the daily target) and **wait for explicit confirmation** before writing anything. Build it from the client's actual choices, not a fixed template: look at all the Πρωινό choices together, all the Μεσημεριανό together, and so on, and pick each category's kcal so that most of its choices fit with sensible, round quantities under the portion rules. Μεσημεριανό is the largest meal, Βραδινό usually comes next; split the two roughly 55/45 unless the dietitian says otherwise. Aim for the total she gives (no built-in +5%).
6. **Compute quantities** using the reference files (food IDs, portion ranges, equivalence tables) — don't call `search_foods` for anything already in [food-database.md](food-database.md).
7. **Write the whole plan in ONE `update_diet_plan` batch call** (all `set_meal_foods`/`set_meal_notes` ops together).
8. **Report back tersely**: kcal per meal category. Never paste the full plan into chat.

**Stop-and-ask triggers** (don't guess past these — resolve immediately, then keep going):
- A requested meal includes a food that isn't in [food-database.md](food-database.md) and doesn't turn up in a live `search_foods` (filtered to `list: 4` — never search or pull from other lists) → stop and ask the dietitian to add it to list 4 in Athlisis first. Never substitute something similar, and never use a food from another list, without asking.
- Anything else you're not confident about (an ambiguous dish description, an order convention that doesn't match a known pattern, a food name that could mean two different things) → stop and ask right there rather than guessing, and update this skill's reference files afterward so the same question doesn't recur.

## Meal-type / day mapping

```
type 0: Πρωινό         type 1: Δεκατιανό       type 2: Μεσημεριανό (1)
type 3: Απογευματινό   type 4: Βραδινό (1)     type 5: Μεσημεριανό (2)
type 6: Βραδινό (2)
```
Each `day` (0-6) is one choice, not a weekday. Max 7 choices per column — 8th+ choice goes to the `(2)` column of the same meal, at the **same kcal** as column `(1)` (don't double-count it in daily totals). Only fill columns/slots the client actually has answers for in the questionnaire — never invent extra choices, never leave a gap by copy-pasting a neighbor.

## Core rules (memorize these, they're violated most often)

- **Isocaloric within a category**: every Πρωινό choice matches every other Πρωινό choice (±30 kcal) — same for each other category. Exception: "Μακαρόνια με κιμά" is allowed to run well above the category target rather than compress pasta/mince below their normal ranges (see portion-ranges file).
- **±30 kcal tolerance exists so quantities can be round** — never contort grams to hit the exact target. Grams go in steps of 5γρ; chicken, fish, beef, steaks, μπιφτέκια and pork go in steps of 10γρ. Ψωμί γερμανικού τύπου is counted in slices of 56γρ. Landing a little above target is better than a portion that's too small or not round (that's the main reason the dietitian bumps quantities up).
- **Protein over starch**: prefer slightly less carbohydrate and slightly more protein in a meal. When a meal's kcal must come down, cut the starch first (πίτα, παξιμάδι, φρυγανιά, ψωμί, ρύζι).
- **Eggs**: always whole numbers. In main meals (Μεσημεριανό/Βραδινό) at least 2 eggs; a single egg only in Πρωινό or a snack.
- **Salad + oil pairing**: wherever "σαλάτα επιλογής" appears, olive oil appears too (default 1 tsp, ID `52361`, 31.5 kcal). Raise oil above 1 tsp only when calories need covering and the other foods can't go any higher. Omelette always gets 2 tsp oil, regardless of calorie fit.
- **"Λαχανικά επιλογής" ≠ "σαλάτα επιλογής"**: λαχανικά επιλογής is its own food (ID `152716`, 40 kcal/φλ., default 2 φλ.); σαλάτα επιλογής is ID `2999`. Use whichever word the client wrote.
- **Σαλάτα επιλογής is always exactly 2 cups** (56 kcal) — never scaled.
- **Food order in a meal mirrors the dish type** — see [food-order-and-substitutions.md](food-order-and-substitutions.md) section 1.
- **Substitution notes**: only write a substitute if the client's own questionnaire mentions the alternative ("Α ή Β"). Always in the form `αντί για [Χγρ Α] → [Χγρ Β]` (e.g. `αντί για 200γρ τσιπούρα → 160γρ σολομό`, `αντί για 100γρ ρύζι → 115γρ πατάτα ψητή`), never "ή Χγρ Β". Compute the calorie-equivalent quantity of B (see equivalence table); multiple substitution notes in one meal are separated by ` / `. Full convention: [food-order-and-substitutions.md](food-order-and-substitutions.md) section 2.
- **List 4 only — no fallback**: always check [food-database.md](food-database.md) (the dietitian's "Τρόφιμά μου" list) before calling `search_foods`. Any live `search_foods` call must be filtered to `list: 4`. Never use lists 0/1/2/5, recipes, aCloud foods, or favorites — if it's not in list 4, stop and ask the dietitian to add it (see stop-and-ask triggers above). That file can go stale (foods get renamed/removed in the app) — if an ID errors as `invalid_food_id`, re-search live (still `list: 4`) and patch both the plan and the reference file.
- **Weekly database refresh**: once a week (or whenever the dietitian mentions adding foods in Athlisis), re-scan the live list 4 via `search_foods` (filters: list=4) against the names already in [food-database.md](food-database.md) and patch any new/renamed/removed entries — don't rely solely on the dietitian remembering to ask for a refresh.
- **Questionnaire shorthand**: "φρυγανιά"/"φρυγανιές" with no other qualifier always means Παπαδοπούλου Χωριάτικες (ID `79605`), never Wasa ("Wasa" only when written explicitly, ID `2997`). "ψάρι" means τσιπούρα (ID `149312`); the dietitian renames it herself when needed. "έτοιμα γεύματα Σκλαβενίτη" means every Σκλαβενίτης ready meal in list 4, each at the category kcal, plus a range note. Full table: [food-order-and-substitutions.md](food-order-and-substitutions.md) section 3.
- **Existing-plan edits use CAPS convention**: a note written in ALL CAPS on a meal slot is a pending instruction from the dietitian, not client content. Execute it, then delete the caps note. Never reorder existing foods in a meal you're editing — copy the food_id order verbatim from `get_diet_plan` and only change quantities/substitutions.

## Quick reference

| Need | File |
|---|---|
| Food IDs, kcal, serving units (the "Τρόφιμά μου" list) | [food-database.md](food-database.md) |
| Portion ranges per food (chicken, pasta, lentils, etc.) + calorie-coverage priority | [portion-ranges-and-equivalents.md](portion-ranges-and-equivalents.md) |
| Starch/bread equivalence multiplier table (rice↔potato↔pasta↔rusk...) | [portion-ranges-and-equivalents.md](portion-ranges-and-equivalents.md) |
| Dish-type food ordering, substitution-note format, food grouping (φασολάκια/μπριάμ, φακές/γίγαντες...), choice-priority order within Μεσημεριανό/Βραδινό | [food-order-and-substitutions.md](food-order-and-substitutions.md) |

## Common mistakes

- Compressing a food below its normal portion range just to hit ±30 kcal (fill the gap with sides/oil/cheese instead — see portion-ranges file for the exact rule and the past incident it came from).
- Reordering foods in an existing meal during an edit (always copy the original food_id order verbatim).
- Calling `search_foods` one ingredient at a time — batch every ingredient for the meal/plan into one call.
- Printing the full plan JSON back to the dietitian instead of a short kcal-per-meal summary.
- Writing a substitution note for an alternative the client never mentioned.
- Writing notes as "ή Χγρ Β αντί για Α" instead of `αντί για Χγρ Α → Χγρ Β`.
- Mapping "λαχανικά επιλογής" to σαλάτα επιλογής (2999) — it is its own food (152716).
- Keeping wrap/sandwich chicken at 120γρ+ when it comes with cheese — 80–100γρ is normal there.
