---
name: doctrine-query-optimization
description: >
  Use when writing Doctrine queries, fixing N+1 problems, paginating large result sets,
  building read models, or tuning DQL/query builder performance. Use when the task mentions
  N+1, slow query, pagination, DQL, hydration, or read model.
---

# Doctrine Query Optimization (Symfony)

## N+1: identify and fix

One query for the parents + one query per parent for a lazy association = **N+1**. It hides in loops that touch a lazy relation.

```php
// ❌ N+1 — every $order->getItems() fires a query
$orders = $repo->findBy(['status' => OrderStatus::Active]);
foreach ($orders as $order) {
    $total = count($order->getItems());   // SELECT ... WHERE order_id = ? — N times
}
```

**Fix A — `JOIN FETCH` (when you need the entities):**

```php
public function findActiveWithItems(): array
{
    return $this->createQueryBuilder('o')
        ->addSelect('i')                       // hydrate items in the same query
        ->leftJoin('o.items', 'i')
        ->andWhere('o.status = :status')
        ->setParameter('status', OrderStatus::Active)
        ->getQuery()
        ->getResult();
}
```

When fetch-joining a to-many and paginating, use Doctrine's `Paginator` (it switches to a windowed two-query strategy so `setMaxResults` stays correct):

```php
$query = $qb->setFirstResult($offset)->setMaxResults($limit)->getQuery();
$paginator = new Paginator($query, fetchJoinCollection: true);
```

**Fix B — read-model DTO (when you only need to display):** don't hydrate entities at all.

```php
public function summaries(OrderStatus $status): array
{
    return $this->createQueryBuilder('o')
        ->select(sprintf(
            'NEW %s(o.id, o.customerEmail, o.status, o.createdAt)',
            OrderSummary::class,
        ))
        ->andWhere('o.status = :status')
        ->setParameter('status', $status)
        ->getQuery()
        ->getResult();   // array of OrderSummary DTOs — no managed entities, no lazy loading
}
```

## Hydration modes

- Default `getResult()` returns managed entities — most expensive (UoW tracks them).
- `getArrayResult()` / `getScalarResult()` — when you only read and never mutate.
- DQL `NEW` (DTO hydration) — best for read endpoints; immutable, no identity map cost.
- For read-only list endpoints, prefer DTOs over entities every time.

## Pagination

```php
// Offset pagination (fine for early pages)
$qb->setFirstResult($page * $perPage)->setMaxResults($perPage);
```

`OFFSET` scans and discards every skipped row — page 5,000 reads 100,000 rows to return 20. For deep pages / infinite scroll, use **keyset (seek) pagination**: filter by the last seen sortable key.

```php
// ✅ Keyset — constant time regardless of depth. UUID v7 / createdAt are sortable.
public function pageAfter(?Uuid $lastId, int $limit): array
{
    $qb = $this->createQueryBuilder('o')
        ->orderBy('o.id', 'DESC')
        ->setMaxResults($limit);

    if ($lastId !== null) {
        $qb->andWhere('o.id < :lastId')->setParameter('lastId', $lastId, 'uuid');
    }

    return $qb->getQuery()->getResult();
}
```

Index the sort key. With a tie-prone sort (`createdAt`), order by `(createdAt DESC, id DESC)` and seek on the tuple so the cursor is stable.

## Batch processing large sets

Don't load a million rows into memory. Iterate and clear the identity map periodically.

```php
$query = $em->createQuery('SELECT o FROM App\Entity\Order o WHERE o.status = :s')
    ->setParameter('s', OrderStatus::Pending);

$batchSize = 500;
$i = 0;
foreach ($query->toIterable() as $order) {
    $order->markStale();
    if (++$i % $batchSize === 0) {
        $em->flush();
        $em->clear();   // detach everything, release memory
    }
}
$em->flush();
$em->clear();
```

For inserts, enable JDBC-style batching and flush in chunks. Note: `GenerationType.IDENTITY`-style auto-increment forces a round-trip per row; UUID v7 keeps batching intact (another reason to use UUIDs).

## Other wins

- Select only the columns you need with **partial DTO hydration**, not whole entities.
- Use `EXISTS`/`SELECT 1 … setMaxResults(1)` for existence checks, not `count()` of loaded rows.
- Add a second-level / result cache only for genuinely hot, rarely-changing queries — measure first.
- Profile with the Symfony Profiler's Doctrine panel; watch query count and duplicate queries.

## Gotchas

- Agent writes a loop that touches a lazy association — fetch-join it or use a read-model DTO.
- Agent fetch-joins a to-many **and** paginates with plain `setMaxResults` — wrap in `Paginator(fetchJoinCollection: true)`.
- Agent hydrates full entities for a read-only list endpoint — use DQL `NEW` DTO hydration.
- Agent uses `OFFSET` for deep pagination — switch to keyset/seek on a sortable indexed key.
- Agent loads huge result sets into an array — use `toIterable()` + periodic `flush()`/`clear()`.
- Agent calls `count($repo->findBy(...))` to check existence — use an `EXISTS`/`SELECT 1` query.
- Agent forgets to index the column used in `WHERE`/`ORDER BY` for keyset — add the index.
