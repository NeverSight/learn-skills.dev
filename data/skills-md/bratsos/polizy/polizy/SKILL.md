---
name: polizy
description: Router for polizy authorization library. Use when user mentions authorization, permissions, access control, RBAC, ReBAC, Zanzibar, or asks "who can do what" questions. Routes to specialized skills.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Authorization

Polizy is a Zanzibar-inspired authorization library for TypeScript/Node.js. It uses relationship tuples to define permissions.

## When to Apply

Activate this skill when:
- User mentions "polizy", "authorization", "permissions", "access control"
- User asks "who can do what", "can user X do Y"
- User wants RBAC, ReBAC, or Zanzibar-style authorization
- User needs to check, grant, or revoke permissions
- User is implementing team/group-based access
- User is implementing folder/file permission inheritance

## Quick Concepts

| Concept | Description |
|---------|-------------|
| **Tuple** | `(subject, relation, object)` - stored permission fact |
| **Subject** | Who: `{ type: "user", id: "alice" }` |
| **Object** | What: `{ type: "document", id: "doc1" }` |
| **Relation** | Role: `owner`, `editor`, `viewer`, `member`, `parent` |
| **Action** | Intent: `view`, `edit`, `delete` (mapped to relations) |

## Route to Specialized Skill

Based on user's task, use the appropriate skill:

### Installation & Setup
**Use:** `polizy-setup`
- "Add authorization to my project"
- "Install polizy"
- "Set up permissions system"
- First-time setup

### Schema Design
**Use:** `polizy-schema`
- "Design permissions schema"
- "What relations do I need"
- "Add new relation type"
- Defining or modifying the authorization model

### Implementation Patterns
**Use:** `polizy-patterns`
- "How do I implement X"
- "Give team access to project"
- "Make files inherit folder permissions"
- "Grant temporary access"
- Any specific authorization scenario

### Storage & Persistence
**Use:** `polizy-storage`
- "Set up database storage"
- "Use Prisma with polizy"
- "Create custom storage adapter"
- Production deployment

### Debugging & Issues
**Use:** `polizy-troubleshooting`
- "Permission check not working"
- "User can't access X but should"
- Error messages
- Unexpected authorization behavior

## Minimal Example

```typescript
import { defineSchema, AuthSystem, InMemoryStorageAdapter } from "polizy";

// 1. Define schema
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

// 2. Create AuthSystem
const authz = new AuthSystem({
  storage: new InMemoryStorageAdapter(),
  schema,
});

// 3. Grant permission
await authz.allow({
  who: { type: "user", id: "alice" },
  toBe: "owner",
  onWhat: { type: "document", id: "doc1" },
});

// 4. Check permission
const canEdit = await authz.check({
  who: { type: "user", id: "alice" },
  canThey: "edit",
  onWhat: { type: "document", id: "doc1" },
});
// => true
```

## Related Skills

- [polizy-setup](../polizy-setup/SKILL.md) - Installation and configuration
- [polizy-schema](../polizy-schema/SKILL.md) - Schema design
- [polizy-patterns](../polizy-patterns/SKILL.md) - Implementation patterns
- [polizy-storage](../polizy-storage/SKILL.md) - Storage adapters
- [polizy-troubleshooting](../polizy-troubleshooting/SKILL.md) - Debugging
