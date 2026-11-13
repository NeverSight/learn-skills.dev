---
name: layered-architecture
description: >
  Use when generating controllers, services, repositories, or DTOs in a Symfony app.
  Enforces layer boundaries: HTTP in controllers, business logic in services, data
  access in repositories, and DTO mapping between them. Forbids entities in responses
  and repository access from controllers.
---

# Layered Architecture (Symfony)

## Layer rules

```
Controller (#[Route])     ← HTTP only. No business logic. No entities in responses.
      ↓ DTOs
Service (application)     ← All business logic. Orchestrates repositories. Owns the transaction.
      ↓ Entities / domain objects
Repository (Doctrine)     ← Data access only. No business logic. Returns entities or read models.
      ↓ DQL / DBAL
Database
```

Dependencies point **downward only**. A repository never calls a service; a service never sees an `Request`.

## Controller layer

- Handles HTTP: route matching, deserializing the request, returning a `Response`.
- Calls **one** service method per endpoint — no orchestration in the controller.
- Never returns a Doctrine entity directly — map to a response DTO (or use serialization groups).
- Never injects a repository — always go through a service.
- No `try/catch` for domain errors — let an exception listener turn them into HTTP responses.

```php
// ✅ GOOD
#[Route('/orders', methods: ['POST'])]
public function create(#[MapRequestPayload] CreateOrderRequest $request): JsonResponse
{
    $order = $this->orderService->createOrder($request);

    return $this->json(OrderResponse::fromEntity($order), Response::HTTP_CREATED);
}

// ❌ BAD — business logic + direct repository + entity returned
#[Route('/orders', methods: ['POST'])]
public function create(Request $request, OrderRepository $orders): JsonResponse
{
    $data = json_decode($request->getContent(), true);
    if (empty($data['items'])) {
        throw new \RuntimeException('No items');     // domain rule in controller
    }
    $order = new Order($data);
    $orders->save($order);                            // controller talks to repository
    return $this->json($order);                       // entity leaks out
}
```

## Service layer

- Contains all business logic, validation rules beyond the DTO, and orchestration.
- Owns the transaction boundary (`EntityManagerInterface::flush()` / `wrapInTransaction()`).
- **Constructor injection only** — never `ContainerInterface` / service locator pulls.
- One service per aggregate (`OrderService`, not `OrderAndPaymentService`).
- Returns domain objects or DTOs — never an HTTP `Request` / `Response`.

```php
// ✅ GOOD
final class OrderService
{
    public function __construct(
        private readonly OrderRepository $orders,
        private readonly InventoryService $inventory,
        private readonly EntityManagerInterface $em,
    ) {}

    public function createOrder(CreateOrderRequest $request): Order
    {
        $this->inventory->reserve($request->items);
        $order = Order::create($request->customerEmail);
        foreach ($request->items as $item) {
            $order->addItem($item->productId, $item->quantity);
        }

        $this->em->persist($order);
        $this->em->flush();

        return $order;
    }
}

// ❌ BAD — service container pull, HTTP type in service
final class OrderService
{
    public function __construct(private ContainerInterface $container) {}

    public function createOrder(Request $request): Response { /* ... */ }
}
```

## Repository layer

- Extends `ServiceEntityRepository<Entity>`.
- Custom queries via the query builder or DQL — raw SQL only when unavoidable.
- Returns entities or read-model DTOs — never associative arrays leaking column names.
- No business logic — pure data access.

```php
// ✅ GOOD
/** @extends ServiceEntityRepository<Order> */
final class OrderRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Order::class);
    }

    /** @return Order[] */
    public function findActiveByCustomer(string $email): array
    {
        return $this->createQueryBuilder('o')
            ->andWhere('o.customerEmail = :email')
            ->andWhere('o.status = :status')
            ->setParameter('email', $email)
            ->setParameter('status', OrderStatus::Active)
            ->getQuery()
            ->getResult();
    }
}
```

## DTOs

- **Separate** request and response DTOs — never reuse one class for both.
- Validation constraints live on the **request** DTO only (see `dto-and-validation`).
- Static factory for mapping: `OrderResponse::fromEntity($order)`.
- Use `readonly` classes / promoted readonly properties — DTOs are immutable.

```php
// ✅ GOOD
final readonly class OrderResponse
{
    /** @param LineItemResponse[] $items */
    public function __construct(
        public string $id,
        public string $status,
        public array $items,
    ) {}

    public static function fromEntity(Order $order): self
    {
        return new self(
            $order->getId()->toRfc4122(),
            $order->getStatus()->value,
            array_map(LineItemResponse::fromEntity(...), $order->getItems()->toArray()),
        );
    }
}
```

## Mapping

- Keep mapping out of controllers and services — static factory on the DTO, or a dedicated mapper.
- Entity → response DTO: `OrderResponse::fromEntity($order)`.
- Request DTO → entity: static factory on the entity (`Order::create(...)`) or a mapper service.
- Collection mapping: `array_map(OrderResponse::fromEntity(...), $orders)` — first-class callable syntax.

## Configuration

- App wiring lives in `config/services.yaml`; rely on autowiring + autoconfiguration.
- Group related settings with `#[Autowire]` bound parameters or a typed config object — not scattered `%env()%` reads inside services.
- Infrastructure-only bean definitions (HTTP clients, factories) go in `config/services.yaml`, never inside a service class.

## Cross-cutting

- Logging: inject `Psr\Log\LoggerInterface` — never `error_log()` / `dump()` in committed code.
- Validation: `#[MapRequestPayload]` validates the DTO automatically; custom rules via constraint validators.
- Exception handling: one `#[AsEventListener(KernelEvents::EXCEPTION)]` listener — never `try/catch` in controllers for domain errors.

## Gotchas

- Agent injects `ContainerInterface` / uses `$this->get()` — use constructor injection of the concrete dependency.
- Agent returns a Doctrine entity from a controller — map to a response DTO (or apply serialization groups).
- Agent injects a repository into a controller — go through a service.
- Agent puts `flush()` and transaction logic in the controller — move it to the service.
- Agent builds a god service (`OrderAndInventoryService`) — split by aggregate.
- Agent decodes JSON manually with `json_decode($request->getContent())` — use `#[MapRequestPayload]` with a DTO.
- Agent reuses one DTO for request and response — keep them separate.
- Agent `try/catch`es domain exceptions in the controller — let the exception listener map them.
