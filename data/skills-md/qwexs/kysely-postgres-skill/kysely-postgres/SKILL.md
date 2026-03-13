---
name: kysely-postgres
description: Write effective, type-safe Kysely queries for PostgreSQL. This skill should be used when working in Node.js/TypeScript backends with Kysely installed, covering query patterns, migrations, type generation, and common pitfalls to avoid.
version: "0.28.x"
last_updated: "2025-01-25"
---

# Kysely for PostgreSQL

Kysely is a type-safe TypeScript SQL query builder. This skill provides patterns for writing effective queries, managing migrations, and avoiding common pitfalls.

**Current version:** 0.28.10 (January 2025)
**Minimum TypeScript version:** 4.6+

## When to Use This Skill

Use this skill when:
- Working in a Node.js/TypeScript project with Kysely installed
- Writing database queries for PostgreSQL
- Creating or modifying database migrations
- Debugging type inference issues in Kysely queries

## What's New in 0.28.x

### Breaking Changes

1. **InferResult returns arrays**: `InferResult<T>` now returns `InsertResult[]`, `UpdateResult[]`, `DeleteResult[]`, `MergeResult[]`. For a single result, use `InferResult<T>[number]`.

2. **Mandatory .execute()**: Removed `preventAwait` — queries no longer throw an error when awaited without `.execute()`, but the result will be `undefined`. Always call `.execute()`.

3. **Removed**: `QueryResult.numUpdatedOrDeletedRows` — use `numAffectedRows` instead.

4. **TypeScript 4.5 and older are no longer supported**.

### New Features

#### Controlled Transactions with Savepoints

```typescript
// Create savepoint and rollback to it
await db.transaction().execute(async (trx) => {
  await trx.insertInto("user").values({ email: "a@test.com" }).execute();
  
  // Create savepoint
  const savepoint = await trx.savepoint("before_risky_op");
  
  try {
    await trx.insertInto("user").values({ email: "duplicate@test.com" }).execute();
  } catch (e) {
    // Rollback to savepoint without canceling the entire transaction
    await savepoint.rollbackToSavepoint();
  }
  
  // First insert will be preserved
});
```

#### await using (Explicit Resource Management)

```typescript
// Automatic rollback when exiting scope without commit
await using trx = await db.startTransaction();

await trx.insertInto("user").values({ email: "test@example.com" }).execute();

// If commit() is not called, transaction will rollback automatically
await trx.commit();
```

#### Read-only Transactions

```typescript
// Read-only transaction (PostgreSQL optimizes these)
await db.transaction().setReadOnly(true).execute(async (trx) => {
  const users = await trx.selectFrom("user").selectAll().execute();
  // INSERT/UPDATE/DELETE will throw a database error
});
```

#### HandleEmptyInListsPlugin

```typescript
import { Kysely, HandleEmptyInListsPlugin } from "kysely";

// Plugin handles empty arrays in IN()
const db = new Kysely<DB>({
  dialect,
  plugins: [new HandleEmptyInListsPlugin()],
});

const ids: number[] = []; // Empty array

// Without plugin: SQL syntax error "IN ()"
// With plugin: automatically replaced with "1 = 0" (always false)
await db.selectFrom("user").where("id", "in", ids).execute();
```

#### Cross Join and Cross Join Lateral

```typescript
// Cross join
const result = await db
  .selectFrom("product")
  .crossJoin("category")
  .select(["product.name", "category.name as categoryName"])
  .execute();

// Cross join lateral (for correlated subqueries)
const result = await db
  .selectFrom("user as u")
  .crossJoinLateral(
    (eb) => eb
      .selectFrom("order")
      .select(["id", "total"])
      .whereRef("order.user_id", "=", "u.id")
      .orderBy("created_at", "desc")
      .limit(3)
      .as("recent_orders")
  )
  .selectAll()
  .execute();
```

#### DynamicModule.table() for Dynamic Tables

```typescript
import { DynamicModule } from "kysely";

const dynamic = new DynamicModule();

// Type-safe dynamic table reference
const tableName = "user" as "user" | "admin";
const users = await db
  .selectFrom(dynamic.table(tableName))
  .selectAll()
  .execute();
```

## Features from 0.27.x

### MERGE Queries (0.27.3+)

```typescript
// MERGE (upsert with full control)
await db
  .mergeInto("product")
  .using("product_updates", "product.sku", "product_updates.sku")
  .whenMatched()
  .thenUpdateSet({
    name: (eb) => eb.ref("product_updates.name"),
    price: (eb) => eb.ref("product_updates.price"),
  })
  .whenNotMatched()
  .thenInsertValues({
    sku: (eb) => eb.ref("product_updates.sku"),
    name: (eb) => eb.ref("product_updates.name"),
    price: (eb) => eb.ref("product_updates.price"),
  })
  .execute();
```

### Clear Methods (0.27.3+)

