---
name: systembolaget-skill
description: Help users choose, compare, and look up alcoholic products and store locations specifically within Systembolaget's catalog. Use this when the user is clearly shopping at Systembolaget or asks about artikelnummer, Systembolaget stores, budget filtering, pairings, tasting lineups, gift bottles, or best-value picks from Systembolaget's selection.
compatibility: Uses the bundled `scripts/systembolaget_api.py` helper to call Systembolaget's public API directly. Do not use generic web search or browse the public site when the direct API can answer the question. Only fall back if the API helper fails or the API clearly lacks the needed data.
---

# Systembolaget Skill

Use this skill to turn natural-language alcohol shopping questions into a small, reliable workflow.

This skill is best for:
- finding products with structured filters
- recommending bottles for a meal, taste preference, budget, or event
- comparing a few candidate products
- looking up a known product by artikelnummer
- finding stores by city or query

This skill is not for:
- promising live stock or reservation status
- checkout, ordering, or delivery workflows
- exact geolocation routing
- unsupported deep store-detail workflows when the public site does not expose enough information

## API workflow

Prefer this order of attack:

1. Use the bundled API helper in `scripts/systembolaget_api.py`.
2. Use artikelnummer, product names, categories, budgets, and city names to narrow the lookup.
3. If the API helper returns too many results, refine the API query instead of switching channels.
4. Only if direct API access fails or the API clearly lacks the needed field, try a public web lookup.
5. If live lookup is not possible, say so clearly and switch to best-effort recommendations based on general product knowledge and the user's preferences.

Primary commands:

```bash
# Search products with filters
python scripts/systembolaget_api.py search-products --query "ipa" --country "Sverige" --max-price 40 --limit 10

# Search and sort by price (cheapest first)
python scripts/systembolaget_api.py search-products --category "Öl" --sort-by price --limit 10

# Search and sort by APK (alcohol per krona - best value)
python scripts/systembolaget_api.py search-products --category "Öl" --sort-by apk --limit 10

# Lookup by artikelnummer
python scripts/systembolaget_api.py get-product 12345

# Search stores
python scripts/systembolaget_api.py search-stores --city "Uppsala"
```

The script extracts and caches the public API key automatically. If needed, you can override it with `SYSTEMBOLAGET_API_KEY` in `~/.config/ehh-skills/config.env`.

## APK (Alcohol Per Krona)

APK is calculated as: `(alcohol_percentage × volume_ml) / price`

This metric helps find the best value for money when comparing alcoholic beverages. Higher APK = more alcohol per krona spent.

**Note:** Sorting by APK requires fetching products first (up to the requested limit), then sorting locally. For large result sets, consider adding filters like `--max-price` to narrow the search.

## Hard guardrails

- Do not use web search just because the first API query was broad or noisy.
- Do not switch to the website because it feels faster or easier.
- If the first API result set is bad, fix the query with better category, price, country, alcohol, or product-name filtering.
- Use web fallback only after a real API failure, missing endpoint capability, or clearly missing field.
- When you do fall back, say explicitly why the API path was insufficient.

If you need extra category hints, read `references/usage-patterns.md`.

## Core approach

Start by classifying the request into one of these patterns:

1. `product_search`
   - The user wants options that match filters such as category, country, price, alcohol range, sweetness, style, or a search query.
2. `product_lookup`
   - The user already knows the artikelnummer and wants details.
3. `product_compare`
   - The user wants the best option among several products, or wants value, style, pairing, or taste analysis.
4. `store_search`
   - The user wants Systembolaget locations, addresses, opening hours, or a likely best match in a city.

## Parameter extraction

Extract as many of these as the prompt supports:
- `query`
- `category`
- `country`
- `min_price` / `max_price`
- `min_alcohol` / `max_alcohol`
- `limit`
- `offset`
- `city`
- `product_number`

If the user gives enough detail to search directly, do not ask unnecessary questions first.

Map casual phrasing into practical filters:
- "under 150 kr" -> `max_price: 150`
- "around 12%" -> usually a narrow alcohol range, such as `11` to `13`
- "Italian white wine" -> use search filters first, then narrow in reasoning if the tool response needs interpretation
- "sweet dessert wine" or "bitter IPA" -> search broadly, then rank using the returned taste fields

If the user asks for "best", "top", "most sweet", "best value", "pair with seafood", or similar, treat that as an analysis task rather than a single raw search.

