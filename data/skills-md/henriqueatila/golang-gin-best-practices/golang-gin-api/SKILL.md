---
name: golang-gin-api
description: "Build REST APIs with Go Gin framework. Covers routing, handler patterns, request binding/validation, middleware chains, error handling, security headers (OWASP), CORS, timeout middleware, and layered project structure. Use when creating Go web servers, REST endpoints, HTTP handlers, or working with the Gin framework. Also activate when the user mentions Gin routes, middleware, JSON responses, request parsing, or API structure in Go."
license: MIT
metadata:
  author: henriqueatila
  version: 1.0.5
---

# golang-gin-api — Core REST API Development

Build production-grade REST APIs with Go and Gin. This skill covers the 80% of patterns you need daily: server setup, routing, request binding, response formatting, and error handling.

## When to Use

- Creating a new Go REST API or HTTP server
- Adding routes, handlers, or middleware to a Gin app
- Binding and validating incoming JSON/query/URI parameters
- Structuring a Go project with a layered project structure
- Wiring handlers → services → repositories in main.go
- Returning consistent JSON error responses

## Project Structure

```
myapp/
├── cmd/
│   └── api/
│       └── main.go          # Entry point, wiring
├── internal/
│   ├── handler/             # HTTP handlers (thin layer)
│   ├── service/             # Business logic
│   ├── repository/          # Data access
│   └── domain/              # Entities, interfaces, errors
├── pkg/
│   └── middleware/          # Shared middleware
└── go.mod
```

Use `internal/` for code that must not be imported by other modules. Use `pkg/` for reusable middleware and utilities.

## Server Setup with Graceful Shutdown

```go
package main

import (
    "context"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
    "myapp/internal/handler"
    "myapp/internal/service"
    "myapp/internal/repository"
    "myapp/pkg/auth"       // see gin-auth skill
    "myapp/pkg/middleware"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    // Production: gin.New() + explicit middleware (NOT gin.Default())
    r := gin.New()
    r.SetTrustedProxies([]string{"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}) // proxy CIDRs — c.ClientIP() is spoofable without this
    // For CDN (Cloudflare/GAE/Fly.io): use r.TrustedPlatform = gin.PlatformCloudflare instead
    r.Use(middleware.Logger(logger))
    r.Use(middleware.Recovery(logger))

    // Dependency injection (db initialized via gin-database skill)
    var db *gorm.DB // see gin-database skill for initialization
    userRepo := repository.NewUserRepository(db)
    userSvc := service.NewUserService(userRepo)
    userHandler := handler.NewUserHandler(userSvc, logger)
    authHandler := handler.NewAuthHandler(userSvc, logger)     // see gin-auth skill
    tokenCfg := auth.TokenConfig{Secret: os.Getenv("JWT_SECRET")} // see gin-auth skill

    registerRoutes(r, userHandler, authHandler, tokenCfg, logger)

    srv := &http.Server{
        Addr:              ":" + os.Getenv("PORT"),
        Handler:           r,
        ReadHeaderTimeout: 10 * time.Second,  // guards against Slowloris (CWE-400)
        ReadTimeout:       30 * time.Second,
        WriteTimeout:      30 * time.Second,
        IdleTimeout:       120 * time.Second,
    }

    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Error("server failed", "error", err)
            os.Exit(1)
        }
    }()

    // Buffered channel — unbuffered misses signals
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        logger.Error("graceful shutdown failed", "error", err)
    }
}
```

## Domain Model

> **Architecture note:** In clean architecture, domain entities should not carry `json` or `binding` tags. Use separate request/response DTOs in the delivery layer. See **golang-gin-clean-arch** Golden Rule 4.

```go
// internal/domain/user.go
package domain

import "time"

type User struct {
    ID           string    `json:"id"`
    Name         string    `json:"name"`
    Email        string    `json:"email"`
    PasswordHash string    `json:"-"` // never exposed via API
    Role         string    `json:"role"`
    CreatedAt    time.Time `json:"created_at"`
    UpdatedAt    time.Time `json:"updated_at"`
}

type CreateUserRequest struct {
    Name     string `json:"name"     binding:"required,min=2,max=100"`
    Email    string `json:"email"    binding:"required,email"`
    Password string `json:"password" binding:"required,min=8"`
    Role     string `json:"role"     binding:"omitempty,oneof=admin user"`
}
```

