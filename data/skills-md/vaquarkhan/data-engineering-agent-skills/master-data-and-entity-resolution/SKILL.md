---
name: master-data-and-entity-resolution
description: Guides agents through master data and entity resolution workflows. Use when matching identities across systems, defining canonical entities, resolving duplicates, or building golden records for shared downstream use.
---

# Master Data And Entity Resolution

## Overview

Use this skill when the data problem is "who or what is this really?" across multiple systems. It helps agents define canonical entities, matching logic, survivorship rules, and downstream-safe resolution behavior.

## When to Use

- building customer, product, or account golden records
- resolving duplicate identities across systems
- defining master data domains
- publishing canonical reference datasets

Do not collapse entity resolution into ad hoc joins if the result becomes a shared dependency.

## Workflow

1. Define the entity contract.
   Include:
   - canonical entity type
   - contributing systems
   - primary identifiers
   - confidence or match logic
   - ownership

2. Choose the matching strategy.
   Common strategies:
   - exact key match
   - deterministic rule-based match
   - probabilistic or scored match

3. Define survivorship rules.
   Decide which system wins for each attribute and under what conditions.

4. Track unresolved and ambiguous cases.

5. Publish master data with clear confidence and lineage context.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "We can just use email as the unique customer key." | Real systems often contain shared, missing, or changing identifiers. |
| "The golden record is obvious once matched." | Attribute-level survivorship and conflict handling still need explicit rules. |
| "Ambiguous matches are edge cases." | They become painful quickly when downstream systems treat them as truth. |

## Red Flags

- no explicit canonical entity definition exists
- survivorship logic is implicit in SQL ordering
- unresolved cases are silently dropped or forced
- downstream consumers are not told match confidence assumptions

## Verification

- [ ] Canonical entity and source systems are explicit
- [ ] Match and survivorship rules are documented
- [ ] Ambiguous cases have a defined handling path
- [ ] Published master data includes lineage or confidence context where needed
