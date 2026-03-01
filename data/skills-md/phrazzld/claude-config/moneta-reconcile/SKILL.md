---
name: moneta-reconcile
description: |
  Verify accounting integrity. Compare totals to source docs, check lots vs holdings, detect duplicates, report gaps.
user-invocable: true
effort: high
---

# /moneta-reconcile

Verify Moneta accounting integrity.

## Steps

1. Load source docs from `source/` and parsed outputs from `normalized/`.
2. Compare per-source transaction counts and totals to originals.
3. Reconcile lots to holdings: sum lots per asset vs `normalized/cost-basis.json` and `normalized/cost-basis-updated.json`.
4. Detect duplicate transactions by `id`, date+amount+source, and cross-file overlaps.
5. Report discrepancies with file path, record id, and delta.

## Examples

```bash
# Refresh normalized data before reconciling
pnpm parse:all
```

```bash
# Rebuild gains before lot checks
pnpm gains
```

## References

- `source/`
- `normalized/transactions.json`
- `normalized/bofa-transactions.json`
- `normalized/river-transactions.json`
- `normalized/strike-transactions.json`
- `normalized/cashapp-transactions.json`
- `normalized/robinhood-transactions.json`
- `normalized/cost-basis.json`
- `normalized/cost-basis-updated.json`
- `normalized/river-lots.json`
- `normalized/strike-lots.json`
- `normalized/robinhood-lots.json`
- `scripts/parse-all.ts`
- `scripts/schema.ts`
