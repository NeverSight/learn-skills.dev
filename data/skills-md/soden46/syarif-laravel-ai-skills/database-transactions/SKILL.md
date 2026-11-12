---
name: database-transactions
description: Keep Laravel writes atomic and consistent with transactions, locks, retries, idempotency, side-effect boundaries, and after-commit dispatch.
tags:
  - laravel
  - php
---

# Database Transactions

Use database transactions for write operations that must be atomic.

This is the canonical transaction skill. It consolidates the former `transactions-and-consistency` topic.

Transaction boundaries usually belong inside an Action or Service, not spread across controllers.

## Required Transaction Cases

Use `DB::transaction()` when a workflow:

- writes multiple related records;
- updates counters, balances, inventory, or state machines;
- coordinates audit records with domain writes;
- creates records and related child rows;
- must not partially succeed.

```php
final class CreateRecord
{
    public function handle(User $actor, array $data): Record
    {
        return DB::transaction(function () use ($actor, $data) {
            $record = Record::create([
                'owner_id' => $actor->id,
                'name' => $data['name'],
            ]);

            $record->items()->createMany($data['items'] ?? []);

            return $record->fresh(['items']);
        });
    }
}
```

## Filesystem Side Effects

Database rollbacks do not roll back files. Track stored paths and clean them up when the database write fails.

```php
$storedPaths = [];

try {
    DB::transaction(function () use ($request, &$storedPaths) {
        $record = Record::create([...]);

        foreach ($request->file('attachments', []) as $file) {
            $storedPaths[] = $file->store("records/{$record->id}", 'public');
        }
    });
} catch (Throwable $exception) {
    Storage::disk('public')->delete($storedPaths);

    throw $exception;
}
```

For delete flows, prefer committing database/audit changes first, then deleting files after the successful transaction unless the product explicitly requires the opposite failure mode.

## Locks And Retries

Use row locks for concurrent updates to shared counters, balances, or ordered state.

```php
DB::transaction(function () use ($recordId) {
    $record = Record::query()
        ->whereKey($recordId)
        ->lockForUpdate()
        ->firstOrFail();

    $record->increment('sequence');
});
```

Keep transactions short. Make retry behavior idempotent when deadlock retries are used.

## After-Commit Work

Dispatch queued jobs/events after commit when they depend on committed records.

Do not hold a database transaction open during slow HTTP calls, mail delivery, document generation, or other remote side effects. Persist the state needed to continue, commit it, and dispatch after commit. Use an outbox or equivalent durable handoff when losing the side effect would be unacceptable.

## Idempotency And Consistency

- Protect retried commands, webhooks, and queued jobs with a stable idempotency key or a domain state check.
- Enforce uniqueness in the database when duplicate prevention is a data invariant.
- Make retry behavior return or recover the original result instead of repeating side effects.
- Keep lock ordering consistent across workflows to reduce deadlocks.
- Use optimistic checks when conflicts should be reported rather than serialized.
- Prefer explicit compensating behavior for filesystem or provider operations that cannot participate in the database transaction.

Test:

- success path;
- rollback path;
- duplicate or retried execution;
- concurrent updates when locking matters;
- filesystem cleanup when applicable;
- after-commit behavior for important workflows.

## Context Efficiency

Layer: 3 (Implementation)

Load this skill only when writes need atomicity or consistency. Do not load with unrelated skills. Keep transactions short, idempotent, and after-commit for side effects. No open transaction during slow HTTP calls or mail delivery.
