---
name: ratkit
description: Comprehensive guide for the ratkit Rust TUI component library built on ratatui 0.29, including feature flags, APIs, and implementation patterns. Use when building, debugging, or extending ratkit applications and examples.
compatibility: Requires Rust 1.70+, Cargo, just, and a terminal environment for interactive TUI demos.
metadata:
  version: "0.2.12"
---

# ratkit

> Comprehensive Rust TUI component library built on ratatui 0.29, providing 21 feature-gated modules (primitives, widgets, services) for building rich terminal applications.

This file provides a complete reference for working with the ratkit codebase. The repository is organized as a single crate at the root level with feature-based modularity. Use this guide to understand component relationships, find APIs, and follow established patterns when implementing new features.

## Agent Operating Rules

1. **Single crate at root**: All code is in `src/` with 21 feature flags (e.g., `button`, `pane`, `markdown-preview`)
2. **Enable features explicitly**: No default features; add required features to Cargo.toml (e.g., `features = ["button", "dialog"]`)
3. **Cross-feature dependencies**: Some features auto-enable others (e.g., `tree-view` enables `widget-event`, `repo-watcher` enables `file-watcher` and `git-watcher`)
4. **Use `just` for all operations**: Build (`just build`), test (`just test`), check (`just check`), demos (`just demo`)
5. **Run examples with `--features` flag**: Examples require their specific features (e.g., `--features markdown-preview`)
6. **Use module-path imports first**: Prefer explicit module paths (e.g., `use ratkit::primitives::button::Button`, `use ratkit::widgets::markdown_preview::MarkdownWidget`) because crate-root re-exports are not guaranteed for every type
7. **StatefulWidget pattern**: Complex widgets require separate state structs persisted in app state
8. **Event loop polling**: Services require regular `check_for_changes()` calls in the event loop
9. **Mouse capture required**: Enable crossterm mouse capture for interactive widgets
10. **Persist widget state**: Never create widget state in render loops - store in app struct
11. **Validate before commits**: Run `just check` (format + lint + test) before committing
12. **Verify feature flags**: Compilation errors often indicate missing feature flags in Cargo.toml

## Environment and Version Constraints

- Rust 1.70+ required (workspace.rust-version in Cargo.toml)
- ratatui 0.29 as the underlying rendering library
- crossterm 0.28 for terminal input/events
- tokio for async runtime
- Single crate at root with 21 feature flags (no workspace members)
- 23 examples in `examples/` (moved from `crates/ratkit/examples/`)
- Optional external deps: notify (file watching), reqwest (ai-chat), pulldown-cmark/syntect (markdown), similar (code-diff)

## Quick Task Playbooks

### Run an example
- **Where to edit**: N/A
- **Related files**: `examples/`
- **Validation**: `cargo run --example button_button_demo --features button`

### Extract smooth-redraw patterns from markdown preview demo
- **Where to edit**: target app event loop (`on_event`) and draw path (`on_draw`)
- **Related files**: `examples/markdown_preview_markdown_preview_demo.rs`
- **Goal**: Port the demo's event-pressure controls and redraw strategy into other TUIs
- **Validation**: Under rapid mouse movement and wheel input, app remains responsive without event backlog

### Run with just
- **Where to edit**: N/A
- **Related files**: `justfile`
- **Validation**: `just demo` (interactive picker) or `just demo-md`, `just demo-md-small`, `just demo-term`, etc.

### Build with specific features
- **Where to edit**: `Cargo.toml` (root level)
- **Related files**: Feature definitions
- **Validation**: `cargo build --features "button,pane,dialog"`

### Build all features
- **Where to edit**: N/A
- **Related files**: All source files
- **Validation**: `cargo build --all-features`

### Run full verification
- **Where to edit**: N/A
- **Related files**: All source files
- **Validation**: `just check` (runs fmt-check, lint, test)

## Getting Started

