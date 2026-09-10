---
name: jinko-task-trial-data-scoping
description: >-
  Find and shortlist ClinicalTrials.gov registry and posted-results records for
  biomedical modeling evidence. Use for NCT discovery, status/phase/results
  screening, endpoint and population inventory, comparator landscapes, and
  ongoing-trial intelligence. Do not use for PubMed publication discovery,
  quantitative extraction, protocol authoring, Jinkō trial execution,
  calibration, model building, or systematic reviews.
compatibility: Requires network access. ClinicalTrials.gov v2 needs no credentials.
metadata:
  author: Nova In Silico
license: MIT
---

# Clinical Trial Data Scoping

Produce a registry candidate inventory, not extracted endpoint data. A registered
outcome is not evidence that numeric results were posted.

## Frame

Establish the condition, intervention or mechanism class, population, comparator,
and purpose: endpoint availability, control-arm or natural-history evidence,
dose/regimen context, safety, or development-landscape intelligence. Confirm any
required status, phase, study type, posted-results requirement, and shortlist
size. Do not impose a status filter silently.

Reuse the Entity Table from `jinko-task-literature-search` when available;
otherwise build `canonical_name`, `synonyms`, `mesh_term`, `related_entities`,
`intent_groups` (`Data`), and `exclusions`. Confirm consequential aliases and
filters before network calls.

## Search

1. Build distinct ClinicalTrials.gov angles from the relevant facets:
   intervention aliases, condition aliases, mechanism class, comparator or
   standard of care, and population/outcome. Prefer precise terms over one broad
   query.
2. Run `scripts/clinical_trials.py` once per angle with separate output files.
   Use `--status`, `--phase`, and `--require-results` only when required by the
   approved frame. The script owns API filtering, raw-response persistence, and
   normalized registry fields.
3. Run `scripts/compile_trials.py` over the angle outputs. It deduplicates by NCT
   ID, preserves query provenance, and ranks by angle count, posted-results
   availability, and record completeness.

This is one search pass. Broader mechanism, sponsor, country, site, or comparator
queries are separate user-approved follow-ups.

## Shortlist

Inspect each retained record against the stated purpose. Distinguish:

- registry-only design or recruitment metadata;
- posted ClinicalTrials.gov results;
- a publication linked to an NCT identifier.

Set `verification_passed` only when the record contains purpose-relevant signals,
such as a matching population/intervention, specified outcome and timeframe,
enrollment and eligibility, appropriate design, or the required results modules.
State the observed signals in `verification_note`; do not infer numeric endpoint
availability from `hasResults` alone.

Complete the fields in `assets/shortlist-schema.json` and run
`scripts/validate_shortlist.py` before presenting `shortlist.json`. Trial records
use `intent_group = Data`, an appropriate registry/results `evidence_type`, and
`nct_id` as their primary identifier.

When associated publications are needed, pass selected NCT IDs to
`jinko-task-literature-search` as `<NCT_ID>[si]` angles. Use
`jinko-task-extract-data-table` only after a quantitative source has been
identified and inspected.

## Artifacts

- `frame.json`: approved scope, Entity Table, filters, and angle definitions;
- per-angle normalized JSON, raw API JSON, and table JSON;
- `merged_trials.json`: deterministic cross-angle candidate pool;
- `shortlist.json`: schema-valid prioritized candidates.

Present a concise Markdown view with NCT link, title, phase/status, results
availability, population, interventions, primary outcomes, and priority rationale.
Clearly separate scoped candidates from analysis-ready data.
