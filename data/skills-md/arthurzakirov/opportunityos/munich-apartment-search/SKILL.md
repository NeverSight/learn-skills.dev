---
name: munich-apartment-search
description: "Search, evaluate, filter, rank, and apply for Munich apartments while balancing commute, rent, transport access, contract flexibility, and future optionality."
---

# Munich Apartment Search Skill

## Purpose

Use this skill when a user wants help searching, evaluating, filtering, ranking, or applying for apartments in Munich.

The goal is not simply to find cheap housing. The goal is to find a private, reasonably priced apartment that fits the user's real constraints while preserving future flexibility.

## Required User Context

Before making specific recommendations, collect or load the user's private context from the private context repository. Do not store personal details in this reusable skill.

Canonical private context location:

```text
$PERSONAL_REPOS_DIR/AgentDesk-private-context/apartment-search/
```

Expected files:

```text
search-context.md
search-profile.yaml
application-log.jsonl
document-manifest.yaml
field-answer-policy.yaml
```

Use `$PERSONAL_REPOS_DIR` from the environment. If it is not set, infer it from the standard repo layout as `$HOME/Repos/personal`. Do not look for private context inside public repositories such as `AgentDesk` or `OpportunityOS`.

When the canonical private context exists, load `search-context.md` first because it contains the long-form search strategy, tradeoffs, and user-specific reasoning. Then load structured files such as `search-profile.yaml`, `application-log.jsonl`, and document manifests as needed. If the private context is missing, say exactly which canonical path is missing and continue only with generic apartment-search guidance.

Useful private inputs include:

- Target commute anchor, such as workplace, university, family location, or frequent destination
- Regular travel obligations and whether they affect location choice
- Budget range and hard maximum warm rent
- Household size and apartment type preference
- Whether the user drives or depends on public transport
- Preferred transport modes, such as walking, U-Bahn, S-Bahn, bus, tram, or bicycle
- Contract flexibility needs and expected life or job changes
- Daily-life needs such as supermarket, gym, medical access, or quiet environment
- Internet and work-from-home requirements

## Core Strategy

Optimize for:

1. Private apartment, not shared housing
2. Reasonable warm rent
3. Strong public transport
4. Short commute to the user's current anchor location
5. Future flexibility for other likely anchors
6. Daily-life convenience
7. Contract flexibility

Avoid over-optimizing for a single employer or for the lowest possible rent.

The best apartment is not necessarily the cheapest one. It is the one that keeps cost reasonable while preserving commute quality, contract flexibility, and access to future opportunities.

## Hard Exclusion Filters

Reject listings immediately if any of the following apply:

- Student-only apartment
- “nur für Studenten”
- “nur für Studierende”
- Schüler-only apartment
- Azubi-only apartment
- “nur für Azubis”
- “Tauschwohnung”
- “Wohnungstausch”
- Requires the user to already have another apartment to exchange
- WG
- WG-Zimmer
- Zimmer in WG
- Shared flat
- Student dormitory
- 24-month minimum rental term
- “Mindestmietdauer 24 Monate”
- “Kündigungsverzicht 24 Monate”
- Fixed-term or lock-in contract around two years
- Rural / village-like location outside Munich with weak access to other job locations
- Warm rent above the user's hard maximum

Important: ImmoScout24 and similar search tools may not reliably support negative filters. If a search query with all negative criteria returns zero results, search more broadly and manually filter titles/descriptions.

## Apartment Type

Preferred:

- Private apartment
- 1-room apartment
- Studio apartment
- Small furnished or unfurnished apartment
- “Apartment”
- “Studio”
- “1-Zimmer-Wohnung”
- “1-Zimmer-Apartment”

Not preferred:

- WG
- Shared flat
- Student dorm
- Exchange apartment
- Temporary serviced apartment with inflated pricing or poor flexibility

## Budget

Set the target warm rent from the user's private context.

Use three bands:

- Ideal: the range where the user can afford rent comfortably
- Acceptable: the upper range that may be worth it for a strong location, contract, or commute
- Avoid: above the user's hard maximum

