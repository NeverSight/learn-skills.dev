---
name: clean-data
description: "Data cleaning, entity matching, and deduplication skill for Claude Code and Codex: triage, standardize, and validate a CSV, Excel, or JSON list of B2B companies or contacts before enrichment. Normalizes company names and domains, validates emails and phone numbers, matches and deduplicates records, and tags invalid rows non-destructively. Run before enrichment or CRM import to avoid paying for noisy records. Use for CRM enrichment prep, company name and website matching, entity matching, and contact deduplication. Works in Claude Code, Codex, and n8n via MCP."
---

# Clean Data

Per-row cleanup on a GTM list before any match or enrich call. Profile, standardize, validate. Never destructive: raw input is preserved, invalid rows are tagged with reason codes rather than deleted. Out of scope: deduplication and canonical entity resolution.

## Input

`$ARGUMENTS` is a path to a CSV, Excel, or JSON file. Parse the user message for optional sub-inputs:

- Schema hints if column names are ambiguous: which column is company name, domain, email, phone, country.
- Entity type: companies, contacts, or both. Default: infer from columns.
- Whether to run an MX-record check on email domains (slower, requires DNS). Default: off.
- Whether to produce a match-ready subset for downstream entity resolution. Default: no.

Example phrasings:

- "Clean this leads CSV before I import it to HubSpot."
- "Normalize the company names and domains in /path/accounts.xlsx."
- "Validate the emails in this file and tag the bad rows."
- "Prep this list for prospect matching, only keep contactable corporate rows."
- "Why does my country column have 200 different spellings."

## Workflow

1. **Copy raw input.** Before any transform, copy the input to `./00_raw/<filename>` and never write back. All transforms write to numbered phase folders: `01_profiled/`, `02_standardized/`, `03_validated/`. The single most common failure mode in cleanup work is destructive transforms with no path back.

2. **Profile the file.** Compute fill rate, cardinality, top values, length distribution, and format-pattern frequency for every column. Save the snapshot. Read it before deciding what to clean.

   ```python
   import pandas as pd
   df = pd.read_csv(input_path)
   profile = pd.DataFrame({
       "fill_rate_pct": (df.notna().mean() * 100).round(1),
       "cardinality": df.nunique(),
       "top_value": df.apply(lambda c: c.dropna().astype(str).mode().iloc[0] if c.dropna().size else None),
       "avg_len": df.apply(lambda c: c.dropna().astype(str).str.len().mean()),
   })
   ```

   Things to look for: country columns with 200+ distinct values (standardization problem, build ISO Alpha-2 lookup); phone columns where under 50% parse as E.164 (need country hint); company-name 99th-percentile length above 100 chars (pasted addresses, quarantine); free-email providers in the top 5 of email column (decide policy now); fields under 10% fill (probably not worth normalizing); literal strings `"NA"`, `"N/A"`, `"None"`, `"null"`, `"-"` (collapse to real nulls before validating).

3. **Standardize string fields.** Run standardization BEFORE validation: a valid email like ` JOHN@ACME.COM ` fails naive regex without trim+lowercase first. For every string column do Unicode NFKC, trim, collapse internal whitespace, strip leading and trailing punctuation, collapse null-token strings to real nulls. Then field-specific:

   - **Company name.** Strip legal suffixes (`Inc`, `LLC`, `Ltd`, `GmbH`, `S.A.`, `株式会社`) at end of string only. Use `cleanco` if available. Keep BOTH raw and normalized columns.
   - **Domain.** Strip protocol and `www`. Fold to the eTLD+1 via `tldextract`. Flag free-email providers and disposable domains separately.
   - **Person name.** Parse with `nameparser`: honorifics, generational suffixes, credentials, particles. If confidence is low, store the raw string with a low-confidence flag.
   - **Phone.** Format to E.164 with `phonenumbers`. Hint country from the country column when available.
   - **Country.** Map free-text to ISO Alpha-2 codes (`United States` to `US`, `UK` to `GB`, `Deutschland` to `DE`). Reusable downstream for country filters.
   - **Address.** Use `libpostal` if installed. Country-aware parsing.

   Common mistake: overwriting the display column with the normalized version. Always keep raw alongside normalized.

4. **Validate field-by-field.** Per field, add a boolean `<field>_valid` and a `<field>_reason` text column when invalid. Tag invalid rows; never delete them.

   - **Emails:** RFC 5322 syntax via `email-validator`; role-address detection (`info@`, `sales@`, `noreply@`, `support@`, `hello@`); disposable-domain check; free-provider flag (`gmail`, `yahoo`, `qq`); optional MX-record check (off by default).
   - **Phones:** parse + format via `phonenumbers`. Tag `invalid_too_short`, `invalid_country`, `invalid_format`.
   - **Domains:** valid eTLD, no IP literals, optional MX check.
   - **Country codes:** valid ISO Alpha-2 after normalization.

5. **Hand off to entity resolution (optional).** This skill cleans rows in isolation; it cannot tell you that `Starbucks EMEA` and `Starbucks Corporation` point to the same company. If the user wants the handoff, produce a match-ready subset and route rows by available signal:

   - Rows with normalized company name + domain: route to **match a business** (name + website, falls back to domain-only on mismatch).
   - Rows with a corporate (not role / free-provider / disposable) email: route to **match a prospect** via email.
   - Rows with parsed person name + company name: route to **match a prospect** via name + company.
   - Rows with a validated LinkedIn URL: route to **match a prospect** via LinkedIn.

   Filter out tagged-invalid rows before the handoff so you do not spend credits matching `noreply@example.com` or disposable addresses. The returned IDs become the join keys for any later **enrich a business** or **enrich a prospect** call.

## Output Format

### Profile Snapshot
Per column: `fill_rate_pct`, `cardinality`, `top_value`, `avg_len`. Markdown table. After cleanup, re-run the profile and show before vs after on touched columns.

### Standardization Map
Per normalized field: raw column name, normalized column name, 3 to 5 example transformations (`"  ACME, Inc. "` to `acme`, `"WWW.Acme.COM"` to `acme.com`, `"+1 (415) 555 1212"` to `+14155551212`).

### Validation Verdict
Per validated field: counts of valid, invalid, risky. Frequency table of reason codes (e.g. `role_address: 42`, `disposable_domain: 18`, `invalid_syntax: 6`).

### Cleaned File
A single CSV at `./03_validated/<input_name>_clean.csv` with all original columns plus `<field>_norm`, `<field>_valid`, and `<field>_reason` columns.

### Match-Ready Subset (only if requested)
A second CSV at `./04_match_ready/<input_name>_for_match.csv` containing only rows that passed validation, plus a one-line summary of which match path each row subset should route to (count by path).

## Limitations

- Does NOT deduplicate or resolve to canonical entities. Two normalized strings can still refer to the same real-world business. Hand off to a match step for that.
- Person-name parsing is best-effort. Non-Western order, hyphenated families, and missing separators are flagged with a low-confidence marker; raw string is always preserved.
- The MX-record check requires DNS and adds 50 to 200ms per unique domain. Off by default.
- Free-email providers (gmail, yahoo) are flagged but cannot be linked to a corporate identity from this skill alone. Pair with a prospect match (email + company) when needed.
- Holding-company and subsidiary pitfalls are out of scope (`meta.com` vs `instagram.com` vs `whatsapp.com`). Resolve via company-hierarchies enrichment after matching.
- If the input lacks a country column entirely, phone normalization defaults to a permissive parser and may mis-format short numbers. Provide a default country in the user message when possible.
