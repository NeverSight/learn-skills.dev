---
name: laravel-authorization-patterns
description: Best practices for Laravel authorization including Gates, Policies, middleware auth, and Blade directives for access control.
---

# Laravel Authorization Patterns

## Gates for General Ability Checks

```php
// In AuthServiceProvider or AppServiceProvider boot()
use Illuminate\Support\Facades\Gate;

Gate::define('access-admin', function (User $user) {
    return $user->is_admin;
});

Gate::define('manage-settings', function (User $user) {
    return $user->hasRole('admin');
});

// Usage
if (Gate::allows('access-admin')) {
    // ...
}

// ✅ Abort if unauthorized
Gate::authorize('access-admin'); // Throws AuthorizationException

// ✅ Check for specific user
Gate::forUser($otherUser)->allows('access-admin');
```

## Policies for Model-Based Authorization

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

class PostPolicy
{
    // Runs before all other checks - return null to fall through
    public function before(User $user, string $ability): ?bool
    {
        if ($user->is_super_admin) {
            return true;
        }

        return null; // Fall through to specific method
    }

    public function viewAny(User $user): bool
    {
        return true;
    }

    public function view(User $user, Post $post): bool
    {
        return $post->is_published || $user->id === $post->user_id;
    }

    public function create(User $user): bool
    {
        return $user->hasVerifiedEmail();
    }

    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post): Response
    {
        if ($user->id !== $post->user_id) {
            return Response::deny('You do not own this post.');
        }

        if ($post->is_published) {
            return Response::denyWithStatus(403, 'Published posts cannot be deleted.');
        }

        return Response::allow();
    }
}
```

Policies are auto-discovered when they follow the `App\Policies\{Model}Policy` convention.

## Response Objects

```php
use Illuminate\Auth\Access\Response;

// ✅ Rich authorization responses
public function publish(User $user, Post $post): Response
{
    if (! $user->hasVerifiedEmail()) {
        return Response::denyWithStatus(403, 'Verify your email first.');
    }

    if ($post->user_id !== $user->id) {
        return Response::denyAsNotFound(); // Returns 404 instead of 403
    }

    return Response::allow();
}

// Inspecting responses without exceptions
$response = Gate::inspect('publish', $post);

if ($response->allowed()) {
    // Publish the post
} else {
    echo $response->message();
}
```

## Middleware Authorization

```php
// ✅ Route-level authorization
Route::put('/posts/{post}', [PostController::class, 'update'])
    ->can('update', 'post');

Route::resource('posts', PostController::class)
    ->middleware('can:viewAny,App\Models\Post')
    ->only(['index']);

// ✅ Route group with gate
Route::middleware('can:access-admin')->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'index']);
    Route::get('/admin/users', [AdminController::class, 'users']);
});
```

## Blade Directives

```php
{{-- ✅ Single ability check --}}
@can('update', $post)
    <a href="{{ route('posts.edit', $post) }}">Edit</a>
@endcan

{{-- ✅ Multiple abilities --}}
@canany(['update', 'delete'], $post)
    <div class="actions">
        @can('update', $post)
            <button>Edit</button>
        @endcan
        @can('delete', $post)
            <button>Delete</button>
        @endcan
    </div>
@endcanany

{{-- ✅ Inverse check --}}
@cannot('create', App\Models\Post::class)
    <p>You do not have permission to create posts.</p>
@endcannot

{{-- ✅ Gate check --}}
@can('access-admin')
    <a href="/admin">Admin Panel</a>
@endcan
```

## Form Request authorize() Integration

```php
class UpdatePostRequest extends FormRequest
{
    // ✅ Combine validation with authorization
    public function authorize(): bool
    {
        return $this->user()->can('update', $this->route('post'));
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
        ];
    }
}
```

## Controller Authorization

```php
class PostController extends Controller
{
    public function index()
    {
        // ✅ Authorize against model class
        $this->authorize('viewAny', Post::class);

        return Post::paginate();
    }

    public function update(UpdatePostRequest $request, Post $post)
    {
        // ✅ Authorize against model instance
        $this->authorize('update', $post);

        $post->update($request->validated());

        return new PostResource($post);
    }

    // ❌ Don't check authorization with manual if statements
    public function destroy(Post $post)
    {
        if (auth()->id() !== $post->user_id) {
            abort(403);
        }
        // Skips policy, no reuse, harder to test
    }

    // ✅ Use policy
    public function destroy(Post $post)
    {
        $this->authorize('delete', $post);

        $post->delete();

        return response()->noContent();
    }
}
```

## Testing Authorization

```php
use Illuminate\Support\Facades\Gate;

// ✅ Test policy methods directly
public function test_user_can_update_own_post(): void
{
    $user = User::factory()->create();
    $post = Post::factory()->for($user)->create();

    $this->assertTrue($user->can('update', $post));
}

public function test_user_cannot_update_others_post(): void
{
    $user = User::factory()->create();
    $post = Post::factory()->create(); // Different user

    $this->assertFalse($user->can('update', $post));
}

// ✅ Test via HTTP
public function test_unauthorized_user_gets_403(): void
{
    $user = User::factory()->create();
    $post = Post::factory()->create();

    $this->actingAs($user)
        ->putJson("/api/posts/{$post->id}", ['title' => 'New Title'])
        ->assertForbidden();
}

// ✅ Bypass authorization in other tests
public function test_post_update_logic(): void
{
    Gate::before(fn () => true); // Allow everything

    // Test business logic without auth concerns
}
```

## Checklist

- [ ] Gates used for general abilities not tied to a model
- [ ] Policies used for all model-based authorization
- [ ] Policies follow auto-discovery naming convention
- [ ] before() returns null to fall through (not false)
- [ ] Response objects used for detailed denial messages
- [ ] Authorization applied via middleware, Form Request, or controller
- [ ] Blade directives used for conditional UI rendering
- [ ] No manual if/abort(403) checks bypassing policies
- [ ] Authorization logic tested for allowed and denied cases
- [ ] Gate::inspect() used when response message is needed
