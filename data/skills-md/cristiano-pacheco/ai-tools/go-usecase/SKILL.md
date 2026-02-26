---
name: go-usecase
description: Generate Go use cases for modular architecture using ports-based dependencies and decorator-based observability. Use when implementing business actions in internal/modules/<module>/usecase/ such as create, update, list, delete, status transitions, uploads, notifications, or any domain operation that orchestrates repositories/services.
---

# Go UseCase

Generate a use case that depends on ports (interfaces), not concrete implementations.

## Create the file

Create one file per operation in:
`internal/modules/<module>/usecase/<operation>_usecase.go`

Use:
- package: `usecase`
- struct name: `<Operation>UseCase`
- method name: `Execute`

## Naming (CRITICAL)

Apply consistent naming for every use case.

Rules:
- file: `<operation>_usecase.go`
- input DTO: `<Operation>Input`
- output DTO: `<Operation>Output`
- use case struct: `<Operation>UseCase`
- constructor: `New<Operation>UseCase`

Example (`contact_create`):
- file: `contact_create_usecase.go`
- input: `ContactCreateInput`
- output: `ContactCreateOutput`
- struct: `ContactCreateUseCase`
- constructor: `NewContactCreateUseCase`

Example (`contact_list`, no real input):
- file: `contact_list_usecase.go`
- input: `ContactListInput` (empty struct)
- output: `ContactListOutput`
- struct: `ContactListUseCase`
- constructor: `NewContactListUseCase`

## Follow the structure (CRITICAL)

Implement this order in the file:
1. Input struct (ALWAYS present; can be empty)
2. Output struct (ALWAYS present; can be empty)
3. Use case struct with dependencies
4. Constructor `New<Operation>UseCase`
5. Public `Execute` method (contains all business logic)

## Current architecture rule

Use cases contain business logic only.

Do NOT include in usecases:
- logger dependencies
- metrics dependencies
- tracing code
- private `execute` method wrappers

Observability and error translation are handled by `ucdecorator` in Fx wiring.

## Use this template

```go
package usecase

import (
	"context"

	"github.com/cristiano-pacheco/bricks/pkg/validator"
	"github.com/cristiano-pacheco/catzi/internal/modules/<module>/ports"
)

type <Operation>Input struct {
	Field string `validate:"required,max=255"`
}

type <Operation>Output struct {
	Result string
}

type <Operation>UseCase struct {
	repo      ports.<Entity>Repository
	validator validator.Validator // include only if needed
}

func New<Operation>UseCase(
	repo ports.<Entity>Repository,
	validator validator.Validator,
) *<Operation>UseCase {
	return &<Operation>UseCase{
		repo:      repo,
		validator: validator,
	}
}

func (uc *<Operation>UseCase) Execute(ctx context.Context, input <Operation>Input) (<Operation>Output, error) {
	if err := uc.validator.Validate(input); err != nil {
		return <Operation>Output{}, err
	}

	// Add business orchestration here
	// - read/write via repositories
	// - call domain services
	// - map model to output DTO

	return <Operation>Output{}, nil
}
```

## Apply variants

### No-input use case

When no parameters are needed, still define an empty input:

```go
type ContactListInput struct{}
```

And keep the same contract:

```go
func (uc *ContactListUseCase) Execute(ctx context.Context, input ContactListInput) (ContactListOutput, error)
```

### No-output use case

When no result payload is needed, define an empty output:

```go
type ContactDeleteOutput struct{}
```

And return it:

```go
return ContactDeleteOutput{}, nil
```

### No-validation use case

When validation is not required, remove `validator.Validator` from dependencies and skip validation.

### Multi-dependency orchestration

Inject multiple ports as interfaces (repositories, caches, services) in the use case struct and constructor.

## Apply common patterns

### Check existing record before create

```go
import brickserrors "github.com/cristiano-pacheco/bricks/pkg/errs"

record, err := uc.repo.FindByX(ctx, input.Field)
if err != nil && !errors.Is(err, brickserrors.ErrRecordNotFound) {
	return <Operation>Output{}, err
}
if record.ID != 0 {
	return <Operation>Output{}, brickserrors.ErrAlreadyExists
}
```

### Convert enum from input

```go
enumVal, err := enum.NewTypeEnum(input.Type)
if err != nil {
	return <Operation>Output{}, err
}
// Assign to your model field
```

### Map list response

```go
items, err := uc.repo.FindAll(ctx)
if err != nil {
	return <Operation>Output{}, err
}

output := <Operation>Output{
	Items: make([]ItemOutput, len(items)),
}
for i, item := range items {
	output.Items[i] = ItemOutput{ID: item.ID, Name: item.Name}
}
return output, nil
```

## Wire with Fx

Register raw usecases and decorate them via `ucdecorator`.

### Minimal provider example

```go
fx.Provide(
	usecase.New<Operation>UseCase,
)
```

### Decorator wiring pattern (recommended)

Use a consolidated provider (`fx.In` + `fx.Out`) and wrap usecases with:

```go
ucdecorator.Wrap(factory, rawUseCase)
```

`Wrap` infers:
- usecase name (e.g. `CategoryCreateUseCase.Execute`)
- metric name (e.g. `category_create`)

No need to pass metric/usecase name strings manually.

### Full module wiring pattern (single-file, `fx.In` + `fx.Out`)

Use this when the module has multiple usecases and you want less boilerplate in `fx.go`.

```go
type decorateIn struct {
	fx.In

	Factory *ucdecorator.Factory
	Create  *usecase.<Entity>CreateUseCase
	List    *usecase.<Entity>ListUseCase
}

type decorateOut struct {
	fx.Out

	Create ucdecorator.UseCase[usecase.<Entity>CreateInput, usecase.<Entity>CreateOutput]
	List   ucdecorator.UseCase[usecase.<Entity>ListInput, usecase.<Entity>ListOutput]
}

func provideDecoratedUseCases(in decorateIn) decorateOut {
	return decorateOut{
		Create: ucdecorator.Wrap(in.Factory, in.Create),
		List:   ucdecorator.Wrap(in.Factory, in.List),
	}
}

var Module = fx.Module(
	"<module>",
	fx.Provide(
		// repositories/services/validators
		// raw usecases
		usecase.New<Entity>CreateUseCase,
		usecase.New<Entity>ListUseCase,

		// decorated usecases
		provideDecoratedUseCases,

		// handlers/routers
	),
)
```

This keeps:
1. Raw constructors simple
2. Decoration centralized in one provider
3. Handler injection strongly typed via `ucdecorator.UseCase[Input, Output]`

## Enforce rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. Depend only on `ports.*` interfaces in use cases.
2. Keep orchestration in use case; keep persistence in repositories.
3. Use a single public `Execute` method; do not create a private `execute` wrapper.
4. Always define both Input and Output structs (use empty struct when needed).
5. Input and Output must NOT contain `json` tags; use validation tags on Input only when needed.
6. Keep naming consistent across file, structs, constructor, and method.
7. Return typed output DTOs; do not leak persistence models directly.
8. Keep observability and translation outside usecases (via decorators).

## Final checklist

1. Create `internal/modules/<module>/usecase/<operation>_usecase.go`.
2. Add Input/Output DTOs for the operation (including empty structs when needed).
3. Inject required ports/services in constructor.
4. Implement a single `Execute` with all business logic.
5. Wire raw usecase in Fx and decorate with `ucdecorator.Wrap(factory, raw)`.
6. Create unit tests using the `go-unit-tests` skill.
7. Run `make test`.
8. Run `make lint`.
9. Run `make nilaway`.
