---
name: trip-planner
description: Plan trips with assumptions, not questions. Trip Planner extracts flight constraints from natural conversation, fills in the gaps with smart defaults, and returns structured flight recommendations with direct booking links. Assume first. Show your work. Book the flight. Just say "trip-planner" to get going.
---

# Trip Planner

A skill that turns natural language into flight recommendations — preferring assumptions over questions.

> *Assume first. Show your work. Book the flight.*

## Core Design Principle

**Assume everything, show everything.** The user corrects what's wrong, not fills in what's missing. The only hard requirement is a destination — everything else has a sensible default.

## Two Flows

| Condition | Flow |
|-----------|------|
| No `.claude/trip-planner.md` exists | **Onboarding Flow** — instant search, then quick setup |
| `.claude/trip-planner.md` exists | **Regular Flow** — FAST: parse, assume, search, recommend |

---

## Onboarding Flow (First Run Only)

**Detection:** Check if `.claude/trip-planner.md` exists. If no config exists, run this flow. Otherwise skip to Regular Flow.

**Goal:** Deliver flight recommendations immediately, then calibrate preferences.

### Step 1: Welcome (skip if user already described a trip)

Read `references/branding.md` and display verbatim:
1. Logo
2. Origin quote
3. Workflow diagram
4. Key concepts

Then check: did the user already describe a trip in their message?

- **Yes** → Skip straight to Step 2 with their input
- **No** → Display:

```
Where are you headed? Just describe your trip naturally:

"I need to fly to Tokyo next month for a week"
"London to Paris, March 15-18, 2 adults"
"Cheapest flights to Barcelona in April"
```

**Wait for user input.**

### Step 2: Parse & Assume

Extract what the user said, then fill everything else with defaults.

Run the **Assumption Engine** (see below) against the user's input with these fallback defaults for onboarding (no config yet):
- Origin: LHR
- Class: Economy
- Passengers: 1 adult
- Budget: Flexible
- Stops: Any
- Currency: GBP

**Show the Assumption Card:**

```
## Assumptions

| Field | Value | Source |
|-------|-------|--------|
| Destination | Tokyo (NRT/HND) | You said |
| Origin | London (LHR) | Default |
| Dates | Mar 10 - Mar 17, 2026 | "next month" + 7 days |
| Passengers | 1 adult | Default |
| Class | Economy | Default |
| Budget | Flexible | Default |
| Stops | Any | Default |

Anything wrong? Say so and I'll re-search. Otherwise I'll find flights.
```

**Wait for corrections or confirmation.**

If user corrects → update assumptions → re-show card → wait again.

If user confirms (or says nothing wrong) → proceed to Step 3.

### Step 3: Search & Present

Run the **Search Strategy** (see below) with confirmed assumptions.

Present recommendations using the output format from `assets/templates/trip-recommendation.md`.

Then offer corrections:

```
Want to adjust anything? Change dates, class, budget — I'll re-search.
```

**Corrections loop:** User adjusts → re-search → re-present. Repeat until satisfied.

### Step 4: Quick Setup

Once the user is happy with results:

```
Nice — that's your first search done.

Want to save your preferences so next time is faster? Quick 5 questions:

1. What's your home airport? (e.g. LHR, JFK, LAX)

2. Any preferred airlines? (comma-separated, or "none")

3. Default budget range per person? (e.g. "under 500", "flexible", "100-300")

4. Preferred class? (economy / premium economy / business / first)

5. Preferred booking platform? (skyscanner / google-flights / kayak)
```

Parse response and use sensible defaults for skipped fields:
- home_airport: "LHR"
- preferred_airlines: []
- budget: "flexible"
- class: "economy"
- platform: "skyscanner"

Write `.claude/trip-planner.md` config (see Config Structure below).

```
Saved to .claude/trip-planner.md

Run /trip-planner anytime — just describe where you want to go.
```

**Exit after onboarding.**

---

## Regular Flow (Every Subsequent Run)

**FAST approach — no questions, just recommend:**
1. Parse intent from natural language
2. Load config for defaults
3. Run Assumption Engine (fill all gaps)
4. Search for flights
5. Present recommendations with booking links