```toml
# Cargo.toml - enable specific features
[dependencies]
ratkit = { version = "0.2.12", features = ["button", "dialog", "pane"] }
```

```rust
use ratkit::prelude::*;
use ratatui::Frame;

struct MyApp;

impl CoordinatorApp for MyApp {
    fn on_event(&mut self, event: CoordinatorEvent) -> LayoutResult<CoordinatorAction> {
        match event {
            CoordinatorEvent::Keyboard(keyboard) => {
                if keyboard.is_escape() {
                    return Ok(CoordinatorAction::Quit);
                }
            }
            _ => {}
        }
        Ok(CoordinatorAction::Continue)
    }

    fn on_draw(&mut self, frame: &mut Frame) {
        // Render your UI here
    }
}

fn main() -> std::io::Result<()> {
    let app = MyApp;
    run(app, RunnerConfig::default())
}
```

## Workspace Overview

The ratkit workspace contains a **single crate** with 21 feature-gated modules organized into:

- **Primitives** (11 modules): Core UI building blocks in `src/primitives/`
  - button, pane, dialog, toast, statusline, scroll, menu_bar, resizable_grid, tree_view, widget_event, termtui
- **Widgets** (6 modules): Higher-level composite widgets in `src/widgets/`
  - markdown_preview, code_diff, ai_chat, hotkey_footer, file_system_tree, theme_picker
- **Services** (4 modules): Background monitoring services in `src/services/`
  - file_watcher, git_watcher, repo_watcher, hotkey_service
- **Core Runtime** (1 module): Application lifecycle in `src/core/`

All modules follow feature-gated compilation. Enable only what you need.

## Core Runtime

The core runtime provides the application lifecycle, event routing, and element management for terminal UI applications.

### Key Components

- **CoordinatorApp trait**: Applications implement this to receive events and render
- **run() / run_with_diagnostics()**: Entry points to start the event loop
- **Element trait**: Implement for custom widgets that integrate with the coordinator
- **RunnerConfig**: Configuration for tick rate, layout debounce, mouse capture

### Architecture

- Three-region layout: Top, Center, Bottom
- Focus management with stack and traversal
- Mouse routing with z-order hit testing
- Element registry with weak references

## UI Primitives

Core UI building blocks for TUI applications, located in `src/primitives/`.

### Feature Flags

Each primitive has an individual feature flag:
- `button`, `pane`, `dialog`, `toast`, `statusline`, `scroll`
- `menu-bar` (enables `widget-event`)
- `resizable-grid`
- `tree-view` (enables `widget-event`)
- `widget-event`
- `termtui`

### Common Patterns

- Builder pattern with `new()` and `with_*` methods
- StatefulWidget pattern for complex state
- Event emission via `WidgetEvent`
- Mouse/keyboard interaction support

### MenuBar Layout Contract (updated)

- `MenuBar::render_with_offset(frame, area, left_offset)` now uses the full available container width for the border: `area.width - left_offset`
- The menu bar border should stretch to the right edge of the provided container, while menu items remain left-aligned within the bar
- If available width is zero after offset, rendering exits early and clears `self.area`
- This behavior was validated with `examples/menu-bar_menu_bar_demo.rs` at fixed 120-column terminal width

## Complex Widgets

Higher-level composite widgets in `src/widgets/`.

### Feature Flags

- `markdown-preview` - Most complex (syntax highlighting, TOC, themes, selection)
- `code-diff` - VS Code-style diff viewer
- `ai-chat` - AI chat interface (requires reqwest, serde)
- `hotkey-footer` - Keyboard shortcut footer
- `file-system-tree` - File browser with devicons
- `theme-picker` - Theme selector with 25+ themes

### External Dependencies

| Widget | Dependencies |
|--------|-------------|
| ai-chat | reqwest, serde, serde_json |
| markdown-preview | pulldown-cmark, syntect, syntect-tui, notify, arboard, dirs |
| code-diff | similar |
| file-system-tree | devicons |

