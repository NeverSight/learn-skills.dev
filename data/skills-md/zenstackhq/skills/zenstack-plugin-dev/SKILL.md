---
name: zenstack-plugin-dev
description: Develop ZenStack V3 plugins. Use when building or declaring a plugin — custom ZModel attributes/functions, CLI code generators (CliPlugin with a generate callback for `zen generate`), or runtime plugins installed via $use/definePlugin (onQuery, onKyselyQuery, onEntityMutation hooks, extending the client, custom query args, computed result fields).
---

# ZenStack V3 — Plugin Development

> Plugins are a **preview** feature and may change in future releases.

A ZenStack plugin can extend the toolkit at **three levels**, independently or together:

1. **Schema (ZModel)** — contribute custom attributes (e.g. `@password`) and functions to the
   schema language.
2. **CLI (code generation)** — participate in `zen generate` to emit artifacts from the schema.
3. **Runtime (ORM)** — install on the client to intercept queries, hook CRUD lifecycle events,
   transform SQL, add custom methods, or compute fields.

ZenStack's `plugin` replaces Prisma's `generator`. To declare/consume plugins in a schema see
`zenstack-schema-modeling`; this skill is about *authoring* them.

Packages: `@zenstackhq/orm` (runtime plugin types), `@zenstackhq/sdk` (CLI plugin types + ZModel
AST). Install the SDK as a dev dependency: `npm install -D @zenstackhq/sdk`.

## Declaring a plugin in ZModel

```zmodel
plugin myPlugin {
    provider = './my-plugin'   // local .ts/.js/.mts/.mjs file, a folder with an index, or an npm package
    output   = './generated'   // arbitrary key=value options, readable by the plugin
}
```

