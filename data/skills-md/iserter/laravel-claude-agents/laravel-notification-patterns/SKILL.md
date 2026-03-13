---
name: laravel-notification-patterns
description: Best practices for Laravel notifications including multi-channel delivery, mail and database notifications, queueing, and on-demand recipients.
---

# Notification Patterns

## Notification Class Structure

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class OrderShipped extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public readonly Order $order,
    ) {}

    public function via(object $notifiable): array
    {
        return ['mail', 'database', 'broadcast'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('Order Shipped')
            ->greeting("Hello {$notifiable->name}!")
            ->line("Your order #{$this->order->number} has been shipped.")
            ->action('Track Order', url("/orders/{$this->order->id}/track"))
            ->line('Thank you for your purchase!');
    }

    public function toArray(object $notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->number,
            'message' => "Order #{$this->order->number} has been shipped.",
        ];
    }
}
```

## Mail Notifications

### MailMessage Builder

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('noreply@example.com', 'App Name')
        ->subject('Invoice Paid')
        ->greeting('Hello!')
        ->line('One of your invoices has been paid.')
        ->lineIf($this->amount > 100, 'This was a large payment.')
        ->action('View Invoice', $this->invoiceUrl)
        ->line('Thank you for using our application!')
        ->salutation('Regards, The Team');
}
```

### Markdown Mail Templates

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Order Confirmation')
        ->markdown('mail.order.confirmed', [
            'order' => $this->order,
            'url' => route('orders.show', $this->order),
        ]);
}
```

```blade
{{-- resources/views/mail/order/confirmed.blade.php --}}
<x-mail::message>
# Order Confirmed

Your order **#{{ $order->number }}** has been confirmed.

<x-mail::table>
| Item       | Quantity | Price   |
|:-----------|:---------|:--------|
@foreach ($order->items as $item)
| {{ $item->name }} | {{ $item->quantity }} | ${{ $item->price }} |
@endforeach
</x-mail::table>

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

### Attachments

```php
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Monthly Report')
        ->line('Please find your monthly report attached.')
        ->attach($this->reportPath, [
            'as' => 'report.pdf',
            'mime' => 'application/pdf',
        ])
        ->attachData($this->csvContent, 'data.csv', [
            'mime' => 'text/csv',
        ]);
}
```

## Database Notifications

### Setup

```bash
php artisan notifications:table
php artisan migrate
```

```php
// Model must use Notifiable trait
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

### Storing Notifications

```php
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
        'message' => "Invoice #{$this->invoice->number} paid.",
    ];
}
```

### Reading and Managing Notifications

```php
// Get all notifications
$notifications = $user->notifications;

// Get unread notifications
$unread = $user->unreadNotifications;

// Mark as read
$user->unreadNotifications->markAsRead();

// Mark a single notification as read
$notification->markAsRead();

// Mark as unread
$notification->markAsUnread();

// Delete old notifications
$user->notifications()->where('created_at', '<', now()->subMonths(3))->delete();
```

## Broadcast Notifications

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

public function toBroadcast(object $notifiable): BroadcastMessage
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}

// Custom channel name (optional)
public function broadcastType(): string
{
    return 'invoice.paid';
}
```

```javascript
// Listening with Echo
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
        console.log(notification.invoice_id);
    });
```

## Slack Notifications

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text("Order #{$this->order->number} shipped")
        ->headerBlock("Order Shipped")
        ->sectionBlock(function (SectionBlock $block) {
            $block->text("Order *#{$this->order->number}* has been shipped.");
            $block->field("*Customer:*\n{$this->order->customer_name}")->markdown();
            $block->field("*Tracking:*\n{$this->order->tracking_number}")->markdown();
        });
}
```

## Queueing Notifications

### Basic Queueing

```php
// ✅ Implement ShouldQueue
class OrderShipped extends Notification implements ShouldQueue
{
    use Queueable;

    // Per-channel queue configuration
    public function viaQueues(): array
    {
        return [
            'mail' => 'mail-queue',
            'database' => 'default',
            'slack' => 'slack-queue',
        ];
    }
}
```

### After Commit

```php
// ✅ Only dispatch after database transaction commits
class OrderShipped extends Notification implements ShouldQueue
{
    use Queueable;