### FileSystemTree visual parity notes (Yazi-style)

When adjusting `file-system-tree` visuals, keep these conventions to match Yazi-like behavior:

- Prefer `devicons::icon_for_file(...).color` (hex) for file icon colors instead of hardcoded extension maps.
- Parse devicons hex colors into `ratatui::style::Color::Rgb` before rendering.
- Selected row background should use item color (directory rows use dir color; file rows use file color) with black foreground text.
- Keep row content alignment stable between selected and non-selected states (avoid 1-column shifts when drawing decorations).
- Directory selection should use a filled highlight; file selection may use rounded edge glyphs if desired.

## Services

Background monitoring services in `src/services/`.

### Feature Flags

- `file-watcher` - Watch files/directories for changes
- `git-watcher` - Monitor git repository state
- `repo-watcher` - Combined file + git watching (enables file-watcher and git-watcher)
- `hotkey-service` - Global hotkey registration and management

### Common Dependencies

All watcher services use the `notify` crate for filesystem events.

## Usage Cards

### CoordinatorApp
- **Use when**: Building any ratkit TUI application
- **Enable/Install**: Core runtime, no feature flag needed
- **Import/Invoke**: `use ratkit::prelude::*;`
- **Minimal flow**:
  1. Define struct implementing `CoordinatorApp`
  2. Implement `on_event()` to handle events
  3. Implement `on_draw()` to render UI
  4. Call `run(app, RunnerConfig::default())`
- **Key APIs**: `on_event()`, `on_draw()`, `on_layout_changed()`
- **Pitfalls**: Runner takes ownership; wrap shared state in `Arc<RwLock<>>`
- **Source**: `src/coordinator.rs`, `src/runner_helper.rs`

### run()
- **Use when**: Starting the main application event loop
- **Enable/Install**: Core runtime, no feature flag
- **Import/Invoke**: `use ratkit::{run, run_with_diagnostics};`
- **Minimal flow**:
  1. Create app implementing `CoordinatorApp`
  2. Create `RunnerConfig::default()` or custom
  3. Call `run(app, config)` or `run_with_diagnostics(app, config)` for debug overlay
- **Key APIs**: `run()`, `run_with_diagnostics()`, `RunnerConfig`
- **Pitfalls**: Blocks until exit; handles terminal init/cleanup
- **Source**: `src/runner_helper.rs`

### Element
- **Use when**: Creating custom widgets that integrate with coordinator
- **Enable/Install**: Core runtime
- **Import/Invoke**: `use ratkit::Element;`
- **Minimal flow**:
  1. Implement `Element` trait for your widget
  2. Define `id()`, `on_render()`, `on_keyboard()`, `on_mouse()`
  3. Register with `ElementMetadata` and region
- **Key APIs**: `id()`, `on_render()`, `on_keyboard()`, `on_mouse()`, `on_focus_gain()`, `on_focus_loss()`, `on_tick()`
- **Pitfalls**: Registry stores weak refs - keep strong refs in app state; return `true` when handling events
- **Source**: `src/registry.rs`

### Button
- **Use when**: Clickable button with hover states
- **Enable/Install**: `features = ["button"]`
- **Import/Invoke**: `use ratkit::Button;`
- **Minimal flow**:
  1. Create `Button::new("Label")`
  2. Call `update_hover(x, y)` on mouse move
  3. Call `is_clicked(x, y)` on click
  4. Render with `render_with_title()`
- **Key APIs**: `new()`, `normal_style()`, `hover_style()`, `update_hover()`, `is_clicked()`
- **Pitfalls**: State must persist in app struct
- **Source**: `src/primitives/button/widget.rs`

### Pane
- **Use when**: Styled panel container with title/icon/padding
- **Enable/Install**: `features = ["pane"]`
- **Import/Invoke**: `use ratkit::Pane;`
- **Minimal flow**:
  1. Create `Pane::new("Title")`
  2. Chain builder methods: `with_icon()`, `with_padding()`, `border_style()`
  3. Render as widget
