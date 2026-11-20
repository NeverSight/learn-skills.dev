---
name: meal-planning
description: Use when building or editing a Cooklang meal plan (.menu file), weekly plans, multi-day menus, or matching servings across days. Not for a single recipe. With a numeric nutrition target ("35% protein", "1800 kcal/day"), screen candidates with nutrition-reports first, then build the plan here; nutrition-goals is only for changing an already-chosen recipe to hit a number.
---

# Skill: meal-planning

**Needs the Cook MCP server** (tools like `list_recipes` and `write_menu`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Do not plan from recipes you have not seen in the collection.

Use when building or editing a .menu file or a multi-day meal plan. The file format is in the `cooklang://menu-format` resource.

Numeric nutrition targets ("35% protein", "1800 kcal/day") do not move the task
elsewhere — they add a filtering step. Screen the candidates with the
nutrition-reports skill ("Screening a shortlist"), then build the plan here.
The nutrition-goals skill is for *changing* one already-chosen recipe to hit a
number, not for picking recipes that already do.

## Workflow

Gather what you need in as few rounds as possible and decide once; every extra round makes you re-read and re-decide the whole plan.

1. **History.** `list_recipes` with `kind: "menu"` lists the existing plans. Read the one or two most recent (by the dates in their names or sections) with `read_recipe` to learn the user's layout (frontmatter, section names, snacks / batch-prep blocks) and which recipes they used lately. Apply the user's repeat rule (e.g. "nothing from the last two weeks") from that.
2. **Candidates.** `search_recipes` with words and/or a `tag` that match the request (course, cuisine, diet, a key ingredient); `list_recipes` with `kind: "recipe"` to browse the whole collection when the request is open-ended. The folder names (`Breakfast/`, `Dinner/`, `Slowcooker/`) are often the best course signal.
3. **Settle the facts once.** Before choosing, write one short list: the plan's dates, who is eating (counts, ages), the repeat window and what it excludes, the constraints. Use it; do not re-derive any of it later.
4. **Read only the recipes you are seriously considering**, all in one round (`read_recipe` per file, in parallel): check `servings` in the metadata, effort (number of steps, cookware — a slow cooker or one pan + few steps = easy), and dietary constraints from the ingredients. Skip files with no steps — they are placeholders.
5. A .menu may only reference recipes that exist in the collection. If the library lacks options, offer to import one first (recipe-import skill).
6. Match servings to the number of people. Cooking once and eating twice is fine (4 servings for 2 people = leftovers). If the user does not say how many days, plan 3 days.
7. Write the plan in .menu format with YAML frontmatter (at least `servings` and `description`) and a `== Snacks ==` section. Run `validate` with the text as `content` and `as_path` set to the target path, then save with `write_menu`. It checks every recipe reference and refuses to save if one doesn't resolve — fix the path rather than forcing.
8. Tell the user what you saved and where. If they asked for a check on the plan (a balanced-diet or nutrition report), render it now on the saved file — see the nutrition-reports skill.

## Choosing well

- Weeknights: quick, one-pot or few-step recipes; save longer cooks and batch prep for the weekend.
- Reuse ingredients across days (half a bunch of coriander, an opened tin of coconut milk) and put perishables early in the week. With a pantry, `pantry_expiring` says what to use up first and `pantry_recipes` what is already covered.
- Plan leftovers on purpose (cook 4 servings for 2 people, eat it twice) and vary cuisines and main proteins across the days.

## Menu line breaks

Days and meals are written as blocks. A block is a labelled group (e.g. `Breakfast:` and its `- @item` lines, or the `== Snacks ==` list). End every line of a block with a trailing `\` EXCEPT the last line of the block; a blank line separates blocks. The `\` is a soft line break that keeps the block as one rendered step. Example:

```
Breakfast: \
- @./Breakfast/Shakshuka{5%servings} \
- @sourdough bread{5%slices}(toasted) \
- @filter coffee{3%cup} and @tea{2%cup}
```

Do NOT put `\` on the last line of a block, and do not backslash a line followed by a blank line.

## Rules

- Include YAML frontmatter on every .menu — at minimum `servings` and `description`. For the full field set, see the metadata skill. The menu's `servings` is how many people eat (reports divide totals by it); it does not scale the references — each reference's own `{N%servings}` does.
- Default to 3 days when the user does not specify a number.
- Always include a `== Snacks ==` section.
- Date sections use `YYYY-MM-DD` (e.g. `== Day 1 (2026-03-07) ==`) — reason: apps use the date to surface a shortcut to today's plan.
- Pay close attention to each recipe's `servings`/`yield` metadata — reason: mis-scaling here propagates into any shopping list or batch-prep math built from the plan.
- Use `@./path{N%servings}` references to existing recipes (path from the collection root, no `.cook` extension) rather than inlining recipe steps into the menu.
- A recipe with no numeric `servings` can't be scaled by `{N%servings}` — the number silently becomes a plain multiplier (×N) — reason: a 2-portion recipe referenced as `{3%servings}` gets tripled, which inflates the shopping list and every nutrition report. Read its body, judge how many portions it makes, and write a bare factor instead (`{1.5}` for 3 people from a 2-portion recipe). In your reply, name these recipes and offer to add `servings` to them (metadata skill) so future plans scale exactly.
- Save menus into a dedicated `menus/` or `plans/` folder unless the user's layout says otherwise.
- For the shopping list, give the saved plan to `shopping_list`; it follows the references, merges duplicates and subtracts the pantry.
- To *evaluate* a plan's nutrition (per-day calories/macros against targets), follow the nutrition-reports skill. To *change* the plan to hit targets, follow nutrition-goals.

## Do not skip the checks

| Excuse | Rebuttal |
|--------|----------|
| "That recipe is probably in the collection." | Reference only paths you saw in `list_recipes` / `search_recipes`. `write_menu` refuses unresolved references; never set `force: true` to get past one. |
| "The plan looks complete, I'll describe it in chat." | Save it with `write_menu` and say where — a plan in chat is not in the user's collection. |
