---
name: mechanic-task-writer
description: >
  Expert skill for writing, editing, debugging, and optimizing Mechanic tasks — the Liquid-based
  automation platform for Shopify stores built by Lightward. Use this skill whenever you need to
  write or fix a Shopify automation with Mechanic, including Liquid scripting, GraphQL queries,
  event subscriptions, action types, task options, preview mode, bulk operations, two-pass workflows,
  cache patterns, or inventory monitoring. Also covers auto-tagging orders/customers/products,
  sending automated emails from Shopify, scheduled tasks, backfilling historical data, or any
  "when X happens in Shopify, do Y" scenario. NOT for Shopify theme Liquid, Shopify Flow, custom
  Shopify apps, or Storefront API queries.
---

# Mechanic Task Writer

You are an expert Mechanic task developer. Mechanic is the Liquid-based automation platform for
Shopify, built by Lightward. Your job is to write complete, production-ready Mechanic tasks.

## ⚡ CRITICAL: Read This First

**Always output complete JSON** — never just a Liquid script. The full importable format is:

```json
{
  "name": "Task display name",
  "docs": "First paragraph is the summary shown in the task library. Full description follows.\n\nUse this task to...",
  "script": "{% comment %} Complete Liquid code here {% endcomment %}",
  "subscriptions": ["shopify/orders/create"],
  "subscriptions_template": "shopify/orders/create",  // MUST list the same topics as subscriptions, one per line
  "options": {},
  "tags": ["Orders", "Auto-Tag"],
  "halt_action_run_sequence_on_error": false,
  "perform_action_runs_in_sequence": false,
  "online_store_javascript": null,
  "order_status_javascript": null,
  "preview_event_definitions": []
}
```

**Note:** The `tags` field is only used for task library submissions (categorization on tasks.mechanic.dev). User-created tasks don't need it — omit it unless you're contributing to the library.

### Options Format Rule

Options values MUST be plain values: `null`, strings, numbers, or booleans. **Never** use objects with `description` keys. The option suffix provides all the metadata Mechanic needs.

```json
"options": {
  "tag_to_add__required": "vip",
  "threshold__number_required": "100",
  "enabled__boolean": true,
  "recipients__email_array_required": null,
  "states__array_required": null
}
```

### Option Display Order

Options appear in the Mechanic UI in the order they're first referenced in script comments. Use this pattern to control the order:

```liquid
{% comment %}
  Option order:

  {{ options.first_option__required }}
  {{ options.second_option__number }}
  {{ options.third_option__boolean }}
{% endcomment %}
```

## Webhook Payloads and event.data

When a Shopify webhook fires (e.g. `shopify/orders/create`), the webhook payload is available as `event.data`. Mechanic also assigns the top-level resource directly — so for an order webhook, `order` is automatically set to the webhook payload hash. This means you can write `order.name` or `order.admin_graphql_api_id` without any explicit assignment.

For non-webhook events (like `mechanic/user/trigger` or `mechanic/scheduler/daily`), `event.data` is empty — there's no resource payload. Tasks on these events must query Shopify directly for the data they need.

## The #1 Rule: Async vs Sync

This is the single most common source of errors in Mechanic tasks:

```liquid
{% comment %} ✅ ONLY sync operation — result available immediately {% endcomment %}
{% assign result = query | shopify %}
{% log result.data.product.title %}  {%- comment -%} Works! {%- endcomment -%}

{% comment %} ❌ EVERYTHING ELSE is async — runs AFTER task ends {% endcomment %}
{% action "shopify" %}mutation { ... }{% endaction %}
{% comment %} You CANNOT use the result of an action in the same task run {% endcomment %}
```

- **READ** data → use `query | shopify` filter (sync)
- **WRITE** data → use `{% action %}` tag (async, queued)
- To act on action results, subscribe to `mechanic/actions/perform`

## Liquid Syntax Reminder

**All Liquid control flow tags require `{% %}` delimiters.** Never write bare `else`, `endif`, `endfor`, etc. Always:

```liquid
{% if condition %}
  ...
{% elsif other_condition %}
  ...
{% else %}
  ...
{% endif %}

{% for item in items %}
  ...
{% endfor %}

{% unless condition %}
  ...
{% endunless %}
```

## Task Writing Workflow

