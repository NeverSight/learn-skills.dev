---
name: gpui-editor
description: >-
  Building text editor components from scratch in GPUI: multi-line text areas, 
  plain-text editors, code editors, rich text. Use when the user is building or 
  debugging a text input, textarea, text editor, or code editor in GPUI; 
  mentions EntityInputHandler, ElementInputHandler, ShapedLine, shape_line, TextRun, 
  marked text/IME, cursor blinking, selections, line numbers, syntax highlighting, 
  or soft wrap in gpui; or asks how Zed's or gpui-component's editor works internally. 
  Organized by feature: core editing loop (input handler, IME, custom Element, 
  cursor/selection painting, hit-testing, blink), multi-line layout and soft wrap 
  (LineWrapper, goal columns, anchor-based scrolling), large-text performance (rope, 
  virtualization, display map), syntax highlighting, decoration (gutter, folding, 
  widgets, comments), selections/multi-cursor/collaboration, search and replace, 
  undo/redo, overlays, and LSP.
---

# Building text editors in GPUI

For writing your own editor component from scratch — any level: multi-line text area, plain-text editor, code editor, rich text. Organized by **feature**. Zed (`zed-industries/zed`) and gpui-component (`longbridge/gpui-component`) are used throughout as reference implementations — proof of working designs, cited inline where each pattern comes from — not as dependencies.

## Navigation

| Feature | File | When to load |
|---------|------|--------------|
| Core editing loop (plain text) | [core-editing.md](references/core-editing.md) | Any editor work. State model, actions/keybindings, `EntityInputHandler`/IME, the custom `Element`, mouse, blink, focus, read-only, events |
| Multi-line, wrap, movement, scroll | [multiline-and-wrap.md](references/multiline-and-wrap.md) | `\n`, soft wrap / `LineWrapper`, buffer-vs-display coordinates, goal columns, word movement, scrolling, autoscroll |
| Performance with large text | [large-text.md](references/large-text.md) | Rope storage, visible-range-only shaping, anchors, the layered display-map contract, incremental budgets |
| Syntax highlighting & styled text | [highlighting.md](references/highlighting.md) | `TextRun` runs, `StyledText`, the swappable highlighter seam, tree-sitter, themes/capture names, style-layer merging |
| Text decoration & widgets | [decoration.md](references/decoration.md) | Decoration collections, gutter & line numbers, indent guides/invisibles, folding, inline widgets, block rows, **comments/annotations** |
| Selections, multi-cursor, collaboration | [selections-and-multicursor.md](references/selections-and-multicursor.md) | Selection model, word/line select modes, `move_with` combinators, rendering N selections, CRDT/collab scope decision |
| Search & replace | [search.md](references/search.md) | Matcher design, session state, match rendering, scrollbar markers, the find/replace panel, replace-all |
| Undo / redo | [undo.md](references/undo.md) | Transactions, ~300 ms grouping, selections in undo, IME grouping, `set_value` vs `replace_all` |
| Overlays | [overlays.md](references/overlays.md) | Anchoring UI to text positions, completion menu, hover/diagnostic popovers, context menu, key routing while open |
| LSP integration | [lsp.md](references/lsp.md) | Position conversions, push-model diagnostics, provider traits, async discipline, semantic tokens, applying server edits |
| Rich text | [rich-text.md](references/rich-text.md) | Document model, styled-range editing semantics, mixed sizes/baselines, mentions/inline images, serialization |

### Read only the section you need

`core-editing.md` is ~430 lines; load the section for the task rather than the whole file:

| Task | `core-editing.md` section |
|------|---------------------------|
| Typing does nothing / IME, marked text, UTF-16 offsets | §3 `EntityInputHandler` |
| Keybindings, Backspace/arrows/copy/paste as actions | §2 Actions + key bindings, §6 Render |
| Painting text, cursor, selection; layout stash | §4 The custom Element |
| Click/drag/double-click hit-testing | §5 Mouse handling |
| Cursor blink, focus, read-only, events | §7, §Read-only, disabled, and events |
| State/anchor shape when starting fresh | §1 The state entity, §Minimal editor checklist |

Likewise, `selections-and-multicursor.md` §Collaboration is the only part relevant to CRDT/automerge integration; `large-text.md` and `multiline-and-wrap.md §Autoscroll` cover scrolling/perf. Reference files do not change between turns — read each once per session.

