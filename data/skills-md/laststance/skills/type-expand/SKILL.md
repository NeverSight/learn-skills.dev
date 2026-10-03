---
name: type-expand
description: Expand TS aliases to shapes
---

# Type Expand

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.

## Purpose

Use this skill to inspect the real shape of complex TypeScript types when IDE hover is not enough.

## Inputs

Use one of these:
- Selected code that includes a target type alias.
- `filePath` + `typeName`.
- A direct alias snippet (`export type X = ...`).

## Workflow

1. Identify target alias name and source file.
2. Run the expander script:

```bash
pnpm exec tsx ~/.agents/skills/type-expand/scripts/expand-type.ts --file <filePath> --type <typeName>
```

（Claude Code: `~/.claude/skills/...`、Cursor: `~/.cursor/skills/...` または `.cursor/skills/...` に symlink される）

3. If project root cannot be inferred, pass tsconfig path:

```bash
pnpm exec tsx ~/.agents/skills/type-expand/scripts/expand-type.ts --file <filePath> --type <typeName> --project <tsconfigPath>
```

4. Return output in this format:

```ts
export type <TypeName> =
| <expanded object type>
| <expanded object type>
```

5. If part of the type cannot be fully resolved, keep best-effort expansion and annotate unresolved fragments inline.

## Expansion Policy

- Prefer concrete object property expansion over alias names.
- Recursively expand unions/intersections.
- Expand instantiated generics where type arguments are known.
- Resolve conditional types (`extends`) and infer-derived parts when checker provides concrete results.
- Flatten common utility-type transformations when symbol/property info is available (`Pick`, `Omit`, `Partial`, `Required`, `Readonly`, `Record`, `Exclude`, `Extract`, `NonNullable`).
- Enforce depth and cycle guards to prevent runaway expansion.

## Output Style

- Keep property names stable and readable.
- Preserve optional (`?`) and readonly modifiers when detectable.
- Use `unknown` for recursion/depth guard fallbacks.

## Additional Resource

- See [reference.md](reference.md) for command examples and troubleshooting.
