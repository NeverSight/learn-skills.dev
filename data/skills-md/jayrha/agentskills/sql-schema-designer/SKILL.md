---
name: sql-schema-designer
description: Designs normalized relational database schemas with primary/foreign keys, constraints, indexes, and deliberate denormalization, producing engine-aware DDL and an ER model. Use this skill when the user asks to design a database schema, model entities and relationships, normalize tables, fix update/insert/delete anomalies, choose data types and keys, add constraints or indexes, write CREATE TABLE DDL, or review/refactor an existing schema for PostgreSQL, MySQL, SQLite, or SQL Server.
license: MIT
---

# SQL Schema Designer

## Overview

Turn fuzzy requirements into a clean, normalized relational schema with correct keys, constraints, indexes, and justified denormalization. Output is runnable DDL plus a documented data model.

Keywords: database schema design, normalization, 1NF 2NF 3NF BCNF, primary key, foreign key, referential integrity, ON DELETE CASCADE, CHECK constraint, unique constraint, surrogate vs natural key, composite key, index, composite index, covering index, denormalization, ER diagram, entity relationship, data modeling, DDL, CREATE TABLE, PostgreSQL, MySQL, SQLite, SQL Server, junction table, many-to-many.

## Workflow

1. **Clarify scope and engine.** Identify the target database engine (PostgreSQL, MySQL, SQLite, SQL Server) because types and identity syntax differ — see `references/data-types-and-constraints.md`. Ask about expected scale, read/write ratio, and whether reporting queries matter.

2. **Extract entities and attributes.** From the domain, list nouns that have independent existence (`customer`, `product`, `order`). Each becomes a table. List the attributes (facts) each must store. Mark attributes that are required vs optional.

3. **Define relationships and cardinality.** For every pair of related entities decide one-to-one, one-to-many, or many-to-many.
   - One-to-many: foreign key on the "many" side.
   - Many-to-many: create a **junction table** with both FKs (its PK is usually the composite of both, or a surrogate plus a UNIQUE on the pair).
   - One-to-one: FK + UNIQUE on the dependent side, or share a PK.

4. **Choose keys.** Pick a primary key per table.
   - Prefer a **surrogate key** (auto-increment / identity / UUID) for stability when natural keys are large, mutable, or composite.
   - Always also declare a **UNIQUE** constraint on the real natural key (email, SKU, ISBN) to preserve business integrity.
   - Use composite natural PKs for pure junction tables when no surrogate is needed.

5. **Normalize to 3NF.** Apply 1NF -> 2NF -> 3NF, removing partial and transitive dependencies. Escalate to BCNF only when a concrete anomaly remains. Use the decomposition checklist in `references/normalization.md`.

6. **Add constraints.** For each column decide `NOT NULL`, `DEFAULT`, `CHECK`. For each FK pick explicit `ON DELETE` / `ON UPDATE` actions (`RESTRICT`, `CASCADE`, `SET NULL`) — never leave them to the engine default silently.

7. **Pick data types** per `references/data-types-and-constraints.md`. Money is exact `NUMERIC`/`DECIMAL`, never float. Instants are UTC and time-zone-aware. Size `VARCHAR` to real limits.

8. **Plan indexes.** Index every FK column. Add indexes for real `WHERE`/`JOIN`/`ORDER BY` patterns, ordering composite-index columns equality-first. Avoid redundant and unused indexes.

9. **Consider denormalization last.** Only after the normalized schema exists and a real query is too slow. Document the source of truth, the sync mechanism, and tolerated staleness.

10. **Emit DDL and the model.** Produce `CREATE TABLE` statements in dependency order (parents before children) and a relationship summary. Fill `templates/schema-design.md`. Optionally run `scripts/validate_schema.py` to lint the SQL for common omissions.

## Decision frameworks

### Surrogate vs natural primary key

| Situation | Choose |
|-----------|--------|
| Natural key is stable, short, single-column (country ISO code) | Natural key |
| Natural key is large, composite, or may change (email, full name) | Surrogate + UNIQUE on natural key |
| Pure junction table (M:N link, no own attributes) | Composite PK of the two FKs |
| Distributed inserts / need ID before insert / hide row counts | UUID surrogate |

### Relationship -> structure

