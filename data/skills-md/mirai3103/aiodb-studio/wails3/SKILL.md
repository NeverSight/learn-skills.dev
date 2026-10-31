---
name: wails3
description: Build cross-platform desktop apps with Go + Web technologies using Wails v3. Use this skill whenever the user is working with Wails v3 — creating a new project, running or building the app, generating TypeScript/JavaScript bindings from Go code, registering services, using the frontend runtime API (Events, Window, Dialogs, Clipboard, Screens, WML), configuring the application, handling service lifecycles, using the CLI, or packaging for distribution. Trigger on any mentions of wails3, wails v3, go desktop app, bindings generation, @wailsio/runtime, or service registration.
---

# Wails v3 Skill

Wails v3 lets you build native desktop apps using Go for the backend and any web framework for the frontend. The Go–JavaScript bridge handles all IPC automatically — no HTTP, no boilerplate.

## Quick Reference

| Topic | Reference File |
|---|---|
| CLI commands (`init`, `dev`, `build`, `package`, `generate`) | `references/cli.md` |
| Services & method bindings (Go → JS) | `references/bindings.md` |
| Frontend Runtime API (`@wailsio/runtime`) | `references/runtime.md` |
| Application API (Go side) | `references/application.md` |

Read only the reference file(s) relevant to the user's question.

---

## Installation

```bash
# Requires Go 1.24+, npm (optional), platform deps (see below)
go install -v github.com/wailsapp/wails/v3/cmd/wails3@latest
wails3 doctor   # verifies all dependencies
```

**Platform dependencies:**
- **macOS**: `xcode-select --install`
- **Windows**: WebView2 Runtime (usually pre-installed)
- **Linux**: `gcc`, `gtk3`, `webkit2gtk` — run `wails3 doctor` for distro-specific instructions

---

## Project Lifecycle

### 1. Create project
```bash
wails3 init -n myapp                              # vanilla template
wails3 init -n myapp -t svelte                    # specific template
wails3 init -n myapp -git github.com/user/myapp   # with git setup
```

### 2. Develop (live reload)
```bash
wails3 dev   # hot-reloads frontend; rebuilds Go on save
```

### 3. Build & Run
```bash
wails3 build       # debug build → ./bin/
./bin/myapp        # run the binary
```

### 4. Package for distribution
```bash
wails3 package     # .app (Mac), .exe installer (Win), AppImage/deb/rpm (Linux)
```

---

## Core Concepts

### Services (Go backend)

Any exported Go struct registered as a service gets its exported methods automatically bound to JavaScript.

```go
type GreetService struct{}

func (g *GreetService) Greet(name string) string {
    return "Hello, " + name + "!"
}

// main.go
app := application.New(application.Options{
    Services: []application.Service{
        application.NewService(&GreetService{}),
    },
})
```

Rules:
- Only **exported methods** (PascalCase) are bound
- Methods may return `value`, `error`, or `(value, error)`
- Services are **singletons** — use mutexes for shared state
- Implement `ServiceStartup(ctx, opts) error` / `ServiceShutdown() error` for lifecycle hooks

### Generating Bindings (TypeScript / JavaScript)

```bash
wails3 generate bindings          # JavaScript (default output: frontend/bindings/)
wails3 generate bindings -ts      # TypeScript
wails3 generate bindings -d ./src/api   # custom output directory
wails3 generate bindings -clean   # clean output dir first
```

Bindings regenerate automatically during `wails3 dev`.

**Generated file layout:**
```
frontend/bindings/
└── myapp/
    ├── greetservice.js   (or .ts)
    └── index.js
```

**Using generated bindings:**
```javascript
import { Greet } from './bindings/myapp/greetservice'

const message = await Greet("World")   // "Hello, World!"
```

Errors returned from Go become JavaScript exceptions — wrap in `try/catch`.

### Frontend Runtime (`@wailsio/runtime`)

```bash
npm install --save @wailsio/runtime
```

```javascript
import { Events, Window, Dialogs, Clipboard, Screens, Application, Browser } from '@wailsio/runtime'

// Side-effect import for context menus & window drag (required even if you don't use the API)
import '@wailsio/runtime'
```

Key modules: `Events`, `Window`, `Dialogs`, `Clipboard`, `Screens`, `Application`, `Browser`, `System`

> For full API signatures and examples, read **`references/runtime.md`**.

### Events (Go ↔ JavaScript)

**Emit from Go:**
```go
app.Event.Emit("data-updated", map[string]interface{}{"count": 42})
```

**Listen in JavaScript:**
```javascript
import { Events } from '@wailsio/runtime'
const unsub = Events.On('data-updated', (e) => console.log(e.data))
// cleanup: unsub()
```

**Emit from JavaScript:**
```javascript
await Events.Emit('button-clicked', { id: 'submit' })
```

---

## Project Structure

```
myapp/
├── main.go              # App entry point, service registration, window setup
├── greetservice.go      # Example service
├── go.mod
├── build/
│   ├── config.yml       # Build config
│   └── Taskfile.yml     # Platform build tasks
├── frontend/
│   ├── index.html
│   ├── main.js
│   ├── package.json
│   └── bindings/        # Auto-generated — do not edit manually
└── Taskfile.yml         # Top-level task runner
```

---

## WML (Wails Markup Language)

Declarative HTML attributes for common actions — no JavaScript needed:

```html
<button wml-event="save-clicked">Save</button>
<button wml-window="Minimise">Minimize</button>
<button wml-window="Close" wml-confirm="Close window?">Close</button>
<a href="#" wml-openurl="https://wails.io">Visit Wails</a>
```

---

## Type Mapping (Go → JS/TS)

| Go | JavaScript/TypeScript |
|---|---|
| `string` | `string` |
| `bool` | `boolean` |
| `int`, `float64`, etc. | `number` |
| `[]T` | `T[]` |
| `map[string]T` | `Record<string, T>` |
| `struct` | `class` (with exported fields) |
| `time.Time` | `Date` |
| `error` | thrown `Error` |
| `chan`, `func` | ❌ Not supported (use events / IDs) |

---

## Common Patterns

**Batch operations** (reduce bridge overhead):
```javascript
// ❌ Slow: N calls
for (const item of items) { await ProcessItem(item) }
// ✅ Fast: 1 call
await ProcessItems(items)
```

**Long-running tasks** — emit progress events instead of blocking:
```go
func (s *MyService) ProcessFile(path string) {
    go func() {
        for progress := range processLines(path) {
            s.app.Event.Emit("progress", progress)
        }
        s.app.Event.Emit("done", nil)
    }()
}
```

**Thread-safe service state:**
```go
type CounterService struct {
    count int
    mu    sync.Mutex
}
func (c *CounterService) Increment() int {
    c.mu.Lock(); defer c.mu.Unlock()
    c.count++; return c.count
}
```

---

For detailed CLI flags, Go Application API, full runtime API with all method signatures, or advanced service patterns — read the relevant reference file listed in the Quick Reference table above.
