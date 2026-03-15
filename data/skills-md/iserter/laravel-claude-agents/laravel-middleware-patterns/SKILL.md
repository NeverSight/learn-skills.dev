---
name: laravel-middleware-patterns
description: Best practices for Laravel middleware including before/after patterns, terminable middleware, groups, parameters, and common middleware implementations.
---

# Middleware Patterns

## Creating Middleware

```bash
php artisan make:middleware EnsureUserIsSubscribed
```

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            return redirect('billing');
        }

        return $next($request);
    }
}
```

## Before vs After vs Terminable Patterns

### Before Middleware

```php
// ✅ Runs before the request hits the controller
class CheckAge
{
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->age < 18) {
            abort(403, 'Underage access denied.');
        }

        return $next($request);
    }
}
```

### After Middleware

```php
// ✅ Runs after the response is generated
class AddSecurityHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');

        return $response;
    }
}
```

### Terminable Middleware

```php
// ✅ Runs after the response has been sent to the browser
class LogRequest
{
    public function handle(Request $request, Closure $next): Response
    {
        $request->attributes->set('start_time', microtime(true));

        return $next($request);
    }

    public function terminate(Request $request, Response $response): void
    {
        $duration = microtime(true) - $request->attributes->get('start_time');

        Log::info('Request completed', [
            'url' => $request->fullUrl(),
            'method' => $request->method(),
            'status' => $response->getStatusCode(),
            'duration_ms' => round($duration * 1000, 2),
        ]);
    }
}
```

## Registering Middleware in bootstrap/app.php

```php
<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {

        // Global middleware (runs on every request)
        $middleware->append(App\Http\Middleware\AddSecurityHeaders::class);
        $middleware->prepend(App\Http\Middleware\TrustProxies::class);

        // Middleware aliases
        $middleware->alias([
            'subscribed' => App\Http\Middleware\EnsureUserIsSubscribed::class,
            'role' => App\Http\Middleware\EnsureUserHasRole::class,
            'locale' => App\Http\Middleware\SetLocale::class,
            'tenant' => App\Http\Middleware\ResolveTenant::class,
        ]);

        // Append to existing groups
        $middleware->appendToGroup('web', [
            App\Http\Middleware\SetLocale::class,
        ]);

        // Define custom groups
        $middleware->group('admin', [
            'auth',
            'role:admin',
            App\Http\Middleware\LogAdminActions::class,
        ]);

        // Middleware priority (execution order)
        $middleware->priority([
            App\Http\Middleware\ResolveTenant::class,
            \Illuminate\Auth\Middleware\Authenticate::class,
            App\Http\Middleware\EnsureUserHasRole::class,
        ]);
    })
    ->create();
```

## Middleware Parameters

```php
class EnsureUserHasRole
{
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (! $request->user()?->hasAnyRole($roles)) {
            abort(403, 'Insufficient permissions.');
        }

        return $next($request);
    }
}
```

### Using Middleware Parameters in Routes

```php
// Single parameter
Route::get('/admin', AdminController::class)
    ->middleware('role:admin');

// Multiple parameters
Route::get('/dashboard', DashboardController::class)
    ->middleware('role:admin,editor');

// ✅ Using class reference with parameters
Route::get('/dashboard', DashboardController::class)
    ->middleware(EnsureUserHasRole::class.':admin,editor');
```

## Middleware Groups

```php
// ✅ Apply group to routes
Route::middleware('admin')->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'dashboard']);
    Route::get('/admin/users', [AdminController::class, 'users']);
});

// ✅ Multiple middleware
Route::middleware(['auth', 'subscribed', 'role:premium'])->group(function () {
    Route::get('/premium/content', PremiumContentController::class);
});
```

## Excluding Middleware

```php
// ✅ Exclude middleware on a specific route
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
    Route::get('/public-page', PublicPageController::class)
        ->withoutMiddleware('auth');
});