```typescript
// Clear specific query parts for dynamic query building
let query = db.selectFrom("user").select(["id", "email"]).where("role", "=", "admin");

// Clear and rebuild
query = query
  .clearSelect()
  .select(["id", "first_name", "last_name"])
  .clearWhere()
  .where("is_active", "=", true);

// Available: clearSelect(), clearWhere(), clearOrderBy(), clearLimit(), clearOffset(), clearGroupBy()
```

### eb.cast() Method (0.27.3+)

```typescript
// Type-safe casting
.select((eb) => [
  eb.cast<number>("price", "integer").as("priceInt"),
  eb.cast(eb.val("123"), "integer").as("numericValue"),
])
```

### WITHIN GROUP for Ordered Aggregates (0.27.4+)

```typescript
// PostgreSQL ordered-set aggregate functions
.select((eb) => [
  eb.fn("percentile_cont", [eb.lit(0.5)])
    .withinGroup((ob) => ob.orderBy("price", "asc"))
    .as("medianPrice"),
])
```

### modifyEnd() for Raw SQL Appendix (0.27.5+)

```typescript
// Append raw SQL to end of query
await db
  .selectFrom("user")
  .selectAll()
  .modifyEnd(sql`FOR UPDATE SKIP LOCKED`)
  .execute();
```

### $narrowType Helper (0.25.0+)

```typescript
// Narrow query result types when you know more than TypeScript
const users = await db
  .selectFrom("user")
  .select(["id", "email", "deleted_at"])
  .where("deleted_at", "is", null)
  .$narrowType<{ deleted_at: null }>() // Tell TS deleted_at is definitely null
  .execute();
// users[0].deleted_at is typed as null, not Date | null
```

### $assertType for Complex Queries

```typescript
// Break type chain for excessively deep types (12+ CTEs)
const result = await db
  .with("cte1", (qb) =>
    qb.selectFrom("user")
      .select(["id", "email"])
      .$assertType<{ id: number; email: string }>()
  )
  .selectFrom("cte1")
  .selectAll()
  .execute();
```

## Reference Files

For detailed examples, see these topic-focused reference files:

- [select-where.ts](references/select-where.ts) - Basic SELECT patterns, WHERE clauses, AND/OR conditions
- [joins.ts](references/joins.ts) - Simple joins, callback joins, subquery joins, cross joins
- [aggregations.ts](references/aggregations.ts) - COUNT, SUM, AVG, GROUP BY, HAVING
- [orderby-pagination.ts](references/orderby-pagination.ts) - ORDER BY, NULLS handling, DISTINCT, pagination
- [ctes.ts](references/ctes.ts) - Common Table Expressions, multiple CTEs, recursive CTEs
- [json-arrays.ts](references/json-arrays.ts) - JSONB handling, array columns, jsonBuildObject, jsonAgg
- [relations.ts](references/relations.ts) - jsonArrayFrom, jsonObjectFrom for nested data
- [mutations.ts](references/mutations.ts) - INSERT, UPDATE, DELETE, UPSERT, INSERT FROM SELECT
- [expressions.ts](references/expressions.ts) - CASE, $if, subqueries, eb.val/lit/not, standalone expressionBuilder

## Core Principles

1. **Prefer Kysely methods over raw SQL**: Almost everything you can do in SQL, you can do in Kysely without `sql``
2. **Use the ExpressionBuilder (eb)**: The `eb` parameter in callbacks is the foundation of type-safe query building
3. **Let TypeScript guide you**: If it compiles, it's likely correct SQL

## ExpressionBuilder (eb) - The Foundation

The `eb` parameter in select/where callbacks provides all expression methods:

```typescript
.select((eb) => [
  eb.ref("column").as("alias"),                    // Column reference
  eb.fn<string>("upper", [eb.ref("email")]),       // Function call (typed!)
  eb.fn.count("id").as("count"),                   // Aggregate function
  eb.fn.sum("amount").as("total"),                 // SUM
  eb.fn.avg("rating").as("avgRating"),             // AVG
  eb.fn.coalesce("nullable_col", eb.val(0)),       // COALESCE
  eb.case().when("status", "=", "active")          // CASE expression
    .then("Active").else("Inactive").end(),
  eb("quantity", "*", eb.ref("unit_price")),       // Binary expression
  eb.exists(subquery),                             // EXISTS
  eb.not(expression),                              // NOT / negation
  eb.cast(eb.val(" "), "text"),                    // Cast value to type
  eb.and([...]),                                   // AND conditions
  eb.or([...]),                                    // OR conditions
])
```

### eb.val() vs eb.lit()

```typescript
// eb.val() - Creates a parameterized value ($1, $2, etc.) - PREFERRED for user input
// Note: eb.val() alone may fail with "could not determine data type of parameter"
// Use eb.cast(eb.val(...), "text") for string values in function arguments
eb.val("user input")                    // Becomes: $1 with parameter "user input"
eb.cast(eb.val("safe"), "text")         // Becomes: $1::text - always works

