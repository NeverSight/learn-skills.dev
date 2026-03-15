---
name: laravel-event-driven-architecture
description: Best practices for Laravel events and listeners including event discovery, queued listeners, subscribers, and model events for decoupled architecture.
---

# Laravel Event-Driven Architecture

## Event Class Structure

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderPlaced
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public readonly Order $order,
    ) {}
}
```

## Listener Class Structure

```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;

class SendOrderConfirmation
{
    public function handle(OrderPlaced $event): void
    {
        $event->order->user->notify(
            new OrderConfirmationNotification($event->order)
        );
    }
}
```

## Automatic Listener Discovery

Laravel auto-discovers listeners when they are in the `App\Listeners` directory and have a `handle` method type-hinting an event. No manual registration needed.

```php
// ✅ Auto-discovered - just create the class with a typed handle method
class SendOrderConfirmation
{
    public function handle(OrderPlaced $event): void { /* ... */ }
}

// ✅ One listener handling multiple events
class AuditLogger
{
    public function handleOrderPlaced(OrderPlaced $event): void { /* ... */ }
    public function handleOrderCancelled(OrderCancelled $event): void { /* ... */ }
}

// ❌ Won't be discovered - missing type hint
class SendOrderConfirmation
{
    public function handle($event): void { /* ... */ }
}
```

## Dispatching Events

```php
// ✅ Using static dispatch
OrderPlaced::dispatch($order);

// ✅ Using event helper
event(new OrderPlaced($order));

// ❌ Calling listeners directly instead of dispatching events
(new SendOrderConfirmation)->handle($order); // Tight coupling
```

## Queued Listeners

```php
use Illuminate\Contracts\Queue\ShouldQueue;

// ✅ Listener runs asynchronously on the queue
class GenerateInvoicePdf implements ShouldQueue
{
    public string $queue = 'invoices';
    public int $tries = 3;
    public array $backoff = [10, 60];

    public function handle(OrderPlaced $event): void
    {
        $pdf = PdfGenerator::fromOrder($event->order);
        Storage::put("invoices/{$event->order->id}.pdf", $pdf);
    }

    public function failed(OrderPlaced $event, \Throwable $exception): void
    {
        // Handle failure
    }

    // Conditionally handle
    public function shouldQueue(OrderPlaced $event): bool
    {
        return $event->order->total > 0;
    }
}
```

## ShouldQueueAfterCommit

```php
use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;

// ✅ Only dispatched to queue after the database transaction commits
class UpdateSearchIndex implements ShouldQueueAfterCommit
{
    public function handle(OrderPlaced $event): void
    {
        SearchIndex::update('orders', $event->order);
    }
}
```

## ShouldDispatchAfterCommit for Transaction Safety

```php
// ✅ Event only dispatches after the surrounding transaction commits
class OrderPlaced
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $afterCommit = true;

    public function __construct(
        public readonly Order $order,
    ) {}
}

// This prevents listeners from running on data that might be rolled back
DB::transaction(function () {
    $order = Order::create($data);
    OrderPlaced::dispatch($order); // Dispatched only after commit
});
```

## Event Subscribers

```php
<?php

namespace App\Listeners;

use Illuminate\Events\Dispatcher;

class OrderEventSubscriber
{
    public function handleOrderPlaced(OrderPlaced $event): void
    {
        // Log order creation
    }

    public function handleOrderShipped(OrderShipped $event): void
    {
        // Send shipping notification
    }

    public function handleOrderCancelled(OrderCancelled $event): void
    {
        // Process refund
    }

    public function subscribe(Dispatcher $events): array
    {
        return [
            OrderPlaced::class => 'handleOrderPlaced',
            OrderShipped::class => 'handleOrderShipped',
            OrderCancelled::class => 'handleOrderCancelled',
        ];
    }
}

// Register in EventServiceProvider
protected $subscribe = [
    OrderEventSubscriber::class,
];
```

## Model Events and Observers

```php
<?php

namespace App\Observers;

use App\Models\Order;

class OrderObserver
{
    public function creating(Order $order): void
    {
        $order->reference = Order::generateReference();
    }

    public function created(Order $order): void
    {
        OrderPlaced::dispatch($order);
    }

    public function updating(Order $order): void
    {
        if ($order->isDirty('status') && $order->status === 'cancelled') {
            $order->cancelled_at = now();
        }
    }

    public function deleted(Order $order): void
    {
        Storage::deleteDirectory("orders/{$order->id}");
    }
}

// Register via model attribute (Laravel 11+)
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy(OrderObserver::class)]
class Order extends Model
{
    // ...
}
```

## When to Use Events vs Direct Calls

```php
// ✅ USE EVENTS when:
// - Multiple side effects from one action
// - Side effects may change independently
// - Side effects can be async
class OrderService
{
    public function place(Order $order): void
    {
        $order->save();

        // Multiple listeners handle: email, invoice, inventory, analytics
        OrderPlaced::dispatch($order);
    }
}

// ✅ USE DIRECT CALLS when:
// - Core business logic that must succeed together
// - Single clear responsibility
// - Synchronous transactional requirement
class OrderService
{
    public function place(Order $order): void
    {
        DB::transaction(function () use ($order) {
            $order->save();
            $this->inventoryService->reserve($order); // Must succeed together
        });

        OrderPlaced::dispatch($order); // Side effects via events
    }
}

// ❌ Don't use events for core logic that must not fail silently
// ❌ Don't use events when you need the return value
```

## Testing Events

```php
use Illuminate\Support\Facades\Event;

// ✅ Assert events were dispatched
public function test_placing_order_fires_event(): void
{
    Event::fake();

    $order = Order::factory()->create();
    $this->orderService->place($order);

    Event::assertDispatched(OrderPlaced::class, function ($event) use ($order) {
        return $event->order->id === $order->id;
    });
}

// ✅ Assert event not dispatched
public function test_cancelled_order_does_not_fire_placed(): void
{
    Event::fake();

    $order = Order::factory()->cancelled()->create();
    $this->orderService->place($order);

    Event::assertNotDispatched(OrderPlaced::class);
}

// ✅ Fake only specific events, let others run normally
public function test_order_with_real_listeners(): void
{
    Event::fake([OrderShipped::class]);

    // OrderPlaced listeners will run, OrderShipped will be faked
}

// ✅ Test listener directly
public function test_send_confirmation_listener(): void
{
    Notification::fake();

    $event = new OrderPlaced(Order::factory()->create());
    (new SendOrderConfirmation)->handle($event);

    Notification::assertSentTo($event->order->user, OrderConfirmationNotification::class);
}
```

## Checklist

- [ ] Events are simple data-carrying objects (no business logic)
- [ ] Listeners have a single responsibility each
- [ ] Queued listeners used for slow operations (email, PDF, API calls)
- [ ] ShouldQueueAfterCommit or $afterCommit used for transaction safety
- [ ] Auto-discovery relied on instead of manual registration where possible
- [ ] Observers used sparingly and only for model lifecycle hooks
- [ ] Core business logic not hidden inside event listeners
- [ ] Events tested with Event::fake and assertDispatched
- [ ] Listeners tested in isolation with direct handle() calls
- [ ] shouldQueue() used to conditionally skip queuing