### Step 1: Parse Intent

Extract from the user's message:
- **Destination(s)** — city names, airport codes, or countries
- **Dates** — explicit dates, relative dates ("next month"), or vague ("in April")
- **Budget** — explicit amounts or qualifiers ("cheap", "under 300")
- **Class** — economy, premium economy, business, first
- **Passengers** — number and type (adults, children, infants)
- **Preferences** — direct flights, specific airlines, time of day, layover preferences
- **Multi-city** — detect "A → B → C → A" or "then" patterns

If the user just names a destination with no other details, that's fine — the Assumption Engine handles the rest.

### Step 2: Load Config

Read `.claude/trip-planner.md` for user defaults.

See `references/config-guide.md` for configuration options.

**Fallback defaults (if config missing or incomplete):**
- name: ""
- home_airport: "LHR"
- class: "economy"
- budget: "flexible"
- currency: "GBP"
- stops: "any"
- preferred_airlines: []
- platform: "skyscanner"

### Step 3: Assumption Engine

Fill missing fields using this priority order:

1. **Explicit user input** — what they said in this message
2. **Config file defaults** — from `.claude/trip-planner.md`
3. **Contextual inference** — smart guesses based on trip type:
   - City break (European short-haul) → 3-4 days
   - Intercontinental → 7-10 days
   - Weekend trip → Friday-Sunday
   - "Holiday" / "vacation" → 7 days
   - Month mentioned but no dates → middle of month, flexible
4. **Smart defaults** — final fallback:
   - 1 adult
   - Economy
   - Flexible budget
   - Any stops
   - Home airport from config (or LHR)
   - Dates: 4 weeks from today, 7 days duration

**Get current date:** Run `date` command — do not rely on system date.

**Show the Assumption Card** (always — every assumption must be visible):

```
## Assumptions

| Field | Value | Source |
|-------|-------|--------|
| Destination | {dest} | You said |
| Origin | {origin} | Config / Default |
| Dates | {dates} | {source} |
| Passengers | {pax} | {source} |
| Class | {class} | {source} |
| Budget | {budget} | {source} |
| Stops | {stops} | {source} |

Anything wrong? Otherwise I'll search.
```

**Wait for corrections or confirmation** before searching.

If user corrects → update → re-show card → wait.

### Step 4: Search

Run the **Search Strategy** (see below) with confirmed assumptions.

### Step 5: Present

Use the output format from `assets/templates/trip-recommendation.md`.

Present 3-5 flight options across three categories:
- **Best Value** — best balance of price, duration, and convenience
- **Cheapest** — lowest price regardless of convenience
- **Fastest** — shortest total travel time

Include direct booking links for each option.

Then offer corrections:

```
Want to adjust anything? I can re-search with different dates, budget, or preferences.
```

**Corrections loop:** User adjusts → re-run from Step 3 with updates → re-present.

---

## Assumption Engine — Detail

The engine runs on every search. It produces a complete set of flight parameters from partial input.

### Priority Order

```
User Input > Config > Context Inference > Smart Defaults
```

### Context Inference Rules