// eb.lit() - Creates a literal value in SQL
// ONLY accepts: numbers, booleans, null - NOT strings (throws "unsafe immediate value")
eb.lit(1)             // Becomes: 1 (directly in SQL)
eb.lit(true)          // Becomes: true
eb.lit(null)          // Becomes: NULL

// For string literals, use sql`` template instead
sql`'active'`         // Becomes: 'active' (directly in SQL)
sql<string>`'label'`  // Typed string literal
```

### Standalone ExpressionBuilder

For reusable helpers outside query callbacks:

```typescript
import { expressionBuilder } from "kysely";
import type { DB } from "./db.d.ts";

// Create standalone expression builder
const eb = expressionBuilder<DB, "user">();

// Use in helper functions
function isActiveUser() {
  return eb.and([
    eb("is_active", "=", true),
    eb("role", "!=", "banned"),
  ]);
}
```

### Conditional Expressions with Arrays

Build dynamic filters by collecting expressions:

```typescript
.where((eb) => {
  const filters: Expression<SqlBool>[] = [];

  if (firstName) filters.push(eb("first_name", "=", firstName));
  if (lastName) filters.push(eb("last_name", "=", lastName));
  if (minAge) filters.push(eb("age", ">=", minAge));

  // Combine all filters with AND (empty array = no filter)
  return eb.and(filters);
})
```

## String Concatenation

Use the `||` operator with `sql` template for clean string concatenation:

```typescript
// RECOMMENDED - Clean and type-safe with eb.ref()
.select((eb) => [
  sql<string>`${eb.ref("first_name")} || ' ' || ${eb.ref("last_name")}`.as("full_name"),
])
// Output: "first_name" || ' ' || "last_name"

// ALTERNATIVE - Pure eb() chaining (parameterized literals)
.select((eb) => [
  eb(eb("first_name", "||", " "), "||", eb.ref("last_name")).as("full_name"),
])
// Output: "first_name" || $1 || "last_name"

// VERBOSE - concat() function (avoid unless you need NULL handling)
.select((eb) => [
  eb.fn<string>("concat", [
    eb.ref("first_name"),
    eb.cast(eb.val(" "), "text"),
    eb.ref("last_name"),
  ]).as("full_name"),
])
```

**Note**: `concat()` treats NULL as empty string, while `||` propagates NULL. Use `concat()` only when you need that NULL behavior.

## Query Patterns

### Basic SELECT

```typescript
// Select all columns
const users = await db.selectFrom("user").selectAll().execute();

// Select specific columns with aliases
const users = await db
  .selectFrom("user")
  .select(["id", "email", "first_name as firstName"])
  .execute();

// Single row (returns T | undefined)
const user = await db.selectFrom("user").selectAll()
  .where("id", "=", userId).executeTakeFirst();

// Single row that must exist (throws if not found)
const user = await db.selectFrom("user").selectAll()
  .where("id", "=", userId).executeTakeFirstOrThrow();
```

### WHERE Clauses

```typescript
// Equality, comparison, IN, LIKE
.where("status", "=", "active")
.where("price", ">", 100)
.where("role", "in", ["admin", "manager"])
.where("name", "like", "%search%")
.where("deleted_at", "is", null)

// Multiple conditions (chained = AND)
.where("is_active", "=", true)
.where("role", "=", "admin")

// OR conditions
.where((eb) => eb.or([
  eb("role", "=", "admin"),
  eb("role", "=", "manager"),
]))

// Complex AND/OR
.where((eb) => eb.and([
  eb("is_active", "=", true),
  eb.or([
    eb("price", "<", 50),
    eb("stock", ">", 100),
  ]),
]))
```

### JOINs

```typescript
// Inner join
.innerJoin("order", "order.user_id", "user.id")

// Left join
.leftJoin("category", "category.id", "product.category_id")

// Self-join with alias
.selectFrom("category as c")
.leftJoin("category as parent", "parent.id", "c.parent_id")

// Multiple joins
.innerJoin("order", "order.id", "order_item.order_id")
.innerJoin("product", "product.id", "order_item.product_id")
.innerJoin("user", "user.id", "order.user_id")
```

### Complex JOINs (Callback Format)

Use the callback format when you need:
- Multiple join conditions (composite keys)
- Mixed column-to-column and column-to-literal comparisons
- OR conditions within joins
- Subquery joins (derived tables)

**Join Builder Methods:**
- `onRef(col1, op, col2)` - Column-to-column comparison
- `on(col, op, value)` - Column-to-literal comparison
- `on((eb) => ...)` - Complex expressions with OR logic

```typescript
// Multi-condition join (composite key + filter)
.leftJoin("invoice as i", (join) =>
  join
    .onRef("sp.service_provider_id", "=", "i.service_provider_id")
    .onRef("sp.year", "=", "i.year")
    .onRef("sp.month", "=", "i.month")
    .on("i.status", "!=", "invalidated")
)

