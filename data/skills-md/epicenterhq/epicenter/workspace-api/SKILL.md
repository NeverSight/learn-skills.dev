---
name: workspace-api
description: Workspace API patterns for defineTable, defineKv, versioning, and migrations. Use when defining workspace schemas, adding versions to existing tables/KV stores, or writing migration functions.
metadata:
  author: epicenter
  version: '4.0'
---

# Workspace API

Type-safe schema definitions for tables and KV stores with versioned migrations.

## When to Apply This Skill

- Defining a new table or KV store with `defineTable()` or `defineKv()`
- Adding a new version to an existing definition
- Writing migration functions
- Converting from shorthand to builder pattern

## Tables

### Shorthand (Single Version)

Use when a table has only one version:

```typescript
import { defineTable } from '@epicenter/workspace';
import { type } from 'arktype';

const usersTable = defineTable(type({ id: UserId, email: 'string', _v: '1' }));
export type User = InferTableRow<typeof usersTable>;
```

Every table schema must include `_v` with a number literal. The type system enforces this — passing a schema without `_v` to `defineTable()` is a compile error.

### Builder (Multiple Versions)

Use when you need to evolve a schema over time:

```typescript
const posts = defineTable()
	.version(type({ id: 'string', title: 'string', _v: '1' }))
	.version(type({ id: 'string', title: 'string', views: 'number', _v: '2' }))
	.migrate((row) => {
		switch (row._v) {
			case 1:
				return { ...row, views: 0, _v: 2 };
			case 2:
				return row;
		}
	});
```

## KV Stores

KV stores are flexible — `_v` is optional. Both patterns work:

### Without `_v` (field presence)

```typescript
import { defineKv } from '@epicenter/workspace';

const sidebar = defineKv(type({ collapsed: 'boolean', width: 'number' }));

// Multi-version with field presence
const theme = defineKv()
	.version(type({ mode: "'light' | 'dark'" }))
	.version(type({ mode: "'light' | 'dark' | 'system'", fontSize: 'number' }))
	.migrate((v) => {
		if (!('fontSize' in v)) return { ...v, fontSize: 14 };
		return v;
	});
```

### With `_v` (explicit discriminant)

```typescript
const theme = defineKv()
	.version(type({ mode: "'light' | 'dark'", _v: '1' }))
	.version(
		type({ mode: "'light' | 'dark' | 'system'", fontSize: 'number', _v: '2' }),
	)
	.migrate((v) => {
		switch (v._v) {
			case 1:
				return { ...v, fontSize: 14, _v: 2 };
			case 2:
				return v;
		}
	});
```

## Branded Table IDs (Required)

Every table's `id` field and every string foreign key field MUST use a branded type instead of plain `'string'`. This prevents accidental mixing of IDs from different tables at compile time.

### Pattern

Define a branded type + arktype pipe pair in the same file as the workspace definition:

```typescript
import type { Brand } from 'wellcrafted/brand';
import { type } from 'arktype';

// 1. Branded type + arktype pipe (co-located with workspace definition)
export type ConversationId = string & Brand<'ConversationId'>;
export const ConversationId = type('string').pipe(
	(s): ConversationId => s as ConversationId,
);

// 2. Wrap in defineTable + co-locate type export
const conversationsTable = defineTable(
	type({
		id: ConversationId,              // Primary key — branded
		title: 'string',
		'parentId?': ConversationId.or('undefined'),  // Self-referencing FK
		_v: '1',
	}),
);
export type Conversation = InferTableRow<typeof conversationsTable>;

const chatMessagesTable = defineTable(
	type({
		id: ChatMessageId,               // Different branded type
		conversationId: ConversationId,   // FK to conversations — branded
		role: "'user' | 'assistant'",
		_v: '1',
	}),
);
export type ChatMessage = InferTableRow<typeof chatMessagesTable>;

// 3. Compose in createWorkspace
export const workspaceClient = createWorkspace(
	defineWorkspace({
		tables: {
			conversations: conversationsTable,
			chatMessages: chatMessagesTable,
		},
	}),
);
```

### Rules

1. **Every table gets its own ID type**: `DeviceId`, `SavedTabId`, `ConversationId`, `ChatMessageId`, etc.
2. **Foreign keys use the referenced table's ID type**: `chatMessages.conversationId` uses `ConversationId`, not `'string'`
3. **Optional FKs use `.or('undefined')`**: `'parentId?': ConversationId.or('undefined')`
4. **Composite IDs are also branded**: `TabCompositeId`, `WindowCompositeId`, `GroupCompositeId`
5. **Brand at generation site**: When creating IDs with `generateId()`, cast through string: `generateId() as string as ConversationId`
6. **Functions accept branded types**: `function switchConversation(id: ConversationId)` not `(id: string)`

### Why Not Plain `'string'`

```typescript
// BAD: Nothing prevents mixing conversation IDs with message IDs
function deleteConversation(id: string) { ... }
deleteConversation(message.id);  // Compiles! Silent bug.

// GOOD: Compiler catches the mistake
function deleteConversation(id: ConversationId) { ... }
deleteConversation(message.id);  // Error: ChatMessageId is not ConversationId
```

