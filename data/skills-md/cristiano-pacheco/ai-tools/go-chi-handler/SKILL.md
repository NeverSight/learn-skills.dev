---
name: go-chi-handler
description: Generate Chi HTTP handlers following Go modular architecture conventions (request/response DTOs, use case orchestration, error handling, swagger annotations, Fx DI). Use when creating HTTP endpoint handlers in internal/modules/<module>/http/chi/handler/ for REST operations (List, Create, Update, Delete, Get) that need to decode requests, call use cases, map responses, and handle errors with proper logging and tracing.
---

# Go Chi Handler

Generate Chi HTTP handler implementations for a Go backend.

## Handler Structure

**Location**: `internal/modules/<module>/http/chi/handler/<resource>_handler.go`

```go
package handler

import (
	"net/http"
	"strconv"

	"github.com/cristiano-pacheco/bricks/pkg/http/request"
	"github.com/cristiano-pacheco/bricks/pkg/http/response"
	"github.com/cristiano-pacheco/bricks/pkg/logger"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/http/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/usecase"
	"github.com/go-chi/chi/v5"
)

type ResourceHandler struct {
	resourceCreateUseCase *usecase.ResourceCreateUseCase
	resourceListUseCase   *usecase.ResourceListUseCase
	resourceUpdateUseCase *usecase.ResourceUpdateUseCase
	resourceDeleteUseCase *usecase.ResourceDeleteUseCase
	errorHandler          response.ErrorHandler
	logger                logger.Logger
}

func NewResourceHandler(
	resourceCreateUseCase *usecase.ResourceCreateUseCase,
	resourceListUseCase   *usecase.ResourceListUseCase,
	resourceUpdateUseCase *usecase.ResourceUpdateUseCase,
	resourceDeleteUseCase *usecase.ResourceDeleteUseCase,
	errorHandler response.ErrorHandler,
	logger logger.Logger,
) *ResourceHandler {
	return &ResourceHandler{
		resourceCreateUseCase: resourceCreateUseCase,
		resourceListUseCase:   resourceListUseCase,
		resourceUpdateUseCase: resourceUpdateUseCase,
		resourceDeleteUseCase: resourceDeleteUseCase,
		errorHandler:          errorHandler,
		logger:                logger,
	}
}
```

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

### List (GET /resource)

```go
// @Summary		List resources
// @Description	Retrieves all resources
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Security 	BearerAuth
// @Success		200	{object}	response.Envelope[[]dto.ResourceResponse]	"Successfully retrieved resources"
// @Failure		401	{object}	errs.Error	"Invalid credentials"
// @Failure		500	{object}	errs.Error	"Internal server error"
// @Router		/api/v1/resources [get]
func (h *ResourceHandler) ListResources(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	output, err := h.resourceListUseCase.Execute(ctx)
	if err != nil {
		h.logger.Error("failed to list resources", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	resources := make([]dto.ResourceResponse, len(output.Resources))
	for i, resource := range output.Resources {
		resources[i] = dto.ResourceResponse{
			ID:   resource.ID,
			Name: resource.Name,
			// ... map other fields
		}
	}

	err = response.JSON(w, http.StatusOK, resources, http.Header{})
	if err != nil {
		h.logger.Error("failed to write response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
}
```

### Create (POST /resource)

```go
// @Summary		Create resource
// @Description	Creates a new resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Security 	BearerAuth
// @Param		request	body	dto.CreateResourceRequest	true	"Resource data"
// @Success		201	{object}	response.Envelope[dto.CreateResourceResponse]	"Successfully created resource"
// @Failure		422	{object}	errs.Error	"Invalid request format or validation error"
// @Failure		401	{object}	errs.Error	"Invalid credentials"
// @Failure		500	{object}	errs.Error	"Internal server error"
// @Router		/api/v1/resources [post]
func (h *ResourceHandler) CreateResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	var createRequest dto.CreateResourceRequest

	err := request.ReadJSON(w, r, &createRequest)
	if err != nil {
		h.logger.Error("failed to parse request body", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	input := usecase.ResourceCreateInput{
		Name: createRequest.Name,
		// ... map other fields
	}

	output, err := h.resourceCreateUseCase.Execute(ctx, input)
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

	err = response.JSON(w, http.StatusCreated, createResponse, http.Header{})
	if err != nil {
		h.logger.Error("failed to write response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
}
```

### Update (PUT /resource/:id)

```go
// @Summary		Update resource
// @Description	Updates an existing resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Security 	BearerAuth
// @Param		id		path	int	true	"Resource ID"
// @Param		request	body	dto.UpdateResourceRequest	true	"Resource data"
// @Success		204		"Successfully updated resource"
// @Failure		422	{object}	errs.Error	"Invalid request format or validation error"
// @Failure		401	{object}	errs.Error	"Invalid credentials"
// @Failure		404	{object}	errs.Error	"Resource not found"
// @Failure		500	{object}	errs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [put]
func (h *ResourceHandler) UpdateResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	var updateRequest dto.UpdateResourceRequest

	err := request.ReadJSON(w, r, &updateRequest)
	if err != nil {
		h.logger.Error("failed to parse request body", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseUint(idStr, 10, 64)
	if err != nil {
		h.logger.Error("invalid resource ID", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	input := usecase.ResourceUpdateInput{
		ID:   id,
		Name: updateRequest.Name,
		// ... map other fields
	}

	err = h.resourceUpdateUseCase.Execute(ctx, input)
	if err != nil {
		h.logger.Error("failed to update resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	response.NoContent(w)
}
```

