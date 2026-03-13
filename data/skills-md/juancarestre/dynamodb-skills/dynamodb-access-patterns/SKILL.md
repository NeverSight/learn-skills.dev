---
name: dynamodb-access-patterns
description: "Interactive skill for eliciting, formalizing, and persisting DynamoDB access patterns. Use when the user wants to start designing a DynamoDB table, define entities, or document how their application will read and write data. This is Step 1 of a 3-step pipeline: access patterns -> table design -> query interfaces. The output is a structured .md file that feeds into the dynamodb-table-design skill."
---

# DynamoDB Access Patterns

This skill guides an interactive conversation to extract, formalize, and persist all access patterns for a DynamoDB single-table design. It is **language-agnostic** and **project-agnostic** -- it works for any application regardless of tech stack.

## When to Use

- The user wants to design a new DynamoDB table from scratch
- The user wants to add new entities to an existing DynamoDB table
- The user says things like "I need to store X and query by Y"
- The user wants to document their access patterns before implementation
- The user has an existing relational schema they want to migrate to DynamoDB

## Pipeline Position

```
  [1. Access Patterns]  -->  2. Table Design  -->  3. Query Interfaces
       (this skill)        (dynamodb-table-     (dynamodb-query-
                            design)              interfaces)
```

This skill produces a `.md` file that is consumed by `dynamodb-table-design`.

---

## Interactive Workflow

### Step 1: Understand the Domain

Ask the user to describe their application at a high level. You need to understand:

1. **What does the application do?** (e-commerce, social network, game, SaaS, etc.)
2. **Who are the actors?** (users, admins, systems, etc.)
3. **What are the main entities?** (the "nouns" of the system)

Ask open-ended questions. Don't assume -- let the user describe their domain.

Example opening:
```
Before designing the DynamoDB table, I need to understand your domain.

1. What does your application do in one sentence?
2. What are the main entities (things you need to store)?
3. Who or what interacts with these entities?
```

### Step 2: Catalog All Entities

For each entity the user mentions, gather:

| Field | Description | Example |
|---|---|---|
| **Name** | Singular name, PascalCase | `Order` |
| **Description** | What it represents | "A purchase made by a customer" |
| **Attributes** | All fields with types | `orderId: string, total: number, status: string, createdAt: datetime` |
| **Relationships** | How it relates to other entities | "Belongs to a User. Contains many OrderItems." |
| **Cardinality** | Expected volume | "~100 orders per user, ~10M total" |
| **Lifecycle** | Does it expire? Get updated? Deleted? | "Updated when status changes. Archived after 1 year." |

Ask the user about EACH entity systematically. Don't skip attributes -- they affect key design later.

**IMPORTANT**: Also identify **counter/aggregate entities** that the user might not think of as entities:
- "Do you need to track counts? (e.g., number of orders per user)"
- "Do you need running totals or balances?"
- "Do you need any metadata records?"

### Step 3: Elicit Access Patterns

This is the most critical step. For EACH entity, ask:

```
For [Entity], how will your application access this data?
Think about every screen, API endpoint, or background job that reads or writes this entity.
```

For each access pattern, capture these fields:

| Field | Description |
|---|---|
| **ID** | Sequential number (AP-001, AP-002, ...) |
| **Entity** | Which entity or entities are involved |
| **Operation** | Read / Write / Update / Delete |
| **Description** | Plain English description |
| **Input Parameters** | What the caller provides |
| **Result Type** | Single item, Collection, or Count |
| **Sort Required** | None, Ascending, Descending -- and by what field |
| **Filters** | Any conditions beyond the lookup key |
| **Pagination** | Yes/No -- is the result set potentially large? |
| **Frequency** | Hot (>100/s), Warm (1-100/s), Cold (<1/s) |
| **Consistency** | Eventual (default) or Strong |
| **Multi-Entity** | Does this pattern need data from multiple entity types in one call? |

**Probing questions to uncover hidden patterns:**

- "How do you list these? All at once, paginated, or filtered?"
- "Do you ever need to sort by anything other than creation time?"
- "Do you need to look this up from the 'other side'?" (e.g., find user by email, not just by userId)
- "Are there any leaderboards, rankings, or sorted lists?"
- "Do you need to check existence before creating?"
- "Are there any batch operations? (create 10 items at once)"
- "Do any items have a TTL or expiration?"
- "Do you need to fetch a parent AND its children in one call?"

### Step 4: Identify Item Collection Opportunities

Review all access patterns and look for cases where **multiple entity types are fetched together**. These are the most valuable patterns in single-table design.

Ask the user:
```
Looking at your access patterns, I see some opportunities to fetch related data in a single query:

- [AP-003] and [AP-007] both need User + Orders data
- [AP-012] needs Product + Reviews together

Do these always get fetched together, or only sometimes?
Are there screens/endpoints where you need BOTH in one call?
```

Mark these patterns explicitly as **item collection candidates**.

### Step 5: Identify Write Patterns and Transactions

For every write operation, determine:

1. **How many items are written per operation?** (single item vs. transaction)
2. **Must they succeed or fail together?** (transaction requirement)
3. **Are there conditional writes?** (don't overwrite if exists, ensure parent exists, etc.)
4. **Do writes affect counters?** (incrementing a count alongside creating an item)

Example questions:
```
When you create an Order:
- Do you also need to update the user's order count?
- Do you need to add it to a global "recent orders" list?
- Should it fail if the user doesn't exist?
```

### Step 6: Validate Completeness

Before persisting, do a final review with the user:

```
Here's a summary of what I've captured:

Entities: [list]
Access Patterns: [count] total
  - Reads: [count]
  - Writes: [count]
  - Multi-entity: [count]

Missing anything? Common things people forget:
- Admin/backoffice access patterns
- Search/filtering patterns
- Reporting or analytics queries (these may go to a different system)
- Migration or bulk import patterns
- Audit trail / history patterns
```

---

## Output Format

Persist the output as a markdown file. The user chooses the path, but suggest `docs/dynamodb/access-patterns.md` or a similar location in their project.

**Read `reference/output-template.md` for the exact file structure to use.**

---

## Rules for the Agent

1. **Never skip the interactive conversation.** Don't generate access patterns from assumptions. Always ask.
2. **Be thorough.** It's better to capture 5 patterns you don't use than miss 1 you need.
3. **Challenge the user.** If they say "I just need basic CRUD", push back with specific questions about sorting, filtering, pagination, and multi-entity reads.
4. **Stay language-agnostic.** Use generic types: `string`, `number`, `boolean`, `datetime`, `list`, `map`. Don't use TypeScript, Python, or Java-specific types.
5. **Don't design keys yet.** This skill is about WHAT data you need, not HOW to store it. Key design happens in the next skill (`dynamodb-table-design`).
6. **Persist the file.** Always write the output to a `.md` file. This file is the input for the next step.
7. **Use the question tool.** When you need to clarify between options, use the interactive question tool to give the user clear choices.
8. **Number everything.** Access patterns must have stable IDs (AP-001, AP-002, ...) because the next skill references them.
9. **Mark multi-entity patterns explicitly.** These are the most important patterns for single-table design.
10. **Include write patterns.** Writes determine transactions and item duplication strategy. They're as important as reads.

## Next Step

Once the access patterns file is complete, tell the user:

```
Access patterns are documented at [file path].

The next step is to design the DynamoDB table structure -- partition keys,
sort keys, GSIs, and map each access pattern to a concrete DynamoDB operation.

To continue, use the `dynamodb-table-design` skill with this file as input.
```
