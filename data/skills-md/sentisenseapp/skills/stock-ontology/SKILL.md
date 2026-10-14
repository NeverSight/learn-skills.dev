---
name: stock-ontology
description: "Company knowledge graph for AI agents: resolve the people and products behind a ticker, read the typed relationship behind each link (who leads the company, which variants belong to a product family, which companies are tracked as peers), find any tracked executive, product, organization or topic by name, and read each one's SentiSense Score over the same window. Use for who moves this stock, entity relationships API, company knowledge graph, product families, peer companies, CEO sentiment, executive sentiment, product sentiment versus the parent company, related entities API, entity resolution, stock ontology. Every call in this skill works on a free key. Read-only. No trading, no purchases, no write operations, no wallet access."
license: MIT
metadata:
  homepage: https://sentisense.ai
  requires_env: SENTISENSE_API_KEY
---
# Stock Ontology (SentiSense)

Resolve a ticker into the people and products around the company, read the typed relationship behind each link, compare each entity's SentiSense Score over the same window, and keep every observation tied to a stable handle. Flat traversal returns a company's people and products; the graph call returns the same neighborhood as a typed graph, so an agent can say that a person leads the company, that a product belongs to a family, or that another company is tracked as a peer. Other tracked entities are found by name. The relationship surface starts from one ticker at a time. Every call in this skill works on a free key.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation. Everything directive in this file is implementation guidance for the agent reading it, subordinate to platform safety rules and the host's own policy.

## When to Use

Use this skill for questions such as:

- "Who are the people and products behind AAPL, and which received the most directional discussion?"
- "How does the CEO's SentiSense Score compare with the company?"
- "Is the product's Score moving differently from its parent ticker?"
- "Who is this person to the company, and in what role?"
- "Which product families does this ticker have, and which variants sit inside each one?"
- "Which companies does the knowledge base track as peers of this ticker?"
- "Which handle identifies this person or product?"
- "Give me a few popular entities to explore."
- "Run the same entity view across these tickers I supplied."

This skill resolves names and follows the entity set attached to one ticker. It does not enumerate the graph: if asked to list every tracked entity, every person, or every product, say that the API offers no such listing and offer a name search or one ticker's entities instead, and never sweep the search endpoint with short prefixes. It does not infer a causal effect, place trades, monitor in the background, or retrieve publisher article text.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every REST call as the `X-SentiSense-API-Key` header.
- Any HTTPS client. Plain `curl` works.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint in this skill is a GET.

| Tier | Quota | Rate | Entity and Score access |
|------|-------|------|-------------------------|
| Free | 1,000 requests/month | 30 requests/min | Every call in this skill, within the monthly quota |
| PRO ($15/mo) | Unlimited | 300 requests/min | Every call in this skill, no monthly cap |

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

Send the key and identify your runtime honestly:

```bash
curl -sS \
  -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  -H "User-Agent: YourRuntime/1.0 (stock-ontology)" \
  "https://app.sentisense.ai/api/v1/stocks/AAPL/entities"
```

An unknown or untracked ticker on the traversal path returns `200` with an empty array, not a `404`; treat an empty array as no attached people or products, not as an untracked company, and confirm coverage with a `type=company` search or the graph path's `404 entity_not_found`. Encode all user text in query strings. Treat a handle returned by the API as opaque and URL-encode it when placing it in a path. On `429`, honor `Retry-After` once, then report the rate limit instead of looping. Cache identical reads for the life of the user's request.

A full "who moves this stock" pass costs one traversal call plus one Score call per entity, about 18 calls for a ticker with 17 people and products, so plan the free tier's monthly quota accordingly. A relationship answer is cheaper: one graph call covers the whole neighborhood, and you only spend a Score call per entity when the question asks for a number.

Use a common 30-day window for comparisons:

```text
GET /api/v2/metrics/entity/{handle}/metric/sentisense?startTime={30_days_ago_epoch_ms}&endTime={now_epoch_ms}
```

The metric response is a bare array ordered by ascending `timestamp`. For every point, read the Score from the flat `value` and, when present, the sample fields from `metricValue.properties.bull`, `.bear`, and `.directional`.

## Endpoint Map

