---
name: golang-tui
description: >-
  Expert TUI development in Go with Charm libraries (Bubble Tea, Lip Gloss, Bubbles) and
  ecosystem packages. Always use when building terminal user interfaces, TUI components,
  styling terminal output, theming, or working with the Elm Architecture in Go.
license: MIT
metadata:
  author: https://github.com/lrstanley
  domain: frontend
  triggers: TUI, terminal UI, Bubble Tea, bubbletea, Lip Gloss, lipgloss, Bubbles, charm, terminal app, Elm Architecture, bubbletint, steep, teatest, go-snaps, go-snap, golden files, x/exp/golden, snapshot testing, tea.Model, tea.Cmd, tea.View, terminal styling, terminal components, Go TUI, TERM, COLORTERM, bracketed paste, PasteMsg, Kitty keyboard, OSC 9, terminal progress
  role: expert
  scope: implementation
  output-format: code
  related-skills: golang
---

# Go TUI Development

Expert Go TUI developer specializing in the Charm ecosystem (Bubble Tea, Lip Gloss,
Bubbles) and supporting libraries (bubbletint, chroma, go-nf). Builds production-grade
terminal applications following the Elm Architecture with proper theming, composition,
and terminal compatibility.

For TUI UX and layout guidance, [tui-design (hyperskills)](https://skills.sh/hyperb1iss/hyperskills/tui-design) is a recommended companion skill.

## Core Workflow

1. **Analyze** -- Understand the codebase, component tree, state flow, dimensions (width, height, weights, padding, margins, borders, etc), and theme setup
2. **Structure** -- Break UI into components (pages, dialogs, etc); keep main.go small
3. **Implement** -- Elm Architecture (Init/Update/View) with idiomatic Charm library usage, accounting for standard styling, theming, and layout conventions
4. **Test & Lint** -- Run tests and linters to ensure the codebase is healthy
5. **Review** -- Ensure changes do not go against this skill's constraints, gotchas, or core patterns

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
| --- | --- | --- |
| Bubble Tea v2 | `references/libraries/bubbletea-v2.md` | Always load when implementing or debugging `tea.Program`, `tea.Model`, `Init` / `Update` / `View`, `tea.Cmd` / `tea.Msg`, built-in messages and commands, async I/O, or key/mouse handling |
| Bubble Tea Examples | `references/libraries/bubbletea-v2-examples.md` | Use when mapping a feature to an official Bubble Tea example, upstream example pattern, or sample app |
| Lip Gloss v2 | `references/libraries/lipgloss-v2.md` | Always load when changing layout math inside styled regions, or when using colors, borders, padding, joins, placement, tables, lists, trees, or the compositor |
| Bubbles v2 | `references/libraries/bubbles-v2.md` | Always load when integrating or troubleshooting Bubbles components such as spinner, textinput, textarea, list, table, tree, viewport, progress, help, paginator, or filepicker |
| Testing | `references/libraries/steep.md` | Always load when writing or fixing Bubble Tea integration tests, component tests, snapshot tests, golden files, `steep`, `teatest`, `go-snaps`, or `go-snap` workflows |
| Chroma | `references/libraries/chroma-v2.md` | Use when adding syntax highlighting, terminal formatters, chroma styles, or `chromatint` integration |
| Bubbletint | `references/libraries/bubbletint-v2.md` | Load before building theme registries, tint switching, dynamic theme updates, or theme-aware Chroma output via `chromatint` |
| Nerd Fonts | `references/libraries/go-nf.md` | Always load when rendering Nerd Font icons or glyphs in user-visible UI so fallback and detection behavior stay correct |
| Notifications | `references/libraries/beeep.md` | Always load when integrating desktop notifications, alerts, or beeps from Bubble Tea, especially with focus-aware delivery |
| Project Structure | `references/project-structure.md` | Use when scaffolding a new app or reorganizing `main.go`, `cmd/`, `internal/`, pages/components, or Taskfile-based workflows |
| Elm Architecture | `references/elm-architecture.md` | Always load when deciding whether work belongs in `Update`, a `tea.Cmd`, or a child model, especially for blocking vs non-blocking behavior |
| Model & Update | `references/model-update.md` | Always load when designing or refactoring models, `Init`, `Update`, `WindowSizeMsg`, command batching, state machines, or sub-component propagation |
| View & Styling | `references/view-styling.md` | Always load when implementing or debugging `View`, per-region width budgets, full-bleed vs inset layout, truncation, border/frame accounting, or adaptive colors |
| Child Model Composition | `references/child-model-composition.md` | Load before adopting a `Component` / `Page` interface, focus routing, dialog overlays, drill-down stacks, or bubbles-backed child models |
| External processes | `references/exec-external.md` | Load before suspending the TUI for `tea.ExecProcess`, pagers, editors, `*exec.Cmd`, or `x/editor` helpers |
| Keymaps | `references/keymaps.md` | Always load when adding or refactoring centralized key bindings, key groups, `key.Matches`, or help integration |
| Terminal Standards | `references/terminal-standards.md` | Always load when handling color-profile or background messages, alt screen, bracketed paste, Kitty keyboard enhancements, OSC behavior, or reduced-color testing; raster protocols are summarized with a link to `references/images.md` |
| Terminal images | `references/images.md` | Load before choosing or implementing Sixel, Kitty, iTerm2 OSC 1337, mosaic unicode, `x/ansi` encoders, or image snapshot strategies |
| Performance | `references/performance.md` | Always load when optimizing `View` hot paths, ANSI-aware width or truncation, allocations, visible-window rendering, `strings.Builder` usage, or FPS tuning |
| Clipboard | `references/clipboard.md` | Load before implementing clipboard copy/read flows, OSC 52 fallback, native clipboard support, or a dual-write strategy |
| Configuration | `references/configuration.md` | Load before choosing config/cache paths, file permissions, validation, migration, or `os.UserConfigDir` / XDG conventions |
| Troubleshooting | `references/troubleshooting.md` | Use when debugging blank screens, freezes, color issues, focus/logging problems, VHS recording, or pprof-based investigation |

## Core Pattern Example

Minimal Bubble Tea v2 fullscreen application:

```go
package main

import (
    "fmt"
    "os"

    tea "charm.land/bubbletea/v2"
)

type model struct {
    width, height int
    count         int
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.width, m.height = msg.Width, msg.Height
    case tea.KeyPressMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case "up", "k":
            m.count++
        case "down", "j":
            m.count--
        }
    }
    return m, nil
}

func (m model) View() tea.View {
    v := tea.NewView(fmt.Sprintf("Count: %d\n\n  up/down: change -- q: quit\n", m.count))
    v.AltScreen = true
    v.WindowTitle = "My App"
    return v
}

func main() {
    if _, err := tea.NewProgram(model{}).Run(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

## Constraints

### MUST DO

- Handle `tea.WindowSizeMsg` in every application (sent on startup and resize)
- Handle `tea.ColorProfileMsg` and `tea.BackgroundColorMsg` for theme/color detection
- Use `strings.Builder` in View to avoid allocations
- Use `ansi.StringWidth` or `lipgloss.Width` instead of `len()` for calculating string width
- Use `key.Matches` with centralized (or per-component) key bindings instead of raw string
  comparison
- Wrap all I/O (HTTP, file, clipboard, blocking calls, etc) in `tea.Cmd` functions
- Components (pages, views, dialogs, buttons, status bars, etc) should always be
  ELM-architecture compliant, not extraneous `Render(...) string` functions
- Keep main.go minimal (flag parsing, dependency creation, tea.NewProgram, error handling)
- Account for borders in layout calculations (subtract 2 from height for top+bottom border
  or use `<style>.GetVerticalBorderSize()` / `GetVerticalFrameSize()`)
- Derive width **per layout region**: do not reuse one `m.width - N` for full-bleed chrome
  and inset form content unless the same outer padding applies; use `GetHorizontalFrameSize()`
  when truncating text inside a bordered/padded block (see `references/view-styling.md`)
- Degrade gracefully when the terminal is smaller than the content: wrap or truncate
  intentionally, hide lower-priority UI first, and render a centered "window too small"
  style warning if the app cannot be used meaningfully at the current size (prefer to only
  do this when the window is really small)
- Always show most frequently used keybinds/help text for the user to know what to do. If
  there are extensive keybinds, opt for a separate help menu or dialog.

### MUST NOT DO

- Block in `Update()` (no I/O, no `time.Sleep`, no blocking channel reads)
- Use `fmt.Println` (stdout is owned by the TUI renderer; use `tea.Println` or `log/slog`)
- Create styles inside `View()` (define at package level or in Update)
- Use `len()` on strings that will be rendered/displayed
- Hardcode terminal dimensions (always read from `tea.WindowSizeMsg` in Update), and prefer using
  `GetHorizontalFrameSize()` / `GetVerticalFrameSize()` (or similar) functions on the style you render
  with, rather than hardcoding 2, 4, etc for borders and padding. references:
  - `references/view-styling.md`
  - `references/libraries/lipgloss-v2.md`
- Let important content overflow, clip, or disappear without an intentional fallback
  for constrained terminal sizes

## Knowledge Reference

Bubble Tea v2, Lip Gloss v2, Bubbles v2, Elm Architecture, tea.Model, tea.Cmd,
tea.Msg, tea.View, tea.Program, tea.NewView, tea.KeyPressMsg, tea.WindowSizeMsg,
tea.ColorProfileMsg, tea.BackgroundColorMsg, bubbletint, tint registry, chroma,
chromatint, go-nf, Nerd Fonts, beeep, x/ansi, x/editor, steep, reel, x/term/steep,
x/exp/teatest, x/exp/golden, go-snaps, go-snap, lipgloss.JoinHorizontal, lipgloss.JoinVertical,
lipgloss.Place, lipgloss.Darken, lipgloss.Lighten, lipgloss.LightDark,
weight-based layout, compositor, spinner, textinput, textarea, list, table,
tree, viewport, paginator, progress, help, filepicker, key.Binding, key.Matches,
OSC 52, clipboard, colorprofile, alt screen, bracketed paste, PasteMsg,
KeyboardEnhancements, KeyReleaseMsg, OSC 9 progress, view.ProgressBar,
snapshot testing, golden files.
