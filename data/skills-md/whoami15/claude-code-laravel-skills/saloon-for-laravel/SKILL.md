---
name: saloon-for-laravel
description: Use Saloon to build elegant API integrations in modern Laravel applications, including connectors, requests, responses, authentication, testing, pagination, and SDK patterns.
compatible_agents:
  - Claude Code
  - Cursor
tags:
  - laravel
  - api
---

# Saloon for Laravel

## When to use this skill

Use this skill when working with SaloonPHP in a Laravel 11+ application:

- Integrating with third-party APIs (REST, JSON, XML)
- Building API connectors, requests, and handling responses
- Authenticating API requests (token, basic, OAuth2, custom)
- Sending request bodies (JSON, form, multipart, XML)
- Testing API integrations with mocking and faking
- Implementing pagination, rate limiting, caching, or retries
- Building reusable SDKs for APIs
- Working with DTOs from API responses

## Core Concepts

- **Connectors** define the API base URL and shared configuration (headers, auth, middleware).
- **Requests** define individual endpoints, HTTP methods, and request-specific data.
- **Responses** provide a rich interface for reading status, headers, and parsed body data.
- Connectors send Requests and return Responses: `$connector->send($request)`.
- Use Artisan commands to generate classes — never create them manually from scratch.
- Store integration classes in `app/Http/Integrations/{ServiceName}/` (configurable in `config/saloon.php`).

## Installation

```bash
composer require saloonphp/laravel-plugin
```

This installs both `saloonphp/saloon` (core) and the Laravel integration. Publish the config file:

```bash
php artisan vendor:publish --tag=saloon-config
```

Optional plugins (install as needed):

```bash
composer require saloonphp/pagination-plugin   # Paginated API responses
composer require saloonphp/cache-plugin         # Response caching
composer require saloonphp/rate-limit-plugin    # Rate limit handling
composer require saloonphp/xml-wrangler         # XML reading/writing
```

## File Structure

```
app/Http/Integrations/
└── Acme/
    ├── AcmeConnector.php
    ├── Requests/
    │   ├── GetUserRequest.php
    │   ├── ListProjectsRequest.php
    │   └── CreateProjectRequest.php
    ├── Responses/
    │   └── AcmeResponse.php
    └── Data/
        └── UserDTO.php
```

## Creating Connectors

Generate with Artisan:

```bash
php artisan saloon:connector Acme AcmeConnector
```

A connector defines the base URL and shared configuration:

```php
namespace App\Http\Integrations\Acme;

use Saloon\Http\Connector;
use Saloon\Traits\Plugins\AcceptsJson;
use Saloon\Traits\Plugins\AlwaysThrowOnErrors;

class AcmeConnector extends Connector
{
    use AcceptsJson;
    use AlwaysThrowOnErrors;

    public function __construct(
        protected readonly string $token,
    ) {}

    public function resolveBaseUrl(): string
    {
        return config('services.acme.base_url');
    }

    protected function defaultHeaders(): array
    {
        return [
            'Authorization' => 'Bearer ' . $this->token,
        ];
    }
}
```

## Creating Requests

Generate with Artisan:

```bash
php artisan saloon:request Acme GetUserRequest
```

Define the HTTP method and endpoint:

```php
namespace App\Http\Integrations\Acme\Requests;

use Saloon\Enums\Method;
use Saloon\Http\Request;

class GetUserRequest extends Request
{
    protected Method $method = Method::GET;

    public function __construct(
        protected readonly string $username,
    ) {}

    public function resolveEndpoint(): string
    {
        return '/users/' . $this->username;
    }
}
```

## Request Body Data

Implement `HasBody` interface with a body trait on the request:

```php
use Saloon\Contracts\Body\HasBody;
use Saloon\Enums\Method;
use Saloon\Http\Request;
use Saloon\Traits\Body\HasJsonBody;

class CreateProjectRequest extends Request implements HasBody
{
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        protected readonly string $name,
        protected readonly bool $private = false,
    ) {}

    public function resolveEndpoint(): string
    {
        return '/projects';
    }

    protected function defaultBody(): array
    {
        return [
            'name' => $this->name,
            'private' => $this->private,
        ];
    }
}
```

Available body traits (each requires implementing `HasBody`):

