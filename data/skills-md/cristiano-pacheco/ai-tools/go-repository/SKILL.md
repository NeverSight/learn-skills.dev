---
name: go-repository
description: Generate Go repository port interfaces and implementations following Go modular architecture conventions. Use when creating data access layers for entities in internal/modules/<module>/ including CRUD operations (Create, FindAll, FindByID, Update, Delete), custom queries, pagination, or transactions.
---

# Go Repository

Generate repository port interfaces and implementations for Go modular architecture conventions.

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

**Custom methods**: Add domain-specific queries as needed (e.g., `FindByName`, `AssignContacts`).

## Repository Implementation Structure

**Location**: `internal/modules/<module>/repository/<entity>_repository.go`

```go
package repository

import (
	"context"
	"errors"
	
	"github.com/cristiano-pacheco/bricks/pkg/errs"
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
	return &EntityRepository{db}
}
```

## Method Implementations

### FindAll (Simple)

```go
func (r *EntityRepository) FindAll(ctx context.Context) ([]model.EntityModel, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.FindAll")
	defer otelSpan.End()

	entities, err := gorm.G[model.EntityModel](r.DB).Find(ctx)
	if err != nil {
		return nil, err
	}
	return entities, nil
}
```

### FindAll (Paginated)

```go
func (r *EntityRepository) FindAll(ctx context.Context, page, pageSize int) ([]model.EntityModel, int64, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.FindAll")
	defer otelSpan.End()

	offset := (page - 1) * pageSize

	var total int64
	if err := r.DB.Model(&model.EntityModel{}).Count(&total).Error; err != nil {
		return nil, 0, err
	}

	entities, err := gorm.G[model.EntityModel](r.DB).
		Limit(pageSize).
		Offset(offset).
		Find(ctx)
	if err != nil {
		return nil, 0, err
	}

	return entities, total, nil
}
```

### FindByID

```go
func (r *EntityRepository) FindByID(ctx context.Context, id uint64) (model.EntityModel, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.FindByID")
	defer otelSpan.End()

	entity, err := gorm.G[model.EntityModel](r.DB).
		Where("id = ?", id).
		Limit(1).
		First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, errs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Create

```go
func (r *EntityRepository) Create(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.Create")
	defer otelSpan.End()

	err := gorm.G[model.EntityModel](r.DB).Create(ctx, &entity)
	return entity, err
}
```

### Update

```go
func (r *EntityRepository) Update(ctx context.Context, entity model.EntityModel) (model.EntityModel, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.Update")
	defer otelSpan.End()

	_, err := gorm.G[model.EntityModel](r.DB).Updates(ctx, entity)
	if err != nil {
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Delete

```go
func (r *EntityRepository) Delete(ctx context.Context, id uint64) error {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.Delete")
	defer otelSpan.End()

	rowsAffected, err := gorm.G[model.EntityModel](r.DB).
		Where("id = ?", id).
		Delete(ctx)
	if err != nil {
		return err
	}
	if rowsAffected == 0 {
		return errs.ErrRecordNotFound
	}
	return nil
}
```

### Custom Query (by field)

```go
func (r *EntityRepository) FindByName(ctx context.Context, name string) (model.EntityModel, error) {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.FindByName")
	defer otelSpan.End()

	entity, err := gorm.G[model.EntityModel](r.DB).
		Where("name = ?", name).
		Limit(1).
		First(ctx)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return model.EntityModel{}, errs.ErrRecordNotFound
		}
		return model.EntityModel{}, err
	}
	return entity, nil
}
```

### Transaction (relationship operations)

```go
func (r *EntityRepository) AssignRelated(ctx context.Context, entityID uint64, relatedIDs []uint64) error {
	ctx, otelSpan := trace.Span(ctx, "EntityRepository.AssignRelated")
	defer otelSpan.End()

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

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Struct**: Embed `*database.PingoDB` only
2. **Constructor**: MUST return pointer `*EntityRepository`
3. **Interface assertion**: Add `var _ ports.EntityRepository = (*EntityRepository)(nil)` below struct
4. **Tracing**: Every method MUST start with `ctx, otelSpan := trace.Span(ctx, "Repo.Method")` and `defer otelSpan.End()`
5. **Queries**: Use `gorm.G[Model](r.DB)` pattern for all queries
6. **First queries**: Add `.Limit(1)` before `.First(ctx)`
7. **Not found**: Return `errs.ErrRecordNotFound` when `errors.Is(err, gorm.ErrRecordNotFound)`
8. **Delete**: Check `rowsAffected == 0` and return `errs.ErrRecordNotFound`
9. **Transactions**: Use `tx := r.DB.Begin()`, rollback on error, commit at end
10. **No comments**: Do not add redundant comments above methods
11. **Validation**: Run `make lint` and `make nilaway` after generation
12. **Add detailed comment on interfaces**: Provide comprehensive comments on the port interfaces to describe their purpose and usage

## Workflow

1. Create port interface in `ports/<entity>_repository.go`
2. Create repository implementation in `repository/<entity>_repository.go`
3. Add Fx wiring to module's `fx.go`
4. Run `make lint` to verify
5. Run `make nilaway` for static analysis
