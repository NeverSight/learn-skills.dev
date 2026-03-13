---
name: laravel-collections
description: >
  Full method API, decision guides, pitfalls, and patterns for Laravel's Collection and
  LazyCollection. Use when choosing the right collection method, writing or reviewing
  collection pipelines, or working with large datasets via cursor/lazy. Triggers on
  collect(), Collection, LazyCollection, map, filter, reduce, pluck, groupBy, each,
  cursor, or fluent array transformations in Laravel.
---

# Laravel Collections

## Quick Decision Guide

### "Which method do I use?"

**Find items:**
| Need | Method |
|------|--------|
| First item matching condition | `first(fn)` or `firstWhere('key', 'value')` |
| First item or throw | `firstOrFail(fn)` |
| Exactly one match or throw | `sole(fn)` |
| Check value exists | `contains('value')` or `contains('key', 'value')` |
| Check key exists | `has('key')` |
| All items match condition | `every(fn)` |

**Transform items:**
| Need | Method |
|------|--------|
| Transform each item | `map(fn)` |
| Transform + flatten one level | `flatMap(fn)` |
| Extract one field | `pluck('name')` |
| Extract field, keyed by another | `pluck('name', 'id')` |
| Select multiple fields | `select(['id', 'name'])` |
| Change keys | `mapWithKeys(fn)` or `keyBy('id')` |
| Map into class instances | `mapInto(DTO::class)` |

**Filter items:**
| Need | Method |
|------|--------|
| Keep matching items | `filter(fn)` |
| Remove matching items | `reject(fn)` |
| Filter by field value | `where('status', 'active')` |
| Filter by field in list | `whereIn('status', ['active', 'pending'])` |
| Keep specific keys only | `only(['id', 'name'])` |
| Remove specific keys | `except(['password'])` |
| Remove duplicates | `unique('email')` |

**Group & organize:**
| Need | Method |
|------|--------|
| Group by field | `groupBy('category')` |
| Group with custom key+value | `mapToGroups(fn)` |
| Split pass/fail | `partition(fn)` |
| Key by field (1 item per key) | `keyBy('id')` |
| Split into chunks | `chunk(100)` |

**Aggregate:**
| Need | Method |
|------|--------|
| Sum values | `sum('price')` |
| Average | `avg('score')` |
| Min/Max | `min('price')` / `max('price')` |
| Reduce to single value | `reduce(fn, $initial)` |
| Count occurrences | `countBy('type')` |
| Percentage matching | `percentage(fn)` |

**Combine collections:**
| Need | Method |
|------|--------|
| Merge (overwrites string keys) | `merge($other)` |
| Append values (re-indexes) | `concat($other)` |
| Keep only shared values | `intersect($other)` |
| Get values not in other | `diff($other)` |
| Pair items by index | `zip($other)` |

## Mutability Rules

**Immutable** (return new collection) - almost everything:
`map`, `filter`, `reject`, `sort`, `merge`, `pluck`, `unique`, ...

**Mutating** (modify in place, return `$this`) - memorize these:
`transform`, `push`, `prepend`, `put`, `pull`, `pop`, `shift`, `splice`, `forget`

```php
// WRONG mental model:
$filtered = $collection->push('item'); // $collection IS modified

// Correct approach when you want immutability:
$new = $collection->concat(['item']); // $collection is unchanged
```

## Common Pitfalls

### 1. `each()` vs `map()` vs `transform()`

```php
// each(): Side-effects, returns ORIGINAL collection
$users->each(fn($u) => $u->notify(new Welcome));

// map(): Transformation, returns NEW collection (original unchanged)
$names = $users->map(fn($u) => $u->name);

// transform(): Transformation, MUTATES original collection
$users->transform(fn($u) => $u->name); // $users is now a collection of names!
```

### 2. `pluck()` key overwrites

When using `pluck('name', 'id')`, duplicate keys silently overwrite:
```php
collect([
    ['id' => 1, 'name' => 'Alice'],
    ['id' => 1, 'name' => 'Bob'],   // Overwrites Alice
])->pluck('name', 'id');
// [1 => 'Bob']  -- Alice is lost!
```
Use `groupBy` if duplicates are expected.

### 3. `filter()` without callback removes all falsy values

```php
collect([0, 1, '', 'hello', null, false, []])->filter()->all();
// [1, 'hello'] -- 0, '', null, false, [] are ALL removed
```
Use `whereNotNull()` if you only want to remove nulls.

### 4. N+1 queries with collection iteration

```php
// BAD: N+1 queries
$users->each(fn($user) => $user->posts->count());

// GOOD: Eager load first
$users->load('posts');
$users->each(fn($user) => $user->posts->count());
```

### 5. Memory with large datasets

```php
// BAD: Loads all users into memory
User::all()->each(fn($u) => process($u));

// GOOD: Constant memory with cursor
User::cursor()->each(fn($u) => process($u));

// GOOD: Chunked processing
User::chunk(1000, fn($users) => $users->each(fn($u) => process($u)));
```

### 6. `sort()` preserves keys

```php
collect([3, 1, 2])->sort()->all();
// [1 => 1, 2 => 2, 0 => 3] -- keys preserved!

collect([3, 1, 2])->sort()->values()->all();
// [1, 2, 3] -- use values() to re-index
```

## Higher-Order Messages

Proxy pattern for clean, concise collection operations:

```php
// Instead of:
$users->map(function ($user) { return $user->name; });

// Write:
$users->map->name;

// Works with methods too:
$users->each->markAsVip();
$users->sum->votes;
$users->filter->isAdmin();
$users->sortBy->name;
$users->reject->isBlocked();
$users->groupBy->department;
```

Supported on: `average`, `avg`, `contains`, `each`, `every`, `filter`, `first`, `flatMap`,
`groupBy`, `keyBy`, `map`, `max`, `min`, `partition`, `reject`, `skipUntil`, `skipWhile`,
`some`, `sortBy`, `sortByDesc`, `sum`, `takeUntil`, `takeWhile`, `unique`.

## Extending with Macros

Register custom collection methods (typically in a service provider's `boot` method):

```php
use Illuminate\Support\Collection;

Collection::macro('toUpper', function () {
    return $this->map(fn($value) => strtoupper($value));
});

// Usage
collect(['foo', 'bar'])->toUpper(); // ['FOO', 'BAR']
```

## Reference Files

- **Full method reference**: See [references/methods.md](references/methods.md) for every Collection method with signatures and descriptions
- **LazyCollection**: See [references/lazy-collections.md](references/lazy-collections.md) for LazyCollection-specific methods, usage patterns, and when to choose lazy vs eager
