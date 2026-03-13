---
name: laravel-actions
description: Write, scaffold, explain, and refactor code using the lorisleiva/laravel-actions package. Use this skill whenever the user is working with Laravel Actions, wants to create an action class, convert a controller/job/listener/command into an action, asks how to use AsAction trait, dispatch an action as a job, use an action as a controller or listener, set up validation/authorization in an action, test or mock actions, or asks anything about the laravel-actions package pattern.
---

# Laravel Actions

`lorisleiva/laravel-actions` lets you write a single PHP class that handles **one specific task** and run it as an **object**, **controller**, **job**, **listener**, or **command** — whichever is appropriate.

Install: `composer require lorisleiva/laravel-actions`
Create: `php artisan make:action MyAction`

## Core structure

Every action is a plain PHP class with the `AsAction` trait and a `handle` method:

```php
use Lorisleiva\Actions\Concerns\AsAction;

class PublishNewArticle
{
    use AsAction;

    public function handle(User $author, string $title, string $body): Article
    {
        return $author->articles()->create(compact('title', 'body'));
    }
}
```

- Place actions in `app/Actions/` grouped by topic (e.g. `app/Actions/Articles/`)
- Name them as short verb-first sentences: `SendWelcomeEmail`, `CreateInvoice`, `SyncContacts`
- Use constructor injection for dependencies — actions are always resolved from the container

## As an Object

```php
// Resolve and run
PublishNewArticle::run($author, 'Title', 'Body');

// Resolve only
$action = PublishNewArticle::make();

// Conditional execution
PublishNewArticle::runIf($condition, $author, 'Title', 'Body');
PublishNewArticle::runUnless($condition, $author, 'Title', 'Body');
```

## As a Controller

Register in routes just like an invokable controller:

```php
Route::post('/articles', PublishNewArticle::class)->middleware('auth');
```

Implement `asController` to map request data to `handle` args:

```php
public function asController(Request $request): ArticleResource
{
    $article = $this->handle(
        $request->user(),
        $request->input('title'),
        $request->input('body'),
    );
    return new ArticleResource($article);
}
```

If `asController` is omitted, `handle` is used directly as the invokable.

**Middleware** on the action itself:
```php
public function getControllerMiddleware(): array
{
    return ['auth', 'verified'];
}
```

**Different responses for JSON vs HTML:**
```php
public function jsonResponse(Article $article, Request $request): ArticleResource
{
    return new ArticleResource($article);
}

public function htmlResponse(Article $article, Request $request): RedirectResponse
{
    return redirect()->route('articles.show', $article);
}
```

**Register routes inline** (optional):
```php
public static function routes(Router $router): void
{
    $router->post('/articles', static::class);
}
```
Then call `Actions::registerRoutes(['app/Actions'])` in a service provider.

**Explicit route methods** for multi-endpoint actions:
```php
Route::get('/articles/create', [PublishNewArticle::class, 'showForm']);
Route::post('/articles', PublishNewArticle::class);
```

## Validation & Authorization (as Controller)

Inject `ActionRequest` to trigger validation/authorization defined on the action itself:

```php
use Lorisleiva\Actions\ActionRequest;

public function asController(ActionRequest $request): ArticleResource
{
    $article = $this->handle(
        $request->user(),
        $request->validated('title'),
        $request->validated('body'),
    );
    return new ArticleResource($article);
}

public function authorize(ActionRequest $request): bool
{
    return $request->user()->can('create', Article::class);
}

public function rules(): array
{
    return [
        'title' => ['required', 'string', 'max:255'],
        'body'  => ['required', 'string'],
    ];
}
```

Additional validation hooks:
```php
public function prepareForValidation(ActionRequest $request): void { /* mutate input */ }
public function withValidator(Validator $validator): void { /* add callbacks */ }
public function afterValidator(Validator $validator): void { /* after hook */ }
public function getValidator(): Validator { /* full control */ }
public function getValidationData(): array { return $this->all(); }
public function getValidationMessages(): array { return []; }
public function getValidationAttributes(): array { return []; }
public function getValidationRedirect(Request $request): string { return url()->previous(); }
public function getValidationErrorBag(): string { return 'default'; }
public function getValidationFailure(): void { throw new ValidationException(...); }
public function getAuthorizationFailure(): void { throw new AuthorizationException(...); }
```

## As a Job

```php
// Async dispatch
PublishNewArticle::dispatch($author, 'Title', 'Body');

// Conditional dispatch
PublishNewArticle::dispatchIf($cond, $author, 'Title', 'Body');
PublishNewArticle::dispatchUnless($cond, $author, 'Title', 'Body');

// Sync dispatch
PublishNewArticle::dispatchSync($author, 'Title', 'Body');

// After response is sent
PublishNewArticle::dispatchAfterResponse($author, 'Title', 'Body');
```

Implement `asJob` only when the job-specific behaviour differs from `handle`:

```php
public function asJob(Team $team): void
{
    $this->handle($team, fullReport: true);
}
```

