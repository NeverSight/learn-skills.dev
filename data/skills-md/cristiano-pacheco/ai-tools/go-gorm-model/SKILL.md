---
name: go-gorm-model
description: Generate Go GORM models following Go modular architecture conventions. Use when creating or updating persistence models in internal/modules/<module>/model/, including table mapping, nullable pointer types, index tags, PostgreSQL-specific types, and timestamps. Always use this skill when asked to create a model, add a GORM struct, map a database table, or generate model files.
---

# Go GORM Model

Generate GORM persistence models in `internal/modules/<module>/model/`.

## Pattern

Model files must follow this location and naming:

- Path: `internal/modules/<module>/model/<entity>_model.go`
- Package: `model`
- Struct name: `<Entity>Model`
- TableName method: `func (*<Entity>Model) TableName() string { return "<table_name>" }`

## File Structure

Use this order:

1. `package model`
2. Imports (`"time"` only — add others only when strictly required)
3. Struct definition with doc comment
4. `TableName()` method with doc comment

## Base Template

```go
package model

import "time"

// EntityModel represents an entity in the database.
type EntityModel struct {
	ID        uint64    `gorm:"primarykey"`
	Name      string
	CreatedAt time.Time
	UpdatedAt time.Time
}

// TableName returns the table name for the entity model.
func (*EntityModel) TableName() string {
	return "entities"
}
```

## Conventions

### IDs and Primary Keys

