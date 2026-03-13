---
name: shopifyql
description: >
  Write, debug, and explain ShopifyQL queries and Shopify Segment Query Language expressions.
  Use this skill whenever the user wants to query Shopify analytics data, build customer segments,
  write ShopifyQL for reports, explore sales/orders/products data via the Shopify Admin API,
  debug a ShopifyQL error, understand available tables/dimensions/metrics, or translate a business
  question into a Shopify query. Also triggers for: "ShopifyQL", "Shopify analytics query",
  "customer segment filter", "Shopify segment", "SHOW FROM sales", "GROUP BY in Shopify",
  "Shopify report query", or any mention of ShopifyQL tables like `sales`, `sessions`, `orders`.
---

# ShopifyQL & Segment Query Language

You are an expert in ShopifyQL (Shopify's commerce analytics query language) and the Shopify
Segment Query Language (for customer segmentation). Help users write correct, efficient queries
and explain what results to expect.

---

## 1. ShopifyQL — Analytics Queries

### Required structure

Every ShopifyQL query must have `FROM` and `SHOW`. All other clauses are optional but **must appear
in this exact order**:

```
FROM <table>
SHOW <metric(s)>
[WHERE <condition>]
[GROUP BY <dimension(s)>]
[SINCE <date> UNTIL <date>] | [DURING <named_range>]
[HAVING <metric_condition>]
[ORDER BY <column> ASC|DESC]
[LIMIT <n>]
[VISUALIZE <column> TYPE <chart_type>]
```

Getting the order wrong is the #1 source of ShopifyQL syntax errors. Always verify the order
when debugging.

### Common tables

| Table | What it contains |
|-------|-----------------|
| `sales` | Revenue, orders, AOV |
| `sessions` | Traffic, conversion |
| `products` | Product performance |
| `customers` | Customer behaviour (LTV, cohorts) |
| `inventory` | Stock levels |
| `marketing` | Channel attribution |
| `finance` | Payouts, fees |

Use `FROM ORGANIZATION sales` to query across multiple stores in a Shopify organization.

### Metrics: pre-aggregated vs aggregate functions

The `sales` table exposes **pre-aggregated metrics** — fields that are already summed per row
when grouped. Use them directly in `SHOW` without a function wrapper:

```shopifyql
FROM sales
SHOW net_items_sold, gross_sales, discounts, returns, net_sales, taxes, total_sales
WHERE product_title IS NOT NULL
GROUP BY product_title
SINCE -30d UNTIL today
ORDER BY total_sales DESC
LIMIT 100
```

Available pre-aggregated metrics on `sales`:
`gross_sales`, `discounts`, `returns`, `net_sales`, `taxes`, `total_sales`, `net_items_sold`,
`average_order_value`, `orders_count`, `net_quantity`

**Aggregate functions** (`sum()`, `count()`, `avg()`, `max()`, `min()`) are available on some
plans and tables, but **may not be supported on all store plans**. If you see a parse error like
"Feature not supported: Could not find valid function sum()", use the pre-aggregated metric
directly (e.g. `net_sales` instead of `sum(net_sales)`).

When aggregate functions are available:
```shopifyql
FROM sales
SHOW sum(net_sales) AS revenue, count(orders) AS orders
GROUP BY product_title
SINCE -30d UNTIL today
```

### WHERE — filtering dimensions

Filters run *before* aggregation (like SQL `WHERE`). Only dimensions, not metrics.

```shopifyql
FROM sales
SHOW net_sales, total_sales
WHERE billing_country = 'US'
AND product_type != 'Gift Card'
GROUP BY product_title
SINCE -30d UNTIL today
```

String operators: `=`, `!=`, `STARTS WITH`, `ENDS WITH`, `CONTAINS`
Logical: `AND`, `OR`, `NOT`
**Always use single quotes for string values.**

### GROUP BY — segmenting data

Required whenever you include a dimension in `SHOW`.

```shopifyql
FROM sales
SHOW product_title, net_sales, total_sales
GROUP BY product_title
ORDER BY total_sales DESC
LIMIT 10
```

### Date filtering

Two approaches — use whichever fits:

**Relative offsets (SINCE/UNTIL):**
```shopifyql
SINCE -30d UNTIL today
SINCE -1y UNTIL -1d
```

**Named ranges (DURING):**
```shopifyql
DURING last_month
DURING last_year
DURING this_week
```

**TIMESERIES** — groups results by a time dimension:
```shopifyql
FROM sales
SHOW net_sales, total_sales
TIMESERIES month
SINCE -3m UNTIL today
```
Valid intervals: `hour`, `day`, `week`, `month`, `quarter`, `year`

### HAVING — filtering after aggregation

Like SQL `HAVING`. Filters on metric values after `GROUP BY`.

```shopifyql
FROM sales
SHOW product_title, net_sales, orders_count
GROUP BY product_title
HAVING net_sales > 1000
ORDER BY net_sales DESC
```

### COMPARE TO — period comparison

```shopifyql
FROM sales
SHOW net_sales, total_sales
SINCE -30d UNTIL today
COMPARE TO previous_period
```

Options: `previous_period`, `previous_year`, `previous_year_match_day_of_week`

### WITH modifiers

Append `WITH` to add computed columns:

```shopifyql
FROM sales
SHOW net_sales
TIMESERIES month
WITH PERCENT_CHANGE, CUMULATIVE_VALUES
```

Available: `TOTALS`, `GROUP_TOTALS`, `PERCENT_CHANGE`, `CUMULATIVE_VALUES`, `CURRENCY`, `TIMEZONE`

### VISUALIZE

```shopifyql
FROM sales
SHOW product_title, net_sales
GROUP BY product_title
ORDER BY net_sales DESC
LIMIT 10
VISUALIZE net_sales TYPE bar
```

Chart types: `bar`, `line`, `donut`, `histogram`, `heatmap`, `table`, `single_stat`

### Semi-joins (MATCHES)

Filter by related entities without writing a subquery:

```shopifyql
FROM customers
SHOW customer_id, net_sales
WHERE products_purchased MATCHES (product_tag = 'sale')
GROUP BY customer_id
```

Functions: `products_purchased`, `orders_placed`, `shopify_email.EVENT()`

### Math on metrics

When aggregate functions are available:
```shopifyql
FROM sales
SHOW sum(net_sales) / count(orders) AS aov
```

### Aliases

```shopifyql
SHOW net_sales AS revenue, orders_count AS orders
```

### TOP N

```shopifyql
FROM sales
SHOW top_5(product_title) AS top_products, net_sales AS revenue
GROUP BY top_products
```

The remainder is grouped as "Other".

---

## 2. Segment Query Language — Customer Segments

Segment queries are **WHERE-only** — no `FROM`, `SHOW`, or other clauses. They're used exclusively
in the Shopify Customers API and Admin segment builder.

### Basic syntax

```
<attribute> <operator> <value>
```

Multiple conditions:
```
<condition1> AND <condition2> OR <condition3>
```

**AND takes precedence over OR.** Use parentheses to override:
```
email_subscription_status = 'SUBSCRIBED' AND (customer_countries CONTAINS 'US' OR amount_spent > 500)
```

Limits: max 10 clauses per query.

> **Important:** `COUNT`, `SUM`, `MAX`, `MEDIAN` and other aggregate functions are **not supported**
> in Segment QL. Use direct attribute comparisons only (e.g. `amount_spent > 500`).

### Operators by data type

| Type | Operators |
|------|-----------|
| Boolean | `=`, `!=` |
| Date | `=`, `!=`, `>`, `>=`, `<`, `<=`, `BETWEEN` |
| Enum | `=`, `!=` |
| Float/Integer | `=`, `!=`, `>`, `>=`, `<`, `<=`, `BETWEEN` |
| String | `=`, `!=` |
| List | `CONTAINS`, `NOT CONTAINS` |
| Function | `MATCHES`, `NOT MATCHES` |

### Date formats

Date values in Segment QL do **not** use quotes (unlike strings).

- Absolute date: `2024-01-01`
- Absolute datetime: `2024-01-01T16:00:00` (shop timezone, 24h format)
- Relative offset: `-7d`, `-2w`, `-1m`, `-1y`
- Named: `today`, `yesterday`

```
last_order_date > -30d
first_order_date BETWEEN 2024-01-01 AND 2024-12-31
last_order_date BETWEEN -365d AND -90d
```

Date operators act on complete 24-hour days in the shop's timezone.

### Core attributes

| Attribute | Type | Example |
|-----------|------|---------|
| `email_subscription_status` | Enum | `= 'SUBSCRIBED'` |
| `sms_subscription_status` | Enum | `= 'SUBSCRIBED'` |
| `amount_spent` | Float | `>= 500.00` |
| `number_of_orders` | Integer | `> 5` |
| `customer_tags` | List\<String\> | `CONTAINS 'wholesale'` (case-insensitive) |
| `customer_countries` | List\<Enum\> | `CONTAINS 'US'` |
| `customer_cities` | List\<Enum\> | `CONTAINS 'US-CA-LosAngeles'` |
| `customer_regions` | List\<Enum\> | `CONTAINS 'NY'` |
| `customer_email_domain` | String | `= 'gmail.com'` |
| `customer_language` | String | `= 'en'` |
| `customer_account_status` | Enum | `= 'ENABLED'` |
| `customer_added_date` | Date | `> -90d` |
| `first_order_date` | Date | `< -365d` |
| `last_order_date` | Date | `> -30d` |
| `abandoned_checkout_date` | Date | `> -7d` |
| `predicted_spend_tier` | Enum | `= 'HIGH'` |
| `rfm_group` | Enum | `= 'CHAMPIONS'` |
| `product_subscription_status` | Enum | `= 'SUBSCRIBER'` |
| `companies` | Integer | `= 123456789` (B2B company ID) |
| `created_by_app_id` | Integer | `= 987654321` |

**Note on List\<String\>:** `customer_tags` comparisons are case-insensitive. Enum-based lists
(e.g. `customer_countries`) are case-sensitive.

### Function conditions

**products_purchased** — by product ID, tag, or date:
```
products_purchased MATCHES ()
products_purchased MATCHES (id = 2012162031638)
products_purchased MATCHES (id IN (1012132033639, 2012162031638))
products_purchased MATCHES (id NOT IN (1012132033639))
products_purchased MATCHES (tag = 'sale', date > -90d)
products_purchased MATCHES (id = 1012132033639, date BETWEEN -12m AND today)
```
List can contain up to 500 IDs. Omitting `id` matches all products; omitting `date` matches all time.

**orders_placed** — by order attributes:
```
orders_placed MATCHES (financial_status = 'paid', date > -30d)
```

**shopify_email.EVENT** — by email campaign interaction (no `()` after event name):
```
shopify_email.opened MATCHES (activity_id = 5240029206, date > -30d)
shopify_email.clicked MATCHES (activity_id IN (5240029206, 1932881090))
shopify_email.bounced NOT MATCHES (activity_id = 5240029206, date BETWEEN -12m AND today)
```
Events: `bounced`, `clicked`, `delivered`, `marked_as_spam`, `opened`, `unsubscribed`
List can contain up to 500 activity IDs.

**anniversary()** — yearly recurring dates (e.g. birthdays):
```
anniversary() MATCHES (date = today, attribute = 'birthdate')
```

**customer_within_distance()** — geo-proximity:
```
customer_within_distance() MATCHES (lat = -33.8688, lng = 151.2093, distance = 50, unit = 'km')
```

**storefront_event** — browsing behaviour:
```
storefront_event.product_viewed MATCHES (product_id = 1234567890, date > -7d)
storefront_event.collection_viewed MATCHES (collection_id = 987654321)
```

**store_credit_accounts** — customers with store credit:
```
store_credit_accounts MATCHES (balance > 0)
```

---

## 3. Query writing workflow

When a user asks a business question, follow this process:

1. **Identify the goal** — analytics report (ShopifyQL) or customer segment (Segment QL)?
2. **Pick the table** — for ShopifyQL, identify the correct `FROM` table
3. **Identify metrics vs dimensions** — for `sales`, prefer pre-aggregated metrics directly; dimensions go in `GROUP BY` (and also in `SHOW`)
4. **Add filters** — `WHERE` for pre-aggregation, `HAVING` for post-aggregation
5. **Set the date range** — always include one unless the user wants all-time data
6. **Verify keyword order** — `FROM → SHOW → WHERE → GROUP BY → SINCE/UNTIL → HAVING → ORDER BY → LIMIT`
7. **Add visualisation** if the user wants a chart

---

## 4. Common ecommerce patterns

Reusable starting points for typical Shopify store analytics and segmentation:

**Top revenue products this month (pre-aggregated):**
```shopifyql
FROM sales
SHOW product_title, product_vendor, product_type,
     net_items_sold, gross_sales, discounts, returns, net_sales, taxes, total_sales
WHERE product_title IS NOT NULL
GROUP BY product_title, product_vendor, product_type
DURING last_month
ORDER BY total_sales DESC
LIMIT 20
```

**Channel attribution:**
```shopifyql
FROM sessions
SHOW referrer_source, sessions_count, converted_sessions
GROUP BY referrer_source
SINCE -30d UNTIL today
ORDER BY converted_sessions DESC
```

**Monthly revenue trend:**
```shopifyql
FROM sales
SHOW net_sales, total_sales, orders_count
TIMESERIES month
SINCE -3m UNTIL today
```

**High-value customer segment (for Shopify Customers):**
```
amount_spent > 500 AND number_of_orders >= 3 AND last_order_date > -90d
```

**Re-engagement segment:**
```
last_order_date BETWEEN -365d AND -90d AND number_of_orders > 1
```

**Wholesale/B2B segment:**
```
customer_tags CONTAINS 'wholesale' OR amount_spent > 2000
```

---

## 5. Debugging checklist

When a query errors or returns unexpected results:

- [ ] Keyword order correct? (`FROM → SHOW → WHERE → GROUP BY → SINCE → HAVING → ORDER → LIMIT`)
- [ ] String values in single quotes (not double)? **Dates do NOT use quotes in Segment QL.**
- [ ] Filtering on a *dimension* in `WHERE`, not a metric?
- [ ] `GROUP BY` included when showing a dimension?
- [ ] Segment query doesn't have `FROM`/`SHOW` (those aren't valid in Segment QL)?
- [ ] `AND` precedence understood? (use parentheses for `OR` groups)
- [ ] Rate limit hit? (429 error → wait 60 seconds)
- [ ] **"Feature not supported: Could not find valid function sum()"** → Store plan doesn't support `sum()`. Use pre-aggregated metrics: `net_sales` instead of `sum(net_sales)`, `orders_count` instead of `count(orders)`.
- [ ] **Unexpected "no valid table data" or blank results** → Check `parseErrors` in the raw API response — it contains the specific reason (unsupported function, syntax error, plan restriction).

---

See `references/tables.md` for full lists of available dimensions and metrics per table.

---

## 6. Execution

When the user wants to **run** a query (trigger phrases: "run it", "execute", "run the query",
"what are the results", "show me the data", "get the data", "fetch results"):

1. Ensure a valid ShopifyQL query has been written (write one if needed)
2. **Hand off to the `shopifyql-executor` agent** — do NOT attempt to run the query yourself
3. The executor agent handles credentials, SDK invocation, and output formatting

If no credentials are configured yet, direct them to run `/shopifyql-setup` first.

### Notes for execution

- Queries with `_ms` columns (`lcp_p75_ms`, `inp_p75_ms`) need `--raw` flag — the executor handles this automatically
- Strip any `VISUALIZE` lines before passing to the executor — the API rejects them
- `WITH TOTALS` adds a null-first-column row that the executor filters out automatically

### After execution

Stay in the conversation to help with:
- **Explain the results** — interpret the data in plain language
- **Refine the query** — adjust filters, date ranges, groupings based on what was returned
- **Compare** — help the user understand trends or outliers in the results
