---
name: typeorm-seeding
description: >
  Create entity factories, seeders, and test data for @kage0x3b/typeorm-seeding.
  Use when creating or editing Factory subclasses, Seeder subclasses, relationship
  descriptors (belongsTo, hasMany, hasOne, sequence, ref), factory variants,
  test setup with SeedingContext, or generating fixture/seed data for TypeORM entities.
---

# typeorm-seeding

Library for creating and seeding TypeORM entities using a factory/seeder pattern. ESM-only, TypeScript.

Four components: **Factory** (defines how to build entities), **SeedingContext** (manages factories, sequences, cleanup), **Descriptors** (relationship/value helpers), **Seeder** (orchestrates factory calls).

## Creating a Factory

```typescript
import { Factory, sequence, type Faker, type FactorySchema } from '@kage0x3b/typeorm-seeding';
import { UserEntity } from './entities/UserEntity.js';

export class UserFactory extends Factory<UserEntity> {
    readonly model = UserEntity;

    define(faker: Faker): FactorySchema<UserEntity> {
        return {
            firstName: faker.person.firstName(),
            lastName: faker.person.lastName(),
            email: sequence((n) => `user${n}@test.com`),
            role: faker.helpers.arrayElement(['user', 'editor', 'viewer']),
        };
    }
}
```

Rules:
- `model` = the TypeORM entity class
- `define(faker)` returns `FactorySchema<T>` — plain values and/or descriptors for each data property
- `FactorySchema<T>` excludes functions and symbols; only covers persistable properties
- Entity must have no required constructor args (created via `new Model()` + `Object.assign`)
- Source imports use `.js` extensions (Node16 module resolution)

### Factory with relationships

```typescript
import { Factory, belongsTo, type Faker, type FactorySchema } from '@kage0x3b/typeorm-seeding';
import { PetEntity } from './entities/PetEntity.js';
import { UserFactory } from './UserFactory.js';

export class PetFactory extends Factory<PetEntity> {
    readonly model = PetEntity;

    define(faker: Faker): FactorySchema<PetEntity> {
        return {
            name: faker.animal.petName(),
            species: faker.helpers.arrayElement(['dog', 'cat', 'bird']),
            owner: belongsTo(UserFactory),
        };
    }
}
```

## Descriptors

All descriptors are imported from `@kage0x3b/typeorm-seeding`.

### `belongsTo(factoryRef, overridesOrEntity?, variant?)`

ManyToOne or owning-side OneToOne. Creates (or references) a parent entity and sets the FK.

```typescript
owner: belongsTo(UserFactory)                                    // auto-create parent
owner: belongsTo(UserFactory, { role: 'admin' })                 // with overrides
owner: belongsTo(UserFactory, existingUser)                      // existing entity (has PK)
owner: belongsTo(UserFactory, undefined, 'admin')                // with variant
owner: belongsTo(UserFactory, { email: 'a@b.com' }, ['admin', 'inactive'])  // variant + overrides
```

Disambiguation: if the second arg has a non-nullish primary key (detected via TypeORM metadata), it's an existing entity; otherwise it's overrides.

Each entity gets its **own** parent. 5 pets with `belongsTo(UserFactory)` = 5 separate users.

### `hasMany(factoryRef, count, overrides?, variant?)`

OneToMany. Creates `count` children referencing back to the parent. Resolved **after** the parent is saved.

```typescript
pets: hasMany(PetFactory, 3)
pets: hasMany(PetFactory, 2, { species: 'dog' })
pets: hasMany(PetFactory, 3, undefined, 'dog')
```

### `hasOne(factoryRef, overrides?, variant?)`

Non-owning OneToOne. Creates a single child referencing back to the parent.

```typescript
profile: hasOne(ProfileFactory)
profile: hasOne(ProfileFactory, { bio: 'Custom bio' })
```

### `sequence(callback)`

Auto-incrementing counter scoped per factory class, starts at 1.

```typescript
orderIndex: sequence((n) => n)
email: sequence((n) => `user${n}@test.com`)
```

### `ref(label)`

Resolves to a previously labeled entity (via `.as(label)`). Throws if label not registered.

```typescript
company: ref('acmeCorp')
```

## Variants

Override `variants(faker)` to define named variations layered on top of `define()`. The `faker` instance is passed as an argument, allowing variants to generate dynamic fake data.

```typescript
export class UserFactory extends Factory<UserEntity> {
    readonly model = UserEntity;

    define(faker: Faker): FactorySchema<UserEntity> {
        return {
            firstName: faker.person.firstName(),
            email: sequence((n) => `user${n}@test.com`),
            role: 'user',
            isActive: true,
        };
    }

    variants(faker: Faker) {
        return {
            admin: {
                role: 'admin',
                email: sequence((n) => `admin${n}@test.com`),
            },
            inactive: { isActive: false },
            withPets: { pets: hasMany(PetFactory, 3) },
        };
    }
}
```

Usage:

```typescript
await userFactory.variant('admin').persistOne();
await userFactory.variant('admin', 'inactive').persistOne();  // combine variants
```

Variants can contain any descriptor. Throws if variant name doesn't exist.

