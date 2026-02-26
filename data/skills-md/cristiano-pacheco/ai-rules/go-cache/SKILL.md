---
name: go-cache
description: Generate Go cache implementations following GO modular architecture conventions. Always use this skill when the user asks to create a cache, add a Redis cache layer, cache short-lived data with TTL, implement rate limiting storage, OTP caching, session caching, OAuth state storage, or any domain cache in internal/modules/<module>/cache/. Invoke proactively whenever the user mentions caching, Redis-backed storage, TTL expiry, or temporary data — even if they don't say "cache" explicitly.
---

# Go Cache

Generate two files for every cache: a **port interface** and a **Redis-backed implementation**.

## Which Variant?

Pick before writing anything:

| Scenario | Variant | Get return type |
|---|---|---|
| Flag, existence check, rate limit | **Boolean flag** | `bool` |
| Structured data — tokens, sessions, profiles | **JSON data** | `*dto.XxxData` |

For TTL:
- **Fixed TTL** — short-lived or individually written entries (OTPs, OAuth state, rate limits, sessions)
- **Randomized TTL** — long-lived entries written in bulk (activation flags, daily metrics) — prevents cache stampede

## Two-File Pattern

Every cache requires exactly two files:

1. **Port interface**: `internal/modules/<module>/ports/<cache_name>_cache.go`
2. **Cache implementation**: `internal/modules/<module>/cache/<cache_name>_cache.go`

### File Layout Order

1. Constants (key prefix, TTL)
2. Implementation struct (`XxxCache`)
3. Compile-time interface assertion
4. Constructor (`NewXxxCache`)
5. Methods (`Set`, `Get`, `Delete`)
6. Helper methods (`buildKey`, `calculateTTL`)

---

## Boolean Flag Cache

Use when caching simple existence flags, presence checks, or rate limit states.

- Store `"1"` as the value
- Return `false, nil` when the key doesn't exist (not an error)

### Port

```go
package ports

import "context"

// XxxCache describes ...
type XxxCache interface {
	Set(ctx context.Context, id uint64) error
	Get(ctx context.Context, id uint64) (bool, error)
	Delete(ctx context.Context, id uint64) error
}
```

### Implementation

```go
package cache

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
	redislib "github.com/redis/go-redis/v9"
)

const (
	entityCacheKeyPrefix = "entity_name:"
	entityCacheTTL       = 10 * time.Minute
)

type EntityCache struct {
	redisClient redis.UniversalClient
}

var _ ports.EntityCache = (*EntityCache)(nil)

func NewEntityCache(redisClient redis.UniversalClient) *EntityCache {
	return &EntityCache{
		redisClient: redisClient,
	}
}

func (c *EntityCache) Set(ctx context.Context, id uint64) error {
	key := c.buildKey(id)
	return c.redisClient.Set(ctx, key, "1", entityCacheTTL).Err()
}

func (c *EntityCache) Get(ctx context.Context, id uint64) (bool, error) {
	key := c.buildKey(id)
	result := c.redisClient.Get(ctx, key)
	if err := result.Err(); err != nil {
		if errors.Is(err, redislib.Nil) {
			return false, nil
		}
		return false, err
	}
	return true, nil
}

func (c *EntityCache) Delete(ctx context.Context, id uint64) error {
	key := c.buildKey(id)
	return c.redisClient.Del(ctx, key).Err()
}

func (c *EntityCache) buildKey(id uint64) string {
	return fmt.Sprintf("%s%d", entityCacheKeyPrefix, id)
}
```

---

## JSON Data Cache

Use when caching structured data. Data structs are defined in the `dto` package, never in `ports`.

- Serialize with `json.Marshal` before storing
- Deserialize with `json.Unmarshal` when retrieving
- Return `nil, nil` on missing key — unless the key is always expected to exist, in which case return a domain error (e.g., `errs.ErrXxxNotFound`)
- Use distinct variable names (`getErr`, `unmarshalErr`) to avoid shadowing

### Port

```go
package ports

import (
	"context"

	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/dto"
}

// XxxCache describes ...
type XxxCache interface {
	Set(ctx context.Context, key string, data dto.XxxData) error
	Get(ctx context.Context, key string) (dto.XxxData, error)
	Delete(ctx context.Context, key string) error
}
```

### Implementation