| Trait | Use Case |
|---|---|
| `HasJsonBody` | JSON payloads (`application/json`) |
| `HasFormBody` | Form data (`application/x-www-form-urlencoded`) |
| `HasMultipartBody` | File uploads (`multipart/form-data`) |
| `HasXmlBody` | XML payloads |
| `HasStringBody` | Raw string body |
| `HasStreamBody` | Stream/binary body |

## Sending Requests

```php
$connector = new AcmeConnector(token: config('services.acme.token'));
$request = new GetUserRequest('johndoe');

$response = $connector->send($request);
```

Using dependency injection in a controller:

```php
class UserController extends Controller
{
    public function show(string $username, AcmeConnector $connector)
    {
        $response = $connector->send(new GetUserRequest($username));

        return $response->json();
    }
}
```

Register the connector in a service provider for DI:

```php
// AppServiceProvider::register()
$this->app->bind(AcmeConnector::class, function () {
    return new AcmeConnector(token: config('services.acme.token'));
});
```

## Handling Responses

```php
$response = $connector->send($request);

// Status checks
$response->successful();     // 200-299
$response->ok();             // 200
$response->failed();         // 400+
$response->status();         // int

// Reading data
$response->json();           // array
$response->json('user.name'); // nested key access
$response->object();         // stdClass
$response->collect();        // Illuminate\Support\Collection
$response->body();           // raw string

// Headers
$response->headers()->all();
$response->header('Content-Type');

// Error handling
$response->throw();          // throw if failed
$response->onError(fn ($response) => logger()->error('API failed', [
    'status' => $response->status(),
]));
```

## Authentication

### Built-in authenticators

```php
use Saloon\Http\Auth\TokenAuthenticator;
use Saloon\Http\Auth\BasicAuthenticator;
use Saloon\Http\Auth\QueryAuthenticator;
use Saloon\Http\Auth\HeaderAuthenticator;

// Bearer token (most common)
$connector->authenticate(new TokenAuthenticator('my-api-token'));

// Basic auth
$connector->authenticate(new BasicAuthenticator('user', 'password'));

// Query parameter auth
$connector->authenticate(new QueryAuthenticator('api_key', 'my-key'));

// Custom header
$connector->authenticate(new HeaderAuthenticator('my-token', 'X-API-Key'));
```

### Default authentication on a connector

```php
class AcmeConnector extends Connector
{
    public function __construct(protected readonly string $token) {}

    protected function defaultAuth(): TokenAuthenticator
    {
        return new TokenAuthenticator($this->token);
    }
}
```

## Error Handling

Use `AlwaysThrowOnErrors` to throw exceptions automatically on failed responses:

```php
use Saloon\Traits\Plugins\AlwaysThrowOnErrors;

class AcmeConnector extends Connector
{
    use AlwaysThrowOnErrors;
}
```

Catch specific exceptions:

```php
use Saloon\Exceptions\Request\RequestException;
use Saloon\Exceptions\Request\ClientException;      // 4xx
use Saloon\Exceptions\Request\ServerException;      // 5xx
use Saloon\Exceptions\Request\FatalRequestException; // network failure

try {
    $response = $connector->send($request);
} catch (ClientException $e) {
    // 4xx error — $e->getResponse() gives the Response object
} catch (ServerException $e) {
    // 5xx error
} catch (FatalRequestException $e) {
    // Connection failure, timeout, etc.
}
```

Custom failure logic on a connector or request:

```php
public function hasRequestFailed(Response $response): ?bool
{
    return $response->json('success') === false;
}
```

## DTOs (Data Transfer Objects)

Implement `createDtoFromResponse` on a request to cast responses:

```php
use Saloon\Http\Request;
use Saloon\Http\Response;

class GetUserRequest extends Request
{
    // ...

    public function createDtoFromResponse(Response $response): UserDTO
    {
        return new UserDTO(
            name: $response->json('name'),
            email: $response->json('email'),
            avatar: $response->json('avatar_url'),
        );
    }
}
```

Then use it:

```php
$user = $connector->send(new GetUserRequest('johndoe'))->dto();
$user = $connector->send(new GetUserRequest('johndoe'))->dtoOrFail();
```

## Middleware

Add middleware on connectors or requests to modify the request/response pipeline:

