---
name: dynamodb-query-interfaces
description: "Generates language-agnostic repository interfaces (method signatures, input/output types, and entity models) from a DynamoDB table design document. Use when the user has a table design .md file (from dynamodb-table-design skill) and wants to generate the code skeleton for their data access layer. This is Step 3 of a 3-step pipeline: access patterns -> table design -> query interfaces."
---

# DynamoDB Query Interfaces

This skill takes a DynamoDB table design document and generates a complete set of repository interfaces: entity types, method signatures, input/output contracts, and key-building utilities. The output is language-agnostic pseudocode that can be directly translated to any language.

## When to Use

- The user has a table design `.md` file (from `dynamodb-table-design` or manually written)
- The user wants to generate the data access layer skeleton
- The user wants type-safe method signatures for every access pattern
- The user wants to see the full repository interface before implementing

## Pipeline Position

```
  1. Access Patterns  -->  2. Table Design  -->  [3. Query Interfaces]
  (dynamodb-access-      (dynamodb-table-       (this skill)
   patterns)              design)
```

**Input**: Table design `.md` file
**Output**: Interface definition `.md` file with pseudocode ready for implementation

---

## Prerequisites

Read the table design file. If it doesn't exist or is incomplete, tell the user to run the `dynamodb-table-design` skill first.

**Read `reference/language-conventions.md` to determine the target language syntax.** Ask the user which language they intend to implement in. If they have no preference, use Generic pseudocode.

---

## Generation Workflow

### Step 1: Generate Entity Models

For each entity in the table design, create a data model type.

**Rules:**
- Include `pk` and `sk` as string fields (these are the DynamoDB key attributes)
- Include GSI key attributes only if the entity uses a GSI
- Include all domain attributes from the table design
- Mark optional fields explicitly
- Add documentation comments referencing the entity description

**Template:**
```
// Entity: [Name]
// Description: [from table design]
// PK: [pattern]
// SK: [pattern]
interface [EntityName] {
  pk: string
  sk: string
  [GSI attributes if applicable]
  [domain attributes with types]
}
```

**Example (Generic):**
```
// Entity: Order
// Description: A purchase made by a customer
// PK: USER#<userId>
// SK: ORDER#<createdAt>#<orderId>
interface Order {
  pk: string                    // USER#<userId>
  sk: string                    // ORDER#<createdAt>#<orderId>
  GSI1PK: optional string       // PRODUCT#<productId> (only if indexed)
  GSI1SK: optional string       // ORDER#<createdAt>#<orderId>
  orderId: string               // ULID
  userId: string
  total: number
  status: string                // PENDING | SHIPPED | DELIVERED | CANCELLED
  items: list<OrderItem>
  createdAt: string             // ISO 8601
  updatedAt: optional string    // ISO 8601
}
```

### Step 2: Generate Key Builder Functions

For each entity, generate a function that builds the PK and SK from domain parameters.

**Template:**
```
// Builds keys for [EntityName]
// AP references: [list of AP IDs that use this key]
function build[EntityName]Key(params) -> { pk: string, sk: string }
```

**Example:**
```
// Builds keys for Order
// AP references: AP-001, AP-002, AP-010, AP-020
function buildOrderKey({ userId: string, createdAt: string, orderId: string }) -> {
  pk: "USER#" + userId,
  sk: "ORDER#" + createdAt + "#" + orderId
}

// Builds the prefix key for querying all orders of a user
// AP references: AP-002
function buildOrderCollectionPrefix({ userId: string }) -> {
  pk: "USER#" + userId,
  skPrefix: "ORDER#"
}
```

**Rules for key builders:**
- One builder per unique key pattern per entity
- Include a prefix builder for every `begins_with` access pattern
- Include a GSI key builder if the entity has GSI attributes
- Document which AP IDs use each builder

### Step 3: Generate Repository Interface

Create one repository interface per entity (or per bounded context if the user prefers a unified repository).

Each method in the repository maps to exactly ONE access pattern from the table design.

**For each method, define:**

1. **Method signature** with typed parameters
2. **Return type** (entity, list of entities, paginated result, or void)
3. **AP reference** (which access pattern it implements)
4. **DynamoDB operation** (from the table design mapping)
5. **Key construction** (which key builder to use)
6. **Notes** (conditions, transaction details, etc.)