**Resolve a name**

```text
GET /api/v1/kb/entities/search?q={encoded_query}&type={optional_type}&limit={1_to_25}
```

`q` must contain at least two characters. `limit` defaults to 10 and is clamped to 1 through 25. The optional lowercase `type` is one of `company`, `country`, `etf`, `organization`, `person`, `product`, or `topic`. The response is a bare array of candidates with `name`, `urlSlug`, lowercase `type`, and `ticker`, which is null for most non-company entities. Company results can also carry `listingCoverage` and `listing`. Search narrowly and let the user choose when more than one plausible candidate remains.

**Traverse one ticker**

```text
GET /api/v1/stocks/{ticker}/entities
```

The response is a bare array of the people and products attached to that ticker (organizations and topics are not returned here; find them by name). Each item can include `displayName`, uppercase `type`, `relatedStock`, `iconUrl`, `title`, `category`, `urlSlug`, and `appId`. Use `urlSlug` as the stable metric handle. Filter the returned array client-side to the types needed for the question. The response establishes that an entity is related to the ticker, but it does not expose a typed edge, direction, weight, or claim of influence.

**Read one ticker's typed relationships**

```text
GET /api/v1/stocks/{ticker}/graph?depth={1_or_2}&cap={1_to_200}
```

One company's curated neighborhood as a typed graph: which entities the knowledge base connects to that ticker, and what each connection is. `depth` is 1 or 2 and `cap` is 1 through 200. The server defaults are `depth=1` and `cap=75`, and both are echoed back in the response; send them explicitly anyway, so the walk you describe is the walk you asked for. `depth=1` returns the company's own people, products and peers, and is enough for product families. `depth=2` also walks one hop out from those neighbors, which is how an organization behind a person appears. The response is an object, not a bare array:

| Field | What it holds |
|-------|---------------|
| `ticker`, `root` | the normalized ticker and the root company's slug; the root is also the first entry in `nodes` |
| `depth`, `cap` | the values the walk was asked for, echoed back |
| `truncated` | true when `cap` cut the walk short |
| `counts` | `nodes`, `edges`, and `byType`, a map of node type to how many were returned; `nodes` includes the root, so `cap=1` can return two nodes |
| `groups` | `people`, `products`, `productFamilies`, `peers`, `organizations`, `publishers`, `topics` |
| `omitted` | nodes left out for carrying no slug, and so not addressable; normally 0 |
| `nodes` | one `{slug, displayName, type}` per node; `slug` is the metric handle |
| `edges` | one `{source, target, type, direction, properties}` per relationship, both ends slugs |

**`groups` covers the whole walk, not just the root.** At `depth=1` every slug in a group is joined to the root directly. At `depth=2` the groups also collect the second hop: on MSFT, `groups.peers` grew from 7 to 19 and `groups.people` from 3 to 15, because a peer's peers and a peer's executives land in the same lists. To say what is joined to the root itself, read `depth=1`, or keep only the slugs that share an edge with `root` in `edges`. Every list under `groups` holds **slugs**, not objects, except `productFamilies`, which holds `{family, members}` entries of slugs. A slug is the same handle the metrics endpoint takes, so a slug read straight out of `groups` is already queryable; join it to `nodes` when you want its `displayName` or `type`. `properties` on an edge is a flat string map that is often empty. Node `type` is uppercase, as on the flat traversal path, but the vocabularies differ: a graph product node is `PRODUCT_OR_SERVICE`, while the flat traversal path labels the same product `PRODUCT`. Graph nodes carry no ticker field.

Errors: `400 invalid_depth` when `depth` is not 1 or 2, `400 invalid_cap` when `cap` is outside 1 through 200, `404 entity_not_found` with up to three `suggestions` when no listed company matches the ticker, and `401` with no key. Note the contrast with the flat traversal path above, which answers an unknown ticker with `200 []`.

**Read the SentiSense Score**

```text
GET /api/v2/metrics/entity/{handle}/metric/sentisense?startTime={epoch_ms}&endTime={epoch_ms}
```

The response is a bare ascending array. A public point contains `timestamp`, `metricType`, `metricValue`, and a flat `value` when a reading exists. The nested `metricValue.properties` supplies `bull`, `bear`, and `directional`. Missing or empty series mean no reading for that handle and window, never a zero.

