---
name: clientstructs
description: "Locate native FFXIV structs and offsets, resolve signatures, and write or debug unsafe FFXIVClientStructs code for Dalamud plugins and Splatoon scripts. Use when working with explicit-layout structs, vtables, source-generator attributes, native signatures, singleton pointers, AtkUnitBase callbacks, AtkValue, data.yml, or adding fields and functions. Covers a pinned memory-layout snapshot; use Dalamud services guidance for plugin lifecycle."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
---

# FFXIVClientStructs

## Compatibility

Use the ClientStructs revision shipped by the target runtime. The bundled source is an offline reference; its exact pin and game executable version are in [snapshot provenance](references/provenance.md). A newer upstream commit alone does not require refreshing this skill.

## Workflow

1. Read the plugin's SDK and ClientStructs references. The running version is available through `IDalamudPluginInterface.GetDalamudVersion().GitHashClientStructs`.
2. Locate the requested native type in [the struct index](references/all-structs.txt). Use `references/structs/` when its revision matches the target. Otherwise read that type, its base types, and relevant generator/runtime code from a checkout at the target's exact commit; see [revision selection](references/guide-conventions-and-version-hygiene.md#select-the-target-revision). An absent index entry does not prove the type is absent upstream. If the target source is unavailable, state what remains unverified and leave native layouts and signatures unchanged.
3. Read the relevant section of [the technical guide](references/guide.md): generator attributes, signature resolution, entry points, addon callbacks, or contributing layouts. Use the [snapshot provenance](references/provenance.md) when comparing revisions.
4. Check pointers and game state before access. Keep game-owned access on the framework thread and reacquire addon pointers after reload or zoning. For addon events, prefer Dalamud's lifecycle services when they expose the event you need.
5. Build against the user's pinned SDK. For a new signature or layout, run the matching ClientStructs resolver/exporter checks described in the guide. If an address remains unresolved, stop calling it and verify the executable version and signature; do not replace it with a guessed address.
6. Report the source revision, build result, and any behavior that could not be tested in game.

## Read game-owned state

After confirming the running revision, call this from a framework-thread callback in the plugin. It copies the value while the pointer is valid and reports unavailable state without retaining a game-owned pointer:

```csharp
using FFXIVClientStructs.FFXIV.Client.Game.UI;

private static unsafe bool TryReadCurrentLevel(out short level)
{
    level = 0;
    var state = PlayerState.Instance();
    if (state == null || !state->IsLoaded)
        return false;

    level = state->CurrentLevel;
    return true;
}
```

The project must allow unsafe code and reference the ClientStructs assembly matching its Dalamud runtime. Compile with `dotnet build` in the plugin project; if a member differs, inspect that revision's `PlayerState` definition before changing the access. A successful build does not validate memory layouts against a different executable.

## Validate a layout change

This applies when the user is contributing to FFXIVClientStructs and already works in their own full checkout of it. Upstream's change-validation workflow builds and runs the repository's `CExporter` project in Release configuration, which writes `ida/errors.txt`. Building it executes that checkout's code, so run it only in the user's own checkout and at their request; do not fetch a copy of the repository to run it.

Inspect `ida/errors.txt` for overlapping fields, size mismatches, name collisions, and missing `data.yml` entries. Correct the reported layout or declaration and rerun the check. The bundled source is a curated reference and cannot run the exporter. Signature resolution also depends on the matching game executable; an exporter pass does not establish that a signature resolves.

## Interop rules

- Dalamud resolves its bundled ClientStructs assembly at startup. A normal plugin must not run the resolver or ship a second copy.
- Explicit-layout structs require the correct size and field offsets. Source-generator features require the documented attributes and a partial unsafe declaration; see [struct definition](references/guide-struct-definition-and-what-the-generator-emits.md#struct-definition-and-what-the-generator-emits).
- Generated pointer accessors may return null during login or zoning. Check each pointer in a chain before dereferencing it.
- Keep `AtkValue` types, allocation ownership, and callback argument order consistent with the target addon. Read [addon work](references/guide-addon-ui-work.md#addon-ui-work) before constructing callbacks.
- Do not cache game-owned pointers across lifetime changes or free memory that the game owns.

## Task routing

| Task | Read |
|---|---|
| Attributes, inheritance, vtables, generated members | [Struct definition](references/guide-struct-definition-and-what-the-generator-emits.md#struct-definition-and-what-the-generator-emits) and `references/generator/` |
| Signature failure or standalone resolver | [Runtime resolution](references/guide-signature-resolution-at-runtime.md#signature-resolution-at-runtime) and `references/runtime/` |
| Player, inventory, actions, UI, objects | [Entry points](references/guide-entry-points-real-members.md#entry-points-real-members), then the specific source file |
| Addons, nodes, AtkValue, callbacks | [Addon work and Callback ownership](references/guide-addon-ui-work.md#addon-ui-work) |
| Add a field/function or inspect data.yml | [Contributing](references/guide-contributing-a-field-or-function.md#contributing-a-field-or-function), [version hygiene](references/guide-conventions-and-version-hygiene.md#conventions-and-version-hygiene), and `references/upstream-docs/` |

The source copies support revision-specific answers; they do not establish compatibility with a newer game patch. See [notices](references/NOTICE.md) for bundled licenses.
