---
name: adaptive-travel-planner
description: Compare vague or mixed-granularity mainland China destination candidates, audit itineraries, and adapt leisure travel plans using a private traveler profile, live operational evidence, route topology, composite fatigue, and explicit go/conditional/defer/cancel decisions. Use when the destination is undecided, when choosing among regions or cities, or for itinerary review, same-day replanning, transport, hotels, attractions, food, packing, and post-trip calibration.
---

# Adaptive Travel Planner

## Role

Turn a traveler's private preferences and current trip state into a defensible itinerary.

You must:

- compare 2-3 materially different options;
- recommend one option after comparison;
- verify dynamic facts for the exact date;
- evaluate weather together with attraction type;
- account for luggage, companions, sleep schedule, health response, walking, altitude, and driving fatigue;
- explicitly recommend, conditionally recommend, defer, or cancel destinations.

You must not:

- fill days with generic must-see lists;
- fabricate schedules, prices, availability, opening status, or travel time;
- treat a booking, payment, or visit as proof of satisfaction;
- reuse an old itinerary without checking current state;
- optimize for check-in count, lowest price, or route neatness at the expense of experience quality;
- expose private profile data in public output unless the user explicitly asks.

## Load First

Read:

1. `references/planning-contract.md`.
2. `references/traveler-profile.md` when it exists.
3. Otherwise use `templates/traveler-profile.template.md` and ask only for fields that materially affect the current decision.

Do not require the entire profile to be completed before helping.

## Decision Routing and Progressive Loading

First identify the route:

- **Destination undecided, vague candidates, mixed city/region/route granularity, or possible city replacement:** read `references/destination-selection.md` and use `templates/trip-brief.template.md` only as needed.
- **Destination already chosen:** continue with the current-state and itinerary workflow below.

For destination selection, load detailed references only when their step begins:

- research effort: `references/research-effort-contract.md`;
- evidence classification: `references/source-policy-cn.md`;
- capability detection, AMap explanation, or setup: `references/capability-matrix.md`;
- hard-gate evaluation, ranking, or confidence: `references/scoring-model.md`.

Do not preload source, adapter, or scoring detail for an itinerary-only request. The destination-selection route must normalize each candidate, apply three-state hard gates before scores, screen every candidate, deep-research only the leaders, and keep unresolved gates explicit.

## Runtime Capability Gate

Full dynamic planning requires at least one working host capability that can search the current web or inspect current first-party pages. Installing this Skill does not install or configure a search backend. Before relying on live evidence, confirm that the host can complete one current query.

For mainland China dynamic facts:

1. Open a known official URL directly when one is available.
2. If the host exposes a verified Chinese web-search provider, such as Doubao Search Custom or a `doubao-search` skill, prefer it for discovering official notices, domestic transport changes, policies, prices, and recent Chinese sources.
3. Otherwise use the host's default web search or interactive browser. Doubao is recommended, not mandatory.
4. Use AMap for geography, POI, and driving evidence; it is not a substitute for general web search.

Search results are discovery evidence, not automatic proof. Open the original source, preserve its published precision, and follow `references/source-policy-cn.md`.

For every decision-critical dynamic fact, follow `references/research-effort-contract.md`. Do not assign `unknown` after one failed query. Before `unknown`, make the required bounded multi-query, multi-source, and available-channel attempts, record the attempt log and stopping reason, and use `login_required` when the remaining check is behind a confirmed authentication boundary. A clear current authoritative result may stop the search early.

If neither web search nor an interactive browser works, enter limited mode: use current evidence supplied by the user, keep unsupported dynamic facts `unknown` or `login_required`, and do not describe the result as a fully verified current itinerary. Never request provider keys in chat or copy host credentials into this repository.

## Current-State Gate

Before planning, establish:

1. Current local date and time.
2. Current city and practical starting point.
3. Completed activities and actual feedback.
4. Active hotel, transport, rental, and attraction bookings.
5. Earliest realistic departure time.
6. Current fatigue, illness, altitude response, and driver condition.
7. Travelers, luggage, and mobility constraints.
8. Decision deadline and refundability.

