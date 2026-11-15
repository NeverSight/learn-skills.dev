---
name: gpui
description: >-
  Build, debug, and review Rust applications using GPUI. Use for GPUI actions and
  keybindings, async work, contexts and entities, events and focus, custom elements,
  layout and styling, lists, overlays, text and assets, components, window chrome,
  testing, or development tooling for inspecting a running GPUI app. Verify APIs
  against the project's pinned GPUI revision.
---

## Project setup

Depend on gpui via the Zed git repo. `gpui_platform` ships with **no default features**, so the
platform features must be enabled explicitly. `font-kit` enables the macOS text system — without
it the app runs but renders no text. `wayland` and `x11` enable the Linux backends (no-ops on
macOS, keep them for portability):

```toml
[dependencies]
gpui_platform = { git = "https://github.com/zed-industries/zed.git", features = ["font-kit", "wayland", "x11"] }
```

## Navigation

Load the relevant reference file based on the task:

| Topic | File | When to load |
|-------|------|--------------|
| Actions & keybindings | [action.md](references/action.md) | `actions!`, `bind_keys`, `on_action`, `key_context` |
| Async, background tasks & tokio | [async.md](references/async.md) | `cx.spawn`, `background_spawn`, `Task`, debounce, tokio interop |
| Context management | [context.md](references/context.md) | `App`, `Window`, `Context<T>`, `AsyncApp` |
| Custom elements (low-level) | [element.md](references/element.md) | `Element` trait, `request_layout`, `prepaint`, `paint` |
| Entity state | [entity.md](references/entity.md) | `Entity<T>`, `WeakEntity`, state management |
| Events & subscriptions | [event.md](references/event.md) | `cx.emit`, `cx.subscribe`, `cx.observe`, `EventEmitter` |
| Focus & keyboard nav | [focus-handle.md](references/focus-handle.md) | `FocusHandle`, `track_focus`, `tab_index`, focus-on-render |
| Global state | [global.md](references/global.md) | `Global` trait, `cx.set_global`, app-wide config |
| Layout & styling | [layout-style.md](references/layout-style.md) | `div()`, flexbox, `min_w_0`, truncation, hover/groups, overflow |
| Scrolling & lists | [list-scroll.md](references/list-scroll.md) | `ScrollHandle`, `uniform_list`, stick-to-bottom, virtualization |
| Overlays | [overlay.md](references/overlay.md) | `deferred`, `anchored`, modals, menus, tooltips, stacking |
| Text, fonts, SVG & assets | [text-styling.md](references/text-styling.md) | `StyledText`, highlights, `add_fonts`, `svg()`, `AssetSource` |
| Components | [component.md](references/component.md) | `RenderOnce` vs `Render`, handler props, borrow idioms |
| Window chrome | [window.md](references/window.md) | `TitlebarOptions`, `WindowControlArea`, appearance/dark mode |
| ElementId | [element-id.md](references/element-id.md) | `ElementId`, `.id()`, uniqueness rules, stateful elements |
| Testing | [test.md](references/test.md) | `#[gpui::test]`, `TestAppContext`, `VisualTestContext` |
| Running-app inspection | [dev-mcp.md](references/dev-mcp.md) | Optional development MCP, input automation, screenshots, frame synchronization, native verification |

## Ground truth

When the project pins gpui via the Zed git repo, the vendored checkout under
`~/.cargo/git/checkouts/zed-*/<rev>/crates/gpui/src/` is ground truth — verify any nontrivial API
signature there (grep) before answering; several of this skill's own past errors came from guessing.

When maintaining an API recipe, record the checked revision near it and
compile-check representative consumers against a stated pin. Distinguish source
inspection, compilation, headless tests, and native interaction checks; one does
not establish the results of the others.

### Focused verification coverage

On Zed revision `4c7244790a075e862eeb4e5ccc12d6c8f5da6f7e` (macOS), representative
action, context, async task, entity callback/model-view, event subscription,
focus, `RenderOnce`, scrolling, and `uniform_list` snippets were compile-checked
with minimal app-specific scaffolding. The startup helper and asset registration
were checked against source. Headless GPUI tests exercised:

- `set_global` and `update_global` notifying a dependent view through its observer.
- Model notifications reaching a view, and reads of a separate entity during an update.
- Modal Tab/Shift-Tab wrapping with background tab stops, including an empty modal.

These checks cover selected recipes. Verify other examples and changed APIs
against the consumer project's pin; native platform interaction remains a
separate check.

The source repository's `validation/gpui/check.py` harness extracts
the marked entity, event, async, timer, deferred-update, and custom text-element
examples directly from Markdown. Those checks are maintained separately from
the earlier temporary audit fixtures described above.

## Extended References

For deep-dive topics, additional reference files are available:

**Element trait:**
- [element-api.md](references/element-api.md) — complete API, hitbox system, event handling
- [element-patterns.md](references/element-patterns.md) — text, interactive, container, composite patterns
- [element-examples.md](references/element-examples.md) — complete text element and draw test; selection and child-management design notes
- [element-best-practices.md](references/element-best-practices.md) — performance, state, common pitfalls
- [element-advanced.md](references/element-advanced.md) — masonry/circular layouts, async updates, virtual lists

**Entity management:**
- [entity-api.md](references/entity-api.md) — complete Entity API, methods, lifecycle
- [entity-patterns.md](references/entity-patterns.md) — model-view, cross-entity communication, observer
- [entity-best-practices.md](references/entity-best-practices.md) — memory, performance, lifecycle, re-entrancy

**Testing:**
- [test-examples.md](references/test-examples.md) — testing examples and patterns
- [test-reference.md](references/test-reference.md) — complete testing API reference
