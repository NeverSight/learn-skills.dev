---
name: go-mapper
description: Generate pure mapper functions for transformations between layers, HTTP DTOs to use case inputs dtos, use case to response dto, etc.
---

# Go Mapper

Generate pure mapper functions for GO modular architecture.

## When to Use

- Map HTTP request DTOs to use case inputs
- Map persistence models to HTTP response DTOs
- Map between any two struct representations across layers
- Convert a slice of structs to a slice of another struct
- Any struct-to-struct transformation that lives in a module

## Location

All mapper files live in `internal/modules/<module>/mapper/`.

One file per domain concept: `<name>_mapper.go` (e.g., `user_mapper.go`).

## Function Signature Pattern

Every mapper function follows the `To` prefix convention. It accepts one or more inputs and returns exactly one output, optionally with an error.

```
func ToXxx(input InputType) OutputType
func ToXxx(input InputType) (OutputType, error)
func ToXxx(a TypeA, b TypeB) OutputType
```

Single output only. Error is the only allowed second return value.

## File Structure

1. Package declaration and imports
2. Public mapper functions
3. Private helper functions (shared logic between public functions)

## Examples

### Basic mapper

```go
package mapper

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/user/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/user/model"
	"github.com/cristiano-pacheco/pingo/internal/modules/user/usecase"
)

func ToCreateUserInput(req dto.CreateUserRequest) usecase.CreateUserInput {
	return usecase.CreateUserInput{
		Name:  req.Name,
		Email: req.Email,
	}
}

func ToUserResponse(u model.UserModel) dto.UserResponse {
	return dto.UserResponse{
		ID:        u.ID,
		Name:      u.Name,
		Email:     u.Email,
		CreatedAt: u.CreatedAt,
	}
}

func ToUserListResponse(models []model.UserModel) []dto.UserResponse {
	responses := make([]dto.UserResponse, len(models))
	for i, u := range models {
		responses[i] = ToUserResponse(u)
	}
	return responses
}
```

### Mapper with multiple inputs

```go
package mapper

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/order/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/order/model"
)

func ToOrderResponse(order model.OrderModel, items []model.OrderItemModel) dto.OrderResponse {
	return dto.OrderResponse{
		ID:    order.ID,
		Total: order.Total,
		Items: toOrderItemResponses(items),
	}
}

func toOrderItemResponses(items []model.OrderItemModel) []dto.OrderItemResponse {
	responses := make([]dto.OrderItemResponse, len(items))
	for i, item := range items {
		responses[i] = dto.OrderItemResponse{
			ID:       item.ID,
			Name:     item.ProductName,
			Quantity: item.Quantity,
			Price:    item.Price,
		}
	}
	return responses
}
```

### Mapper with error return

Use when transformation can fail (e.g., parsing, validation during mapping).

```go
package mapper

import (
	"github.com/cristiano-pacheco/pingo/internal/modules/product/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/product/errs"
	"github.com/cristiano-pacheco/pingo/internal/modules/product/model"
)

func ToProductModel(req dto.CreateProductRequest) (model.ProductModel, error) {
	price, err := parsePrice(req.Price)
	if err != nil {
		return model.ProductModel{}, errs.ErrInvalidPrice
	}
	return model.ProductModel{
		Name:  req.Name,
		Price: price,
	}, nil
}
```

### Slice mapper pattern

When mapping a single item, add a corresponding list function if the type appears in collections.

```go
func ToArticleResponse(a model.ArticleModel) dto.ArticleResponse {
	return dto.ArticleResponse{
		ID:     a.ID,
		Title:  a.Title,
		Author: toAuthorResponse(a),
	}
}

func ToArticleListResponse(models []model.ArticleModel) []dto.ArticleResponse {
	responses := make([]dto.ArticleResponse, len(models))
	for i, a := range models {
		responses[i] = ToArticleResponse(a)
	}
	return responses
}

func toAuthorResponse(a model.ArticleModel) dto.AuthorResponse {
	return dto.AuthorResponse{
		ID:   a.AuthorID,
		Name: a.AuthorName,
	}
}
```

## Naming

- File: `<name>_mapper.go` in `mapper/` package
- Public functions: `ToXxx` — where `Xxx` is the output type name (e.g., `ToUserResponse`, `ToCreateUserInput`)
- Private helpers: `toXxx` — lowercase prefix for shared sub-mapping logic
- Slice variants: `ToXxxList` or `ToXxxListResponse`

## Rules

1. **Functions only** — no structs, no interfaces, no constructors, no port files
2. **`To` prefix** — every public function starts with `To`
3. **Single output** — one return value, or one return value + error
4. **No `context.Context`** — mappers are pure transformations, no I/O
5. **No side effects** — no logging, no database calls, no external dependencies
6. **Private helpers** — extract shared sub-mapping logic into private functions
7. **No comments on functions** — function names are self-documenting via the `To` convention
8. **Slice helpers** — add a list variant when the mapped type appears in collections
9. **Error return only when transformation can fail** — prefer no-error signatures; use error only for parsing or conversion failures

## Workflow

1. Create mapper file in `mapper/<name>_mapper.go`
2. Run `make lint` to verify code quality
3. Run `make nilaway` for static analysis