## Thin Handler Pattern

> **Security note:** In production, never expose raw `err.Error()` to clients. Return generic messages and log the error server-side. See **golang-gin-clean-arch** error handling patterns.

Handlers bind input, call a service, and format the response. No business logic.

```go
// internal/handler/user_handler.go
package handler

import (
    "log/slog"
    "net/http"

    "github.com/gin-gonic/gin"
    "myapp/internal/domain"
    "myapp/internal/service"
)

type UserHandler struct {
    svc    service.UserService
    logger *slog.Logger
}

func NewUserHandler(svc service.UserService, logger *slog.Logger) *UserHandler {
    return &UserHandler{svc: svc, logger: logger}
}

func (h *UserHandler) Create(c *gin.Context) {
    var req domain.CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        // validationErrors formats validator messages into field-level errors (see error-handling.md)
        c.JSON(http.StatusBadRequest, gin.H{
            "error":  "validation failed",
            "fields": validationErrors(err),
        })
        return
    }

    user, err := h.svc.Create(c.Request.Context(), req)
    if err != nil {
        handleServiceError(c, err, h.logger)
        return
    }

    c.JSON(http.StatusCreated, user)
}

func (h *UserHandler) GetByID(c *gin.Context) {
    type uriParams struct {
        ID string `uri:"id" binding:"required"`
    }
    var params uriParams
    if err := c.ShouldBindURI(&params); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request parameters"})
        return
    }

    user, err := h.svc.GetByID(c.Request.Context(), params.ID)
    if err != nil {
        handleServiceError(c, err, h.logger)
        return
    }

    c.JSON(http.StatusOK, user)
}
```

## Route Registration

```go
func registerRoutes(r *gin.Engine, userHandler *handler.UserHandler, authHandler *handler.AuthHandler, tokenCfg auth.TokenConfig, logger *slog.Logger) {
    // Health check — no auth required
    r.GET("/health", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{"status": "ok"})
    })

    api := r.Group("/api/v1")

    // Public routes
    public := api.Group("")
    {
        public.POST("/users", userHandler.Create)
        public.POST("/auth/login", authHandler.Login)
    }

    // Protected routes — for JWT middleware, see gin-auth skill
    protected := api.Group("")
    protected.Use(middleware.Auth(tokenCfg, logger)) // see gin-auth skill
    {
        protected.GET("/users/:id", userHandler.GetByID)
        protected.GET("/users", userHandler.List)
        protected.PUT("/users/:id", userHandler.Update)
        protected.DELETE("/users/:id", userHandler.Delete)
    }
}
```

## Request Binding Patterns

```go
// JSON body
var req domain.CreateUserRequest
if err := c.ShouldBindJSON(&req); err != nil { ... }

// Query string: GET /users?page=1&limit=20&role=admin
type ListQuery struct {
    Page  int    `form:"page"  binding:"min=1"`
    Limit int    `form:"limit" binding:"min=1,max=100"`
    Role  string `form:"role"  binding:"omitempty,oneof=admin user"`
}
var q ListQuery
if err := c.ShouldBindQuery(&q); err != nil { ... }

// URI parameters: GET /users/:id
type URIParams struct {
    ID string `uri:"id" binding:"required"`
}
var params URIParams
if err := c.ShouldBindURI(&params); err != nil { ... }
```

**Critical:** Always use `ShouldBind*` — `Bind*` auto-aborts with 400 and prevents custom error responses.

## Input Sanitization

Struct tags validate format and constraints. Sanitize string fields **after** binding to neutralize injection payloads before they reach services or storage.

```go
import (
    "html"
    "path/filepath"
    "strings"
)

func (h *UserHandler) Create(c *gin.Context) {
    var req domain.CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Sanitize after bind: trim whitespace, escape HTML entities
    req.Name = strings.TrimSpace(req.Name)
    req.Name = html.EscapeString(req.Name)
    req.Email = strings.TrimSpace(req.Email)
    req.Email = strings.ToLower(req.Email)

    user, err := h.svc.Create(c.Request.Context(), req)
    // ...
}
```

For file uploads, always strip directory components from client-supplied filenames:

