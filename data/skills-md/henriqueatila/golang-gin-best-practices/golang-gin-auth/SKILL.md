---
name: golang-gin-auth
description: "Implement authentication and authorization in Go Gin APIs. Covers JWT middleware (jti blacklisting, refresh rotation), login/register handlers, bcrypt password hashing, RBAC, CSRF protection, rate limiting on auth endpoints, secure cookies, and admin impersonation guards. Use when adding auth, login, signup, JWT tokens, user sessions, permissions, or role checks to a Gin application."
license: MIT
metadata:
  author: henriqueatila
  version: 1.0.4
---

# golang-gin-auth — Authentication & Authorization

Add JWT-based authentication and role-based access control to a Gin API. This skill covers the patterns you need for secure APIs: JWT middleware, login handler, token lifecycle, and RBAC.

## When to Use

- Adding JWT authentication to a Gin API
- Implementing login or registration endpoints
- Protecting routes with middleware
- Implementing role-based or permission-based access control (RBAC)
- Handling token refresh and revocation
- Getting the current user in any handler

## Dependencies

```bash
go get github.com/golang-jwt/jwt/v5
go get golang.org/x/crypto
go get github.com/google/uuid
go get golang.org/x/time/rate
```

## Claims Struct

Define custom JWT claims that embed `jwt.RegisteredClaims` (architectural recommendation — uses `github.com/golang-jwt/jwt/v5`):

```go
// internal/auth/claims.go
package auth

import "github.com/golang-jwt/jwt/v5"

// Claims holds the JWT payload for access tokens. Embed RegisteredClaims for standard fields.
// RegisteredClaims.ID carries the jti — required for token blacklisting.
type Claims struct {
    jwt.RegisteredClaims
    UserID string `json:"uid"`
    Email  string `json:"email"`
    Role   string `json:"role"`
    // Add Roles []string for multi-role support, TenantID for multi-tenancy
}

// RefreshClaims is the minimal payload for refresh tokens.
// Only the subject (UserID) is needed — refresh doesn't need role/email.
type RefreshClaims struct {
    jwt.RegisteredClaims
    // RegisteredClaims.ID carries the jti for per-token blacklisting.
}
```

## Token Generation and Validation

```go
// internal/auth/token.go
package auth

import (
    "errors"
    "fmt"
    "time"

    "github.com/golang-jwt/jwt/v5"
    "github.com/google/uuid"
)

// TokenConfig holds secrets and TTLs. Load from environment, never hardcode.
type TokenConfig struct {
    AccessSecret  []byte
    RefreshSecret []byte
    AccessTTL     time.Duration // e.g. 15 * time.Minute
    RefreshTTL    time.Duration // e.g. 7 * 24 * time.Hour
    Issuer        string        // e.g. "myapp"
    Audience      []string      // e.g. ["api.myapp.com"]
}

// GenerateAccessToken creates a signed JWT access token for the given user.
// Architectural recommendation — not part of the Gin API.
func GenerateAccessToken(cfg TokenConfig, userID, email, role string) (string, error) {
    now := time.Now()
    claims := Claims{
        RegisteredClaims: jwt.RegisteredClaims{
            ID:        uuid.NewString(), // jti — required for token blacklisting
            Subject:   userID,
            Issuer:    cfg.Issuer,
            Audience:  jwt.ClaimStrings(cfg.Audience),
            IssuedAt:  jwt.NewNumericDate(now),
            NotBefore: jwt.NewNumericDate(now), // token not valid before issue time
            ExpiresAt: jwt.NewNumericDate(now.Add(cfg.AccessTTL)),
        },
        UserID: userID,
        Email:  email,
        Role:   role,
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    signed, err := token.SignedString(cfg.AccessSecret)
    if err != nil {
        return "", fmt.Errorf("sign access token: %w", err)
    }
    return signed, nil
}

// GenerateRefreshToken creates a longer-lived refresh token (user ID only).
func GenerateRefreshToken(cfg TokenConfig, userID string) (string, error) {
    now := time.Now()
    claims := RefreshClaims{
        RegisteredClaims: jwt.RegisteredClaims{
            ID:        uuid.NewString(), // jti — required for per-token blacklisting
            Subject:   userID,
            Issuer:    cfg.Issuer,
            IssuedAt:  jwt.NewNumericDate(now),
            NotBefore: jwt.NewNumericDate(now),
            ExpiresAt: jwt.NewNumericDate(now.Add(cfg.RefreshTTL)),
        },
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    signed, err := token.SignedString(cfg.RefreshSecret)
    if err != nil {
        return "", fmt.Errorf("sign refresh token: %w", err)
    }
    return signed, nil
}

// ParseAccessToken validates and parses a JWT access token.
func ParseAccessToken(cfg TokenConfig, tokenStr string) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(t *jwt.Token) (any, error) {
        if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
        }
        return cfg.AccessSecret, nil
    })
    if err != nil {
        if errors.Is(err, jwt.ErrTokenExpired) {
            return nil, fmt.Errorf("token expired: %w", err)
        }
        return nil, fmt.Errorf("invalid token: %w", err)
    }
    claims, ok := token.Claims.(*Claims)
    if !ok || !token.Valid {
        return nil, fmt.Errorf("invalid token claims")
    }
    return claims, nil
}
```

