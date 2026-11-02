---
name: atlas-craft
description: "Refine production interfaces: color, typography, layout, accessibility, UI polish and copy while preserving project identity. On request, build a workbench for a component’s existing states."
disable-model-invocation: false
---

# Atlas Craft

Choose from the requested outcome and context, honoring an explicit choice. Ask only when ambiguity changes the method. Read [Scope and ownership](references/ownership.md) and the selected methods; combine domains when they serve complementary parts of the task.

| Mode | Need | Read and follow |
| --- | --- | --- |
| Color | Palette, tokens, rendered contrast or color usage | [Color](references/color/index.md) |
| Type | Font choice, sizing, wrapping and typographic detail | [Type](references/type/index.md) |
| Layout | Spacing, alignment, grouping, adaptivity or spatial RTL | [Layout](references/layout/index.md) |
| Accessibility | Semantics, keyboard paths, focus, forms or assistive technology | [Accessibility](references/accessibility/index.md) |
| UI Polish | Surfaces, radius, elevation, icons and optical alignment | [UI Polish](references/ui/index.md) |
| Copy | Labels, errors, empty states, confirmations and localized strings | [Copy](references/copy/index.md) |
| States | On request, expose one real component's existing states in a temporary workbench with fixtures and a switcher | [States](references/states/state-machine.md) |

States requires a request for that workbench or `state-machine`; ordinary refinement does not create it. Setup leaves product code and live data unchanged and hands over the workbench before visual edits. Requested refinement then uses the relevant domains, preserving the component's identity. Remove the workbench only when the user asks.

Preserve accepted identity and project foundations; a new design direction needs its own decision. Load related domains only when the selected method needs their rules. A request to review is read-only; apply fixes when the user asks for refinement or implementation.

When polish includes animation or gestures, follow [Motion ownership](references/motion-ownership.md). Motion references are bundled for those decisions. Whole-interface audits and change reviews belong to Atlas Review; substantial prose belongs to Writing for Humans.

When the task involves mobile browser behavior—keyboard overlap, browser chrome, tap feedback or scroll gestures—read [Mobile Web](references/mobile-web/mobile-native.md).

Report browser and assistive-technology checks that could not run as verification gaps. Bundled instructions do not supply missing runtime tools.
