---
name: laravel-feature-flags
description: Best practices for Laravel Pennant feature flags including defining features, checking activation, scoping, rich values for A/B testing, and gradual rollouts.
---

# Feature Flags with Laravel Pennant

## Installing Pennant

```bash
composer require laravel/pennant
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
php artisan migrate
```

## Defining Features

### Closure-Based Features

```php
<?php

// app/Providers/AppServiceProvider.php
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

public function boot(): void
{
    // Simple boolean feature
    Feature::define('new-dashboard', function () {
        return true;
    });

    // Scoped to the authenticated user
    Feature::define('beta-access', function (User $user) {
        return $user->is_beta_tester;
    });

    // Gradual rollout with lottery
    Feature::define('redesigned-checkout', function (User $user) {
        return Lottery::odds(1, 10); // 10% of users
    });

    // Based on user attributes
    Feature::define('premium-features', function (User $user) {
        return $user->subscribed('premium');
    });
}
```

### Class-Based Features

```bash
php artisan pennant:feature NewOnboarding
```

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewOnboarding
{
    // Resolve the feature's initial value
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternal() => true,
            $user->created_at->isAfter('2025-01-01') => true,
            default => Lottery::odds(1, 5),
        };
    }
}
```

```php
// Usage with class-based features
Feature::active(NewOnboarding::class); // for the authenticated user
Feature::for($user)->active(NewOnboarding::class);
```

## Checking Features

### Basic Checks

```php
use Laravel\Pennant\Feature;

// ✅ Check if active
if (Feature::active('new-dashboard')) {
    // Show new dashboard
}

// ✅ Check if inactive
if (Feature::inactive('new-dashboard')) {
    // Show old dashboard
}

// ✅ Check multiple features
if (Feature::allAreActive(['new-dashboard', 'beta-access'])) {
    // All features are active
}

if (Feature::someAreActive(['feature-a', 'feature-b'])) {
    // At least one is active
}

if (Feature::allAreInactive(['deprecated-feature', 'old-ui'])) {
    // None of these are active
}

if (Feature::someAreInactive(['feature-a', 'feature-b'])) {
    // At least one is inactive
}
```

### Getting Values

```php
// Get the resolved value (may not be boolean)
$value = Feature::value('purchase-button');

// Get values for multiple features
$values = Feature::values(['feature-a', 'feature-b']);
// ['feature-a' => true, 'feature-b' => 'variant-b']
```

## Feature Scoping

### User Scoping

```php
// Check for the currently authenticated user (default)
Feature::active('beta-access');

// Check for a specific user
Feature::for($user)->active('beta-access');

// Check for multiple users
$users = User::where('role', 'admin')->get();
Feature::for($users)->active('beta-access');
```

### Team / Custom Scoping

```php
// Define a team-scoped feature
Feature::define('team-billing-v2', function (Team $team) {
    return $team->plan === 'enterprise';
});

// Check for a specific team
Feature::for($team)->active('team-billing-v2');
```

### Nullable Scope

```php
// Define a feature with nullable scope (for guests)
Feature::define('maintenance-banner', function (User|null $user) {
    return config('app.show_maintenance_banner');
});

// Check without authentication
Feature::for(null)->active('maintenance-banner');
```

## Rich Values for A/B Testing

```php
// Define a feature with rich values
Feature::define('purchase-button', function (User $user) {
    return Lottery::odds(1, 3)->choose(
        fn () => 'blue-button',   // 33%
        fn () => 'green-button',  // 67% (default)
    );
});

// Alternative: deterministic assignment
Feature::define('purchase-button', function (User $user) {
    return match ($user->id % 3) {
        0 => 'blue-button',
        1 => 'green-button',
        2 => 'red-button',
    };
});
```

```blade
{{-- Using rich values in views --}}
@php $variant = Feature::value('purchase-button') @endphp

@if ($variant === 'blue-button')
    <button class="bg-blue-600 text-white">Buy Now</button>
@elseif ($variant === 'green-button')
    <button class="bg-green-600 text-white">Buy Now</button>
@else
    <button class="bg-red-600 text-white">Buy Now</button>
@endif
```

## Conditional Execution

```php
// ✅ Execute code based on feature state
Feature::when('new-dashboard',
    fn () => $this->renderNewDashboard(),
    fn () => $this->renderOldDashboard(),
);

// ✅ With rich values
Feature::when('purchase-button',
    fn ($variant) => view('buttons.' . $variant),
    fn () => view('buttons.default'),
);

// ✅ Unless (inverse)
Feature::unless('legacy-mode',
    fn () => $this->useModernApi(),
    fn () => $this->useLegacyApi(),
);
```

## Blade Directives

```blade
{{-- ✅ Basic feature check --}}
@feature('new-dashboard')
    <x-new-dashboard :user="$user" />
@else
    <x-legacy-dashboard :user="$user" />
@endfeature

{{-- ✅ Class-based feature --}}
@feature(App\Features\NewOnboarding::class)
    <x-new-onboarding-wizard />
@endfeature

{{-- ✅ Combine with other directives --}}
@auth
    @feature('premium-features')
        <x-premium-sidebar />
    @else
        <x-standard-sidebar />
    @endfeature
@endauth
```

## Middleware

```php
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