Munich is expensive. Do not chase unrealistic bargains if they come with student-only restrictions, WG setup, bad location, or strange contracts.

## Size

For users who prioritize savings, smaller apartments can be a rational tradeoff.

Target:

- Around 18–30 m²
- Less space is acceptable if layout is practical
- No strict minimum square meter requirement beyond basic livability

Reasoning:

- More square meters usually means higher rent
- Saving money is more important than having extra space
- A compact studio is acceptable if location, internet, and contract quality are good

## Building and Condition

Preferred:

- Built after 2000 if possible
- Modern building
- Recently renovated / “saniert”
- Good insulation
- No very old Altbau if avoidable

This is a preference, not always a hard filter. However, old poorly insulated Altbau apartments are less attractive because of possible issues with heating, noise, internet infrastructure, and general reliability.

## Internet

Internet quality is important for users who work from home, work in tech, study remotely, or rely heavily on stable connectivity.

Preferred:

- Glasfaser
- Otherwise strong cable or DSL availability
- Check provider availability for the exact address before signing

Look for:

- “Glasfaser”
- “Highspeed Internet”
- “Kabelanschluss”
- “DSL verfügbar”

## Public Transport Requirements

If the user does not own a car or does not drive, ignore parking and car access unless there is a special reason.

Important:

- Strong public transport access is a core requirement
- U-Bahn or S-Bahn should be reachable on foot
- Preferred walking time to useful station: 7–10 minutes max
- Short walking time to a reliable line matters more than theoretical map proximity
- Bus can be useful, but avoid depending on an inconvenient low-frequency bus as the main commute

Preferred transit:

- U-Bahn
- S-Bahn
- High-frequency lines
- Robust and simple routes
- Ideally 0–1 transfers to the user's main anchor

U-Bahn access can be more robust than relying only on S-Bahn in some Munich corridors. Still verify construction, disruptions, and real door-to-door commute.

## Commute

Target:

- Preferably less than 30 minutes door-to-door to the user's main anchor location, unless the user sets a different threshold
- Include walking time
- Include waiting time
- Include transfer time
- Reliability matters

Identify relevant areas and stations from the user's private commute anchors. Prefer neighborhoods that provide robust access to the main anchor while keeping access to other parts of Munich.

## Future Flexibility

This is a major criterion.

If the user may switch jobs, schools, or daily routines, the apartment should not be too optimized for one current anchor alone.

Preference:

- Avoid living too far outside Munich
- Prefer locations with access to many possible Munich work, study, and daily-life locations
- Inner-city, inner-west, and inner-southwest locations preserve optionality better
- Do not choose a far outer station just because it is slightly cheaper if it makes many other jobs harder to reach

The apartment should work for the current anchor now and still remain useful if the user's next anchor is in another part of Munich.

## Location Ranking

Build a search-specific location ranking instead of relying on a fixed neighborhood list.

Use three tiers:

- A-tier: short, reliable commute to the main anchor plus strong access to other parts of Munich
- B-tier: acceptable commute and good daily-life infrastructure, but weaker optionality or more transfers
- C-tier: only worth considering for unusually strong price, contract, or apartment quality

Normally deprioritize:

- Far outer endpoints with weak optionality
- Locations outside Munich with weak public transport access
- Neighborhoods that work only for one current anchor and would make future changes difficult

## Daily-Life Infrastructure

### Supermarket

Important:

- Supermarket within 10–12 minutes walking
- Better: 5–8 minutes walking

Useful nearby options:

- REWE
- EDEKA
- Aldi
- Lidl
- dm / Rossmann as bonus

For users without a car, grocery access is a real constraint.

### Gym / Sauna

This is a bonus, not a hard requirement.

Preferred:

- Higher-quality gym nearby or reachable by U-Bahn/S-Bahn
- Sauna is a strong plus
- Modern equipment
- User-specific gym budget, if any
- Match gym quality to the user's actual fitness habits and budget

Good enough:

- Premium gym reachable within around 30 minutes by public transport
- Should not require crossing the entire city with annoying transfers

