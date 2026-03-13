---
name: go-chi-handler
description: Generate Chi HTTP handlers, use case orchestration, Use for REST endpoint handlers or web http handlers.
---

# Go Chi Handler

Generate Chi HTTP handler implementations for a Go backend.

## When to Use

- Create HTTP endpoint handlers for REST operations
- List, Create, Update, Delete, Get handlers
- Request/response DTO mapping with use case orchestration
- Swagger-annotated endpoints

## Handler Structure

**Location**: `internal/modules/<module>/http/chi/handler/<resource>_handler.go`

```go
package handler

import (
	"net/http"
	"fmt"
	"strconv"
	"strings"

	brickserrs "github.com/cristiano-pacheco/bricks/pkg/errs"
	"github.com/cristiano-pacheco/bricks/pkg/http/request"
	"github.com/cristiano-pacheco/bricks/pkg/http/response"
	"github.com/cristiano-pacheco/bricks/pkg/logger"
	"github.com/cristiano-pacheco/bricks/pkg/ucdecorator"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/http/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/usecase"
	"github.com/go-chi/chi/v5"
)

type ResourceHandler struct {
	resourceCreateUseCase ucdecorator.UseCase[usecase.ResourceCreateInput, usecase.ResourceCreateOutput]
	resourceListUseCase   ucdecorator.UseCase[usecase.ResourceListInput, usecase.ResourceListOutput]
	resourceUpdateUseCase ucdecorator.UseCase[usecase.ResourceUpdateInput, usecase.ResourceUpdateOutput]
	resourceDeleteUseCase ucdecorator.UseCase[usecase.ResourceDeleteInput, usecase.ResourceDeleteOutput]
	resourceGetUseCase    ucdecorator.UseCase[usecase.ResourceGetInput, usecase.ResourceGetOutput]
	errorHandler          response.ErrorHandler
	logger                logger.Logger
}

func NewResourceHandler(
	resourceCreateUseCase ucdecorator.UseCase[usecase.ResourceCreateInput, usecase.ResourceCreateOutput],
	resourceListUseCase ucdecorator.UseCase[usecase.ResourceListInput, usecase.ResourceListOutput],
	resourceUpdateUseCase ucdecorator.UseCase[usecase.ResourceUpdateInput, usecase.ResourceUpdateOutput],
	resourceDeleteUseCase ucdecorator.UseCase[usecase.ResourceDeleteInput, usecase.ResourceDeleteOutput],
	resourceGetUseCase ucdecorator.UseCase[usecase.ResourceGetInput, usecase.ResourceGetOutput],
	errorHandler response.ErrorHandler,
	logger logger.Logger,
) *ResourceHandler {
	return &ResourceHandler{
		resourceCreateUseCase: resourceCreateUseCase,
		resourceListUseCase:   resourceListUseCase,
		resourceUpdateUseCase: resourceUpdateUseCase,
		resourceDeleteUseCase: resourceDeleteUseCase,
		resourceGetUseCase:    resourceGetUseCase,
		errorHandler:          errorHandler,
		logger:                logger,
	}
}
```

**Key points**:
- Use cases are always `ucdecorator.UseCase[Input, Output]` generic interface — never concrete `*usecase.ResourceUseCase` pointers
- Import `brickserrs` with alias: `brickserrs "github.com/cristiano-pacheco/bricks/pkg/errs"`
- Constructor returns pointer `*ResourceHandler`

## DTOs (Data Transfer Objects)

Request and response DTOs are defined in `internal/modules/<module>/http/dto/<resource>_dto.go`.

**Typical DTO structure**:

```go
package dto

type CreateResourceRequest struct {
	Field1 string `json:"field1"`
	Field2 int    `json:"field2"`
}

type CreateResourceResponse struct {
	ID     uint64 `json:"id"`
	Field1 string `json:"field1"`
	Field2 int    `json:"field2"`
}

type UpdateResourceRequest struct {
	Field1 string `json:"field1"`
	Field2 int    `json:"field2"`
}

type ResourceResponse struct {
	ID     uint64 `json:"id"`
	Field1 string `json:"field1"`
	Field2 int    `json:"field2"`
}
```

**Key points**:
- DTOs live in the HTTP transport layer, separate from use case inputs or models
- Use JSON tags for serialization
- Keep DTOs focused on HTTP contract, not domain logic

## Handler Method Patterns

All handler methods use the `Handle` prefix: `HandleListResources`, `HandleCreateResource`, etc.

### List (GET /resources)

