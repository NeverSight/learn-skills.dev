---
name: minecraft-native-ui
description: Build native Minecraft screens, widgets, and menus.
license: MIT
metadata:
  version: "0.1.0"
  author: Hermes
  hermes-tags: "Minecraft, Modding, UI, Screens"
---

# Minecraft Native UI

Build Minecraft-native interfaces for blocks, items, tools, editors, diagnostics, overlays, and inventory menus using vanilla screens, widgets, rendering, input, and networking. This does not prescribe a third-party UI framework; exact project mappings, loader APIs, and the target Minecraft branch remain the source of truth.

## When to Use

- “Add a native UI to this block, item, or tool.”
- “Build an editor, canvas, picker, settings screen, or diagnostic view.”
- “Add a container menu with synchronized slots.”
- “Create reusable Minecraft widgets, tabs, lists, or overlays.”
- “Port a screen from 1.20 or 1.21 to 26.1.”
- “Review focus, resize, input, narration, or client/server safety.”

## Prerequisites

- Read Minecraft, loader, mappings, and Java versions from project Gradle files with `read_file`.
- Locate existing screens, widgets, menu types, open helpers, key mappings, payloads, and client registration with `search_files`.
- Inspect the exact-version source branch and matching official loader documentation.
- For multi-loader projects, identify common, client, and loader-specific source sets before editing.
- No credentials or environment variables are required.

## How to Run

Use `search_files` and `read_file` to trace how the UI opens, owns state, handles input, renders, and saves. Apply changes with `patch`, then invoke the project’s existing Gradle build, client, game-test, and dedicated-server tasks through the `terminal` tool.

Read [version scope and menu/network boundaries](references/version-and-boundaries.md) when choosing loader factories, migrating opening data, or designing client tests.

## Quick Reference

- General client view: `Screen`
- Inventory backend: `AbstractContainerMenu`
- Inventory view: `AbstractContainerScreen<M>`
- Native controls: `Button`, `EditBox`, `AbstractWidget`
- Widget setup: `init`, `addRenderableWidget`, `removeWidget`
- Navigation: `Minecraft#setScreen`, previous-screen reference
- Focus: `setInitialFocus`, `setFocused`, `isFocused`
- Input: `keyPressed`, `charTyped`, mouse handlers
- Accessibility: `updateWidgetNarration`, `NarrationElementOutput`
- Menu factory: `MenuType<M>`
- Menu opening: `ServerPlayer#openMenu`, `MenuProvider`
- Initial menu context: `FriendlyByteBuf`, `RegistryFriendlyByteBuf`
- NeoForge factory: `IMenuTypeExtension.create`
- Fabric factory: `ExtendedScreenHandlerType` (API name; mapped menu classes differ)
- Mojmap 1.20.1/1.21.1 rendering: `GuiGraphics` (later 1.21 releases need separate inspection)
- 26.1 migration leads: `GuiGraphicsExtractor`, `extractRenderState`, `RenderPipelines`; resolve exact target signatures before use.

## Procedure

1. **Pin the exact UI API.**
   - Inspect Gradle files and live Git refs before choosing imports or overrides.
   - Treat 1.20.x, 1.21.x, and 26.1 as distinct rendering/input APIs. Do not transplant signatures by class name alone.

2. **Classify the interface before designing it.**
   - Use plain `Screen` for item/tool configuration, editors, canvases, examples, logs, settings, diagnostics, and other client views without vanilla slot semantics.
   - Use `AbstractContainerMenu` plus `AbstractContainerScreen` when slots, carried stacks, shift-clicking, or server-authoritative inventory interaction matter.
   - Use an overlay or HUD hook for information that belongs over gameplay rather than in modal navigation.
   - Compose native widgets and rendering primitives before introducing a framework.

