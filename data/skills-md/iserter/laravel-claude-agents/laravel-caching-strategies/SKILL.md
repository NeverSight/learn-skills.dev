---
name: laravel-caching-strategies
description: Best practices for Laravel caching including cache patterns, tags, atomic locks, flexible cache, and cache invalidation strategies.
---

# Laravel Caching Strategies

## Core Cache Patterns

```php
use Illuminate\Support\Facades\Cache;

// ✅ remember - cache for a duration
$users = Cache::remember('users:active', now()->addMinutes(30), function () {
    return User::where('active', true)->get();
});

// ✅ rememberForever - cache until manually cleared
$settings = Cache::rememberForever('app:settings', function () {
    return Setting::all()->pluck('value', 'key');
});

// ✅ flexible - stale-while-revalidate pattern
// Fresh for 5 min, serves stale for up to 15 min while revalidating in background
$stats = Cache::flexible('dashboard:stats', [300, 900], function () {
    return DashboardStats::calculate();
});

// ✅ put / get / forget
Cache::put('key', $value, now()->addHours(1));
$value = Cache::get('key', 'default');
Cache::forget('key');

// ❌ Querying the database when cache would suffice
$settings = Setting::all(); // Every request hits the DB
```

## Cache Tags for Grouped Invalidation

```php
// ✅ Tag related cache entries
Cache::tags(['posts', 'users'])->put("user:{$userId}:posts", $posts, 3600);
Cache::tags(['posts'])->put("post:{$postId}", $post, 3600);
Cache::tags(['users'])->put("user:{$userId}:profile", $profile, 3600);

// ✅ Flush all caches for a tag group
Cache::tags(['posts'])->flush(); // Clears all post-related caches

// ✅ Retrieve tagged cache
$posts = Cache::tags(['posts', 'users'])->get("user:{$userId}:posts");

// Note: Cache tags are only supported by redis and memcached drivers
```

## Atomic Locks

```php
use Illuminate\Support\Facades\Cache;

// ✅ Prevent concurrent execution
$lock = Cache::lock('processing:order:' . $orderId, 10); // 10 second lock

if ($lock->get()) {
    try {
        // Process order exclusively
        $this->processOrder($orderId);
    } finally {
        $lock->release();
    }
}

// ✅ Block and wait for lock (up to 5 seconds)
$lock = Cache::lock('report:generate', 30);

$lock->block(5, function () {
    // Acquired lock, do work
    $this->generateReport();
}); // Lock auto-released after closure

// ✅ Cross-process lock with owner token
$lock = Cache::lock('deployment', 120);

if ($lock->get()) {
    $owner = $lock->owner();
    // Pass $owner to another process
}

// In the other process
Cache::restoreLock('deployment', $owner)->release();

// ❌ Forgetting to release locks
$lock->get();
$this->doWork(); // If this throws, lock is never released
```

## Cache Memoization

```php
use Illuminate\Support\Facades\Cache;

// ✅ memo - in-memory cache for the current request lifecycle
// Avoids repeated cache store lookups within the same request
$config = Cache::memo('app:config', function () {
    return Config::loadFromDatabase();
});

// Subsequent calls return the in-memory value without hitting Redis/Memcached
$config = Cache::memo('app:config', fn () => Config::loadFromDatabase());
```

## Model Caching Patterns

```php
class Product extends Model
{
    // ✅ Cache on read with automatic invalidation
    public static function findCached(int $id): ?self
    {
        return Cache::remember(
            "product:{$id}",
            now()->addHour(),
            fn () => static::find($id)
        );
    }

    // ✅ Invalidate cache on model changes
    protected static function booted(): void
    {
        static::saved(function (Product $product) {
            Cache::forget("product:{$product->id}");
            Cache::tags(['products'])->flush();
        });

        static::deleted(function (Product $product) {
            Cache::forget("product:{$product->id}");
            Cache::tags(['products'])->flush();
        });
    }
}

// ✅ Cache query results with tags for group invalidation
class ProductService
{
    public function getFeatured(): Collection
    {
        return Cache::tags(['products'])->remember(
            'products:featured',
            now()->addMinutes(30),
            fn () => Product::where('featured', true)->with('category')->get()
        );
    }
}
```

## Cache Key Conventions

```php
// ✅ Use consistent, descriptive key patterns
"user:{$userId}:profile"
"post:{$postId}:comments:page:{$page}"
"tenant:{$tenantId}:settings"
"api:github:repos:{$username}"
"report:daily:{$date}"

// ✅ Include cache-busting identifiers when data shape changes
"v2:user:{$userId}:profile"

// ❌ Vague or collision-prone keys
"data"
"user"
"temp"
"cache_1"
```

## Common Pitfalls

```php
// ❌ Caching null results without handling them
$user = Cache::remember("user:{$id}", 3600, fn () => User::find($id));
// If user doesn't exist, null is cached for an hour

// ✅ Handle null explicitly
$user = Cache::remember("user:{$id}", 3600, function () use ($id) {
    return User::find($id) ?? new NullUser();
});

// ❌ No invalidation strategy
Cache::forever('products:all', Product::all());
// Data becomes stale with no way to refresh

// ✅ Use TTL or event-based invalidation
Cache::remember('products:all', now()->addMinutes(15), fn () => Product::all());

// ❌ Caching too aggressively (serialization cost > query cost)
Cache::remember('user:count', 3600, fn () => User::count());
// Simple COUNT queries are often fast enough without caching

// ✅ Cache expensive operations
Cache::remember('dashboard:analytics', 3600, function () {
    return DB::table('orders')
        ->selectRaw('DATE(created_at) as date, SUM(total) as revenue')
        ->groupByRaw('DATE(created_at)')
        ->orderBy('date')
        ->get();
});

// ❌ Cache stampede - many requests regenerate cache simultaneously
// ✅ Use flexible() for stale-while-revalidate or atomic locks for regeneration
```

## Checklist

- [ ] remember/rememberForever used instead of manual get/put
- [ ] flexible() used for high-traffic keys that tolerate brief staleness
- [ ] Cache tags used for grouped invalidation (Redis/Memcached only)
- [ ] Atomic locks used for exclusive operations
- [ ] Model caches invalidated on save/delete events
- [ ] Cache keys follow a consistent naming convention
- [ ] TTLs set appropriately (not too long, not too short)
- [ ] Null/empty results handled to avoid caching nothing
- [ ] Expensive queries cached, trivial queries left uncached
- [ ] Cache stampede prevented with flexible() or locks
