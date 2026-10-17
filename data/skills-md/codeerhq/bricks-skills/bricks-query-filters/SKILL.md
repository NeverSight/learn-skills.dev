---
name: bricks-query-filters
description: "Build or debug Bricks Query Filters, including source fields, target query bindings, indexing and AJAX result states."
---

# Bricks: query filters

Connect each filter to its target query and verify indexing for sources that require it.

## The 8 filter elements

Defined at `includes/query-filters.php:705-716` and `includes/elements/filter-*.php`.

| Element | `$name` | Use when | Filter type |
|---|---|---|---|
| Filter - Checkbox | `filter-checkbox` | Multi-select values, taxonomies | `checkbox` |
| Filter - Radio | `filter-radio` | Single-select value | `radio` |
| Filter - Select | `filter-select` | Single-select dropdown | `select` |
| Filter - Range | `filter-range` | Numeric range (price, rating) | `range` |
| Filter - Search | `filter-search` | Text search across fields | `search` |
| Filter - Datepicker | `filter-datepicker` | Date range filter | `datepicker` |
| Filter - Submit / Reset | `filter-submit` | Explicit submit/reset button (non-live forms) | `apply` or `reset` (via `filterButtonType`) |
| Filter - Active Filters | `filter-active-filters` | Shows currently-active filters as chips | `active-filters` |

Every filter element extends `Filter_Element_Base` in `includes/elements/filter-base.php`.

## Target-query binding

Every filter element has a **`filterQueryId`** setting pointing at the query-element `_id` it filters. Without it, the filter does nothing: no error, no warning. The dropdown in the builder is labelled **"Target query"** and lists all query-producing elements on the page.

Where it lives: `filter-base.php:1100-1108`, control type `query-list`.

