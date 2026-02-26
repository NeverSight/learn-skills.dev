---
name: go-service
description: Generate Go services following GO modular architecture conventions (Fx DI, OTEL tracing, interface-first design). Use when creating reusable business services in internal/modules/<module>/service/ - email senders, token generators, hashing utilities, template compilers, cache-backed lookups, or any domain service that encapsulates a single responsibility and is consumed by use cases or other services.
---

# Go Service

Generate service files for GO modular architecture conventions.

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
- Preferred pattern:

```go
if err != nil {
	s.logger.Error("ServiceName.MethodName failed", logger.Error(err))
	return err
}
```

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Three files**: DTOs in `dto/`, port interface in `ports/`, implementation in `service/`
2. **Interface in ports**: Interface lives in `ports/<name>_service.go`
3. **DTOs in dto**: Input/output structs live in `dto/<name>_dto.go`
4. **Interface assertion**: Add `var _ ports.XxxService = (*XxxService)(nil)` below the struct
5. **Constructor**: MUST return pointer `*XxxService`
6. **Tracing**: Every I/O method MUST use `trace.Span` with `defer span.End()`
7. **Context**: Methods performing I/O accept `context.Context` as first parameter
8. **No comments on implementations**: Do not add redundant comments above methods in the implementations
9. **Add detailed comment on interfaces**: Provide comprehensive comments on the port interfaces to describe their purpose and usage
10. **Dependencies**: Always depend on port interfaces, never concrete implementations
11. **Error logging**: Every returned error must be logged first using Bricks logger (`s.logger.Error(..., logger.Error(err))`)

## Workflow

1. Create DTO file in `dto/<name>_dto.go` (if input/output structs are needed)
2. Create port interface in `ports/<name>_service.go`
3. Create service implementation in `service/<name>_service.go`
4. Add Fx wiring to module's `fx.go`
5. Run `make lint` to verify
6. Run `make nilaway` for static analysis
