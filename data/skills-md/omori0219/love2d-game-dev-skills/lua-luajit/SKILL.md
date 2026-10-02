---
name: lua-luajit
description: Use this skill when writing, reviewing, debugging, or refactoring Lua intended for LuaJIT 2.1 / Lua 5.1-compatible runtimes, including LÖVE/Love2D projects that use LuaJIT or Lua 5.1-style Lua. Apply LuaJIT-conscious syntax, local-first scoping, table-returning modules, consistent method syntax, predictable table/array handling, nil-safe logic, and avoid Lua 5.2/5.3/5.4-only features unless the project explicitly supports them.
---

# LuaJIT / Lua 5.1 Compatibility Skill

Use this skill to produce conservative, maintainable Lua intended for LuaJIT 2.1 and Lua 5.1-compatible runtimes. It is especially intended for game projects such as LÖVE/Love2D when the target build uses LuaJIT or Lua 5.1-style Lua, where AI coding agents must avoid accidentally emitting newer Lua syntax or fragile Lua patterns.

## Scope

This skill covers:

- LuaJIT 2.1 / Lua 5.1-compatible syntax and runtime assumptions.
- Safe Lua coding conventions for AI-generated code.
- Review and debugging checks for common Lua mistakes.
- Small-to-medium modules, gameplay scripts, utility modules, and refactors.

This skill does **not** cover:

- LÖVE/Love2D API rules. Use a separate Love2D skill for `love.load`, `love.update`, `love.draw`, assets, input, filesystem, and release behavior.
- Advanced LuaJIT FFI usage unless the user explicitly asks for it.
- A single mandatory architecture for every Lua project.
- A guarantee that every LÖVE/Love2D build uses LuaJIT or the same bytecode/runtime behavior. Verify the target LÖVE version and platform when that matters.

When the project already has a style, follow the existing project style first, then apply this skill as compatibility and safety guardrails.

## Operating Principles

When writing or changing Lua code:

1. **Target LuaJIT 2.1 / Lua 5.1 by default.** Do not use Lua 5.2+ syntax or libraries unless the project already uses them or the user explicitly permits them.
2. **Preserve existing project conventions.** Before changing code, inspect how modules, methods, arrays, globals, and errors are handled nearby.
3. **Make the smallest safe change.** Avoid broad rewrites unless the user asks for a refactor.
4. **Prefer clarity over cleverness.** Lua metatables, coroutines, and FFI are powerful, but should not be introduced casually.
5. **Explain compatibility assumptions when relevant.** If a proposed solution depends on a LuaJIT extension, say so.
6. **Respond in the user's language.** Keep code comments in the project's existing language unless the user asks otherwise.

## Non-Negotiable Rules

### 1. Use `local` by default

- Declare variables, functions, and module imports as `local` unless a global is intentionally required.
- Never create accidental globals through assignment.
- Treat undeclared assignment as a bug unless the project clearly uses a global namespace pattern.

### 2. Avoid Lua 5.2+ assumptions by default

Do not use these unless the project explicitly supports them:

- `_ENV`
- `goto`
- `table.pack` / `table.unpack` as a default API assumption
- `utf8` library
- `//` integer division
- bitwise operators such as `&`, `|`, `~`, `<<`, `>>`
- to-be-closed variables such as `<close>`
- Lua 5.4-style warnings or attributes

For bitwise operations on LuaJIT, prefer `local bit = require("bit")` and use `bit.band`, `bit.bor`, `bit.bxor`, `bit.lshift`, etc.

### 3. Use simple table-returning modules

Prefer this module shape unless the project uses another clear convention:

- Import dependencies with `local`.
- Create a local module table.
- Define module functions on the table.
- Return the table at the end.
- Avoid module-level side effects beyond simple constants or setup.

See `examples/clean-module.lua` when a concrete shape is useful.

### 4. Keep `:` and `.` method syntax consistent

- Use `function obj:method(...)` when the function expects `self`.
- Call it as `obj:method(...)`.
- Use `function obj.method(obj, ...)` only when the project already prefers explicit `self`.
- Do not define with `:` and call with `.` unless intentionally passing `self` manually.

### 5. Treat Lua truthiness correctly

- Only `nil` and `false` are false.
- `0`, `""`, empty tables, and empty strings are truthy.
- Do not write logic that assumes JavaScript/Python-style falsiness.

### 6. Keep array-like tables dense

- Lua arrays are conventionally 1-indexed dense sequences.
- Avoid holes such as `items[3] = nil` when using `#items` or `ipairs`.
- Use explicit counters or map tables when sparse keys are required.
- Do not rely on `#t` for sparse tables.

### 7. Use `pairs` and `ipairs` intentionally

- Use `ipairs` for dense array-like sequences.
- Use `pairs` for dictionaries/maps.
- Do not rely on iteration order from `pairs`.

### 8. Be careful with multiple return values

- In Lua, function calls may expand to multiple values only in specific expression-list positions.
- Parenthesized function calls collapse to one value.
- Capture values explicitly when clarity matters.

See `examples/multiple-returns.lua` for review examples.

### 9. Avoid unsafe or environment-sensitive APIs unless asked

Do not introduce these casually:

- `loadstring`, `load`, or bytecode loading.
- `debug` library usage.
- LuaJIT `ffi`.
- `os.execute` or shell calls.
- Global monkey-patching of standard libraries.

If the user asks for one of these, explain the risk and keep the change narrowly scoped.

### 10. Do not overuse metatables

Use metatables only when they provide clear value and the project already supports the pattern. For beginner-facing or AI-maintained code, prefer plain tables and explicit functions.

## Review Checklist

When reviewing Lua code, check the following before giving a final answer:

- Are there accidental globals?
- Is the code compatible with LuaJIT 2.1 / Lua 5.1?
- Are module imports and helper functions local?
- Are `:` and `.` calls consistent?
- Are dense arrays kept dense?
- Is `#` used only on proper sequences?
- Does the code rely on `pairs` order?
- Are `nil` and `false` handled correctly?
- Are multiple return values handled intentionally?
- Did the change avoid unnecessary metatables, FFI, debug APIs, and shell execution?
- Did the change preserve the existing project style?

## When More Detail Is Needed

Load these references only when relevant:

- `references/compatibility.md` — LuaJIT 2.1 / Lua 5.1 compatibility assumptions.
- `references/style-guide.md` — default coding conventions for AI-written Lua.
- `references/common-pitfalls.md` — common bugs and how to avoid them.
- `references/review-checklist.md` — more detailed review procedure.
- `references/sources.md` — official references used to build this skill.
- `examples/` — small examples showing recommended shapes.

## Response Style

When using this skill, keep responses practical:

- For implementation tasks: make the change, then briefly mention any LuaJIT/Lua 5.1 compatibility concern.
- For review tasks: list concrete issues first, then suggested fixes.
- For debugging tasks: identify the likely Lua-specific cause before proposing broader architecture changes.
- Do not lecture the user with a full Lua tutorial unless they ask for one.