```go
// @Summary		List resources
// @Description	Retrieves all resources
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Success		200	{object}	response.Envelope[[]dto.ResourceResponse]	"Successfully retrieved resources"
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
// @Router		/api/v1/resources [get]
func (h *ResourceHandler) HandleListResources(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	output, err := h.resourceListUseCase.Execute(ctx, usecase.ResourceListInput{})
	if err != nil {
		h.logger.Error("failed to list resources", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	resources := make([]dto.ResourceResponse, 0, len(output.Resources))
	for _, resource := range output.Resources {
		resources = append(resources, dto.ResourceResponse{
			ID:   resource.ID,
			Name: resource.Name,
			// ... map other fields
		})
	}

	if err = response.JSON(w, http.StatusOK, resources, http.Header{}); err != nil {
		h.logger.Error("failed to write list resources response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
}
```

### Create (POST /resources)

```go
// @Summary		Create resource
// @Description	Creates a new resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Param		request	body	dto.CreateResourceRequest	true	"Resource data"
// @Success		201	{object}	response.Envelope[dto.CreateResourceResponse]	"Successfully created resource"
// @Failure		422	{object}	brickserrs.Error	"Invalid request format or validation error"
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
// @Router		/api/v1/resources [post]
func (h *ResourceHandler) HandleCreateResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	var createRequest dto.CreateResourceRequest
	if err := request.ReadJSON(w, r, &createRequest); err != nil {
		h.logger.Error("failed to parse request body", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	output, err := h.resourceCreateUseCase.Execute(ctx, usecase.ResourceCreateInput{
		Name: createRequest.Name,
		// ... map other fields
	})
	if err != nil {
		h.logger.Error("failed to create resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	createResponse := dto.CreateResourceResponse{
		ID:   output.ID,
		Name: output.Name,
		// ... map other fields
	}

	if err = response.JSON(w, http.StatusCreated, createResponse, http.Header{}); err != nil {
		h.logger.Error("failed to write create resource response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
}
```

### Update (PUT /resources/:id)

```go
// @Summary		Update resource
// @Description	Updates an existing resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Param		id		path	int						true	"Resource ID"
// @Param		request	body	dto.UpdateResourceRequest	true	"Resource data"
// @Success		204		"Successfully updated resource"
// @Failure		422	{object}	brickserrs.Error	"Invalid request format or validation error"
// @Failure		404	{object}	brickserrs.Error	"Resource not found"
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [put]
func (h *ResourceHandler) HandleUpdateResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	id, err := h.parseUintPathParam(r, "id")
	if err != nil {
		h.logger.Error("invalid resource id", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	var updateRequest dto.UpdateResourceRequest
	if err = request.ReadJSON(w, r, &updateRequest); err != nil {
		h.logger.Error("failed to parse request body", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	if _, err = h.resourceUpdateUseCase.Execute(ctx, usecase.ResourceUpdateInput{
		ID:   id,
		Name: updateRequest.Name,
		// ... map other fields
	}); err != nil {
		h.logger.Error("failed to update resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	response.NoContent(w)
}
```

### Delete (DELETE /resources/:id)

```go
// @Summary		Delete resource
// @Description	Deletes an existing resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Param		id	path	int	true	"Resource ID"
// @Success		204		"Successfully deleted resource"
// @Failure		404	{object}	brickserrs.Error	"Resource not found"
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [delete]
func (h *ResourceHandler) HandleDeleteResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	id, err := h.parseUintPathParam(r, "id")
	if err != nil {
		h.logger.Error("invalid resource id", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	if _, err = h.resourceDeleteUseCase.Execute(ctx, usecase.ResourceDeleteInput{ID: id}); err != nil {
		h.logger.Error("failed to delete resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	response.NoContent(w)
}
```

### Get by ID (GET /resources/:id)

```go
// @Summary		Get resource
// @Description	Retrieves a resource by ID
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Param		id	path	int	true	"Resource ID"
// @Success		200	{object}	response.Envelope[dto.ResourceResponse]	"Successfully retrieved resource"
// @Failure		404	{object}	brickserrs.Error	"Resource not found"
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [get]
func (h *ResourceHandler) HandleGetResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	id, err := h.parseUintPathParam(r, "id")
	if err != nil {
		h.logger.Error("invalid resource id", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	output, err := h.resourceGetUseCase.Execute(ctx, usecase.ResourceGetInput{ID: id})
	if err != nil {
		h.logger.Error("failed to get resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	resourceResponse := dto.ResourceResponse{
		ID:   output.ID,
		Name: output.Name,
		// ... map other fields
	}

	if err = response.JSON(w, http.StatusOK, resourceResponse, http.Header{}); err != nil {
		h.logger.Error("failed to write get resource response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
}
```

