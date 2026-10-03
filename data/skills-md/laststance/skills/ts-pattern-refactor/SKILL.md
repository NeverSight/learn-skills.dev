---
name: ts-pattern-refactor
description: Refactor branches to ts-pattern
---

# ts-pattern Refactor

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Convert error-prone conditional code to `match().with().exhaustive()` — without over-applying it.

## When to Use

- Sweeping a TS/React codebase for ts-pattern opportunities
- A discriminated union (`{ kind: ... }`, `status: 'a' | 'b' | ...`) has grown new variants and the UI dispatch is scattered
- Reviewing JSX with nested ternaries or `&&` fragment chains keyed off the same discriminator

## Judgment Criteria

The number of branches alone is **not** the trigger. Look at **syntactic form × context**.

| Pattern | Refactor? | Why |
|---|---|---|
| JSX dispatch on a discriminator (renders different elements per variant) | **Yes** | JSX edits are visually noisy; ts-pattern keeps each branch's structure parallel |
| Nested ternary (`a ? x : b ? y : z`) | **Yes** | Hard to edit; format breaks easily on add/remove |
| Repeated `{x === 'a' && ...}{x === 'b' && ...}` chains on the same discriminator | **Yes** | Implicit fall-through bugs; ts-pattern enforces exhaustiveness |
| Discriminated union with 4+ variants, dispatched anywhere | **Yes** | `.exhaustive()` catches missing variants at compile time |
| Plain TS `if (x.kind === 'a') return ...; if (x.kind === 'b') return ...` | **No** | Single-condition if-chains are structurally hard to break — leave them |
| 2-3 branch simple if/else or switch | **No** | Per react-rules.md: ts-pattern is for 4+ cases / discriminated unions |
| Single-case `{status === 'x' && <Block />}` | **No** | One condition is fine as `&&` |

**Rule of thumb:** if a future variant addition could silently fall through the existing code, refactor. If the structure prevents that already, leave it.

## Workflow

### Phase 1 — Detect

Run these greps from repo root. Each surfaces a different smell:

```bash
# Nested ternaries — a ? b : c ? d : e
rg -n --type ts --type tsx '\?\s*[^?:]+:\s*[^?:]+\?\s*[^?:]+:' src/

# Repeated `===` checks on the same discriminator (status, kind, type)
rg -n --type tsx '(status|kind|type)\s*===\s*' src/ | awk -F: '{print $1":"$2}' | sort | uniq -c | sort -rn | head -20

# JSX `&&` chains on a discriminator (heuristic — review hits)
rg -n --type tsx '\{\s*\w+\s*===\s*[\x27"]\w+[\x27"]\s*&&' src/

# Existing ts-pattern usage (skip files that are already migrated)
rg -l 'from .ts-pattern.' src/
```

For discriminated-union sites, use Serena to find every dispatch:

```
mcp__serena__find_referencing_symbols { name_path: "UpdateStatus", relative_path: "src/shared/types.ts" }
```

Read `~/.claude/projects/<this-project>/memory/feedback_ts_pattern_threshold.md` if present — it records earlier decisions on this same codebase.

### Phase 2 — Apply

Use Context7 (`mcp__context7__query-docs` with library `/gvergnaud/ts-pattern`) for current API. Common conversions:

**Nested ternary → match**

```tsx
// Before
const label = status === 'error' ? error
  : status === 'available' ? `Version ${v} available`
  : status === 'downloading' ? `Downloading ${v}...`
  : `Version ${v} ready`

// After
const label = match(status)
  .with('error', () => error)
  .with('available', () => `Version ${v} available`)
  .with('downloading', () => `Downloading ${v}...`)
  .with('ready', () => `Version ${v} ready to install`)
  .exhaustive()
```

**JSX if-chain on discriminated union → match**

```tsx
// Before
if (content.kind === 'empty') return <EmptyState />
if (content.kind === 'binary') return <BinaryPlaceholder {...content} />
if (content.kind === 'image') return <img src={content.data.dataUrl} />
return <TextPreview content={content.data.content} />

// After
return match(content)
  .with({ kind: 'empty' }, () => <EmptyState />)
  .with({ kind: 'binary' }, ({ fileName, size }) => <BinaryPlaceholder fileName={fileName} size={size} />)
  .with({ kind: 'image' }, ({ data }) => <img src={data.dataUrl} alt={data.name} />)
  .with({ kind: 'text' }, ({ data }) => <TextPreview content={data.content} />)
  .exhaustive()
```

**Multiple values, same branch:**

```tsx
.with('available', 'downloading', () => <Download className="..." />)
```

**Add a one-line comment** above each `match()` block stating *why* the call site is exhaustive (e.g. "narrowed to four visible phases above"). Future readers should see at a glance that adding a variant breaks compilation here.

### Phase 3 — Verify

Run in parallel; each must pass:

```bash
pnpm typecheck   # exhaustiveness errors surface here
pnpm lint
pnpm test        # vitest run (includes browser mode)
```

If the project has e2e:

```bash
npx tsc -p e2e/tsconfig.json --noEmit  # e2e has its own tsconfig
pnpm test:e2e
```

Any failure → fix or revert that single file → re-run only the failing check.

## Things NOT to Do

- **Don't refactor plain TS single-condition if-chains.** They're structurally safe; ts-pattern just adds a dependency without preventing real bugs.
- **Don't add `.otherwise(() => null)` to silence exhaustiveness errors.** That defeats the purpose. Either handle the variant or use `.exhaustive()` and let the compiler complain.
- **Don't refactor 2-3 branch logic.** react-rules.md draws the line at 4+ — respect it.
- **Don't combine the refactor with unrelated cleanups.** One concern per commit; reviewers can verify behavior parity.

## References

- Project rule: `~/.claude/rules/react-rules.md` — "ts-pattern Usage" section
- ts-pattern docs (live): Context7 `/gvergnaud/ts-pattern`
- Validated examples in `skills-desktop`:
  - `src/renderer/src/components/UpdateToast.tsx` — 6-state union, four match blocks
  - `src/renderer/src/components/skills/FileContent.tsx` — 4-variant `PreviewContent` JSX dispatch
- Counter-example (intentionally not refactored): `src/renderer/src/components/skills/agentSelectionHelpers.ts:getOccupiedAgentReason` — plain TS single-condition if-chain