    public $afterCommit = true;
}
```

### Delayed Notifications

```php
$user->notify(
    (new OrderShipped($order))->delay([
        'mail' => now()->addMinutes(5),
        'database' => now(),
    ])
);
```

### Retry and Failure Handling

```php
class OrderShipped extends Notification implements ShouldQueue
{
    use Queueable;

    public $tries = 3;
    public $backoff = [30, 60, 120];

    public function failed(\Throwable $exception): void
    {
        // Handle failure (log, alert, etc.)
        Log::error('OrderShipped notification failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

## Conditional Sending

```php
public function shouldSend(object $notifiable, string $channel): bool
{
    // Don't send mail if user disabled email notifications
    if ($channel === 'mail') {
        return $notifiable->prefers_email_notifications;
    }

    // Don't notify about small amounts
    return $this->invoice->amount > 10;
}
```

## On-Demand Notifications

```php
use Illuminate\Support\Facades\Notification;

// ✅ Send to an email address without a user model
Notification::route('mail', 'admin@example.com')
    ->route('slack', '#alerts')
    ->notify(new ServerHealthReport($server));

// ✅ With recipient name
Notification::route('mail', ['admin@example.com' => 'Admin User'])
    ->notify(new WeeklyDigest());
```

## Sending Notifications

```php
use Illuminate\Support\Facades\Notification;

// Via the Notifiable trait
$user->notify(new OrderShipped($order));

// Via the Notification facade (multiple recipients)
Notification::send($users, new OrderShipped($order));

// ❌ Don't loop to send individually
foreach ($users as $user) {
    $user->notify(new OrderShipped($order)); // Inefficient
}

// ✅ Send to a collection
Notification::send(User::all(), new SystemAnnouncement($message));
```

## Custom Notification Channels

```php
class SmsChannel
{
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toSms($notifiable);
        $phone = $notifiable->routeNotificationFor('sms', $notification);

        // Send SMS via your provider
        SmsProvider::send($phone, $message);
    }
}

// In the notification
public function via(object $notifiable): array
{
    return [SmsChannel::class, 'database'];
}

public function toSms(object $notifiable): string
{
    return "Your order #{$this->order->number} has been shipped.";
}

// On the notifiable model
public function routeNotificationForSms(Notification $notification): string
{
    return $this->phone_number;
}
```

## Testing Notifications

```php
use Illuminate\Support\Facades\Notification;

public function test_order_shipped_notification_is_sent(): void
{
    Notification::fake();

    // Perform action that triggers notification
    $order = Order::factory()->create();
    $order->ship();

    // Assert notification was sent
    Notification::assertSentTo(
        $order->user,
        OrderShipped::class,
        function (OrderShipped $notification, array $channels) use ($order) {
            return $notification->order->id === $order->id
                && in_array('mail', $channels)
                && in_array('database', $channels);
        }
    );

    // Assert not sent to other users
    Notification::assertNotSentTo(
        User::factory()->create(),
        OrderShipped::class,
    );

    // Assert count
    Notification::assertSentToTimes($order->user, OrderShipped::class, 1);

    // Assert nothing sent
    Notification::assertNothingSent();
}
```

### Testing Mail Content

```php
public function test_order_shipped_mail_content(): void
{
    $order = Order::factory()->create();
    $notification = new OrderShipped($order);

    $mail = $notification->toMail($order->user);

    $this->assertEquals('Order Shipped', $mail->subject);
    $this->assertStringContainsString($order->number, $mail->render());
}
```

## Checklist

- [ ] Notification class uses appropriate channels via `via()`
- [ ] Mail notifications use MailMessage builder or markdown templates
- [ ] Database notifications table is migrated
- [ ] `toArray()` returns only serializable data for database storage
- [ ] Long-running notifications implement `ShouldQueue`
- [ ] Queue names configured per channel with `viaQueues()`
- [ ] `afterCommit` set when sending within database transactions
- [ ] `shouldSend()` used for conditional delivery logic
- [ ] On-demand notifications used for non-model recipients
- [ ] Bulk sending uses `Notification::send()` instead of loops
- [ ] Notification tests use `Notification::fake()`
- [ ] Retry and failure handling configured for queued notifications
