---
name: zenstack-migrate-from-v2
description: Upgrade an existing ZenStack V2 project to V3. Use when renaming V2 packages (zenstack, @zenstackhq/runtime), moving access control to the policy plugin, converting future() to post-update/before(), replacing abstract models with types+mixins, updating server adapters (getPrisma → getClient), and migrating client-side TanStack Query hooks.
---

# Migrating from ZenStack V2 to V3

ZenStack V3 is a major rewrite: the Prisma ORM engine is replaced with ZenStack's own engine built
on [Kysely](https://kysely.dev), while the ZModel schema stays largely compatible and the query API
stays PrismaClient-compatible. Supported databases: **PostgreSQL, MySQL, SQLite**.

Because V2 was Prisma-based, the migration has two layers: the generic Prisma→ZenStack changes, then
the V2-specific deltas below. For general setup/CLI see `zenstack-project-setup`.

## Step 1 — Do the Prisma migration first

V2 ran on Prisma, so start with the **`zenstack-migrate-from-prisma`** skill (swap deps, move the
schema to `zenstack/schema.zmodel`, replace the client with `ZenStackClient`, update generate/migrate
scripts). Then apply the V2-specific steps below.

## Step 2 — Rename ZenStack packages

```bash
npm uninstall zenstack @zenstackhq/runtime
npm install @zenstackhq/schema @zenstackhq/orm
npm install --save-dev @zenstackhq/cli
```

| V2 | V3 |
| -- | -- |
| `zenstack` (CLI) | `@zenstackhq/cli` |
| `@zenstackhq/runtime` | `@zenstackhq/orm` |
| — | `@zenstackhq/schema` (new) |

The CLI command moves from `zenstack <cmd>` to `zen <cmd>` (e.g. `zen generate`).

## Step 3 — Access control is now a plugin

In V2 access control was built into the runtime (`enhance(prisma)`). In V3 it's an opt-in plugin.

1. Install it: `npm install @zenstackhq/plugin-policy`
2. Declare it in the schema:
   ```zmodel
   plugin policy {
       provider = '@zenstackhq/plugin-policy'
   }
   ```
3. Wrap the client and bind the user per request:
   ```ts
   import { ZenStackClient } from '@zenstackhq/orm';
   import { PolicyPlugin } from '@zenstackhq/plugin-policy';

   export const db = new ZenStackClient(schema, { dialect });
   export const authDb = db.$use(new PolicyPlugin());   // was: enhance(prisma, { user })
   // per request:
   const userDb = authDb.$setAuth(user);                // was: passing { user } to enhance()
   ```

See `zenstack-access-control` for the full policy/runtime model.

## Step 4 — Post-update policies: `future()` → `post-update` + `before()`

V2 expressed post-update conditions with `future()` inside an `update` rule. V3 uses a dedicated
`post-update` operation, where bare field references mean the **new** values and `before()` reads the
**old** ones.

```zmodel
// V2
@@deny('update', future().ownerId != ownerId)

// V3
@@deny('post-update', ownerId != before().ownerId)
```

## Step 5 — Abstract models → types + mixins

V2's `abstract model` + `extends` becomes a `type` applied with `with` (see
`zenstack-schema-modeling`).

```zmodel
// V2
abstract model Timestamped {
    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt
}
model Post extends Timestamped { title String }

// V3
type Timestamped {
    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt
}
model Post with Timestamped { title String }
```

(Note: `extends` still exists in V3, but for **polymorphism** via `@@delegate`, which is a different
feature — don't use it as a plain mixin replacement.)

## Step 6 — Server adapters

V3 requires you to pass an explicit `apiHandler` (`RPCApiHandler` or `RestApiHandler`), and the
client-supplying callback is renamed `getPrisma` → `getClient`:

```ts
// V2
ZenStackMiddleware({ getPrisma: (req) => enhance(prisma, { user: getUser(req) }) });

// V3
ZenStackMiddleware({
    apiHandler: new RPCApiHandler({ schema }),
    getClient: (req) => authDb.$setAuth(getUser(req)),
});
```

See `zenstack-crud-server` for all frameworks and both API styles.

## Step 7 — Client-side hooks (TanStack Query)

Flat hook names are replaced by hooks grouped under a client that mirrors the ORM:

```ts
// V2
import { useFindManyUser } from '~/hooks';
const { data } = useFindManyUser({ where: { ... } });

// V3
import { useClientQueries } from '@zenstackhq/tanstack-query/react';
import { schema } from '~/zenstack/schema';

const client = useClientQueries(schema);
const { data } = client.user.useFindMany({ where: { ... } });
```

**SWR support was dropped** in V3. See `zenstack-crud-server` for the full TanStack Query setup.

## Step 8 — Other plugin/utility migrations

- **Zod**: now a utility rather than a plugin (see the zod utility docs).
- **OpenAPI**: folded into the automatic CRUD API handlers — generate a spec via
  `apiHandler.generateSpec()` (see `zenstack-crud-server`).
- **Custom plugins**: the V3 plugin system is revised; consult the current plugin docs.

## After upgrading

Run `zen generate`, typecheck, and exercise your test suite / app. Confirm access control behaves as
expected now that it's an explicit `$use(new PolicyPlugin())` + `$setAuth()` flow rather than V2's
implicit `enhance()`.

## Reference docs

Full ZenStack documentation for this topic is bundled under [`references/`](references/):

- [migrate-v2.md](references/migrate-v2.md) — official "Migrating from ZenStack v2" guide
