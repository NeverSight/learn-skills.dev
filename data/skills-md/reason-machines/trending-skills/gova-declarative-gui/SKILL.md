---
name: gova-declarative-gui
description: Build native desktop apps in Go using Gova's declarative, component-based GUI framework with reactive state and platform-native integrations.
triggers:
  - build a desktop app with Go
  - declarative GUI in Go
  - native desktop app Go framework
  - gova component state
  - Go GUI reactive state
  - cross-platform desktop app Go
  - gova dev hot reload
  - Go native dialogs desktop
---

# Gova Declarative GUI Framework

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Gova is a declarative GUI framework for Go that builds native desktop apps for macOS, Windows, and Linux from a single codebase. Views are plain Go structs, state is explicit via a `Scope`, and `go build` produces one static binary. Internally powered by Fyne (BSD-3), but the public API is stable and renderer-independent.

---

## Install

```bash
go get github.com/nv404/gova@latest
```

Optional CLI:

```bash
go install github.com/nv404/gova/cmd/gova@latest
```

**Prerequisites:**
- Go 1.26+
- C toolchain: Xcode CLT (macOS), `build-essential` + `libgl1-mesa-dev` (Linux), MinGW (Windows)

---

## Key CLI Commands

| Command | Purpose |
|---|---|
| `gova dev ./path/to/app` | Hot reload — watch `.go` files, rebuild and relaunch on save |
| `gova build ./path/to/app` | Compile to `./bin/<name>` static binary |
| `gova run ./path/to/app` | Build and launch once, no file watching |
| `go build -ldflags "-s -w"` | Stripped binary (~23 MB for simple apps) |

---

## Core Concepts

### 1. Components as Structs

A component is a Go struct implementing `Body(s *g.Scope) g.View`. Fields on the struct are typed props; zero values are defaults.

```go
package main

import g "github.com/nv404/gova"

type Greeting struct {
    Name string // prop with zero-value default ""
}

func (c Greeting) Body(s *g.Scope) g.View {
    name := c.Name
    if name == "" {
        name = "World"
    }
    return g.Text("Hello, " + name + "!").Font(g.Title)
}
```

### 2. Reactive State with Scope

State lives on the `*g.Scope` passed to `Body`. No hidden scheduler, no hook-ordering rules.

```go
func (Counter) Body(s *g.Scope) g.View {
    count := g.State(s, 0) // typed signal, initial value 0

    return g.VStack(
        g.Text(count.Format("Count: %d")).Font(g.Title),
        g.HStack(
            g.Button("-", func() { count.Set(count.Get() - 1) }),
            g.Button("+", func() { count.Set(count.Get() + 1) }),
        ).Spacing(g.SpaceMD),
    ).Padding(g.SpaceLG)
}
```

### 3. Entry Point

```go
func main() {
    g.Run("My App", g.Component(MyComponent{}))
}
```

---

## Layout Primitives

```go
// Vertical stack
g.VStack(child1, child2, child3).Spacing(g.SpaceMD).Padding(g.SpaceLG)

// Horizontal stack
g.HStack(child1, child2).Spacing(g.SpaceSM)

// Layered/overlapping stack
g.ZStack(background, foreground)

// Scaffold (app shell with nav, toolbar, etc.)
g.Scaffold(
    g.NavBar("Title"),
    content,
)
```

### Spacing Constants

| Constant | Use |
|---|---|
| `g.SpaceSM` | Small gaps |
| `g.SpaceMD` | Medium gaps |
| `g.SpaceLG` | Large padding |

---

## Built-in Views

```go
g.Text("Hello").Font(g.Title)        // styled text
g.Text("body text").Font(g.Body)

g.Button("Click me", func() { /* handler */ })

g.TextField(value.Get(), func(s string) { value.Set(s) })

g.Toggle(enabled.Get(), func(b bool) { enabled.Set(b) })

g.Image("path/to/image.png")

g.Spacer() // flexible space
g.Divider()
```

### Font Constants

`g.Title`, `g.Headline`, `g.Body`, `g.Caption`, `g.Mono`

---

## State Patterns

### Basic State

```go
count := g.State(s, 0)
count.Get()        // read
count.Set(42)      // write, triggers re-render
count.Format("Value: %d") // returns formatted string signal
```

### Derived / Computed State

```go
doubled := g.Derived(s, func() int {
    return count.Get() * 2
})
```

### Effects (side effects on state change)

```go
g.Effect(s, func() {
    fmt.Println("count changed to", count.Get())
}, count) // dependencies
```

### Persisted State (survives hot reload)

```go
name := g.PersistedState(s, "user-name", "")
```

---

## Full Example: Todo App

```go
package main

import g "github.com/nv404/gova"

type Todo struct {
    Text string
    Done bool
}

type TodoApp struct{}

func (TodoApp) Body(s *g.Scope) g.View {
    todos := g.State(s, []Todo{})
    input := g.State(s, "")

    addTodo := func() {
        if input.Get() == "" {
            return
        }
        todos.Set(append(todos.Get(), Todo{Text: input.Get()}))
        input.Set("")
    }

    rows := make([]g.View, 0, len(todos.Get()))
    for i, todo := range todos.Get() {
        i, todo := i, todo // capture loop vars
        rows = append(rows, g.HStack(
            g.Toggle(todo.Done, func(v bool) {
                list := todos.Get()
                list[i].Done = v
                todos.Set(list)
            }),
            g.Text(todo.Text),
        ).Spacing(g.SpaceSM))
    }

    return g.VStack(
        g.Text("Todos").Font(g.Title),
        g.VStack(rows...).Spacing(g.SpaceSM),
        g.HStack(
            g.TextField(input.Get(), func(v string) { input.Set(v) }),
            g.Button("Add", addTodo),
        ).Spacing(g.SpaceSM),
    ).Padding(g.SpaceLG)
}

func main() {
    g.Run("Todo", g.Component(TodoApp{}))
}
```

