---
name: define-domain-language
license: MIT
description: >
  Use when a Ruby feature, bug, or architecture discussion has fuzzy
  business terminology and you need shared vocabulary. Identifies canonical terms,
  resolves naming conflicts, maps synonyms to one concept, and generates a glossary
  for Ruby-first workflows. Trigger words: DDD, shared vocabulary, define terms,
  bounded context naming, what should we call this, terminology alignment, DDD glossary,
  naming inconsistency.
metadata:
  version: 1.0.0
  user-invocable: "true"
  origin: "Extracted from igmarin/rails-agent-skills v5.1.17"
---
# Define Domain Language


## Quick Reference

| Topic | Rule |
|-------|------|
| Canonical term | Pick one business term for one concept |
| Synonyms | Capture them, then choose one preferred term |
| Overloaded words | Flag them early; split meanings explicitly |
| Naming | Prefer business meaning over technical shorthand |
| Output | Return a usable glossary, not abstract theory |

## HARD-GATE

```text
DO NOT introduce DDD terminology without grounding it in the user's real domain language.
DO NOT rename code concepts until the glossary is explicit enough to justify the change.
ALWAYS flag overloaded or conflicting terms before recommending modeling changes.
```

## Core Process

**Core principle:** Agree on business language before choosing models, services, or boundaries.

### Process

1. **Collect terms:** Pull candidate nouns, roles, states, events, and actions from the request, PRD, tickets, existing docs, and code names. Scan class and file names across layers:
   ```bash
   grep -rh "^class \|^module " lib/ app/ --include="*.rb" | sort
   ```
2. **Group synonyms:** Identify words that appear to mean the same thing and words that are overloaded across multiple meanings.
3. **Choose canonical terms:** Prefer the clearest business term; keep aliases only as migration notes or search hints.
4. **Define each term:** Write one short definition, expected invariants, and related concepts.
5. **Flag ambiguity:** List terms that need user confirmation or that likely indicate multiple bounded contexts.
6. **Hand off:** Refer to the Integration table below to select the appropriate next skill based on what the glossary reveals.

### Inline Example: Resolving Customer vs. Client vs. Account

The codebase uses `Customer`, `Client`, and `Account` interchangeably. After collecting usages:

- **Customer** — person who places an order (Sales context). Canonical term chosen.
- **Client** — alias used in legacy billing code; map to `Customer` with a migration note.
- **Account** — overloaded: means login credentials in Auth context *and* billing record in Finance context. Flag as two distinct concepts requiring a bounded-context split.

Result: one canonical term (`Customer`) replaces two aliases, and one overloaded term (`Account`) is split before any model changes are made.

## Output Style

When using this skill, return:

1. **Glossary details**:
   - Canonical term
   - Aliases / conflicting words
   - Definition
   - Key invariant or business rule
   - Likely related context
   - Open questions
2. **Example structure**:
   | Canonical term | Aliases | Definition | Invariant | Context |
   |----------------|---------|------------|-----------|----------|
   | Shipment | Parcel, Package | Physical goods sent to a customer address | Must reference a valid Order | Fulfillment |
3. **Language**: Must be in English unless explicitly requested otherwise.

## Extended Resources

Load only when the task needs examples or a reusable glossary schema:

- [EXAMPLES.md](./EXAMPLES.md) — Naming-inconsistency example and resolved glossary.
- [assets/examples.md](./assets/examples.md) — JSON glossary entry example.
- [assets/glossary_schema.json](./assets/glossary_schema.json) — Optional schema for persisted glossary entries.

## Integration

| Skill | When to chain |
|-------|---------------|
| **review-domain-boundaries** | When the glossary suggests multiple bounded contexts or language leakage |
| **model-domain** | When the terms are clear enough to decide entities, value objects, and services |
