---
name: testing-pyramid
description: >
  Use when writing tests for a Symfony app — unit, integration (Kernel), and functional
  (WebTestCase) tests, the test database, fixtures/factories (Foundry), and what to mock.
  Use when the task mentions test, PHPUnit, WebTestCase, KernelTestCase, fixtures, or
  coverage.
---

# Testing Pyramid (Symfony + PHPUnit)

## The shape

```
        ╱╲        Functional (few)   — WebTestCase: real HTTP kernel, real DB, full stack
       ╱──╲       Integration (some) — KernelTestCase: container + DB, no HTTP
      ╱────╲      Unit (many)        — plain PHPUnit: pure PHP, no container, no DB
     ╱──────╲
```

Most tests are fast unit tests of domain logic. A smaller layer of integration tests covers wiring + persistence. A thin top layer of functional tests covers the critical user-facing flows end-to-end. **Don't invert it** — a suite that's all `WebTestCase` is slow and brittle.

## Unit tests — domain logic, no framework

Test value objects, aggregates, and services with their collaborators mocked. No container, no DB, milliseconds each.

```php
final class OrderTest extends TestCase
{
    public function test_confirming_an_empty_order_is_rejected(): void
    {
        $order = Order::place();

        $this->expectException(\DomainException::class);
        $order->confirm();                       // invariant: can't confirm empty
    }

    public function test_adding_a_line_to_a_confirmed_order_is_rejected(): void
    {
        $order = Order::place();
        $order->addItem(Uuid::v7(), 2);
        $order->confirm();

        $this->expectException(\DomainException::class);
        $order->addItem(Uuid::v7(), 1);
    }
}
```

Mock only what you **own and inject** (ports/repositories). Don't mock value objects or the framework.

```php
// ✅ mock the repository PORT
$orders = $this->createMock(OrderRepository::class);
$orders->method('ofId')->willReturn($existingOrder);
$service = new CancelOrderHandler($orders);
```

## Integration tests — wiring + persistence

`KernelTestCase` boots the container; pull real services and hit a real (test) database. Use it to verify repository queries, Doctrine mapping, and service wiring.

```php
final class OrderRepositoryTest extends KernelTestCase
{
    private EntityManagerInterface $em;
    private OrderRepository $repo;

    protected function setUp(): void
    {
        self::bootKernel();
        $this->em = self::getContainer()->get(EntityManagerInterface::class);
        $this->repo = self::getContainer()->get(OrderRepository::class);
    }

    public function test_find_active_by_customer_returns_only_active(): void
    {
        OrderFactory::createOne(['customerEmail' => 'a@x.io', 'status' => OrderStatus::Active]);
        OrderFactory::createOne(['customerEmail' => 'a@x.io', 'status' => OrderStatus::Cancelled]);

        $result = $this->repo->findActiveByCustomer('a@x.io');

        self::assertCount(1, $result);
    }
}
```

## Functional tests — the real HTTP stack

`WebTestCase` sends a real request through the kernel. Reserve it for critical flows and contract checks (status codes, problem+json shape, auth).

```php
final class CreateOrderTest extends WebTestCase
{
    public function test_post_orders_returns_201_with_location(): void
    {
        $client = static::createClient();

        $client->request('POST', '/api/orders', server: [
            'CONTENT_TYPE' => 'application/json',
        ], content: json_encode([
            'customerEmail' => 'buyer@example.com',
            'items' => [['productId' => Uuid::v7()->toRfc4122(), 'quantity' => 2]],
        ]));

        self::assertResponseStatusCodeSame(201);
        self::assertResponseHasHeader('Location');
    }

    public function test_invalid_payload_returns_422_problem_json(): void
    {
        $client = static::createClient();
        $client->request('POST', '/api/orders', content: json_encode(['customerEmail' => 'not-an-email']));

        self::assertResponseStatusCodeSame(422);
        self::assertResponseHeaderSame('Content-Type', 'application/problem+json');
    }
}
```

## The test database

- A separate DB for `test` (`.env.test` / `DATABASE_URL`); never run tests against dev/prod data.
- Reset state between tests with **DAMA\DoctrineTestBundle** (wraps each test in a transaction and rolls back) — far faster than truncating.
- Build schema from migrations in CI so tests catch migration drift.

```bash
php bin/console --env=test doctrine:database:create
php bin/console --env=test doctrine:migrations:migrate --no-interaction
```

## Fixtures via factories (Foundry / Zenstruck)

Prefer `zenstruck/foundry` factories over static fixture files — readable, overridable per test, no shared mutable state.

```php
final class OrderFactory extends PersistentProxyObjectFactory
{
    public static function class(): string { return Order::class; }

    protected function defaults(): array
    {
        return [
            'customerEmail' => self::faker()->email(),
            'status' => OrderStatus::Pending,
        ];
    }
}

// In a test
$order = OrderFactory::createOne(['status' => OrderStatus::Active]);
OrderFactory::createMany(5);
```

## Conventions

- Name tests by behavior: `test_confirming_an_empty_order_is_rejected`, not `testConfirm`.
- Arrange / Act / Assert structure; one logical assertion target per test.
- Don't assert on private internals — test observable behavior.
- Keep functional tests few and focused on contracts; push logic coverage down to unit tests.
- No network calls in tests — mock HTTP clients (`MockHttpClient`).

## Gotchas

- Agent writes everything as `WebTestCase` — invert back to a pyramid: most logic in fast unit tests.
- Agent mocks the entity / value object under test — only mock injected ports/collaborators.
- Agent hits dev/prod DB or shares state across tests — use a `test` DB + DAMA transaction rollback.
- Agent builds the test schema with `schema:update` — run migrations so tests catch drift.
- Agent makes real HTTP/API calls in tests — use `MockHttpClient`.
- Agent writes brittle assertions on serialized internals — assert status codes, headers, and visible fields.
- Agent uses static SQL fixture dumps — use Foundry factories for readable, isolated data.
- Agent forgets to assert the `application/problem+json` content type on error-path tests.