// Join with OR conditions
.leftJoin("order as o", (join) =>
  join
    .onRef("o.user_id", "=", "u.id")
    .on((eb) =>
      eb.or([
        eb("o.status", "=", "completed"),
        eb("o.status", "=", "shipped"),
      ])
    )
)

// Subquery join (derived table) - two callbacks
.leftJoin(
  (eb) =>
    eb
      .selectFrom("order")
      .select((eb) => [
        "user_id",
        eb.fn.count("id").as("order_count"),
        eb.fn.max("created_at").as("last_order_at"),
      ])
      .groupBy("user_id")
      .as("order_stats"),  // MUST have alias!
  (join) => join.onRef("order_stats.user_id", "=", "u.id")
)

// Cross join (0.28.x+) - cartesian product
.crossJoin("category")

// Cross join lateral (0.28.x+) - subquery can reference outer table columns
// Perfect for "top N per group" patterns
.crossJoinLateral(
  (eb) => eb
    .selectFrom("order")
    .select(["id", "total_amount"])
    .whereRef("order.user_id", "=", "u.id")
    .orderBy("created_at", "desc")
    .limit(3)
    .as("recent_orders")
)

// Left join lateral - includes rows without matches
.leftJoinLateral(
  (eb) => eb
    .selectFrom("review")
    .select(["rating"])
    .whereRef("review.product_id", "=", "p.id")
    .limit(1)
    .as("latest_review")
)

// Legacy workaround (before 0.28.x) - always-true condition
.leftJoin("summary_cte", (join) =>
  join.on(sql`true`, "=", sql`true`)
)
```

### Aggregations

```typescript
.select((eb) => [
  "status",
  eb.fn.count("id").as("count"),
  eb.fn.sum("total_amount").as("totalAmount"),
  eb.fn.avg("total_amount").as("avgAmount"),
])
.groupBy("status")
.having((eb) => eb.fn.count("id"), ">", 5)
```

### ORDER BY

```typescript
// Simple ordering
.orderBy("created_at", "desc")
.orderBy("name", "asc")

// NULLS FIRST / NULLS LAST - use order builder callback
.orderBy("category_id", (ob) => ob.asc().nullsLast())
.orderBy("priority", (ob) => ob.desc().nullsFirst())

// Multiple columns - chain orderBy calls (array syntax is deprecated)
.orderBy("category_id", "asc")
.orderBy("price", "desc")
.orderBy("name", "asc")
```

### CTEs (Common Table Expressions)

Use CTEs for complex queries with multiple aggregation levels:

```typescript
const result = await db
  .with("order_totals", (db) =>
    db.selectFrom("order")
      .innerJoin("user", "user.id", "order.user_id")
      .select((eb) => [
        "user.id as userId",
        "user.email",
        eb.fn.sum("order.total_amount").as("totalSpent"),
        eb.fn.count("order.id").as("orderCount"),
      ])
      .groupBy(["user.id", "user.email"])
  )
  .selectFrom("order_totals")
  .selectAll()
  .orderBy("totalSpent", "desc")
  .execute();
```

### JSON Aggregation (PostgreSQL)

```typescript
import { jsonBuildObject } from "kysely/helpers/postgres";
// Note: jsonAgg is accessed via eb.fn.jsonAgg(), not imported

.with("tasks", (db) =>
  db.selectFrom("task")
    .leftJoin("user", "user.id", "task.assignee_id")
    .select((eb) => [
      "task.job_id",
      eb.fn.jsonAgg(
        jsonBuildObject({
          id: eb.ref("task.id"),
          status: eb.ref("task.status"),
          assignee: jsonBuildObject({
            id: eb.ref("user.id"),
            name: eb.fn<string>("concat", [
              eb.ref("user.first_name"),
              eb.cast(eb.val(" "), "text"),
              eb.ref("user.last_name"),
            ]),
          }),
        })
      )
      .filterWhere("task.id", "is not", null) // Filter nulls from left join
      .as("tasks"),
    ])
    .groupBy("task.job_id")
)
```

## JSON, JSONB, and Array Handling

### JSONB Columns

**NO `JSON.stringify` or `JSON.parse` needed!** The `pg` driver handles JSONB automatically:

```typescript
// INSERT - pass objects directly
await db
  .insertInto("user")
  .values({
    email: "test@example.com",
    metadata: { preferences: { theme: "dark" }, count: 42 },
  })
  .execute();

// UPDATE - pass objects directly
await db
  .updateTable("user")
  .set({
    metadata: { preferences: { theme: "light" } },
  })
  .where("id", "=", userId)
  .execute();

// READ - returns parsed object, not string
const user = await db
  .selectFrom("user")
  .select(["id", "metadata"])
  .executeTakeFirst();
console.log(user.metadata.preferences.theme); // "dark" - already an object!
```

### Array Columns (text[], int[], etc.)

**NO `JSON.stringify` needed for array columns!** The `pg` driver handles arrays natively:

```typescript
// INSERT with array - pass array directly
await db
  .insertInto("product")
  .values({
    name: "Product",
    tags: ["phone", "electronics", "premium"], // Direct array!
  })
  .execute();

