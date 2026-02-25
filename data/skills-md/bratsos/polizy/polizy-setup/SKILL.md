---
name: polizy-setup
description: Setup and installation guide for polizy authorization library. Use when adding authorization to a project, installing polizy, choosing storage adapters, or setting up for the first time.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Setup

Guide for installing and configuring polizy in your project.

## When to Apply

- User says "add authorization to my project"
- User says "install polizy" or "set up polizy"
- User has no existing polizy configuration
- User asks about initial setup or storage selection
- User is starting a new project with authorization needs

## Priority Table

| Priority | Task | Notes |
|----------|------|-------|
| Critical | Install package | `npm install polizy` |
| Critical | Define schema | Relations, actions, mappings |
| Critical | Choose storage | InMemory (dev) or Prisma (prod) |
| Important | Test setup | Verify with a permission check |
| Optional | Configure options | Depth limits, logging |

## Step-by-Step Setup

### Step 1: Install

```bash
npm install polizy
# or
pnpm add polizy
# or
yarn add polizy
```

### Step 2: Define Schema

Create your authorization model:

```typescript
import { defineSchema } from "polizy";

const schema = defineSchema({
  // Define relationship types
  relations: {
    owner: { type: "direct" },    // Direct user → resource
    editor: { type: "direct" },
    viewer: { type: "direct" },
    member: { type: "group" },    // Group membership
    parent: { type: "hierarchy" } // Folder → file
  },

  // Map actions to relations that grant them
  actionToRelations: {
    delete: ["owner"],
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"]
  },

  // Optional: How permissions propagate through hierarchies
  hierarchyPropagation: {
    view: ["view"],  // view on parent → view on children
    edit: ["edit"]
  }
});
```

### Step 3: Choose Storage Adapter

**For development/testing:**
```typescript
import { InMemoryStorageAdapter } from "polizy";

const storage = new InMemoryStorageAdapter();
```

**For production (Prisma):**
```typescript
import { PrismaAdapter } from "polizy/prisma-storage";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const storage = PrismaAdapter(prisma);
```

See [PRISMA-SETUP.md](references/PRISMA-SETUP.md) for Prisma model requirements.

### Step 4: Create AuthSystem

```typescript
import { AuthSystem } from "polizy";

const authz = new AuthSystem({
  storage,
  schema,
});
```

### Step 5: Verify Setup

```typescript
// Grant a permission
await authz.allow({
  who: { type: "user", id: "alice" },
  toBe: "owner",
  onWhat: { type: "document", id: "doc1" }
});

// Check it works
const canEdit = await authz.check({
  who: { type: "user", id: "alice" },
  canThey: "edit",
  onWhat: { type: "document", id: "doc1" }
});

console.log("Setup working:", canEdit); // true
```

## Storage Decision Matrix

| Factor | InMemoryStorageAdapter | PrismaAdapter |
|--------|----------------------|---------------|
| Persistence | No (lost on restart) | Yes |
| Multi-instance | No | Yes |
| Setup | Zero config | Requires Prisma model |
| Performance | Fastest | Database-dependent |
| Use case | Testing, dev | Production |

## Complete Minimal Setup

```typescript
// auth.ts
import {
  defineSchema,
  AuthSystem,
  InMemoryStorageAdapter
} from "polizy";

const schema = defineSchema({
  relations: {
    owner: { type: "direct" },
    viewer: { type: "direct" },
  },
  actionToRelations: {
    edit: ["owner"],
    view: ["owner", "viewer"],
  },
});

const storage = new InMemoryStorageAdapter();

export const authz = new AuthSystem({ storage, schema });
```

## Configuration Options

```typescript
const authz = new AuthSystem({
  storage,
  schema,

  // Optional: Max depth for group/hierarchy traversal (default: 10)
  defaultCheckDepth: 10,

  // Optional: Throw error instead of returning false on max depth
  throwOnMaxDepth: false,

  // Optional: Field separator for field-level permissions (default: "#")
  fieldSeparator: "#",

  // Optional: Custom logger
  logger: {
    warn: (msg) => console.warn("[Polizy]", msg)
  }
});
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Cannot find module 'polizy'" | Run `npm install polizy` |
| TypeScript errors in schema | Ensure `defineSchema` is imported from "polizy" |
| Prisma model not found | See [PRISMA-SETUP.md](references/PRISMA-SETUP.md) |
| Permission check returns false | Verify relation is in `actionToRelations` for that action |

## Next Steps

After setup, use these skills:
- **[polizy-schema](../polizy-schema/SKILL.md)** - Design your authorization model
- **[polizy-patterns](../polizy-patterns/SKILL.md)** - Implement authorization scenarios
- **[polizy-storage](../polizy-storage/SKILL.md)** - Production storage setup

## References

- [PRISMA-SETUP.md](references/PRISMA-SETUP.md) - Full Prisma configuration
- [FRAMEWORK-INTEGRATIONS.md](references/FRAMEWORK-INTEGRATIONS.md) - Next.js, Express examples
