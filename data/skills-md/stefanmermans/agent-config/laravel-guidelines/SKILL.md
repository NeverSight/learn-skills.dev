---
name: laravel-guidelines
description: When dealing with a Laravel project, these guidelines must always be followed.
---

# Laravel Guidelines

This document outlines best practices for building robust, maintainable, and modern Laravel applications. Focus is placed on clean architecture, efficient database usage, and reliable testing strategies.

## 1. General Principles

- **Correctness > Clarity > Consistency > Performance > Cleverness**.
- **KISS**: Keep It Simple, Stupid. Avoid over-engineering.
- **DRY (Don't Repeat Yourself)**: Extract shared logic but be pragmatic. Duplication is cheaper than the wrong abstraction.
- **SOLID**: Adhere to SOLID principles, with particular emphasis on **Single Responsibility (SRP)** in classes and methods.
- **Strict Typing**: Use PHP's strict typing (`declare(strict_types=1);`) to ensure type safety.
- **Config/Env**: Prefer `config()` and `.env` variables over hardcoded strings to ensure flexibility across environments.

## 2. Modern PHP Features

Leverage modern PHP features (8.1/8.2+) for cleaner, more expressive code:

- **Constructor Property Promotion**: Reduce boilerplate in DTOs and Services.
- **Readonly Properties**: Ensure immutability for value objects and DTOs.
- **Enums**: Use backed Enums for status fields and categories instead of constants or magic strings.
- **Match Expressions**: Use `match` instead of complex `switch` or `if/else` chains.
- **Named Arguments**: Improve readability for functions with many parameters (though prefer refactoring to parameter objects/DTOs if too many).

## 3. Architecture

### Controllers

- **Keep Thin**: Controllers should only handle HTTP concerns (validation, request parsing, response formatting).
- **Delegate Logic**: Business logic differs from HTTP logic. Delegate complex operations to **Services** or **Actions**.
- **API Resources**: Use `JsonResource` for response shaping. This decouples the API response structure from the database model and ensures consistency.

### Services (Actions)

- **Single Responsibility (SRP)**: A Service or Action should typically do **one thing well**. Avoid "Manager" classes that become god-objects.
  - *Good*: `CreateUserAction`, `ProcessPaymentService`.
  - *Bad*: `UserService` (handling creation, deletion, reporting, notification, etc.).
- **Stateless**: Services should generally be stateless. Pass data via method arguments.
- **Dependency Injection**: Prefer dependency injection where it improves testability and clarity. Inject dependencies via the constructor.

### Validation (Form Requests)

- **Always use Form Requests**: Use Form Requests for complex validation. Do not validate in the controller.
- **Type Hinting**: Type-hint the Form Request in the controller method.
- **Business Rules**: Simple business rules (e.g., "email must be unique") belong in Form Requests. Complex state-dependent rules belong in the Service/Action.
- **Authorization**: Use the `authorize()` method in Form Requests for basic request authorization.

## 4. Eloquent & Database (Deep Dive)

### Queries & Performance

- **Strict Mode**: Enable Eloquent Strict Mode in non-production environments to prevent lazy loading, unfillable attribute assignments, and accessing missing attributes.

    ```php
    // AppServiceProvider.php
    Model::shouldBeStrict(!app()->isProduction());
    ```

- **Eager Loading**: Prevent N+1 problems by eager loading relationships using `with()` or `load()`.

    ```php
    // Bad
    $users = User::all();
    foreach ($users as $user) { echo $user->profile->name; } // N+1 query
    
    // Good
    $users = User::with('profile')->get();
    ```

- **Select Specific Columns**: When querying large tables, select only necessary columns to reduce memory usage.

    ```php
    User::select('id', 'name', 'email')->get();
    ```

- **Chunking**: Use `chunk()` or `cursor()` for initializing heavy processing on large datasets to keep memory usage low.

### Transactions

- **Multi-step Writes**: Use DB Transactions (`DB::transaction(...)`) for operations involving multiple write steps (e.g., creating a user and their initial settings) to ensure data integrity.

### Typing

- **Type Templating**: Use PHPDoc for type templating when necessary, especially for collections and relations, to aid static analysis and IDE autocompletion.

    ```php
    /** @var Collection<int, User> $users */
    ```

### Scopes

- **Local Scopes**: Encapsulate common query logic into reusable local scopes. Naming should be readable and expressive.

    ```php
    // Model
    public function scopeActive(Builder $query): void {
        $query->where('is_active', true);
    }
    
    // Usage
    User::active()->get();
    ```

- **Global Scopes**: Use sparingly. They apply to *all* queries on the model and can lead to unexpected behavior if hidden implementation details are forgotten.

### Observers

- **Use with Caution**: Observers are "magic" and hidden from the code flow, making debugging difficult.
- **Explicit Registration**: Prefer using the `#[ObservedBy(UserObserver::class)]` attribute on the Model to make the connection explicit and less "magic".
- **Single Responsibility**: Observers should adhere to SRP. Do not create a single Observer for all events; separate them if the logic is distinct.
- **Prefer explicit calls**: For critical logic, explicit calls (e.g., firing an Event from a Service) are often better than Observers.
- **Appropriate Use Cases**: Cache clearing, simple logging, or generating slugs/metadata where the operation is strictly tied to the database record lifecycle and not complex business logic.

### Fillable vs. Guarded

- **Use `$fillable`**: Explicitly strictly define which attributes can be mass-assigned. This is a security feature.
- **Avoid `$guarded = []`**: While convenient, unguarding models globally opens up Mass Assignment Vulnerabilities if `all()` is passed from requests.

### Updating Patterns

- **Atomic Updates**: Use `update()` for simple updates based on validated data.

    ```php
    $user->update($validatedData);
    ```

- **Explicit Property Setting**: For complex logic, set properties explicitly then call `save()`. This makes changes tracked and explicit.

    ```php
    $user->status = UserStatus::Active;
    $user->activated_at = now();
    $user->save();
    ```

- **Mass Updates**: Use `update()` on a query builder relative to a scope for efficient bulk updates.
  - *Warning*: This will **not** trigger Eloquent events or Observers. If you need side effects, you must trigger them manually or iterate (which is slower).

    ```php
    User::active()->where('last_login', '<', now()->subYear())->update(['status' => 'archived']);
    ```

### Enums & Casting

- **Cast Enums**: Use native PHP Backed Enums for attribute casting.

    ```php
    protected $casts = [
        'status' => UserStatus::class,
    ];
    ```

- This ensures type safety and prevents invalid states from entering the application logic.

### Pruning

- **Prunable Trait**: Use the `Prunable` or `MassPrunable` trait for models that need periodic cleanup (e.g., logs, tokens). Define the `prunable()` query builder method to automate deletion logic.

### Relations

- **Prefer Relation Helpers**: Prefer relationship helper methods over setting foreign key columns manually. This keeps intent explicit and reduces coupling to schema details.

    ```php
    // Preferred
    $model->relation()->attach($relation);

    // Avoid when a relation helper exists
    $model->relation_id = $relation->id;
    $model->save();
    ```

- **Factories Should Build Relations, Not IDs**: In tests and seeders, prefer factory relationship helpers such as `has()`, `for()`, and `hasAttached()` over assigning `*_id` via `state()` or `create()`.

    ```php
    // Preferred
    Model::factory()->for(Relation::factory())->create();

    // Avoid when relation helpers can express the same intent
    Model::factory()->state([
        'relation_id' => Relation::factory(),
    ])->create();
    ```

- **Use Relationship-Aware Query Helpers**: Prefer Eloquent relationship query helpers over manual foreign key filters when possible.

    ```php
    // Preferred
    Order::query()->whereBelongsTo($customer)->get();

    // Avoid when a relationship-aware helper exists
    Order::query()->where('customer_id', $customer->id)->get();
    ```

- **Why**: Avoiding manual relation wiring in writes and queries (where possible) makes code more robust and allows it to keep working if underlying model relationships or key details change.

## 5. Security (Authorization)

- **Policies**: Use Policies for all resource-based authorization.
  - Create one policy per Model (e.g., `UserPolicy`, `PostPolicy`).
  - Register them in `AuthServiceProvider` (usually auto-discovered).
- **Gates**: Use Gates for simple, non-resource-specific actions (e.g., `Gate::define('access-dashboard', ...)`).
- **Controller Authorization**: Use `$this->authorize()` (or `Gate::authorize()`) in controller methods, or middleware for route groups. Do **not** rely solely on UI hiding; backend verification is mandatory.

## 6. Testing

- **Runner**: Prefer Laravel’s default test runner and conventions.
- **AAA Pattern**: Structure all tests using **Arrange, Act, Assert**.

    ```php
    public function test_user_can_register() {
        // Arrange
        $data = ['name' => fake()->name(), 'email' => fake()->safeEmail(), 'password' => fake()->password()];
        
        // Act
        $response = $this->post('/register', $data);
        
        // Assert
        $response->assertStatus(201);
        $this->assertDatabaseHas(User::class, ['email' => $data['email']]);
    }
    ```
- **Factories**: Prefer factories and builders for test setup over manual instantiation.
  - Use `state()` methods for variations (e.g., `User::factory()->admin()->create()`).
  - Avoid massive manual creation of dependencies.
- **Faking**: Always use `fake()` for values instead of hardcoding, unless a fixed value is absolutely required for the test logic.
- **Mocking**: Use Laravel's fakes for external services to keep tests fast and deterministic.
  - `Mail::fake()`, `Event::fake()`, `Notification::fake()`, `Queue::fake()`.
  - Assert against the fakes to verify interaction.
- **Keep tests small**: Each function in a tests class should test one thing only!

## 7. Laravel Tooling

- **Generators**: If the project documents artisan usage, prefer the project’s generators and commands over creating files manually.


## 8. Dependency injection

- **Service Instantiation**: Do not manually create services that have dependency injection that should be resolved by Larvel (this is always the case for services). Instead realy on the global app(...) helper
```php
// Bad
$service = new Service($dependency);

// Good
$service = app(Service::class);
```

## 9. Stricly typed code

- **Classes over keyed arrays**: Prefer using classes over keyed arrays for data transfer objects. This improves type safety and makes code more readable. If the project has 
laravel-data by spatie installed. Use that for Data classes.

```php
// Bad
$data = [
    'name' => 'John',
    'email' => 'john@example.com',
    'password' => 'secret',
];

// Good
$data = new UserData(
    name: 'John',
    email: 'john@example.com',
    password: 'secret',
);
```