3. **Trace state ownership and the open path.**
   - Find the interaction or keybind, client/server boundary, constructor inputs, previous-screen behavior, save/cancel callbacks, and all payload handlers.
   - Separate authoritative game state, editable draft state, and rendered derived state.
   - A screen may optimistically mirror state for responsiveness, but the server validates and applies gameplay changes.
   - Never open a client screen by loading client classes from common or dedicated-server code.

4. **Model standalone screen context explicitly.**
   - Pass the item hand, item identity, block position, previous screen, initial value, read-only state, or save callback through a focused context object rather than unrelated globals.
   - Super Factory Manager uses text-edit open contexts so disk, example, title-screen, and configuration editors can share UI while keeping different load/save/close behavior.
   - Define whether a child screen replaces the current screen or returns/pushes back to it. Preserve the intended parent on close.

5. **Build lifecycle-safe widgets.**
   - Create and recreate widgets in `init()`; calculate positions from current `width`, `height`, or container origins.
   - Preserve user drafts, search text, selection, camera position, or other intentional state across `resize`/reinitialization.
   - For filtered or dynamic controls, remove stale widgets before adding replacements. If rebuilding during a click would corrupt focus, defer the rebuild until the next render/tick, as SFM’s label-gun screen does.
   - Keep widget collections as screen state when they need bulk visibility, activation, or removal changes.

6. **Treat focus and input as architecture.**
   - Set an initial focus for text fields, terminals, canvases, and custom controls; restore focus after buttons that should not retain it.
   - Call `super` first or last deliberately. A native container owns slot input; a custom editor may intentionally bypass default tab navigation and route key impulses itself.
   - Forward mouse/key events to the focused child before fallback when building composite controls.
   - Enable key repeat only where text editing needs it, and restore global/raw callbacks in both `onClose` and `removed`.
   - Handle Enter, Escape, clipboard shortcuts, dragging, scrolling, and character input separately where the version API does.

7. **Design reusable native controls.**
   - Extend `AbstractWidget` for controls with custom state, rendering, input, or narration; use builders only to standardize construction.
   - Implement narration with `updateWidgetNarration` and meaningful translated labels/tooltips.
   - Keep geometry, enabled/visible state, focus state, and action callbacks explicit.
   - For lists, tabs, palettes, and canvases, separate the model (selection, cursor, zoom, content) from rendering and event routing.

8. **Handle text editors and canvases as real applications.**
   - Keep mutable text/cursor/selection state in a model rather than reconstructing it from rendered strings.
   - Define save, discard, read-only, and close-confirmation behavior through the open context.
   - Bound pasted/networked content and preserve clipboard failures as user-visible errors rather than crashes.
   - For zoomable canvases, store world-space camera/model coordinates separately from screen-space hit testing; clamp zoom and make resize behavior deterministic.
   - SFM demonstrates multi-cursor text editing, grammar-backed views, draggable canvas content, configuration sub-screens, and diagnostics using plain native `Screen` subclasses.

9. **Implement inventory-backed screens only when needed.**
   - Register `MenuType<M>` on both physical sides and its screen only in client setup.
   - Construct identical slot order on client and server; record half-open ranges for machine inventory, player inventory, and hotbar.
   - Implement `stillValid` and `quickMoveStack`, including the no-move case and source-slot updates.
   - Use loader extended factories only for bounded initial host context. Initial opening data is not continuous synchronization.

10. **Separate synchronization channels.**
    - Let menu slots synchronize item stacks and use `DataSlot`/`ContainerData` only for suitable small integer state.
    - Use bounded payloads for tool settings, edits, labels, filters, actions, strings, and complex state.
    - Every serverbound handler validates the active item/menu, hand or host, permissions, distance, indices, lengths, and allowed transition.
    - Do not trust a client-side item snapshot or block position merely because the screen received it at open time.