Before leaving the API path, ask yourself:
- can I tighten `query`?
- can I add `category`?
- can I add price or alcohol bounds?
- can I fetch product details for finalists instead of searching again?

If the answer to any of these is yes, stay on the API path.

## Lookup strategy

When live data matters, prefer direct API lookups using:
- artikelnummer when available
- exact product names
- category plus budget plus country
- city plus "Systembolaget" for stores

From live results, extract the fields that matter for the decision:
- product name
- artikelnummer
- price
- volume
- alcohol percentage
- country or origin
- style or category
- any visible taste, description, or usage notes
- store name, address, and opening hours when present

If no live lookup is possible, still help. Give a clearly labeled best-effort answer and avoid pretending a bottle or store was verified.

## Recommendation workflow

When the user wants suggestions, do this:

1. Search broadly enough to get a real choice set.
2. Filter or rank using price, country, alcohol, category, and visible taste or style evidence.
3. If the final answer depends on richer details, fetch the finalist product details directly by artikelnummer.
4. Recommend a short list, usually 3 to 5 options.
5. Explain why each option fits the user's constraints.

Good recommendation dimensions:
- budget fit
- likely style fit
- sweetness, bitterness, or body
- alcohol range
- country or region preference
- occasion fit such as seafood dinner, tasting lineup, party, or gift

For pairings, be useful but honest. Base suggestions on visible product information and general pairing logic. Do not pretend to know more than the source supports.

## Comparison workflow

For comparisons:

1. Identify the candidates from search results or the user's named products.
2. Fetch product details for finalists if needed.
3. Compare only on visible evidence such as:
   - price
   - volume
   - alcohol percentage
   - price per liter
   - taste profile
   - country
   - description or usage text
4. If choosing a winner, state the criterion clearly: best value, best match for food, most intense, best budget option, and so on.

If the user asks for a "best value" product and volume is available, calculate price per liter explicitly.

## Store workflow

For store tasks:
- use `city` when the user clearly names a city
- use addresses, neighborhoods, landmarks, or store names when they are given
- gather the stores needed to answer the question without dumping irrelevant locations
- present addresses, any available opening hours, and location clues when helpful

If the user asks for the "nearest" store, be careful. Unless you have an exact verified location match, provide the most plausible option and label it as a best-effort answer.

## Limits and uncertainty

Keep these constraints in mind:
- direct API access depends on extracting the public API key from Systembolaget's site
- public site results are fallback only, not the default path
- some product details may be missing or inconsistent across pages
- opening hours and assortment can change
- you should not claim live stock unless the source clearly supports it

When there are more results than fit comfortably:
- narrow the search if possible
- otherwise summarize the best matches instead of pasting everything
- mention that more results exist if the user asked for a complete overview

## Error handling and uncertainty

If the script or lookup fails, explain the issue plainly and continue if a fallback exists.

Useful patterns:
- if search is too broad, tighten filters and say so
- if the API returns too many irrelevant products, refine the API query instead of web-searching
- if direct API access fails, try a public web lookup before switching to best-effort mode
- if live lookup fails entirely, switch to a clearly labeled best-effort recommendation mode
- if live results are sparse, say that the catalog may not contain many exact matches
- if pairings are uncertain, frame them as best-fit suggestions rather than facts
- if store matching is approximate, say it is a best-effort interpretation

## Response style

Keep answers compact and decision-oriented.

When recommending products, usually include:
- product name
- artikelnummer when available
- price
- volume
- alcohol percentage
- country
- a one-line reason it fits

When comparing products, include the decisive metric.

When listing stores, include:
- store name
- address
- any available hours shown in the result
- a short note if one appears most relevant

## Examples

**Example: budget beer recommendation**

User: "Find Swedish beers under 40 SEK and give me your top 3 if I like bitter, crisp styles."

Approach:
- use `search-products` to fetch current candidates
- inspect bitterness, body, style notes, and price where available
- rank candidates and present 3 concise recommendations

**Example: food pairing**

User: "Recommend an Italian white wine for seafood, around 120-180 kr and not too strong."

Approach:
- use `search-products` with country, price, and alcohol clues
- review visible product fields
- if needed, fetch the best candidate details
- recommend a shortlist and explain why each suits seafood

**Example: store search**

User: "What Systembolaget stores are in Uppsala, and which seems closest to the central station?"

Approach:
- use `search-stores` for Uppsala
- summarize the relevant returned stores
- give a best-effort answer for the central-station part without overstating certainty