// READ - returns as native JavaScript array
const product = await db
  .selectFrom("product")
  .select(["name", "tags"])
  .executeTakeFirst();
console.log(product.tags); // ["phone", "electronics", "premium"]

// UPDATE array
await db
  .updateTable("product")
  .set({ tags: ["updated", "tags"] })
  .where("id", "=", productId)
  .execute();
```

### Querying Arrays

```typescript
// Array contains all values (@>) - operator works natively!
.where("tags", "@>", sql`ARRAY['phone', 'premium']::text[]`)

// Arrays overlap (&&) - operator works natively!
.where("tags", "&&", sql`ARRAY['premium', 'basic']::text[]`)

// Array contains value (ANY) - type-safe with eb.fn
.where((eb) => eb(sql`${searchTerm}`, "=", eb.fn("any", [eb.ref("tags")])))
// eb.ref("tags") validates column exists - eb.ref("invalid") would be a TS error
```

### Querying JSONB

```typescript
// Key exists (?) - operator works natively!
.where("metadata", "?", "theme")

// Any key exists (?|) - operator works natively!
.where("metadata", "?|", sql`array['theme', 'language']`)

// All keys exist (?&) - operator works natively!
.where("metadata", "?&", sql`array['theme', 'notifications']`)

// JSONB contains (@>) - operator works natively!
.where("metadata", "@>", sql`'{"notifications": true}'::jsonb`)

// Extract field as text (->> as operator) - type-safe!
.where((eb) => eb(eb("metadata", "->>", "theme"), "=", "dark"))
// eb("metadata", ...) validates column - eb("invalid", ...) would be TS error

// Extract nested path (#>> still needs sql``)
.where(sql`metadata#>>'{preferences,theme}'`, "=", "dark")

// In SELECT - type-safe with eb()
.select((eb) => [
  eb("metadata", "->", "preferences").as("prefs"),   // Returns JSONB
  eb("metadata", "->>", "theme").as("theme"),        // Returns text
])
// Nested paths still need sql``
.select(sql`metadata#>'{preferences,theme}'`.as("t"))   // Nested as JSONB
.select(sql<string>`metadata#>>'{a,b}'`.as("t"))        // Nested as text
```

### JSONPath (PostgreSQL 12+)

```typescript
// JSONPath match (@@) - works as native operator!
.where("metadata", "@@", sql`'$.preferences.theme == "dark"'`)

// JSONPath exists (@?) - NOT in Kysely's allowlist, use function instead
// Use jsonb_path_exists() for type-safe column validation
.where((eb) =>
  eb.fn("jsonb_path_exists", [eb.ref("metadata"), sql`'$.preferences.theme'`])
)
// eb.ref("metadata") validates column - eb.ref("invalid") would be TS error

// Extract with JSONPath - type-safe with eb.fn
.select((eb) => [
  "id",
  eb.fn("jsonb_path_query_first", [eb.ref("metadata"), sql`'$.preferences.theme'`]).as("theme"),
])

// JSONPath with variables
const searchValue = "dark";
.where((eb) =>
  eb.fn("jsonb_path_exists", [
    eb.ref("metadata"),
    sql`'$.preferences.theme ? (@ == $val)'`,
    sql`jsonb_build_object('val', ${searchValue}::text)`,
  ])
)
```

### Conditional Queries ($if)

Use `$if()` for runtime-conditional query modifications:

```typescript
const result = await db
  .selectFrom("user")
  .selectAll()
  .$if(!includeInactive, (qb) => qb.where("is_active", "=", true))
  .$if(includeMetadata, (qb) => qb.select("metadata"))
  .$if(!!searchTerm, (qb) => qb.where("name", "like", `%${searchTerm}%`))
  .$if(!!roleFilter, (qb) => qb.where("role", "in", roleFilter!))
  .execute();
```

**Type behavior**: Columns added via `$if` become optional in the result type since inclusion isn't guaranteed at compile time.

### Relations (jsonArrayFrom / jsonObjectFrom)

Kysely is NOT an ORM - it uses PostgreSQL's JSON functions for nested data:

```typescript
import { jsonArrayFrom, jsonObjectFrom } from "kysely/helpers/postgres";

// One-to-many: User with their orders
const users = await db
  .selectFrom("user")
  .select((eb) => [
    "user.id",
    "user.email",
    jsonArrayFrom(
      eb
        .selectFrom("order")
        .select(["order.id", "order.status", "order.total_amount"])
        .whereRef("order.user_id", "=", "user.id")
        .orderBy("order.created_at", "desc")
    ).as("orders"),
  ])
  .execute();

// Many-to-one: Product with its category
const products = await db
  .selectFrom("product")
  .select((eb) => [
    "product.id",
    "product.name",
    jsonObjectFrom(
      eb
        .selectFrom("category")
        .select(["category.id", "category.name"])
        .whereRef("category.id", "=", "product.category_id")
    ).as("category"),
  ])
  .execute();
