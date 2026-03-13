---
name: go-service
description: Generate services. Use for reusable single-responsibility business services or domain services.
---

# Go Service

Generate service files for GO modular architecture conventions.

## When to Use

- Create reusable business services for a module
- Email senders, token generators, password hashers
- Template compilers, cache-backed lookups
- Any single-responsibility domain service consumed by use cases or other services.

## Three-File Pattern

Every service requires up to three files:

1. **DTO structs** (if needed): `internal/modules/<module>/dto/<service_name>_dto.go`
2. **Port interface**: `internal/modules/<module>/ports/<service_name>_service.go`
3. **Service implementation**: `internal/modules/<module>/service/<service_name>_service.go`

### DTO File Layout Order

1. Input/output structs

### Port File Layout Order

1. Interface definition (`XxxService` — no suffix)

### Service File Layout Order

1. Implementation struct (`XxxService`)
2. Compile-time interface assertion
3. Constructor (`NewXxxService`)
4. Methods

## DTO Structure

**Location**: `internal/modules/<module>/dto/<service_name>_dto.go`

```go
package dto

type DoSomethingInput struct {
	Field string
}
```

## Port Interface Structure

**Location**: `internal/modules/<module>/ports/<service_name>_service.go`

```go
package ports

import (
	"context"

	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/dto"
)

// DoSomethingService <describe what this service does and when to use it>.
type DoSomethingService interface {
	Execute(ctx context.Context, input dto.DoSomethingInput) error
}
```

## Service Implementation Structure

**Location**: `internal/modules/<module>/service/<service_name>_service.go`

```go
package service

import (
	"context"

	"github.com/cristiano-pacheco/bricks/pkg/logger"
	"github.com/cristiano-pacheco/bricks/pkg/otel/trace"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
)

type DoSomethingService struct {
	logger logger.Logger
	// other dependencies
}

var _ ports.DoSomethingService = (*DoSomethingService)(nil)

func NewDoSomethingService(
	logger logger.Logger,
) *DoSomethingService {
	return &DoSomethingService{
		logger: logger,
	}
}

func (s *DoSomethingService) Execute(ctx context.Context, input dto.DoSomethingInput) error {
	ctx, span := trace.Span(ctx, "DoSomethingService.Execute")
	defer span.End()

	// Business logic here
	// if err != nil {
	// 	s.logger.Error("DoSomethingService.Execute failed", logger.Error(err))
	// 	return err
	// }

	return nil
}
```

## Service Variants

### Single-action service (Execute pattern)

Use `Execute` method with a dedicated input struct when the service does one thing.

DTO (`dto/send_email_confirmation_dto.go`):

```go
type SendEmailConfirmationInput struct {
	UserModel             model.UserModel
	ConfirmationTokenHash []byte
}
```

Port (`ports/send_email_confirmation_service.go`):

```go
type SendEmailConfirmationService interface {
	Execute(ctx context.Context, input dto.SendEmailConfirmationInput) error
}
```

### Multi-method service (named methods)

Use descriptive method names when the service groups related operations.

Port (`ports/hash_service.go`):

```go
type HashService interface {
	GenerateFromPassword(password []byte) ([]byte, error)
	CompareHashAndPassword(hashedPassword, password []byte) error
	GenerateRandomBytes() ([]byte, error)
}
```

### Stateless service (no dependencies)

Omit logger and config when the service is a pure utility with no I/O.

```go
type HashService struct{}

func NewHashService() *HashService {
	return &HashService{}
}
```

## Tracing

Services performing I/O MUST use `trace.Span`. Pure utilities (hashing, template compilation) skip tracing.

```go
ctx, span := trace.Span(ctx, "ServiceName.MethodName")
defer span.End()
```

Span name format: `"StructName.MethodName"`

## Naming

- Port interface: `XxxService` (in `ports` package, no suffix)
- Implementation struct: `XxxService` (in `service` package, same name — disambiguated by package)
- Constructor: `NewXxxService`, returns a pointer of the struct implementation

## Logger Parameter Naming

Always name the logger parameter `logger` in constructors — never `l` or `log`:

```go
// Correct
func NewDoSomethingService(logger logger.Logger) *DoSomethingService {
	return &DoSomethingService{logger: logger}
}

// Wrong — never use 'l' or 'log' as the parameter name
func NewDoSomethingService(l logger.Logger) *DoSomethingService { ... }
func NewDoSomethingService(log logger.Logger) *DoSomethingService { ... }
```