// ✅ Exclude from controller
class PublicController extends Controller
{
    public static function middleware(): array
    {
        return [
            new \Illuminate\Routing\Controllers\Middleware('auth', except: ['index', 'show']),
        ];
    }
}
```

## Controller Middleware

```php
use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class PostController extends Controller implements HasMiddleware
{
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('subscribed', only: ['create', 'store']),
            new Middleware('role:editor', except: ['index', 'show']),
        ];
    }
}
```

## Common Middleware Patterns

### Rate Limiting

```php
// bootstrap/app.php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

->withMiddleware(function (Middleware $middleware) {
    // Rate limiter is configured in AppServiceProvider
})

// AppServiceProvider
public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });

    RateLimiter::for('uploads', function (Request $request) {
        return Limit::perMinute(5)->by($request->user()->id);
    });
}
```

```php
// Usage in routes
Route::middleware('throttle:api')->group(function () {
    Route::apiResource('posts', PostController::class);
});

Route::post('/upload', UploadController::class)
    ->middleware('throttle:uploads');
```

### Locale Middleware

```php
class SetLocale
{
    public function handle(Request $request, Closure $next): Response
    {
        $locale = $request->header('Accept-Language')
            ?? $request->user()?->preferred_locale
            ?? config('app.locale');

        if (in_array($locale, config('app.supported_locales', ['en']))) {
            app()->setLocale($locale);
        }

        return $next($request);
    }
}
```

### Tenant Scoping

```php
class ResolveTenant
{
    public function handle(Request $request, Closure $next): Response
    {
        $tenant = Tenant::where('domain', $request->getHost())->first();

        if (! $tenant) {
            abort(404, 'Tenant not found.');
        }

        app()->instance(Tenant::class, $tenant);

        // Set tenant context for queries
        config(['database.connections.tenant.database' => $tenant->database]);

        return $next($request);
    }

    public function terminate(Request $request, Response $response): void
    {
        // Clean up tenant context
        app()->forgetInstance(Tenant::class);
    }
}
```

### CORS Middleware

```php
class HandleCors
{
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->isMethod('OPTIONS')) {
            $response = response('', 204);
        } else {
            $response = $next($request);
        }

        $response->headers->set('Access-Control-Allow-Origin', config('cors.allowed_origins', '*'));
        $response->headers->set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        $response->headers->set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        $response->headers->set('Access-Control-Max-Age', '86400');

        return $response;
    }
}
```

### Cache Response Middleware

```php
class CacheResponse
{
    public function handle(Request $request, Closure $next, int $minutes = 60): Response
    {
        if ($request->method() !== 'GET') {
            return $next($request);
        }

        $key = 'response_' . sha1($request->fullUrl());

        return Cache::remember($key, now()->addMinutes($minutes), function () use ($next, $request) {
            return $next($request);
        });
    }
}
```

```php
// Usage
Route::get('/static-page', StaticPageController::class)
    ->middleware(CacheResponse::class.':30');
```

## Best Practices

```php
// ✅ Keep middleware focused on a single responsibility
class EnsureEmailIsVerified { /* only checks email verification */ }
class EnsureUserIsSubscribed { /* only checks subscription */ }

// ❌ Don't combine unrelated concerns in one middleware
class CheckEverything { /* checks auth + subscription + role + locale */ }

// ✅ Use class references instead of string aliases for type safety
Route::middleware(EnsureUserHasRole::class.':admin')->group(function () {
    // ...
});

// ✅ Return early to avoid deep nesting
public function handle(Request $request, Closure $next): Response
{
    if (! $request->user()) {
        return redirect('login');
    }

    return $next($request);
}

// ❌ Avoid modifying the request object extensively
// Use form requests or controller logic for complex input manipulation
```

## Checklist

- [ ] Middleware has a single, clear responsibility
- [ ] Before/after/terminable pattern chosen correctly for the use case
- [ ] Middleware registered in `bootstrap/app.php`
- [ ] Aliases defined for frequently used middleware
- [ ] Middleware parameters used for configurable behavior
- [ ] Groups created for commonly combined middleware
- [ ] `withoutMiddleware()` used for route-level exclusions
- [ ] Rate limiting configured for API and sensitive endpoints
- [ ] Controller middleware uses `HasMiddleware` interface
- [ ] Terminable middleware used for post-response tasks (logging, cleanup)
- [ ] Middleware priority set for execution order dependencies