| Signal | Inference |
|--------|-----------|
| European city + no dates | City break: 3-4 days |
| Intercontinental + no dates | 7-10 days |
| "Weekend" mentioned | Friday evening → Sunday evening |
| "Holiday" / "vacation" | 7 days |
| Month only, no specific dates | Middle of month, flag as flexible |
| "Christmas" / "Easter" / "New Year" | Standard holiday date ranges |
| "Summer" / "Winter" | Peak month of that season |
| Return to origin in multi-city | Round trip, proportional days per city |
| "Cheap" / "budget" mentioned | Sort by price, flag budget airlines |
| "Direct" / "non-stop" mentioned | Filter to direct flights only |
| No class mentioned + business destination | Still assume economy (don't upsell) |

### Destination Resolution

When user gives a city name:
- Map to primary airport code(s)
- For cities with multiple airports, include all (e.g. London → LHR/LGW/STN, Tokyo → NRT/HND, New York → JFK/EWR/LGA)
- For countries or regions, map to capital or most common tourist airport

### Date Handling

- Always use `date` command for current date
- "Next month" → 1st of next month + duration
- "In March" → March 15 (mid-month) + duration, flag as flexible
- "March 15" → exact date + duration
- "March 15-18" → exact range
- "Next weekend" → upcoming Friday-Sunday
- No dates at all → 4 weeks from today + duration based on trip type

---

## Search Strategy

### Step A: Construct Booking URL

Build a Skyscanner URL (or platform from config) from parameters:

```
https://www.skyscanner.net/transport/flights/{origin}/{dest}/{depart_date}/{return_date}/?adults={n}&cabinclass={class}&currency={currency}
```

**Skyscanner URL format:**
- Dates: `YYMMDD` (e.g. `260315` for March 15, 2026)
- Origin/dest: airport codes lowercase (e.g. `lhr`, `nrt`)
- Cabin class: `economy`, `premiumeconomy`, `business`, `first`

For multi-city, construct per-leg URLs.

**Google Flights URL (if configured):**
```
https://www.google.com/travel/flights?q=flights+from+{origin}+to+{dest}+on+{date}
```

### Step B: WebSearch for Pricing

Run 2-3 WebSearch queries per leg to gather current pricing intelligence:

**Query templates:**
- `"flights {origin} to {dest} {month} {year} price"`
- `"cheap flights {origin} to {dest} {month} {year}"`
- `"{airline} {origin} {dest} {month} {year} fare"` (if preferred airline set)

Parse results for:
- Airlines operating the route
- Approximate price ranges
- Flight duration and stop information
- Any deals or sales mentioned

### Step C: WebFetch Booking Page (optional)

Attempt `WebFetch` on the constructed Skyscanner URL to get live pricing.

- **If successful:** Extract specific flight options with prices
- **If blocked/failed:** Gracefully fall back to WebSearch data. Do not retry or error — just note that prices are approximate

### Step D: Compile Results

Merge data from WebSearch and WebFetch (if available):
- Deduplicate by airline + route + approximate time
- Sort into three categories: Best Value, Cheapest, Fastest
- Include direct booking URL for each option
- Flag any data as "approximate" if from WebSearch only vs live pricing

### Multi-City Search

For multi-city trips (e.g. "London → Paris → Rome → London"):
1. Decompose into individual legs
2. Search each leg independently (can run WebSearch queries in parallel)
3. Present combined itinerary overview + per-leg options
4. Calculate total cost across all legs
5. Provide individual booking links per leg AND a combined multi-city search link

---

## Config Structure

Stored as `.claude/trip-planner.md` in user's working directory.

```yaml
name: "Foluso"
home_airport: "LHR"

preferences:
  class: "economy"
  budget: "flexible"
  currency: "GBP"
  stops: "any"
  preferred_airlines: []
  time_preference: "any"    # morning / afternoon / evening / any

platform:
  primary: "skyscanner"     # skyscanner / google-flights / kayak
```

See `references/config-guide.md` for full field documentation.

---

## Key Principles

- **Assume everything, show everything.** Never ask a question when you can make a reasonable assumption. Always show what you assumed so the user can correct.
- **One hard requirement: destination.** Everything else has a default. A user saying "flights to Tokyo" is enough to produce a full recommendation.
- **Value first, setup later.** Search before asking for configuration. Onboarding creates value immediately.
- **Corrections over questions.** Present assumptions, let user fix what's wrong. Faster than asking upfront.
- **Show your sources.** Every assumption in the card has a "Source" column. Every price has a booking link.
- **Graceful degradation.** If WebFetch fails, fall back to WebSearch. If WebSearch is sparse, still show what you have with booking links.
- **Always get current date.** Run `date` command — do not rely on system date or knowledge cutoff.
- **Multi-city is first-class.** Not an afterthought. Decompose, search per-leg, present combined.

---

## File Paths

| Type | Path |
|------|------|
| Config | `.claude/trip-planner.md` |
| Skill | `.claude/skills/trip-planner/SKILL.md` |
| Branding | `references/branding.md` |
| Config Reference | `references/config-guide.md` |
| Future Enhancements | `references/future.md` |
| Output Template | `assets/templates/trip-recommendation.md` |