## JWT Middleware

Extracts the Bearer token, validates it, and injects claims into `gin.Context` via `c.Set`. Handlers read claims via `c.Get`.

```go
// pkg/middleware/auth.go
package middleware

import (
    "log/slog"
    "net/http"
    "strings"

    "github.com/gin-gonic/gin"
    "myapp/internal/auth"
)

const (
    ClaimsKey = "claims"   // key used for c.Set / c.Get
    UserIDKey  = "user_id" // convenience string key for c.GetString
)

// Auth returns a Gin middleware that validates JWT Bearer tokens.
// Aborts with 401 if the token is missing, malformed, or expired.
func Auth(cfg auth.TokenConfig, logger *slog.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        header := c.GetHeader("Authorization")
        if header == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "authorization header required"})
            return
        }

        parts := strings.SplitN(header, " ", 2)
        if len(parts) != 2 || !strings.EqualFold(parts[0], "Bearer") {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid authorization header format"})
            return
        }

        claims, err := auth.ParseAccessToken(cfg, parts[1])
        if err != nil {
            logger.Warn("jwt validation failed", "error", err)
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid or expired token"})
            return
        }

        // Inject claims and convenience string keys for type-safe access
        c.Set(ClaimsKey, claims)
        c.Set(UserIDKey, claims.UserID)
        c.Next()
    }
}
```

## Registration — Password Hashing

Always hash passwords with bcrypt before storing. Use cost >= 12 for production.

```go
// internal/handler/auth_handler.go (Register method)

type registerRequest struct {
    Email    string `json:"email"    binding:"required,email"`
    Password string `json:"password" binding:"required,min=8"`
}

func (h *AuthHandler) Register(c *gin.Context) {
    var req registerRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request body"})
        return
    }

    // Hash password with bcrypt — cost 12 minimum for production
    hash, err := bcrypt.GenerateFromPassword([]byte(req.Password), 12)
    if err != nil {
        h.logger.Error("failed to hash password", "error", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
        return
    }

    user, err := h.userRepo.Create(c.Request.Context(), domain.CreateUserRequest{
        Email:        req.Email,
        PasswordHash: string(hash),
    })
    if err != nil {
        h.logger.Error("failed to create user", "error", err)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
        return
    }

    c.JSON(http.StatusCreated, gin.H{"user_id": user.ID})
}
```

## Login Handler

> **Security note:** Never expose raw `err.Error()` to clients. Return generic messages and log the error server-side. See **golang-gin-clean-arch** error handling patterns.

Validates credentials via `UserRepository`, then returns both tokens. Thin handler — no business logic beyond orchestration.

```go
// internal/handler/auth_handler.go
package handler

import (
    "log/slog"
    "net/http"

    "github.com/gin-gonic/gin"
    "golang.org/x/crypto/bcrypt"
    "myapp/internal/auth"
    "myapp/internal/domain"
)

type AuthHandler struct {
    userRepo domain.UserRepository
    tokenCfg auth.TokenConfig
    logger   *slog.Logger
}

func NewAuthHandler(userRepo domain.UserRepository, cfg auth.TokenConfig, logger *slog.Logger) *AuthHandler {
    return &AuthHandler{userRepo: userRepo, tokenCfg: cfg, logger: logger}
}

type loginRequest struct {
    Email    string `json:"email"    binding:"required,email"`
    Password string `json:"password" binding:"required"`
}

type tokenResponse struct {
    AccessToken  string `json:"access_token"`
    RefreshToken string `json:"refresh_token"`
}

func (h *AuthHandler) Login(c *gin.Context) {
    var req loginRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request body"})
        return
    }

    user, err := h.userRepo.GetByEmail(c.Request.Context(), req.Email)
    if err != nil {
        // Return generic message — don't leak whether email exists
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
        return
    }

    if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password)); err != nil {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
        return
    }

    accessToken, err := auth.GenerateAccessToken(h.tokenCfg, user.ID, user.Email, user.Role)
    if err != nil {
        h.logger.Error("failed to generate access token", "error", err, "user_id", user.ID)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
        return
    }

    refreshToken, err := auth.GenerateRefreshToken(h.tokenCfg, user.ID)
    if err != nil {
        h.logger.Error("failed to generate refresh token", "error", err, "user_id", user.ID)
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
        return
    }

    c.JSON(http.StatusOK, tokenResponse{
        AccessToken:  accessToken,
        RefreshToken: refreshToken,
    })
}
```

## Protected Routes — Applying Auth Middleware

