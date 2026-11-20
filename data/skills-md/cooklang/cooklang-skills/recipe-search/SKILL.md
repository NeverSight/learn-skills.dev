---
name: recipe-search
description: Use when the user wants to find recipes in their Cooklang collection (.cook files, .menu plans) by ingredient, tag, cuisine, course, title or a half-remembered phrase - "what recipes use chickpeas?", "find my Italian dinners", "where's that lemon cake?".
---

# Skill: recipe-search

Use when the user wants to find recipes in their collection.

**Needs the Cook MCP server** (tools like `search_recipes` and `read_recipe`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Do not guess at what the collection holds.

## The tools

- `search_recipes` — `query` and/or `tag`. Returns `hits` (`path`, `name`): best match first when there is a `query`; a `tag`-only search is sorted by path.
  - **Every word in `query` must match** (AND), case-insensitively, as a substring of the file name or the file's text (frontmatter, ingredients, steps, notes). `chicken rice` finds recipes with both; `tomato` also matches `tomatoes`.
  - `tag` keeps only files whose frontmatter `tags` list contains that tag (case-insensitive, whole tag). `query` may be empty when `tag` is set.
- `list_recipes` — browse instead of search: `dir` for one folder (folder names are often the course: `Breakfast/`, `Desserts/`), `kind` `"recipe"`, `"menu"` or `"all"`.
- `read_recipe` — a hit's metadata (servings, time, tags) and steps, when you need them.

## Workflow

1. Turn the request into the narrowest cheap search:
   - an ingredient or dish → `query` with one or two distinctive words (`chickpea`, `lemon cake`);
   - a tag the collection uses (`vegetarian`, `quick`) → `tag`;
   - a course → `list_recipes` with `dir` when the collection has a folder for it;
   - a cuisine or diet → try `tag` first, then `query` (it also matches frontmatter like `cuisine: Italian`).
2. Too many hits: add a word or a `tag`. None: drop a word, try a shorter stem (`aubergin` for aubergine/aubergines), or a synonym (`courgette`/`zucchini`). For "X or Y", run one search per word and merge the results.
3. Present hits as a short list of names with their paths. Read only the few you need to say more about (servings, time) — not every hit.
4. Offer the obvious next step: open one, scale it (scale-recipe), add it to a plan (meal-planning), or build a shopping list (shopping-list).

## Rules

- Only name recipes the tools returned, with their paths exactly as returned. If nothing matches, say so and offer to import one (recipe-import).
- "What can I cook with what I have?" is a pantry question: use `pantry_recipes` (pantry skill).
- Nutrition criteria ("over 30 g protein") are a screen, not a search: narrow here first, then follow nutrition-reports ("Screening a shortlist").
- If searches keep missing because tags are inconsistent (`Italian` vs `italian` vs `italian-food`), mention it and offer the organize-collection audit.
