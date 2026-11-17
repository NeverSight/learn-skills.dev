---
name: ratatui-tui
description: |
  Build terminal UIs with ratatui following 2026 Rust best practices.
  Use when: (1) Creating new TUI apps, (2) Adding widgets/layouts,
  (3) Keyboard navigation/state management, (4) Image integration via
  ratatui-image, (5) Async event handling, (6) Shimmer/loading animations
  via tui-shimmer, (7) Reviewing TUI code, (8) Release optimization.
  Covers v0.30.1 API, Elm Architecture, StatefulWidget, color-eyre.
---

# Ratatui TUI Development

## Quick Start

1. **Copy template** to project:
   ```bash
   cp -r ~/.agents/skills/ratatui-tui/assets/templates/<template>/* .
   ```

   Or generate from the official templates repo:
   ```bash
   cargo install --locked cargo-generate
   cargo generate ratatui/templates
   ```

2. **Run**:
   ```bash
   cargo run
   ```

## Version Notes (0.30.x)

Targets **0.30.x** (MSRV 1.88, edition 2024); run `cargo info ratatui` for the current patch release.

- **Modular workspace**: apps keep depending on `ratatui`; widget *libraries*
  should depend on `ratatui-core` for API stability and fewer dependencies.
- **`ratatui::run(|terminal| ...)`**: initializes the terminal, installs a
  panic hook that restores it, runs the closure, and restores on exit.
- **`Block::shadow(...)`** (new in 0.30.1): drop shadows for blocks/popups.
- **Breaking since 0.29**: `block::Title` removed, `layout::Alignment` renamed
  to `HorizontalAlignment`, `Flex::SpaceAround` now matches flexbox semantics
  (use `Flex::SpaceEvenly` for the old behavior), `Marker` is non-exhaustive.
- **Performance**: disabling `default-features` also disables `layout-cache`;
  re-enable it explicitly or layout performance drops sharply.

## Template Selection

| Complexity | Template | Use Case |
|------------|----------|----------|
| Minimal | `hello-world` | Learning, quick demos |
| Simple | `simple-app` | Single-screen apps, tools |
| Async | `async-app` | Background tasks, network |
| Full | `component-app` | Multi-view, config, logging |

**Decision tree:**
- Need async/network? → `async-app`
- Multiple screens/components? → `component-app`
- Just a simple tool? → `simple-app`
- Learning ratatui? → `hello-world`

## Project Setup

### Minimal Cargo.toml
```toml
[package]
name = "my-tui"
version = "0.1.0"
edition = "2024"

[dependencies]
ratatui = "0.30"
crossterm = "0.29"
color-eyre = "0.6"
```

### Full Dependencies (component-app)
```toml
[dependencies]
ratatui = "0.30"
crossterm = { version = "0.29", features = ["event-stream"] }
color-eyre = "0.6"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
clap = { version = "4", features = ["derive"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
serde = { version = "1", features = ["derive"] }
config = "0.15"
dirs = "6"

# Optional: image support (default features include chafa-dyn, which overrides chafa-static)
ratatui-image = { version = "11", default-features = false, features = ["crossterm", "image-defaults", "chafa-static"] }

# Optional: shimmer text animation
tui-shimmer = "0.1"
```

### Release Profile
```toml
[profile.release]
lto = true
codegen-units = 1
panic = "abort"
strip = true
```

## Core Loop: TEA (The Elm Architecture)

```
Model → Message → Update → View
  ↑                         |
  └─────────────────────────┘
```

```rust
struct App {
    counter: i32,
    should_quit: bool,
}

enum Message {
    Increment,
    Decrement,
    Quit,
}

impl App {
    fn update(&mut self, msg: Message) {
        match msg {
            Message::Increment => self.counter += 1,
            Message::Decrement => self.counter -= 1,
            Message::Quit => self.should_quit = true,
        }
    }

    fn view(&self, frame: &mut Frame) {
        let text = format!("Counter: {}", self.counter);
        frame.render_widget(Paragraph::new(text), frame.area());
    }
}
```

## Styling Rules

**Use Stylize trait helpers:**
```rust
use ratatui::style::Stylize;

// Good
"text".bold()
"text".dim()
"text".cyan()
"text".on_dark_gray()
"text".bold().cyan()

// Avoid
Style::default().fg(Color::White)  // hardcoded white
Style::default().fg(Color::Black)  // hardcoded black
Style::new().add_modifier(Modifier::BOLD)  // verbose
```

