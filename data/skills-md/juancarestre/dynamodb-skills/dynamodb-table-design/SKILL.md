---
name: dynamodb-table-design
description: "Designs a DynamoDB single-table structure from a documented set of access patterns. Use when the user has an access patterns .md file (from dynamodb-access-patterns skill) and wants to design partition keys, sort keys, GSIs, composite keys, and map every access pattern to a concrete DynamoDB query operation. This is Step 2 of a 3-step pipeline: access patterns -> table design -> query interfaces."
---

# DynamoDB Table Design

This skill takes a formalized access patterns document and produces a complete DynamoDB single-table design. It maps every access pattern to a concrete DynamoDB operation with explicit key conditions.

## When to Use

- The user has an access patterns `.md` file (from `dynamodb-access-patterns` or manually written)
- The user wants to design PK/SK structures for their entities
- The user wants to decide which GSIs they need
- The user wants to verify that every access pattern is covered by the table design
- The user wants to add a new entity to an existing table design

## Pipeline Position

```
  1. Access Patterns  -->  [2. Table Design]  -->  3. Query Interfaces
  (dynamodb-access-       (this skill)           (dynamodb-query-
   patterns)                                      interfaces)
```

**Input**: Access patterns `.md` file
**Output**: Table design `.md` file consumed by `dynamodb-query-interfaces`

---

## Prerequisites

Before starting, read the access patterns file. If it doesn't exist or is incomplete, tell the user to run the `dynamodb-access-patterns` skill first.

If the user already has a table in production and wants to add entities, also read their existing table design file (if any) to understand current keys and GSIs.

---

## Design Workflow

### Step 1: Read and Validate Access Patterns

Read the access patterns file and verify:

1. Every access pattern has an ID (AP-XXX)
2. Every pattern specifies input parameters and result type
3. Multi-entity patterns are explicitly marked
4. Write patterns specify transaction requirements

If anything is missing, ask the user to clarify before proceeding.

### Step 2: Group Entities into Item Collections

This is the core of single-table design. Analyze the access patterns to determine which entities should share a partition key.

**Rules for grouping:**

1. **Entities fetched together in a multi-entity read MUST share a PK.**
   - If AP-003 fetches User + Orders together, they must share a PK.

2. **1:N relationships where the parent is always known go under the parent's PK.**
   - Orders belong to a User -> `PK = USER#userId`

3. **Entities accessed only by their own ID get their own PK.**
   - A Product looked up by productId -> `PK = PRODUCT#productId`

4. **Global collections (list all, leaderboard) use a static PK.**
   - All products catalog -> `PK = PRODUCTS`

5. **N:N or deeply nested relationships use composite PKs.**
   - Items in a specific cart -> `PK = USER#userId#CART#cartId`

Present the proposed grouping to the user:

```
Based on your access patterns, here's how I'd group entities:

Item Collection 1: User scope
  PK = USER#<userId>
  Contains: User, Order, Balance, Preferences
  Supports: AP-001, AP-002, AP-003, AP-005

Item Collection 2: Product catalog
  PK = PRODUCTS
  Contains: Product (catalog entries)
  Supports: AP-006, AP-007

Item Collection 3: Product detail
  PK = PRODUCT#<productId>
  Contains: Product (full record), Review
  Supports: AP-008, AP-009, AP-010

Does this grouping make sense? Any patterns I'm missing?
```

### Step 3: Design Primary Keys

For each item type, define the PK and SK.

**Key Design Principles:**

#### Separator Convention
Use `#` as the separator between key segments. This is the universal DynamoDB convention.

```
PK = ENTITY_PREFIX#identifier
SK = ENTITY_PREFIX#identifier
```

#### PK Patterns

| Pattern | Format | Use Case |
|---|---|---|
| Entity-scoped | `ENTITY#<id>` | Self-lookup, entity owns its collection |
| Parent-scoped | `PARENT#<parentId>` | Children queried under a parent |
| Static collection | `COLLECTION_NAME` | Global lists, catalogs, leaderboards |
| Hierarchical | `PARENT#<id>#CHILD#<childId>` | Deep nesting (use sparingly) |

#### SK Patterns

| Pattern | Format | Use Case |
|---|---|---|
| Same as PK | `ENTITY#<id>` | 1:1 self-referencing record |
| Child entity | `CHILD_TYPE#<childId>` | Items in a collection |
| Composite | `TYPE#<sortField>#<uniqueId>` | Multi-field sorting |
| Metadata | `METADATA` or `COUNTER` | Singleton items in a collection |
| Timestamp-prefixed | `TYPE#<ISO-timestamp>#<id>` | Time-ordered collections |

#### Sort Key Design for Range Queries

If an access pattern needs sorting or range queries, the sort field MUST be encoded in the SK:

```
# Sort by date (newest first -- use ScanIndexForward=false)
SK = ORDER#2024-01-15T10:30:00Z#01HORDERID

# Sort by score (string-encoded numbers must be zero-padded)
SK = SCORE#000150#01HPLAYERID    (score=150, padded to 6 digits)

# Sort by status + date (hierarchical sort)
SK = ORDER#SHIPPED#2024-01-15T10:30:00Z#01HORDERID
```

**Zero-padding rule**: When numbers are used in string sort keys, they MUST be zero-padded to a fixed width so lexicographic order matches numeric order. Decide the maximum expected value and pad accordingly.

**Descending order trick**: To sort descending without `ScanIndexForward=false`, invert the value:
```
SK = SCORE#<(MAX_SCORE - actualScore) zero-padded>#<id>
```

