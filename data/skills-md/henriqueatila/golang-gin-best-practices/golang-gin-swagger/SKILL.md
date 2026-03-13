---
name: golang-gin-swagger
description: "Generate Swagger/OpenAPI documentation for Go Gin APIs using swaggo/swag. Covers full CRUD + auth endpoint annotations, model documentation, Swagger UI setup, security definitions, and CI/CD integration. Use when adding API docs, Swagger UI, OpenAPI spec, endpoint documentation, or auto-generated API reference to a Gin application."
license: MIT
metadata:
  author: henriqueatila
  version: 1.0.3
---

# golang-gin-swagger — Swagger/OpenAPI Documentation

Generate and serve Swagger/OpenAPI documentation for Gin APIs using [swaggo/swag](https://github.com/swaggo/swag). This skill covers the 80% you need daily: setup, handler annotations, model tags, Swagger UI, and doc generation.

## When to Use

- Adding Swagger/OpenAPI documentation to a Gin API
- Documenting endpoints with request/response schemas
- Serving Swagger UI for interactive API exploration
- Generating `swagger.json`/`swagger.yaml` from Go annotations
- Documenting JWT Bearer auth in OpenAPI spec
- Setting up CI/CD to validate docs are up to date

## Dependencies

```bash
# CLI tool (generates docs from annotations)
go install github.com/swaggo/swag/cmd/swag@latest

# Go module dependencies
go get -u github.com/swaggo/gin-swagger
go get -u github.com/swaggo/files
```

Ensure `$(go env GOPATH)/bin` is in your `$PATH` so the `swag` CLI is available.

## General API Annotations

Place these directly before `main()` in `cmd/api/main.go`. Only one annotation block per project.

```go
// @title           My API
// @version         1.0
// @description     Production-grade REST API built with Gin.

// @contact.name    API Support
// @contact.email   support@example.com

// @license.name    MIT
// @license.url     https://opensource.org/licenses/MIT

// @host            localhost:8080
// @BasePath        /api/v1
// @schemes         http https

// @securityDefinitions.apikey  BearerAuth
// @in                          header
// @name                        Authorization
// @description                 Enter: Bearer {token}
func main() { ... }
```

## Serving Swagger UI

```go
package main

import (
    "os"

    "github.com/gin-gonic/gin"
    swaggerFiles "github.com/swaggo/files"
    ginSwagger   "github.com/swaggo/gin-swagger"

    _ "myapp/docs" // CRITICAL: blank import registers the generated spec
)

func main() {
    r := gin.New()

    // Only expose Swagger UI outside production
    if os.Getenv("GIN_MODE") != "release" {
        r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
    }

    // ... register routes, start server
}
```

Access at: `http://localhost:8080/swagger/index.html`

**Swagger UI options:**

```go
r.GET("/swagger/*any", ginSwagger.WrapHandler(
    swaggerFiles.Handler,
    ginSwagger.URL("/swagger/doc.json"),
    ginSwagger.DocExpansion("list"),           // "list"|"full"|"none"
    ginSwagger.DeepLinking(true),
    ginSwagger.DefaultModelsExpandDepth(1),    // -1 hides models section
    ginSwagger.PersistAuthorization(true),     // retains Bearer token across reloads
    ginSwagger.DefaultModelExpandDepth(1),    // expand depth for example section
    ginSwagger.DefaultModelRendering("example"), // "example"|"model"
))
```

## Dynamic Host Configuration

Override spec values at runtime for multi-environment deploys:

```go
import (
    "os"
    "myapp/docs"
)

func main() {
    docs.SwaggerInfo.Host     = os.Getenv("API_HOST") // e.g. "api.prod.example.com"
    docs.SwaggerInfo.Schemes  = []string{"https"}
    docs.SwaggerInfo.BasePath = "/api/v1"
    // ...
}
```

## Handler Annotations

Annotate each handler to document the endpoint. Always start with a Go doc comment.

```go
// CreateUser godoc
//
// @Summary      Create a new user
// @Description  Register a new user account
// @Tags         users
// @Accept       json
// @Produce      json
// @Param        request  body      domain.CreateUserRequest  true  "Create user payload"
// @Success      201      {object}  domain.User
// @Failure      400      {object}  domain.ErrorResponse
// @Failure      409      {object}  domain.ErrorResponse
// @Failure      500      {object}  domain.ErrorResponse
// @Router       /users [post]
func (h *UserHandler) Create(c *gin.Context) { ... }

// GetByID godoc
//
// @Summary      Get user by ID
// @Description  Retrieve a single user by UUID
// @Tags         users
// @Produce      json
// @Security     BearerAuth
// @Param        id   path      string  true  "User ID (UUID)"
// @Success      200  {object}  domain.User
// @Failure      400  {object}  domain.ErrorResponse
// @Failure      401  {object}  domain.ErrorResponse
// @Failure      404  {object}  domain.ErrorResponse
// @Failure      500  {object}  domain.ErrorResponse
// @Router       /users/{id} [get]
func (h *UserHandler) GetByID(c *gin.Context) { ... }

// List godoc
//
// @Summary      List users
// @Description  List users with pagination and optional role filter
// @Tags         users
// @Produce      json
// @Security     BearerAuth
// @Param        page   query     int     false  "Page number"      default(1) minimum(1)
// @Param        limit  query     int     false  "Items per page"   default(20) minimum(1) maximum(100)
// @Param        role   query     string  false  "Filter by role"   Enums(admin, user)
// @Success      200    {array}   domain.User
// @Failure      400    {object}  domain.ErrorResponse
// @Failure      401    {object}  domain.ErrorResponse
// @Failure      500    {object}  domain.ErrorResponse
// @Router       /users [get]
func (h *UserHandler) List(c *gin.Context) { ... }
```

**Critical rules:**
- `@Router` uses `{id}` (OpenAPI style), not `:id` (Gin style)
- `@Security BearerAuth` must match the name in `@securityDefinitions.apikey BearerAuth`
- Use named structs in `@Success`/`@Failure` — never `gin.H{}` or `map[string]interface{}`

## Model Documentation

> **Architecture note:** In clean architecture, domain entities should not carry `json` or `binding` tags. Use separate request/response DTOs in the delivery layer. See **golang-gin-clean-arch** Golden Rule 4. The tags here are shown for Swagger annotation purposes — in a clean-arch project, apply them to DTO structs, not domain entities.

Add `example`, `format`, and constraint tags to struct fields for rich Swagger docs:

```go
// internal/domain/user.go
package domain

import "time"

// User represents an authenticated system user.
type User struct {
    ID        string    `json:"id"         example:"550e8400-e29b-41d4-a716-446655440000" format:"uuid"`
    Name      string    `json:"name"       example:"Jane Doe"    minLength:"2" maxLength:"100"`
    Email     string    `json:"email"      example:"jane@example.com" format:"email"`
    Role      string    `json:"role"       example:"admin"       enums:"admin,user"`
    CreatedAt time.Time `json:"created_at" example:"2024-01-15T10:30:00Z" format:"date-time"`
    UpdatedAt time.Time `json:"updated_at" example:"2024-01-15T10:30:00Z" format:"date-time"`

    PasswordHash string `json:"-" swaggerignore:"true"`
}

// CreateUserRequest is the payload for POST /users.
type CreateUserRequest struct {
    Name     string `json:"name"     example:"Jane Doe"        binding:"required,min=2,max=100"`
    Email    string `json:"email"    example:"jane@example.com" binding:"required,email"`
    Password string `json:"password" example:"s3cur3P@ss!"      binding:"required,min=8"`
    Role     string `json:"role"     example:"user"             binding:"omitempty,oneof=admin user" enums:"admin,user"`
}

// ErrorResponse is the standard API error envelope.
type ErrorResponse struct {
    Error string `json:"error" example:"resource not found"`
}
```

**Key struct tags for swag:**

| Tag | Purpose | Example |
|-----|---------|---------|
| `example:"..."` | Sample value in Swagger UI | `example:"jane@example.com"` |
| `format:"..."` | OpenAPI format | `format:"uuid"`, `format:"email"`, `format:"date-time"` |
| `enums:"a,b"` | Allowed values | `enums:"admin,user"` |
| `swaggerignore:"true"` | Exclude field from docs | Hide `PasswordHash` |
| `swaggertype:"string"` | Override inferred type | For `time.Time`, `sql.NullInt64` |
| `minimum:` / `maximum:` | Numeric bounds | `minimum:"1" maximum:"100"` |
| `minLength:` / `maxLength:` | String length bounds | `minLength:"2" maxLength:"100"` |
| `default:"..."` | Default value | `default:"20"` |

## Generating Docs

```bash
# Standard cmd/ layout
swag init -g cmd/api/main.go -d ./,./internal/handler,./internal/domain

# Format annotations first (recommended)
swag fmt && swag init -g cmd/api/main.go

# Parse types from internal/ packages
swag init -g cmd/api/main.go --parseInternal

# Output: docs/docs.go, docs/swagger.json, docs/swagger.yaml
```

**Commit the generated `docs/` directory.** Re-run `swag init` after every handler or model change.

## Makefile Integration

```makefile
.PHONY: docs docs-check

docs:
	swag fmt
	swag init -g cmd/api/main.go -d ./,./internal/... --exclude ./vendor

docs-check:
	swag init -g cmd/api/main.go -d ./,./internal/... --exclude ./vendor
	git diff --exit-code docs/
```

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `swag` CLI not found | Add `$(go env GOPATH)/bin` to `$PATH` |
| Docs not updating | Re-run `swag init` — no watch mode |
| Blank import `_ "myapp/docs"` missing | Without it, spec is never registered — Swagger UI shows empty |
| `@Router` uses `:id` instead of `{id}` | Use `{id}` in annotations (OpenAPI), `:id` in Gin routes |
| `@Security` name mismatch | Must match `@securityDefinitions.apikey` name exactly |
| `time.Time` rendered as object | Add `swaggertype:"string" format:"date-time"` on field |
| Type not found during parsing | Add `--parseInternal` or `--parseDependency` flag |
| `map[string]interface{}` in response | Replace with a named struct |
| `internal_` prefix on model names | Known bug with `--parseInternal` — use `--useStructName` |

## Excluding Swagger from Production Binary

Use build tags to strip Swagger UI from production builds entirely:

```go
// file: swagger.go
//go:build swagger

package main

import (
    _ "myapp/docs"
    ginSwagger   "github.com/swaggo/gin-swagger"
    swaggerFiles "github.com/swaggo/files"
    "github.com/gin-gonic/gin"
)

func registerSwagger(r *gin.Engine) {
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
}
```

```go
// file: swagger_noop.go
//go:build !swagger

package main

import "github.com/gin-gonic/gin"

func registerSwagger(r *gin.Engine) {} // no-op in production
```

Build with `go build -tags swagger .` for dev/staging, `go build .` for production.

## Reference Files

Load these when you need deeper detail:

- **[references/annotations.md](references/annotations.md)** — Complete annotation reference: all @Param types, file uploads, response headers, enum from constants, model renaming, grouped responses, multiple auth schemes
- **[references/ci-cd.md](references/ci-cd.md)** — GitHub Actions workflow, PR validation, pre-commit hooks, OpenAPI 3.0 conversion, multiple swagger instances, swag init flags reference

## Cross-Skill References

- For handler patterns (ShouldBindJSON, route groups, error handling): see the **golang-gin-api** skill
- For JWT middleware and `@securityDefinitions.apikey BearerAuth`: see the **golang-gin-auth** skill
- For testing annotated handlers: see the **golang-gin-testing** skill
- For adding `swag init` to Docker builds: see the **golang-gin-deploy** skill

## Official Docs

If this skill doesn't cover your use case, consult the [swag GitHub](https://github.com/swaggo/swag), [gin-swagger GoDoc](https://pkg.go.dev/github.com/swaggo/gin-swagger), or [Swagger 2.0 spec](https://swagger.io/specification/v2/).
