---
name: type-system
description: Use when analyzing types, reviewing type safety, or strengthening the type system. Scans for 7 categories of type weakness and produces concrete before/after fixes.
---

# Type System Opportunity Analyzer

Analyze code for type system weaknesses. Produce concrete before/after transformations.

## When to Use

- Reviewing or creating TypeScript types/interfaces
- Before or after refactoring domain models
- Code review where type safety matters
- User asks to "strengthen types", "improve type safety", or "find type issues"

## Scan Categories (Priority Order)

### 1. Impossible States
Optional fields that are only valid in certain states. Fix with **discriminated unions**.

```typescript
// BAD: commentId exists on LIKE_ON_POST — impossible but representable
interface Notification { type: NotificationType; commentId?: string }

// GOOD: compiler enforces which fields exist per type
type Notification = CommentNotification | LikeNotification;
```

### 2. Trust Boundary Violations
Mappers returning `Record<string, unknown>` or `any`. Fix with **typed interfaces**.

```typescript
// BAD: typo in column name compiles fine, fails silently at runtime
function mapUser(data: Partial<User>): Record<string, unknown> { ... }

// GOOD: typo is a compile error
function mapUser(data: Partial<User>): SupabaseUserUpdate { ... }
```

### 3. Unvalidated Data Flow
`as any` casts on API response data. Fix with **explicit join row types** and **runtime guards** (not non-null assertions).

```typescript
// BAD: silent cast hides structural mismatch
const post = row as any;

// GOOD: typed join row + runtime guard at trust boundary
interface PostJoinFields { board_title: string | null; ... }
if (!row.commentId) throw new Error(`Missing commentId for ${row.id}`);
```

### 4. Primitive Obsession — IDs
Multiple `string` params that are different entity IDs. Fix with **branded types** (only where argument-swapping bugs are likely).

```typescript
// BAD: silently swapped
function block(blockerId: string, blockedId: string) { ... }

// GOOD: compile error on swap (use sparingly — ergonomic cost is real)
type UserId = string & { readonly __brand: 'UserId' };
```

### 5. Repeated Inline Types
Same shape defined in 3+ places. Fix with **shared type extraction**.

```typescript
// BAD: { userId: string; userName: string; userProfileImage: string } in 5 files
// GOOD: import type { UserSummary } from '@/shared/model/UserSummary';
```

### 6. Missing API Contracts
Inline anonymous return types on API/mapper functions. Fix with **named DTO interfaces**.

```typescript
// BAD: return type is inferred anonymous object
function fetchNotifications() { return rows.map(r => ({ id: r.id, ... })); }

// GOOD: named DTO separates DB shape from domain model
interface NotificationDTO { id: string; type: NotificationType; ... }
```

### 7. Optional Fields That Are Always Present
Fields marked `?` that mappers always provide. Fix by **removing the `?`**.

```typescript
// BAD: createdAt?: Timestamp — but every mapper always sets it
// GOOD: createdAt: Timestamp — consumers don't need unnecessary null checks
```

## Output Format

For each finding:
```
### [Category] — [Short Description]
**Problem:** What's wrong and what bugs it allows.
**Location:** file:line
**Before:** current code
**After:** improved code
**Effort:** Low / Medium / High
```

## Testing Guidance

- **DO** test mapper behavior (input row -> output shape, defaults, edge cases)
- **DON'T** use `expectTypeOf` tests — they test the compiler, not your code
- **DO** use `@ts-expect-error` to verify that invalid shapes are rejected
- **DO** use runtime guards (`if (!field) throw`) at trust boundaries instead of `!` assertions

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Branded IDs on every `string` | Noise without value for non-ID strings | Only brand entity IDs that appear as swappable function params |
| Discriminated union for 2-state boolean | Overkill for `isRead: boolean` | Only use for 3+ states or correlated optional fields |
| Typing Supabase rows to match TS model | Hides the mapping layer; DB schema != domain model | Type the DB row shape separately (DTO), map explicitly |
| Making all fields required | Breaks construction sites that build objects incrementally | Only require fields that are always present after the primary mapper |
| Non-null assertions at trust boundaries | Hides missing data bugs at runtime | Use runtime guards that throw descriptive errors |
| `expectTypeOf` tests | Tests the compiler, not your code; provides no regression safety | Test mapper behavior with real inputs and assertions |