**Color palette:**
- Primary: `.cyan()`, `.green()`
- Error: `.red()`
- Warning: `.yellow()` (sparingly)
- Muted: `.dim()`, `.dark_gray()`
- Accent: `.magenta()`

**Text wrapping:**
```rust
use textwrap::wrap;
use ratatui::text::Line;

let wrapped: Vec<Line> = wrap(&long_text, width as usize)
    .into_iter()
    .map(|cow| Line::from(cow.into_owned()))
    .collect();
```

See: [references/style-guide.md](references/style-guide.md)

## Widget Patterns

### StatefulWidget
```rust
struct MyList {
    items: Vec<String>,
}

struct MyListState {
    selected: usize,
}

impl StatefulWidget for MyList {
    type State = MyListState;

    fn render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State) {
        // render with state.selected
    }
}

// Usage
frame.render_stateful_widget(my_list, area, &mut state);
```

### Layout
```rust
let [header, main, footer] = Layout::vertical([
    Constraint::Length(1),
    Constraint::Fill(1),
    Constraint::Length(1),
]).areas(frame.area());

let [left, right] = Layout::horizontal([
    Constraint::Percentage(30),
    Constraint::Fill(1),
]).areas(main);
```

### Built-in State Types
- `ListState` - for List widget
- `TableState` - for Table widget
- `ScrollbarState` - for Scrollbar

See: [references/architecture-patterns.md](references/architecture-patterns.md)

## Async Event Handling

```rust
use crossterm::event::{EventStream, Event, KeyCode};
use futures::StreamExt;
use tokio::select;

async fn run(mut app: App) -> Result<()> {
    let mut events = EventStream::new();

    loop {
        // Render
        terminal.draw(|f| app.view(f))?;

        // Handle events
        select! {
            Some(Ok(event)) = events.next() => {
                if let Event::Key(key) = event {
                    match key.code {
                        KeyCode::Char('q') => break,
                        KeyCode::Up => app.update(Message::Up),
                        KeyCode::Down => app.update(Message::Down),
                        _ => {}
                    }
                }
            }
            // Add other channels here (background tasks, timers)
        }

        if app.should_quit {
            break;
        }
    }
    Ok(())
}
```

See: [references/async-patterns.md](references/async-patterns.md)

## Image Integration

Targets `ratatui-image` 11.x; its API changes between majors, so check docs.rs
before reusing older snippets.

```rust
use ratatui::layout::Size;
use ratatui_image::{picker::Picker, protocol::Protocol, Image, Resize};

// Query protocol and font size once at startup; keep the picker on the app
let picker = Picker::from_query_stdio()?;

// Encode once, fitted inside a box of cells; do this outside `draw`
// (on a worker thread for large images)
let dyn_img = image::open("photo.png")?;
let protocol: Protocol = picker.new_protocol(dyn_img, Size::new(40, 20), Resize::Fit(None))?;

// In render, drawing a pre-encoded Protocol is cheap
frame.render_widget(Image::new(&protocol), area);
```

**Key points:**
- For portable binaries use `chafa-static` with `default-features = false`;
  the default `chafa-dyn` takes precedence when both are enabled
