---
name: data-freshness-check
description: "Systematic verification of data accuracy and freshness during web research. Use when gathering factual data about organizations, legal entities, statistics, regulations, or any factual claims. Ensures every fact is sourced, timestamped, and cross-referenced. Triggers on: researching organizations, verifying legal/fiscal data, compiling dossiers, auditing existing data, any task involving factual claims from web sources."
---

# Data Freshness & Accuracy Check

## When to Activate

This skill activates automatically when:
- Researching any organization, company, or association (legal data, financials, governance)
- Gathering factual data from the web (statistics, regulations, dates, amounts, addresses)
- Compiling dossiers or reference files with factual claims
- Auditing or updating existing data files
- Any task where the user asks to "verify", "check", "update", or "confirm" data

## 5-Step Verification Protocol

### Step 1 — Identify Claims
List every factual data point being used or produced:
- Legal identifiers (SIREN, SIRET, RNA, RCS, VAT numbers)
- Names (legal names, trade names, directors, officers)
- Dates (creation, modification, deadlines, events)
- Addresses (registered office, branches, contact info)
- Amounts (budgets, revenues, grant amounts, thresholds)
- Statuses (legal form, tax status, certifications, labels)
- Statistics (number of employees, beneficiaries, members)
- Regulations (laws, articles, decrees — check if still in force)

### Step 2 — Map to Authoritative Sources
For each data type, identify THE authoritative source:

**Source Authority Hierarchy** (highest to lowest reliability):

| Priority | Source Type | Examples | Trust Level |
|:---:|---|---|:---:|
| 1 | Official registries | RNA (journal-officiel.gouv.fr), SIRENE (annuaire-entreprises.data.gouv.fr), RCS (infogreffe.fr), BODACC | ★★★★★ |
| 2 | Government websites | .gouv.fr, EUR-Lex, Légifrance, service-public.fr | ★★★★★ |
| 3 | Entity's own official site | Corporate/association website, annual reports | ★★★★☆ |
| 4 | Recognized databases | OpenCorporates, Societe.com, CompanyCheck | ★★★☆☆ |
| 5 | Dated press articles | Major newspapers, trade publications with dates | ★★★☆☆ |
| 6 | Undated third-party content | Blogs, directories, aggregators | ★★☆☆☆ |
| 7 | AI training data / memory | Previously known facts without fresh verification | ★☆☆☆☆ |

**NEVER treat Priority 7 (AI memory) as verified data.** Always fetch from Priority 1-3 sources.

### Step 3 — Fetch & Cross-Reference
- Verify each fact on ≥2 independent sources when possible
- Prioritize Priority 1-2 sources over all others
- When sources disagree, flag the discrepancy with `⚡ ÉCART` and note both values
- Record the exact URL where each fact was found (not just the domain)

### Step 4 — Timestamp & Status
Assign to each data point:
- `date_verified`: ISO date (YYYY-MM-DD) of when you actually checked
- `source_url`: exact URL
- `freshness_status`:

| Status | Age | Meaning |
|---|---|---|
| 🟢 FRESH | < 3 months | Recently verified, high confidence |
| 🟡 AGING | 3-12 months | Likely still accurate, monitor |
| 🟠 STALE | > 12 months | May have changed, re-verify before use |
| 🔴 EXPIRED | > 24 months | Unreliable, must re-verify |
| ⚪ UNVERIFIED | N/A | Not yet checked against authoritative source |

### Step 5 — Report
Produce a verification table in this exact format:

```markdown
| Donnée | Valeur | Source | URL | Vérifié le | Fraîcheur |
|---|---|---|---|---|---|
| Nom légal | Association XYZ | RNA | https://... | 2026-02-12 | 🟢 FRESH |
```

## Freshness Thresholds by Data Type

| Data Type | Max Acceptable Age | Recheck Frequency |
|---|---|---|
| Legal identifiers (SIREN, RNA) | 12 months | Annual |
| Registered address | 6 months | Semi-annual |
| Directors / Officers | 6 months | Semi-annual |
| Financial data (revenue, budget) | 6 months | Per fiscal year |
| Employee count | 12 months | Annual |
| Contact info (phone, email) | 3 months | Quarterly |
| Regulations / Laws | Verify if amended | Before each use |
| Grant deadlines / AAP dates | 1 month | Monthly |
| Statistics / Impact numbers | 12 months | Annual |
| Prices / Rates / Thresholds | 6 months | Semi-annual |

## Failure Modes & Flags

Use these flags in output when issues are found:

- `✅ CONFIRMÉ` — Verified on authoritative source, fresh
- `⚠️ À VÉRIFIER` — Single source only, or non-authoritative source
- `❌ PÉRIMÉ` — Data older than acceptable threshold, needs refresh
- `🔍 NON TROUVÉ` — Data not found on any authoritative source
- `⚡ ÉCART` — Different values found across sources (list both)
- `🆕 MISE À JOUR` — Data has changed since last known value

## Mandatory Rules

1. **NEVER present unverified data as fact.** If unverified, mark it `⚪ UNVERIFIED`.
2. **NEVER invent data.** Prefer "donnée non disponible" over fabrication.
3. **ALWAYS include the exact URL** of each source (not just the website name).
4. **ALWAYS timestamp** each verification in ISO format (YYYY-MM-DD).
5. **When updating existing files**, produce a diff showing what changed and why.
6. **When sources conflict**, present BOTH values and recommend which to use based on source authority.
7. **For legal/regulatory data**, always check Légifrance for the currently in-force version.
8. **For French associations**, the minimum verification set is: RNA status, SIREN active status, registered address, current directors, last published accounts.

## Integration Notes

This skill complements other research skills. It does not replace domain-specific knowledge — it ensures the **factual foundation** is solid before domain reasoning begins.

When activated alongside other skills, this skill's verification protocol runs FIRST (gather and verify facts), then domain skills apply their reasoning on verified data.