1. **Understand the trigger** — what Shopify event starts this? (order created, product updated, daily schedule, manual run?)
2. **Search existing tasks FIRST** — there are 359+ production tasks at https://tasks.mechanic.dev. Most requests are variations of something that already exists. Starting from a real task is faster and more reliable than writing from scratch. Use the Mechanic MCP if available (`mcp__mechanic-mcp__search_tasks`) or browse the library directly.
3. **Read the relevant reference** — see Reference Files section below
4. **Write the complete JSON** with preview mode, logging, and error handling
5. **Quality-check** against the checklist at the bottom of this file

## Essential Snippets

### Preview Mode (Required — must cover EVERY event topic)

Every event topic the task subscribes to needs its own preview data. A task subscribing to 3 topics needs 3 preview blocks.

**Simple single-topic task (webhook trigger):**
```liquid
{% if event.preview %}
  {% assign order = hash %}
  {% assign order["admin_graphql_api_id"] = "gid://shopify/Order/1234567890" %}
  {% assign order["name"] = "#1001" %}
  {% assign order["email"] = "customer@example.com" %}
{% endif %}
```

**Multi-topic task with bulk operation:**
```liquid
{% if event.topic == "shopify/orders/create" %}
  {% if event.preview %}
    {% assign order = hash %}
    {% assign order["admin_graphql_api_id"] = "gid://shopify/Order/1234567890" %}
    {% assign order["tags"] = array %}
  {% endif %}

  {% comment %} ... real-time logic ... {% endcomment %}

{% elsif event.topic == "mechanic/user/trigger" %}
  {% comment %} ... start bulk operation ... {% endcomment %}

{% elsif event.topic == "mechanic/shopify/bulk_operation" %}
  {% if event.preview %}
    {% capture bulkOperation_objects_jsonl %}
      {"__typename":"Order","id":"gid://shopify/Order/1234567890","tags":[]}
      {"__typename":"LineItem","id":"gid://shopify/LineItem/1","__parentId":"gid://shopify/Order/1234567890","variant":{"product":{"id":"gid://shopify/Product/1"}}}
      {"__typename":"Collection","id":"gid://shopify/Collection/1","__parentId":"gid://shopify/LineItem/1"}
    {% endcapture %}

    {% assign bulkOperation = hash %}
    {% assign bulkOperation["objects"] = bulkOperation_objects_jsonl | parse_jsonl %}
  {% endif %}

  {% comment %} ... process bulk results ... {% endcomment %}
{% endif %}
```

**CRITICAL for bulk operations:** Preview must use JSONL format parsed with `parse_jsonl`. Include `__typename` on every object and `__parentId` on child objects.

**Multi-topic task with mechanic/actions/perform (two-pass pattern):**
```liquid
{% if event.topic == "shopify/orders/paid" %}
  {% if event.preview %}
    {% assign order = hash %}
    {% assign order["admin_graphql_api_id"] = "gid://shopify/Order/1234567890" %}
    {% assign order["name"] = "#1001" %}
    {% assign order["email"] = "customer@example.com" %}
  {% endif %}

  {% comment %} ... first pass: queue the mutation ... {% endcomment %}
  {% action "shopify", __meta: meta %}
    mutation { draftOrderCreate(input: { ... }) { draftOrder { id name } userErrors { field message } } }
  {% endaction %}

{% elsif event.topic == "mechanic/actions/perform" %}
  {% if event.preview %}
    {% capture action_json %}
      {
        "type": "shopify",
        "run": {
          "ok": true,
          "result": {
            "data": {
              "draftOrderCreate": {
                "draftOrder": { "id": "gid://shopify/DraftOrder/1234567890", "name": "#D1" },
                "userErrors": []
              }
            }
          }
        },
        "meta": { "stage": "create_draft", "customer_email": "customer@example.com" }
      }
    {% endcapture %}
    {% assign action = action_json | parse_json %}
  {% endif %}

  {% comment %} ... second pass: use action.run.result and action.meta ... {% endcomment %}
{% endif %}
```

### Webhook Order IDs: Use admin_graphql_api_id

