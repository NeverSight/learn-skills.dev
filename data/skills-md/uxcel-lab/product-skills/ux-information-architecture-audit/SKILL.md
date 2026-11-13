---
name: ux-information-architecture-audit
description: Run a structured information architecture audit on a sitemap, navigation tree, category structure, menu labels, or multi-screen product. Produces a severity-rated issue list with concrete fixes — catches scheme/task mismatches, narrow-and-deep hierarchies, low-information-scent labels, inconsistent labeling systems, single-path findability, and dead-end pages. Use when auditing IA, site structure, categories, taxonomy, or labels, or as a validation step after generating navigation or any multi-screen structure.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Information Architecture Audit Skill

## What this skill changes vs. default behavior

By default, Claude critiques a structure by eyeballing the category names — it rarely tests whether the *organization scheme* matches how users actually seek, whether labels carry information scent before the click, whether the hierarchy's breadth/depth ratio forces click-tunneling, or whether users landing mid-site can orient at all. This audit forces four things: every finding names the violated IA principle; labels are tested for scent ("could a user predict the destination?"), consistency, and vocabulary fit; the structure is checked against the seeking modes it must serve, not just the browse-from-homepage path; and findings come severity-rated with concrete fixes — including which research method (card sort, search-log analysis, free listing) would settle a contested call.

This is an **evaluative** skill: it auto-runs whenever a sitemap, navigation structure, category system, or multi-screen flow is being reviewed — and as a validation step after generative skills that structure content (`ux-navigation`, `ux-menus`, `ux-search`).

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when an orchestrator (`ux-design-review`) or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **Tier B — offered**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. Organization scheme matches the user's task

Schemes are exact (alphabetical, chronological, geographical) or subjective (topical, task-oriented, audience, metaphor, hybrid). Exact schemes work only when users know the item's name; subjective schemes serve browsing and discovery. The choice follows from top user tasks, not from what's easiest to build.

**Flag when:** alphabetical ordering on content users browse by category (a spa listing services A–Z); chronological where users seek by topic; a metaphor scheme requiring users to learn the metaphor; a hybrid mixing many schemes deep in navigation (fine on a homepage, confusing at depth).

- ❌ Documentation sorted A–Z by article title.
- ✅ Docs grouped by user task ("Getting started," "Billing," "API"), with an A–Z index as a supplement.

### 2. Structure: breadth, depth, and type

