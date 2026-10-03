---
name: colorful-type
description: Brand TS types
---

# Colorful Type

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Replace colorless primitives with domain-rich types. Every `string` answers: **"string of WHAT?"** Every `number` answers: **"number of WHAT?"**

TypeScript types are human-readable annotations. They communicate what domain concept a value represents, where it belongs (UI/logic/data/config), and what constraints apply.

## When to Use

- Codebase has `string`, `number`, `boolean` params that represent domain concepts (IDs, names, statuses, counts)
- `ReturnType<typeof fn>` or `Parameters<typeof fn>[0]` used where a named type should exist
- Code review or onboarding reveals type signatures don't communicate domain intent
- After a major feature lands and types need hardening

### Do NOT Use When

- Prototyping or spike (premature type hardening slows exploration)
- Generic utility functions (`identity<T>`, `debounce`, `pipe`) — these legitimately use primitives/generics
- Test fixtures and mocks (test-internal types are fine as primitives)

## Transformation Targets

| Target | Before (Colorless) | After (Colorful) | Priority |
|--------|-------------------|-------------------|----------|
| ID fields | `id: string` | `id: UserId` (branded) | HIGH |
| Status/enum | `status: string` | `status: SymlinkStatus` | HIGH |
| Domain strings | `name: string` | `name: User['displayName']` | HIGH |
| Utility types | `ReturnType<typeof getUser>` | `User` | MEDIUM |
| Callbacks | `(data: any) => void` | `(skill: Skill) => void` | MEDIUM |
| Domain numbers | `count: number` | `count: Agent['skillCount']` | MEDIUM |
| Booleans | `isValid: boolean` | `isValid: Symlink['isValid']` | LOW |

### Leave Alone

- Loop counters, array indices (`i: number`)
- Generic type parameters (`<T>`, `<K extends string>`)
- Third-party library type boundaries
- Temporary computation variables (`const sum: number = a + b`)
- String literals in template expressions

## Workflow

### Phase 1: Explore (Parallel Subagents)

Launch 3 Explore subagents in parallel:

**Agent A — Domain Type Inventory:**
Find all `type`/`interface` definitions. List domain types with fields and JSDoc presence. Identify root entities vs derived types.

**Agent B — Primitive Usage Map:**
Search `: string`, `: number`, `: boolean` in function signatures, variable declarations, interface fields. EXCLUDE: type definition files themselves, generics, test files. Group by domain concept.

**Agent C — Utility Type Audit:**
Search `ReturnType<`, `Parameters<`, `Awaited<`, `Partial<`, `Pick<` and index access patterns. Identify which could be replaced with named types.

### Phase 2: Enrich Base Types with JSDoc

For each domain type definition:

```typescript
// BEFORE
interface Skill {
  name: string;
  path: string;
  version: number;
}

// AFTER
/**
 * A reusable AI agent capability package containing a SKILL.md manifest.
 * Symlinked into agent skill directories for cross-agent sharing.
 * @example { name: "tdd-workflow", path: "~/.agents/skills/tdd-workflow", version: 2 }
 */
interface Skill {
  /** Human-readable identifier matching the directory name. @example "tdd-workflow" */
  name: string;
  /** Absolute filesystem path to the skill directory. @example "~/.agents/skills/tdd-workflow" */
  path: string;
  /** Schema version of the SKILL.md manifest format (currently 1 or 2). */
  version: number;
}
```

Every JSDoc includes: `@description` (domain meaning), `@example` (realistic value). Property-level JSDoc for each field.

### Phase 3: Create Branded & Named Types

```typescript
// === Branded types — prevent mixing IDs across domains ===
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, 'UserId'>;
type SkillId = Brand<string, 'SkillId'>;
type AgentId = Brand<string, 'AgentId'>;
type Timestamp = Brand<number, 'Timestamp'>;

// === Union types — finite domain values ===
type SymlinkStatus = 'valid' | 'broken' | 'missing';
type ThemeMode = 'light' | 'dark' | 'system';

// === Indexed access — "a field of a known entity" ===
type SkillName = Skill['name'];
type AgentDir = AgentConfig['dir'];
```

**Decision rule:**
- Value is an ID → Branded type (prevents mixing `UserId` and `SkillId`)
- Value is one of finite set → Union/enum type
- Value is a field of a known entity → Indexed access type
- Otherwise → New named type alias in shared types

### Phase 4: Batch Replacement

Replace all primitives in one pass, ordered by scope:

1. **Function signatures** — parameters and return types
2. **Interface/type fields** — in non-root types that USE domain types
3. **Variable declarations** — explicit annotations
4. **State shapes** — Redux/Zustand payloads, selectors
5. **IPC/API types** — communication boundaries

**Rules:**
- Named domain type exists → use directly (`UserId`, `SymlinkStatus`)
- Value is a field of known entity → index access (`Skill['name']`)
- Neither → create new named type in shared types file
- NEVER use `as` casts — fix the source
- NEVER change runtime behavior — annotation-only changes

### Phase 5: Verify

```bash
pnpm typecheck   # or tsc --noEmit — zero errors required
pnpm lint        # no new warnings
```

Generate transformation report:
- Primitives replaced (count by type and domain concept)
- JSDoc annotations added/enriched
- New named/branded types created
- Remaining primitives with justification

## Acceptance Criteria

- Zero typecheck errors
- Every domain entity type has JSDoc with `@description` and `@example`
- No `string` represents a domain concept (IDs, names, paths, statuses)
- No `number` represents a domain quantity (counts, versions, timestamps)
- No `ReturnType<typeof fn>` where a named type exists
- Transformation report presented to user

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Replace ALL primitives including loop counters | Only replace at domain boundaries — leave generic computation alone |
| Create branded type for every single string field | Only brand when mixing is dangerous (IDs). Use index access for simple fields |
| Add `as UserId` casts everywhere | Create factory functions: `const userId = (id: string): UserId => id as UserId` |
| Modify runtime behavior while refactoring types | Type-only changes. If a test behavior changes, you went too far |
| Over-nest index access: `Config['db']['host']` | Create named alias: `type DbHost = Config['db']['host']` for readability |
| Skip JSDoc on "obvious" types | Domain meaning is never obvious to newcomers. Always document the WHY |

## Scope Boundaries

- Do NOT modify third-party library type definitions
- Do NOT add runtime type checking (compile-time only)
- Do NOT change any runtime behavior
- Do NOT over-abstract: single-use types can stay inline
- Do NOT touch test files unless they export types used in production
