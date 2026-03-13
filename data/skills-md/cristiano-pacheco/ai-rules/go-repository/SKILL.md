---
name: go-repository
description: Generate repository port interfaces and GORM implementations. Use for data access layers, CRUD, custom queries, pagination, transactions.
---

# Go Repository

Generate repository port interfaces and implementations for Go modular architecture conventions.

## When to Use

- Create data access layers for entities
- CRUD operations (Create, FindAll, FindByID, Update, Delete)
- Custom queries, pagination, transactions
- Join queries and filtered lookups

## Two-File Pattern

Every repository requires two files:

1. **Port interface**: `internal/modules/<module>/ports/<entity>_repository.go`
2. **Repository implementation**: `internal/modules/<module>/repository/<entity>_repository.go`

## Port Interface Structure

**Location**: `internal/modules/<module>/ports/<entity>_repository.go`

```go
package ports

import (
	"context"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/model"
)

// EntityRepository defines entity persistence operations.
//
// Add a comprehensive comment here describing the purpose of the repository,
// what domain concept it represents, and any non-obvious behavior.
type EntityRepository interface {
	FindAll(ctx context.Context) ([]model.EntityModel, error)
	FindByID(ctx context.Context, id uint64) (model.EntityModel, error)
	Create(ctx context.Context, entity model.EntityModel) (model.EntityModel, error)
	Update(ctx context.Context, entity model.EntityModel) (model.EntityModel, error)
	Delete(ctx context.Context, id uint64) error
}
```

**Pagination variant**:
```go
FindAll(ctx context.Context, page, pageSize int) ([]model.EntityModel, int64, error)
```

**Custom methods**: Add domain-specific queries as needed (e.g., `FindByName`, `FindBySKU`).

## Repository Implementation Structure

**Location**: `internal/modules/<module>/repository/<entity>_repository.go`

```go
package repository

import (
	"context"
	"errors"

	brickserrs "github.com/cristiano-pacheco/bricks/pkg/errs"
	"github.com/cristiano-pacheco/bricks/pkg/otel/trace"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/model"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
	"github.com/cristiano-pacheco/pingo/internal/shared/database"
	"gorm.io/gorm"
)

type EntityRepository struct {
	*database.PingoDB
}

var _ ports.EntityRepository = (*EntityRepository)(nil)

func NewEntityRepository(db *database.PingoDB) *EntityRepository {
	return &EntityRepository{PingoDB: db}
}
```

> **Note**: The constructor MUST use named field initialization `{PingoDB: db}`, not positional `{db}`.

## Method Implementations

### FindAll (Simple)

```go
func (r *EntityRepository) FindAll(ctx context.Context) ([]model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.FindAll")
	defer span.End()

	entities, err := gorm.G[model.EntityModel](r.DB).Find(ctx)
	if err != nil {
		return nil, err
	}
	return entities, nil
}
```

### FindAll (Paginated with dynamic filters)

When you need optional WHERE filters or pagination, fall back to raw GORM — `gorm.G` does not support dynamic multi-condition builds. Use `r.DB.WithContext(ctx).Model(...)` for these cases:

```go
func (r *EntityRepository) FindAll(
	ctx context.Context,
	filter dto.EntityFilter,
	paginationParams paginator.Params,
) ([]model.EntityModel, int64, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.FindAll")
	defer span.End()

	baseQuery := r.DB.WithContext(ctx).Model(&model.EntityModel{})
	if filter.Status != "" {
		baseQuery = baseQuery.Where("status = ?", filter.Status)
	}
	if filter.Name != nil && strings.TrimSpace(*filter.Name) != "" {
		baseQuery = baseQuery.Where("name ILIKE ?", "%"+strings.TrimSpace(*filter.Name)+"%")
	}

	var totalCount int64
	if err := baseQuery.Count(&totalCount).Error; err != nil {
		return nil, 0, err
	}

	query := baseQuery.Order("id DESC")
	if paginationParams.Limit() > 0 {
		query = query.Limit(paginationParams.Limit())
	}
	if paginationParams.Offset() > 0 {
		query = query.Offset(paginationParams.Offset())
	}

	results := make([]model.EntityModel, 0)
	if err := query.Find(&results).Error; err != nil {
		return nil, 0, err
	}

	return results, totalCount, nil
}
```

### FindAll (JOIN query)

For queries that require JOINs, also use raw GORM:

```go
func (r *EntityRepository) FindByRelatedID(
	ctx context.Context,
	relatedID uint64,
) ([]model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.FindByRelatedID")
	defer span.End()

	var results []model.EntityModel
	err := r.DB.WithContext(ctx).
		Model(&model.EntityModel{}).
		Joins("JOIN related_table rt ON rt.entity_id = entities.id").
		Where("rt.related_id = ?", relatedID).
		Order("rt.id ASC").
		Find(&results).Error
	if err != nil {
		return nil, err
	}

	return results, nil
}
```

### FindByID

