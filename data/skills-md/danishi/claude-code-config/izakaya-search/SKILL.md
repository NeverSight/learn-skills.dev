---
name: izakaya-search
description: >
  Search and recommend izakaya (Japanese-style pubs) and restaurants
  based on party size, budget, area, and additional preferences.
  Aggregates reviews from gourmet sites (Tabelog, Hot Pepper Gourmet, Gurunavi)
  and Google Maps, calculates composite ratings, and provides
  reservation links and Google Maps directions for quick booking.
---

# Izakaya Search - Japanese Restaurant Recommendation Skill

Interactively find the best izakaya and restaurants by hearing the user's
requirements and searching gourmet sites and Google Maps.

---

## Workflow

### Step 1: Interview the user

Ask the user the following questions using the `AskUserQuestion` tool.
Gather all required information before searching. If any additional context
is provided by the user (e.g., "quiet atmosphere", "private rooms",
"all-you-can-drink"), incorporate it into the search.

#### Required information

| Item | Question example | Notes |
|---|---|---|
| **Area / location** | "Which area or station are you looking for?" | Accept station names, city names, or landmarks |
| **Party size** | "How many people?" | Important for seat/room availability |
| **Budget per person** | "What is your budget per person?" | Accept ranges like "3,000-5,000 yen" |

#### Optional information (ask if not already provided)

| Item | Question example | Notes |
|---|---|---|
| **Date and time** | "When are you planning to go?" | Affects availability and course options |
| **Cuisine preferences** | "Any preferred cuisine type?" | e.g., Japanese, seafood, yakitori, Korean, etc. |
| **Must-have features** | "Any requirements?" | e.g., private rooms, smoking/non-smoking, all-you-can-drink, accessibility |
| **Occasion** | "What is the occasion?" | e.g., casual drinks, welcome/farewell party, date, business dinner |

### Step 2: Search for restaurants

Use `WebSearch` to search across multiple gourmet platforms. Execute
multiple searches in parallel when possible for efficiency.

#### Search queries to execute

Build search queries combining the user's requirements. Always search
at least these sources:

1. **Tabelog (食べログ)**
   ```
   "食べログ {area} 居酒屋 {cuisine} {features}"
   ```

2. **Hot Pepper Gourmet (ホットペッパーグルメ)**
   ```
   "ホットペッパー {area} 居酒屋 {party_size}名 {budget}"
   ```

3. **Gurunavi (ぐるなび)**
   ```
   "ぐるなび {area} 居酒屋 {features} {cuisine}"
   ```

4. **Google Maps**
   ```
   "Google Maps {area} 居酒屋 {cuisine} 口コミ"
   ```

#### Search strategy

- Run 3-5 parallel `WebSearch` calls with different query variations
- Include budget and party size keywords in queries
- Add optional preferences (private room, all-you-can-drink, etc.)
- Search for specific course/plan information when budget is specified
- If initial results are insufficient, refine queries and search again
- Prefer extracting information from `WebSearch` snippets when possible,
  especially for sites known to block `WebFetch` (see Step 3)

### Step 3: Gather detailed information

Use `WebFetch` to visit the top candidate restaurant pages and collect:

- Restaurant name and address
- Business hours and regular holidays
- Review ratings from each source
- Course menus and pricing
- Seat count and room types (counter, table, private room, tatami)
- Reservation availability
- Direct reservation page URLs
- Notable features (all-you-can-drink plans, smoking policy, etc.)

#### WebFetch resilience strategy

**Batch size control (critical):**
Parallel `WebFetch` calls share a failure boundary — if one call returns
an error (403, 404, timeout), **all sibling calls in the same batch are
cancelled**. To mitigate this:

1. **Limit parallel batches to 2-3 calls maximum** (never 5+)
2. **Group by reliability tier** — put sites that are likely to succeed
   together, and isolate risky sites into their own batch or run them
   sequentially
3. **Prioritize high-value fetches** — fetch the most important pages
   first so that even if later batches fail, you already have usable data