```go
package cache

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/redis"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/dto"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
	redislib "github.com/redis/go-redis/v9"
)

const (
	entityCacheKeyPrefix = "entity_name:"
	entityCacheTTL       = 10 * time.Minute
)

type EntityCache struct {
	redisClient redis.UniversalClient
}

var _ ports.EntityCache = (*EntityCache)(nil)

func NewEntityCache(redisClient redis.UniversalClient) *EntityCache {
	return &EntityCache{
		redisClient: redisClient,
	}
}

func (c *EntityCache) Set(ctx context.Context, key string, data dto.EntityData) error {
	cacheKey := c.buildKey(key)
	jsonData, err := json.Marshal(data)

	if err != nil {
		return fmt.Errorf("marshal entity data: %w", err)
	}

	return c.redisClient.Set(ctx, cacheKey, jsonData, entityCacheTTL).Err()
}

func (c *EntityCache) Get(ctx context.Context, key string) (dto.EntityData, error) {
	cacheKey := c.buildKey(key)
	result := c.redisClient.Get(ctx, cacheKey)

	if getErr := result.Err(); getErr != nil {
		if errors.Is(getErr, redislib.Nil) {
			return dto.EntityData{}, nil
		}
		return dto.EntityData{}, getErr
	}

	jsonData, err := result.Bytes()

	if err != nil {
		return dto.EntityData{}, fmt.Errorf("get bytes: %w", err)
	}

	var entityData dto.EntityData
	if unmarshalErr := json.Unmarshal(jsonData, &entityData); unmarshalErr != nil {
		return dto.EntityData{}, fmt.Errorf("unmarshal entity data: %w", unmarshalErr)
	}
	
	return entityData, nil
}

func (c *EntityCache) Delete(ctx context.Context, key string) error {
	cacheKey := c.buildKey(key)
	return c.redisClient.Del(ctx, cacheKey).Err()
}

func (c *EntityCache) buildKey(key string) string {
	return entityCacheKeyPrefix + key
}
```

---

## Key Building

String ID (simple concatenation):

```go
func (c *EntityCache) buildKey(id string) string {
	return entityCacheKeyPrefix + id
}
```

Uint64 ID:

```go
func (c *EntityCache) buildKey(id uint64) string {
	return fmt.Sprintf("%s%d", entityCacheKeyPrefix, id)
}
```

Composite key:

```go
func (c *EntityCache) buildKey(userID uint64, resourceID string) string {
	return fmt.Sprintf("%s%d:%s", entityCacheKeyPrefix, userID, resourceID)
}
```

## TTL Configuration

**Fixed TTL** — for short-lived data where stampede is not a concern:

```go
const (
	entityCacheKeyPrefix = "entity_name:"
	entityCacheTTL       = 10 * time.Minute
)
```

**Randomized TTL** — for long-lived data created in bulk (prevents cache stampede):

```go
import "math/rand"

const (
	entityCacheKeyPrefix = "entity_name:"
	entityCacheTTLMin    = 23 * time.Hour
	entityCacheTTLMax    = 25 * time.Hour
)

func (c *EntityCache) calculateTTL() time.Duration {
	min := entityCacheTTLMin.Milliseconds()
	max := entityCacheTTLMax.Milliseconds()
	randomMs := min + rand.Int63n(max-min+1)
	return time.Duration(randomMs) * time.Millisecond
}
```

Common TTL ranges:
- `5-15 minutes` — OTP codes, OAuth state, rate limits
- `50-70 minutes` — User sessions
- `12-25 hours` — Activation flags, daily metrics
- `6.5-7.5 days` — Weekly aggregations

## Naming

- Port interface: `XxxCache` (`ports` package, no suffix)
- Implementation struct: `XxxCache` (`cache` package — same name, disambiguated by package)
- Constructor: `NewXxxCache`, returns `*XxxCache`
- Constants: lowercase, package-level (e.g. `entityCacheKeyPrefix`, `entityCacheTTL`)

## Fx Wiring

Add to `internal/modules/<module>/module.go`:

```go
fx.Provide(
	fx.Annotate(
		cache.NewXxxCache,
		fx.As(new(ports.XxxCache)),
	),
),
```

## Dependencies

- `redis.UniversalClient` from `"github.com/cristiano-pacheco/bricks/pkg/redis"`
- `redislib "github.com/redis/go-redis/v9"` for nil detection

## Critical Rules

1. **No standalone functions**: When a file contains a struct with methods, do not add standalone functions. Use private methods on the struct instead.
2. **Two files**: Port in `ports/`, implementation in `cache/`
2. **Interface assertion**: `var _ ports.XxxCache = (*XxxCache)(nil)` immediately below the struct
3. **Constructor**: Returns `*XxxCache` (pointer)
4. **Context**: Always accept `ctx context.Context` as first parameter — never call `context.Background()` internally
5. **Redis nil**: Import `redislib "github.com/redis/go-redis/v9"` and check with `errors.Is(err, redislib.Nil)`
6. **TTL scope**: TTL is an implementation detail — never expose it as a method parameter
7. **buildKey**: Always use a `buildKey()` helper; `+` for string IDs, `fmt.Sprintf` for numeric IDs
8. **Missing keys**: Boolean cache returns `false, nil`; JSON cache returns `nil, nil` (or a domain error if the key must exist)
9. **DTOs in dto package**: Data structs belong in `dto/`, never defined inline in `ports/`
10. **No method comments**: Only port interfaces get doc comments; implementation methods do not
11. **Error messages**: `"action noun: %w"` format (e.g., `"marshal oauth state: %w"`, `"get bytes: %w"`)

## Workflow

1. Decide variant: Boolean flag or JSON data?
2. Create port interface in `ports/<name>_cache.go`
3. Create cache implementation in `cache/<name>_cache.go`
4. Add Fx wiring to `module.go`
5. Run `make lint`
6. Run `make nilaway`
