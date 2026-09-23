---
name: kolsprite-search
description: Use compatible KOLSprite MCP tools for a straightforward current TikTok creator, product, video, or shop lookup. Use for searches, filters, profiles, comparisons, and returned statistics. Do not use for multi-step opportunity evaluation, cold-start planning, content strategy, creator-program design, competitor diagnosis, or growth strategy.
---

# KOLSprite Search

Route a direct TikTok data request to the smallest useful call through the active connection that exposes the compatible KOLSprite tool contract. Use MCP automatically; do not ask whether to use it.

## Compatible MCP routing

- Prefer the SellerSpace Yunya unified MCP when it is available and authenticated.
- Support direct business tools plus current and legacy Yunya facade entrypoints.
- In direct mode, resolve and call the required category, creator, product, video, or shop tool by its semantic business name.
- In Yunya facade mode, when a required business tool is not visible at the host's top level, make at most one host-level discovery attempt and prefer the product-specific `yunya_search_kolsprite_tools`. Query the smallest set of tools needed for the lookup; use the exact internal tool names and complete input schemas returned, then invoke them through `call_read_tool`.
- If the product-specific entrypoint is unavailable but the legacy generic `yunya__search_tools` is discoverable, use it with provider `kolsprite`, operation `read`, and the same query. Do not prefer the generic entrypoint when the product-specific one is available.
- Do not guess a facade namespace, internal tool name, wrapper, category value, or arguments. Reuse discovered names and schemas throughout the lookup.
- A host-level miss for a business tool does not prove that it is absent from the internal catalogue. Only report a missing dependency after direct exposure and the available current or legacy facade lookup fail. If neither facade entrypoint can be discovered, report a connector-discovery failure and do not switch to an unrelated data source as if it were equivalent.
- A standalone KOLSprite MCP remains compatible only when it exposes the same required semantic tool names, input schemas, and response shapes.
- If both connections are enabled, use one connection for the entire lookup, prefer Yunya, and never duplicate a paid call across both services.
- If a required tool is absent or schema-incompatible, report that dependency gap and narrow or stop the lookup instead of guessing a substitute.

## Tool routing

- Creator-category value resolution: call `creator_category_list` before `creator_search` when the user requests a creator-content category and no verified accepted value is already available in the current run.
- Product-category ID resolution: call `product_category_list` before a category-filtered creator, product, video, or shop search when no verified accepted ID is already available in the current run.
- Creator identity, audience scale, engagement, content category, selling activity, contactability, or creator shortlist: call `creator_search`.
- Product identity, price, rating, reviews, listing date, sales, growth, creator count, or video count: call `product_search`.
- Shoppable video identity, creator, product, views, engagement, sales, recency, or duration: call `video_search`.
- Shop identity, type, category, rating, products, sales, creators, or videos: call `shop_search`.

Use multiple tools only when the user's direct lookup genuinely needs joined records. Reuse returned IDs when a downstream tool accepts them. Examples include `shop_search` followed by `product_search` with `shop_id`, or `product_search` followed by `video_search` with `product_id`.

Do not claim that `creator_search` identifies the exact creators who promoted a specific product: the public creator tool currently supports category and performance filtering, not a product-ID relationship query.

## Category resolution

- Treat category-list tools as parameter resolvers, not user-facing search results or required preflight calls. Skip them when no category filter is needed or a valid current-run value has already been returned.
- Match the user's Chinese or English creator-category wording against `creator_category_list`; pass the returned `value` to `creator_search.category_list`.
- Traverse the recursive `product_category_list` tree and match `categoryCn` or `categoryEn`; pass the returned full `category` value to `product_search.cat_ids`, `shop_search.category`, `video_search.product_category_list`, or `creator_search.product_category_list` as applicable.
- Interpret content niche or account positioning as a creator category, and selling, promoted-product, or collaboration direction as a product category. Do not set both category filters merely to hedge an ambiguous phrase such as “beauty creator”; use the request context, state a material assumption, or ask once only when the choice would materially change the result.
- The current search schemas accept an array but support only one category value. Choose the narrowest unambiguous match that preserves the user's intent. If two plausible mappings would materially change the result, ask once; otherwise use the broader valid parent and disclose it.
- Never pass a display label where an accepted value/ID is required, invent an ID, or freeze the live catalogue in Skill text. Reuse one successful mapping across the current run. If the resolver is unavailable or no safe match exists, omit the category filter, use a clearly labelled keyword-bounded query when useful, and disclose the limitation.
- Use the semantic tool names above. The MCP host may add a client- or server-specific namespace to the callable name; do not hardcode one agent's prefix.