---

## Native Dialogs (macOS: NSAlert / NSOpenPanel; other platforms: Fyne fallback)

```go
// Alert dialog
g.Button("Alert", func() {
    g.Alert(g.AlertOptions{
        Title:   "Warning",
        Message: "Something happened.",
        Style:   g.AlertWarning,
    })
})

// Open file dialog
g.Button("Open File", func() {
    path, err := g.OpenFileDialog(g.OpenFileOptions{
        Title:      "Choose a file",
        Extensions: []string{".txt", ".md"},
    })
    if err == nil && path != "" {
        filePath.Set(path)
    }
})

// Save file dialog
g.Button("Save", func() {
    dest, err := g.SaveFileDialog(g.SaveFileOptions{
        Title:           "Save As",
        DefaultFilename: "output.txt",
    })
    if err == nil && dest != "" {
        // write to dest
    }
})
```

---

## Platform Integration (macOS Dock)

```go
// Dock badge (macOS)
g.DockBadge("3")
g.DockBadge("") // clear badge

// Dock progress (macOS)
g.DockProgress(0.75) // 0.0–1.0
g.DockProgress(-1)   // hide

// Dock menu (macOS)
g.SetDockMenu([]g.MenuItem{
    {Label: "New Window", Action: func() { /* ... */ }},
    {Label: "Preferences", Action: func() { /* ... */ }},
})
```

---

## Theming and Colors

```go
// Dark/light toggle
g.Button("Toggle Theme", func() {
    if g.CurrentTheme() == g.ThemeDark {
        g.SetTheme(g.ThemeLight)
    } else {
        g.SetTheme(g.ThemeDark)
    }
})

// Semantic colors in custom views
g.Text("Primary").Color(g.ColorPrimary)
g.Text("Secondary").Color(g.ColorSecondary)
g.Text("Danger").Color(g.ColorDanger)
```

---

## Component Composition with Viewable

```go
type Card struct {
    Title   string
    Content g.View
}

func (c Card) Body(s *g.Scope) g.View {
    return g.VStack(
        g.Text(c.Title).Font(g.Headline),
        g.Divider(),
        c.Content,
    ).Padding(g.SpaceMD)
}

// Usage
g.Component(Card{
    Title:   "My Card",
    Content: g.Text("Card body text"),
})
```

---

## Navigation / Multi-View

```go
type NotesApp struct{}

func (NotesApp) Body(s *g.Scope) g.View {
    selected := g.State(s, "list")

    switch selected.Get() {
    case "detail":
        return g.Component(DetailView{OnBack: func() { selected.Set("list") }})
    default:
        return g.Component(ListView{OnSelect: func() { selected.Set("detail") }})
    }
}
```

---

## App Icon at Runtime

```go
func main() {
    app := g.NewApp("My App")
    app.SetIcon("assets/icon.png") // set before Run
    app.Run(g.Component(MyComponent{}))
}
```

---

## Hot Reload with PersistedState

When using `gova dev`, use `g.PersistedState` to keep UI state across rebuilds:

```go
func (MyApp) Body(s *g.Scope) g.View {
    // survives hot reload, lost on full restart
    activeTab := g.PersistedState(s, "active-tab", "home")
    // ...
}
```

---

## Project Structure (recommended)

```
myapp/
├── main.go          # g.Run entry point
├── components/
│   ├── header.go
│   └── sidebar.go
├── views/
│   ├── home.go
│   └── settings.go
├── assets/
│   └── icon.png
└── go.mod
```

---

## Platform Support Matrix

| Feature | macOS | Windows | Linux |
|---|---|---|---|
| Core UI | ✅ | ✅ | ✅ |
| Hot reload | ✅ | ✅ | ✅ |
| App icon | ✅ | ✅ | ✅ |
| Native dialogs | NSAlert/NSOpenPanel | Fyne fallback | Fyne fallback |
| Dock/taskbar | NSDockTile ✅ | Planned | Planned |

---

## Troubleshooting

**`cgo: C compiler not found`**
- macOS: `xcode-select --install`
- Linux: `sudo apt install build-essential libgl1-mesa-dev`
- Windows: Install MinGW-w64 and add to PATH

**`go build` fails with OpenGL errors on Linux**
```bash
sudo apt install libgl1-mesa-dev xorg-dev
```

**Hot reload not picking up changes**
- Ensure you're using `gova dev`, not `go run`
- Confirm `.go` files are in a directory watched by `gova dev ./path`

**Binary is large (~32 MB)**
- Strip symbols: `go build -ldflags "-s -w" -o ./bin/myapp`
- Result: ~23 MB. This is expected — Fyne (OpenGL renderer) is bundled.

**State not updating the UI**
- Always call `count.Set(...)` — mutating a slice/map in place without `Set` won't trigger re-render
- For slices: copy, modify, then set: `list := todos.Get(); list[i] = newVal; todos.Set(list)`

**API breakage (pre-1.0)**
- Pin a specific tag: `go get github.com/nv404/gova@v0.x.y`
- Check the [CHANGELOG](https://github.com/nv404/gova) before upgrading

---

## Useful Links

- Docs: https://gova.dev
- Getting started: https://gova.dev/docs/getting-started/installation
- State & effects: https://gova.dev/docs/state/state
- Native dialogs: https://gova.dev/docs/overlays/native-dialogs
- CLI reference: https://gova.dev/docs/cli/overview
- pkg.go.dev: https://pkg.go.dev/github.com/nv404/gova