```

### Reusable Helpers

Create composable, type-safe helper functions using `Expression<T>`:

```typescript
import { Expression, sql } from "kysely";

// Helper that takes and returns Expression<string>
function lower(expr: Expression<string>) {
  return sql<string>`lower(${expr})`;
}

// Use in queries
.where(({ eb, ref }) => eb(lower(ref("email")), "=", email.toLowerCase()))
```

### Splitting Query Building and Execution

Build queries without executing, useful for dynamic query construction:

```typescript
// Build query (doesn't execute)
let query = db
  .selectFrom("user")
  .select(["id", "email"]);

// Add conditions dynamically
if (role) {
  query = query.where("role", "=", role);
}
if (isActive !== undefined) {
  query = query.where("is_active", "=", isActive);
}

// Execute when ready
const results = await query.execute();

// Or compile to SQL without executing
const compiled = query.compile();
console.log(compiled.sql);        // The SQL string
console.log(compiled.parameters); // Bound parameters
```

### Subqueries

```typescript
// Subquery in WHERE
.where("id", "in",
  db.selectFrom("order").select("user_id").where("status", "=", "completed")
)

// EXISTS subquery
.where((eb) =>
  eb.exists(
    db.selectFrom("review")
      .select(sql`1`.as("one"))
      .whereRef("review.product_id", "=", eb.ref("product.id"))
  )
)
```

### INSERT Operations

```typescript
// Single insert with returning
const user = await db
  .insertInto("user")
  .values({ email: "test@example.com", first_name: "Test", last_name: "User" })
  .returning(["id", "email"])
  .executeTakeFirst();

// Multiple rows
await db
  .insertInto("user")
  .values([
    { email: "a@example.com", first_name: "A", last_name: "User" },
    { email: "b@example.com", first_name: "B", last_name: "User" },
  ])
  .execute();

// Upsert (ON CONFLICT) - type-safe with expression builder
await db
  .insertInto("product")
  .values({ sku: "ABC123", name: "Product", stock_quantity: 10 })
  .onConflict((oc) =>
    oc.column("sku").doUpdateSet((eb) => ({
      stock_quantity: eb("product.stock_quantity", "+", eb.ref("excluded.stock_quantity")),
    }))
  )
  .execute();
// eb("product.invalid_column", ...) would be a TypeScript error!

// Insert from SELECT
await db
  .insertInto("archive")
  .columns(["user_id", "data", "archived_at"])
  .expression(
    db.selectFrom("user")
      .select(["id", "metadata", sql`now()`.as("archived_at")])
      .where("is_active", "=", false)
  )
  .execute();
```

### UPDATE Operations

```typescript
// Simple update
await db
  .updateTable("user")
  .set({ is_active: false })
  .where("id", "=", userId)
  .execute();

// Update with expression
await db
  .updateTable("product")
  .set((eb) => ({
    stock_quantity: eb("stock_quantity", "+", 10),
  }))
  .where("sku", "=", "ABC123")
  .returning(["id", "stock_quantity"])
  .executeTakeFirst();
```

## Transactions

### Basic Transaction

```typescript
// Callback-based transaction (automatic commit/rollback)
await db.transaction().execute(async (trx) => {
  const user = await trx
    .insertInto("user")
    .values({ email: "test@example.com", first_name: "Test", last_name: "User" })
    .returning("id")
    .executeTakeFirstOrThrow();

  await trx
    .insertInto("order")
    .values({ user_id: user.id, status: "pending", total_amount: "0" })
    .execute();

  // If any query throws an error, the entire transaction will rollback
});
```

### Controlled Transactions (0.28.x+)

```typescript
// startTransaction() — manual control over commit/rollback
const trx = await db.startTransaction();

try {
  await trx.insertInto("user").values({ email: "a@test.com" }).execute();
  await trx.commit();
} catch (e) {
  await trx.rollback();
  throw e;
}

// With await using — automatic rollback when exiting scope
await using trx = await db.startTransaction();
await trx.insertInto("user").values({ email: "b@test.com" }).execute();
await trx.commit(); // Without commit() transaction will rollback automatically
```

### Savepoints (0.28.x+)

```typescript
await db.transaction().execute(async (trx) => {
  await trx.insertInto("user").values({ email: "first@test.com" }).execute();

  // Create savepoint
  const sp = await trx.savepoint("before_second");

  try {
    await trx.insertInto("user").values({ email: "duplicate@test.com" }).execute();
  } catch (e) {
    // Rollback only to savepoint, without canceling first insert
    await sp.rollbackToSavepoint();
  }

  // first@test.com will be preserved
});
```

### Read-only Transactions (0.28.x+)

```typescript
// PostgreSQL optimizes read-only transactions
await db.transaction().setReadOnly(true).execute(async (trx) => {
  const users = await trx.selectFrom("user").selectAll().execute();
  // INSERT/UPDATE/DELETE will throw a database error
});
```

### Isolation Levels

```typescript
await db
  .transaction()
  .setIsolationLevel("serializable") // or "read committed", "repeatable read"
  .execute(async (trx) => {
    // Maximum isolation
  });