- Use `uint64` for the `ID` primary key field, always tagged `gorm:"primarykey"`.
- Foreign key fields (references to another table's PK) also use `uint64` when NOT NULL, or `*uint64` when nullable.

### Time Fields

- Use `time.Time` for `TIMESTAMPTZ` columns (`CreatedAt`, `UpdatedAt`, etc.).
- No explicit column tag needed — GORM maps `CreatedAt` → `created_at` by convention.

### Nullable Fields

Use **Go pointer types** for nullable columns. Never use `database/sql` types (`sql.NullString`, `sql.NullInt32`, etc.) — those are not used in this codebase.

| SQL nullable type | Go type |
|---|---|
| `TEXT` / `VARCHAR` nullable | `*string` |
| `BIGINT` nullable (value) | `*int64` |
| `BIGINT` nullable (FK) | `*uint64` |
| `BOOLEAN` nullable | `*bool` |
| `TIMESTAMPTZ` nullable | `*time.Time` |

Examples from this codebase:

```go
Description      *string  // nullable TEXT
PromotionalPrice *int64   // nullable BIGINT value
CategoryID       *uint64  // nullable BIGINT FK
SceneContext     *string  // nullable TEXT
```

### Column Tags

Do NOT add `gorm:"column:..."` tags. GORM automatically maps Go field names to snake_case column names (`ProductID` → `product_id`, `CreatedAt` → `created_at`, etc.). Only add tags when there is a specific GORM feature to declare.

Add tags only for:
- `gorm:"primarykey"` — primary key
- `gorm:"uniqueIndex"` / `gorm:"uniqueIndex:name"` — unique constraints
- `gorm:"index"` — regular indexes
- `gorm:"type:jsonb"` — PostgreSQL JSONB columns
- `gorm:"default:'value'"` — column-level defaults
- `gorm:"->;column:name"` — computed/read-only virtual columns

### Index and Constraint Tags

Declare indexes inline on the field:

```go
Slug         string `gorm:"uniqueIndex"`
ProductID    uint64 `gorm:"index"`

// Named composite unique index (both fields must share the same name)
CollectionID uint64 `gorm:"uniqueIndex:idx_collection_product"`
ProductID    uint64 `gorm:"uniqueIndex:idx_collection_product"`
```

### PostgreSQL-Specific Types

- `JSONB` → `[]byte` with `gorm:"type:jsonb"`
- `default` values → `gorm:"default:'value'"`

```go
Attributes   []byte `gorm:"type:jsonb"`
PrimaryColor string `gorm:"default:'#1d4ed8'"`
```

### Value Types vs FK Types

BIGINT is not always `uint64`. Distinguish by semantics:

- Primary key: `uint64` with `gorm:"primarykey"`
- Foreign key NOT NULL: `uint64`
- Foreign key nullable: `*uint64`
- Numeric value (price, weight, size, quantity): `int64` / `*int64`
- Small integer (sort order, display order): `int`
- Boolean: `bool`

## Generation Steps

1. Identify module and entity.
2. Read the migration SQL file and confirm the exact table name and column definitions.
3. Create `internal/modules/<module>/model/<entity>_model.go`.
4. Map each SQL column to the correct Go field name and type.
5. Use pointer types for nullable columns.
6. Add GORM tags only where needed (index, uniqueIndex, type, default).
7. Add doc comment to the struct and to `TableName()`.
8. Verify struct field order matches the column order in the migration (for readability).

## Type Mapping Guide

| SQL Type | NOT NULL | Nullable |
|---|---|---|
| `BIGSERIAL PRIMARY KEY` | `uint64` + `gorm:"primarykey"` | — |
| `BIGINT` FK | `uint64` | `*uint64` |
| `BIGINT` value | `int64` | `*int64` |
| `INT` | `int` | `*int` |
| `VARCHAR` / `TEXT` | `string` | `*string` |
| `BOOLEAN` | `bool` | `*bool` |
| `TIMESTAMPTZ` | `time.Time` | `*time.Time` |
| `JSONB` | `[]byte` + `gorm:"type:jsonb"` | — |

## Example: Simple Model

```go
package model

import "time"

// CategoryModel represents a category in the database.
type CategoryModel struct {
	ID         uint64    `gorm:"primarykey"`
	Name       string    `gorm:"uniqueIndex"`
	Slug       string    `gorm:"uniqueIndex"`
	ShowInMenu bool
	CreatedAt  time.Time
	UpdatedAt  time.Time
}

// TableName returns the table name for the category model.
func (*CategoryModel) TableName() string {
	return "categories"
}
```

## Example: Model with Nullable Fields and JSONB

```go
package model

import "time"

// ProductModel represents a product in the database.
type ProductModel struct {
	ID               uint64  `gorm:"primarykey"`
	Title            string
	Description      string
	Price            int64
	PromotionalPrice *int64
	SKU              string  `gorm:"uniqueIndex"`
	Status           string
	WeightGrams      *int64
	WidthCm          *int64
	LengthCm         *int64
	HeightCm         *int64
	StockQuantity    int64
	CategoryID       *uint64
	Attributes       []byte  `gorm:"type:jsonb"`
	CreatedAt        time.Time
	UpdatedAt        time.Time
}

// TableName returns the table name for the product model.
func (*ProductModel) TableName() string {
	return "products"
}
```

## Example: Join Table (Composite Unique Index)

```go
package model

import "time"

// CollectionProductModel represents the many-to-many relationship
// between collections and products.
type CollectionProductModel struct {
	ID           uint64    `gorm:"primarykey"`
	CollectionID uint64    `gorm:"uniqueIndex:idx_collection_product"`
	ProductID    uint64    `gorm:"uniqueIndex:idx_collection_product"`
	CreatedAt    time.Time
}

// TableName returns the table name for the collection product model.
func (*CollectionProductModel) TableName() string {
	return "collection_products"
}
```

## Example: Model with Default Values

```go
package model

import "time"

// ProfileModel represents the business profile in the database.
type ProfileModel struct {
	ID            uint64    `gorm:"primarykey"`
	BusinessName  string
	WhatsAppPhone string
	LogoPath      string
	LogoMimeType  string
	PrimaryColor  string    `gorm:"default:'#1d4ed8'"`
	AccentColor   string    `gorm:"default:'#16a34a'"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

// TableName returns the table name for the profile model.
func (*ProfileModel) TableName() string {
	return "profiles"
}
```

## Critical Rules

- Models are persistence only — business logic belongs in use cases.
- Do not expose GORM models directly in HTTP DTO responses.
- Keep field names and types aligned with SQL migrations.
- Use Go pointer types (`*string`, `*int64`, `*uint64`) for nullable columns — never `database/sql` types.
- Do NOT add `gorm:"column:..."` tags unless GORM convention cannot handle the mapping.
- Never use `json` tags on GORM models.
- Use module-local model package only (`internal/modules/<module>/model`).
- Always add doc comments on the struct and `TableName()` method.
- Do not change existing column or table names without a corresponding migration update.

## Checklist

- [ ] File at `internal/modules/<module>/model/<entity>_model.go`
- [ ] Struct named `<Entity>Model` with doc comment
- [ ] `ID uint64` with `gorm:"primarykey"`
- [ ] Nullable columns use pointer types (`*string`, `*int64`, `*uint64`)
- [ ] No `database/sql` import or nullable SQL types
- [ ] No explicit `gorm:"column:..."` tags unless required
- [ ] Index/constraint tags present where migration defines them (`uniqueIndex`, `index`)
- [ ] PostgreSQL-specific columns tagged (`type:jsonb`, `default:...`)
- [ ] `TableName()` with doc comment returns exact SQL table name
- [ ] No `json` tags
