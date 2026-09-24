---
name: semantic-gap-analysis
description: Use when a page ranks for a keyword but isn't in the top 3 and you want to know exactly what's missing. The agent compares the page to the top-ranking competitors and produces a specific list of entities, subtopics, and relationships to add.
---

# Semantic Gap Analysis

Identifies the exact entities, subtopics, predicates, and relationships that are missing from your page but present in top-ranking competitors. This is the content brief for what to add — not a generic "write more depth" recommendation.

Google's NLP models (BERT, MUM, Gemini) build a semantic graph of your content. If you're missing nodes or edges that competitors have, your content reads as shallow to the algorithm. This skill finds the exact missing nodes.

## Input

- **URL of your page** (required)
- **Target keyword** the page should rank for (required)

## Role

You are a semantic SEO specialist in the tradition of Koray Tuğberk GÜBÜR. You think in entities, attributes, and relationships — not keywords.

## Step 1: Read Your Page

Fetch the URL. Extract:
- Main topic and sub-topics
- All named entities (people, places, products, concepts, dates, organizations)
- All predicates (verbs that signal the contextual depth — for "coffee brewing", verbs like grind, extract, bloom, tamp)
- Internal structure: H2/H3 hierarchy
- What the page explicitly covers and what it implicitly assumes

## Step 2: Read the Top 3 Competitors

Google the target keyword. Fetch the top 3 results in full. If one won't fetch, take the next result down and say so — a gap list built on an inferred page is worthless. For each:
- Extract entities, predicates, and structural elements the same way
- Note what they cover that your page doesn't
- Note the depth at which they discuss each entity (single mention vs. full section)

## Step 3: Build the Semantic Inventory

Create three lists side by side:

| Your page covers | Competitors cover but you don't | Unique to your page |
|---|---|---|

Be specific. "Pricing models" is too generic. "Three-tier vs usage-based pricing with examples from Stripe and Twilio" is specific.

## Step 4: Classify the Gaps

For each gap, classify its importance:

- **Core gap** — all 3 competitors cover this, you don't. Critical to add.
- **Differentiator gap** — 1-2 competitors cover this and it's working for them. Worth adding.
- **Commodity gap** — everyone covers this superficially. Add briefly or skip.
- **Opportunity gap** — competitors skip this, you could own it. Your angle.

## Step 5: Map Entity Relationships

For the core gaps, identify the Entity-Attribute-Value (EAV) relationships that should exist:

- **Entity**: what is it
- **Attribute**: what properties does it have that matter
- **Value/Relation**: how does it relate to other entities in this topic space

Example for "espresso machine reviews":
- Entity: La Marzocco Linea Mini
- Attribute: brew pressure, boiler type, price point
- Relation: competes with Rocket Appartamento, used by third-wave cafes

This is what competitors are implicitly encoding when they write detailed sections — you need the same density.

## Step 6: Output

### Semantic Fingerprint
One sentence on what your page actually "talks about" to an NLP model, and what it should talk about.

### Your Page
List of entities and predicates currently present.

### Competitor Coverage
What each top 3 competitor covers that yours doesn't (specific sections, with brief notes on why they chose to include them).

### Gap List

| Gap | Importance | Add to section | Depth required |
|---|---|---|---|

Importance: Core / Differentiator / Commodity / Opportunity.
Section: where in your H2/H3 structure this belongs.
Depth: Paragraph / subsection / full section.

### Entity Relationships to Encode
The EAV triples that should appear in your page, even if just in passing. These are the signals that tell Google "this content understands the topic space."

### Unique Angle to Preserve
What your page does well that competitors don't. Don't lose this when adding depth.

### Content Addition Plan
Specific sections to add or expand, in order of priority. Each with: section heading, 2-3 sentence description of what goes in it, estimated word count.

## What to Ignore

- **Keyword density for related terms** — don't force. Semantic relevance is about covering the entities, not repeating the keyword variants.
- **Fluff additions** — every section you add should carry actual information. Padding defeats the purpose.
- **Wikipedia-style completeness** — you don't need to cover everything. You need to cover enough that an NLP model recognizes the topic depth.

## Next Step

Turn the content addition plan into an actual rewrite: use the `improve-content` skill with your page URL as input, and paste the gap list as context.

## Bundled references

Load from `references/` only when the step calls for them.

- **`eav-triple-worked-examples.md`** — full Entity-Attribute-Value examples across 6 niches for Step 5 (when the EAV framework feels abstract and you need concrete analogues)
- **`predicate-verb-fields.md`** — domain-specific verb fields that signal contextual depth to NLP models (Step 3, when extracting predicates from competitor pages)
- **`gap-classification-rubric.md`** — detailed scoring for Core / Differentiator / Commodity / Opportunity gaps (Step 4, when classification is ambiguous)
- **`topic-cluster-strategy.md`** — how the gap list feeds into cluster architecture (optional, when the gaps reveal missing spokes rather than in-page sections)
