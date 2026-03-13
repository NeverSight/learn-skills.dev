---
name: go-logging
description: Use when adding or configuring structured logging in Go projects, integrating zap-based log with request context, or when the user asks about logging. Places log package under pkg/logs for new projects.
---

# Go Logging (zap-based)

Structured logging using zap with console/file output, rotation, and request context.

## Placement

| Project Type | Path / Lookup order |
|--------------|---------------------|
| **New project** | `pkg/logs/` |
| **Existing project** | 1) `pkg/log` 2) `pkg/logs` 3) `pkg/utils/log/` (fallback) |

For **new projects**, **MUST** create the log package under `pkg/logs/`.

For **existing projects**, use the first found among `pkg/log`, `pkg/logs`; only use `pkg/utils/log/` when neither exists.

## Dependencies

- `go.uber.org/zap`
- `github.com/natefinch/lumberjack` (for file rotation)
- For `WithRequestID`: a `request` package that provides `GetRequestID(ctx)` and `REQUEST_ID_KEY`; new projects may implement a simple version using `context.Value` with a custom key.

## Config

```go
type Config struct {
    Console   bool   // console output
    AddSource bool   // caller info
    Level     string // debug, info, warn, error, fatal
    Format    string // json | text
    Rotate    OutFile
}

type OutFile struct {
    Enabled    bool
    OutputPath string
    MaxSize    int  // MB
    MaxAge     int  // days
    MaxBackups int
    Compress   bool
    LocalTime  bool
}
```

## Dual Output (file + console)

When **OutFile.Enabled** and **Console** are both true, output **MUST** go to both disk and console. Use `zapcore.NewMultiWriteSyncer` to combine writers:

```go
var mws []zapcore.WriteSyncer

if c.Rotate.Enabled {
    rotateCfg := &lumberjack.Logger{
        Filename:   fn,
        MaxSize:    c.Rotate.MaxSize,
        MaxAge:     c.Rotate.MaxAge,
        MaxBackups: c.Rotate.MaxBackups,
        Compress:   c.Rotate.Compress,
        LocalTime:  c.Rotate.LocalTime,
    }
    mws = append(mws, zapcore.AddSync(rotateCfg))
}
if c.Console {
    mws = append(mws, zapcore.AddSync(os.Stdout))
}

mw := zapcore.NewMultiWriteSyncer(mws...)
core := zapcore.NewCore(encoder, mw, level)
```

## Init

Call from `main` or server bootstrap:

```go
log.Init(log.Config{
    Console:   true,
    AddSource: true,
    Level:     "info",
    Format:    "json",
    Rotate: log.OutFile{
        Enabled:    true,
        OutputPath: "./logs",  // or pkg/logs relative path
        MaxSize:    100,
        MaxAge:     7,
        MaxBackups: 3,
    },
})
```

## API Summary

| Function | Purpose |
|----------|---------|
| `log.Init(c Config)` | Initialize logger (call once at startup) |
| `log.Logger() *zap.Logger` | Get global logger; returns default console if not initialized |
| `log.WithRequestID(ctx, l) *zap.Logger` | Attach request_id from context to logger |
| `log.Debug/Info/Warn/Error(msg, fields...)` | Package-level logging |

## Service Usage Pattern

1. **Inject logger** via constructor: `NewService(..., logger *zap.Logger)`.
2. **Use `WithRequestID(ctx, logger)`** at the start of request-scoped methods.
3. **Structured fields**: `zap.Error(err)`, `zap.String()`, `zap.Any()`, `zap.Int()`.
4. **Log at boundaries** only: entry, validation failure, success, error—avoid logging in loops.
5. **Do NOT log** secrets, tokens, passwords, or PII.

## Quick Reference

| Level | When |
|-------|------|
| Debug | Development/troubleshooting |
| Info | Normal flow, key operations |
| Warn | Validation failure, retry |
| Error | Operation failure, before return err |

For full usage examples, see [examples.md](examples.md).