// In routes
Route::get('/new-dashboard', NewDashboardController::class)
    ->middleware(EnsureFeaturesAreActive::using('new-dashboard'));

// Multiple features required
Route::get('/beta', BetaController::class)
    ->middleware(EnsureFeaturesAreActive::using('beta-access', 'new-dashboard'));

// In route groups
Route::middleware([
    'auth',
    EnsureFeaturesAreActive::using('beta-access'),
])->group(function () {
    Route::get('/beta/dashboard', [BetaController::class, 'dashboard']);
    Route::get('/beta/settings', [BetaController::class, 'settings']);
});
```

### Custom Response for Inactive Features

```php
// In AppServiceProvider
use Symfony\Component\HttpKernel\Exception\HttpException;

public function boot(): void
{
    // Redirect when feature is inactive
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return redirect()->route('dashboard')
                ->with('warning', 'This feature is not available.');
        }
    );
}
```

## Activating and Deactivating Programmatically

```php
// Activate for a specific user
Feature::for($user)->activate('new-dashboard');

// Activate with a specific value
Feature::for($user)->activate('purchase-button', 'green-button');

// Activate for all users
Feature::activateForEveryone('new-dashboard');

// Activate for everyone with a value
Feature::activateForEveryone('purchase-button', 'blue-button');

// Deactivate for a specific user
Feature::for($user)->deactivate('new-dashboard');

// Deactivate for everyone
Feature::deactivateForEveryone('new-dashboard');

// Forget stored value (will be re-resolved next check)
Feature::for($user)->forget('new-dashboard');

// Purge all stored values for a feature
Feature::purge('new-dashboard');

// Purge all features
Feature::purge();
```

### Bulk Updates

```php
// Activate for a group of users
$betaUsers = User::where('is_beta_tester', true)->get();

foreach ($betaUsers as $user) {
    Feature::for($user)->activate('new-dashboard');
}
```

## Eager Loading Features

```php
// ✅ Eager load features to avoid repeated queries
Feature::for($user)->load(['new-dashboard', 'beta-access', 'premium-features']);

// ✅ Load all defined features
Feature::for($user)->loadAll();

// Then check without additional queries
if (Feature::active('new-dashboard')) { /* ... */ }
if (Feature::active('beta-access')) { /* ... */ }
```

## Updating Stored Values

```php
// ✅ Check and store the initial value
Feature::active('new-dashboard'); // Resolves and stores

// ✅ Later, get the latest resolved value (ignoring stored)
$fresh = Feature::for($user)->value('new-dashboard');
```

## In-Memory Driver (for Testing or Stateless)

```php
// config/pennant.php
'default' => env('PENNANT_STORE', 'database'),

'stores' => [
    'array' => [
        'driver' => 'array',
    ],
    'database' => [
        'driver' => 'database',
        'connection' => null,
        'table' => 'features',
    ],
],
```

## Testing Feature Flags

```php
use Laravel\Pennant\Feature;

public function test_new_dashboard_is_shown_when_feature_active(): void
{
    // Activate the feature for the test
    Feature::activate('new-dashboard');

    $response = $this->actingAs($this->user)
        ->get('/dashboard');

    $response->assertSee('New Dashboard');
}

public function test_old_dashboard_is_shown_when_feature_inactive(): void
{
    // Deactivate the feature for the test
    Feature::deactivate('new-dashboard');

    $response = $this->actingAs($this->user)
        ->get('/dashboard');

    $response->assertSee('Classic Dashboard');
}

public function test_rich_value_determines_button_variant(): void
{
    Feature::for($this->user)->activate('purchase-button', 'green-button');

    $response = $this->actingAs($this->user)
        ->get('/shop');

    $response->assertSee('bg-green-600');
}

public function test_feature_middleware_blocks_inactive_features(): void
{
    Feature::deactivate('beta-access');

    $response = $this->actingAs($this->user)
        ->get('/beta/dashboard');

    $response->assertStatus(400);
}

public function test_gradual_rollout_is_consistent(): void
{
    // Features are stored after first resolution, so they stay consistent
    $firstCheck = Feature::for($this->user)->active('redesigned-checkout');
    $secondCheck = Feature::for($this->user)->active('redesigned-checkout');

    $this->assertEquals($firstCheck, $secondCheck);
}
```

### Using Array Driver in Tests

```php
// phpunit.xml or .env.testing
// PENNANT_STORE=array

// Or in test setup
protected function setUp(): void
{
    parent::setUp();
    Feature::store('array');
}
```

## Checklist

- [ ] Pennant installed and migrations run
- [ ] Features defined with clear, descriptive names
- [ ] Closure-based features used for simple flags
- [ ] Class-based features used for complex resolution logic
- [ ] Feature scoping matches business domain (user, team, etc.)
- [ ] Rich values used for A/B testing variants
- [ ] `@feature` Blade directive used in templates
- [ ] `EnsureFeaturesAreActive` middleware guards feature-gated routes
- [ ] Features eager loaded to prevent repeated queries
- [ ] Programmatic activation/deactivation used for admin controls
- [ ] Tests use `Feature::activate()` / `Feature::deactivate()` for deterministic behavior
- [ ] Array driver used in test environment for speed
- [ ] Old features purged after full rollout
