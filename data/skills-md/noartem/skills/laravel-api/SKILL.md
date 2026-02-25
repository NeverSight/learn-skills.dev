---
name: laravel-api
description: Build production-grade Laravel REST APIs using opinionated architecture patterns with Laravel best practices. Use when building, scaffoling, or reviewing Laravel APIs with specifications for stateless design, versioned endpoints, invokable controllers, Form Request DTOs, Action classes, JWT authentication, and PSR-12 code quality standards. Triggers on "build a Laravel API", "create Laravel endpoints", "add API authentication", "review Laravel API code", "refactor Laravel API", or "improve Laravel code quality".
---

# Laravel API - Steve's Architecture

Build Laravel REST APIs with clean, stateless, resource-scoped architecture.

## Quick Start

When user requests a Laravel API, follow this workflow:

1. **Understand requirements** - What resources? What operations? Authentication needed?
2. **Initialize project structure** - Set up routing, remove frontend bloat
3. **Build first resource** - Complete CRUD to establish pattern
4. **Add authentication** - JWT via PHP Open Source Saver
5. **Iterate on remaining resources** - Follow established pattern

## Core Architecture Principles

Read `references/architecture.md` for comprehensive details. Key principles:

1. **Stateless by design** - No hidden dependencies, explicit data flow
2. **Boundary-first** - Clear separation of HTTP, business logic, data layers
3. **Resource-scoped** - Routes, controllers organized by resource
4. **Version discipline** - Namespace-based versioning, HTTP Sunset headers

## Code Quality Standards

All code must follow Laravel best practices and PSR-12 standards:

1. **Preserve Functionality** - Refactorings change HOW code works, never WHAT it does
2. **Explicit Over Implicit** - Prefer clear, readable code over clever shortcuts
3. **Type Declarations** - Always use return types on methods, parameter types where beneficial
4. **Avoid Nested Ternaries** - Use match expressions, switch, or if/else for clarity
5. **Consistent Naming** - Follow PSR-12 and Laravel conventions strictly
6. **Proper Namespacing** - Organize imports logically, use full type hints

**When reviewing or refactoring code:**
- Focus on clarity and maintainability over cleverness
- Simplify complex nested logic into readable structures
- Extract magic values into named constants or config
- Remove unnecessary complexity while preserving exact behavior

## Project Structure

```
routes/api/
  routes.php              # Main entry point, version grouping
  tasks.php               # All task routes, all versions
  projects.php            # All project routes, all versions

app/Http/
  Controllers/{Resource}/V1/
    StoreController.php   # Always invokable
    IndexController.php
    ShowController.php
  Requests/{Resource}/V1/
    StoreTaskRequest.php  # Validation + payload() method
  Payloads/{Resource}/
    StoreTaskPayload.php  # Simple DTOs with toArray()
  Responses/
    JsonDataResponse.php  # Implements Responsable
    JsonErrorResponse.php
  Middleware/
    HttpSunset.php

app/Actions/{Resource}/
  CreateTask.php          # Single-purpose business logic

app/Services/             # Only when logic too complex for Actions

app/Models/
  Task.php                # HasUlids trait, simple data access
```

## Building a New Resource Endpoint

### Step 1: Model

Always use ULIDs. Keep models simple - data access only.

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

final class Task extends Model
{
    use HasFactory;
    use HasUlids;
    
    protected $fillable = [
        'title',
        'description',
        'status',
        'project_id',
    ];

    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];

    public function project(): BelongsTo
    {
        return $this->belongsTo(Project::class);
    }
}
```

### Step 2: Routes

Create resource route file at `routes/api/{resource}.php`:

```php
use App\Http\Controllers\Tasks\V1;

Route::middleware(['auth:api'])->group(function () {
    Route::get('/tasks', V1\IndexController::class);
    Route::post('/tasks', V1\StoreController::class);
    Route::get('/tasks/{task}', V1\ShowController::class);
    Route::patch('/tasks/{task}', V1\UpdateController::class);
    Route::delete('/tasks/{task}', V1\DestroyController::class);
});
```

Include in `routes/api/routes.php`:

```php
Route::prefix('v1')->group(function () {
    require __DIR__ . '/tasks.php';
});
```

### Step 3: DTO (Payload)

Create at `app/Http/Payloads/{Resource}/{Operation}Payload.php`:

```php
<?php

declare(strict_types=1);

namespace App\Http\Payloads\Tasks;

final readonly class StoreTaskPayload
{
    public function __construct(
        public string $title,
        public ?string $description,
        public string $status,
        public string $projectId,
    ) {}

    public function toArray(): array
    {
        return [
            'title' => $this->title,
            'description' => $this->description,
            'status' => $this->status,
            'project_id' => $this->projectId,
        ];
    }
}
```

### Step 4: Form Request

Create at `app/Http/Requests/{Resource}/V1/{Operation}Request.php`:

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\Tasks\V1;

use App\Http\Payloads\Tasks\StoreTaskPayload;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

final class StoreTaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:1000'],
            'status' => ['required', Rule::in(['pending', 'in_progress', 'completed'])],
            'project_id' => ['required', 'string', 'exists:projects,id'],
        ];
    }

    public function payload(): StoreTaskPayload
    {
        return new StoreTaskPayload(
            title: $this->string('title')->toString(),
            description: $this->string('description')->toString(),
            status: $this->string('status')->toString(),
            projectId: $this->string('project_id')->toString(),
        );
    }
}
```