11. **Adapt rendering by version.**
    - On 1.20.1/1.21.1, follow the exact branch’s `GuiGraphics`, `render`, and background methods. Do not generalize those signatures across all 1.21.x releases.
    - On 26.1, inspect current signatures. SFM and Sophisticated Core use `GuiGraphicsExtractor`, `extractRenderState`, and `RenderPipelines`; extraction submits render state instead of issuing older immediate calls.
    - Keep rendering side-effect free: mutation, packet sends, saves, and expensive parsing should not happen merely because a frame is extracted.
    - Verify mapping renames such as `ResourceLocation` versus `Identifier` in the target branch.

12. **Choose an extraction level from proven projects.**
    - Super Factory Manager: direct native screens for label selection, text editors, drawing canvas, logs, examples, settings, diagnostics, and container management; shared open contexts, builders, widgets, and screen-change helpers tie them together.
    - CC:Tweaked: focused widgets and input forwarding for terminal-like screens; loader services isolate menu factories.
    - Sophisticated Storage/Core: shared screen bases, tabs, upgrades, settings, reusable controls, and explicit custom synchronization.
    - Applied Energistics 2: typed menu builders and host locators for many block, part, item, and submenu hosts.
    - Extract repeated lifecycle and state contracts, not merely repeated drawing calls.

13. **Verify the complete interaction.**
    - Open from every supported origin: block, item, keybind, parent screen, or server menu.
    - Test resize/reinit, focus traversal, keyboard-only use, narration, clipboard, cancel/save, reopen, reconnect, and resource reload.
    - For menus, also test shift-click both ways, two viewers, removed hosts, invalid payloads, and dedicated-server startup.
    - Inspect logs for client-class loading, menu mismatch, rejected payload, texture, narration, and desynchronization errors.

## Pitfalls

- “Native UI” is broader than container menus; forcing every screen through `AbstractContainerScreen` adds incorrect inventory lifecycle.
- `Screen` is physical-client code and must not leak into common registration or payload handlers.
- Rebuilding widgets during their own callback can reset focus or leave stale listeners.
- `resize` commonly calls `init()` and can destroy unsaved text unless state is preserved first.
- Rendering methods may run often or through extraction; they are not save/network hooks.
- Raw GLFW callbacks must chain the previous callback and be restored on every removal path.
- Matching slot coordinates do not prove matching slot order.
- Sophisticated Storage is All Rights Reserved. Study architecture and independently implement it; do not copy substantial code.
- Repository default branches may not match the requested Minecraft line. Enumerate live refs first.

## Verification

Invoke the repository’s full build through the `terminal` tool, then open each changed UI from its real origin and prove resize, focus, input, save/cancel, and reopen behavior; for synchronized actions, confirm the dedicated server accepts valid requests, rejects invalid ones, and logs no client-class or protocol errors.

## Source Leads

The branch list below is retained as discovery guidance, not immutable evidence for every current API. The linked version-boundary reference separates menu, network, and rendering contracts. Re-resolve branches before implementing 26.1 code.

- Super Factory Manager: `https://github.com/TeamDman/SuperFactoryManager` (`1.20.1`, `1.21.1`, `26.1.2` branches), including label gun, text editors, canvas, logs, examples, diagnostics, widgets, and manager menus.
- CC:Tweaked: `https://github.com/cc-tweaked/CC-Tweaked` (`mc-1.20.x`, `mc-1.21.x`, `mc-26.1` branches).
- Sophisticated Storage/Core: `https://github.com/P3pp3rF1y/SophisticatedStorage`, `https://github.com/P3pp3rF1y/SophisticatedCore` (`1.20.x`, `1.21.x`, `26.1` branches).
- Applied Energistics 2: `https://github.com/AppliedEnergistics/Applied-Energistics-2` (`1.20.1`, `1.21.1` branches).
- Forge 1.20 menus: `https://docs.minecraftforge.net/en/1.20.x/gui/menus/`.
- Fabric screen handlers: `https://wiki.fabricmc.net/tutorial:screenhandler`.
