---
name: dayz-scripting
description: Enforce Script rules for DayZ mods — engine invariants, memory and ref lifecycle, modded-class semantics, code style.
when_to_use: Writing, modifying, or reviewing a `.c` file.
paths: ["**/*.c"]
---

# DayZ scripting

## Invariants

Five limits of the language and the engine. The compiler accepts every violation below — the failure surfaces later, as a silent no-op or a segfault.

- **Branch with `if` / `else`.** Enforce Script has no ternary operator.
- **One statement, one line.** A signature, call, argument list, or attributed field declaration stays on a single line however long it runs.
- **`ref` lives on class fields** and inside template parameters (`array<ref T>`, `map<int, ref T>`). Locals, parameters, return types, and typedefs are already strong; a `ref` there corrupts the reference count.
- **Release by nulling.** Assign `null` and let ARC collect. Entities go through `g_Game.ObjectDelete(entity)` — `delete` on an entity crashes.
- **`modded class Foo` already descends from `Foo`.** Write the header bare: a `: Bar` is dropped without a warning, and `Foo` still descends from the original.

## Style contract

- **Braces** — Allman on `class` and function headers, K&R inside bodies. Every control-flow body is braced, so the shortest `if` is three lines.
- **Indent** — 4 spaces.
- **Naming** — `PascalCase` for classes, structs, enum types, methods, public fields, and auto-bind widget fields; `m_` / `s_` + `PascalCase` for private-protected and static fields; `camelCase` for parameters and locals; `UPPER_SNAKE_CASE` for enum values and constants.
- **Comments** — `//` lines throughout; `/** */` doxygen blocks on classes and public APIs. English in comments, identifiers, and string literals.
- **`override`** on every method that overrides a parent.
- **Casting** — `Class.CastTo(var, val)` when the result is checked on the spot, `Foo.Cast(bar)` when the check comes later. Both can return null; check before use.
- **Globals** — reach the game through `g_Game`. It is the global itself, where `GetGame()` pays a proto native call to return it.
- **Collections** — `array<T> items = {}` is the primary initializer; `new array<T>` when assigning into a `ref` field.
- **Client and server** — split on `g_Game.IsDedicatedServer()` in init and load code. `IsClient()` and `IsServer()` only start telling the truth after loading finishes.

## Reference

| Read | When |
|------|------|
| `reference/memory-refs.md` | `ref`, `autoptr`, `new`, destructors, or any question of who owns what |
| `reference/modded-classes.md` | any `modded class` — super chains, private access, modded constants, modded vs plain inheritance |
| `reference/engine-pitfalls.md` | a segfault, a compiler error pointing at the wrong file, an unexplained runtime crash, or a value saved in an entity's record (`OnStoreSave` / `OnStoreLoad`) |
| `reference/language-rules.md` | `notnull`, `out` / `inout`, `foreach`, `switch`, overloading, index operators, `auto` |
| `reference/code-style.md` | formatting the contract above leaves open — column alignment, blank lines, doxygen shape |

For widget-driving code — layouts, menus, HUD — call the Skill tool with "dayz-ui".