- **Key APIs**: `new()`, `with_icon()`, `with_padding()`, `with_uniform_padding()`, `border_style()`
- **Pitfalls**: Padding reduces inner content area
- **Source**: `src/primitives/pane/mod.rs`

### Dialog
- **Use when**: Modal dialogs for confirmation/information
- **Enable/Install**: `features = ["dialog"]`
- **Import/Invoke**: `use ratkit::primitives::dialog::{Dialog, DialogWidget, DialogAction, DialogActionsLayout, DialogWrap, DialogShadow, DialogModalMode};`
- **Minimal flow**:
  1. Create `Dialog::new(title, message)` or `Dialog::confirm(...)`
  2. Configure layout and visuals with `.actions_layout(...)`, `.message_alignment(...)`, `.content_padding(...)`, `.wrap_mode(...)`, `.shadow(...)`, `.overlay(...)`
  3. Configure actions/keys with `.buttons(...)`, `.default_selection(...)`, `.next_keys(...)`, `.previous_keys(...)`, `.confirm_keys(...)`, `.cancel_keys(...)`
  4. In event loop, route keys to `dialog.handle_key_event(...)` and react to `DialogAction`
  5. Render with `DialogWidget::new(&mut dialog)`
- **Key APIs**: `actions_layout()`, `actions_alignment()`, `message_alignment()`, `content_padding()`, `wrap_mode()`, `hide_footer()`, `footer()`, `footer_style()`, `shadow()`, `overlay()`, `modal_mode()`, `body_renderer()`, `handle_key_event()`, `handle_mouse_confirm()`, `blocks_background_events()`
- **Pitfalls**: If you want `Tab` to control inner body UI (for example a list) instead of dialog actions, remove `Tab` from dialog keymap and handle it in your app event loop; if you want no action row, set `.buttons(vec![])`
- **Source**: `src/primitives/dialog/`

### Dialog interaction patterns
- **Vertical actions**: `.actions_layout(DialogActionsLayout::Vertical)` for stacked action menus
- **Horizontal actions**: `.actions_layout(DialogActionsLayout::Horizontal)` for classic Yes/No rows
- **No actions shown**: `.buttons(vec![])` hides the actions row so dialog body content can be primary
- **Custom body widget**: implement `DialogBodyRenderer` and pass `.body_renderer(Box::new(...))` to render a selectable list/menu inside dialog chrome
- **Blocking modal**: `.modal_mode(DialogModalMode::Blocking)` plus `blocks_background_events()` to prevent background input handling
- **Tab delegation**: use `.next_keys(...)` / `.previous_keys(...)` to exclude `Tab` and route `Tab` to body-level focus/selection logic

### Toast
- **Use when**: Auto-dismissing notifications
- **Enable/Install**: `features = ["toast"]`
- **Import/Invoke**: `use ratkit::{ToastManager, ToastLevel};`
- **Minimal flow**:
  1. Create `ToastManager::new()` in app state
  2. Add toasts via `.success()`, `.error()`, `.info()`, `.warning()`
  3. Call `cleanup()` before render
  4. Render with `render_toasts()`
- **Key APIs**: `ToastManager::new()`, `.add()`, `.success()`, `.error()`, `.cleanup()`
- **Pitfalls**: Must call `cleanup()` to remove expired; doesn't auto-expire
- **Source**: `src/primitives/toast/`

### MenuBar
- **Use when**: Top-level horizontal navigation with mouse and keyboard selection
- **Enable/Install**: `features = ["menu-bar"]` (auto-enables `widget-event`)
- **Import/Invoke**: `use ratkit::primitives::menu_bar::{MenuBar, MenuItem};`
- **Minimal flow**:
  1. Create `MenuBar::new(vec![MenuItem::new("File", 0), ...])`
  2. Optionally set initial selection with `.with_selected(index)`
  3. On mouse move: call `update_hover(x, y)`; on click: call `handle_click(x, y)` or `handle_mouse(x, y)`
  4. Render with `render()` or `render_with_offset()`