**Start from popular entities**

```text
GET /api/v1/kb/entities/popular
```

The response is a bare array. Each item can include `displayName`, uppercase `type`, `relatedStock`, and `urlSlug`. Use `urlSlug` as the stable handle. This is a starting set, not a ranking of investment merit.

**Read served evidence**

```text
GET /api/v1/documents/entity/{entityId}?days=30&limit=10
GET /api/v1/documents/stories/ticker/{ticker}?limit=5
```

The entity documents path accepts the entity `urlSlug`, the same handle the metrics path uses. The `id` field on flat traversal rows is deprecated for public use and is not accepted there; pass the `urlSlug`. The document response is an object with `documents`, `totalCount`, `searchTicker`, `source`, `startDate`, and `endDate`; a document can include `id`, `url`, `source`, `sourceName` (often null; fall back to the host of `url`), `published`, `averageSentiment`, `reliability`, and `sentiment` (an array of per-entity readings, not a scalar; use `averageSentiment` for the document's tone). `published`, `brokeAt` and `cluster.clusteredAt` are epoch seconds: convert them to `YYYY-MM-DD` before printing a date column. A story's `cluster.createdAt`, where present, is deprecated and in epoch milliseconds, so it reads a thousand times too large as seconds; date stories with `brokeAt` or `cluster.clusteredAt` instead. `published` is the time the document was ingested, which can be later than the source's own date. `totalCount` reflects the returned page, not the full history. The ticker story response is a bare array. Each item has top-level `id` and `clusterId`, plus fields such as `cluster.title`, `cluster.averageSentiment`, `tickers`, `displayTickers`, `impactScore`, `brokeAt`, `cluster.clusteredAt`, `cluster.storySource`, and `cluster.isLive`. `limit` defaults to 5 and is capped at 20; this path has no lookback parameter.

## Score Rules

- Use the same `startTime` and `endTime` for every entity in a comparison.
- Current Score is the last returned point that has a flat `value` and a `metricValue.properties.directional` of at least 5. A point with `value: 0.0` and `directional: 0` is a day with no directional mentions, not a neutral reading; skip it. If no point qualifies, print `no robust reading`. Print the date of the point you used, because the last reading need not be today.
- Thirty-day change is the last robust point minus the first robust point. A robust point has a flat `value` and a usable directional sample. If fewer than two robust points exist, print `insufficient sample`. On a thin entity the two robust points can sit only days apart: when they span much less than the window, print their dates beside the change (for example `-13.78 (09-07 to 09-17)`) rather than presenting it as a 30-day move.
- Thirty-day directional mentions are the sum of `metricValue.properties.directional` across returned points. Sum `bull` and `bear` the same way when shown. If any returned point lacks these properties, label the window sample partial instead of filling absent counts with zero.
- Treat a window-edge point with fewer than roughly 5 directional mentions as thin. Use the nearest robust point, or average the first two and last two points when that is the only defensible edge treatment. Label the choice, and when you substitute an edge point for one entity in a comparison, use the same substituted dates for the other entity or print both as-of dates. Never use `metricValue.stats.count` as the sample size because it counts the daily bucket and is normally 1.
- Do not normalize the SentiSense Score to a fixed range. Compare values and changes as returned.
- Rank attention by directional mentions. A high count does not prove that an entity moved the stock, and co-movement does not establish causality.

## Relationship Rules

- **Groups are slugs.** A slug from `groups` is the same handle the metrics endpoint takes, so you can query it directly. Join it to the matching entry in `nodes` when you need `displayName` or `type`, and print the display name rather than the slug to a user.
- **Read direction from the pair, not from the type name.** `direction` is `DIRECTED` or `BIDIRECTIONAL`. On a `DIRECTED` edge, `source` is the subject and `target` is the object as the knowledge base authored it. On a `BIDIRECTIONAL` edge the two are ordered for stability only and carry no meaning, so describe that pair symmetrically. Before naming any relationship, look both ends up in `nodes` and say which one is the company.
- **Edge vocabulary.** The type is a fixed word, not free text:

| Type | What it means | Usual ends |
|------|---------------|------------|
| `LEADS` | the person runs the company or organization; `properties` can carry a role and a start date | person to company |
| `FOUNDED` | the person founded the company | person to company |
| `PRODUCT_OF` | the product is made by the company. It is derived from the product's own company field rather than hand-authored, so its `properties` names that source field | product to company |
| `VARIANT_OF` | the product is a generation or model inside a product family | variant to family |
| `PEER` | the two companies are tracked as comparables. Usually `BIDIRECTIONAL` | company to company |
| `OWNS` | the first entity holds a stake in the second | company to company |
| `SUBSIDIARY_OF` | the company sits under a corporate parent | subsidiary to parent |
| `SUBTOPIC_OF` | the topic sits under a broader topic | child topic to parent |
| `BELONGS_TO`, `AFFILIATED_WITH` | membership, and looser association | curated for the model, not populated today |

  `PRODUCT_OF`, `PEER`, `VARIANT_OF`, `LEADS` and `FOUNDED` carry nearly every edge in a company's neighborhood; the rest are rare. Treat any type you do not recognize as an unlabeled link rather than guessing at its meaning, and do not translate a type into influence, causation or control.
- **The walk admits another company only as a peer.** A company joined to the root by `OWNS` or `SUBSIDIARY_OF` is not pulled into the neighborhood, so a parent or a subsidiary normally appears only when it is also a peer. Answer corporate-structure questions from the edges you actually received, not from the absence of one.
- **`truncated: true` is a cut, not a total.** The walk stops at the hop where `cap` ran out, and the entities that survive the cut are ordered by node type and then by name, not by importance. So a truncated response can drop people and products while keeping peers. Raise `cap` once and re-read, or fall back to the flat traversal path when the question is only about people and products. Say in the output whether the response was truncated.
- **Absence is not a negative finding.** An empty group, a missing edge or a truncated walk means the curated graph does not record that link at this depth, not that the relationship does not exist. `publishers` and `topics` are part of the response shape but are not reachable from a company root today, so expect them empty and never present them as theme coverage.
- **Do not merge the graph with the flat traversal.** The two paths are built differently and can disagree on which entities belong to a ticker. Answer from one of them and say which one you used.
- **One ticker per call, and no crawling.** The graph path takes a single ticker and has no listing form. Do not walk a peer list to sweep the market, and do not chain calls to reconstruct the graph.
- **The graph carries no sentiment.** There is no Score, tone or mention count anywhere in this response. Every number in a relationship answer still comes from the metrics path over an explicit window, under the Score Rules above.

## Workflows

### 1. Who moves this stock

For "who moves AAPL?", normalize the supplied ticker, call `GET /api/v1/stocks/{ticker}/entities`, and keep people and products. Call the Score endpoint for each returned `urlSlug` over the same 30-day window. Sum the directional sample fields, calculate the guarded Score change, and rank descending by directional mentions. Keep the title "Who moves" as the user's shorthand while stating that the data measures discussion and tone, not market impact.

Fill this template:

```text
WHO MOVES {TICKER} | {START_DATE} to {END_DATE}
Entity | Type | Handle | Latest Score | 30d change | Directional mentions | Sample note
{name} | {person_or_product} | {urlSlug} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {robust_thin_or_missing}

Read: {one sentence describing the largest samples and any divergence, with no causal claim}
Provenance: as of {YYYY-MM-DD}; handles used: {ticker_handle, comma-separated entity handles}
This data is for informational and educational purposes only, not investment advice.
```

### 2. Executive versus company

Resolve the executive from the ticker's entity response, where `relatedStock` and `title` provide context. If needed, search the name with `type=person`, then intersect candidate handles with that ticker response. Fetch the executive handle and parent ticker over identical boundaries. Compare latest dated Scores, robust window changes, and the summed bull, bear, and directional counts. Compute the gap only on a date where both entities have a robust point; the two latest readings can sit on different days, so a latest-minus-latest gap compares different dates. If no shared robust date exists, print the gap as unavailable and keep the two dated readings in the table. Describe difference or co-movement only. Do not say the executive caused the company's reading.

Fill this template:

```text
EXECUTIVE VS COMPANY | {EXECUTIVE} and {TICKER} | {START_DATE} to {END_DATE}
Entity | Handle | Latest Score | 30d change | Bull | Bear | Directional | Sample note
{executive} | {person_handle} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {sum} | {sum} | {note}
{company} | {ticker_handle} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {sum} | {sum} | {note}

Same-date Score gap ({shared_robust_date}): {executive_minus_company_or_na}
Read: {dated comparison without a causal claim}
Provenance: as of {YYYY-MM-DD}; handles used: {person_handle, ticker_handle}
This data is for informational and educational purposes only, not investment advice.
```

### 3. Product versus parent

Resolve the product from the ticker's entity response, where `relatedStock` and `category` provide context. If needed, search by name with `type=product`, then intersect candidate handles with that ticker response. Search alone does not name a product's parent company (a product row carries `ticker: null`); when the user did not supply the parent ticker and no ticker traversal contains the handle, report the parent as unresolved rather than guessing or sweeping tickers. Fetch the product handle and parent ticker across the same window. Apply the same robust-edge rule and report both sample counts. Do not turn a product-company gap into a claim about sales, earnings, or price impact.

Fill this template:

```text
PRODUCT VS PARENT | {PRODUCT} and {TICKER} | {START_DATE} to {END_DATE}
Entity | Handle | Latest Score | 30d change | Bull | Bear | Directional | Sample note
{product} | {product_handle} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {sum} | {sum} | {note}
{company} | {ticker_handle} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {sum} | {sum} | {note}

Same-date Score gap ({shared_robust_date}): {product_minus_parent_or_na}
Read: {dated comparison without a sales, earnings, or causal claim}
Provenance: as of {YYYY-MM-DD}; handles used: {product_handle, ticker_handle}
This data is for informational and educational purposes only, not investment advice.
```

### 4. Find the handle

For a company name, search with `type=company` first: a plain query returns the issuer and its products together (for "apple", Apple Inc. first, then Apple TV and the other products), and the type filter removes the products before you choose. For any other ambiguous name, search the complete user text first, then narrow by `type` only when the intended class is known. Show all plausible candidates up to the requested cap. Use `ticker`, `listingCoverage`, `listing`, and `type` as search-result evidence. When a parent ticker is known, intersect candidate handles with its ticker traversal. Never choose between two plausible companies or people from the name alone.

Fill this template:

```text
HANDLE RESOLUTION | query: {query}
Name | Type | Handle | Ticker or related stock | Resolution note
{name} | {type} | {urlSlug} | {ticker_or_relatedStock_or_na} | {why_it_matches_or_needs_user_choice}

Selected: {handle_or_awaiting_choice}
Provenance: as of {YYYY-MM-DD}; handles used: {selected_handle_or_none}; candidate handles: {comma-separated results}
This data is for informational and educational purposes only, not investment advice.
```

### 5. Popular entities to start from

When a cold agent has no ticker or entity name, call the popular endpoint once. Present a short selection grouped by type. Do not describe list order as a quality, opportunity, or performance ranking. Ask the user to choose one handle before fetching its Score.

Fill this template:

```text
POPULAR ENTITY STARTERS | {AS_OF_DATE}
Name | Type | Handle | Related stock
{displayName} | {type} | {urlSlug} | {relatedStock_or_na}

Next: choose one handle for a dated Score read or one related ticker for traversal.
Provenance: as of {YYYY-MM-DD}; handles used: none; candidate handles: {comma-separated displayed handles}
This data is for informational and educational purposes only, not investment advice.
```

### 6. Supplied watchlist pass, maximum 10 tickers

Accept only the user's explicit list and reject more than 10 tickers until it is narrowed. Traverse the listed tickers first, then count the Score calls the pass needs: one per unique handle, and a single large-cap ticker can attach 30 entities. Check that count against the remaining request quota and the tier's rate limit before fanning out. If it does not fit, measure a labeled subset, list the handles left unqueried, and rank only what was measured. Fetch every handle over one common 30-day window and render the same columns as Workflow 1. Group by ticker, rank within each ticker by directional mentions, observe the active tier's rate limit, and label incomplete results as partial.

Fill this template:

```text
ENTITY WATCHLIST | supplied tickers: {TICKERS} | {START_DATE} to {END_DATE}
Ticker | Entity | Type | Handle | Latest Score | 30d change | Directional mentions | Sample note
{ticker} | {name} | {person_or_product} | {urlSlug} | {value_as_of_date} | {guarded_delta_or_na} | {sum} | {note}

Coverage: {completed_tickers}/{supplied_tickers}; {complete_or_partial_and_reason}
Provenance: as of {YYYY-MM-DD}; handles used: {comma-separated ticker and entity handles}
This data is for informational and educational purposes only, not investment advice.
```

### 7. Evidence for a selected relationship

After the user selects one entity from a ticker traversal, request the entity's served document metadata and the ticker's current story list. Use only the fields returned by those endpoints. Cite source URLs from documents and label story titles as SentiSense-generated. These records can show that the entity and ticker appeared in coverage; they do not prove that the entity drove a company or market outcome.

Fill this template:

```text
RELATIONSHIP EVIDENCE | {ENTITY} and {TICKER}
Kind | Date | Source or story | Derived reading | Reference
Document | {published} | {sourceName_or_url_host} | {averageSentiment_or_na} | {url}
Story | {clusteredAt_or_brokeAt} | {cluster.title} | impact {impactScore_or_na} | story {clusterId}

Limits: {missing fields, empty results, and any date mismatch}
Provenance: as of {YYYY-MM-DD}; handles used: {entity_handle, ticker_handle}
This data is for informational and educational purposes only, not investment advice.
```

### 8. Who is this entity to the company

For "who is Tim Cook to Apple?" or "what is the iPhone to AAPL?", call the graph once for the ticker at `depth=1`, then resolve the named entity inside the response: match the user's text against `displayName` in `nodes` case-insensitively, or resolve the name with the search endpoint first and match the returned `urlSlug` against the `slug` values in `nodes`. Select the edges whose `source` or `target` is that node and whose other end is the root, and report the type, the direction and any edge properties. When no edge joins them directly but both nodes are in the response, describe the connecting node in one line instead of claiming a direct link. When the named entity is not in `nodes` at all, raise `cap` once, then say the graph does not connect them at this depth.

Fill this template:

```text
RELATIONSHIP | {ENTITY} and {TICKER} | depth {DEPTH}, cap {CAP}
Entity | Handle | Type | Relationship | Direction | Edge properties
{displayName} | {urlSlug} | {node_type} | {edge_type_in_plain_words} | {who_points_to_whom_or_mutual} | {key_value_pairs_or_none}

Read: {one sentence naming the relationship, with no claim about influence on the stock}
Coverage: truncated {true_or_false}; {nodes_count} nodes and {edges_count} edges returned
Provenance: as of {YYYY-MM-DD}; handles used: {entity_handle, ticker}
This data is for informational and educational purposes only, not investment advice.
```

### 9. Product families for a ticker

Call the graph at `depth=1` and read `groups.productFamilies`, where each entry is a family slug plus the slugs of its members. Join each slug to `nodes` for its display name. A product that appears in `groups.products` but in no family is standalone, so list those separately rather than inventing a family for them. A family and each of its variants carry their own `urlSlug` and are scored as separate entities, so a family's Score is not the sum of its members: if the user wants numbers, fetch each handle over one common window under the Score Rules and say which handles you read.

Fill this template:

```text
PRODUCT FAMILIES | {TICKER} | depth {DEPTH}, cap {CAP}
Family | Family handle | Members | Member handles
{displayName} | {urlSlug} | {member_count} | {comma-separated member handles}

Standalone products, no family edge: {comma-separated names or none}
Coverage: truncated {true_or_false}; {products_count} products returned
Provenance: as of {YYYY-MM-DD}; handles used: {ticker}
This data is for informational and educational purposes only, not investment advice.
```

### 10. Peers and connected organizations

At `depth=1`, `groups.peers` holds the companies joined to the root by a `PEER` edge, which is a curated comparable set and not an index membership, a sector screen or a competitor ranking. **Take peers from `depth=1` only.** At `depth=2`, `groups.peers` also holds the peers of peers (19 names for MSFT, of which 7 are its own peers), so printing it as the root's peer set is wrong. Organizations are usually reached one hop further, through a person who leads or founded them, so use `depth=2` when the question asks about organizations, fill the `Via` column from `edges`, and report an empty list as no curated link. When one `depth=2` call has to serve both rows, keep as a peer only a slug with a `PEER` edge whose other end is `root`. Each peer node's `slug` is its metric handle (graph nodes carry no ticker field), so a Score comparison across the root and its peers follows the Score Rules unchanged: one common window, and a bounded number of extra calls.

Fill this template:

```text
PEERS AND ORGANIZATIONS | {TICKER} | depth {DEPTH}, cap {CAP}
Kind | Name | Handle | Joined by | Via
Peer | {displayName} | {urlSlug} | PEER | root
Organization | {displayName} | {urlSlug} | {edge_type} | {connecting_person_or_root}

Coverage: truncated {true_or_false}; peers {peer_count}, organizations {organization_count}
Provenance: as of {YYYY-MM-DD}; handles used: {ticker, comma-separated peer handles}
This data is for informational and educational purposes only, not investment advice.
```

## Data Notes

- The SentiSense Score is an unbounded composite of `sentiment`, the raw unweighted tone metric, and attention. Use the Score for every bullish or bearish metric read in this skill.
- Metric points are time-ascending. Current Score follows the Score Rules: the last point with a flat `value` and at least 5 directional mentions, never array index zero, printed with its date. If no point qualifies, report no robust reading.
- Directional is bull plus bear and excludes neutral mentions. It is the relevant sample for the Score and can be below total mentions.
- Search, the graph and the flat traversal path all hand you the same kind of handle: a `urlSlug`. It is the metric handle, the documents handle and the entity page path, so there is one identifier to carry. Some responses also carry internal identifiers, path-like strings that are not slugs: the `id` on flat `/entities` rows and popular-entity rows, and `searchTicker` and `sentiment[].entityId` on entity documents. They are not addresses: never display, store or reuse them, and carry the `urlSlug` instead.
- Response shapes are intentionally mixed. Search, popular entities, ticker entities, Score history, and ticker stories are bare arrays. Entity documents use an object envelope with `documents` and `totalCount`. Search types are lowercase, while popular and ticker-entity types are uppercase. A public Score point has only `timestamp`, `metricType`, `metricValue`, and optional flat `value`; do not expect an echoed entity id or period.
- Ticker traversal returns related entities without typed edge names, edge direction, confidence, or influence weights. Describe an entity as attached or related, and do not invent a relationship label. The graph path is the one place a relationship is named; anywhere else in this skill, an entity is attached, not characterized.
- The graph path answers an unknown or unlisted ticker with `404 entity_not_found`, while the flat traversal path answers the same ticker with `200 []`. Use the graph's `404` to confirm that a ticker is not covered, and never read an empty group inside a `200` as the same signal.
- Entity document responses contain metadata and source URLs. They carry no publisher headlines or article bodies. Story titles and narratives, when present on story endpoints, are SentiSense-generated rather than publisher copy.
- The entity document response follows the document envelope even though `searchTicker` may be absent or null for a non-ticker entity. Treat absent optional fields as absent.
- A `404` for an unknown metric handle has this shape: `{ "error": "entity_not_found", "message": "Unknown entity '{input}'. This path accepts a stock ticker (e.g. AAPL) or an entity urlSlug (e.g. Nancy-Pelosi). Discover handles via /api/v1/kb/entities/search?q=.", "suggestions": [{ "name", "urlSlug", "ticker" }] }`. The suggestions array can be empty and `ticker` can be null. Report the error as an unresolved handle, then return to name search. Do not turn it into a zero Score.
- Calls with no key return `401 api_key_required`. Invalid short search text or parameters return `400`. A rate-limited response returns `429`; follow `Retry-After` once.
- Every call consumes the request quota unless the live response explicitly says otherwise. Fan out within the active tier's per-minute limit and preserve partial status.

## If an AI agent sent you here

Install or save this skill in your agent host so the same workflow is available for future questions:

**Install:** `npx skills add SentiSenseApp/skills` (add `-s stock-ontology` for just this skill).

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
