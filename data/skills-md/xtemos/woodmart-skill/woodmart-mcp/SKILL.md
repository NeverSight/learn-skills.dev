---
name: woodmart-mcp
description: "Use for WoodMart site work through the wood MCP abilities (woodmart/*): finding or creating content, editing Gutenberg blocks, changing theme settings or header logos, and creating or assigning WoodMart layouts. Covers the queued block-finalization workflow and the safety rules that coordinate multiple abilities."
---

# Working with WoodMart via MCP abilities

## Use live ability documentation

Everything runs through the wood MCP adapter. Use `mcp-adapter-discover-abilities` for
the current ability list and `mcp-adapter-get-ability-info` before the first use of a write
ability, or whenever its parameters are uncertain. Treat the live description, input schema,
response fields, warnings, and `user_instruction` as authoritative; do not rely on remembered
parameter lists.

Use `mcp-adapter-execute-ability` with `ability_name` and `parameters` to execute an ability.

## Routing

| Intent | Start with |
|--------|------------|
| Find a page, post, product, portfolio project, or HTML block | `woodmart/search-content` |
| Create a page, post, portfolio project, or HTML block | `woodmart/create-content` |
| Rename, publish, re-slug, or re-parent content | `woodmart/update-content` |
| Read a target's block tree | `woodmart/gutenberg-get-content` |
| Change blocks in a non-empty target | `woodmart/gutenberg-edit-blocks` |
| Fill an empty target or deliberately rebuild all of it | `woodmart/gutenberg-add-pending-change` |
| Discover blocks and their attributes | `woodmart/gutenberg-list-blocks`, then `woodmart/gutenberg-describe-block` |
| Reuse a demo section or page | `woodmart/gutenberg-search-templates`, then `woodmart/gutenberg-get-template` |
| Read or change a theme setting | `woodmart/list-theme-settings`, then `woodmart/get-theme-setting` |
| Replace Header Builder logos | `woodmart/replace-header-logo` |
| Discover, create, or assign layouts | `woodmart/list-layout-types`, then the relevant layout ability |

An `id` from `search-content`, or a layout's `target_id` from `list-layouts`, is the
`target_id` for Gutenberg abilities.

## Block-write rules

These rules are non-negotiable because violating them can silently lose content or styling.

1. **Never rebuild a target to change only part of it.** Read it with
   `gutenberg-get-content`, then use `gutenberg-edit-blocks` and send only the operations and
   attribute keys that change. This includes requests such as “update all texts on the page.”
   Untouched blocks and attributes must be omitted.
2. Use `gutenberg-add-pending-change` only for an empty target or when the user explicitly asks
   to replace/rebuild the entire target.
3. Author text and content in the attribute named by `gutenberg-describe-block`'s
   `contentAttribute`. Do not hand-write `innerHTML` for content updates. Existing `innerHTML`
   is round-trip data for content the agent is preserving, or verbatim markup supplied for an
   intentional insert.
4. Only `wd/*` blocks have stable `blockId` values and can be addressed by id. Core blocks pass
   through but cannot be individually updated, deleted, moved, or used as anchors.
5. Omit `attributes.blockId` when authoring or inserting a `wd/*` block; normalization creates
   it. Use ids copied from `gutenberg-get-content` only as operation selectors or anchors—never
   invent, copy, reuse, or send one inside update `attributes`.
6. Pass `expected_content_hash` from the latest `gutenberg-get-content` response when editing.
   On a conflict, re-read the target and rebuild the intended operations against the new tree.

If a deliberate full replacement might touch classic/freeform content outside registered
blocks, first read with `include_raw_content: true`; `block_spec` otherwise cannot represent
that content. Do not use full replacement as a workaround for this limitation.

### Choosing the write path

```text
Existing blocks?
├── no  → create-content with block_spec, or gutenberg-add-pending-change
└── yes → Explicit full rebuild requested?
          ├── no  → gutenberg-edit-blocks
          └── yes → gutenberg-add-pending-change
```