Wire the engine with `gin.New()` + explicit middleware, then apply `Auth` to route groups:

```go
// cmd/api/main.go — engine setup (always gin.New(), never gin.Default() in production)
r := gin.New()
r.Use(middleware.Logger(logger))
r.Use(middleware.Recovery(logger))
registerRoutes(r, authHandler, userHandler, tokenCfg, logger)
```

```go
// cmd/api/main.go (route registration)
func registerRoutes(r *gin.Engine, authHandler *handler.AuthHandler, userHandler *handler.UserHandler, cfg auth.TokenConfig, logger *slog.Logger) {
    r.GET("/health", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{"status": "ok"})
    })

    api := r.Group("/api/v1")

    // Auth routes — rate-limited: 5 requests per minute per IP
    authRoutes := api.Group("/auth")
    authRoutes.Use(middleware.IPRateLimiter(rate.Every(12*time.Second), 5))
    {
        authRoutes.POST("/login", authHandler.Login)
        authRoutes.POST("/register", authHandler.Register)
        authRoutes.POST("/refresh", authHandler.Refresh)
    }
    api.POST("/users", userHandler.Create) // registration (also rate-limit in production)

    // Protected routes — JWT required
    protected := api.Group("")
    protected.Use(middleware.Auth(cfg, logger))
    {
        protected.GET("/users/:id", userHandler.GetByID)
        protected.PUT("/users/:id", userHandler.Update)
        protected.DELETE("/users/:id", userHandler.Delete)

        // Admin-only routes — add RBAC middleware
        admin := protected.Group("/admin")
        admin.Use(middleware.RequireRole("admin"))
        {
            admin.GET("/users", userHandler.List)
        }
    }
}
```

### Rate Limiter Middleware

```go
// pkg/middleware/rate_limiter.go
package middleware

import (
    "net/http"
    "sync"

    "github.com/gin-gonic/gin"
    "golang.org/x/time/rate"
)

// IPRateLimiter limits requests per IP using a token-bucket algorithm.
// r controls how fast tokens refill; b is the burst (max simultaneous requests).
func IPRateLimiter(r rate.Limit, b int) gin.HandlerFunc {
    limiters := make(map[string]*rate.Limiter)
    var mu sync.Mutex

    getLimiter := func(ip string) *rate.Limiter {
        mu.Lock()
        defer mu.Unlock()
        if lim, ok := limiters[ip]; ok {
            return lim
        }
        lim := rate.NewLimiter(r, b)
        limiters[ip] = lim
        return lim
    }

    return func(c *gin.Context) {
        lim := getLimiter(c.ClientIP())
        if !lim.Allow() {
            c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"error": "too many requests"})
            return
        }
        c.Next()
    }
}
```

> **Production note:** The in-process map above works for single-instance deployments. For multi-instance deployments, use a Redis-backed limiter (e.g. `go-redis/redis_rate`) so limits are shared across all pods.

## Getting Current User in Handlers

```go
// Read claims injected by Auth middleware
func (h *UserHandler) GetMe(c *gin.Context) {
    // Option 1: type-safe string shortcut
    userID := c.GetString(middleware.UserIDKey)

    // Option 2: full claims object (for role, email, etc.)
    val, exists := c.Get(middleware.ClaimsKey)
    if !exists {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
        return
    }
    claims, ok := val.(*auth.Claims)
    if !ok {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
        return
    }

    user, err := h.svc.GetByID(c.Request.Context(), userID)
    if err != nil {
        handleServiceError(c, err, h.logger)
        return
    }

    c.JSON(http.StatusOK, gin.H{
        "user": user,
        "role": claims.Role,
    })
}
```

## Reference Files

Load these when you need deeper detail:

- **[references/jwt-patterns.md](references/jwt-patterns.md)** — Access + refresh token architecture, token refresh endpoint, token blacklisting (Redis), RS256 vs HS256, custom claims, storage recommendations (httpOnly cookie vs localStorage), CSRF protection, complete auth flow
- **[references/rbac.md](references/rbac.md)** — RequireRole/RequireAnyRole middleware, permission-based access, role hierarchy, multi-tenant authorization, resource-level authorization, complete RBAC example

## Cross-Skill References

- For handler patterns (ShouldBindJSON, error responses, route groups): see the **golang-gin-api** skill
- For `UserRepository` interface and `GetByEmail` implementation: see the **golang-gin-database** skill
- For testing JWT middleware and auth handlers: see the **golang-gin-testing** skill
- **golang-gin-clean-arch** → Architecture: where auth middleware fits (delivery layer only), DI patterns for auth services

## Official Docs

If this skill doesn't cover your use case, consult the [Gin documentation](https://gin-gonic.com/docs/), [golang-jwt GoDoc](https://pkg.go.dev/github.com/golang-jwt/jwt/v5), or [Gin GoDoc](https://pkg.go.dev/github.com/gin-gonic/gin).
