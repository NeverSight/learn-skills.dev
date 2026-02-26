---
name: jgi-lakehouse
description: Query JGI Lakehouse (Dremio) for genomics metadata across GOLD/IMG/Mycocosm/Phytozome and download genome files via IMG taxon OIDs.
---

# JGI Lakehouse

Use JGI Lakehouse (Dremio) for metadata queries and the JGI filesystem for sequence downloads.

## Instructions

1. Authenticate to Dremio using a PAT.
2. Explore schemas and tables to find the required metadata.
3. Run SQL queries for project/sample/taxon discovery.
4. Use IMG taxon OIDs to fetch genome packages from the filesystem.
5. Validate outputs and record provenance.

## Quick Reference

| Task | Action |
|------|--------|
| Auth setup | See `docs/authentication.md` |
| SQL cheatsheet | See `docs/sql-quick-reference.md` |
| Table catalog | See `docs/data-catalog.md` |
| GOLD exploration | See `docs/explore_gold.md` |

## Input Requirements

- DREMIO_PAT token (for Lakehouse access)
- Query intent (taxonomy, ecosystem, project IDs, etc.)
- JGI filesystem access for downloads

## Output

- Query results (tables or CSVs)
- Lists of taxon OIDs or accessions
- Downloaded genome packages (FNA/FAA/GFF)

## Quality Gates

- [ ] SQL queries return expected row counts
- [ ] Taxon OIDs map to existing filesystem packages
- [ ] Downloaded files pass basic integrity checks

## Examples

### Example 1: Basic GOLD query

```sql
SELECT gold_id, project_name
FROM "gold-db-2 postgresql".gold.project
WHERE is_public = 'Yes'
LIMIT 5;
```

## Troubleshooting

**Issue**: Authentication failures
**Solution**: Re-create the PAT and confirm it is exported before querying.

**Issue**: Missing genome files
**Solution**: Verify IMG taxon OIDs and filesystem path permissions.
