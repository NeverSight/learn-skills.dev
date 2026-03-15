---
name: migrating-code
description: Safe code migrations with backward compatibility and reversibility. Use when upgrading dependencies, changing database schemas, API versioning, or transitioning between technologies.
---

# Migrating Code

## Core Principles

1. **Never break production** - Backward compatible until fully rolled out
2. **Small, reversible steps** - Each step independently deployable
3. **Test at every stage** - Before, during, and after
4. **Have rollback ready** - Always

## Migration Checklist

```
- [ ] Pre-Migration: Read changelog, identify breaking changes, ensure test coverage
- [ ] During: Small steps, test each, monitor errors, rollback ready
- [ ] Post: Verify tests, check metrics, remove scaffolding, update docs
```

## Database Schema

### Safe Patterns

| Operation | Pattern |
|-----------|---------|
| Add column | Add nullable first → backfill → add constraints |
| Remove column | Stop writes → deploy code that doesn't read → drop column |
| Rename column | Add new → dual-write → backfill → switch reads → drop old |
| Change type | New column → dual-write → migrate in batches → switch → drop |

**Never:** Add NOT NULL without defaults to tables with data.

## API Migrations

### Deprecation Process

1. Add deprecation warnings to old endpoints
2. Document migration path
3. Set and communicate sunset date
4. Monitor usage
5. Remove after usage drops

```json
{
  "data": {},
  "_warnings": [{
    "code": "DEPRECATED_ENDPOINT",
    "message": "Use /api/v2/users instead",
    "sunset": "2025-06-01"
  }]
}
```

## Framework Upgrades

1. **Upgrade to latest minor first** - Get deprecation warnings
2. **Fix warnings** - Before major upgrade
3. **One major at a time** - Don't batch
4. **Test after each step**

### Adapter Pattern for Library Swaps

```typescript
// Wrap library usage
// lib/date.ts
import moment from 'moment';
export const formatDate = (date: Date, format: string) =>
  moment(date).format(format);

// Migration: just change the adapter
import { format } from 'date-fns';
export const formatDate = (date: Date, fmt: string) =>
  format(date, fmt);
```

## Gradual Rollout

Use feature flags:
```typescript
if (featureFlags.useNewSystem) {
  return newService.process(order);
} else {
  return legacyService.process(order);
}
```

Roll out: 1% → 10% → 50% → 100% → remove flag

## Common Pitfalls

**Avoid:**
- Big bang migrations
- No rollback plans
- Skipping dual-write phase
- Single large data transactions
- Removing old code before new is proven

**Do:**
- Small, reversible steps
- Test rollback procedures
- Batch large data migrations
- Keep old paths until new verified
