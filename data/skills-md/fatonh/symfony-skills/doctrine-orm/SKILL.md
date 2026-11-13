---
name: doctrine-orm
description: >
  Use when creating Doctrine ORM 3 entities, associations, repositories, enums, or UUID
  identifiers in Symfony. Defines entity conventions, attribute mapping, fetch strategy,
  and repository structure. Use when the task mentions entity, Doctrine, repository,
  association, or mapping.
---

# Doctrine ORM 3 (Symfony)

## Entity conventions

```php
#[ORM\Entity(repositoryClass: OrderRepository::class)]
#[ORM\Table(name: 'orders')]
class Order
{
    #[ORM\Id]
    #[ORM\Column(type: UuidType::NAME, unique: true)]   // symfony/uid type
    private Uuid $id;

    #[ORM\Column(length: 255)]
    private string $customerEmail;

    #[ORM\Column(enumType: OrderStatus::class)]          // backed enum, stored as string
    private OrderStatus $status;

    /** @var Collection<int, OrderItem> */
    #[ORM\OneToMany(targetEntity: OrderItem::class, mappedBy: 'order', cascade: ['persist'], orphanRemoval: true)]
    private Collection $items;

    #[ORM\Column(type: Types::DATETIME_IMMUTABLE)]
    private \DateTimeImmutable $createdAt;

    #[ORM\Column(type: Types::DATETIME_IMMUTABLE, nullable: true)]
    private ?\DateTimeImmutable $updatedAt = null;

    // private constructor — force creation through a named factory
    private function __construct(string $customerEmail)
    {
        $this->id = Uuid::v7();                            // sortable UUID
        $this->customerEmail = $customerEmail;
        $this->status = OrderStatus::Pending;
        $this->items = new ArrayCollection();
        $this->createdAt = new \DateTimeImmutable();
    }

    public static function create(string $customerEmail): self
    {
        return new self($customerEmail);
    }

    // Behavior, not a setter
    public function addItem(Uuid $productId, int $quantity): void
    {
        $this->items->add(new OrderItem($this, $productId, $quantity));
    }

    public function getId(): Uuid { return $this->id; }
    public function getStatus(): OrderStatus { return $this->status; }
    /** @return Collection<int, OrderItem> */
    public function getItems(): Collection { return $this->items; }
}
```

## Rules

- **IDs:** `symfony/uid` `Uuid` (prefer UUID v7 — time-ordered, index-friendly). Never expose auto-increment integers in a public API.
- **Enums:** `#[ORM\Column(enumType: OrderStatus::class)]` with a **backed** enum (string). Never store the ordinal/int.
- **Dates:** `Types::DATETIME_IMMUTABLE` + `\DateTimeImmutable`. Never mutable `\DateTime`.
- **Collections:** initialize in the constructor (`new ArrayCollection()`), typed `Collection<int, X>`. Never null.
- **No public setters** — expose behavior methods; getters are fine.
- **Factory creation** — private constructor + named static factory (`Order::create()`), so an entity can't be built in an invalid state.
- **`declare(strict_types=1);`** in every file.

## Associations & fetch strategy

- `#[ORM\ManyToOne]` and `#[ORM\ManyToMany]` are **LAZY** by default — keep it that way. Never `fetch: 'EAGER'`.
- The **owning side** holds the FK column (`#[ORM\JoinColumn]`); the inverse side uses `mappedBy`.
- Keep both sides in sync with a helper on the owning aggregate.

```php
// Child owns the FK
#[ORM\ManyToOne(targetEntity: Order::class, inversedBy: 'items')]
#[ORM\JoinColumn(name: 'order_id', nullable: false, onDelete: 'CASCADE')]
private Order $order;
```

```php
// ❌ BAD — eager fetch loads the whole graph on every query
#[ORM\ManyToOne(fetch: 'EAGER')]
private Customer $customer;
```

Use `cascade: ['persist']` deliberately; avoid `cascade: ['remove']` — prefer `orphanRemoval` or explicit deletion so you don't accidentally wipe shared records.

## Repositories

```php
/** @extends ServiceEntityRepository<Order> */
final class OrderRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Order::class);
    }

    public function save(Order $order, bool $flush = false): void
    {
        $this->getEntityManager()->persist($order);
        if ($flush) {
            $this->getEntityManager()->flush();
        }
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

- Type the repository with `@extends ServiceEntityRepository<Entity>` so static analysis knows the return types.
- `exists*` checks: `SELECT 1 … setMaxResults(1)` is faster than loading the entity.
- Never put business logic in repositories (see `layered-architecture`).

## Value objects: embeddables & custom types

```php
#[ORM\Embedded(class: Address::class)]
private Address $shippingAddress;
```

For single-column value objects (`Email`, `Money`), write a custom DBAL type so the model stays rich and the schema stays flat.

## Gotchas

- Agent uses `fetch: 'EAGER'` on associations — keep `ManyToOne`/`ManyToMany` LAZY; fetch explicitly when needed (see `doctrine-query-optimization`).
- Agent uses auto-increment `int` IDs — use `symfony/uid` `Uuid` (v7).
- Agent stores enums as int / uses `enumType` with a pure (non-backed) enum — use a string-backed enum.
- Agent adds public setters to entities — use behavior methods + a factory.
- Agent uses mutable `\DateTime` — use `\DateTimeImmutable` with `DATETIME_IMMUTABLE`.
- Agent forgets `orphanRemoval: true` on owning `OneToMany` — orphaned child rows pile up.
- Agent adds `cascade: ['remove']` casually — prefer `orphanRemoval` / explicit deletes to avoid wiping shared rows.
- Agent leaves collections uninitialized — `new ArrayCollection()` in the constructor.
- Agent uses Doctrine annotations (`@ORM\Entity`) — use PHP 8 attributes.
- Agent forgets the `@extends ServiceEntityRepository<Entity>` generic — analysis loses return types.