- **Key APIs**: `new()`, `with_selected()`, `update_hover()`, `handle_click()`, `handle_mouse()`, `selected()`, `render_with_offset()`
- **Pitfalls**: Border fills full container width; do not assume border auto-sizes to label content
- **Source**: `src/primitives/menu_bar/menu_bar.rs`, `examples/menu-bar_menu_bar_demo.rs`

### TreeView
- **Use when**: Hierarchical data with expand/collapse/selection
- **Enable/Install**: `features = ["tree-view"]` (auto-enables widget-event)
- **Import/Invoke**: `use ratkit::{TreeNode, TreeView, TreeViewState, TreeNavigator};`
- **Minimal flow**:
  1. Build `TreeNode` hierarchy
  2. Create `TreeView::new(nodes)` with render_fn
  3. Create `TreeViewState::new()` for selection/expansion
  4. Use `TreeNavigator` for keyboard handling
- **Key APIs**: `TreeNode::new()`, `TreeView::new()`, `TreeViewState::new()`, `TreeNavigator::new()`
- **Pitfalls**: TreeViewState must persist; TreeNavigator handles all keyboard nav
- **Source**: `src/primitives/tree_view/`

### MarkdownWidget
- **Use when**: Rendering markdown with syntax highlighting, TOC, themes
- **Enable/Install**: `features = ["markdown-preview"]` (complex dependencies)
- **Import/Invoke**: `use ratkit::widgets::markdown_preview::{MarkdownWidget, ScrollState, SourceState, ...};`
- **Minimal flow**:
  1. Create state structs (ScrollState, SourceState, etc.) in app state
  2. Create `MarkdownWidget::new(content, scroll, source, ...)`
  3. Handle keyboard with `handle_key()`
  4. Render with ratatui
- **Key APIs**: `new()`, `handle_key()`, `handle_mouse()`, `.show_toc()`, `.toggle_toc()`, `.with_frontmatter_collapsed()`, `set_frontmatter_collapsed()`, `.show_scrollbar()`
- **Pitfalls**: Requires mouse capture enabled; state must persist across renders; frontmatter collapse is section-based (section id `0`); large markdown with many fenced code blocks can increase first-render time if syntax highlighter initialization is repeated (parser now reuses one `SyntaxHighlighter` per parse call)
- **Source**: `src/widgets/markdown_preview/widgets/markdown_widget/`

### Markdown demo variants
- **Use when**: Choosing markdown content size for preview behavior checks
- **Run**: `just demo-md` (opencode SDK skill markdown) and `just demo-md-small` (ratkit skill markdown)
- **Expected behavior**: Both variants render with TOC, statusline, hover interactions, and copy support
- **Startup profiling**: Run `target/debug/examples/markdown_preview_markdown_preview_demo --startup-probe` (with `RATKIT_MD_DEMO_FILE=...`) to print `MARKDOWN_DEMO_READY_MS=<ms>` for repeatable load-time comparisons
- **Source**: `examples/markdown_preview_markdown_preview_demo.rs`, `justfiles/utilities/demo-md.just`

### FileSystemTree
- **Use when**: Browsing local files/directories with icons and keyboard navigation
- **Enable/Install**: `features = ["file-system-tree"]`
- **Import/Invoke**: `use ratkit::widgets::file_system_tree::{FileSystemTree, FileSystemTreeState, FileSystemTreeConfig};`
- **Minimal flow**:
  1. Create `FileSystemTree::new(root_path)` or `with_config(...)`
  2. Persist `FileSystemTreeState` in app state
  3. Route nav keys to `handle_navigation_key(...)`
  4. Route filter keys to `handle_filter_key(...)` when filter mode is active
