---
name: laravel-queue-patterns
description: Best practices for Laravel queues including job structure, batching, chaining, middleware, retry strategies, and error handling.
---

# Laravel Queue Patterns

## Job Structure

```php
<?php

namespace App\Jobs;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessOrder implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public readonly Order $order,
    ) {}

    public function handle(PaymentGateway $gateway): void
    {
        $gateway->charge($this->order);

        $this->order->update(['status' => 'processed']);
    }

    public function failed(\Throwable $exception): void
    {
        $this->order->update(['status' => 'failed']);

        // Notify admin, log, etc.
    }
}
```

## Dispatch Patterns

```php
// ✅ Standard dispatch
ProcessOrder::dispatch($order);

// ✅ Dispatch to specific queue/connection
ProcessOrder::dispatch($order)
    ->onQueue('payments')
    ->onConnection('redis');

// ✅ Delayed dispatch
ProcessOrder::dispatch($order)->delay(now()->addMinutes(5));

// ✅ Conditional dispatch
ProcessOrder::dispatchIf($order->isPaid(), $order);
ProcessOrder::dispatchUnless($order->isCancelled(), $order);

// ✅ Dispatch after database transaction commits
ProcessOrder::dispatch($order)->afterCommit();

// ❌ Dispatching inside a transaction without afterCommit
DB::transaction(function () use ($order) {
    $order->save();
    ProcessOrder::dispatch($order); // Job may run before commit
});

// ✅ Safe inside transactions
DB::transaction(function () use ($order) {
    $order->save();
    ProcessOrder::dispatch($order)->afterCommit();
});
```

## Job Middleware

```php
use Illuminate\Queue\Middleware\RateLimited;
use Illuminate\Queue\Middleware\ThrottlesExceptions;
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProcessOrder implements ShouldQueue
{
    public function middleware(): array
    {
        return [
            // Rate limit to 10 jobs per minute
            new RateLimited('orders'),

            // Prevent overlapping by order ID
            (new WithoutOverlapping($this->order->id))
                ->releaseAfter(60)
                ->expireAfter(300),

            // Throttle on exceptions - wait 5 min after 3 exceptions
            (new ThrottlesExceptions(3, 5))
                ->backoff(5),
        ];
    }
}

// Define rate limiter in AppServiceProvider
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('orders', function ($job) {
    return Limit::perMinute(10);
});
```

## Job Chaining

```php
use Illuminate\Support\Facades\Bus;

// ✅ Sequential execution - next job runs only if previous succeeds
Bus::chain([
    new ValidateOrder($order),
    new ChargePayment($order),
    new SendConfirmation($order),
    new UpdateInventory($order),
])->onQueue('orders')->dispatch();

// ✅ With catch callback
Bus::chain([
    new ValidateOrder($order),
    new ChargePayment($order),
])->catch(function (\Throwable $e) use ($order) {
    $order->update(['status' => 'failed']);
})->dispatch();
```

## Job Batching

```php
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new ProcessCsvChunk($file, 0, 1000),
    new ProcessCsvChunk($file, 1000, 2000),
    new ProcessCsvChunk($file, 2000, 3000),
])
->then(function (Batch $batch) {
    // All jobs completed successfully
    Notification::send($user, new ImportComplete());
})
->catch(function (Batch $batch, \Throwable $e) {
    // First batch job failure detected
})
->finally(function (Batch $batch) {
    // Batch finished (success or failure)
    Storage::delete($file);
})
->name('CSV Import')
->onQueue('imports')
->allowFailures()
->dispatch();

// Check batch progress
$batch = Bus::findBatch($batchId);
echo $batch->progress(); // Percentage complete
```

Jobs in a batch must use the `Illuminate\Bus\Batchable` trait.

## Unique Jobs

```php
use Illuminate\Contracts\Queue\ShouldBeUnique;

class RecalculateReport implements ShouldQueue, ShouldBeUnique
{
    public function __construct(
        public readonly int $reportId,
    ) {}

    // Unique for 1 hour
    public int $uniqueFor = 3600;

    // Custom unique ID
    public function uniqueId(): string
    {
        return (string) $this->reportId;
    }
}
```

## Retry Strategies

```php
class ProcessWebhook implements ShouldQueue
{
    // ✅ Fixed number of attempts
    public int $tries = 5;

    // ✅ Or retry until a time limit
    public function retryUntil(): \DateTime
    {
        return now()->addHours(2);
    }

    // ✅ Max exceptions before marking failed (allows manual releases)
    public int $maxExceptions = 3;

    // ✅ Exponential backoff (seconds between retries)
    public array $backoff = [10, 60, 300]; // 10s, 1m, 5m

    // ✅ Timeout per attempt
    public int $timeout = 120;

    public function handle(): void
    {
        // If an unrecoverable error occurs, fail immediately
        if ($this->isInvalid()) {
            $this->fail('Invalid webhook payload.');
            return;
        }

        // Process...
    }
}
```

## Idempotency Patterns

```php
class ChargePayment implements ShouldQueue
{
    public function handle(PaymentGateway $gateway): void
    {
        // ✅ Check if already processed before acting
        if ($this->order->payment_id) {
            return; // Already charged, skip
        }

        $payment = $gateway->charge($this->order->total);

        // ✅ Use atomic update to prevent double processing
        $affected = Order::where('id', $this->order->id)
            ->whereNull('payment_id')
            ->update(['payment_id' => $payment->id]);

        if ($affected === 0) {
            return; // Another worker already processed this
        }
    }
}
```

## Testing Queues

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Queue;

// ✅ Assert job was dispatched
public function test_order_dispatches_processing_job(): void
{
    Queue::fake();

    $order = Order::factory()->create();
    $order->process();

    Queue::assertPushed(ProcessOrder::class, function ($job) use ($order) {
        return $job->order->id === $order->id;
    });
}

// ✅ Assert chain
public function test_order_dispatches_chain(): void
{
    Bus::fake();

    $order = Order::factory()->create();
    $order->fulfill();

    Bus::assertChained([
        ValidateOrder::class,
        ChargePayment::class,
        SendConfirmation::class,
    ]);
}

// ✅ Assert batch
public function test_import_dispatches_batch(): void
{
    Bus::fake();

    (new CsvImporter)->import($file);

    Bus::assertBatched(function ($batch) {
        return $batch->jobs->count() === 3
            && $batch->jobs->every(fn ($job) => $job instanceof ProcessCsvChunk);
    });
}

// ✅ Execute job to test handler logic
public function test_process_order_charges_payment(): void
{
    $order = Order::factory()->create();

    ProcessOrder::dispatchSync($order);

    $this->assertNotNull($order->fresh()->payment_id);
}
```

## Checklist

- [ ] Jobs implement ShouldQueue and use standard traits
- [ ] Jobs accept only serializable data (models, primitives)
- [ ] Retry strategy configured ($tries, $backoff, retryUntil)
- [ ] failed() method handles cleanup and notifications
- [ ] afterCommit() used when dispatching inside transactions
- [ ] Job middleware used for rate limiting and overlap prevention
- [ ] Chains used for sequential dependent operations
- [ ] Batches used for parallel independent operations
- [ ] Jobs are idempotent (safe to run multiple times)
- [ ] ShouldBeUnique used to prevent duplicate jobs
- [ ] Queue and Bus fakes used in tests