## Contract Preferences

Preferred:

- Normal unbefristeter Mietvertrag
- Standard tenant cancellation rights
- No long minimum rental period
- 12-month minimum may be acceptable
- 24-month commitment should be avoided

Avoid:

- “Mindestmietdauer 24 Monate”
- “Kündigungsverzicht 24 Monate”
- “befristet für 24 Monate”
- Long fixed-term commitments
- Unclear serviced apartment contracts with poor flexibility

Do not rely on finding a Nachmieter unless the contract clearly supports it. A Nachmieter is a fallback, not the main exit strategy.

## Search Strategy

Do not put all negative filters into the search query. That can produce zero results or unreliable behavior.

Use this process:

1. Search broadly using positive criteria
2. Retrieve a manageable result set
3. Manually remove hard-exclusion listings
4. Score remaining listings
5. Prioritize by contract, location, commute, price, and infrastructure

## Useful Positive Search Terms

Use German terms when searching German listing sites:

```text
1-Zimmer-Wohnung München
1-Zimmer-Apartment München
Studio Apartment München
Apartment München [TARGET_NEIGHBORHOOD]
Apartment München [COMMUTE_ANCHOR_AREA]
Apartment München [TRANSIT_LINE]
Mietwohnung München bis [MAX_WARM_RENT] warm
Apartment München U-Bahn Nähe
Apartment München S-Bahn Nähe
Berufstätige
Young Professionals
unbefristet
saniert
modern
möbliert
Glasfaser
Highspeed Internet
Supermarkt fußläufig
```

## Manual Negative Terms

Watch for and exclude:

```text
Student
Studenten
Studierende
nur für Studenten
nur für Studierende
Azubi
Auszubildende
Schüler
Tauschwohnung
Wohnungstausch
WG
WG-Zimmer
Zimmer in WG
Mindestmietdauer 24 Monate
Kündigungsverzicht 24 Monate
befristet 24 Monate
Wohnen auf Zeit
```

## Example Search Prompts

### Broad Munich Search

```text
1 Zimmer Apartment Mietwohnung München [MIN_RENT] bis [MAX_WARM_RENT] Euro bis [MAX_SIZE] qm Baujahr ab [MIN_BUILD_YEAR] U-Bahn S-Bahn Nähe [TARGET_NEIGHBORHOODS] eigene Wohnung
```

### Location-Focused Search

```text
1 Zimmer Apartment München [TARGET_NEIGHBORHOODS] [MIN_RENT] [MAX_WARM_RENT] Euro U-Bahn Nähe S-Bahn Nähe eigene Wohnung
```

### Commute-Anchor-Focused Search

```text
Apartment München nahe [COMMUTE_ANCHOR_AREA] [RELEVANT_NEIGHBORHOODS] [RELEVANT_LINES] 1 Zimmer bis [MAX_WARM_RENT] Euro eigene Wohnung
```

## Listing Scoring Checklist

For every listing, score it against:

| Criterion | Target |
|---|---|
| Private apartment | must have |
| Not student-only | must have |
| Not WG | must have |
| Not Tauschwohnung | must have |
| No 24-month lock-in | must have |
| Warm rent | ideally within user's comfortable range; max is user's hard maximum |
| Commute to main anchor | usually <30 min door-to-door, unless user sets another threshold |
| Station walking time | <10 min, ideally <7 min |
| Public transport | U-Bahn/S-Bahn preferred |
| Future job flexibility | not too far outside Munich |
| Supermarket | <10–12 min walking |
| Internet | Glasfaser/cable/strong DSL check |
| Building condition | modern / renovated preferred |
| Gym/sauna | bonus |

## Decision Logic

Reject immediately if a listing violates any hard exclusion filter.

If it passes hard filters, prioritize in this order:

1. Private apartment and contract suitability
2. Location and transport optionality
3. Commute to the user's main anchor
4. Warm rent
5. Supermarket access
6. Internet quality
7. Building condition
8. Gym / sauna access

Important principle:

Do not choose a bad contract or bad location just because the rent is slightly lower.
