---
name: ottergui
description: "Build, debug, and extend FFXIV Dalamud plugins using OtterGui, including code used by Puni.sh plugins such as AutoRetainer and Artisan. Use to set up OtterGui and its nested OtterGuiInternal submodule, fix a plugin not compiling because of OtterGui or SDK mismatches, adapt code between Limiana, upstream, and Artisan pins, or implement tables, selectors, combo controls, clipping, buttons, and color pickers with ImUtf8, ImRaii, ItemSelector, Table and Column, FileSystemSelector, FilterComboCache, and ImGuiClip. Luna and ImSharp are separate successor APIs."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
---

# OtterGui

This reference covers the Limiana OtterGui fork and its nested OtterGuiInternal dependency, with comparisons to upstream and Artisan. These snapshots have different APIs and SDK requirements. Compare the consumer's gitlink with the [exact reference revisions](references/VERSIONS.txt) before applying an example from another plugin.

## Workflow

1. Inspect `.gitmodules`, project references, SDK, and the actual OtterGui commit. Use [fork differences](references/topic-fork-delta.md) when the source of a copied example differs from the consumer.
2. Read [setup](references/topic-setup.md) for installation or build failures. OtterGuiInternal is a nested submodule; inspect `git submodule status --recursive` and initialize declared submodules with `git submodule update --init --recursive` when needed.
3. Search `references/api-index.txt` and `references/public-types.txt`, then read the declaration under `references/src/`. A missing index entry requires checking source or the consumer's exact pin before concluding that a member is absent.
4. Read the matching widget topic below. Qualify `OtterGui.Raii.ImRaii` when stock Dalamud's `ImRaii` is also imported, and follow the selected implementation's disposal rules.
5. Build with the consumer's SDK. Fix missing nested sources, a mismatched SDK/target framework, or a signature that belongs to another fork before retrying. Do not update the library pin merely to make an unrelated example compile.
6. In an available client, exercise the changed selector/table/control, repeated window draws, and plugin unload. Verify filtering, sorting, and save behavior when changed, then inspect `/xllog`. Report source-only or build-only verification explicitly if no client was available.

## Task routing

| Task | Read |
|---|---|
| Dependency installation and build recovery | [Setup](references/topic-setup.md), [minimal project wiring](references/guide-setup-in-one-screen.md) |
| Fork, upstream, or Artisan compatibility | [Fork differences](references/topic-fork-delta.md) |
| ImUtf8 strings and overloads | [ImUtf8](references/topic-imutf8.md), [string and scope examples](references/guide-what-you-need-on-nearly-every-task.md) |
| RAII scopes | [RAII](references/topic-raii.md) |
| Table and column types | [Tables](references/topic-table.md) |
| FileSystem, tree selector, persistence | [Filesystem](references/topic-filesystem.md) |
| Selectors, combos, buttons, other widgets | [Widgets](references/topic-widgets.md) |
| Clipping and utility methods | [Helpers](references/topic-helpers.md) |
| Services and general classes | [Services and classes](references/topic-services-classes.md) |
| Consumer examples | [Usage examples](references/topic-usage-in-the-wild.md), [consumer architecture](references/guide-how-the-popular-plugins-use-it.md) |
| Find an API family or compare similarly named types | [Namespaces](references/guide-namespaces.md), [API catalog](references/guide-compact-catalogue.md) |
| Debug filter polarity, scope ownership, clipping, or fork-specific behavior | [Pitfalls](references/guide-pitfalls.md) |
| Port an existing OtterGui integration to Luna when requested | [OtterGui to Luna](references/guide-ottergui-to-luna.md) |

[The technical guide](references/guide.md) records snapshot provenance and indexes the references above. Source-derived examples have not been compiled or tested in game as part of the original snapshot. [NOTICE.md](references/NOTICE.md) covers Apache-2.0 OtterGui and BSL-1.0 OtterGuiInternal; preserve those notices when copying source.