### Descriptors in overrides

Overrides accept descriptors, not just plain values. The type is `FactoryOverrides<T>`.

```typescript
// sequence in override — unique email per entity
const users = await userFactory.build(5, {
    email: sequence((n) => `batch-${n}@test.com`),
});

// belongsTo in override — create a specific parent
const pet = await petFactory.persistOne({
    owner: belongsTo(UserFactory, { role: 'admin' }),
});

// ref in override — reference a labeled entity
await userFactory.persistOne().as('manager');
const report = await reportFactory.buildOne({
    assignedTo: ref('manager'),
});
```

Variant in relationship descriptors:

```typescript
user: belongsTo(UserFactory, undefined, 'admin')   // parent created with admin variant
pets: hasMany(PetFactory, 2, undefined, 'dog')      // children created with dog variant
```

## Creating a Seeder

```typescript
import { Seeder } from '@kage0x3b/typeorm-seeding';

export class DatabaseSeeder extends Seeder {
    async run(): Promise<void> {
        const admin = await this.factory(UserFactory)
            .variant('admin')
            .persistOne()
            .as('adminUser');

        await this.factory(PetFactory).persist(3, { owner: admin });
        await this.factory(UserFactory).persist(10);
    }
}
```

- Extend `Seeder`, implement `run()`
- `this.factory(FactoryClass)` returns the factory instance (same as `this.ctx.getFactory()`)
- `this.ctx` accesses the `SeedingContext` for refs, store, etc.
- `.as(label)` registers the entity for later lookup via `ref('label')` or `ctx.ref<T>('label')`
- `.as()` only works on `persistOne()`/`buildOne()`, not on `persist(n)`/`build(n)`

Run seeders: `await ctx.runSeeders([SetupSeeder, DataSeeder]);` — runs in order, shares context.

## Test Setup

### Cleanup-per-test pattern

```typescript
import { DataSource } from 'typeorm';
import { createSeedingContext, SeedingContext } from '@kage0x3b/typeorm-seeding';

let dataSource: DataSource;
let ctx: SeedingContext;

beforeAll(async () => {
    dataSource = new DataSource({
        type: 'better-sqlite3',
        database: ':memory:',
        entities: [UserEntity, PetEntity],
        synchronize: true,
    });
    await dataSource.initialize();
});

beforeEach(() => {
    ctx = createSeedingContext(dataSource);
    // Or with a custom faker instance for deterministic output:
    // ctx = createSeedingContext(dataSource, { faker: seededFaker });
});

afterEach(async () => {
    await ctx.cleanup();   // deletes all created entities in reverse order
});

afterAll(async () => {
    await dataSource.destroy();
});
```

### Transaction-per-test pattern

Each test runs in a transaction that rolls back — no cleanup needed.

```typescript
let ctx: SeedingContext;
let txCtx: SeedingContext;
let queryRunner: QueryRunner;

beforeAll(async () => {
    // ... dataSource setup ...
    ctx = createSeedingContext(dataSource);
});

beforeEach(async () => {
    ctx.reset();   // resets sequences, refs, and creation log
    queryRunner = dataSource.createQueryRunner();
    await queryRunner.startTransaction();
    txCtx = ctx.withTransaction(queryRunner.manager);
});

afterEach(async () => {
    await queryRunner.rollbackTransaction();
    await queryRunner.release();
});

// In tests, use txCtx instead of ctx:
const user = await txCtx.getFactory(UserFactory).variant('withPets').persistOne();
```

## Common Pitfalls

- **No constructor args**: Entities must work with `new Entity()` + `Object.assign`. No required constructor parameters.
- **Overrides accept descriptors**: Override parameters (`FactoryOverrides<T>`) accept plain values, `null`, or any descriptor (`belongsTo`, `hasMany`, `hasOne`, `sequence`, `ref`).
- **Overrides replace descriptors**: Passing `{ owner: existingUser }` replaces the entire `belongsTo` descriptor. The factory won't create a new parent.
- **Separate parents per belongsTo**: Each entity gets its own parent by default. To share a parent, pass it explicitly as an override.
- **Sequence scoping**: Sequences are scoped per factory class, not per variant. `UserFactory` and `UserFactory.variant('admin')` share the same counter.
- **`.as()` on single-entity methods only**: `.as(label)` is only available on `persistOne()`/`buildOne()`, not `persist(n)`/`build(n)`.
- **Enum values in variants**: When using TypeScript enums in variants, you may need `as any` cast due to `Partial<FactorySchema<T>>` typing: `role: UserRole.ADMIN as any`.

## Advanced

- **Context store**: Typed shared state via `ctx.store` with module augmentation. See `docs/public-api.md` for details.
- **Labeled refs**: `.as(label)` + `ref('label')` for ad-hoc entity references across factories/seeders.
- **Transaction support**: `ctx.withTransaction(em)` creates a child context scoped to a transaction.
- **Resolution internals**: 7-phase schema resolution. See `docs/internal-implementation.md` for SchemaResolver phases.
- **Full API reference**: See `docs/public-api.md` for all methods on Factory, SeedingContext, and Seeder.