### Reference Implementation

See `apps/tab-manager/src/lib/workspace.ts` for the canonical example with 7 branded ID types.

## Workspace File Structure

A workspace file has two layers:

1. **Table definitions with co-located types** — `defineTable(schema)` as standalone consts, each immediately followed by `export type = InferTableRow<typeof table>`
2. **`createWorkspace(defineWorkspace({...}))` call** — composes pre-built tables into the client

### Pattern

```typescript
import {
	createWorkspace,
	defineTable,
	defineWorkspace,
	type InferTableRow,
} from '@epicenter/workspace';

// ─── Tables (each followed by its type export) ──────────────────────────

const usersTable = defineTable(
	type({
		id: UserId,
		email: 'string',
		_v: '1',
	}),
);
export type User = InferTableRow<typeof usersTable>;

const postsTable = defineTable(
	type({
		id: PostId,
		authorId: UserId,
		title: 'string',
		_v: '1',
	}),
);
export type Post = InferTableRow<typeof postsTable>;

// ─── Workspace client ───────────────────────────────────────────────────

export const workspaceClient = createWorkspace(
	defineWorkspace({
		id: 'my-workspace',
		tables: {
			users: usersTable,
			posts: postsTable,
		},
	}),
);
```

### Why This Structure

- **Co-located types**: Each `export type` sits right below its `defineTable` — easy to verify 1:1 correspondence, easy to remove both together.
- **Error co-location**: If you forget `_v` or `id`, the error shows on the `defineTable()` call right next to the schema — not buried inside `defineWorkspace`.
- **Schema-agnostic inference**: `InferTableRow` works with any Standard Schema (arktype, zod, etc.) and handles migrations correctly (always infers the latest version's type).
- **Fast type inference**: `InferTableRow<typeof usersTable>` resolves against a standalone const. Avoids the expensive `InferTableRow<NonNullable<(typeof definition)['tables']>['key']>` chain that forces TS to resolve the entire `defineWorkspace` return type.
- **No intermediate `definition` const**: `defineWorkspace({...})` is inlined directly into `createWorkspace()` since it's only used once.

### Anti-Pattern: Inline Tables + Deep Indirection

```typescript
// BAD: Tables inline in defineWorkspace, types derived through deep indirection
const definition = defineWorkspace({
	tables: {
		users: defineTable(type({ id: 'string', email: 'string', _v: '1' })),
	},
});
type Tables = NonNullable<(typeof definition)['tables']>;
export type User = InferTableRow<Tables['users']>;

// GOOD: Extract table, co-locate type, inline defineWorkspace
const usersTable = defineTable(type({ id: UserId, email: 'string', _v: '1' }));
export type User = InferTableRow<typeof usersTable>;

export const workspaceClient = createWorkspace(
	defineWorkspace({ tables: { users: usersTable } }),
);
```

## The `_v` Convention

- `_v` is a **number** discriminant field (`'1'` in arktype = the literal number `1`)
- **Required for tables** — enforced at the type level via `CombinedStandardSchema<{ id: string; _v: number }>`
- **Optional for KV stores** — KV keeps full flexibility
- In arktype schemas: `_v: '1'`, `_v: '2'`, `_v: '3'` (number literals)
- In migration returns: `_v: 2` (TypeScript narrows automatically, `as const` is unnecessary)
- Convention: `_v` goes last in the object (`{ id, ...fields, _v: '1' }`)

## Migration Function Rules

1. Input type is a union of all version outputs
2. Return type is the latest version output
3. Use `switch (row._v)` for discrimination (tables always have `_v`)
4. Final case returns `row` as-is (already latest)
5. Always migrate directly to latest (not incrementally through each version)

## Anti-Patterns

### Incremental migration (v1 -> v2 -> v3)

```typescript
// BAD: Chains through each version
.migrate((row) => {
  let current = row;
  if (current._v === 1) current = { ...current, views: 0, _v: 2 };
  if (current._v === 2) current = { ...current, tags: [], _v: 3 };
  return current;
})

// GOOD: Migrate directly to latest
.migrate((row) => {
  switch (row._v) {
    case 1: return { ...row, views: 0, tags: [], _v: 3 };
    case 2: return { ...row, tags: [], _v: 3 };
    case 3: return row;
  }
})
```

### Note: `as const` is unnecessary

TypeScript contextually narrows `_v: 2` to the literal type based on the return type constraint. Both of these work:

```typescript
return { ...row, views: 0, _v: 2 }; // Works — contextual narrowing
return { ...row, views: 0, _v: 2 as const }; // Also works — redundant
```

## References

- `packages/epicenter/src/workspace/define-table.ts`
- `packages/epicenter/src/workspace/define-kv.ts`
- `packages/epicenter/src/workspace/index.ts`
- `packages/epicenter/src/workspace/create-tables.ts`
- `packages/epicenter/src/workspace/create-kv.ts`