Broad-and-shallow beats narrow-and-deep — every extra level is a forced guess. Categories should be mutually exclusive (limited cross-listing is fine; everywhere-cross-listing means the categories don't work). The structure type must fit the content: hierarchy for top-down browsing, database/metadata for large homogeneous sets (catalogs, directories), sequential for step-by-step processes, flat for small sites; hypertext links only as a supplement, never the main structure.

**Flag when:** content buried 4+ levels deep; one category holding 80% of items while siblings hold 3; the same item cross-listed nearly everywhere; a large catalog with no metadata/filter model; a structure that already strains at current content volume (the growth test: where do the next 50 items go?).

- ❌ Products > Software > Tools > Utilities > Converters > PDF (6 levels, one path)
- ✅ Three top-level categories + faceted filters that cut the same set by price, brand, and type.

### 3. Labeling system quality

Labels must use the audience's vocabulary (jargon-free, matching mental models — "Inbox," not "Message repository") and be **consistent as a system**: same style, syntax (don't mix verb-, noun-, and question-based), granularity ("Electronics" doesn't sit beside "Smartphones"), and comprehensiveness ("Men's Shoes" and "Kids' Shoes" with no "Women's Shoes" makes users distrust the whole system). Icons-as-labels need text unless the option set is small and learned.

**Flag when:** the same destination has different names on different screens ("Search" / "Browse" / "Find"); category names are CTA verbs ("Explore," "Discover," "Learn") that say nothing about content; conversational labels where users want speed ("I want to pay my taxes" → "Pay Taxes"); parallel-language forced until labels go redundant; unlabeled ambiguous icons.

- ❌ Nav: "Explore" · "Discover" · "More"
- ✅ Nav: "Courses" · "Pricing" · "Help"

### 4. Information scent

Users choose links by predicting how likely the destination answers their question. Every link label, summary, and image is a promise about the destination; weak or wrong promises cost a click *and* trust. Pages need immediate context — headings and descriptions that confirm "you're in the right place."

**Flag when:** "Learn more" / "Click here" links; link text that doesn't match the destination page's content; generic or misrepresentative category imagery (a tomato basket for "Fruit"); landing pages that are one big image with no orienting text; summaries that don't say what the content actually covers.

- ❌ "Learn more →" (destination unguessable)
- ✅ "How to fix a leaking faucet →"

### 5. Findability across seeking modes

People arrive in different modes: known-item search, exploratory seeking, directed/semi-directed/undirected browsing, re-finding, and "don't know what you need to know." A structure that serves only one mode loses everyone else. This demands **multiple classification paths** (browse + search + filters), search where content is large, related-content links for evolving needs, and re-finding support (recently viewed, history) since people heavily revisit.

**Flag when:** browse is the only path through a large content set (no search); search-only with no browsable structure for users who can't name what they want; no related/contextual links for exploratory users; nothing supports returning to previously seen items; navigation assumes domain expertise novices don't have ("Resources" hiding tax forms — say "Tax Forms").

- ❌ A 5,000-product store navigable only by its category tree.
- ✅ Category tree + search with suggestions + filters + "Recently viewed."

### 6. Every page is a front door

Users land mid-site from search and links. Any page must let them identify where they are, reach main areas, and recover — no orphan pages or dead ends. (How that's rendered — breadcrumbs, headers, highlighted nav states — belongs to `ux-navigation`; this audit checks the *capability* exists.)

**Flag when:** detail pages with no path to siblings or parent category; landing pages disconnected from global navigation; no "where am I" signal anywhere on deep pages.

- ❌ A product page reachable from Google with no category links, no nav, and no related items.
- ✅ The same page with breadcrumb trail, category links, and alternatives — useful even when *this* product isn't right.

### 7. Choices and disclosure

Show few options at a time and reveal detail progressively — an IA can be complete and still overwhelm by presenting everything at once. Prioritize the links that serve primary user types and key tasks rather than exposing the full tree.

**Flag when:** a mega-menu exposing 60 links with no grouping; every level of the hierarchy visible at once; key tasks buried in an exhaustive A–Z of everything the org offers.

- ❌ Banking app home listing all 32 account operations.
- ✅ Balance, Transfer, Pay Bills up front; the rest behind "All services."

> **Tension note:** multiple classification vs. simplicity — more paths help diverse users but each adds surface; add a path only for a real seeking mode, not hypothetically. Consistency vs. natural language — don't force parallel labels ("Read Travel Guides") where natural phrasing ("Travel Guides") is clearer. And mutual exclusivity vs. cross-listing — some items legitimately live in two places; flag *systematic* ambiguity, not every judgment call.

---

## Evidence over opinion

When a finding is contestable, name the method that settles it rather than asserting taste:

- **Open card sort** — users' natural groupings and language; for building or questioning the category model.
- **Closed card sort** — whether existing categories work; which are confusing or redundant.
- **Search-log analysis** — the words users actually type (term choice, length, jargon vs. plain).
- **Free listing** — cheap vocabulary elicitation for label candidates.
- **Content inventory & audit** — what content exists, what's redundant/outdated, before judging its arrangement.

A recommendation like "rename 'Resources' — closed card sort showed users can't predict its contents" is a finding; "I'd call it something else" is not.

---

## Severity rating

Rate each finding by **lostness cost** — how often users hit it × how badly it strands them:

| Severity | Meaning |
|---|---|
| **Critical** | Users cannot find primary content or complete key tasks (core content buried or mislabeled, no path serving the dominant seeking mode, dead-end entry pages) |
| **Major** | Frequent disorientation and wasted clicks (narrow-deep hierarchy, low-scent navigation labels, inconsistent label system, missing search on large sets) |
| **Minor** | Friction users recover from (mixed label granularity in a secondary menu, weak summaries, suboptimal scheme on low-traffic sections) |
| **Cosmetic** | Polish; don't pad the report with these |

Overlaps: sentence-level copy clarity and tone belong to `ux-microcopy-audit` — this audit owns the label *system* (consistency, scent, vocabulary fit). Navigation component placement and rendering belong to `ux-navigation`. Keyboard/screen-reader navigability belongs to `ux-accessibility-audit`. Search interaction design belongs to `ux-search` — this audit checks whether search *exists where needed* and is fed by sound structure.

---

## Output format

```
## Information Architecture Audit — [Target]
Context: [product type · content volume · primary user tasks/seeking modes, if known]

### Critical
- [Issue] — what's wrong → fix (and the method that would settle it, if contested). (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest lostness-cost fixes.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — content volume (50 pages vs. 50,000 changes every recommendation), primary user tasks, audience domain familiarity, and which seeking modes dominate. IA value is also strategic: check the structure serves the business's key actions, not just tidiness.
2. **Audit from entry points, not the homepage** — walk in as a search-engine arrival on a deep page, as a known-item searcher, and as a browser. The homepage-down view hides most IA failures.
3. **Only flag real costs** — an imperfect scheme on a 12-page site users navigate fine is not a finding.
4. **Respect the tensions** — don't demand more paths *and* more simplicity in the same report without saying which wins where.
5. **Be specific in fixes** — propose the regrouping, rewrite the label, name the research method. Never just "improve the navigation."

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Critique category names by taste | Test labels for scent, vocabulary fit, and system consistency — and name the method that settles contested calls |
| Audit only the homepage-down browse path | Walk known-item search, exploratory, deep-link entry, and re-finding |
| Praise a tidy-looking deep hierarchy | Check breadth/depth: broad-and-shallow wins; count clicks to key content |
| Treat search as optional garnish | Flag missing search on large sets; flag search-only with no browse |
| Accept "Explore" / "Discover" / "Learn more" | Require labels that predict the destination |
| Recommend one fixed classification for everyone | Check for multiple paths matching real seeking modes |
| Re-derive copy tone or accessibility specifics | Defer to `ux-microcopy-audit` / `ux-accessibility-audit` |
| Ignore where the next 50 items will go | Apply the growth test to every structure |
| Deliver an unranked issue dump | Severity by lostness cost + top-3 priorities |

---

## Source lessons (Uxcel)

- [The Principles of Information Architecture](https://uxcel.com/lessons/the-principles-of-information-architecture-251)
- [Organization Systems](https://uxcel.com/lessons/organization-systems-111)
- [Intro to Information Architecture](https://uxcel.com/lessons/information-architecture-470)
- [Basic Components of IA](https://uxcel.com/lessons/basic-components-of-ia-296)
- [Labelling System](https://uxcel.com/lessons/labelling-system-461)
- [How People Navigate](https://uxcel.com/lessons/how-people-navigate-483)
- [How People Seek Information](https://uxcel.com/lessons/how-people-seek-information-191)
- [Content Inventory & Audit](https://uxcel.com/lessons/content-inventory-audit-973)
- [Card Sorting in UX Research](https://uxcel.com/lessons/card-sorting-237)
