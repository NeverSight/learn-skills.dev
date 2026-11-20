---
name: report-authoring
description: Use when the user wants to write or run a custom Jinja report template over a Cooklang recipe (.cook) or meal plan (.menu) with render_report - a computed value, a cost estimate, a custom summary or printout - or save a reusable report template. For nutrition use nutrition-reports; for a plain format conversion use export-recipe.
---

# Skill: Report Authoring

**Needs the Cook MCP server** (tools like `render_report` and `write_config`). If these tools are missing, the Cook MCP server isn't connected: if you installed the cooklang plugin or extension, check that its `cook` server is running (e.g. `/mcp`) or reinstall it; otherwise add it from https://github.com/cook-md/cook-mcp. Do not compute report values by hand instead.

Author and run **Jinja2 report templates** over the user's recipes with the
`render_report` tool — or reuse a saved one — then answer from the output or
present the report. Use this skill when the user wants a computed value
(ingredient counts, a scaled printout), a custom report or summary, or a new
report template. For nutrition or dietitian-style evaluations, follow the
nutrition-reports skill instead.

Templates that don't call nutrition functions render locally, with no login.
Datastore values live in YAML files under `db/`; cook-mcp has no tool that
writes them, so ask the user to add data there (or use your client's file
tools).

## The tool

`render_report` renders one template against one `.cook` recipe or `.menu`
plan and returns `{ "rendered", "checks", "resolve_failures" }`, or an error
naming the template line. It never edits files.

Arguments — the template, **exactly one** of:
- `template` — inline Jinja2 source, for drafts and one-off reports.
- `template_path` — a saved template file, relative to the collection root
  (e.g. `reports/cost.md.jinja`). Prefer it whenever a suitable saved
  template exists.

The input, **exactly one** of:
- `input_path` — a `.cook` or `.menu` file as `list_recipes` returned it (kind
  inferred from the extension).
- `input` — inline Cooklang text, with `kind` (`"cook"` or `"menu"`).

Optional:
- `scale` — recipe scale factor (default 1). Scales `.cook` recipes only, not
  `.menu` quantities.
- `base_path` — folder that `@./` references resolve from; defaults to the
  collection root, which is almost always right.

## Template context and filters

Within a template you have:
- `ingredients` — list; each item has `.name` and `.quantity`.
- `metadata` — recipe metadata, including `metadata.title` and any custom keys.
- `scale` — the numeric scale factor.
- For `.menu` input: `plan` — the plan's days and meals with their expanded
  ingredients (a menu is read through `plan.*`, not `ingredients`).

Collection data:
- `aisled(ingredients)` — groups ingredients by store aisle from
  `config/aisle.conf`: a map of aisle → items, unlisted items under `other`.
  Use it with `| items`.
- `excluding_pantry(ingredients)` — drops ingredients already in
  `config/pantry.conf`; `from_pantry(ingredients)` keeps only those.
- `db('key.path')` — reads the collection's YAML datastore, the `db/` folder
  at the root: `db('eggs.shopping.price')` is the `price` key of
  `db/eggs/shopping.yml`. Use it for per-ingredient data the recipes don't
  carry (prices, shelf life, densities). A missing key renders empty.

Filters available:
- Standard Jinja: `sort(attribute='name')`, `default(...)`, `round`, `join`,
  `selectattr`, `items`, `length`.
- Text: `titleize`, `humanize`, `upcase_first`.
- Numbers: `number_with_precision`, `number_with_delimiter`,
  `number_to_percentage`, `number_to_currency`, `format_price`, `numeric`.

Example — an ingredients list:

```jinja
# {{ metadata.title | default("Ingredients") }}

{% for ingredient in ingredients | sort(attribute='name') -%}
- {{ ingredient.name }}{% if ingredient.quantity %}: {{ ingredient.quantity }}{% endif %}
{% endfor %}
```

Example — a cost estimate from the datastore, skipping what's in stock:

```jinja
{% set ns = namespace(total=0) %}
{% for aisle, items in aisled(excluding_pantry(ingredients)) | items %}
## {{ aisle | titleize }}
{% for i in items -%}
{% set price = db(i.name ~ '.shopping.price') %}
- {{ i.name }}{% if price %}: {{ price | format_price }}{% set ns.total = ns.total + price %}{% endif %}
{% endfor %}
{% endfor %}
**Estimated total:** {{ ns.total | format_price }}
```

For a plain shopping list, use the `shopping_list` tool rather than a template:
it merges duplicates across recipes, groups by aisle and subtracts the pantry.

## Workflow: reuse or author -> render -> present

1. Saved templates live in `reports/` (CookCLI) or `config/reports/` (Cook
   Editor): `list_recipes` `kind: "template"` lists both. If one matches the request (read the name;
   ask the user when it isn't conclusive), render it with `template_path` and
   skip to step 4.
2. Otherwise draft the template inline.
3. Call `render_report` with `template`. If it errors, read the message
   (minijinja reports the line), fix the template, and render again until it
   renders cleanly.
4. To answer a question (e.g. "how many ingredients?"), read `rendered` and
   reply with the answer. To present a report, show the rendered markdown to
   the user as it came back.

## Saving a reusable template

When the user wants to keep a report, save the template as a `.jinja` file:
- Save it where the collection already keeps templates — `reports/` (CookCLI)
  or `config/reports/` (Cook Editor), whichever `list_recipes`
  `kind: "template"` shows in use; default `reports/`. Subfolders are fine.
- Declare the output format via the inner extension:
  `weekly-cost.md.jinja` -> markdown, `menu.html.jinja` -> HTML,
  `shopping.txt.jinja` -> plain text.
- Save it with `write_config` (`path` e.g. `reports/weekly-cost.md.jinja`,
  the full template as `content`), and tell the user where.
- From then on, render it with `template_path` — never re-send the source
  inline.

Render inline for one-off questions; offer once to save a template, and save
only if the user accepts.