### Step 5: Action

Create at `app/Actions/{Resource}/{Operation}.php`:

```php
<?php

declare(strict_types=1);

namespace App\Actions\Tasks;

use App\Http\Payloads\Tasks\StoreTaskPayload;
use App\Models\Task;

final readonly class CreateTask
{
    public function handle(StoreTaskPayload $payload): Task
    {
        return Task::create($payload->toArray());
    }
}
```

### Step 6: Controller

Create invokable controller at `app/Http/Controllers/{Resource}/V1/{Operation}Controller.php`:

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Tasks\V1;

use App\Actions\Tasks\CreateTask;
use App\Http\Requests\Tasks\V1\StoreTaskRequest;
use App\Http\Responses\JsonDataResponse;
use Illuminate\Http\JsonResponse;

final readonly class StoreController
{
    public function __construct(
        private CreateTask $createTask,
    ) {}

    public function __invoke(StoreTaskRequest $request): JsonResponse
    {
        $task = $this->createTask->handle(
            payload: $request->payload(),
        );

        return new JsonDataResponse(
            data: $task,
            status: 201,
        );
    }
}
```

## Response Format

Standard format for all responses:

**Success:**
```json
{
    "data": {...},
    "meta": {...}
}
```

**Error (Problem+JSON):**
```json
{
    "type": "about:blank",
    "title": "Validation Failed",
    "status": 422,
    "detail": "The given data was invalid",
    "errors": {...}
}
```

## Query Building

Use Spatie Query Builder for filtering, sorting, includes:

```php
use Spatie\QueryBuilder\QueryBuilder;

$tasks = QueryBuilder::for(Task::class)
    ->allowedFilters(['status', 'priority'])
    ->allowedSorts(['created_at', 'due_date'])
    ->allowedIncludes(['project', 'assignee'])
    ->paginate();
```

## Versioning Endpoints

When creating V2:

1. Create V2 namespace: `App\Http\Controllers\Tasks\V2\`
2. Add V2 route group in resource file
3. Add Sunset middleware to V1 routes:

```php
Route::middleware(['auth:api', 'http.sunset:2025-12-31'])->group(function () {
    // V1 routes
});
```

## Authentication Setup

Use PHP Open Source Saver JWT package:

```bash
composer require php-open-source-saver/jwt-auth
php artisan vendor:publish --provider="PHPOpenSourceSaver\JWTAuth\Providers\LaravelServiceProvider"
php artisan jwt:secret
```

Configure in `config/auth.php`:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

## Essential Setup

Add to `app/Providers/AppServiceProvider.php`:

```php
use Illuminate\Database\Eloquent\Model;

public function boot(): void
{
    Model::shouldBeStrict(); // Prevent N+1 queries
}
```

Register HttpSunset middleware in `app/Http/Kernel.php`:

```php
protected $middlewareAliases = [
    'http.sunset' => \App\Http\Middleware\HttpSunset::class,
];
```

## Anti-Patterns to Avoid

- Using auto-increment IDs instead of ULIDs
- Business logic in models
- Multiple actions per controller
- Accessing request data directly in controllers/actions
- Hidden query scopes
- Service classes when an Action would suffice
- Breaking changes without versioning
- Inconsistent response formats
- Nested ternary operators (use match expressions instead)
- Missing type declarations on methods and parameters
- Overly compact "clever" code that sacrifices readability

## Code Review & Refactoring

When reviewing or refactoring Laravel API code, apply these principles:

### Simplification Checklist

1. **Preserve Functionality** - Ensure refactorings don't change behavior
2. **Check Type Safety** - Add missing return types and parameter types
3. **Simplify Logic** - Replace nested ternaries with match expressions
4. **Extract Complexity** - Move complex conditions into named methods
5. **Verify Standards** - Ensure PSR-12 compliance with declare(strict_types=1)
6. **Improve Naming** - Use descriptive names that reveal intent

### Match Expression Pattern

Replace nested ternaries with match for clarity:

```php
// ❌ Avoid: Nested ternary
$status = $task->completed_at 
    ? ($task->verified ? 'verified' : 'completed')
    : ($task->started_at ? 'in_progress' : 'pending');

// ✅ Prefer: Match expression
$status = match (true) {
    $task->completed_at && $task->verified => 'verified',
    $task->completed_at => 'completed',
    $task->started_at => 'in_progress',
    default => 'pending',
};
```

## References

- **architecture.md** - Comprehensive architectural patterns and principles
- **code-examples.md** - Complete working examples for every component
- **code-quality.md** - Laravel best practices, refactoring patterns, and PSR-12 standards

## Templates

Template files in `assets/templates/` for quick scaffolding:
- Controller.php
- FormRequest.php
- Payload.php
- Action.php
- Model.php