```

## Migrations

### Configuration (kysely.config.ts)

```typescript
import { PostgresDialect } from "kysely";
import { defineConfig } from "kysely-ctl";
import pg from "pg";

export default defineConfig({
  dialect: new PostgresDialect({
    pool: new pg.Pool({
      connectionString: process.env.DATABASE_URL,
    }),
  }),
  migrations: {
    migrationFolder: "src/db/migrations",
  },
  seeds: {
    seedFolder: "src/db/seeds",
  },
});
```

### Migration Commands

```bash
npx kysely migrate:make migration-name  # Create migration
npx kysely migrate:latest               # Run all pending migrations
npx kysely migrate:down                 # Rollback last migration
npx kysely seed make seed-name          # Create seed
npx kysely seed run                     # Run all seeds
```

### Migration File Structure

```typescript
import type { Kysely } from "kysely";
import { sql } from "kysely";

// Always use Kysely<any> - migrations should be frozen in time
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable("user")
    .addColumn("id", "bigint", (col) => col.primaryKey().generatedAlwaysAsIdentity())
    .addColumn("email", "text", (col) => col.notNull().unique())
    .addColumn("created_at", "timestamptz", (col) => col.notNull().defaultTo(sql`now()`))
    .execute();

  // IMPORTANT: Always index foreign key columns!
  await db.schema.createIndex("idx_order_user_id").on("order").column("user_id").execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable("user").execute();
}
```

### Recommended Column Types

```typescript
// Primary keys: Use identity columns (SQL standard, prevents accidental ID conflicts)
.addColumn("id", "bigint", (col) => col.primaryKey().generatedAlwaysAsIdentity())
// NOT serial/bigserial - those allow manual ID inserts that can cause conflicts

// Timestamps: Always use timestamptz (stores UTC, converts to client timezone)
.addColumn("created_at", "timestamptz", (col) => col.notNull().defaultTo(sql`now()`))
// NOT timestamp - loses timezone information

// Money: Use numeric with precision (exact decimal, no floating point errors)
.addColumn("price", "numeric(10, 2)", (col) => col.notNull())
// NOT float/real/double precision - those have rounding errors

// Strings: Use text (no length limit, same performance as varchar)
.addColumn("name", "text", (col) => col.notNull())
// varchar(n) only if you need a hard length constraint

// JSON: Use jsonb (binary, indexable, faster queries)
.addColumn("metadata", "jsonb")
// NOT json - stored as text, no indexing, slower

// Foreign keys: Create indexes manually (PostgreSQL doesn't auto-index FKs)
await db.schema.createIndex("idx_order_user_id").on("order").column("user_id").execute();
```

### Data Type Gotchas

```typescript
// CORRECT - Space after comma in numeric types
.addColumn("price", "numeric(10, 2)")

// WRONG - Will fail with "invalid column data type"
.addColumn("price", "numeric(10,2)")

// For complex types, use sql template
.addColumn("price", sql`numeric(10, 2)`)
```

## Type Generation

Use `kysely-codegen` to generate types from your database:

```bash
npx kysely-codegen --url "postgresql://..." --out-file src/db/db.d.ts
```

Generated types use:
- `Generated<T>` for auto-increment columns (optional on insert)
- `ColumnType<Select, Insert, Update>` for different operation types
- `Timestamp` for timestamptz columns

## Common Pitfalls to Avoid

### 1. Don't Resort to `sql`` When Kysely Has a Method

```typescript
// WRONG
.select(sql`count(*)`.as("count"))

// RIGHT
.select((eb) => eb.fn.countAll().as("count"))
```

### 2. Don't Forget .execute()

Queries are lazy - they won't run without calling an execute method:

```typescript
// This does nothing!
db.selectFrom("user").selectAll();

// This runs the query
await db.selectFrom("user").selectAll().execute();
```

### 3. Use whereRef for Column-to-Column Comparisons

```typescript
// WRONG - Compares to string literal "other.column"
.where("table.column", "=", "other.column")

// RIGHT - Compares to actual column value
.whereRef("table.column", "=", "other.column")
```

### 4. Type Your Function Returns

```typescript
// Better type inference
eb.fn<string>("concat", [...])
eb.fn<number>("length", [...])
```

### 5. PostgreSQL Does NOT Auto-Index Foreign Keys

Always create indexes on foreign key columns:

```typescript
await db.schema.createIndex("idx_order_user_id").on("order").column("user_id").execute();
```

### 6. Always Type `sql` Template Literals

When using `sql` template literals, the inferred type is `unknown` since Kysely can't know what the SQL expression resolves to. Always provide an explicit type:

```typescript
// WRONG - Returns unknown type
eb.fn.coalesce("some_json_col", sql`'{}'::jsonb`)

// RIGHT - Explicit type annotation
eb.fn.coalesce("some_json_col", sql<Record<string, unknown>>`'{}'::jsonb`)

// For complex types (e.g., JSON column from a CTE), use typeof with eb.ref
// This ensures the fallback type matches the column type exactly
eb.fn
  .coalesce(
    eb.ref("jobs_agg.jobs"),
    sql<typeof eb.ref<"jobs_agg.jobs">>`'[]'::json`
  )
  .as("jobs")
```

**Key rule**: Every `sql` template literal should have a type parameter: `sql<TYPE>`. This ensures proper type inference throughout your query chain.

### 7. DATE Columns Cause Timezone Issues

By default, the `pg` driver converts DATE columns to JavaScript `Date` objects. This causes timezone problems:

```
Database: 2025-01-01 (just a date, no time)
JS Date:  2025-01-01T00:00:00.000Z (interpreted as UTC midnight)
User in NYC sees: Dec 31, 2024 (5 hours behind UTC)
```

**Solution: Parse DATE as string and let the frontend handle formatting**

Step 1: Configure `pg` to return DATE as string:

```typescript
import pg from "pg";

// Tell pg to return DATE columns as strings instead of Date objects
const DATE_OID = 1082;
pg.types.setTypeParser(DATE_OID, (val: string) => val);
```

Step 2: Update `kysely-codegen` to generate matching types:

```bash
npx kysely-codegen \
  --url="$DATABASE_URL" \
  --out-file=server/db/db.d.ts \
  --dialect=postgres \
  --date-parser=string
```

Now DATE columns return strings like `"2025-01-01"` and the frontend can parse/format respecting the user's timezone.

**Note**: This applies to DATE columns only. TIMESTAMPTZ columns already handle timezones correctly by storing UTC and converting on read.

## PostgreSQL Helpers Summary

All helpers from `kysely/helpers/postgres`:

```typescript
import {
  jsonArrayFrom,    // One-to-many relations (subquery → array)
  jsonObjectFrom,   // Many-to-one relations (subquery → object | null)
  jsonBuildObject,  // Build JSON object from expressions
  mergeAction,      // Get action performed in MERGE query (PostgreSQL 15+)
} from "kysely/helpers/postgres";
```

**Note**: `jsonAgg` is NOT imported - use `eb.fn.jsonAgg()` instead.

### mergeAction (PostgreSQL 15+)

For MERGE queries, get which action was performed:

```typescript
import { mergeAction } from "kysely/helpers/postgres";

const result = await db
  .mergeInto("person")
  .using("person_updates", "person.id", "person_updates.id")
  .whenMatched()
  .thenUpdateSet({ name: eb.ref("person_updates.name") })
  .whenNotMatched()
  .thenInsertValues({ id: eb.ref("person_updates.id"), name: eb.ref("person_updates.name") })
  .returning([mergeAction().as("action"), "id"])
  .execute();

// result[0].action is 'INSERT' | 'UPDATE' | 'DELETE'
```

## Extending Kysely

### Custom Helper Functions

Most extensions use the `sql` template tag with `RawBuilder<T>`:

```typescript
import { sql, RawBuilder } from "kysely";

// Create a typed helper function
function json<T>(value: T): RawBuilder<T> {
  return sql`CAST(${JSON.stringify(value)} AS JSONB)`;
}

// Use in queries
.select((eb) => [
  json({ name: "value" }).as("data"),
])
```

### Custom Expression Classes

For reusable expressions, implement the `Expression<T>` interface:

```typescript
import { Expression, OperationNode, sql } from "kysely";

class JsonValue<T> implements Expression<T> {
  readonly #value: T;

  constructor(value: T) {
    this.#value = value;
  }

  get expressionType(): T | undefined {
    return undefined;
  }

  toOperationNode(): OperationNode {
    return sql`CAST(${JSON.stringify(this.#value)} AS JSONB)`.toOperationNode();
  }
}
```

**Note**: Module augmentation and inheritance-based extension are not recommended.

## Handling "Excessively Deep Types" Error

### The Problem

Complex queries with many CTEs can overwhelm TypeScript's type instantiation limits:

```
Type instantiation is excessively deep and possibly infinite
```

This commonly occurs with 12+ `with` clauses, as Kysely's nested helper types accumulate.

### The Solution: `$assertType`

Use `$assertType` to simplify the type chain at intermediate points:

```typescript
const result = await db
  .with("cte1", (qb) =>
    qb.selectFrom("user")
      .select(["id", "email"])
      .$assertType<{ id: number; email: string }>()  // Simplify type here
  )
  .with("cte2", (qb) =>
    qb.selectFrom("cte1")
      .select("email")
      .$assertType<{ email: string }>()
  )
  // ... more CTEs
  .selectFrom("cteN")
  .selectAll()
  .execute();
```

**Key points**:
- The asserted type must structurally match the actual type (full type safety preserved)
- Apply to several intermediate `with` clauses in large queries
- TypeScript cannot automatically simplify these types - explicit assertion is required
