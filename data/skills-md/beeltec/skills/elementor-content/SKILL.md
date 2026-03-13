---
name: elementor-content
description: Use when creating, reading, updating, or deleting Elementor page builder content — editing exported JSON template files or WordPress database records via WP-CLI. Covers pages, templates, containers, sections, and all built-in widget types.
---

# Elementor Content

Directly read, create, modify, and restructure Elementor page builder content by working with the underlying JSON data — either in exported `.json` template files or in the WordPress database via WP-CLI.

## When to Use

- Creating or editing Elementor page/template content
- Modifying widget settings (text, images, styles, links)
- Restructuring page layouts (moving sections, adding containers)
- Bulk-updating content across multiple Elementor pages
- Importing/exporting Elementor templates
- Building new Elementor pages from scratch
- Creating Theme Builder templates (header, footer, single, archive) programmatically

## Operational Modes

### Mode 1: JSON Template Files

Work directly with `.json` files exported from Elementor (Library → Export Template). Read, edit, and write the file. Import back via Elementor UI or WP-CLI.

### Mode 2: WP-CLI Database Operations

Read/write the `_elementor_data` post meta key in WordPress. Requires WP-CLI access and a running WordPress installation. See `references/wp-cli-operations.md`.

## Core Workflow

1. **Identify mode** — JSON file on disk, or live WordPress database?
2. **Read** the content — parse the JSON file or fetch via `wp post meta get`
3. **Understand the tree** — Elementor content is a nested array of elements (see `references/element-structure.md`)
4. **Locate target** — find the element to modify by walking the tree; match on `widgetType`, `settings` content, or `id`
5. **Modify** — change settings, add/remove/reorder elements
6. **Validate** — run the validation checklist below before writing
7. **Write** — save the JSON file or update via `wp post meta update`
8. **Flush cache** — if using WP-CLI, run `wp elementor flush-css` to regenerate stylesheets

## Reference Guides

| Topic | File | Load when... |
|-------|------|-------------|
| JSON structure & hierarchy | `references/element-structure.md` | You need to understand the data format, nesting rules, or settings patterns |
| Widget types & settings | `references/widget-catalog.md` | You need to create a widget or modify widget-specific settings |
| WP-CLI operations | `references/wp-cli-operations.md` | You're working with a live WordPress database (not a JSON file) |
| Theme Builder templates | `references/theme-builder-templates.md` | You're creating header, footer, single, or archive templates programmatically |

## Quick Reference: Common Operations

**Change a heading:**
Find the element with `"widgetType": "heading"`, update `settings.title`.

**Add a button to a container:**
Create a new element with `"elType": "widget"`, `"widgetType": "button"`, generate a unique `id`, set `settings.text` and `settings.link`, and append to the parent container's `elements` array.

**Restructure layout:**
Move elements between parent containers by cutting from one `elements` array and pasting into another. Ensure no element appears in two places.

**Create a new page:**
Build the full JSON tree: outer container(s) → inner containers/widgets. Wrap in template format if exporting, or write directly to `_elementor_data` via WP-CLI.

**Create a Theme Builder template:**
Requires post meta (`_elementor_template_type`, `_elementor_conditions`), taxonomy term (`elementor_library_type`), AND registration in the `elementor_pro_theme_builder_conditions` option. See `references/theme-builder-templates.md` for the full checklist — missing any step will silently fail.

**Change styling:**
Modify the relevant settings key on the element. Responsive variants use `_tablet` and `_mobile` suffixes. Dimensions use `{top, right, bottom, left, unit, isLinked}` objects.

## Element ID Generation

Every element requires a unique `id` — an **8-character lowercase hexadecimal string** (e.g., `"3f2a1b7c"`). Generate randomly; ensure no duplicates within the document.

## Constraints

- **MUST** preserve valid JSON at all times
- **MUST** keep every element's `id` unique within the document
- **MUST** maintain correct nesting: containers hold containers or widgets; widgets have `"elements": []` (empty)
- **MUST** include `elType` on every element
- **MUST** include `widgetType` on every widget element
- **MUST NOT** place widgets directly inside the root array — they must be inside a container (or legacy section → column)
- **MUST NOT** leave orphaned references (e.g., removing a container but leaving its children elsewhere)
- **MUST** flush CSS cache after database writes (`wp elementor flush-css`)

## Validation Checklist

Before writing the modified content:

- [ ] Valid JSON (parseable without errors)
- [ ] All `id` values are unique 8-char hex strings
- [ ] Every element has `elType` set (`"container"`, `"widget"`, `"section"`, or `"column"`)
- [ ] Every widget has `widgetType` set to a valid type
- [ ] Widgets have `"elements": []` (empty array, never omitted)
- [ ] No widgets at root level — all wrapped in containers
- [ ] Settings values use correct format (dimensions, URLs, media objects)
- [ ] Template wrapper (if applicable) has `type`, `version`, `title`, `content`
