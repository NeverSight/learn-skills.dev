---
name: scale-recipe
description: Use when the user wants a Cooklang recipe (.cook) for more or fewer people - "double this", "halve the cake", "scale the carbonara for 6", "how much flour for 3 loaves". Shows scaled quantities without changing the file; changing the saved recipe is cooklang-editing.
---

# Skill: scale-recipe

Use when the user wants a recipe's quantities for a different number of servings or batches.

**Needs the Cook MCP server** (tools like `read_recipe` and `validate`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Do not work out scaled amounts by hand instead.

## Workflow

1. Find the recipe with `search_recipes` (or `list_recipes`) and use the path exactly as returned. Never scale a recipe the collection doesn't have.
2. Work out the factor. `read_recipe` takes `scale` as a **factor** (2 doubles, 0.5 halves), not a target number of servings.
   - "For 6 people": read the recipe once (no `scale`) and take `servings` from its metadata; factor = 6 / servings (e.g. 6 / 4 = 1.5).
   - "Double", "half", "3 loaves of a 1-loaf recipe": the factor is given.
   - No numeric `servings` and the user asked for a head count: look at the body, judge how many portions it makes, state that assumption, then pick the factor. Offer to add `servings` (metadata skill) so it scales exactly next time.
3. Call `read_recipe` with `path` and `scale`. Every quantity in the parsed `recipe` (`ingredients[].quantity`, `timers`) is already scaled, and `recipe.metadata.map.servings` shows the new count. Use those numbers; do not multiply anything yourself. Steps come back as `items` that point at ingredients by index, not as text.
4. Present the scaled ingredient list (original → scaled where helpful, original amounts are in `source`). If the user is cooking from it and wants the steps with amounts filled in, render them with `render_report` (same `input_path` and `scale`, a template that loops over `sections`; the export-recipe skill has one) rather than rebuilding sentences by hand.
5. Point out what the numbers can't tell them (below).

## What scaling does and doesn't cover

- **Fixed quantities** written `{=…}` (e.g. `@salt{=1%pinch}`) do not scale. Find them in `source` and say so ("salt stays 1 pinch"). `validate` warns "Unnecessary scaling lock modifier" on them; that is a parser quirk, not a problem.
- **Unitless counts** scale too: 3 eggs × 1.5 = 4.5 eggs. Round to something cookable and say what you rounded (4 large or 5 small eggs).
- **Recipe references** (`@./Sauces/Pesto{150%g}`) scale as one line. Their own ingredients are not expanded by `read_recipe`; for the full scaled ingredient list across sub-recipes, call `shopping_list` with `recipes: ["<path>:<factor>"]` (e.g. `"Dinner/Lasagne.cook:1.5"`), which follows references.
- **Timers and cookware** don't change. Say when it matters: a doubled stew needs a bigger pot, a doubled cake needs two tins or a longer bake, roasting more food crowds the pan.
- **Baking and seasoning** are less linear than the arithmetic. Leavening (baking soda, yeast) and salt are safest scaled modestly and adjusted; beyond about 2× suggest cooking in batches.

## Rules

- Scaling to show amounts does not touch the file. Only change the saved recipe if the user asks to make the new size permanent; then follow cooklang-editing: update every quantity and `servings` in the frontmatter, `validate` the content, save with `write_recipe` (full file).
- For a meal plan, scale each reference inside the `.menu` (`@./Dinner/Chili{6%servings}`); see the meal-planning skill.
- For a shopping list at a different size, give `"<path>:<factor>"` to `shopping_list` rather than scaling and summing yourself (shopping-list skill).