**Configure job defaults:**
```php
public string $queue = 'emails';
public int $tries = 3;
public int $timeout = 60;
public int $maxExceptions = 2;

public function configureJob(JobDecorator $job): void
{
    $job->onQueue('high')->delay(now()->addMinutes(5));
}

public function getJobBackoff(): array { return [10, 30, 60]; }
public function getJobRetryUntil(): DateTime { return now()->addHour(); }
public function getJobMiddleware(): array { return [new WithoutOverlapping($this->team->id)]; }
```

**Unique jobs:**
```php
use Illuminate\Contracts\Queue\ShouldBeUnique;

class SendTeamReport implements ShouldBeUnique
{
    use AsAction;

    public function getJobUniqueId(Team $team): int { return $team->id; }
    public function getJobUniqueFor(): int { return 3600; }
}
```

**Job chaining:**
```php
SendWelcomeEmail::withChain([
    VerifyEmailAddress::makeJob($user),
    AssignDefaultRole::makeJob($user),
])->dispatch($user);
```

**Batching:**
```php
use Illuminate\Support\Facades\Bus;

Bus::batch([
    ProcessInvoice::makeJob($invoiceA),
    ProcessInvoice::makeJob($invoiceB),
])->dispatch();
```

**Horizon tags & display name:**
```php
public function getJobTags(Team $team): array { return ["team:{$team->id}"]; }
public function getJobDisplayName(): string { return 'Send Team Report'; }
```

## As a Listener

Register in `EventServiceProvider`:
```php
protected $listen = [
    UserRegistered::class => [SendWelcomeEmail::class],
];
```

Or with the Event facade:
```php
Event::listen(UserRegistered::class, SendWelcomeEmail::class);
```

For a **queueable listener**, add `implements ShouldQueue` to the action.

Use `asListener` to map event data to `handle` args:
```php
public function asListener(UserRegistered $event): void
{
    $this->handle($event->user);
}
```

## As a Command

Register in `Kernel::$commands` or auto-register:
```php
Actions::registerCommands(['app/Actions']);
```

```php
use Illuminate\Console\Command;

class SendTeamReport
{
    use AsAction;

    public string $commandSignature = 'teams:report {team_id}';
    public string $commandDescription = 'Send the weekly report to a team.';

    public function asCommand(Command $command): void
    {
        $team = Team::findOrFail($command->argument('team_id'));
        $this->handle($team);
        $command->info('Report sent!');
    }

    // Dynamic signature/description/help:
    public function getCommandSignature(): string { return '...'; }
    public function getCommandDescription(): string { return '...'; }
    public function getCommandHelp(): string { return '...'; }
    public function isCommandHidden(): bool { return false; }
}
```

## Testing & Mocking

```php
// Mock — set expectations before running
PublishNewArticle::mock()
    ->shouldReceive('handle')
    ->once()
    ->andReturn($fakeArticle);

// Shorthand
PublishNewArticle::mock()->shouldRun()->once()->andReturn($fakeArticle);
PublishNewArticle::mock()->shouldNotRun();

// Partial mock (only mocked methods get expectations)
PublishNewArticle::partialMock()->shouldReceive('fetch')->andReturn([...]);

// Spy — run first, assert after
PublishNewArticle::spy()->shouldHaveReceived('handle')->once();
PublishNewArticle::spy()->allowToRun();

// Lifecycle helpers
PublishNewArticle::isFake();   // bool — is currently mocked?
PublishNewArticle::clearFake(); // reset to real implementation
```

**Assert jobs were dispatched:**
```php
Queue::fake();

// ...trigger code...

PublishNewArticle::assertPushed();
PublishNewArticle::assertPushed(2); // dispatched exactly N times
PublishNewArticle::assertPushed(fn ($action, $args) => $args[0]->is($team));
PublishNewArticle::assertNotPushed();
PublishNewArticle::assertPushedOn('high', fn ($action, $args) => true);
```

## WithAttributes (optional, v2.1+)

For actions that benefit from validated, unified attribute bags (useful when porting v1 code or when the same validation should apply across object and controller usage):

```php
use Lorisleiva\Actions\Concerns\AsAction;
use Lorisleiva\Actions\Concerns\WithAttributes;

class PublishNewArticle
{
    use AsAction;
    use WithAttributes;

    public function handle(User $author, array $data = []): Article
    {
        $this->fill($data);
        $this->validateAttributes(); // triggers authorize + rules
        return $author->articles()->create($this->validated());
    }

    public function asController(ActionRequest $request): Article
    {
        $this->fillFromRequest($request);
        return $this->handle($request->user());
    }
}
```

`WithAttributes` methods: `fill`, `set`, `get`, `has`, `all`, `only`, `except`, `fillFromRequest`, `validateAttributes`.

Note: when `WithAttributes` is used, the `ActionRequest` will **not** auto-validate — call `$request->validate()` manually if needed.

## More granular traits

Instead of `AsAction` you can cherry-pick:
- `AsObject` — `run`, `make`, `runIf`, `runUnless`
- `AsController` — controller decorator support
- `AsJob` — job decorator support
- `AsListener` — listener decorator support
- `AsCommand` — command decorator support
- `AsFake` — mock/spy support

## Reference docs

For full API details, see:
- [references/api.md](references/api.md) — complete method list per trait
