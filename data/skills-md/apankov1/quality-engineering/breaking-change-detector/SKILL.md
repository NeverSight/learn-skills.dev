---
name: breaking-change-detector
description: "Detect breaking changes across 6 categories: contracts, database schemas, RPC endpoints, WebSocket protocols, serialized state, and event sourcing."
---

# Breaking Change Detector

Detects breaking changes that could disrupt active sessions or lose client compatibility across 6 categories.

**When to use**: Modifying shared contract/interface packages, changing database schema or migrations, RPC/API endpoint signature changes, WebSocket message format changes, serialized state schema changes, before merging any contract/schema changes.

**When not to use**: Adding new optional fields (non-breaking), internal refactoring without API changes, documentation or test-only changes.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Nobody uses the old format" | Active sessions and stored data use the old format right now | Check backward compatibility |
| "We'll fix the clients" | Clients update on their own schedule, not yours | Keep old format supported |
| "It's just a rename" | A rename IS a removal + addition -- all consumers need updating | Deprecate, don't rename |
| "The migration handles it" | Migrations run once; replay/recovery may encounter old data indefinitely | Use tolerant reader pattern |

---

## Included Utilities

```typescript
// Breaking change classification (zero dependencies)
import { classifyFieldChange, classifySerializedSchema, classifyEventTypeChanges } from './breaking-change.ts';
```

## Backward Compatibility Checklist

When modifying contracts or schemas:
- [ ] All existing fields preserved (or deprecated with fallback)
- [ ] New fields are optional or have `.catch()` defaults
- [ ] Type changes are widening only
- [ ] Database migration handles existing data
- [ ] Old event formats still supported for replay
- [ ] WebSocket protocol versioned
- [ ] API endpoints maintain compatibility
- [ ] Tests validate old data still deserializes correctly
- [ ] Serialized state schemas use `.catch()` for all fields
- [ ] `fromJSON()` methods use `safeParse()` with graceful fallback

## Violation Rules

| Slug | Rule | Severity |
|------|------|----------|
| `contract_field_removal` | Removed/renamed fields in shared interfaces | must-fail |
| `schema_without_catch` | Serialized schema fields missing `.catch()` default | must-fail |
| `strict_parse_in_deserialize` | Using `.parse()` instead of `.safeParse()` in fromJSON | must-fail |
| `migration_drops_column` | Column removal without data migration | must-fail |
| `endpoint_removed` | API endpoint removed without deprecation period | must-fail |
| `event_type_renamed` | Event type name changed (incompatible with replay) | must-fail |

## Coverage

| Category | Utility | Status |
|----------|---------|--------|
| 1. Contract fields | `classifyFieldChange()` | Code + tests |
| 2. Database schema | -- | Doc-only (requires SQL diffing) |
| 3. RPC/API endpoints | -- | Doc-only (requires OpenAPI diffing) |
| 4. WebSocket protocol | -- | Doc-only (requires message schema diffing) |
| 5. Serialized state | `classifySerializedSchema()` | Code + tests |
| 6. Event sourcing | `classifyEventTypeChanges()` | Code + tests |

Categories 2-4 require static analysis of SQL migrations, OpenAPI specs, or protocol schemas -- tools beyond the scope of a pure-function utility. See [categories.md](./references/categories.md) for detection commands and safe patterns.

## Output Format

```markdown
## CRITICAL -- Will Disrupt Active Sessions

### Contract: Removed UserState.score field
**File**: src/contracts/types.ts:42
**Impact**: Active sessions fail on state load
**Fix**: Deprecate instead:
  /** @deprecated Use points instead */
  score?: number;
  points: number;

## WARNING -- Migration Required

### Database: Renamed column without migration
**File**: migrations/0036_rename_field.sql:5
**Impact**: Existing rows have NULL values
**Fix**: Add data migration step

## SAFE Changes

- Added optional field `UserState.metadata`
- New API endpoint `orders.archive`
- Widened type `Status: 'active' | 'paused'` to include `'archived'`
```

## Framework Adaptation

This skill applies to any system with shared contracts/interfaces, persistent state, event sourcing, real-time protocols, or RPC/API layers with independent client release cycles.

See [categories.md](./references/categories.md) for detailed detection patterns, code examples, and safe alternatives for each of the 6 categories.