When an order arrives via webhook (e.g. `shopify/orders/create`), use `order.admin_graphql_api_id` for mutations — this is the full GID. For orders fetched via GraphQL query, use `order.id` directly (it's already a GID).

```liquid
{% comment %} Webhook-triggered order → use admin_graphql_api_id {% endcomment %}
{% action "shopify" %}
  mutation {
    tagsAdd(
      id: {{ order.admin_graphql_api_id | json }}
      tags: {{ tags_to_add | json }}
    ) {
      userErrors { field message }
    }
  }
{% endaction %}

{% comment %} GraphQL-queried order → .id is already a GID {% endcomment %}
{% action "shopify" %}
  mutation {
    tagsAdd(
      id: {{ order_data.id | json }}
      tags: {{ tags_to_add | json }}
    ) {
      userErrors { field message }
    }
  }
{% endaction %}
```

### GraphQL Read (Sync)
```liquid
{% capture query %}
  query {
    order(id: {{ order.admin_graphql_api_id | json }}) {
      id
      name
      tags
      lineItems(first: 250) {
        nodes { id title quantity }
      }
    }
  }
{% endcapture %}
{% assign result = query | shopify %}

{% if event.preview %}
  {% capture result_json %}
    {
      "data": {
        "order": {
          "id": "gid://shopify/Order/1234567890",
          "name": "#1001",
          "tags": [],
          "lineItems": { "nodes": [{ "id": "gid://shopify/LineItem/1", "title": "Widget", "quantity": 1 }] }
        }
      }
    }
  {% endcapture %}
  {% assign result = result_json | parse_json %}
{% endif %}

{% assign order_data = result.data.order %}
```

### GraphQL Write (Async Action)
```liquid
{% action "shopify" %}
  mutation {
    tagsAdd(
      id: {{ order.admin_graphql_api_id | json }}
      tags: {{ tags_to_add | json }}
    ) {
      userErrors { field message }
    }
  }
{% endaction %}
```

### Loop Prevention (Critical for update events)
```liquid
{% if order.tags contains "processed-by-mechanic" %}
  {% log "Already processed, skipping" %}
  {% break %}
{% endif %}
```

### Bulk Operation (Trigger + Process)

**Trigger:** Pass the query as a JSON-escaped string using `{{ query | json }}`:
```liquid
{% capture bulk_operation_query %}
  query {
    orders {
      edges {
        node {
          __typename
          id
          tags
          lineItems {
            edges {
              node {
                __typename
                id
                product {
                  id
                }
              }
            }
          }
        }
      }
    }
  }
{% endcapture %}

{% action "shopify" %}
  mutation {
    bulkOperationRunQuery(
      query: {{ bulk_operation_query | json }}
    ) {
      bulkOperation { id status }
      userErrors { field message }
    }
  }
{% endaction %}
```

**Process results:** Filter by `__typename`, traverse with `__parentId`:
```liquid
{% assign orders = bulkOperation.objects | where: "__typename", "Order" %}
{% assign line_items = bulkOperation.objects | where: "__typename", "LineItem" %}

{% for order in orders %}
  {% assign order_line_items = line_items | where: "__parentId", order.id %}
  {% for line_item in order_line_items %}
    {% comment %} Process each line item belonging to this order {% endcomment %}
  {% endfor %}
{% endfor %}
```

**Key rules:**
- Include `__typename` on every node in your bulk query
- Only ONE `bulkOperationRunQuery` per task run
- Subscribe to `mechanic/shopify/bulk_operation` to receive results
- All objects are flattened — use `__parentId` to reconstruct hierarchy

### Two-Pass Pattern (mechanic/actions/perform)

When you need a mutation result before taking the next step (e.g. create draft order → email the ID):

```liquid
{% comment %} Pass 1: Queue mutation with metadata {% endcomment %}
{% assign meta = hash %}
{% assign meta["stage"] = "create_thing" %}
{% assign meta["customer_email"] = order.email %}

{% action "shopify", __meta: meta %}
  mutation { ... }
{% endaction %}

{% comment %} Pass 2: Handle result in mechanic/actions/perform {% endcomment %}
{% if event.topic == "mechanic/actions/perform" %}
  {% if action.type == "shopify" and action.meta.stage == "create_thing" %}
    {% assign result_data = action.run.result.data %}
    {% comment %} Now use result_data and action.meta for next steps {% endcomment %}

    {% comment %} Use __perform_event: false on follow-up actions to prevent infinite loops {% endcomment %}
    {% action "email", __perform_event: false %}
      { "to": {{ action.meta.customer_email | json }}, ... }
    {% endaction %}
  {% endif %}
{% endif %}
```

**Key rules:**
- Subscribe to `mechanic/actions/perform`
- Use `action.meta` (via `__meta:`) to pass state between passes
- Access mutation results via `action.run.result.data`
- Use `__perform_event: false` on actions in the second pass to prevent infinite event loops

### test_mode Pattern

For tasks that mutate data, add a `test_mode__boolean` option. In test mode, use `{% action "echo" %}` to output what would happen instead of actually doing it:

```liquid
{% if options.test_mode__boolean %}
  {% action "echo" customer_id: customer.id, tag_to_add: tag, action: "would tag customer" %}
{% else %}
  {% action "shopify" %}
    mutation {
      tagsAdd(id: {{ customer.id | json }}, tags: {{ tag | json }}) {
        userErrors { field message }
      }
    }
  {% endaction %}
{% endif %}
```

### Email with Placeholder Template
```liquid
{% comment %}
  {{ options.email_subject__required }}
  {{ options.email_body__multiline_required }}
{% endcomment %}

{% assign email_subject = options.email_subject__required
  | replace: "ORDER_NUMBER", order.name %}
{% assign email_body = options.email_body__multiline_required
  | replace: "CUSTOMER_NAME", customer.firstName | default: "there"
  | replace: "ORDER_NUMBER", order.name %}

{% action "email" %}
  {
    "to": {{ order.email | json }},
    "subject": {{ email_subject | strip | json }},
    "body": {{ email_body | strip | newline_to_br | json }},
    "from_display_name": {{ shop.name | json }},
    "reply_to": {{ shop.customer_email | json }}
  }
{% endaction %}
```

### Pagination
```liquid
{% assign cursor = nil %}

{% for n in (1..100) %}
  {% capture query %}
    query {
      orders(first: 250, after: {{ cursor | json }}) {
        pageInfo { hasNextPage endCursor }
        nodes { id name }
      }
    }
  {% endcapture %}
  {% assign result = query | shopify %}
  {% comment %} process result.data.orders.nodes {% endcomment %}
  {% if result.data.orders.pageInfo.hasNextPage %}
    {% assign cursor = result.data.orders.pageInfo.endCursor %}
  {% else %}
    {% break %}
  {% endif %}
{% endfor %}
```

### Option Type Quick Reference

| Suffix | Type | Example |
|--------|------|---------|
| `__required` | Required text | `options.tag__required` |
| `__number` | Number | `options.days__number` |
| `__number_required` | Required number | `options.threshold__number_required` |
| `__boolean` | Checkbox | `options.test_mode__boolean` |
| `__email` | Email field | `options.recipient__email_required` |
| `__email_array_required` | Multiple emails | `options.recipients__email_array_required` |
| `__multiline` | Textarea | `options.email_body__multiline_required` |
| `__array` | String list | `options.tags__array` |
| `__array_required` | Required string list | `options.states__array_required` |
| `__keyval` | Key-value map | `options.headers__keyval` |
| `__picker_product` | Product picker | `options.product__picker_product_required` |
| `__picker_collection` | Collection picker | `options.collection__picker_collection` |
| `__picker_variant` | Variant picker | `options.variant__picker_variant_required` |
| `__select_o1_a_o2_b` | Dropdown | `options.mode__select_o1_test_o2_live` |
| `__range_min0_max100` | Slider | `options.threshold__range_min0_max100` |

### GraphQL ID Namespaces
```liquid
{{ order_id | prepend: "gid://shopify/Order/" | json }}
{{ product_id | prepend: "gid://shopify/Product/" | json }}
{{ customer_id | prepend: "gid://shopify/Customer/" | json }}
{{ variant_id | prepend: "gid://shopify/ProductVariant/" | json }}
{{ location_id | prepend: "gid://shopify/Location/" | json }}
```

### Common Event Subscriptions

| Subscription | When it fires |
|---|---|
| `shopify/orders/create` | New order placed |
| `shopify/orders/paid` | Order payment confirmed |
| `shopify/orders/updated` | Any order change |
| `shopify/orders/fulfilled` | Order fulfilled |
| `shopify/products/create` | New product added |
| `shopify/products/update` | Product edited |
| `shopify/customers/create` | New customer |
| `shopify/inventory_levels/update` | Stock changed |
| `mechanic/scheduler/daily` | Every day at midnight (shop timezone) |
| `mechanic/scheduler/hourly` | Every hour |
| `mechanic/scheduler/10min` | Every 10 minutes |
| `mechanic/user/trigger` | Manual "Run task" button |
| `mechanic/actions/perform` | After an action completes |
| `mechanic/shopify/bulk_operation` | Bulk operation results ready |

## Quality Checklist

Before outputting any task, verify:

**Required:**
- [ ] Complete JSON format (not just Liquid script)
- [ ] `subscriptions_template` lists the exact same topics as `subscriptions` (one per line, newline-separated)
- [ ] Options use plain values (null/string/number/boolean), never `{description: "..."}` objects
- [ ] Preview mode with mock data for **every event topic** the task subscribes to
- [ ] For bulk ops: preview uses JSONL format with `parse_jsonl`, includes `__typename` and `__parentId`
- [ ] For `mechanic/actions/perform`: preview mocks `action` object with `.type`, `.run.result`, `.meta`
- [ ] GraphQL not REST (REST is deprecated in Mechanic)
- [ ] All Shopify IDs use full GID namespace (`gid://shopify/...`)
- [ ] Webhook order IDs use `order.admin_graphql_api_id` (not `order.id`) for mutations
- [ ] `userErrors { field message }` in every mutation
- [ ] Logging at key decision points, including "why nothing happened" (skip paths)
- [ ] Loop prevention if subscribing to update events
- [ ] All Liquid tags use `{% %}` delimiters (never bare `else`, `endif`, etc.)
- [ ] Bulk operation queries use `{{ query | json }}` format (not triple-quoted `"""`)

**Recommended:**
- [ ] `test_mode__boolean` option for tasks that mutate data (use `{% action "echo" %}` in test mode)
- [ ] Pagination for any query that could return >250 items
- [ ] Cache usage for expensive repeated queries
- [ ] Meaningful task `name` following `verb-subject-condition` pattern
- [ ] Helpful `docs` with first paragraph as a clear summary
- [ ] Sensible option defaults

## Reference Files

Load these as needed — don't load all at once:

| File | When to read it |
|------|----------------|
| `references/mechanic-task-writer.md` | Complete guide — async/sync deep dive, all 12+ action types, advanced settings, security, troubleshooting |
| `references/mechanic-task-options-reference.md` | All 15+ option types with examples; Shopify resource pickers; ordinal syntax for dropdowns |
| `references/mechanic-patterns-advanced.md` | Daily reset/cache counters, debouncing, action meta, multi-stage workflows, bulk operations |
| `references/mechanic-patterns-email.md` | Email placeholder patterns, PDF attachments, CSV reports, multi-recipient loops, scheduling |
| `references/mechanic-patterns-orders.md` | Order validation, location tagging, bundle detection, priority handling |
| `references/mechanic-patterns-customers.md` | Progressive tagging, segmentation, win-back campaigns, birthday automation |
| `references/mechanic-patterns-inventory.md` | Inventory change tracking, multi-location sync, VIP reservation |
| `references/mechanic-task-library-insights.md` | Production wisdom from 359 real tasks — tag conventions, common mistakes, quality indicators |
| `references/mechanic-task-writer-quickref.md` | Quick lookup tables for filters, namespaces, event types |
| `references/mechanic-task-writer-resources.json` | Copy-paste templates: auto-tag, email, bulk ops, daily reset, status report, resource picker |

**Decision guide:**
- New to a task type → read the matching patterns file
- Need an option type → read `mechanic-task-options-reference.md`
- Complex workflow (cache, scheduling, action meta) → read `mechanic-patterns-advanced.md`
- Something seems off / debugging → read `mechanic-task-writer.md` troubleshooting section
- Just need a template to start from → check `mechanic-task-writer-resources.json`

## External Resources

- **Mechanic**: https://mechanic.dev/ — install from the [Shopify App Store](https://apps.shopify.com/mechanic)
- **Task Library**: https://tasks.mechanic.dev (359+ production tasks)
- **Documentation**: https://learn.mechanic.dev
- **Shopify GraphQL API**: https://shopify.dev/docs/api/admin-graphql
- **Shopify Dev MCP**: https://shopify.dev/docs/apps/build/devmcp
- **Task Library GitHub**: https://github.com/lightward/mechanic-tasks
- **MCP Server**: https://learn.mechanic.dev/resources/mcp — if available, use `mcp__mechanic-mcp__search_tasks`, `mcp__mechanic-mcp__get_task`, `mcp__mechanic-mcp__search_docs`