**Example:**
```
interface OrderRepository {

  // AP-001: Get a specific order by orderId
  // Operation: Query
  // Table/GSI: Table
  // Key: ORDER#<orderId> / = ORDER#<orderId>
  function getOrderById({ orderId: string }) -> optional Order

  // AP-002: List all orders for a user, newest first
  // Operation: Query
  // Table/GSI: Table
  // Key: USER#<userId> / begins_with(ORDER#)
  // Params: ScanIndexForward=false, paginated
  function listUserOrdersPaginated({
    userId: string,
    limit: number,
    cursor: optional string
  }) -> PaginatedResult<Order>

  // AP-010: Create a new order
  // Operation: TransactWriteItems
  // Items:
  //   1. Put ORDER in user collection (condition: attribute_not_exists(pk))
  //   2. Put ORDER self-record (condition: attribute_not_exists(pk))
  //   3. Update ORDER_COUNT +1
  function createOrder({
    userId: string,
    orderId: string,
    total: number,
    status: string,
    items: list<OrderItem>
  }) -> Order
}
```

### Step 4: Generate Transaction Helper Types

For write operations that involve multiple items, define the transaction structure:

```
// AP-010: Create order transaction
transaction CreateOrderTransaction {
  items: [
    {
      operation: Put
      entity: Order (user collection)
      key: buildOrderKey({ userId, createdAt, orderId })
      condition: attribute_not_exists(pk)
    },
    {
      operation: Put
      entity: Order (self-record)
      key: buildOrderCatalogKey({ orderId })
      condition: attribute_not_exists(pk)
    },
    {
      operation: Update
      entity: OrderCount
      key: buildOrderCountKey({ userId })
      update: SET count = count + :inc
      values: { ":inc": 1 }
    }
  ]
}
```

### Step 5: Validate Coverage

Create a traceability matrix showing that every AP is covered:

```
| AP ID | Method | Status |
|-------|--------|--------|
| AP-001 | OrderRepository.getOrderById | Covered |
| AP-002 | OrderRepository.listUserOrdersPaginated | Covered |
| AP-010 | OrderRepository.createOrder | Covered |
```

Every AP MUST have status "Covered". If any AP is "Not Covered", the design has a gap.

---

## Output Format

Persist the output as a markdown file. Suggest `docs/dynamodb/query-interfaces.md` or alongside the other files.

**Read `reference/output-template.md` for the exact file structure to use.**

---

## Multi-Entity Read Pattern

When a single Query returns items of different entity types (the power of single-table design), the repository method must:

1. Accept the common PK parameter
2. Return a structured object with typed fields for each entity type
3. Document that the implementation filters by SK prefix in application code

```
// AP-003: Get user profile with recent orders
// This is a SINGLE DynamoDB Query that returns heterogeneous items.
// The implementation:
//   1. Queries PK=USER#<userId> with no SK condition (or begins_with(""))
//   2. Iterates results, grouping by SK prefix:
//      - SK starts with "USER#"   -> User entity
//      - SK starts with "ORDER#"  -> Order entity
//      - SK starts with "BALANCE" -> Balance entity
//   3. Returns the structured result
function getUserProfileWithOrders({ userId: string }) -> {
  user: optional User,
  orders: list<Order>,
  balance: optional Balance
}
```

---

## Rules for the Agent

1. **Read the table design file first.** Never generate interfaces without a table design.
2. **One method per access pattern.** Don't combine multiple APs into one method unless they're truly the same query.
3. **Every method references its AP ID.** This maintains traceability from requirements to code.
4. **Include DynamoDB operation details in comments.** The implementer should know exactly what DynamoDB call to make from the interface alone.
5. **Use the user's preferred language syntax.** If they say TypeScript, use TypeScript. If they say Python, use Python dataclasses/Protocols. Default to generic pseudocode.
6. **Key builders are separate from repository methods.** This allows reuse and testing.
7. **Pagination is always cursor-based.** Never expose page numbers or offsets -- DynamoDB doesn't support them.
8. **Document transaction structures explicitly.** Multi-item writes are the most complex operations; make them crystal clear.
9. **Validate complete coverage.** The traceability matrix must show 100% coverage.
10. **Persist the file.** Always write the output to a `.md` file.

## Next Step

Once the interfaces file is complete, tell the user:

```
Query interfaces are documented at [file path].

You now have the complete design pipeline:
  1. Access Patterns: [path]
  2. Table Design:    [path]
  3. Interfaces:      [path]

The next step is implementation. You can use these interfaces as the contract
for your data access layer. Each method comment contains the exact DynamoDB
operation, key construction, and conditions needed.

Recommended implementation order:
  1. Entity models (types/interfaces/classes)
  2. Key builder functions
  3. Repository methods (reads first, then writes)
  4. Integration tests against DynamoDB Local or a test table
```
