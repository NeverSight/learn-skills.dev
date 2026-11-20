---
name: shopping-list
description: Use when the user asks for a shopping or grocery list from Cooklang recipes (.cook) or a meal plan (.menu), or wants store-aisle grouping (config/aisle.conf) for their lists.
---

# Skill: shopping-list

**Needs the Cook MCP server** (tools like `shopping_list` and `search_recipes`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Never sum quantities by hand instead.

Use when the user asks for a shopping or grocery list from recipes or a meal plan.

Use the `shopping_list` tool. It does the arithmetic: merges duplicate ingredients across recipes, follows recipe references (a .menu's recipes and their sub-recipes), groups items by aisle from `config/aisle.conf`, and subtracts what `config/pantry.conf` already holds. Never hand-sum quantities yourself — it is error-prone and drifts from what the user's apps compute.

## Workflow

1. Find the recipes or plans: `search_recipes` when the user names dishes, `list_recipes` (`kind: "menu"` for plans) to browse. Never reference a recipe that is not in the collection.
2. Call `shopping_list` with `recipes`: paths exactly as those tools returned them. Append `:N` to scale one entry, e.g. `"Dinner/Pasta.cook:2"` for a double batch. A .menu plan is one entry; its own `{N%servings}` references already set the amounts.
3. Pantry: by default items in stock are subtracted. Set `ignore_pantry: true` when the user wants the full list (e.g. shopping for someone else's kitchen).
4. Format: the default JSON is grouped by aisle — present it as a grouped checklist. Set `format: "markdown"` when the user wants text to paste or print.
5. Report `diagnostics` that matter: references that didn't resolve, ingredients that couldn't be merged because their units differ.

## Aisle grouping

Items not listed in `config/aisle.conf` are not grouped under a store aisle. Run `validate` with no arguments to see ingredients with no aisle. If the user wants store-ordered output, author it. The file is a list of `[category]` sections; order of sections and items is significant — arrange to match the store layout. Define synonyms with `|`:

```
[produce]
potatoes

[dairy]
milk
butter

[canned goods]
tuna|chicken of the sea
```

Save it with `write_config` (`path: "config/aisle.conf"`), always the full file — keep the existing sections and add to them. Parse problems come back as warnings in `diagnostics`; fix them and save again. Afterwards, run `validate` with no arguments to see ingredients with no aisle.

## Saved lists in Cook apps

Cook apps keep a saved list in a hidden `.shopping-list` file at the collection root: recipe references (`./Mains/Carbonara{2}`, nested two spaces per level for menu → recipe → sub-recipe) plus free-hand items (`olive oil{4%l}`, `salt`), with `--` comments. Only author it if the user asks for a list that shows up in their app, and only with your client's file tools; cook-mcp does not write it. The app computes totals from it, so never put summed quantities there.