**Rules:**
- The target element must exist on the same page (header/footer queries can be targeted from the page if they're visible in the tree).
- The target must be a query-producing element: Posts, Users, Terms, Container/Block/Section/Div with query-loop enabled.
- Setting the target on one filter doesn't set it on sibling filters: each filter needs its own `filterQueryId`.
- MCP: `set-filter-target-query` updates this on one filter; `update-filter-element` can update it alongside other config.

## The filter index

Filters that populate options from the database need indexed values. Bricks maintains table `{prefix}bricks_filters_index` (defined at `query-filters.php:7`).

**Indexable filter types** (`query-filters.php:740-748`): `checkbox`, `radio`, `select`, `range`, `datepicker`. Not indexable: `search`, `submit`, `active-filters`.

**Index triggers:** Bricks hooks post, term, user, and meta changes while Query Filters are enabled: `save_post`, `delete_post`, `set_object_terms`, `updated_post_meta`, `deleted_post_meta`, `edit_attachment`, `edited_term`, `delete_term`, `profile_update`, `user_register`, and `delete_user`. It also watches Bricks-content meta writes through `update_post_metadata` / `added_post_meta` so filter elements stay registered.

**Enable the feature first:** filter elements exist only while Query Filters are
enabled (`enableQueryFilters`, via `bricks/set-global-settings`). On Bricks
versions that do not say so, a disabled feature surfaces as a missing
`add_element_filter-*` permission; check the setting before treating that as a
deliberate restriction.

**Reindex through MCP:** `bricks/reindex-filters` takes `{}`, requires
`manage_options` and mirrors `WP Admin > Bricks > Settings > Query filters >
Regenerate filter index`. Every call rebuilds the whole index, so read `pending`
and `progress` from its result rather than calling it again. If a saved filter
shows no options, call it once, then check the rendered options.

Reindex may be needed after:
- Bulk-importing posts / users / terms (the triggers fire per-item but may be slow or skipped in bulk imports).
- Enabling a new filter on an existing field.
- Changing the indexed field's structure.

**Serialized meta values:** if the meta field stores serialized data (PHP-serialized array / JSON blob), filters can't index it as separate selectable values unless something expands it into rows. `bricks/query_filters/custom_field_index_rows` can do that for non-native providers such as ACF or Meta Box. Current source only applies that filter when `$provider !== 'none'`; plain native post meta is stored as one raw value by `generate_custom_field_index_rows()` (`includes/query-filters.php:1975-2024`).

```php
add_filter( 'bricks/query_filters/custom_field_index_rows', function( $rows, $object_id, $meta_key, $provider, $object_type ) {
    if ( $meta_key !== 'my_array_field' || $object_type !== 'post' ) return $rows;

    $raw = get_post_meta( $object_id, $meta_key, true );
    $decoded = maybe_unserialize( $raw );

    if ( ! is_array( $decoded ) ) return $rows;

    return array_map( fn( $v ) => [
        'filter_value' => $v,
        'filter_value_display' => $v,
    ], $decoded );
}, 10, 5 );
```

## Data sources

Filters that populate selectable values use **`filterSource`** (`filter-base.php`). Core Bricks registers three sources:

| Source | Setting keys | Use for |
|---|---|---|
| `taxonomy` | `filterTaxonomy`, `filterTermInclude`, `filterTermExclude`, `filterTaxonomyOrder`, `filterTaxonomyOrderBy` | WP taxonomies (category, post_tag, product_cat, custom taxonomies) |
| `wpField` | `sourceFieldType` (post/user/term), `wpPostField` / `wpUserField` / `wpTermField` | Native WP fields: post_author, post_date, user_role, etc. |
| `customField` | `sourceFieldType`, `customFieldKey`, label mapping | ACF / Meta Box / Pods / native meta keys |

WooCommerce adds `wcField` when its query-filter integration is active (`includes/integrations/query-filters/woocommerce.php:22-85`).

Custom providers can be registered via `bricks/filter_element/data_source_{source_key}`: see the `bricks-hooks-reference` skill.

## Frontend handshake: what actually happens on click

1. User clicks a filter option.
2. Bricks frontend JS reads filter instances from `window.bricksData.filterInstances` and the selected filter state.
3. It POSTs JSON to the Bricks REST endpoint `query_result` with `queryElementId`, `postId`, selected filters, original query vars, language, and template context (`src/assets/js/frontend.js:13313-13370`).
4. `Api::render_query_result()` runs the target query with the filter's meta_query / tax_query injected (`includes/api.php:1490-1530`).
5. Returns HTML for the target query's loop. Frontend swaps it in, updates URL via pushState.

**The 3 conditions the target query must meet for AJAX swap to work:**
1. The query loop emits Bricks loop markers. Current source adds `data-brx-loop-start` on server render and frontend JS converts it to `<!--brx-loop-start-{queryId}-->`.
2. No optimizer or cache layer removes those markers. Preserve Bricks `brx-loop` markers in HTML optimization settings.
3. The target query's `_id` actually matches what the filter sent. This can break after duplicating a component or section that contains the query.

## Components and filter targets

Current Bricks has component-aware query-loop handling: query trails can carry `data-query-component-id`, and frontend AJAX uses that component id when locating the loop DOM (`includes/elements/base.php:4163-4168`, `src/assets/js/frontend.js:2157-2210`).

Still, a filter only works when its `filterQueryId` points to a query instance present on the rendered page. If a component instance contains a filter but not the matching query, the filter has no usable target. Prefer keeping the filter and its target query together at the page/template level, or ship them together inside the same component.

## Scope rule: "Use query filter" on the source loop

Some loops need explicit opt-in for filter compatibility: primarily **nested loops and loops populated via `bricks/query/run`**. The flag `useQueryFilter` lives on the query-producing element. For standard Posts/Users/Terms loops at the page level, the flag is typically on by default.

If your filter UI renders but the target loop doesn't swap: check the target loop's settings panel for a "Use query filters" / "Filterable" toggle and enable it.

## Hooks: when the UI isn't enough

| Hook | Kind | Purpose |
|---|---|---|
| `bricks/filter_element/controls` | filter | Mutate the builder controls for all filters |
| `bricks/filter_element/populated_options` | filter | Mutate the option list after population |
| `bricks/filter_element/data_source_{source}` | filter | Register/mutate a custom data source |
| `bricks/filter_element/count_source_{source}` | filter | Custom per-source count for result-count display |
| `bricks/filter_element/filtered_source` | filter | Final filtered source |
| `bricks/query_filters/custom_field_meta_query` | filter | Customize meta_query for custom-field filters |
| `bricks/query_filters/range_custom_field_meta_query` | filter | Same for range filters |
| `bricks/query_filters/datepicker_custom_field_meta_query` | filter | Same for datepicker filters |
| `bricks/query_filters/custom_field_index_rows` | filter | Expand serialized/array meta into index rows |
| `bricks/query_filters/get_filter_object_ids` | filter | Object IDs a filter restricts to |
| `bricks/filter/taxonomy_args` | filter | Args for taxonomy term query |
| `bricks/filter_element/datepicker_db_date_format` | filter | DB date format for datepicker |

See the `bricks-hooks-reference` skill for the full index.

## Silent-failure debug order

1. **Filter renders but nothing happens on click?**
   a. Open DevTools Network tab, click a filter option. Do you see a POST to the Bricks REST `query_result` endpoint? No -> frontend JS broken (check for JS errors, conflicting scripts).
   b. Request fires but returns empty HTML -> `filterQueryId` doesn't match any query on the page, or target query has no results with the filter applied.
   c. Request succeeds, HTML comes back, but DOM doesn't update -> loop-marker stripping or target mismatch. Check source for `data-brx-loop-start` and the live DOM for `brx-loop-start`.

2. **Custom-field filter shows no options?**
   a. Use `bricks/reindex-filters` for authorized indexing repair; verify its result and the rendered options.
   b. If the field is serialized/array: hook `bricks/query_filters/custom_field_index_rows` to unpack.
   c. If the field was just added: save any post of that type once: that triggers per-post indexing.

3. **Filter options show but selecting them doesn't narrow results?**
   a. Wrong meta comparison: numeric field using string compare. Hook `bricks/query_filters/custom_field_meta_query` to fix.
   b. Values include whitespace / case mismatch: index holds one form, frontend sends another.

4. **"Active filters" element shows nothing even after filtering?**
   a. It needs its own `filterQueryId` set to the same target. It's not auto-bound.

5. **Works on one page, breaks on another?**
   a. Component duplication changed the target ID. Check `filterQueryId` against the rendered query instance.
   b. Header/footer loop targeted from a page, but header/footer render order doesn't include it on the archive. Move the target.

6. **Datepicker filter compares against the wrong format?**
   a. Hook `bricks/filter_element/datepicker_db_date_format` to match the stored format.

## MCP abilities for query filters

- `list-query-filters`: enumerate every filter element on a page, with target binding status.
- `get-filter-element`: full settings of one filter.
- `update-filter-element`: update any filter's config (source, options, target).
- `set-filter-target-query`: quick-path for the most common mistake (missing target binding).
- `reindex-filters`: rebuild the index and run one bounded pass; requires `manage_options`.

The `bricks-query-loops` skill covers the source-loop side of filter/loop integration.

## Never do

- Expect a filter with no `filterQueryId` to work. It won't, and there's no error.
- Put filters inside components that might render on pages without their target query.
- Trust that a custom-field filter has options immediately after bulk-importing the field's data. Always reindex.
- Remove Bricks loop markers during HTML optimization.
- Use `search` filters on large datasets without a proper search index (ElasticPress, Algolia). Bricks' default search is a `LIKE '%term%'` against post_title/post_content: slow on 10k+ rows.
