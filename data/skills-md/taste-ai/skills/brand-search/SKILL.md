---
name: brand-search
description: Use when the user needs website design references — whether they describe a style or mood, name reference sites, want brands visually similar to an existing site, or ask for a website without an established visual direction (e.g. "build a website for my bakery"). Finds real websites from a curated library to inform design decisions before building.
---

# Brand Search

## 1. Pick the right search tool

Both tools return the same thing: website references, each with summary brand metadata and a screenshot. They differ in what goes in.

`search_brands`: a natural-language query goes in. What the user or the agent asked for becomes the query. Ex: `search_brands("dark brutalist developer tools")`, `search_brands("warm pastel skincare landing pages")`.
`search_similar_brands`: the `submission_id` of a completed extraction goes in, and that site's nearest visual neighbours come out. Ex: you extracted linear.app, got back its `submission_id`, and pass that id in.

### `search_brands`

Build each query knowing what you're looking for — style, layout, palette, motion, tone — and write it by the guidelines below.

- Always follow the original intent of the user's or agent's prompt. Don't add anything they didn't ask for, and don't translate what they did. If the prompt says "monochromatic", the query is monochromatic, not "black and white".
- Inspect every returned result as described in step 3 before selecting references.

A prompt that's just a vibe gets a query that's just the vibe: `search_brands("dreamy editorial skincare, calm and warm", top_k=6)`.

When the user names a style or movement, carry the word exactly as they wrote it. The search is what interprets style terms, including ones nothing is formally tagged with — swapping in your own synonym would decide what the search was supposed to decide. `search_brands("vintage feeling clothing brand site")` keeps "vintage" even though the corpus's official tag for that register is "Retro": the user said vintage, so vintage is what gets searched. Same discipline behind `search_brands("y2k web aesthetic for a music label")` and `search_brands("swiss international style studio portfolio")`.

When a color or tone seeds the prompt, recruit by color role rather than hue: the useful cluster is sites where the tone plays the same structural part — ground, ink, or accent — never hue neighbours where it plays a different one. `search_brands("cream ground with a terracotta accent")` is built that way.

A reference with a pivot goes inside the query itself, where it steers the search instead of supplying a reference: `search_brands("like Notion but for restaurants")`. Run the site-to-site path too, as its own set — covered below.

When the prompt already crosses industries — "playful colorful consumer fintech", "a B2B SaaS brand that feels gaming inspired" — that pairing travels straight into the query, no invention needed: `search_brands("playful colorful consumer fintech")`, `search_brands("B2B SaaS brand that feels gaming inspired")`.

### `search_similar_brands`

Use this one when you already have a brand and want others that look like it — whether that brand is the inspiration to follow or the anchor to pivot away from. It reads a completed extraction, not a url, so get the anchor first:

- You already have the extraction — from this run or an earlier one — so pass its `submission_id` straight to `search_similar_brands`.
- You only have a url — off a `search_brands` card, or a site the user named — so extract it first: `extract_brand(url)` → poll → `search_similar_brands(submission_id)`. The loop is written out in step 4.

An unqualified site — "like ours", "competitors of acme.com", "sites like patagonia.com" — calls for two lenses at once: `search_similar_brands(submission_id)` on the extraction follows the *look* (whole-gestalt visual neighbors), while an anchored deep `search_brands` follows the *meaning* (the cultural neighborhood) — `search_brands("outdoor apparel brand with rugged environmental storytelling")` for patagonia.com. Inspect the two sets separately, rank preserved inside each.

When sources are already named — "layout of linear.app, colors of ramp.com" — extract them directly, since they're already the reference: `extract_brand("https://linear.app")`, `extract_brand("https://ramp.com")`. Pull `search_similar_brands(submission_id)` on either only if the board wants more of that look; the facets those sites don't cover go to `search_brands` instead.

A site with a pivot runs its second path alongside the query: extract the anchor and take its neighbors — `search_similar_brands(submission_id)` on Notion's extraction, for a "like Notion but for restaurants" prompt. Keep the sets apart: the query carries the pivot, the neighbors only map the anchor's visual neighborhood.

And a winner worth mining isn't a prompt shape at all but the tool's other use — a second lens on a result set already in hand, `search_similar_brands(submission_id)` on the first-ranked result, covered in step 3.

## 2. Write the query without deciding the style

Build each query from what the prompt actually says: industry, page type, audience, content, named references, and any style, layout or palette words the user wrote. Your own assumptions never become aesthetic search filters. If the prompt names no style, leave style out and let the returned references show you what the directions are.

Don't decorate a query with adjectives the prompt never used — "bold retro", "appetite-forward", "neighborhood energy". Every invented descriptor pre-decides what the corpus was supposed to decide, and the results come back agreeing with you. Expressive descriptors belong in a later query, once they cite something you saw in the results and you're hunting more evidence for it.

A prompt can also hand you adjectives that aren't facts at all. "A personal website that is completely custom and unique" names no industry, no style, no reference. "Custom" and "unique" describe every prompt and search on none of them — `search_brands("completely custom and unique personal website")` just returns whatever the corpus tags as unusual, which isn't the same thing. Drop the empty adjectives, search the one real fact left (`search_brands("personal portfolio website")`), and let the results propose the directions.

`top_k` defaults to 6. Raise it (max 12) when the prompt wants a broad moodboard.

## 3. Inspect results without re-ranking

Results come back ranked: the top ones are what the search judged closest to your query, and anything labeled discovery is still a site the search considers aligned with that style, in there to keep the set diverse.

The discovery results show inspiration related to the style, carrying different facets of it, a palette you'd never have thought to write into the query, a layout structure, an illustration or type treatment.

All results of every query, including every discovery result, are mandatory evidence. For each result, read its metadata and description and view its screenshot. Inspect results in their returned order before selecting references. If you describe motion or interaction, verify it on the live site. A result may be set aside when its observed design conflicts with the user's prompt; state the specific mismatch.

If a result earns a closer read, run `extract_brand` on it. Once it's extracted, `search_similar_brands` on it widens the set with more of that brand's visual neighbourhood.

## 4. Acquire the source

Extract only when you actually need more than the card gives. The metadata, description and screenshot are usually enough to judge a reference and often enough to design from. Reach for `extract_brand` when you're going to build directly off that source and need its real values — type, spacing, palette, layout structure — or when you need a `submission_id` to feed `search_similar_brands`. Don't push a whole result set through extraction by default.

When you do need it, send the source through `extract_brand` and poll until it lands:

```
extract_brand(url)                       → submission_id
poll_brand_extraction(submission_id)     # accepted → extracting → ... → completed or failed
get_brand_extraction_result(submission_id)
```

While a batch runs, study the sources you already have and come back to the queue. Read each completed result with `get_brand_extraction_result`. Record failures and replace them with the next ranked result from the same query.