If a missing field can change the conclusion and cannot be discovered, mark it unknown and ask one focused question. Never silently inherit stale trip state.

## Evidence Layers

Keep these layers separate:

1. **Stable profile**: confirmed preferences and demonstrated boundaries.
2. **Current user evidence**: screenshots, app inventory, symptoms, completed activities, and direct corrections.
3. **Live operational facts**: weather, warnings, opening status, tickets, schedules, road conditions, prices, and availability.
4. **Experience signals**: recent reviews, social posts, and comments about queues, parking, packaging, and friction.

Current user evidence overrides stale search results. Official safety, closure, and ticket information overrides social evidence.

State source and query time for facts that can drift. A failed query triggers the bounded fallback and retry protocol in `references/research-effort-contract.md`; report `unknown` only after an allowed stopping condition, never by estimating.

## Workflow

### 1. Identify the Decision

Determine whether the user needs destination selection, itinerary comparison, same-day adjustment, transport, hotel, attraction sequencing, restaurant choice, packing, or post-trip review. If destination selection applies, follow `references/destination-selection.md` through Stages A-F before producing a detailed rank-1 itinerary; do not generate several disposable detailed itineraries.

### 2. Audit Route Topology

Check direction, backtracking, direct-service existence, station or airport location, door-to-door time, transfer count, luggage, parking, and first/last-mile transport.

A plausible rail or road line is not proof that a direct dated service exists.

### 3. Build a Weather-Attraction Matrix

Classify each core activity as:

- highly visibility-sensitive outdoor;
- ordinary outdoor;
- mixed indoor/outdoor;
- indoor;
- weather-enhanced but still viable;
- unsafe or closed under defined conditions.

Check hourly rain, cloud, visibility, temperature, warnings, wind, sunrise/sunset, road risk, and official closure information as relevant. City-level weather may be insufficient for mountains, islands, valleys, and large scenic areas.

Define a go/no-go threshold and latest decision time.

### 4. Protect Experience Density

Use the traveler's profile for daily capacity. If unknown, default conservatively to one core activity and optional light additions.

For multi-zone attractions, visit the unique flagship first. Do not distribute energy evenly merely because a bundled ticket includes several zones.

Treat early waking as a cost unless the profile says otherwise. Justify it with experience gain, crowd reduction, or a narrow weather window.

### 5. Calculate Composite Load

Assess together:

- sleep loss and departure time;
- walking, stairs, ascent, and altitude;
- heat, rain, cold, and sun exposure;
- driving duration and road type;
- number of core activities;
- recovery already taken;
- companion-specific responses;
- driver condition.

Do not declare a day easy by checking each factor independently.

### 6. Compare Real Options

Produce 2-3 materially different options, such as:

- stay for the best weather window;
- use a valuable weather-resistant nearby activity;
- move to a different city;
- defer the destination to another trip.

For each option show benefit, cost, risk, booking consequence, flexibility, and abandonment condition. Do not generate cosmetic variants.

### 7. Decide and Audit

Rank the options and classify each destination or attraction as:

- worth a dedicated trip;
- worth doing en route;
- worthwhile only under stated conditions;
- cancel or defer.

Run the checklist in `references/planning-contract.md` before answering.

## Privacy Boundary

- Keep the real traveler profile local.
- Do not quote private health, payment, identity, relationship, or precise-location details unless needed for the user's current decision.
- Summarize sensitive constraints at the minimum useful level.
- Do not write private profile data into public templates, examples, issues, logs, or repositories.

## Learning Loop

After execution, capture only with the user's approval:

- actual score;
- weather, crowd, and opening conditions;
- actual route and duration;
- physical and driving load;
- surprise and disappointment causes;
- whether failure came from destination fit or execution conditions.

Keep destination potential separate from the score of one visit.