## Fx Wiring

Add to `internal/modules/<module>/fx.go`:

```go
fx.Provide(
	fx.Annotate(
		service.NewXxxService,
		fx.As(new(ports.XxxService)),
	),
),
```

## Dependencies

Services depend on interfaces only. Common dependencies:

- `logger.Logger` — structured logging
- Other `ports.XxxService` interfaces — compose services
- `ports.XxxRepository` — data access
- `ports.XxxCache` — caching layer

## Error Logging Rule

- Always use the Bricks logger package: `github.com/cristiano-pacheco/bricks/pkg/logger`
- Every time a service method returns an error, log it immediately before returning
- Any service that can return an error MUST have a `logger logger.Logger` field
- **Canonical pattern** — always use `s.logger.Error` with `logger.Error(err)` as a field:

```go
if err != nil {
	s.logger.Error("ServiceName.MethodName failed", logger.Error(err))
	return err
}
```

- **Forbidden** — never use `WithError`:

```go
// Wrong — never use this form
s.logger.WithError(err).Error("message")
```

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, ALL helper logic must be private methods on the struct — never standalone package-level functions. This applies even to tiny utilities. See [Anti-pattern: Standalone functions](#anti-pattern-standalone-functions).
2. **No duplicate helpers across files**: Within the same `service` package, never define two standalone functions (or private methods on different structs) that do the same thing under different names. If two services need the same utility, each should have its own private method with the same name on their respective structs.
3. **Three files**: DTOs in `dto/`, port interface in `ports/`, implementation in `service/`
4. **Interface in ports**: Interface lives in `ports/<name>_service.go`
5. **DTOs in dto**: Input/output structs live in `dto/<name>_dto.go`
6. **Interface assertion**: Add `var _ ports.XxxService = (*XxxService)(nil)` below the struct
7. **Constructor returns pointer**: Normal constructor returns `*XxxService`. The only exception is when initialization requires fallible I/O (e.g., parsing a key, creating a directory, connecting to a resource at startup) — then return `(*XxxService, error)`.
8. **Tracing**: Every I/O method MUST use `trace.Span` with `defer span.End()`
9. **Context**: Methods performing I/O accept `context.Context` as first parameter
10. **No comments on implementations**: Do not add comments above the struct type, the constructor, or any method (public or private) in implementation files. Comments belong only on port interfaces.
11. **Add detailed comment on interfaces**: Provide comprehensive comments on the port interfaces to describe their purpose and usage
12. **Dependencies**: Always depend on port interfaces, never concrete implementations
13. **Error logging**: Every returned error must be logged first using `s.logger.Error(..., logger.Error(err))` — never `WithError`
14. **Logger field required**: Any service that can return an error must have a `logger logger.Logger` field and use it before returning errors

## Anti-pattern: Standalone functions

Standalone functions at the package level are forbidden when a struct with methods exists in the file. They pollute the package namespace, can collide with helpers in other service files, and fragment logic that belongs to the struct.

**Wrong** — standalone helper alongside struct methods:

```go
type SlugService struct{}

func (s *SlugService) Generate(_ context.Context, name string) string {
	return normalizeWithoutDiacritics(strings.ToLower(name)) // calls standalone fn
}

// Wrong: this is a standalone function, not a method
func normalizeWithoutDiacritics(input string) string {
	// ...
}
```

**Correct** — private method on the struct:

```go
type SlugService struct{}

func (s *SlugService) Generate(_ context.Context, name string) string {
	return s.normalizeWithoutDiacritics(strings.ToLower(name)) // calls private method
}

func (s *SlugService) normalizeWithoutDiacritics(input string) string {
	// ...
}
```

This rule applies to ALL helpers — string utilities, crypto helpers, normalizers, formatters — regardless of how small or "pure" they are.

## Workflow

1. Create DTO file in `dto/<name>_dto.go` (if input/output structs are needed)
2. Create port interface in `ports/<name>_service.go`
3. Create service implementation in `service/<name>_service.go`
4. Add Fx wiring to module's `fx.go`
5. Run `make lint` to verify
6. Run `make nilaway` for static analysis