### Step 4: Identify GSI Requirements

For each access pattern NOT covered by the table's PK/SK, determine if a GSI is needed.

**You need a GSI when:**

| Situation | Example |
|---|---|
| Query by a non-key attribute | "Find user by email" (table PK is userId) |
| Different sort order on same collection | "Orders by total" (table SK sorts by date) |
| Inverted relationship | "Find all orders containing product X" |
| Global sorted view | "Leaderboard sorted by score" |

**GSI Design Rules:**

1. **Reuse GSIs aggressively.** DynamoDB allows max 20 GSIs per table. Each GSI costs additional storage and write capacity. Design GSI keys to be overloaded across entity types when possible.

2. **Name GSIs generically.** Use `GSI1`, `GSI2`, `GSI3` for overloaded indexes. Use descriptive names only for single-purpose indexes (e.g., `email-index`).

3. **GSI key attributes follow the naming convention:**
   - Overloaded: `GSI1PK` (String), `GSI1SK` (String)
   - Single-purpose: The actual attribute name (e.g., `email` as PK, `createdAt` as SK)

4. **Choose the right projection:**
   - `ALL` -- projects all attributes (default, simplest, most expensive)
   - `KEYS_ONLY` -- only key attributes (cheapest, requires table fetch for other attributes)
   - `INCLUDE` -- specific attributes (middle ground)

5. **Sparse indexes are powerful.** If only some items have the GSI attributes, only those items appear in the index. Use this to create filtered views.

Present GSI decisions to the user:

```
I need the following GSIs:

GSI1 (overloaded, String/String):
  - User lookup by email: GSI1PK=EMAIL#<email>, GSI1SK=EMAIL#<email>
  - Order leaderboard: GSI1PK=ORDERS, GSI1SK=ORDER#<total-inverted>#<orderId>
  Projection: ALL

No additional GSIs needed. Total: 1 GSI.

Does this look right? Are there access patterns I should reconsider?
```

### Step 5: Map Every Access Pattern to a DynamoDB Operation

This is the accountability step. EVERY access pattern from the input file must be mapped to a concrete DynamoDB operation.

For each access pattern, define:

| Field | Description |
|---|---|
| **AP ID** | Reference to the access pattern |
| **DynamoDB Operation** | Query, GetItem, BatchGetItem, PutItem, TransactWriteItems, UpdateItem, DeleteItem |
| **Table or GSI** | Which index to use |
| **PK Value** | Exact partition key value (with placeholders) |
| **SK Condition** | `=`, `begins_with`, `>`, `<`, `>=`, `<=`, `BETWEEN` |
| **SK Value(s)** | The sort key value(s) |
| **Additional Parameters** | Limit, ScanIndexForward, FilterExpression, ProjectionExpression |
| **Condition Expression** | For writes: conditions that must be met |

Example:
```
AP-001: Get user by userId
  Operation: Query
  Table: Main
  PK: USER#<userId>
  SK: = USER#<userId>
  Params: Limit=1

AP-002: List orders for user, newest first
  Operation: Query
  Table: Main
  PK: USER#<userId>
  SK: begins_with(ORDER#)
  Params: ScanIndexForward=false, Limit=20, paginated

AP-010: Create order
  Operation: TransactWriteItems
  Items:
    1. Put: PK=USER#<userId>, SK=ORDER#<timestamp>#<orderId> (Condition: attribute_not_exists(pk))
    2. Put: PK=ORDER#<orderId>, SK=ORDER#<orderId> (Condition: attribute_not_exists(pk))
    3. Update: PK=USER#<userId>, SK=ORDER_COUNT (SET count = count + 1)
```

### Step 6: Validate the Design

**Read `reference/validation-checklist.md` and run through every check with the user before finalizing.**

---

## Output Format

Persist the output as a markdown file. Suggest `docs/dynamodb/table-design.md` or alongside the access patterns file.

**Read `reference/output-template.md` for the exact file structure to use.**

---

## Common Design Patterns

**Read `reference/design-patterns.md` for a catalog of reusable single-table design patterns.** Reference these when making key design decisions and present relevant patterns to the user.

---

## Rules for the Agent

1. **Read the access patterns file first.** Never design keys without documented access patterns.
2. **Map EVERY access pattern.** If a pattern can't be mapped, it's a design problem -- don't skip it.
3. **Prefer the base table over GSIs.** Only add a GSI when the base table genuinely can't serve the pattern.
4. **Be interactive.** Present groupings and key designs to the user for approval before finalizing.
5. **Show concrete examples.** For each entity, include a sample JSON item.
6. **Document decisions.** When there are trade-offs (e.g., duplication vs. extra query), explain both options and document the choice.
7. **Stay language-agnostic.** Use DynamoDB operation names (Query, GetItem, TransactWriteItems) not SDK-specific function names.
8. **Challenge hot partitions.** If a static PK like `PRODUCTS` will receive heavy traffic, discuss sharding strategies with the user.
9. **Consider write amplification.** If an entity is written to 3 item collections, that's 3x write cost. Make sure it's justified.
10. **Persist the file.** Always write the output to a `.md` file.

## Next Step

Once the table design file is complete, tell the user:

```
Table design is documented at [file path].

The next step is to generate the query interface -- method signatures
for every access pattern, ready to be implemented in your language of choice.

To continue, use the `dynamodb-query-interfaces` skill with this file as input.
```
