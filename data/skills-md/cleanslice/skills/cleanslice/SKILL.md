---
name: cleanslice
description: CleanSlice architecture for NestJS + Nuxt full-stack apps. Use for vertical slice features, gateway pattern, Provider.vue, Pinia stores, DTOs, or any CleanSlice project work.
---

# CleanSlice

---

## Quick Start

CleanSlice organizes code into **vertical slices** — self-contained feature modules following Clean Architecture.

**Fixed stack:** NestJS + Prisma (API) · Nuxt 3 + Vue 3 + Pinia (App) · Tailwind + shadcn-vue (UI)

---

## Quick Reference

| Need | Answer |
|------|--------|
| Slice folder name | SINGULAR: `user/` not `users/` |
| Route/page files | PLURAL: `/users`, `users.vue` |
| DTO file name | camelCase: `createUser.dto.ts` |
| Data access layer | Gateway (NOT Repository) |
| State management | Pinia `stores/` (NOT composables) |
| Component entry | `Provider.vue` required in every folder |
| DI tokens | Abstract class with `I` prefix: `IUserGateway` |
| Backend order | schema → types → gateway → service → mapper → dtos → controller → module |
| Frontend order | nuxt.config → stores → components → pages |
| Implementation order | API first, then App |

---

## Bundled Resources

**References** (`references/`):

- `workflow.md` — Four-phase workflow, fix-bug workflow, git commits, system prompt
- `backend.md` — NestJS slice structure, module, controller, service, gateway, mapper, DTOs, types
- `frontend.md` — Nuxt slice structure, auto-imports, Provider.vue, stores, composables
- `gateway.md` — Gateway pattern with full code examples (abstract class, DI wiring)
- `typescript.md` — TypeScript standards (no-any, I prefix, Types suffix, import aliases)
- `errors.md` — Error pattern (BaseError, domain errors, interceptor, no try/catch in controllers)

---

## When to Load References

1. **Load `references/workflow.md` when:**
   - Starting any new feature, project, or bug fix
   - User asks how to plan or structure work
   - Need the four-phase workflow or system prompt
   - **Trigger phrases:** "new feature", "add", "create", "build", "implement", "plan", "start"

2. **Load `references/backend.md` when:**
   - Implementing any API slice (NestJS)
   - Writing controllers, gateways, mappers, DTOs, modules
   - Questions about backend file structure or standards
   - **Trigger phrases:** "controller", "DTO", "module", "NestJS", "API", "endpoint", "Prisma"

3. **Load `references/frontend.md` when:**
   - Implementing any App slice (Nuxt)
   - Writing stores, components, pages, composables
   - Questions about auto-imports, Provider.vue, or Pinia
   - **Trigger phrases:** "store", "page", "component", "Nuxt", "Vue", "Provider", "frontend"

4. **Load `references/gateway.md` when:**
   - Implementing data access layer
   - Questions about Gateway vs Repository
   - DI injection tokens and abstract class pattern
   - **Trigger phrases:** "gateway", "repository", "data layer", "inject", "DI"

5. **Load `references/typescript.md` when:**
   - Questions about naming conventions or TypeScript rules
   - Writing interfaces, enums, types, or imports
   - Any code review or standards check
   - **Trigger phrases:** "interface", "enum", "type", "naming", "any", "import alias", "standards"

6. **Load `references/errors.md` when:**
   - Implementing error handling in any slice
   - Creating domain error classes
   - Questions about where errors belong or how they flow
   - **Trigger phrases:** "error", "exception", "throw", "not found", "catch", "BaseError"

---

## Critical Rules

### Mandatory Four-Phase Workflow

Every task follows these phases — **stop and wait for user approval between each**:

| Phase | What You Do | End With |
|-------|-------------|----------|
| **Phase 1** | High-level plan: slices, pages, endpoints (NO file paths) | "Do you approve?" → STOP |
| **Phase 2** | Detailed plan: file paths, schemas, components, DTOs | "Do you approve?" → STOP |
| **Phase 3** | Implementation: API first, then App | — |
| **Phase 4** | Review: validate against patterns, plan next iteration | "STOP or continue?" → STOP |

### Technology Stack (FIXED — Never Ask)

```
api/    → NestJS + Prisma
app/    → Nuxt 3 + Vue 3 + Pinia
styling → Tailwind + shadcn-vue
db      → PostgreSQL (SQLite for dev)
```

### Slice Structure

```
API slice                           App slice
api/src/slices/{slice}/             app/slices/{slice}/
├── {slice}.module.ts               ├── nuxt.config.ts
├── {slice}.controller.ts           ├── pages/
├── domain/                         │   ├── {slices}.vue        ← plural
│   ├── {slice}.types.ts            │   └── {slices}/[id].vue
│   ├── {slice}.service.ts          ← optional, for business logic
│   └── {slice}.gateway.ts          ├── components/
├── data/                           │   └── {slice}/
│   ├── {slice}.gateway.ts          │       ├── Provider.vue    ← REQUIRED
│   └── {slice}.mapper.ts           │       └── Layout.vue
└── dtos/                           ├── stores/
    ├── {slice}.dto.ts              │   └── {slice}.ts
    └── create{Slice}.dto.ts        └── composables/
```

---

## Forbidden Patterns

| Wrong | Correct |
|-------|---------|
| `.repository.ts` | `.gateway.ts` |
| `AiService`, `ChatService` (data access) | `AiGateway`, `ChatGateway` — external integrations are gateways |
| `UserRepository` | `UserGateway` (Prisma IS the repository) |
| `composables/useChat.ts` for state | `stores/chat.ts` |
| `create-message.dto.ts` | `createMessage.dto.ts` |
| `ChatWindow.vue` | `chat/Provider.vue` |
| `features/` | `slices/` |
| `hooks/` | `stores/` |
| React / Next.js / Vite | Nuxt |
| Express | NestJS |
| TypeORM | Prisma |
| Vanilla CSS | Tailwind + shadcn-vue |
| File paths in Phase 1 | Save for Phase 2 |

---

## Git Commit Format

```
<type>: <description>
```

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change, no feature/fix |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |

Add `!` for breaking changes: `feat!: change response format`

Rules: lowercase · no period · imperative mood · under 72 chars

---

## Official Documentation

- CleanSlice Docs: https://cleanslice.org
- CleanSlice MCP: https://mcp.cleanslice.org
- GitHub: https://github.com/CleanSlice/nest-nuxt-starter-kit
