---
name: go-interfaces
description: Go interface design with registry, middleware, and hooks for Beluga AI v2. Use when creating interfaces, extension contracts, or adding hooks/middleware.
---

# Go Interface Design

## Extension Contract (4 parts)

### 1. Interface (small, 1-4 methods)

```go
type ChatModel interface {
    Generate(ctx context.Context, msgs []schema.Message, opts ...GenerateOption) (*schema.AIMessage, error)
    Stream(ctx context.Context, msgs []schema.Message, opts ...GenerateOption) iter.Seq2[schema.StreamChunk, error]
    BindTools(tools []tool.Tool) ChatModel
    ModelID() string
}
```

### 2. Hooks (all fields optional, nil = skip)

```go
type Hooks struct {
    BeforeGenerate func(ctx context.Context, msgs []schema.Message) (context.Context, []schema.Message, error)
    AfterGenerate  func(ctx context.Context, resp *schema.AIMessage, err error) (*schema.AIMessage, error)
    OnError        func(ctx context.Context, err error) error
}
func ComposeHooks(hooks ...Hooks) Hooks { /* chain: each receives output of previous */ }
```

### 3. Middleware: `func(T) T`

```go
type Middleware func(ChatModel) ChatModel
func ApplyMiddleware(model ChatModel, mws ...Middleware) ChatModel {
    for i := len(mws) - 1; i >= 0; i-- { model = mws[i](model) }
    return model
}
```

### 4. Registry

See `go-framework` skill.

## Rules

- Accept interfaces, return structs.
- If interface > 4 methods, split it.
- Optional capabilities via type assertion: `if br, ok := r.(BatchRetriever); ok { ... }`
- Embed for composition: `type MyAgent struct { agent.BaseAgent; ... }`
- Hook naming: `Before<Action>` (modify input), `After<Action>` (modify output), `On<Event>` (observe/modify).
- Middleware applies first (outermost), hooks fire within execution.
