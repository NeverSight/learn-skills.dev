---
name: dayz-ui
description: DayZ UI rules — `.layout` / `.styles` / `.imageset` formats, widget scripting, menus, HUD, and the engine invariants that make UI fail silently.
when_to_use: Writing, modifying, or reviewing UI — a layout, style, or imageset file, or `.c` code that drives widgets. Also on any request to build a menu, a HUD, a window, or a screen, or to wire a script to a widget.
paths: ["**/*.layout", "**/*.styles", "**/*.imageset"]
---

# DayZ UI

## Invariants

- **Every acquisition is paired.** A menu takes things from the game and gives them back in the matching lifecycle hook. Pair at one level — `OnShow`/`OnHide` or constructor/destructor — and keep both halves there. An unreleased acquisition survives the menu.

  | Acquire | Release | Left unreleased |
  |---------|---------|-----------------|
  | `GetMission().AddActiveInputExcludes({"menu"})` | `RemoveActiveInputExcludes({"menu"})` | input dead until the game restarts |
  | `GetUIManager().ShowCursor(true)` | `ShowCursor(false)` | cursor stuck over the world |
  | `GetMission().Pause()` | `Continue()` | world frozen |
  | `CallLater(fn, ms, true)` | `Remove(fn)` | callback fires into a destroyed object |

- **`Unlink()` frees a widget.** Nulling `m_Root` breaks only the script's link; the tree stays in the workspace, rendering and costing frames on every open. Call `m_Root.Unlink()`, then null. The root a `UIScriptedMenu` returns from `Init()` is the engine's to free — everything created by hand is yours.
- **Cast what `FindAnyWidget` returns, and check it.** It hands back a base `Widget` or null, so type-specific methods need `TextWidget.Cast(...)` or `Class.CastTo(...)` and a null check. `Frame`, `Content`, `Panel`, `SmartPanel`, `Embeded`, `ThreeStateCheckbox`, and `Window` have no script class at all — use them as the base `Widget`.
- **Widget callbacks live on `CALL_CATEGORY_GUI`.** It runs whenever the client UI does. `SYSTEM` is for non-UI work that also runs server-side; `GAMEPLAY` stalls while a menu is open.
- **Auto-bind matches names exactly.** In a `scriptclass`, a field named `TitleLabel` binds the widget named `TitleLabel`; `m_TitleLabel` binds nothing and stays null. Take the bare name, or bind by hand with `FindAnyWidget` + `Cast`.
- **`scriptclass` names a class that exists.** A typo compiles, renders, and never runs — no log line either way.
- **Anchors take the `_ref` form** — `center_ref`, `right_ref`, `bottom_ref`. Bare `center` collapses the widget onto the parent's top-left corner. Left and top are the defaults, written by omitting the attribute.
- **`.styles` and `.imageset` load once registered** in `config.cpp` under `CfgMods` → `class defs` → `class widgetStyles` / `class imageSets`. Unregistered, widgets render Default and images come back blank. Layouts load by path through `CreateWidgets` and need no entry.

## File locations

| Type | Path |
|------|------|
| Layout | `gui/layouts/` |
| Styles | `gui/looknfeel/` |
| Imageset | `gui/imagesets/` |
| Fonts | `gui/fonts/` |
| Textures (`.edds`) | `gui/textures/` |

## Reference

| Read | When |
|------|------|
| `reference/widget-scripting.md` | any UI code — creating widgets, events and their return semantics, `UIScriptedMenu`, HUD, `ScriptParams` |
| `reference/layout-fundamentals.md` | writing a `.layout` — syntax, the widget class hierarchy, property groups, positioning and exact-flags |
| `reference/widget-catalog.md` | a specific widget's own properties and script methods |
| `reference/style-system.md` | `.styles` — item slots, states, Color encoding, or a widget rendering Default |
| `reference/imageset-format.md` | `.imageset` — atlas regions, tiling flags, `set:… image:…` references |
| `reference/edds-format.md` | `.edds` — Workbench import, GUIDs, `imageTexture` |
| `reference/ui-pitfalls.md` | an input freeze, a dead widget, a leak, or UI behaving in a way nothing above explains |

For the Enforce Script rules the `.c` side of the UI still has to satisfy, call the Skill tool with "dayz-scripting".
