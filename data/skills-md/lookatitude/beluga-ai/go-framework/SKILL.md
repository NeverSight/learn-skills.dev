---
name: go-framework
description: Go framework design patterns for Beluga AI v2. Use when designing package structure, registries, lifecycle, or creating new packages.
---

# Go Framework Patterns

## Package Structure

```
<package>/
├── <interface>.go     # Extension contract
├── registry.go        # Register(), New(), List()
├── hooks.go           # Lifecycle hooks
├── middleware.go       # Middleware type + Apply()
└── providers/          # Built-in implementations
```

## Registry + Factory

```go
var (
    mu       sync.RWMutex
    registry = make(map[string]Factory)
)

func Register(name string, f Factory) {
    mu.Lock()
    defer mu.Unlock()
    registry[name] = f
}

func New(name string, cfg ProviderConfig) (Interface, error) {
    mu.RLock()
    f, ok := registry[name]
    mu.RUnlock()
    if !ok {
        return nil, fmt.Errorf("unknown provider %q (registered: %v)", name, List())
    }
    return f(cfg)
}

func List() []string { /* sorted keys */ }
```

## Functional Options

```go
type Option func(*options)
func WithTimeout(d time.Duration) Option { return func(o *options) { o.timeout = d } }
func New(opts ...Option) *Thing { o := defaults(); for _, opt := range opts { opt(&o) }; return &Thing{opts: o} }
```

## Provider Registration

```go
func init() {
    llm.Register("openai", func(cfg llm.ProviderConfig) (llm.ChatModel, error) { return New(cfg) })
}
// Users import: import _ "github.com/lookatitude/beluga-ai/llm/providers/openai"
```

## Rules

- Compile-time interface check: `var _ Interface = (*Impl)(nil)`
- Lifecycle: Start(ctx), Stop(ctx), Health() — shutdown in reverse order.
- Error handling: return `(T, error)`, wrap with core.Error, check IsRetryable().
- context.Context is always first parameter.