- Query the protocol once, not per frame
- `Image` is stateless and fixed-size; all encoding happens in `new_protocol`
- `StatefulImage` refits to its render area and encodes at render time, which
  blocks; drive it through `ratatui_image::thread::ThreadProtocol` (see the
  crate's `examples/thread.rs` and `examples/tokio.rs`)

See: [references/image-integration.md](references/image-integration.md)

## Shimmer / Loading Animation

[tui-shimmer](https://github.com/vinhnx/tui-shimmer) sweeps a highlight
across text — the "Loading…"/"Thinking…" effect used by coding-agent TUIs.

```rust
use ratatui::style::Style;
use ratatui::text::Line;
use tui_shimmer::{shimmer_spans_with_style, shimmer_spans_with_style_at_phase};

// Time-driven (call every frame; re-render on a tick to animate)
let spans = shimmer_spans_with_style("Loading...", Style::new().cyan());
frame.render_widget(Line::from(spans), area);

// Deterministic: drive phase (0.0..1.0) from app state — testable, pausable
let phase = (self.start.elapsed().as_secs_f32() / 2.0) % 1.0;
let spans = shimmer_spans_with_style_at_phase("Working...", Style::new().cyan(), phase);
```

**Key points:**
- Animation needs redraws: add a tick event (~80-120ms) to the event loop
  (`select!` with `tokio::time::interval`, or `event::poll` timeout)
- Prefer the `_at_phase` variant with phase stored in the Model — keeps
  rendering pure and animation testable
- True color with automatic fallback for limited terminals
- API is experimental until 1.0 — pin and review minor bumps

## Error Handling

`ratatui::run()` / `ratatui::init()` install a panic hook that restores the
terminal before panicking — do not write one by hand. Install color-eyre
**first** so the terminal is restored before its report prints:

```rust
use color_eyre::eyre::Result;

fn main() -> Result<()> {
    color_eyre::install()?;        // eyre hooks before terminal init
    // App::run is the app's own main loop (see templates), not a ratatui API
    let result = ratatui::run(|terminal| App::default().run(terminal));
    Ok(result?)
}
```

Only write a manual panic hook when constructing `Terminal`/`Backend` by
hand instead of via `ratatui::init()`.

**Error propagation:**
```rust
// Use ? for recoverable errors
let file = std::fs::read_to_string(path)?;

// Use color_eyre context
let config = load_config()
    .wrap_err("Failed to load configuration")?;
```

## Release Build

```bash
cargo build --release
```

Binary at `target/release/<name>`.

**Size optimization** — replaces the Release Profile block above when binary
size matters more than speed:
```toml
[profile.release]
lto = true
codegen-units = 1
panic = "abort"
strip = true
opt-level = "z"  # size over speed
```

## Templates Overview

### hello-world (~25 lines)
Minimal ratatui demo using `ratatui::run()`.

### simple-app (~80 lines)
Synchronous event loop, App struct, basic render.

### async-app (~120 lines)
Tokio runtime, EventStream, `select!` pattern.

### component-app (~300 lines)
Full modular structure:
- `main.rs` - entry point
- `app.rs` - App state, update logic
- `event.rs` - event handling
- `ui.rs` - rendering
- `action.rs` - Action enum
- `tui.rs` - terminal setup
- `config.rs` - configuration with dirs
- `logging.rs` - tracing setup

## Common Patterns

### Centered Popup
```rust
fn centered_rect(percent_x: u16, percent_y: u16, area: Rect) -> Rect {
    let [_, center, _] = Layout::vertical([
        Constraint::Percentage((100 - percent_y) / 2),
        Constraint::Percentage(percent_y),
        Constraint::Percentage((100 - percent_y) / 2),
    ]).areas(area);

    let [_, center, _] = Layout::horizontal([
        Constraint::Percentage((100 - percent_x) / 2),
        Constraint::Percentage(percent_x),
        Constraint::Percentage((100 - percent_x) / 2),
    ]).areas(center);

    center
}
```

With a drop shadow (0.30.1+):
```rust
use ratatui::layout::Offset;
use ratatui::widgets::{Block, Shadow};

let popup = Block::bordered()
    .title("Confirm")
    .shadow(Shadow::dark_shade().offset(Offset::new(2, 1)));
```

### Key Bindings Display
```rust
let help = Line::from(vec![
    " q ".bold().cyan(),
    "quit ".dim(),
    " ↑↓ ".bold().cyan(),
    "navigate ".dim(),
    " Enter ".bold().cyan(),
    "select ".dim(),
]);
```

### Status Bar
```rust
let status = Line::from(vec![
    " MODE ".bold().on_cyan(),
    format!(" {} items ", count).dim().into(),
]);
```

## Multi-Agent TUI Review Workflow

[workflows/tui-review.js](workflows/tui-review.js) is a dynamic-workflow
template for Claude Code's `Workflow` tool. It fans out one reviewer per
TUI dimension — TEA architecture, terminal safety, styling, event handling,
render performance — then adversarially verifies each finding before
reporting, so only confirmed issues survive. In agents without the
`Workflow` tool (Codex), skip the script and apply those five
dimensions as a manual review checklist instead.

Treat it as a **template, not a script to run verbatim**: adjust the target
path, dimensions, and severity threshold to the codebase. It fans out several
agents, so run it when the user asks for a TUI review or a pre-release check:

```
Workflow({
  scriptPath: "~/.agents/skills/ratatui-tui/workflows/tui-review.js",
  args: { path: "src/" },
})
```

Or ask: "run the TUI review workflow from the ratatui-tui skill on src/".

## Checklist

Before shipping:

- [ ] `cargo fmt`
- [ ] `cargo clippy --all-features` clean
- [ ] No `unwrap()` outside tests
- [ ] Terminal restored on all exit paths (`ratatui::run()` or `init`/`restore`)
- [ ] `cargo build --release` succeeds
- [ ] Test on target terminal(s)
