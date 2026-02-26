---
name: tracking-taxonomy-updates
description: Track and reconcile taxonomy updates across NCBI, GTDB, ICTV, and community eukaryote frameworks with versioned provenance.
---

# Tracking Taxonomy Updates

Use authoritative sources to report taxonomy changes with explicit versions, dates, and provenance.

## Instructions

1. Determine scope (domain, timeframe, output type).
2. Pull authoritative updates and release notes.
3. Extract versioned changes and impacts.
4. If assigning taxonomy, run domain-appropriate tools and normalize IDs.
5. Deliver a versioned report with conflicts flagged.

## Quick Reference

| Task | Action |
|------|--------|
| Sources | See `reference/sources.md` |
| Tools | See `reference/tools.md` |
| IDs/ranks | See `reference/ranks-and-identifiers.md` |
| Report template | See `reference/report-template.md` |
| QA checklist | See `reference/qa-checklist.md` |
| Environment | See `env/README.md` |

## Input Requirements

- Domain(s) and timeframe
- Source systems to compare (NCBI/GTDB/ICTV/etc.)
- Sequences or genomes (for assignment workflows)

## Output

- Versioned taxonomy update summary
- Conflict report across sources
- Standardized taxonomy assignment table (when applicable)

## Quality Gates

- [ ] Every “latest” claim includes date, version, and authority
- [ ] Stable identifiers used for joins (taxids, GTDB IDs)
- [ ] Provenance captured (tool version, DB release, run date)

## Examples

### Example 1: Update scan scope

```text
Domains: Bacteria + Archaea
Timeframe: last 12 months
Output: summary table + pipeline impact notes
```

## Troubleshooting

**Issue**: Conflicting taxonomy between sources
**Solution**: Report both with explicit conflict flags and provenance.

**Issue**: Missing stable IDs
**Solution**: Resolve via TaxonKit and capture merged/deleted taxid warnings.