**Site reliability tiers:**

| Tier | Sites | Strategy |
|---|---|---|
| Tier 1 (reliable) | Google Maps, aumo, ヒトサラ, さんたつ, TripAdvisor | Safe to batch together (2-3 per batch) |
| Tier 2 (sometimes blocked) | ぐるなび (`r.gnavi.co.jp`) | Fetch individually or with Tier 1 sites |
| Tier 3 (frequently blocked) | 食べログ (`tabelog.com`), ホットペッパー (`hotpepper.jp`), RETRIP (`rtrp.jp`) | Fetch individually; expect 403 errors |
| Tier 4 (not fetchable) | JS-rendered SPAs (colmo, etc.) | Skip `WebFetch`; rely on `WebSearch` snippets only |

**Fallback strategy when WebFetch fails:**

1. Extract as much information as possible from `WebSearch` result
   snippets (ratings, addresses, phone numbers often appear in snippets)
2. Try alternative URLs for the same restaurant on a different platform
3. Use Google Maps search results, which tend to be the most accessible
4. If a specific restaurant page is critical, try the Google cached
   version via `WebSearch`: `"cache:{url}"` or `"{restaurant_name} site:{domain}"`

### Step 4: Calculate composite review ratings

Compute a weighted composite score from available review sources:

| Source | Weight | Score range | Notes |
|---|---|---|---|
| Google Maps | 45% | 1.0 - 5.0 | Largest review volume; highest weight |
| Tabelog | 35% | 1.0 - 5.0 | Most trusted for food quality in Japan |
| Hot Pepper / Gurunavi | 20% | 1.0 - 5.0 | Useful for atmosphere and service |

**Composite score formula:**

```
composite = (google * 0.45) + (tabelog * 0.35) + (hotpepper_or_gurunavi * 0.20)
```

- If a source is unavailable, redistribute its weight proportionally
  to the remaining sources
- Example: If only Google (4.2) and Tabelog (3.8) are available:
  - Google weight: 0.45 / (0.45 + 0.35) = 0.5625
  - Tabelog weight: 0.35 / (0.45 + 0.35) = 0.4375
  - Composite: (4.2 * 0.5625) + (3.8 * 0.4375) = 4.025
- Display scores rounded to 2 decimal places
- Include the number of reviews from each source when available

#### Google Maps fake review (sakura) detection

Google Maps reviews are susceptible to fake positive reviews (サクラ).
When gathering Google Maps data, **always check for the following red flags**
and apply a penalty to the Google Maps score if detected:

| Red flag | How to detect | Penalty |
|---|---|---|
| Suspiciously high ratio of 5-star reviews | >80% of reviews are 5-star with very few 3-4 star | -0.3 from Google score |
| Generic/short praise comments | Many reviews are only 1-2 sentences like "美味しかった！" with no detail | -0.2 from Google score |
| Reviewer profiles with only 1 review | Multiple reviewers who have only ever reviewed this one restaurant | -0.3 from Google score |
| Review spike pattern | Large number of reviews posted within a short time period | -0.3 from Google score |
| Score gap vs. Tabelog | Google score is ≥1.0 higher than Tabelog score for the same restaurant | -0.2 from Google score |

**Detection process:**

1. When using `WebFetch` on the Google Maps page, scan the visible review
   comments (at least 5-10 recent reviews)
2. Check if most comments are generic one-liners without specific dish
   or experience details
3. Look at reviewer info: are they "Local Guide" with many reviews, or
   single-review accounts?
4. Compare the Google Maps score against the Tabelog score; a gap of ≥1.0
   is a strong signal of inflated reviews
5. Apply cumulative penalties (cap at -0.8 total) and note the adjustment
   in the output as "**adjusted score**"
6. If fake reviews are suspected, add a warning emoji and note:
   `⚠ Google Maps score adjusted ({original} → {adjusted}): suspected fake reviews detected`

### Step 5: Format and present results

Present **3 to 5 recommended restaurants** directly in Markdown format as follows:

---

#### Recommendation output format

For each restaurant, present:

```markdown
## {rank}. {restaurant_name}

**Composite Rating: {composite_score}/5.00** ({total_reviews} reviews)

| Source | Rating | Reviews |
|---|---|---|
| Tabelog | {score}/5.0 | {count} reviews |
| Google Maps | {score}/5.0 | {count} reviews |
| Hot Pepper | {score}/5.0 | {count} reviews |

- **Genre:** {cuisine_type}
- **Area:** {area} ({nearest_station}, {walk_minutes} min walk)
- **Budget:** {budget_range} per person
- **Hours:** {business_hours}
- **Regular holiday:** {holidays}
- **Seats:** {seat_count} seats ({room_types})
- **Features:** {features}

### Recommended courses

| Course name | Price | Duration | Includes |
|---|---|---|---|
| {course_name} | {price} | {duration} | {description} |

### Quick links

- [Tabelog page]({tabelog_url})
- [Hot Pepper page]({hotpepper_url})
- [Google Maps]({google_maps_url})
- [Reserve on Tabelog]({tabelog_reservation_url})
- [Reserve on Hot Pepper]({hotpepper_reservation_url})
- [Call to reserve](tel:{phone_number})
```

---

### Step 6: Assist with reservation

After presenting results, ask the user:

- "Would you like more details about any of these restaurants?"
- "Shall I search for more options with different criteria?"
- "Would you like help narrowing down the choice?"

If the user selects a restaurant, provide:

1. Direct reservation page links (one-click access)
2. Phone number for telephone reservations
3. Google Maps link for directions
4. Recommended course based on their budget and party size

---

## Tips for Effective Searching

- **Area specificity matters:** "新宿駅東口" yields better results than "新宿"
- **Include occasion context:** Searching "歓送迎会" or "女子会" gives targeted results
- **Budget keywords help:** Include "3000円" or "飲み放題付き" to filter results
- **Verify recency:** Check that business hours and holiday info are current
- **Cross-reference ratings:** A restaurant with high ratings on both Tabelog and
  Google Maps is more reliably good than one with a high score on only one platform

See `references/search-guide.md` for a comprehensive search strategy reference.

---

## Error Handling

### Search-level issues

| Issue | Solution |
|---|---|
| No results found for area | Broaden the area (e.g., "新宿" instead of "新宿三丁目") |
| Budget too restrictive | Suggest adjusting budget range or removing course requirement |
| No reviews available | Note this to the user; rely on other available sources |
| Outdated information suspected | Warn the user and suggest calling to confirm |
| All-you-can-drink not available | Suggest alternative plans or nearby options that offer it |

### WebFetch access errors

| Error | Affected sites | Solution |
|---|---|---|
| **HTTP 403 Forbidden** | 食べログ, ホットペッパー, RETRIP | Bot protection is active. Do NOT retry. Use `WebSearch` snippets for ratings/info, or fetch the same restaurant from a Tier 1 site instead |
| **HTTP 404 Not Found** | ホットペッパー (store pages) | URL may have changed. Search for the restaurant name + "ホットペッパー" via `WebSearch` to find the current URL |
| **Sibling call cancelled** | Any site in a failed batch | A different call in the same parallel batch failed. Re-fetch the cancelled URLs in a new, smaller batch (1-2 calls) |
| **Empty/JS-only content** | colmo, some SPA-based review sites | Site requires JavaScript rendering. Skip `WebFetch` and rely on `WebSearch` snippets only |
| **Timeout** | Any site under heavy load | Retry once individually (not in a batch). If still failing, fall back to `WebSearch` snippets |

### Recovery priority

When multiple fetches fail, prioritize recovery in this order:

1. **Google Maps pages** — highest weight in composite score (45%)
2. **Tabelog search result pages** — often accessible even when individual store pages are blocked
3. **ぐるなび store pages** — moderate success rate
4. **ホットペッパー** — lowest priority due to frequent blocks; use `WebSearch` snippets for course/coupon info