- **1:N** — FK on the many side, indexed, NOT NULL if mandatory.
- **M:N** — junction table `a_b(a_id, b_id, ...)`, PK `(a_id, b_id)`, each FK indexed.
- **1:1** — FK + UNIQUE on the optional side, or shared PK for mandatory.
- **Self-reference (hierarchy)** — FK to same table (`manager_id -> employee.id`), `ON DELETE SET NULL` or `RESTRICT`.

### NULL decision

Use NULL only for genuinely "unknown / not applicable" facts. Never use NULL as a flag or a magic value. If a column is almost always present, make it `NOT NULL DEFAULT ...`.

## Worked example (condensed)

Requirement: customers place orders; each order has many line items referencing products; products belong to categories.

```sql
CREATE TABLE category (
  category_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name         VARCHAR(100) NOT NULL,
  CONSTRAINT uq_category_name UNIQUE (name)
);

CREATE TABLE product (
  product_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku          VARCHAR(40)  NOT NULL,
  name         VARCHAR(200) NOT NULL,
  unit_price   NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
  category_id  BIGINT NOT NULL REFERENCES category(category_id)
                 ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT uq_product_sku UNIQUE (sku)
);
CREATE INDEX ix_product_category ON product(category_id);

CREATE TABLE customer (
  customer_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email        VARCHAR(254) NOT NULL,
  full_name    VARCHAR(200) NOT NULL,
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
  CONSTRAINT uq_customer_email UNIQUE (email)
);

CREATE TABLE "order" (
  order_id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id  BIGINT NOT NULL REFERENCES customer(customer_id)
                 ON UPDATE CASCADE ON DELETE RESTRICT,
  status       VARCHAR(20) NOT NULL DEFAULT 'pending'
                 CHECK (status IN ('pending','paid','shipped','cancelled')),
  ordered_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_order_customer ON "order"(customer_id);

CREATE TABLE order_item (
  order_id     BIGINT NOT NULL REFERENCES "order"(order_id)
                 ON DELETE CASCADE,          -- items are owned by the order
  product_id   BIGINT NOT NULL REFERENCES product(product_id)
                 ON DELETE RESTRICT,
  quantity     INTEGER NOT NULL CHECK (quantity > 0),
  unit_price   NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),  -- snapshot at sale time
  PRIMARY KEY (order_id, product_id)
);
CREATE INDEX ix_order_item_product ON order_item(product_id);
```

Notes that make this correct: `order_item.unit_price` is a deliberate point-in-time snapshot (not a 3NF violation); `order_item` PK is the composite of its FKs; the order->item FK cascades (ownership) while item->product restricts (a referenced product cannot vanish); every FK is indexed.

See `examples/ecommerce-schema.md` for the full annotated walkthrough including a many-to-many tag example.

## Best Practices

- Normalize to 3NF first; denormalize only with evidence and a sync plan.
- Give every table a primary key. No exceptions.
- Declare UNIQUE on natural keys even when using a surrogate PK.
- Make `NOT NULL` the default; justify every nullable column.
- Use exact `NUMERIC`/`DECIMAL` for money; UTC time-zone-aware types for instants.
- State `ON DELETE`/`ON UPDATE` explicitly on every foreign key.
- Index all foreign keys and real query predicates; order composite indexes equality-first.
- Use CHECK constraints to encode domain rules (status whitelists, positive amounts, date ordering).
- Emit DDL in dependency order so it runs top-to-bottom without forward references.
- Use consistent snake_case naming and the constraint prefixes in `references/data-types-and-constraints.md`.

## Common Pitfalls

- **Storing lists in a column** (CSV, JSON array of IDs) instead of a child table — breaks 1NF and querying.
- **No primary key**, or using a mutable natural key as PK that later changes everywhere.
- **Unindexed foreign keys** — silently slow joins and cascading deletes.
- **Float for money** — rounding errors. Always exact decimal.
- **Missing referential actions** — accidental orphan rows or blocked deletes you didn't intend.
- **Over-normalizing** to 5NF when 3NF suffices, or **over-indexing** every column and crushing write throughput.
- **Confusing a snapshot with redundancy** — copied `unit_price`/`document_name` at transaction time is intentional, not denormalization to "fix."
- **Premature denormalization** with no consistency mechanism, leaving cached aggregates permanently wrong.
- **Local-time timestamps** without zone info, making ordering and conversions ambiguous.
