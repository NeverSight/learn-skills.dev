---
name: laravel-routes-best-practices
description: Keep routes clean and focused on mapping requests to controllers; avoid business logic, validation, or database operations in route files
---

# Routes Best Practices

Keep your route files clean and focused on mapping requests to controllers. Routes should never contain business logic, validation, or database operations.

## Anti-Pattern: Business Logic in Routes

```php
// BAD: Business logic directly in routes
Route::post('/order/{order}/cancel', function (Order $order) {
    if ($order->status !== 'pending') {
        return response()->json(['error' => 'Cannot cancel'], 400);
    }

    $order->status = 'cancelled';
    $order->cancelled_at = now();
    $order->save();

    Mail::to($order->user)->send(new OrderCancelled($order));

    return response()->json(['message' => 'Order cancelled']);
});

// BAD: Validation in routes
Route::post('/users', function (Request $request) {
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
    ]);

    return User::create($validated);
});
```

## Best Practice: Clean Route Definitions

```php
// GOOD: Routes only map to controllers
Route::post('/order/{order}/cancel', [OrderController::class, 'cancel']);
Route::post('/users', [UserController::class, 'store']);

// GOOD: Use route groups for organization
Route::prefix('api/v1')->group(function () {
    Route::apiResource('orders', OrderController::class);
    Route::post('orders/{order}/cancel', [OrderController::class, 'cancel']);
});

// GOOD: Named routes for maintainability
Route::post('/order/{order}/cancel', [OrderController::class, 'cancel'])
    ->name('orders.cancel');

// GOOD: Middleware in routes, logic in controllers
Route::middleware(['auth', 'verified'])->group(function () {
    Route::resource('admin/users', AdminUserController::class);
});
```

## Controller Implementation

```php
// app/Http/Controllers/OrderController.php
class OrderController extends Controller
{
    public function __construct(
        private readonly OrderCancellationService $cancellationService
    ) {}

    public function cancel(CancelOrderRequest $request, Order $order)
    {
        $this->cancellationService->cancel($order);

        return response()->json([
            'message' => 'Order cancelled successfully'
        ]);
    }
}

// app/Http/Requests/CancelOrderRequest.php
class CancelOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('cancel', $this->route('order'));
    }

    public function rules(): array
    {
        return [
            'reason' => 'nullable|string|max:500',
        ];
    }
}
```

## Route File Organization

```php
// routes/web.php - Keep it minimal
Route::get('/', [HomeController::class, 'index']);
Route::get('/about', [PageController::class, 'about']);

require __DIR__ . '/auth.php';
require __DIR__ . '/admin.php';

// routes/admin.php - Separate concerns
Route::prefix('admin')
    ->middleware(['auth', 'admin'])
    ->name('admin.')
    ->group(function () {
        Route::get('/dashboard', [AdminDashboardController::class, 'index'])
            ->name('dashboard');
        Route::resource('users', AdminUserController::class);
    });

// routes/api.php - API routes
Route::prefix('v1')->group(function () {
    Route::apiResource('products', Api\ProductController::class);
    Route::post('products/{product}/reviews', [Api\ReviewController::class, 'store']);
});
```

## Key Principles

1. **Routes are declarations, not implementations**
   - Define the HTTP verb, path, and controller method
   - Nothing more

2. **Use route model binding**

   ```php
   // Laravel automatically resolves the Order model
   Route::put('/orders/{order}', [OrderController::class, 'update']);
   ```

3. **Group related routes**

   ```php
   Route::controller(OrderController::class)->group(function () {
       Route::get('/orders', 'index');
       Route::get('/orders/{order}', 'show');
       Route::post('/orders', 'store');
   });
   ```

4. **Use resource controllers when appropriate**

   ```php
   Route::resource('photos', PhotoController::class)
       ->only(['index', 'show'])
       ->names('gallery.photos');
   ```

5. **Leverage route caching in production**
   ```bash
   sail artisan route:cache
   ```

## Common Mistakes to Avoid

- ❌ Database queries in route closures
- ❌ Complex conditionals or loops in routes
- ❌ Direct model manipulation in routes
- ❌ Sending emails or notifications from routes
- ❌ File operations in route definitions
- ❌ API calls to external services in routes
- ❌ Session or cache manipulation in routes

## When to Use Route Closures

Route closures are acceptable only for:

- Simple static page renders
- Temporary debugging/testing (remove before committing)
- Quick prototypes (refactor to controllers before production)

```php
// Acceptable for simple static views
Route::view('/terms', 'legal.terms');
Route::view('/privacy', 'legal.privacy');

// Or simple redirects
Route::redirect('/home', '/dashboard');
Route::permanentRedirect('/old-about', '/about');
```

## Testing Routes

```php
test('order cancellation route requires authentication', function () {
    $order = Order::factory()->create();

    $response = $this->postJson("/orders/{$order->id}/cancel");

    $response->assertUnauthorized();
});

test('route names are properly defined', function () {
    expect(route('orders.cancel', ['order' => 1]))
        ->toBe('http://localhost/orders/1/cancel');
});
```

Remember: If you're writing more than one line of code in a route definition, it belongs in a controller!