```go
func (r *EntityRepository) FindByID(ctx context.Context, id uint64) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.FindByID")
	defer span.End()

	entity, err := gorm.G[model.EntityModel](r.DB).
		Where("id = ?", id).
		Limit(1).
		First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, brickserrs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Create

```go
func (r *EntityRepository) Create(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.Create")
	defer span.End()

	err := gorm.G[model.EntityModel](r.DB).Create(ctx, &entity)
	return entity, err
}
```

**When the module defines a conflict error**, map `gorm.ErrDuplicatedKey`:

```go
func (r *EntityRepository) Create(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.Create")
	defer span.End()

	err := gorm.G[model.EntityModel](r.DB).Create(ctx, &entity)
	if err != nil {
		if errors.Is(err, gorm.ErrDuplicatedKey) {
			return model.EntityModel{}, errs.ErrEntityNameConflict
		}
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Update

For updates where all fields are non-zero, use the `gorm.G` Updates pattern:

```go
func (r *EntityRepository) Update(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.Update")
	defer span.End()

	rowsAffected, err := gorm.G[model.EntityModel](r.DB).
		Where("id = ?", entity.ID).
		Updates(ctx, entity)
	if err != nil {
		return model.EntityModel{}, err
	}
	if rowsAffected == 0 {
		return model.EntityModel{}, brickserrs.ErrRecordNotFound
	}

	updated, err := gorm.G[model.EntityModel](r.DB).Where("id = ?", entity.ID).Limit(1).First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, brickserrs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return updated, nil
}
```

### Update (Zero-Value Fields)

GORM's `Updates()` skips zero values (`false`, `0`, `""`). When any updated field may be zero, use one of two patterns:

**Option A — `map[string]any`** (when fields are heterogeneous or sparse):

```go
func (r *EntityRepository) Update(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.Update")
	defer span.End()

	updates := map[string]any{
		"name":      entity.Name,
		"is_active": entity.IsActive, // bool: would be skipped by plain Updates()
		"count":     entity.Count,    // int: would be skipped when 0
	}

	result := r.DB.WithContext(ctx).
		Model(&model.EntityModel{}).
		Where("id = ?", entity.ID).
		Updates(updates)
	if result.Error != nil {
		return model.EntityModel{}, result.Error
	}
	if result.RowsAffected == 0 {
		return model.EntityModel{}, brickserrs.ErrRecordNotFound
	}

	updated, err := gorm.G[model.EntityModel](r.DB).Where("id = ?", entity.ID).Limit(1).First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, brickserrs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return updated, nil
}
```

**Option B — `Select(fields).Updates(&entity)`** (when updating a fixed set of columns):

```go
result := r.DB.WithContext(ctx).
	Model(&model.EntityModel{}).
	Where("id = ?", entity.ID).
	Select("name", "slug", "is_active").
	Updates(&entity)
```

### Single-Field Targeted Update

For methods that set one field by ID and return no model (e.g., `MarkEmailConfirmed`, `SetTOTPEnabled`), raw GORM is correct — this is intentional, not a deviation:

```go
func (r *EntityRepository) MarkConfirmed(ctx context.Context, id uint64) error {
	ctx, span := trace.Span(ctx, "EntityRepository.MarkConfirmed")
	defer span.End()

	return r.DB.WithContext(ctx).Model(&model.EntityModel{}).
		Where("id = ?", id).
		Update("confirmed", true).Error
}
```

### Delete

```go
func (r *EntityRepository) Delete(ctx context.Context, id uint64) error {
	ctx, span := trace.Span(ctx, "EntityRepository.Delete")
	defer span.End()

	rowsAffected, err := gorm.G[model.EntityModel](r.DB).
		Where("id = ?", id).
		Delete(ctx)
	if err != nil {
		return err
	}
	if rowsAffected == 0 {
		return brickserrs.ErrRecordNotFound
	}
	return nil
}
```

### Bulk Cleanup Delete

For `DeleteExpired`-style operations, zero rows deleted is not an error — discard `rowsAffected`:

```go
func (r *EntityRepository) DeleteExpired(ctx context.Context) error {
	ctx, span := trace.Span(ctx, "EntityRepository.DeleteExpired")
	defer span.End()

	_, err := gorm.G[model.EntityModel](r.DB).
		Where("expires_at < ?", time.Now().UTC()).
		Delete(ctx)
	return err
}
```

### Custom Query (by field)

```go
func (r *EntityRepository) FindByName(ctx context.Context, name string) (model.EntityModel, error) {
	ctx, span := trace.Span(ctx, "EntityRepository.FindByName")
	defer span.End()

	entity, err := gorm.G[model.EntityModel](r.DB).
		Where("name = ?", name).
		Limit(1).
		First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, brickserrs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Transaction (relationship operations)

```go
func (r *EntityRepository) AssignRelated(ctx context.Context, entityID uint64, relatedIDs []uint64) error {
	ctx, span := trace.Span(ctx, "EntityRepository.AssignRelated")
	defer span.End()

	tx := r.DB.Begin()

	_, err := gorm.G[model.EntityRelationModel](tx).
		Where("entity_id = ?", entityID).
		Delete(ctx)
	if err != nil {
		tx.Rollback()
		return err
	}

	var relations []model.EntityRelationModel
	for _, relatedID := range relatedIDs {
		relations = append(relations, model.EntityRelationModel{
			EntityID:  entityID,
			RelatedID: relatedID,
		})
	}

	err = gorm.G[model.EntityRelationModel](tx).CreateInBatches(ctx, &relations, len(relations))
	if err != nil {
		tx.Rollback()
		return err
	}

	if commitErr := tx.Commit().Error; commitErr != nil {
		return commitErr
	}

	return nil
}
```

## Fx Wiring

**Add to `internal/modules/<module>/fx.go`**:

```go
fx.Provide(
	fx.Annotate(
		repository.NewEntityRepository,
		fx.As(new(ports.EntityRepository)),
	),
),
```

## Anti-Patterns (Do NOT Do These)

### Missing `.Limit(1)` before `.First()` — BAD

```go
// BAD: missing Limit(1) — always add it before First()
entity, err := gorm.G[model.EntityModel](r.DB).
    Where("id = ?", id).
    First(ctx)  // ← wrong
```

```go
// GOOD
entity, err := gorm.G[model.EntityModel](r.DB).
    Where("id = ?", id).
    Limit(1).   // ← required
    First(ctx)
```

### Wrong span variable name — BAD

```go
// BAD: using 'span' instead of 'span'
ctx, span := trace.Span(ctx, "EntityRepository.FindByID")
defer span.End()
```

```go
// GOOD
ctx, span := trace.Span(ctx, "EntityRepository.FindByID")
defer span.End()
```

### Redundant method comments — BAD

```go
// BAD: comment that just restates the method name
// FindByID finds an entity by ID.
func (r *EntityRepository) FindByID(ctx context.Context, id uint64) (model.EntityModel, error) {

// BAD: comment that just restates the constructor
// NewEntityRepository creates a new entity repository.
func NewEntityRepository(db *database.PingoDB) *EntityRepository {
```

```go
// GOOD: no comment on self-evident methods
func (r *EntityRepository) FindByID(ctx context.Context, id uint64) (model.EntityModel, error) {

// GOOD: comment only when behavior needs explanation
// FindByPriority resolves a template using collection+category, then category, then global fallback.
func (r *AIPromptTemplateRepository) FindByPriority(...)
```

### Positional constructor initialization — BAD

```go
// BAD: positional — fragile if struct fields change
return &EntityRepository{db}
```

```go
// GOOD: named field
return &EntityRepository{PingoDB: db}
```

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Struct**: Embed `*database.PingoDB` only.
3. **Constructor**: MUST return pointer `*EntityRepository` and use named field init: `{PingoDB: db}`.
4. **Interface assertion**: Add `var _ ports.EntityRepository = (*EntityRepository)(nil)` below the struct.
5. **Tracing**: Every method MUST start with `ctx, span := trace.Span(ctx, "Repo.Method")` and `defer span.End()`. Always name the variable `span`, never `span`.
6. **`.Limit(1)` before `.First()`**: Every single-record lookup MUST have `.Limit(1)` immediately before `.First(ctx)`. No exceptions.
7. **Not found**: Return `brickserrs.ErrRecordNotFound` when `errors.Is(err, gorm.ErrRecordNotFound)`.
8. **Delete rowsAffected**: Check `rowsAffected == 0` and return `brickserrs.ErrRecordNotFound` for targeted deletes. For bulk cleanup (DeleteExpired, etc.), discard rowsAffected — zero rows is not an error.
9. **Zero-value updates**: Use `map[string]any` or `Select(fields).Updates(&model)` when any field may be a zero value (`false`, `0`, `""`). Plain `Updates(entity)` silently skips zero values.
10. **Complex queries**: Use `gorm.G[Model](r.DB)` for simple queries. Fall back to `r.DB.WithContext(ctx).Model(...)` only when `gorm.G` is insufficient: dynamic multi-condition WHERE, JOINs, subqueries, or `.Select()` with raw SQL fragments.
11. **Module-specific errors**: Prefer module-defined errors (e.g., `errs.ErrEntityNotFound`) over the generic `brickserrs.ErrRecordNotFound` when the module's `errs/` package defines them. Map `gorm.ErrDuplicatedKey` to a module conflict error when one exists.
12. **No redundant method comments**: Do not add comments above methods that merely restate the method name (e.g., `// FindByID finds an entity by ID.`). Only add comments where the logic or behavior is non-obvious.
13. **Comments on interfaces**: Port interfaces MUST have a comprehensive doc comment on the type explaining its purpose and any non-obvious behavior.
14. **Validation**: Run `make lint` and `make nilaway` after generation.

## Workflow

1. Create port interface in `ports/<entity>_repository.go`
2. Create repository implementation in `repository/<entity>_repository.go`
3. Add Fx wiring to module's `fx.go`
4. Run `make lint` to verify
5. Run `make nilaway` for static analysis
