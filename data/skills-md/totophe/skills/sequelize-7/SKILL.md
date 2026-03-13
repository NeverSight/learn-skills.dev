---
name: sequelize-7
description: "Comprehensive reference for Sequelize v7 (alpha), the TypeScript-first Node.js ORM supporting PostgreSQL, MySQL, MariaDB, SQLite, MSSQL, DB2, and Snowflake. Use when working with @sequelize/core package: defining models with decorators, writing database queries (CRUD, associations, raw SQL), managing transactions, hooks, connection pools, setting up associations, or migrating from Sequelize v6 to v7."
metadata:
  version: "1.0.0"
  sequelize-version: "7.x-alpha"
  author: totophe
---

# Sequelize v7 — Claude Skill

## Key Differences from Sequelize v6

- Package renamed: `sequelize` → `@sequelize/core`
- Dialects are separate packages (e.g., `@sequelize/postgres`, `@sequelize/sqlite3`)
- Decorator-based model definitions (recommended over `Model.init()`)
- Constructor only accepts a single options object (no URL string as first arg)
- `dialectOptions` removed — settings go in top-level options
- CLS transactions enabled by default (no manual setup needed)
- Default association names are now camelCase (`userId` not `UserId`)
- `sequelize.transaction()` only creates managed transactions; use `sequelize.startUnmanagedTransaction()` for unmanaged
- JSON null vs SQL NULL distinction: inserting `null` into JSON stores JSON `'null'`, not SQL `NULL`
- Minimum: Node >= 18, TypeScript >= 5.0

## Skill Files

| File | Contents |
|------|----------|
| [getting-started.md](references/getting-started.md) | Installation, connection, TypeScript setup, logging |
| [models.md](references/models.md) | Model definitions, data types, decorators, timestamps, naming, validation, indexes |
| [querying.md](references/querying.md) | CRUD operations, operators, WHERE clauses, raw SQL, JSON querying, subqueries |
| [associations.md](references/associations.md) | HasOne, HasMany, BelongsTo, BelongsToMany, eager loading |
| [advanced.md](references/advanced.md) | Transactions, hooks, scopes, connection pool, paranoid models, optimistic locking, read replication, migrations |

## Quick Reference — Common Patterns

### Minimal Model (TypeScript + Decorators)

```typescript
import { Model, InferAttributes, InferCreationAttributes, CreationOptional, DataTypes } from '@sequelize/core';
import { Attribute, PrimaryKey, AutoIncrement, NotNull } from '@sequelize/core/decorators-legacy';

export class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {
  @Attribute(DataTypes.INTEGER)
  @PrimaryKey
  @AutoIncrement
  declare id: CreationOptional<number>;

  @Attribute(DataTypes.STRING)
  @NotNull
  declare name: string;

  @Attribute(DataTypes.STRING)
  declare email: string | null;

  declare createdAt: CreationOptional<Date>;
  declare updatedAt: CreationOptional<Date>;
}
```

### Initialize Sequelize

```typescript
import { Sequelize } from '@sequelize/core';
import { PostgresDialect } from '@sequelize/postgres';

const sequelize = new Sequelize({
  dialect: PostgresDialect,
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'user',
  password: 'pass',
  models: [User],
});
```

### Basic CRUD

```typescript
// Create
const user = await User.create({ name: 'Alice' });

// Read
const users = await User.findAll({ where: { name: 'Alice' } });
const one = await User.findByPk(1);

// Update
await user.update({ name: 'Bob' });
await User.update({ name: 'Bob' }, { where: { id: 1 } });

// Delete
await user.destroy();
await User.destroy({ where: { id: 1 } });
```

### Association with Eager Loading

```typescript
const posts = await Post.findAll({
  include: ['comments'],
  where: { authorId: 1 },
});
```

### Managed Transaction

```typescript
const result = await sequelize.transaction(async () => {
  const user = await User.create({ name: 'Alice' });
  await Profile.create({ userId: user.id, bio: 'Hello' });
  return user;
});
```