## Query rules

1. Infer explicit filters such as market, keyword, category, price, followers, engagement, sales, growth, date, sort, and page size.
2. Use tool defaults for optional inputs when the choice does not materially change the answer. State material assumptions.
3. Ask only for information that is both required and not safely inferable.
4. Translate a requested result count into the smallest sufficient page plan. When the user asks for “all,” use the maximum supported page size and continue until there is no next page, the requested scope is exhausted, the service limit is reached, or an error stops collection.
5. Deduplicate paginated records by their stable object ID. Report requested count, page range, raw rows, deduplicated rows, and stop reason.
6. Apply the user's sort. If the live schema does not confirm a server-side sort value, sort locally only within the disclosed collected scope.
7. Before encoding a percentage growth filter, inspect the live schema or a verified official example. Never guess whether 50% is represented as `50` or `0.5`; if still unresolved, omit that filter and explain the limitation.
8. If an initial query is empty, relax one nonessential filter or try one close synonym when that still answers the user's intent. Report the relaxation rather than silently changing scope.
9. Stop after the requested lookup or bounded comparison is answered. Route decision-oriented follow-ups to `tiktok-shop-growth-research`.

## Point-aware execution

- Point use follows the actual executed tool under the current account rules; selecting this Skill is not itself a charge record.
- Use the smallest call/page plan that answers the request, reuse returned records, and do not repeat an identical paid call without a disclosed reason.
- Do not hardcode or estimate point prices. Report a deduction or remaining balance only when the current MCP response or host client exposes it.
- Stop on insufficient points and label completed pages/rows plus remaining work. Ask before adding discretionary tools or pages beyond the user's requested scope when that expansion materially increases point use.

## Errors and incomplete collection

- Stop the affected chain on authentication failure, unavailable tools, insufficient points/entitlement, rate-limit errors, or repeated server failure.
- Never retry a point, entitlement, rate-limit, or authentication error by changing credentials, evading limits, or shrinking requests to conceal the interruption.
- Label an interrupted collection **incomplete** and state completed pages/rows, remaining requested work, and which conclusions apply only to the collected sample.
- Never call the first page or a rate-limited collection “all results.”
- When a current server error, schema mismatch, empty category result, or suspiciously repeated stable-ID page occurs, consult the dated [known-issues ledger](../tiktok-shop-growth-research/references/known-issues.md). Treat it as a retest guide, not proof that a historical issue is still active.

## Evidence and response rules

- Base TikTok facts only on current MCP output. Never fabricate missing records or metrics.
- Label the source, market, filters, sort, period basis, page, and returned sample size when they affect interpretation.
- Preserve the field's actual time window. Do not relabel total or unspecified sales as 7-day or 30-day sales.
- Distinguish MCP fields from client calculations. Show a formula or plain-language method for any calculated rate, rank, or concentration.
- Treat keyword matches as candidates until product/category relevance is checked.
- Treat an empty result as “no records returned under these conditions,” not proof that the object or market does not exist.
- Use a returned object link when useful. Do not invent TikTok or KOLSprite URLs.
- Lead with the result or shortlist; keep secondary dimensions out unless they change the user's decision.
- For analytical requests, end with a prioritized action, the evidence supporting it, the metric to observe, and a review or stop condition. Do not append an action plan to a simple lookup when the user did not ask for one.
- For a reusable analytical run or partner-facing example, apply the shared [run evidence display](../tiktok-shop-growth-research/references/evidence-display.md) and do not describe query execution as a measured customer outcome.
