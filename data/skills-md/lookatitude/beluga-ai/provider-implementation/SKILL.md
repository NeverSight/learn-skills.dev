---
name: provider-implementation
description: Implementing providers for Beluga AI v2 registries. Use when creating LLM, embedding, vectorstore, voice, or any other provider.
---

# Provider Implementation

## Checklist

1. Implement the full interface (ChatModel, Embedder, VectorStore, STT, TTS, etc.).
2. Register via `init()` with parent package's `Register()`.
3. Map provider errors to `core.Error` with correct ErrorCode.
4. Support context cancellation.
5. Include token/usage metrics where applicable.
6. Compile-time check: `var _ Interface = (*Impl)(nil)`.
7. Unit tests with mocked HTTP responses (httptest).

## File Structure

```
llm/providers/openai/
├── openai.go          # Implementation + New() + init()
├── stream.go          # Streaming
├── errors.go          # Error mapping
├── openai_test.go     # Tests
└── testdata/          # Recorded HTTP responses
```

## Template

```go
var _ llm.ChatModel = (*Model)(nil)

func init() {
    llm.Register("openai", func(cfg llm.ProviderConfig) (llm.ChatModel, error) { return New(cfg) })
}

func New(cfg llm.ProviderConfig) (*Model, error) {
    if cfg.APIKey == "" { return nil, &core.Error{Op: "openai.new", Code: core.ErrAuth, Message: "API key required"} }
    return &Model{client: newClient(cfg.APIKey, cfg.BaseURL), model: cfg.Model}, nil
}

func (m *Model) Stream(ctx context.Context, msgs []schema.Message, opts ...llm.GenerateOption) iter.Seq2[schema.StreamChunk, error] {
    return func(yield func(schema.StreamChunk, error) bool) { /* stream implementation */ }
}
```

## Error Mapping

```go
switch apiErr.StatusCode {
case 401: code = core.ErrAuth
case 429: code = core.ErrRateLimit
case 408, 504: code = core.ErrTimeout
case 400: code = core.ErrInvalidInput
}
```

See `docs/providers.md` for provider categories and priorities.