`provider` resolution order: local file path → folder with an index → npm package. CLI plugins must
be **ESM**; TypeScript providers are loaded via [jiti](https://github.com/unjs/jiti). The built-in
`@core/typescript` plugin runs automatically; `@core/prisma` emits a Prisma schema.

## Runtime plugins

A runtime plugin is an object implementing `RuntimePlugin` from `@zenstackhq/orm`. Define it three
ways; `definePlugin` gives the best type inference:

```ts
import { definePlugin, type RuntimePlugin } from '@zenstackhq/orm';

// plain object / definePlugin (recommended)
const plugin = definePlugin({ id: 'my-plugin', /* hooks… */ });

// or a class
class MyPlugin implements RuntimePlugin<typeof schema> {
    id = 'my-plugin';
    /* hooks… */
}
```

Install on the client (immutable — returns a new client, original unchanged); remove with
`$unuse(id)` / `$unuseAll()`. You can also pass `plugins: [...]` to the `ZenStackClient` constructor.

```ts
const db = new ZenStackClient(schema, { dialect });
const withPlugin = db.$use(plugin);              // new client
const plain = withPlugin.$unuse('my-plugin');    // remove by id
// or: new ZenStackClient(schema, { dialect, plugins: [plugin] });
```

Every plugin needs a unique `id`. Add any combination of the hooks below.

### `onQuery` — intercept ORM operations

Fires for ORM API calls only (`findMany`, `create`, …), **not** the query builder. Wrap, modify
args, short-circuit, or post-process results via `proceed`.

```ts
definePlugin({
    id: 'timing',
    onQuery: async ({ model, operation, args, proceed }) => {
        const start = Date.now();
        const result = await proceed(args);
        console.log(`${model}.${operation} took ${Date.now() - start}ms`);
        return result;
    },
});
```

### `onKyselyQuery` — intercept/transform SQL

The lowest-level hook: every DB access (ORM *and* query builder) flows through Kysely here, so you
can inspect or rewrite the SQL AST (`OperationNode`) before `proceed`. Good for soft-deletes,
injected filters, column transforms.

```ts
import type { OnKyselyQueryCallback } from '@zenstackhq/orm';

const hook: OnKyselyQueryCallback<typeof schema> = async ({ query, proceed }) => {
    // inspect/transform `query` (a Kysely OperationNode), e.g. with an OperationNodeTransformer
    return proceed(query);
};
definePlugin({ id: 'sql-rewrite', onKyselyQuery: hook });
```

### `onEntityMutation` — before/after create·update·delete

Lifecycle hooks around entity mutations, with lazy loaders for the affected rows.

```ts
definePlugin({
    id: 'audit',
    onEntityMutation: {
        runAfterMutationWithinTransaction: false, // default: run after the tx commits
        async beforeEntityMutation({ model, action, loadBeforeMutationEntities }) {
            // action: 'create' | 'update' | 'delete'
            if (model === 'Post' && action === 'update') {
                const before = await loadBeforeMutationEntities();
            }
        },
        async afterEntityMutation({ model, action, loadAfterMutationEntities }) {
            const after = await loadAfterMutationEntities();
        },
    },
});
```

Set `runAfterMutationWithinTransaction: true` to run the after-hook atomically inside the mutation's
transaction. Note: mutations triggered by DB cascades are **not** captured, and the loaders can be
expensive on bulk mutations.

### Extending the client (`client`)

Add custom methods/properties under `client`. Names **must be `$`-prefixed** so they don't shadow
model accessors; grouping under one `$namespace` object is recommended.

```ts
const cacheDb = db.$use(definePlugin({
    id: 'cache',
    client: {
        $cache: {
            get stats() { return { hits: 0, misses: 0 }; },
            async invalidate() { /* … */ },
        },
    },
}));
await cacheDb.$cache.invalidate();
```

### Custom query args (`queryArgs`)

Accept extra options on ORM calls, validated with a Zod schema. Target `$all`, the
`$create`/`$read`/`$update`/`$delete` groups, or specific operations.

```ts
import { z } from 'zod';

definePlugin({
    id: 'cache',
    queryArgs: {
        $read: z.object({ cache: z.strictObject({ ttl: z.number().positive().optional() }).optional() }),
    },
    onQuery: ({ args, proceed }) => proceed(args), // read (args as any).cache
});
// await db.user.findMany({ where: {...}, cache: { ttl: 60 } });
```

### Computed result fields (`result`, v3.5.0+)

Add virtual fields computed after a query from declared `needs` fields.

```ts
definePlugin({
    id: 'full-name',
    result: {
        user: {
            fullName: {
                needs: { firstName: true, lastName: true },
                compute: (user) => `${user.firstName} ${user.lastName}`,
            },
        },
    },
});
```

## CLI plugins (code generation)

A CLI plugin is an ESM module whose **default export** is a `CliPlugin` with a `generate` callback.
It runs during `zen generate`, receiving the parsed ZModel AST.

```ts
import type { CliPlugin } from '@zenstackhq/sdk';
import { isDataModel, type InvocationExpr } from '@zenstackhq/sdk/ast';
import fs from 'node:fs';

const plugin: CliPlugin = {
    name: 'Password Report',
    // statusText is optional
    generate: ({ model, defaultOutputPath, pluginOptions }) => {
        if (pluginOptions['report'] !== true) return;       // options come from the ZModel plugin block
        let out = '# Password Fields\n\n';
        for (const dm of model.declarations.filter(isDataModel)) {
            for (const field of dm.fields) {
                const attr = field.attributes.find((a) => a.decl.$refText === '@password');
                if (attr) out += `- ${dm.name}.${field.name}\n`;
            }
        }
        fs.writeFileSync(`${defaultOutputPath}/password-fields.md`, out, 'utf-8');
    },
};
export default plugin;
```

`generate` receives `{ model, defaultOutputPath, pluginOptions }` — the ZModel AST, the resolved
output directory (the `output` option or a default), and the options from the `plugin` block.

## Schema plugins (custom attributes & functions)

Declare new ZModel attributes/functions in a `.zmodel` the plugin ships, then use them in the app
schema. `@@@targetField` constrains where an attribute applies.

```zmodel
// my-plugin/plugin.zmodel
attribute @password(hasher: Any) @@@targetField([StringField])
function bcryptHasher(rounds: Int): Any {}
```

```zmodel
// app schema
model User {
    id       Int    @id @default(autoincrement())
    password String @password(hasher: bcryptHasher(10))
}
```

## End-to-end pattern: password hasher

The docs' worked example combines all three levels into one plugin package:

1. **Schema** — `plugin.zmodel` defines `@password` + `bcryptHasher()`; the app schema applies
   `@password(hasher: bcryptHasher(10))` to a field.
2. **CLI** — a `CliPlugin.generate` walks the AST and emits a "password fields" report when the
   `report` option is set.
3. **Runtime** — a `RuntimePlugin` with `onKyselyQuery` uses a Kysely `OperationNodeTransformer` to
   detect `@password` fields (via `schema.models[...].fields[...].attributes`) and hash values on
   `INSERT`/`UPDATE` before they hit the database.

Install with `db.$use(new PasswordHasherPlugin())` (or the `plugins` constructor option), then
`npm install -D @zenstackhq/sdk` and `zen generate` to run the CLI side.

> Use **Zod v4** for `queryArgs` schemas to match ZenStack's bundled version.

## Reference docs

Full ZenStack documentation for this topic is bundled under [`references/`](references/):

- [plugin-dev.md](references/plugin-dev.md) — end-to-end plugin development guide
- [runtime-plugins-overview.md](references/runtime-plugins-overview.md) — runtime plugin model
- [extending-orm-client.md](references/extending-orm-client.md) — client methods, query args, computed fields
- [entity-mutation-hooks.md](references/entity-mutation-hooks.md) — before/after mutation hooks
- [kysely-query-hooks.md](references/kysely-query-hooks.md) — `onKyselyQuery` SQL transformation
- [query-api-hooks.md](references/query-api-hooks.md) — `onQuery` ORM interception
- [zmodel-plugin.md](references/zmodel-plugin.md) — declaring plugins in ZModel
- [zmodel-plugin-reference.md](references/zmodel-plugin-reference.md) — `plugin` block reference