```go
safeName := filepath.Base(file.Filename)
dst := filepath.Join("uploads", safeName)
```

## Centralized Error Handling

> **Note:** This `AppError` is a simplified version for this skill's examples. For the canonical domain error pattern with `Detail` field and 5xx guard, see the **golang-gin-clean-arch** skill.

```go
// internal/domain/errors.go
package domain

import "errors"

type AppError struct {
    Code    int
    Message string
    Err     error
}

func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error  { return e.Err }

// Is enables errors.Is() to match AppErrors by code or unwrap to check sentinel errors.
func (e *AppError) Is(target error) bool {
    t, ok := target.(*AppError)
    if ok {
        return e.Code == t.Code
    }
    return errors.Is(e.Err, target)
}

var (
    ErrNotFound       = &AppError{Code: 404, Message: "resource not found"}
    ErrUnauthorized   = &AppError{Code: 401, Message: "unauthorized"}
    ErrForbidden      = &AppError{Code: 403, Message: "forbidden"}
    ErrConflict       = &AppError{Code: 409, Message: "resource already exists"}
    ErrValidation     = &AppError{Code: 422, Message: "validation failed"}
)
```

```go
// internal/handler/errors.go
package handler

import (
    "errors"
    "log/slog"
    "net/http"

    "github.com/gin-gonic/gin"
    "myapp/internal/domain"
)

// handleServiceError maps domain errors to HTTP responses.
// Logger is used to record 5xx errors — the actual error is never sent to clients.
func handleServiceError(c *gin.Context, err error, logger *slog.Logger) {
    var appErr *domain.AppError
    if errors.As(err, &appErr) {
        if appErr.Code >= 500 {
            logger.ErrorContext(c.Request.Context(), "service error", "error", err, "path", c.FullPath())
        }
        c.JSON(appErr.Code, gin.H{"error": appErr.Message})
        return
    }
    logger.ErrorContext(c.Request.Context(), "unhandled error", "error", err, "path", c.FullPath())
    c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
}
```

## Goroutine Safety

**Always call `c.Copy()` before passing `*gin.Context` to a goroutine.** The original context is reused by the pool after the request ends.

```go
func (h *UserHandler) CreateWithNotification(c *gin.Context) {
    var req domain.CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    user, err := h.svc.Create(c.Request.Context(), req)
    if err != nil {
        handleServiceError(c, err, h.logger)
        return
    }

    // c.Copy() — safe to use in goroutine, original c is NOT
    cCopy := c.Copy()
    go func() {
        h.notifier.SendWelcome(cCopy.Request.Context(), user)
    }()

    c.JSON(http.StatusCreated, user)
}
```

## Reference Files

Load these when you need deeper detail:

- **[references/routing.md](references/routing.md)** — Route groups, API versioning, path parameters, pagination, wildcard routes, file uploads, custom validators, request size limits
- **[references/middleware.md](references/middleware.md)** — CORS, security headers, request logging with slog, rate limiting, request ID, timeout, recovery, custom middleware template
- **[references/error-handling.md](references/error-handling.md)** — Full AppError system, sentinel errors, validation error formatting, panic recovery, consistent JSON error format
- **[references/websocket.md](references/websocket.md)** — WebSocket with gorilla/websocket: upgrade handler, hub pattern, auth before upgrade, ping/pong keepalive, graceful shutdown, JSON messages, testing
- **[references/rate-limiting.md](references/rate-limiting.md)** — Deep-dive rate limiting: token bucket, sliding window, Redis distributed, per-user/API-key quotas, tiered limits, response headers, graceful degradation

## Cross-Skill References

- For JWT middleware to protect routes: see the **golang-gin-auth** skill
- For wiring repositories into services and handlers: see the **golang-gin-database** skill
- For testing handlers and services: see the **golang-gin-testing** skill
- For Dockerizing this project structure: see the **golang-gin-deploy** skill
- **golang-gin-clean-arch** → Architecture: 4-layer separation, dependency injection, error propagation, input sanitization

## Official Docs

If this skill doesn't cover your use case, consult the [Gin documentation](https://gin-gonic.com/docs/) or [Gin GoDoc](https://pkg.go.dev/github.com/gin-gonic/gin).