### URL Param Helper (private method)

Handlers that parse path parameters should use a private method on the struct — not a standalone function:

```go
func (h *ResourceHandler) parseUintPathParam(r *http.Request, paramName string) (uint64, error) {
	value := strings.TrimSpace(chi.URLParam(r, paramName))
	if value == "" {
		return 0, h.newBadRequestError(fmt.Sprintf("missing path param %q", paramName))
	}

	parsed, err := strconv.ParseUint(value, 10, 64)
	if err != nil {
		return 0, h.newBadRequestError(fmt.Sprintf("invalid path param %q", paramName))
	}

	return parsed, nil
}

func (h *ResourceHandler) newBadRequestError(message string) *brickserrs.Error {
	return brickserrs.New("MODULE_90", message, http.StatusBadRequest, nil)
}
```

# Request/Response Mapping

Handler methods bridge HTTP requests/responses (DTOs from `internal/modules/<module>/http/dto`) with use case inputs/outputs.

### Request to Use Case Input

```go
// Decode request
var req dto.CreateResourceRequest

err := request.ReadJSON(w, r, &req)
if err != nil {
	h.logger.Error("failed to parse request body", logger.Error(err))
	h.errorHandler.Error(w, err)
	return
}

// Map to use case input
input := usecase.ResourceCreateInput{
	Field1: req.Field1,
	Field2: req.Field2,
}
```

### Use Case Output to Response

```go
// Execute use case
output, err := h.resourceCreateUseCase.Execute(ctx, input)
if err != nil {
	h.logger.Error("failed to create resource", logger.Error(err))
	h.errorHandler.Error(w, err)
	return
}

// Map to response DTO
response := dto.CreateResourceResponse{
	ID:     output.ID,
	Field1: output.Field1,
	Field2: output.Field2,
}
```

## Swagger Annotation Rules

1. **@Summary**: Brief action description (e.g., "List resources", "Create resource")
2. **@Description**: Full description of what the endpoint does
3. **@Tags**: Plural resource name (e.g., "Resources", "Contacts")
4. **@Accept**: Always `json`
5. **@Produce**: Always `json`
6. **@Security**: Add `BearerAuth` if authentication required
7. **@Param**: Define path params and request body
   - Path param: `@Param id path int true "Resource ID"`
   - Request body: `@Param request body dto.CreateResourceRequest true "Resource data"`
8. **@Success**: Status code with response type
   - 200: `{object} response.Envelope[dto.ResourceResponse]`
   - 201: `{object} response.Envelope[dto.CreateResourceResponse]`
   - 204: No content, just description string
9. **@Failure**: Common errors (404, 422, 500) with `{object} brickserrs.Error` (note the alias)
10. **@Router**: `/api/v1/resources/{id} [method]`

## Error Handling Pattern

Every error in every handler method must follow this exact pattern — no exceptions, including input validation and URL param parse errors:

```go
if err != nil {
	h.logger.Error("descriptive error message", logger.Error(err))
	h.errorHandler.Error(w, err)
	return
}
```

Standard error messages:
- `"failed to parse request body"` — JSON decode error
- `"invalid resource id"` — URL param parsing error
- `"failed to list resources"` — List use case error
- `"failed to create resource"` — Create use case error
- `"failed to update resource"` — Update use case error
- `"failed to delete resource"` — Delete use case error
- `"failed to get resource"` — Get use case error
- `"failed to write list resources response"` — JSON response write error (include the operation name)

## Fx Wiring

**Add to `internal/modules/<module>/fx.go`**:

```go
fx.Provide(handler.NewResourceHandler),
```

The handler is typically provided to the router, not exposed as a port.

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, never add package-level standalone functions. All helpers must be private methods on the struct (e.g., `parseUintPathParam`, `newBadRequestError`).
2. **Struct**: Include all use cases, `response.ErrorHandler`, and `logger.Logger`
3. **Constructor**: Must return pointer `*ResourceHandler`
4. **Context**: Always get from request: `ctx := r.Context()`
5. **Request decoding**: Use `request.ReadJSON(w, r, &dto)` — declare variable first, then call ReadJSON
6. **URL params**: Parse via a private `parseUintPathParam` method using `chi.URLParam` + `strconv.ParseUint`
7. **Error handling**: Always call `h.logger.Error(...)` AND `h.errorHandler.Error(w, err)` then return — for ALL errors, including validation/input parse errors
8. **Response mapping**: Map use case output to DTO; never return use case outputs directly
9. **Success responses**:
   - List/Get: `response.JSON(w, http.StatusOK, data, http.Header{})`
   - Create: `response.JSON(w, http.StatusCreated, data, http.Header{})`
   - Update/Delete: `response.NoContent(w)`