### Delete (DELETE /resource/:id)

```go
// @Summary		Delete resource
// @Description	Deletes an existing resource
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Security 	BearerAuth
// @Param		id	path	int	true	"Resource ID"
// @Success		204		"Successfully deleted resource"
// @Failure		401	{object}	errs.Error	"Invalid credentials"
// @Failure		404	{object}	errs.Error	"Resource not found"
// @Failure		500	{object}	errs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [delete]
func (h *ResourceHandler) DeleteResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseUint(idStr, 10, 64)
	if err != nil {
		h.logger.Error("invalid resource ID", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	input := usecase.ResourceDeleteInput{
		ID: id,
	}

	err = h.resourceDeleteUseCase.Execute(ctx, input)
	if err != nil {
		h.logger.Error("failed to delete resource", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	response.NoContent(w)
}
```

### Get by ID (GET /resource/:id)

```go
// @Summary		Get resource
// @Description	Retrieves a resource by ID
// @Tags		Resources
// @Accept		json
// @Produce		json
// @Security 	BearerAuth
// @Param		id	path	int	true	"Resource ID"
// @Success		200	{object}	response.Envelope[dto.ResourceResponse]	"Successfully retrieved resource"
// @Failure		401	{object}	errs.Error	"Invalid credentials"
// @Failure		404	{object}	errs.Error	"Resource not found"
// @Failure		500	{object}	errs.Error	"Internal server error"
// @Router		/api/v1/resources/{id} [get]
func (h *ResourceHandler) GetResource(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	idStr := chi.URLParam(r, "id")
	id, err := strconv.ParseUint(idStr, 10, 64)
	if err != nil {
		h.logger.Error("invalid resource ID", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}

	input := usecase.ResourceGetInput{
		ID: id,
	}

	output, err := h.resourceGetUseCase.Execute(ctx, input)
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

	err = response.JSON(w, http.StatusOK, resourceResponse, http.Header{})
	if err != nil {
		h.logger.Error("failed to write response", logger.Error(err))
		h.errorHandler.Error(w, err)
		return
	}
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
9. **@Failure**: Common errors (401, 404, 422, 500) with `{object} errs.Error`
10. **@Router**: `/api/v1/resources/{id} [method]`

## Request/Response Mapping

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

## Error Handling Pattern

Every error follows this pattern:

```go
if err != nil {
	h.logger.Error("descriptive error message", logger.Error(err))
	h.errorHandler.Error(w, err)
	return
}
```

Error messages:
- "failed to parse request body" - JSON decode error
- "invalid resource ID" - URL param parsing error
- "failed to list resources" - List use case error
- "failed to create resource" - Create use case error
- "failed to update resource" - Update use case error
- "failed to delete resource" - Delete use case error
- "failed to get resource" - Get use case error
- "failed to write response" - JSON response write error

## Fx Wiring

**Add to `internal/modules/<module>/fx.go`**:

```go
fx.Provide(handler.NewResourceHandler),
```

The handler is typically provided to the router, not exposed as a port.

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Struct**: Include all use cases, `response.ErrorHandler`, and `logger.Logger`
2. **Constructor**: MUST return pointer `*ResourceHandler`
3. **Context**: Always get from request: `ctx := r.Context()`
4. **Request decoding**: Use `request.ReadJSON(w, r, &dto)` - declare variable first, then call ReadJSON
5. **URL params**: Use `chi.URLParam(r, "paramName")` and `strconv.ParseUint` for IDs
6. **Error handling**: Always log error and call `h.errorHandler.Error(w, err)` then return
7. **Response mapping**: Map use case output to DTO, don't return use case outputs directly
8. **Success responses**: 
   - List/Get: Use `response.JSON(w, http.StatusOK, data, http.Header{})`
   - Create: Use `response.JSON(w, http.StatusCreated, data, http.Header{})`
   - Update/Delete: Use `response.NoContent(w)`
9. **Swagger**: MUST add complete swagger annotations for every handler method
10. **No comments**: Do not add redundant comments inside method bodies
11. **Validation**: Run `make lint` and `make update-swagger` after generation

## Workflow

1. Create handler struct with use case dependencies
2. Implement constructor `NewResourceHandler`
3. Implement handler methods following patterns above
4. Add swagger annotations to all methods
5. Add Fx wiring to module's `fx.go`
6. Run `make lint` and `make nilaway` to verify the static tests
7. Run `make update-swagger` to regenerate swagger docs
