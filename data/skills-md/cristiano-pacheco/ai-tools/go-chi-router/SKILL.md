---
name: go-chi-router
description: Generate Chi router implementations following Go modular architecture conventions (Chi router from bricks package, Fx DI with chi.Route interface, REST endpoints). Always use this skill when creating or modifying HTTP route registration in internal/modules/<module>/http/chi/router/, including any new router file, CRUD routes (GET, POST, PUT, DELETE), custom action endpoints, versioned APIs, route groups with middleware, or wiring routers into a module's fx.go.
---

# Go Chi Router

Generate Chi router implementations for Go backend HTTP transport layer.

**Location**: `internal/modules/<module>/http/chi/router/<resource>_router.go`

## Router Implementation

```go
package router

import (
	"github.com/cristiano-pacheco/bricks/pkg/http/server/chi"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/http/chi/handler"
)

type ResourceRouter struct {
	handler *handler.ResourceHandler
}

func NewResourceRouter(h *handler.ResourceHandler) *ResourceRouter {
	return &ResourceRouter{handler: h}
}

func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Get("/api/v1/resources/{id}", r.handler.GetResource)
	router.Post("/api/v1/resources", r.handler.CreateResource)
	router.Put("/api/v1/resources/{id}", r.handler.UpdateResource)
	router.Delete("/api/v1/resources/{id}", r.handler.DeleteResource)
}
```

## Router Patterns

### Custom Endpoints

Use `POST` with a verb suffix for non-CRUD state transitions. Use nested paths for sub-resources.

```go
func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Post("/api/v1/resources", r.handler.CreateResource)
	router.Post("/api/v1/resources/{id}/activate", r.handler.ActivateResource)
	router.Post("/api/v1/resources/{id}/deactivate", r.handler.DeactivateResource)
	router.Get("/api/v1/resources/{id}/items", r.handler.ListResourceItems)
	router.Post("/api/v1/resources/{id}/items", r.handler.AddResourceItem)
}
```

### Route Groups (with middleware)

Use `router.Group` to scope middleware to a subset of routes without affecting others.

```go
func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Get("/api/v1/resources/{id}", r.handler.GetResource)
	router.Group(func(r chi.Router) {
		r.Use(middleware.Auth)
		r.Post("/api/v1/resources", r.handler.CreateResource)
		r.Put("/api/v1/resources/{id}", r.handler.UpdateResource)
		r.Delete("/api/v1/resources/{id}", r.handler.DeleteResource)
	})
}
```

### Multiple Handlers

When a router logically owns routes across two related resources (e.g., a resource and its items), inject both handlers via the constructor.

```go
type ResourceRouter struct {
	resourceHandler *handler.ResourceHandler
	itemHandler     *handler.ItemHandler
}

func NewResourceRouter(
	resourceHandler *handler.ResourceHandler,
	itemHandler *handler.ItemHandler,
) *ResourceRouter {
	return &ResourceRouter{
		resourceHandler: resourceHandler,
		itemHandler:     itemHandler,
	}
}

func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.resourceHandler.ListResources)
	router.Post("/api/v1/resources", r.resourceHandler.CreateResource)
	router.Get("/api/v1/items", r.itemHandler.ListItems)
	router.Post("/api/v1/items", r.itemHandler.CreateItem)
}
```

## Fx Wiring

Add to `internal/modules/<module>/fx.go`. The `fx.As(new(chi.Route))` and `fx.ResultTags` are required — they register the router into the `routes` group so the HTTP server discovers it automatically.

```go
fx.Provide(
	fx.Annotate(
		router.NewResourceRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
),
```

**Multiple routers in the same module**:

```go
fx.Provide(
	fx.Annotate(
		router.NewResourceRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
	fx.Annotate(
		router.NewItemRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
),
```

## URL Path Conventions

- **Version prefix**: `/api/v1/`
- **Resource names**: Plural nouns (`/resources`, `/contacts`, `/monitors`)
- **Resource ID**: `{id}` path param (`/resources/{id}`)
- **Nested resources**: `/resources/{id}/items`
- **Nested with two IDs**: `/resources/{resourceId}/items/{itemId}`
- **Actions**: Verb suffix for non-CRUD (`/resources/{id}/activate`)
- **Bulk**: `/resources/bulk` with appropriate HTTP method

## HTTP Methods

- `GET`: Retrieve (list or single)
- `POST`: Create, or trigger an action
- `PUT`: Full update
- `PATCH`: Partial update
- `DELETE`: Remove

## Naming Conventions

- **Struct**: `<Resource>Router` (PascalCase)
- **Constructor**: `New<Resource>Router`
- **File**: `<resource>_router.go` (snake_case)
- **Handler methods**: Match action — `ListResources`, `CreateResource`, `ActivateResource`

## Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. The struct holds only handler pointer(s) — no other state
2. Constructor returns a pointer (`*ResourceRouter`)
3. `Setup` method signature is exactly `Setup(server *chi.Server)` — never deviate
4. Always call `server.Router()` inside `Setup` to get the chi router
5. Every route must start with `/api/v1/`
6. Resource names in paths are plural nouns
7. Fx wiring requires both `fx.As(new(chi.Route))` and `fx.ResultTags(\`group:"routes"\`)`
8. Imports: only `bricks/pkg/http/server/chi` and the handler package (plus middleware if using route groups)
9. No comments in the file — the code is self-describing
10. Run `make lint` after generating

## Workflow

1. Create `internal/modules/<module>/http/chi/router/<resource>_router.go`
2. Define struct with handler field(s)
3. Implement constructor
4. Implement `Setup(server *chi.Server)` with all routes
5. Add Fx wiring to `internal/modules/<module>/fx.go`
6. Run `make lint` and `make nilaway` to ensure code quality and no nil pointer issues