## Build order by editor level

- **Multi-line text area:** core-editing → multiline-and-wrap §1–§5. Plain `String`, logical lines, no gutter.
- **Plain-text editor:** + large-text (rope, virtualization), scrolling/autoscroll, undo, search.
- **Code editor:** + highlighting, decoration (gutter/line numbers first), then overlays + lsp as needed; folding last.
- **Rich text:** plain-text editor + rich-text.md (span-table document model); highlighting/decoration provide the rendering machinery.

Skip until a feature demands them: multi-cursor (but adopt the selection *shape* from day one — it's free), folding, virtual text, block rows, minimap, collaboration (a day-one architecture decision if you ever need it — see selections-and-multicursor.md §Collaboration).

## Cross-cutting facts (memorize these)

- **Two input channels, one focus handle.** Named commands (Backspace, arrows, copy/paste) are GPUI *actions* dispatched through `key_context` + key bindings. Plain printable characters and IME composition arrive through the platform text-input system via an `EntityInputHandler` registered with `window.handle_input(&focus_handle, ElementInputHandler::new(bounds, entity), cx)` — **inside `paint`, every frame**. An editor with no input-handler registration silently accepts no typing.
- **UTF-16 at the IME boundary, bytes inside.** Every `EntityInputHandler` method speaks UTF-16 code units; LSP positions are UTF-16 too. Convert at the boundaries; keep everything internal in UTF-8 byte offsets.
- **One mutation funnel.** All editing — typing, backspace, cut, paste, IME commit, replace-all, server edits — flows through `replace_text_in_range`. Deletion is "select the range, replace with `""`". This is also the single instrumentation point for undo.
- **Layout state round-trips through the entity.** The element writes last frame's shaped lines + bounds back onto the entity at the end of `paint`; mouse hit-testing, IME geometry, and overlay anchoring read them next frame. Include the element's font/font_size/line_height in that stash: handler-context `window.text_style()` is the root style, not your element's.
- **You can't schedule a frame from inside prepaint/paint.** `cx.notify()` and `window.refresh()` are silently dropped while `draw_phase != None`, so state mutated mid-draw (e.g. a `ScrollHandle` offset) renders only on the next *incidental* redraw — up to a blink-tick later. Anything that must be visible next frame (autoscroll especially — multiline-and-wrap.md §Autoscroll) belongs in handler context, which runs before the frame draws.
- **Shape only visible lines; never re-shape to scroll.** Horizontal scroll is an origin translation; vertical scroll changes which rows get shaped. Per-frame cost must be O(viewport), never O(document).
- **Anything that outlives one edit is an anchor, not an offset** — selections, scroll top, decorations, folds, diagnostics, comments.
- **Vertical movement needs a pixel goal column**, not a character column (tabs, ligatures, proportional fonts break column math).
- **Buffer coordinates ≠ display coordinates.** The moment soft wrap (or folding) exists, keep them as distinct Rust types.
- **Styles resolve by name at paint time** ("keyword" → theme color), so theme switches never re-parse; style sources merge in a fixed priority: syntax < semantic tokens < decorations < selection/IME.
- GPUI is pre-1.0: pin a revision, and verify signatures against the vendored checkout under `~/.cargo/git/checkouts/` rather than guessing.

## Where to read real code

- **Runnable from-scratch examples (start here):** Zed repo `crates/gpui/examples/input.rs` (single-line; note the defects listed in core-editing.md) and `crates/gpui/examples/view_example/example_editor.rs` (multi-line + blink + tests).
- **Zed's editor** (the maximal design): `crates/rope/`, `crates/text/` (buffer/anchors/undo), `crates/editor/src/display_map.rs` (module doc = the architecture essay), `crates/editor/src/element.rs` (EditorElement), `selections_collection.rs`, `movement.rs`, `input.rs` (IME), `scroll/`.
- **gpui-component's editor** (the mid-size design point — ~50K-line ceiling, one team): engine at `crates/base/src/input/base/state.rs`, paint/virtualization in `crates/base/src/input/base/element.rs`, highlighter seam in `crates/base/src/input/editor/highlighting.rs` + `crates/ui/src/highlighter/`, search/undo/decorations/lsp under `crates/base/src/input/editor/`.