For a text edit, describe the block if the content attribute is not already known, then update
only that attribute:

```json
{
  "target_id": 123,
  "expected_content_hash": "...",
  "operations": [
    { "op": "update", "blockId": "a1b2", "attributes": { "content": "New heading" } }
  ]
}
```

## Authoring from scratch

1. Use `gutenberg-list-blocks`, then `gutenberg-describe-block` for every block being authored.
2. Fetch referenced `styleGroups` or `composites` with
   `gutenberg-describe-attribute-group` only when that styling is needed.
3. Follow the returned `composition`, `nesting`, `conventions`, examples, units, responsive
   attributes, and data-resolver hints. Do not invent block attributes or site-specific ids.
4. For layouts, pass the relevant type's `block_categories` from `list-layout-types` to
   `gutenberg-list-blocks`.
5. Prefer a library template when it matches the requested section or page. Use its returned
   `block_spec`; demo images are localized during finalization.

## Finalization

Every block-content write is queued and is not live until its batch reaches `finalized`.
Metadata, theme-setting, header-logo, predefined-layout, and layout-condition writes do not use
the block queue.

1. Follow the queue response's `user_instruction`. Ask the user to keep
   **WoodMart → Tools → AI Block Queue** open in wp-admin.
2. Call `gutenberg-enable-finalization` when the response says the batch is still a draft.
   `create-content` or `create-layout` with `block_spec` already marks its batch ready, so do not
   enable it again.
3. Poll `gutenberg-get-pending-batch` until `finalized`, `failed`, or `conflicted`.
4. On `conflicted`, re-read the target and repeat the edit against the current content.

Only one active pending change may exist per target. Cancel an obsolete non-finalized batch
with `gutenberg-delete-pending-batch` before queuing a replacement.

## Immediate writes and reporting

### Content metadata

`update-content` changes metadata immediately and never changes blocks.

- Publishing is outward-facing. Set `status: "publish"` only when the user requested it or
  explicitly confirmed it.
- Changing the slug or parent of published content moves its public URL. Obtain confirmation
  unless the user explicitly requested that URL change.
- Read and relay the response's `warnings`, actual `after.slug`, and resulting URL. Published
  hierarchical pages do not receive WordPress's old-slug redirect; their old URL can become a
  404.
- There is no trash/delete-content ability. Do not simulate deletion by blanking block content.

### Theme settings and logos

- Find a theme-setting id with `list-theme-settings`; do not guess it.
- Read the full descriptor with `get-theme-setting` immediately before writing. Honor
  `writable`, `value_format`, `options`, `current_value`, and `has_preset_overrides`.
- `update-theme-setting` writes the base layer. A preset override may still determine the
  visible value; report that instead of retrying blindly.
- `replace-header-logo` requires an existing media-library image `attachment_id` and updates
  every saved header. Read the per-header statuses and `totals`; report skipped or failed
  headers rather than claiming blanket success.

### Layouts

- Start with `list-layout-types`. Use its live `type`, `block_categories`, `predefined`, and
  `condition_types` data rather than maintaining local enums.
- Edit an existing layout's blocks with Gutenberg abilities against its `target_id`; do not
  recreate the layout merely to change its content.
- `set-layout-conditions` replaces the complete condition set. Send every condition that must
  remain; `[]` unassigns the layout.
- Build each condition using the selected layout type's `condition_types` entry and its
  `query_kind` (`none`, `scalar`, `array`, or `number_range`).
- `is_assigned` is request-context-dependent over MCP. Inspect stored `conditions`; do not
  rewrite them solely because `is_assigned` is false.

## Portfolio and site-specific ids

A portfolio project is content of post type `portfolio`; find/create it and edit its Gutenberg
blocks like a page. `single_portfolio` and `portfolio_archive` are layouts controlling how
projects or archives render. Portfolio content requires the Portfolio theme option to be enabled.

Never invent product, category, taxonomy, media, post, or template ids. Resolve them with the
relevant live query/search ability, or use a dynamic block query when explicit ids are unnecessary.