- **Key APIs**: `new()`, `with_config()`, `handle_navigation_key()`, `enter_filter_mode()`, `expand_selected()`, `collapse_selected()`
- **Pitfalls**: Keep icon colors sourced from devicons, and preserve selection-row alignment when adding rounded highlight glyphs
- **Source**: `src/widgets/file_system_tree/widget.rs`, `src/widgets/file_system_tree/config.rs`, `src/widgets/file_system_tree/state.rs`

### FileWatcher
- **Use when**: Detecting file/directory changes
- **Enable/Install**: `features = ["file-watcher"]` (uses notify crate)
- **Import/Invoke**: `use ratkit::services::file_watcher::FileWatcher;`
- **Minimal flow**:
  1. Create `FileWatcher::for_file()` or `FileWatcher::for_directory()`
  2. Call `watch(path)`
  3. Poll `check_for_changes()` in event loop
  4. Get changes with `get_changed_paths()`
- **Key APIs**: `for_file()`, `for_directory()`, `watch()`, `check_for_changes()`, `get_changed_paths()`
- **Pitfalls**: Must poll regularly; `get_changed_paths()` clears queue; debounced (100ms/200ms)
- **Source**: `src/services/file_watcher/`

### HotkeyService
- **Use when**: Centralized hotkey management with scope filtering
- **Enable/Install**: `features = ["hotkey-service"]`
- **Import/Invoke**: `use ratkit::services::hotkey_service::{Hotkey, HotkeyRegistry, HotkeyScope};`
- **Minimal flow**:
  1. Create `HotkeyRegistry::new()`
  2. Register hotkeys with `Hotkey::new(key, description).scope(scope)`
  3. Set active scope with `set_active_scope()`
  4. Query with `lookup(key, scope)` in event loop
- **Key APIs**: `HotkeyRegistry::new()`, `register()`, `lookup()`, `set_active_scope()`
- **Pitfalls**: Uses `&'static str` for scopes; must handle crossterm events separately
- **Source**: `src/services/hotkey_service/`

## API Reference

### Core Runtime

| Component | Key APIs |
|-----------|----------|
| CoordinatorApp | `on_event()`, `on_draw()`, `on_layout_changed()` |
| run | `run()`, `run_with_diagnostics()` |
| Element | `id()`, `on_render()`, `on_keyboard()`, `on_mouse()`, `on_focus_gain()`, `on_focus_loss()`, `on_tick()` |
| RunnerConfig | `tick_rate`, `layout_debounce`, `mouse_router_config` |

### Primitives

| Primitive | Key APIs |
|-----------|----------|
| Button | `new()`, `normal_style()`, `hover_style()`, `update_hover()`, `is_clicked()` |
| Pane | `new()`, `with_icon()`, `with_padding()`, `with_uniform_padding()`, `border_style()` |
| Dialog | `new()`, `info()`, `warning()`, `error()`, `success()`, `confirm()`, `buttons()` |
| Toast | `ToastManager::new()`, `.add()`, `.success()`, `.error()`, `.cleanup()` |
| TreeView | `TreeNode::new()`, `TreeView::new()`, `TreeViewState::new()`, `TreeNavigator::new()` |
| Scroll | `calculate_scroll_offset()` |

### Services

| Service | Key APIs |
|---------|----------|
| FileWatcher | `for_file()`, `for_directory()`, `watch()`, `check_for_changes()`, `get_changed_paths()` |
| GitWatcher | `new()`, `with_config()`, `watch()`, `check_for_changes()` |
| RepoWatcher | `new()`, `with_config()`, `watch()`, `check_for_changes()`, `get_change_set()` |
| HotkeyRegistry | `new()`, `register()`, `lookup()`, `set_active_scope()` |

## Common Pitfalls

### Feature Flags

1. **No default features**: Must explicitly enable every feature you use
2. **Cross-feature deps**: `tree-view` enables `widget-event`; `repo-watcher` enables `file-watcher` and `git-watcher`
3. **Missing feature errors**: "unresolved import" usually means missing feature flag

### State Management