```php
class AcmeConnector extends Connector
{
    public function __construct()
    {
        // Request middleware
        $this->middleware()->onRequest(function (PendingRequest $pendingRequest) {
            $pendingRequest->headers()->add('X-Request-ID', Str::uuid()->toString());
        });

        // Response middleware
        $this->middleware()->onResponse(function (Response $response) {
            logger()->info('Acme API responded', ['status' => $response->status()]);
        });
    }
}
```

Use the `boot` method for one-time setup:

```php
public function boot(PendingRequest $pendingRequest): void
{
    $pendingRequest->config()->add('timeout', 60);
}
```

## Testing with Saloon Facade

The Laravel plugin provides a `Saloon` facade for fluent test mocking:

```php
use Saloon\Laravel\Facades\Saloon;
use Saloon\Http\Faking\MockResponse;

it('fetches a user from the API', function () {
    Saloon::fake([
        GetUserRequest::class => MockResponse::make(
            body: ['name' => 'Sam', 'email' => 'sam@example.com'],
            status: 200,
        ),
    ]);

    $response = $this->get('/api/users/johndoe');

    $response->assertOk();

    Saloon::assertSent(GetUserRequest::class);
    Saloon::assertSentCount(1);
});
```

### Sequence responses

```php
Saloon::fake([
    GetUserRequest::class => MockResponse::sequence([
        MockResponse::make(['attempt' => 1], 500),
        MockResponse::make(['attempt' => 2], 200),
    ]),
]);
```

### Assertions

```php
Saloon::assertSent(GetUserRequest::class);
Saloon::assertSent(fn (Request $request) => $request->resolveEndpoint() === '/users/johndoe');
Saloon::assertNotSent(DeleteUserRequest::class);
Saloon::assertSentCount(2);
Saloon::assertNothingSent();
```

### Prevent stray requests

Ensure all API requests are mocked in tests:

```php
Saloon::fake();
// or
Saloon::allowStrayRequests();
```

## Retry Logic

Set retry properties on connectors or requests:

```php
class AcmeConnector extends Connector
{
    protected int $tries = 3;
    protected int $retryInterval = 500;           // milliseconds
    protected bool $useExponentialBackoff = true;
    protected bool $throwOnMaxTries = true;

    public function handleRetry(FatalRequestException|RequestException $exception, Request $request): bool
    {
        // Return false to stop retrying
        if ($exception instanceof RequestException && $exception->getResponse()->status() === 422) {
            return false;
        }

        return true;
    }
}
```

## Pagination

Install the pagination plugin:

```bash
composer require saloonphp/pagination-plugin
```

Implement the `HasPagination` interface on your connector:

```php
use Saloon\Http\Connector;
use Saloon\PaginationPlugin\PagedPaginator;
use Saloon\PaginationPlugin\Contracts\HasPagination;

class AcmeConnector extends Connector implements HasPagination
{
    public function paginate(Request $request): PagedPaginator
    {
        return new class(connector: $this, request: $request) extends PagedPaginator
        {
            protected function isLastPage(Response $response): bool
            {
                return empty($response->json('next_page_url'));
            }

            protected function getPageItems(Response $response, Response $originalResponse): array
            {
                return $response->json('data');
            }
        };
    }
}
```

Use the paginator:

```php
$paginator = $connector->paginate(new ListProjectsRequest);

foreach ($paginator as $response) {
    $projects = $response->json('data');
}

// Or collect all items
$allProjects = $paginator->collect()->all();
```

Available paginator types: `PagedPaginator`, `OffsetPaginator`, `CursorPaginator`.

## Rate Limiting

Install the rate limit plugin:

```bash
composer require saloonphp/rate-limit-plugin
```

Add rate limiting to your connector:

```php
use Saloon\Http\Connector;
use Saloon\RateLimitPlugin\Contracts\RateLimitStore;
use Saloon\RateLimitPlugin\Limit;
use Saloon\RateLimitPlugin\Stores\LaravelCacheStore;
use Saloon\RateLimitPlugin\Traits\HasRateLimits;

class AcmeConnector extends Connector
{
    use HasRateLimits;

    protected function resolveLimits(): array
    {
        return [
            Limit::allow(5000)->everyHour(),
        ];
    }

    protected function resolveRateLimitStore(): RateLimitStore
    {
        return new LaravelCacheStore(cache()->store());
    }
}
```

## Caching Responses

Install the cache plugin:

```bash
composer require saloonphp/cache-plugin
```

Add caching to a request:

```php
use Saloon\CachePlugin\Contracts\Cacheable;
use Saloon\CachePlugin\Contracts\Driver;
use Saloon\CachePlugin\Drivers\LaravelCacheDriver;
use Saloon\CachePlugin\Traits\HasCaching;
use Saloon\Http\Request;

class GetUserRequest extends Request implements Cacheable
{
    use HasCaching;

    public function resolveCacheDriver(): Driver
    {
        return new LaravelCacheDriver(cache()->store());
    }

    public function cacheExpiryInSeconds(): int
    {
        return 3600; // 1 hour
    }
}
```

## Concurrency & Pools

Send multiple requests concurrently:

```php
use Saloon\Http\Response;

$pool = $connector->pool(
    requests: [
        new GetUserRequest('alice'),
        new GetUserRequest('bob'),
        new GetUserRequest('charlie'),
    ],
    concurrency: 5,
    responseHandler: function (Response $response, int $key) {
        logger()->info('User fetched', ['data' => $response->json('name')]);
    },
    exceptionHandler: function (Exception $exception, int $key) {
        logger()->error('Request failed', ['key' => $key]);
    },
);

$pool->send()->wait();
```

## OAuth2 Authentication

Create an OAuth2 connector:

```bash
php artisan saloon:connector Acme AcmeOAuthConnector
```

```php
use Saloon\Http\Connector;
use Saloon\Http\Auth\AccessTokenAuthenticator;
use Saloon\Traits\OAuth2\AuthorizationCodeGrant;

class AcmeOAuthConnector extends Connector
{
    use AuthorizationCodeGrant;

    public function resolveBaseUrl(): string
    {
        return config('services.acme.base_url');
    }

    protected function resolveAccessTokenUrl(): string
    {
        return config('services.acme.base_url') . '/oauth/token';
    }

    protected function resolveAuthorizationUrl(): string
    {
        return config('services.acme.base_url') . '/oauth/authorize';
    }
}
```

Usage in a controller:

```php
// Redirect to OAuth provider
public function redirect(AcmeOAuthConnector $connector)
{
    return $connector->getAuthorizationUrl(
        scopes: ['read', 'write'],
        state: session()->get('state'),
    );
}

// Handle callback
public function callback(Request $request, AcmeOAuthConnector $connector)
{
    $authenticator = $connector->getAccessToken(
        code: $request->query('code'),
    );

    // Store for later — use encrypted cast on your model
    $user->update(['acme_token' => $authenticator]);
}
```

Store OAuth tokens with the provided Eloquent cast:

```php
use Saloon\Laravel\Casts\EncryptedOAuthAuthenticatorCast;

class User extends Authenticatable
{
    protected function casts(): array
    {
        return [
            'acme_token' => EncryptedOAuthAuthenticatorCast::class,
        ];
    }
}
```

## Building SDKs

Organize connector methods as a clean SDK interface:

```php
class AcmeConnector extends Connector
{
    public function getUser(string $username): Response
    {
        return $this->send(new GetUserRequest($username));
    }

    public function listProjects(string $username): Response
    {
        return $this->send(new ListProjectsRequest($username));
    }

    public function createProject(string $name, bool $private = false): Response
    {
        return $this->send(new CreateProjectRequest($name, $private));
    }
}
```

Usage becomes expressive:

```php
$acme = new AcmeConnector(token: config('services.acme.token'));

$user = $acme->getUser('johndoe')->dto();
$projects = $acme->listProjects('johndoe')->collect('data');
```

## Telescope & Pulse Integration

Use the Laravel HTTP sender for Telescope and Pulse visibility:

```php
// config/saloon.php
'default_sender' => \Saloon\Laravel\HttpSender::class,
```

## Common Pitfalls

- Forgetting to implement `HasBody` interface when sending request body data.
- Not using Artisan commands (`saloon:connector`, `saloon:request`) to generate classes.
- Using the wrong HTTP method enum — always use `Saloon\Enums\Method`.
- Forgetting to install `saloonphp/pagination-plugin` for pagination (required in v3).
- Not setting `HttpSender` in config when Telescope or Pulse visibility is needed.
- Not mocking all requests in tests — use `Saloon::fake()` to prevent stray requests.