10. **Swagger**: Must add complete swagger annotations for every handler method; use `brickserrs.Error` (not `errs.Error`) in `@Failure` lines
11. **No comments**: Do not add redundant comments inside method bodies
12. **Validation**: Run `make lint` and `make update-swagger` after generation

## Anti-Patterns (NEVER DO)

These patterns have appeared in the codebase and must not be repeated:

### ❌ Raw `w.WriteHeader` instead of `response.NoContent`

```go
// BAD
w.WriteHeader(http.StatusNoContent)

// GOOD
response.NoContent(w)
```

### ❌ Standalone package-level functions in handler files

```go
// BAD — standalone functions at package level violate the no-standalone-functions rule
func isResourceEmpty(output usecase.ResourceGetOutput) bool {
    return output.Name == ""
}

func firstNonEmpty(values ...string) string { ... }

// GOOD — private methods on the handler struct
func (h *ResourceHandler) isResourceEmpty(output usecase.ResourceGetOutput) bool {
    return output.Name == ""
}

func (h *ResourceHandler) firstNonEmpty(values ...string) string { ... }
```

### ❌ Missing logger call before errorHandler for validation/parse errors

```go
// BAD — skips the logger
if parseErr != nil {
    h.errorHandler.Error(w, brickserrs.New("MODULE_90", "invalid id", http.StatusBadRequest, nil))
    return
}

// GOOD — always log before handling
if parseErr != nil {
    h.logger.Error("invalid resource id", logger.Error(parseErr))
    h.errorHandler.Error(w, parseErr)
    return
}
```

### ❌ Inline `brickserrs.New()` with hardcoded error codes in handler bodies

Errors must be defined in the module's `errs/` package (use the `go-error` skill), not created ad-hoc inside handler method bodies.

```go
// BAD — hardcoded error codes inline in handler logic
h.errorHandler.Error(w, brickserrs.New("CATALOG_90", "invalid category_id", http.StatusBadRequest, nil))

// GOOD — reference a named error from the module's errs/ package
h.errorHandler.Error(w, errs.ErrInvalidCategoryID)
```

The exception is the `newBadRequestError` private method used for URL param parsing — that is the one acceptable place for inline construction, scoped to a helper method on the struct.

### ❌ Concrete use case types in struct fields and constructor

```go
// BAD — concrete pointer types
type ResourceHandler struct {
    resourceCreateUseCase *usecase.ResourceCreateUseCase
}

// GOOD — generic ucdecorator interface
type ResourceHandler struct {
    resourceCreateUseCase ucdecorator.UseCase[usecase.ResourceCreateInput, usecase.ResourceCreateOutput]
}
```

### ❌ Handler method names without `Handle` prefix

```go
// BAD
func (h *ResourceHandler) ListResources(w http.ResponseWriter, r *http.Request) { ... }
func (h *ResourceHandler) CreateResource(w http.ResponseWriter, r *http.Request) { ... }

// GOOD
func (h *ResourceHandler) HandleListResources(w http.ResponseWriter, r *http.Request) { ... }
func (h *ResourceHandler) HandleCreateResource(w http.ResponseWriter, r *http.Request) { ... }
```

### ❌ Wrong error type in swagger `@Failure` annotations

```go
// BAD — errs.Error is not the correct reference
// @Failure		500	{object}	errs.Error	"Internal server error"

// GOOD — use the brickserrs alias
// @Failure		500	{object}	brickserrs.Error	"Internal server error"
```

## Workflow

1. Create handler struct with use case dependencies (using `ucdecorator.UseCase[Input, Output]`)
2. Implement constructor `NewResourceHandler`
3. Implement handler methods with `Handle` prefix following patterns above
4. Add private `parseUintPathParam` + `newBadRequestError` methods if path params are needed
5. Add swagger annotations to all methods (using `brickserrs.Error` in `@Failure`)
6. Add Fx wiring to module's `fx.go`
7. Run `make lint` and `make nilaway` to verify static tests
8. Run `make update-swagger` to regenerate swagger docs