1. **StatefulWidget pattern**: Complex widgets require persistent state in app struct
2. **Never create state in render**: Always store widget state in app struct
3. **Weak references**: Element registry stores weak refs - keep strong refs in app

### Event Handling

1. **Return values**: Return `true` when consuming events, `false` to propagate
2. **Mouse capture**: Must enable crossterm mouse capture for interactions
3. **Poll services**: Must call `check_for_changes()` regularly on watchers

### Examples

1. **Feature flags required**: Examples need their specific features: `--features markdown-preview`
2. **Just commands**: Use `just demo` for interactive picker or `just demo-*` for specific demos
3. **Port behavior, not just API calls**: Reuse input coalescing and selective redraw patterns from demos, not only widget construction code

## Smooth Redraw Patterns (Extracted from Markdown Preview Demo)

Use this section to transfer the demo's responsiveness patterns into other ratkit apps.

### Core anti-throttling techniques

1. **Coalesce high-rate mouse move events**
   - Pattern: On `MouseEventKind::Moved`, skip handling if last processed move was too recent.
   - Demo value: ~24ms guard (`last_move_processed.elapsed() < Duration::from_millis(24)`).
   - Effect: Prevents motion events from overwhelming the queue during fast pointer movement.

2. **Gate redraws to meaningful state changes**
   - Pattern: Return `CoordinatorAction::Continue` by default for move events; return `Redraw` only when UI state actually changes.
   - Demo behavior: Move events redraw only on `MarkdownEvent::TocHoverChanged { .. }`.
   - Effect: Avoids redraw storms and keeps frame pacing stable.

3. **Use differential handling for move vs non-move mouse events**
   - Pattern: Treat clicks/wheel/drag as higher-value events and redraw immediately; aggressively filter move-only noise.
   - Effect: Maintains interaction fidelity while reducing unnecessary render pressure.

4. **Bound periodic work with moderate tick rate**
   - Pattern: Configure non-aggressive ticks and use tick handler for lightweight maintenance only.
   - Demo value: `RunnerConfig { tick_rate: Duration::from_millis(250), .. }`.
   - Effect: Reduces idle churn and avoids periodic tasks competing with interactive redraws.

5. **Persist heavy widget state outside draw loop**
   - Pattern: Store all stateful structs in app state and mutate incrementally in event handlers.
   - Demo structures: `ScrollState`, `SourceState`, `CacheState`, `CollapseState`, `ExpandableState`, `GitStatsState`, `VimState`, `SelectionState`, `DoubleClickState`.
   - Effect: Prevents reallocation/reparse overhead on each frame and stabilizes render latency.

6. **Keep `on_draw` render-only**
   - Pattern: Avoid heavy parsing, file reads, or expensive recomputation in `on_draw`; do those on state transitions.
   - Effect: More predictable frame time and smoother UI under bursty input.

### Event-loop blueprint to reuse in other apps

- **Keyboard**: early-return `Continue` for non-keydown; map only actionable keys to state changes, then redraw.
- **Mouse moved**: coalesce by time window; update hover state; redraw only on meaningful diff.
- **Mouse non-moved**: apply action (click/wheel/selection), then redraw.
- **Tick**: run lightweight expirations/cleanup; redraw only when cleanup changed visible state.
- **Resize**: redraw.

### Porting checklist (copy into new feature work)

- Add `last_move_processed: Instant` to app state and time-gate move handling.
- Ensure event handlers return `Continue` unless visible state changed.
- Separate ephemeral notifications/cleanup into tick-driven maintenance.
- Keep widget state persistent and mutate in place.
- Verify smoothness under rapid mouse movement and continuous wheel scrolling.

## Optional

### Additional Resources

- **Examples**: 23 examples in `examples/`
- **Just commands**: Run `just help` for all available commands
- **Build**: `just build` or `cargo build -p ratkit --all-features`
- **Test**: `just test`

### Version

- Current: 0.2.12
- Rust: 1.70+
