---
name: laravel-backend-expert
description: Expert Laravel backend development covering the full ecosystem. Use this skill whenever the user mentions Laravel backend, Laravel application development, Blade views, Livewire, Laravel queues, jobs, events, mail, notifications, file uploads, storage, caching, Redis, Laravel commands, scheduling, middleware, policies, gates, service providers, service classes, repositories, or general Laravel server-side development. Trigger for any non-API Laravel work including web applications, admin panels, and background processing.
---
# Laravel Backend Expert

A comprehensive skill for building production-grade Laravel applications covering the full backend ecosystem: web applications, background processing, real-time features, file handling, caching, and architecture patterns for Laravel 10/11+.

## Core Philosophy

Build Laravel applications that are:
- **Modular** - Service classes, repositories, clean separation of concerns
- **Performant** - Queues, caching, optimized queries
- **Real-time** - Events, broadcasting, notifications
- **Secure** - Authorization, input validation, file handling
- **Maintainable** - Architecture patterns, testing, documentation

---

## Application Architecture

### Layered Architecture

```
app/
├── Console/
│   └── Commands/
│       ├── ProcessReport.php
│       └── CleanupExpiredRecords.php
├── Events/
│   └── UserRegistered.php
├── Exceptions/
│   └── Handler.php
├── Http/
│   ├── Controllers/
│   ├── Middleware/
│   └── Requests/
├── Jobs/
│   └── SendWelcomeEmail.php
├── Listeners/
│   └── SendWelcomeNotification.php
├── Mail/
│   └── WelcomeEmail.php
├── Models/
├── Notifications/
│   └── InvoicePaid.php
├── Policies/
│   └── PostPolicy.php
├── Providers/
│   └── AppServiceProvider.php
├── Repositories/
│   ├── Contracts/
│   │   └── UserRepositoryInterface.php
│   └── UserRepository.php
├── Services/
│   ├── PaymentService.php
│   └── ReportGeneratorService.php
└── View/
    └── Components/
        └── Alert.php
```

---

## Service Classes

Services encapsulate business logic and complex operations.

### Service Pattern

```php
<?php

namespace App\Services;

use App\Models\User;
use App\Repositories\Contracts\UserRepositoryInterface;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Exception;

class UserService
{
    public function __construct(
        protected UserRepositoryInterface $userRepository,
        protected PaymentService $paymentService
    ) {}

    /**
     * Create a new user with related data.
     */
    public function createUser(array $data): User
    {
        return DB::transaction(function () use ($data) {
            $user = $this->userRepository->create([
                'name' => $data['name'],
                'email' => $data['email'],
                'password' => Hash::make($data['password']),
            ]);

            // Assign default role
            $user->assignRole('member');

            // Create related records
            if (isset($data['company'])) {
                $user->company()->create($data['company']);
            }

            // Dispatch events
            event(new UserRegistered($user));

            return $user;
        });
    }

    /**
     * Update user with profile picture handling.
     */
    public function updateUser(User $user, array $data): User
    {
        return DB::transaction(function () use ($user, $data) {
            if (isset($data['profile_picture'])) {
                $data['profile_picture'] = $this->uploadProfilePicture(
                    $data['profile_picture'],
                    $user->profile_picture
                );
            }

            $user->update($data);

            return $user->fresh();
        });
    }

    /**
     * Soft delete user and cleanup.
     */
    public function deleteUser(User $user): void
    {
        DB::transaction(function () use ($user) {
            // Revoke all tokens
            $user->tokens()->delete();

            // Cancel subscriptions
            if ($user->subscription) {
                $this->paymentService->cancelSubscription($user->subscription);
            }

            // Soft delete
            $user->delete();
        });
    }

    protected function uploadProfilePicture($file, ?string $oldPath): string
    {
        if ($oldPath) {
            Storage::disk('public')->delete($oldPath);
        }

        return $file->store('profile-pictures', 'public');
    }
}
```

### Service Provider Registration

```php
<?php

namespace App\Providers;

use App\Repositories\Contracts\UserRepositoryInterface;
use App\Repositories\UserRepository;
use App\Services\PaymentService;
use App\Services\UserService;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // Bind interfaces to implementations
        $this->app->bind(UserRepositoryInterface::class, UserRepository::class);

        // Register singletons
        $this->app->singleton(PaymentService::class, function ($app) {
            return new PaymentService(config('services.stripe.secret'));
        });

        // Register with dependencies
        $this->app->singleton(UserService::class, function ($app) {
            return new UserService(
                $app->make(UserRepositoryInterface::class),
                $app->make(PaymentService::class)
            );
        });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
```

---

## Repository Pattern

Repositories abstract data access logic.

### Repository Interface

```php
<?php

namespace App\Repositories\Contracts;

use App\Models\User;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Collection;

interface UserRepositoryInterface
{
    public function find(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function create(array $data): User;
    public function update(User $user, array $data): bool;
    public function delete(User $user): bool;
    public function getActive(): Collection;
    public function paginate(int $perPage = 15): LengthAwarePaginator;
}
```

### Repository Implementation

```php
<?php

namespace App\Repositories;

use App\Models\User;
use App\Repositories\Contracts\UserRepositoryInterface;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Collection;

class UserRepository implements UserRepositoryInterface
{
    public function find(int $id): ?User
    {
        return User::with(['roles', 'company'])->find($id);
    }

    public function findByEmail(string $email): ?User
    {
        return User::where('email', $email)->first();
    }

    public function create(array $data): User
    {
        return User::create($data);
    }

    public function update(User $user, array $data): bool
    {
        return $user->update($data);
    }

    public function delete(User $user): bool
    {
        return $user->delete();
    }

    public function getActive(): Collection
    {
        return User::where('is_active', true)
            ->orderBy('name')
            ->get();
    }

    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return User::with(['roles'])
            ->orderBy('created_at', 'desc')
            ->paginate($perPage);
    }
}
```

---

## Queues & Jobs

### Creating Jobs

```bash
php artisan make:job ProcessPodcast
```

### Job Class

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The number of times the job may be attempted.
     */
    public int $tries = 3;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     */
    public int $maxExceptions = 3;

    /**
     * The number of seconds the job can run before timing out.
     */
    public int $timeout = 120;

    /**
     * Indicate if the job should be marked as failed on timeout.
     */
    public bool $failOnTimeout = true;

    /**
     * Delete the job if its models no longer exist.
     */
    public bool $deleteWhenMissingModels = true;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public string $format = 'mp3'
    ) {
        $this->onQueue('podcasts');
    }

    /**
     * Calculate the number of seconds to wait before retrying the job.
     */
    public function backoff(): array
    {
        return [10, 30, 60]; // Wait 10s, then 30s, then 60s
    }

    /**
     * Determine the time at which the job should timeout.
     */
    public function retryUntil(): \DateTime
    {
        return now()->addHours(2);
    }

    /**
     * Get the tags that should be assigned to the job.
     */
    public function tags(): array
    {
        return ['podcast:' . $this->podcast->id, 'format:' . $this->format];
    }

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Check if batch is cancelled
        if ($this->batch()?->cancelled()) {
            return;
        }

        // Process the podcast
        $processor->process($this->podcast, $this->format);

        // Update progress
        $this->batch()?->incrementProcessed();
    }

    /**
     * Handle a job failure.
     */
    public function failed(?Throwable $exception): void
    {
        Log::error('Podcast processing failed', [
            'podcast_id' => $this->podcast->id,
            'error' => $exception?->getMessage(),
        ]);

        $this->podcast->update(['status' => 'failed']);
    }

    /**
     * Determine if the job should be dispatched.
     */
    public function shouldQueue(): bool
    {
        return $this->podcast->status !== 'processed';
    }
}
```

### Dispatching Jobs

```php
use App\Jobs\ProcessPodcast;
use App\Jobs\OptimizePodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

// Basic dispatch
ProcessPodcast::dispatch($podcast);

// Dispatch with delay
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(5));

// Dispatch if condition is true
ProcessPodcast::dispatchIf($podcast->needsProcessing(), $podcast);

// Dispatch after response (for long-running tasks)
ProcessPodcast::dispatchAfterResponse($podcast);

// Dispatch synchronously (bypasses queue)
ProcessPodcast::dispatchSync($podcast);

// Job batching
Bus::batch([
    new ProcessPodcast($podcast1),
    new ProcessPodcast($podcast2),
    new OptimizePodcast($podcast1),
])->then(function (Batch $batch) {
    // All jobs completed successfully
    ReleasePodcast::dispatch($batch->id);
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure detected
    Log::error('Batch failed', ['batch_id' => $batch->id]);
})->finally(function (Batch $batch) {
    // Always runs
})->name('Podcast Processing Batch')
  ->onQueue('podcasts')
  ->allowFailures()
  ->dispatch();

// Chain jobs (run sequentially)
Bus::chain([
    new ProcessPodcast($podcast),
    new OptimizePodcast($podcast),
    new ReleasePodcast($podcast),
])->catch(function (Throwable $e) {
    Log::error('Job chain failed');
})->dispatch();
```

### Queue Configuration

```php
// config/queue.php
'connections' => [
    'redis' => [
        'driver' => 'redis',
        'connection' => 'default',
        'queue' => env('REDIS_QUEUE', 'default'),
        'retry_after' => 90,
        'block_for' => 5,
        'after_commit' => true, // Dispatch after DB transaction commits
    ],
],
```

### Running Queue Workers

```bash
# Basic worker
php artisan queue:work

# With options
php artisan queue:work redis --queue=high,default,low --tries=3 --timeout=60

# Process a single job
php artisan queue:work --once

# Process all jobs and stop
php artisan queue:work --stop-when-empty

# Daemon listener (production)
php artisan queue:listen redis --queue=high,default

# Restart all workers after deployment
php artisan queue:restart

# Monitor queue health
php artisan queue:monitor redis:default,redis:high
```

---

## Events & Listeners

### Creating Events & Listeners

```bash
php artisan make:event UserRegistered
php artisan make:listener SendWelcomeEmail --event=UserRegistered
```

### Event Class

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class UserRegistered
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
        public bool $sendWelcomeEmail = true
    ) {}

    /**
     * Get the tags that should be assigned to the event.
     */
    public function tags(): array
    {
        return ['user:' . $this->user->id];
    }
}
```

### Listener Class

```php
<?php

namespace App\Listeners;

use App\Events\UserRegistered;
use App\Mail\WelcomeEmail;
use App\Notifications\NewUserNotification;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Facades\Mail;

class SendWelcomeEmail implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * The number of times the listener may be attempted.
     */
    public int $tries = 3;

    /**
     * Create the event listener.
     */
    public function __construct()
    {
        //
    }

    /**
     * Handle the event.
     */
    public function handle(UserRegistered $event): void
    {
        if (!$event->sendWelcomeEmail) {
            return;
        }

        Mail::to($event->user->email)
            ->send(new WelcomeEmail($event->user));

        // Notify admins
        $admins = User::where('role', 'admin')->get();
        foreach ($admins as $admin) {
            $admin->notify(new NewUserNotification($event->user));
        }
    }

    /**
     * Handle a job failure.
     */
    public function failed(UserRegistered $event, \Throwable $exception): void
    {
        // Handle failure
    }

    /**
     * Determine if the listener should be queued.
     */
    public function shouldQueue(UserRegistered $event): bool
    {
        return $event->user->email_verified_at !== null;
    }
}
```

### Registering Events & Listeners

```php
<?php

namespace App\Providers;

use App\Events\UserRegistered;
use App\Events\OrderShipped;
use App\Listeners\SendWelcomeEmail;
use App\Listeners\UpdateInventory;
use Illuminate\Auth\Events\Verified;
use Illuminate\Auth\Listeners\SendEmailVerificationNotification;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * The event to listener mappings for the application.
     */
    protected $listen = [
        UserRegistered::class => [
            SendWelcomeEmail::class,
            AssignDefaultRole::class,
            CreateCustomerPortal::class,
        ],
        OrderShipped::class => [
            UpdateInventory::class,
            SendShippingNotification::class,
        ],
        Verified::class => [
            SendEmailVerificationNotification::class,
        ],
    ];

    /**
     * The subscriber classes to register.
     */
    protected $subscribe = [
        UserEventSubscriber::class,
    ];

    /**
     * Register any events for your application.
     */
    public function boot(): void
    {
        parent::boot();

        // Event subscribers
    }
}
```

### Dispatching Events

```php
use App\Events\UserRegistered;
use Illuminate\Support\Facades\Event;

// Dispatch event
UserRegistered::dispatch($user);

// Using event helper
event(new UserRegistered($user));

// Using Event facade
Event::dispatch(new UserRegistered($user));

// Until (dispatch and wait for listeners)
$response = Event::until(new UserRegistered($user));

// Fake for testing
Event::fake();
UserRegistered::dispatch($user);
Event::assertDispatched(UserRegistered::class);
```

---

## Mail

### Creating Mailables

```bash
php artisan make:mail WelcomeEmail --markdown=emails.welcome
php artisan make:mail InvoicePaid --view=emails.invoice
```

### Mailable Class

```php
<?php

namespace App\Mail;

use App\Models\User;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Attachment;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class WelcomeEmail extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        public User $user,
        public string $activationLink
    ) {
        $this->onQueue('emails');
    }

    /**
     * Get the message envelope.
     */
    public function envelope(): Envelope
    {
        return new Envelope(
            from: new Address('noreply@example.com', 'App Name'),
            replyTo: [
                new Address('support@example.com', 'Support'),
            ],
            subject: 'Welcome to ' . config('app.name'),
            tags: ['welcome'],
            metadata: [
                'user_id' => $this->user->id,
            ],
        );
    }

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'emails.welcome',
            with: [
                'userName' => $this->user->name,
                'activationLink' => $this->activationLink,
                'appUrl' => config('app.url'),
            ],
        );
    }

    /**
     * Get the attachments for the message.
     */
    public function attachments(): array
    {
        return [
            Attachment::fromPath('/path/to/file.pdf')
                ->as('welcome-guide.pdf')
                ->withMime('application/pdf'),

            Attachment::fromStorage('welcome-bonus.pdf')
                ->as('bonus.pdf'),

            Attachment::fromData(fn() => $this->generatePdf(), 'report.pdf')
                ->withMime('application/pdf'),
        ];
    }

    /**
     * Get the message headers.
     */
    public function headers(): Headers
    {
        return new Headers(
            messageId: 'custom-message-id@example.com',
            references: ['previous-message@example.com'],
            text: [
                'X-Custom-Header' => 'Custom Value',
            ],
        );
    }
}
```

### Sending Mail

```php
use App\Mail\WelcomeEmail;
use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

// Basic sending
Mail::to($user->email)->send(new WelcomeEmail($user, $link));

// Multiple recipients
Mail::to($user->email)
    ->cc($manager->email)
    ->bcc($admin->email)
    ->send(new OrderShipped($order));

// Using mailable methods
Mail::to($request->user())
    ->cc(['admin@example.com', 'manager@example.com'])
    ->bcc('archive@example.com')
    ->locale('es')
    ->send(new WelcomeEmail($user));

// Queue mail
Mail::to($user->email)->queue(new WelcomeEmail($user));
Mail::to($user->email)->later(now()->addMinutes(5), new WelcomeEmail());

// Send to a collection
$users = User::where('subscribed', true)->get();
foreach ($users as $user) {
    Mail::to($user)->queue(new Newsletter($user));
}

// Or use Mailer
Mail::mailer('marketing')
    ->to($user->email)
    ->send(new MarketingEmail());
```

### Mail Views

```blade
{{-- resources/views/emails/welcome.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Hello, {{ $userName }}!</h1>

    <p>Welcome to our platform. Please activate your account:</p>

    <a href="{{ $activationLink }}" class="button">
        Activate Account
    </a>

    <p>Or copy this link: {{ $activationLink }}</p>

    <footer>
        <p>© {{ date('Y') }} {{ config('app.name') }}</p>
    </footer>
</body>
</html>
```

---

## Notifications

### Creating Notifications

```bash
php artisan make:notification InvoicePaid
php artisan make:notification OrderShipped --markdown=notifications.order
```

### Notification Class

```php
<?php

namespace App\Notifications;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\BroadcastMessage;
use Illuminate\Notifications\Messages\DatabaseMessage;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Messages\SlackMessage;
use Illuminate\Notifications\Notification;

class OrderShipped extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct(
        public Order $order,
        public string $trackingNumber
    ) {}

    /**
     * Get the notification's delivery channels.
     */
    public function via(object $notifiable): array
    {
        $channels = ['database'];

        if ($notifiable->email_verified_at) {
            $channels[] = 'mail';
        }

        if ($notifiable->prefers_sms) {
            $channels[] = 'vonage';
        }

        return $channels;
    }

    /**
     * Get the mail representation of the notification.
     */
    public function toMail(object $notifiable): MailMessage
    {
        $url = route('orders.track', $this->order->id);

        return (new MailMessage)
            ->subject('Your Order Has Shipped!')
            ->greeting('Hello ' . $notifiable->name . ',')
            ->line('Your order #' . $this->order->id . ' has been shipped.')
            ->line('Tracking Number: ' . $this->trackingNumber)
            ->action('Track Your Order', $url)
            ->line('Thank you for your purchase!')
            ->salutation('Best regards, ' . config('app.name'))
            ->tag('order-shipped')
            ->metadata('order_id', $this->order->id);
    }

    /**
     * Get the array representation of the notification.
     */
    public function toDatabase(object $notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'tracking_number' => $this->trackingNumber,
            'amount' => $this->order->total,
            'message' => 'Your order has been shipped!',
        ];
    }

    /**
     * Get the broadcast representation of the notification.
     */
    public function toBroadcast(object $notifiable): BroadcastMessage
    {
        return new BroadcastMessage([
            'order_id' => $this->order->id,
            'message' => 'Order shipped!',
            'tracking_url' => route('orders.track', $this->order->id),
        ]);
    }

    /**
     * Get the Slack representation of the notification.
     */
    public function toSlack(object $notifiable): SlackMessage
    {
        return (new SlackMessage)
            ->success()
            ->content('Order shipped!')
            ->attachment(function ($attachment) {
                $attachment->title('Order #' . $this->order->id)
                    ->fields([
                        'Tracking' => $this->trackingNumber,
                        'Amount' => '$' . number_format($this->order->total, 2),
                    ]);
            });
    }

    /**
     * Determine if the notification should be sent.
     */
    public function shouldSend(object $notifiable, string $channel): bool
    {
        return $this->order->status === 'shipped';
    }
}
```

### Sending Notifications

```php
use App\Notifications\OrderShipped;
use App\Notifications\DatabaseNotification;
use Illuminate\Support\Facades\Notification;

// Via notifiable entity (User model)
$user->notify(new OrderShipped($order, 'TRACK123'));

// To multiple users
$users = User::where('subscribed', true)->get();
Notification::send($users, new DatabaseNotification($data));

// Locale specific
$user->notify((new OrderShipped($order))->locale('es'));

// On demand (not via user model)
Notification::route('mail', 'admin@example.com')
    ->notify(new SystemAlert($alert));

Notification::route('mail', [
    'admin@example.com' => 'Admin',
    'manager@example.com' => 'Manager',
])->notify(new CriticalAlert());

// Via multiple channels
Notification::route('mail', 'user@example.com')
    ->route('vonage', '5555555555')
    ->notify(new UrgentNotification());
```

### Retrieving Notifications

```php
// Get all notifications
$notifications = $user->notifications;

// Get unread notifications
$unread = $user->unreadNotifications;

// Mark as read
$notification->markAsRead();

// Mark all as read
$user->unreadNotifications->markAsRead();

// Delete notification
$notification->delete();

// Delete all
$user->notifications()->delete();
```

---

## File Storage

### Configuration

```php
// config/filesystems.php
'disks' => [
    'local' => [
        'driver' => 'local',
        'root' => storage_path('app'),
        'throw' => false,
    ],

    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL') . '/storage',
        'visibility' => 'public',
        'throw' => false,
    ],

    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
        'url' => env('AWS_URL'),
        'endpoint' => env('AWS_ENDPOINT'),
        'use_path_style_endpoint' => env('AWS_USE_PATH_STYLE_ENDPOINT', false),
        'throw' => false,
    ],
],
```

### Basic Operations

```php
use Illuminate\Support\Facades\Storage;

// Store file
$path = Storage::disk('public')->put('avatars', $request->file('avatar'));
$path = $request->file('avatar')->store('avatars', 'public');
$path = $request->file('avatar')->storePublicly('avatars', 's3');

// Store with custom name
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id . '.' . $request->file('avatar')->extension(),
    's3'
);

// Retrieve file
$contents = Storage::disk('s3')->get('file.jpg');
$url = Storage::disk('s3')->url('file.jpg');
$temporaryUrl = Storage::disk('s3')->temporaryUrl(
    'file.jpg',
    now()->addMinutes(5)
);

// Check existence
$exists = Storage::disk('s3')->exists('file.jpg');
$missing = Storage::disk('s3')->missing('file.jpg');

// Download
return Storage::disk('s3')->download('file.jpg', 'custom-name.jpg');

// Delete
Storage::disk('s3')->delete('file.jpg');
Storage::disk('s3')->delete(['file1.jpg', 'file2.jpg']);

// Copy & Move
Storage::disk('s3')->copy('old/file.jpg', 'new/file.jpg');
Storage::disk('s3')->move('old/file.jpg', 'new/file.jpg');

// File metadata
$size = Storage::disk('s3')->size('file.jpg');
$lastModified = Storage::disk('s3')->lastModified('file.jpg');
$mimeType = Storage::disk('s3')->mimeType('file.jpg');

// Directories
$files = Storage::disk('s3')->files('directory');
$allFiles = Storage::disk('s3')->allFiles('directory');
$directories = Storage::disk('s3')->directories('directory');
$allDirectories = Storage::disk('s3')->allDirectories('directory');
Storage::disk('s3')->makeDirectory('new/directory');
Storage::disk('s3')->deleteDirectory('directory');
```

### File Upload Controller

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class FileUploadController extends Controller
{
    public function upload(Request $request)
    {
        $request->validate([
            'file' => ['required', 'file', 'max:10240'], // 10MB max
            'type' => ['required', 'in:avatar,document,image'],
        ]);

        $file = $request->file('file');
        $type = $request->type;

        // Validate file type
        $allowedMimes = match ($type) {
            'avatar' => ['jpeg', 'png', 'jpg', 'webp'],
            'document' => ['pdf', 'doc', 'docx', 'xls', 'xlsx'],
            'image' => ['jpeg', 'png', 'jpg', 'gif', 'webp', 'svg'],
        };

        if (!in_array($file->extension(), $allowedMimes)) {
            return back()->withErrors(['file' => 'Invalid file type.']);
        }

        // Store file
        $path = $file->store($type . 's', 's3');

        // Get URL
        $url = Storage::disk('s3')->url($path);

        return response()->json([
            'message' => 'File uploaded successfully',
            'path' => $path,
            'url' => $url,
        ]);
    }

    public function download(string $path)
    {
        if (!Storage::disk('s3')->exists($path)) {
            abort(404, 'File not found');
        }

        return Storage::disk('s3')->download($path);
    }

    public function delete(string $path)
    {
        Storage::disk('s3')->delete($path);

        return response()->json(['message' => 'File deleted']);
    }
}
```

---

## Caching

### Cache Operations

```php
use Illuminate\Support\Facades\Cache;

// Store
Cache::put('key', 'value', $seconds = 3600);
Cache::put('key', 'value', now()->addHours(1));
Cache::forever('key', 'value');

// Store if not exists
Cache::add('key', 'value', 3600); // Returns false if exists

// Retrieve
$value = Cache::get('key');
$value = Cache::get('key', 'default');
$value = Cache::get('key', function () {
    return 'computed default';
});

// Retrieve or store (remember)
$value = Cache::remember('users.active', 3600, function () {
    return User::where('active', true)->get();
});

// Retrieve and delete
$value = Cache::pull('key');

// Check existence
if (Cache::has('key')) {
    // ...
}

// Increment/Decrement
Cache::increment('counter');
Cache::increment('counter', 5);
Cache::decrement('counter');

// Delete
Cache::forget('key');
Cache::forget('users.*'); // Wildcard (Redis only)
Cache::flush(); // Clear all

// Tags (Redis, Memcached, DynamoDB)
Cache::tags(['users', 'admins'])->put('user:1', $user, 3600);
Cache::tags(['users'])->flush();
```

### Cache Locks

```php
use Illuminate\Support\Facades\Cache;

// Basic lock
$lock = Cache::lock('processing', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds
    // Do work...
    $lock->release();
}

// With callback (auto-release)
Cache::lock('processing', 10)->get(function () {
    // Do work...
    // Lock released automatically
});

// Wait for lock
$lock = Cache::lock('processing', 10)->block(5, function () {
    // Wait max 5 seconds for lock, then execute
    // Lock released automatically
});

// Owner check
$lock = Cache::store('redis')->lock('processing', 10, 'owner-token');
$lock->ownedByCurrentProcess(); // Check ownership

// Force release
$lock->forceRelease();
```

### Model Caching

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Cache;

class Category extends Model
{
    public static function getCached()
    {
        return Cache::remember('categories.all', 3600, function () {
            return static::with('children')->whereNull('parent_id')->get();
        });
    }

    public static function getCachedById(int $id)
    {
        return Cache::remember("categories.{$id}", 3600, function () use ($id) {
            return static::with('children')->findOrFail($id);
        });
    }

    protected static function booted(): void
    {
        static::saved(function () {
            Cache::forget('categories.all');
            Cache::forget('categories.tree');
        });

        static::deleted(function () {
            Cache::forget('categories.all');
        });
    }
}
```

---

## Commands & Scheduling

### Creating Commands

```bash
php artisan make:command ProcessReport
php artisan make:command SendWeeklyEmail --command=email:weekly
```

### Command Class

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Services\ReportService;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Mail;

class SendWeeklyReport extends Command
{
    /**
     * The name and signature of the console command.
     */
    protected $signature = 'report:weekly
                            {--user= : Send report to specific user ID}
                            {--format=pdf : Report format (pdf|csv|excel)}
                            {--notify : Send email notification}
                            {--force : Force regeneration}';

    /**
     * The console command description.
     */
    protected $description = 'Generate and send weekly reports';

    /**
     * Execute the console command.
     */
    public function handle(ReportService $reportService): int
    {
        $this->info('Starting weekly report generation...');

        $format = $this->option('format');
        $force = $this->option('force');
        $userId = $this->option('user');

        // Progress bar
        $users = $userId
            ? User::where('id', $userId)->get()
            : User::where('active', true)->get();

        $bar = $this->output->createProgressBar($users->count());
        $bar->start();

        foreach ($users as $user) {
            $report = $reportService->generate($user, $format, $force);

            if ($this->option('notify')) {
                Mail::to($user)->queue(new WeeklyReportMail($report));
            }

            $bar->advance();
        }

        $bar->finish();
        $this->newLine();

        $this->info("Reports sent to {$users->count()} users.");

        return Command::SUCCESS;
    }

    /**
     * Prompt for missing input arguments.
     */
    protected function promptForMissingArguments(): void
    {
        if (!$this->option('format')) {
            $format = $this->choice(
                'Which format would you like?',
                ['pdf', 'csv', 'excel'],
                'pdf'
            );
            $this->input->setOption('format', $format);
        }
    }
}
```

### Task Scheduling

```php
<?php

// app/Console/Kernel.php (Laravel 10)
// or bootstrap/app.php (Laravel 11)

use Illuminate\Console\Scheduling\Schedule;

// In Laravel 11 (bootstrap/app.php)
->withSchedule(function (Schedule $schedule) {
    // Daily at midnight
    $schedule->command('cache:clear')
        ->daily()
        ->at('00:00');

    // Hourly
    $schedule->command('reports:generate')
        ->hourly()
        ->withoutOverlapping()
        ->runInBackground();

    // Every 5 minutes
    $schedule->command('queue:monitor redis:default')
        ->everyFiveMinutes();

    // Weekly on Monday at 8 AM
    $schedule->command('email:weekly')
        ->weeklyOn(1, '08:00')
        ->emailOutputTo('admin@example.com');

    // Cron expression
    $schedule->command('cleanup')
        ->cron('0 0 * * *'); // Daily at midnight

    // Conditional scheduling
    $schedule->command('reports:generate')
        ->daily()
        ->when(function () {
            return app()->environment('production');
        });

    // Between hours
    $schedule->command('process:queue')
        ->everyMinute()
        ->between('08:00', '18:00')
        ->weekdays();

    // Job scheduling
    $schedule->job(new ProcessReport)
        ->daily()
        ->onOneServer(); // Prevent overlap across servers

    // Shell command
    $schedule->exec('node /path/to/script.js')
        ->daily();

    // Call closure
    $schedule->call(function () {
        User::where('expires_at', '<', now())->delete();
    })->daily();

    // With hook
    $schedule->command('reports:generate')
        ->daily()
        ->before(function () {
            // Before task runs
        })
        ->after(function () {
            // After task completes
        })
        ->onSuccess(function () {
            // Only on success
        })
        ->onFailure(function () {
            // Only on failure
        });

    // Output handling
    $schedule->command('logs:process')
        ->daily()
        ->appendOutputTo(storage_path('logs/scheduler.log'))
        ->emailOutputOnFailure('admin@example.com');
})
```

### Running Scheduler

```bash
# Add to crontab
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1

# Run scheduler (development)
php artisan schedule:run

# Test specific task
php artisan schedule:test

# List scheduled tasks
php artisan schedule:list

# Run work daemon
php artisan schedule:work
```

---

## Middleware

### Creating Middleware

```bash
php artisan make:middleware CheckRole
php artisan make:middleware EnsureEmailIsVerified
```

### Middleware Class

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckRole
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (! $request->user()) {
            return redirect('login');
        }

        foreach ($roles as $role) {
            if ($request->user()->hasRole($role)) {
                return $next($request);
            }
        }

        abort(403, 'Unauthorized action.');
    }

    /**
     * Handle tasks after the response.
     */
    public function terminate(Request $request, Response $response): void
    {
        // Post-response logic (logging, etc.)
    }
}
```

### Registering Middleware

```php
<?php

// bootstrap/app.php (Laravel 11)
use App\Http\Middleware\CheckRole;
use App\Http\Middleware\EnsureEmailIsVerified;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        // Global middleware (runs on every request)
        $middleware->append(\App\Http\Middleware\ForceJsonResponse::class);

        // Web middleware group
        $middleware->web(append: [
            \App\Http\Middleware\HandleInertiaRequests::class,
        ]);

        // API middleware group
        $middleware->api(prepend: [
            \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        ]);

        // Aliases (for route middleware)
        $middleware->alias([
            'role' => CheckRole::class,
            'verified' => EnsureEmailIsVerified::class,
        ]);

        // Exclude from CSRF
        $middleware->validateCsrfTokens(except: [
            'stripe/*',
            'webhook/*',
        ]);
    })
    ->create();
```

### Using Middleware in Routes

```php
// Single middleware
Route::get('/admin', fn() => 'Admin')->middleware('role:admin');

// Multiple middleware
Route::middleware(['auth', 'verified', 'role:admin'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});

// Controller constructor
class AdminController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('role:admin')->only(['destroy', 'update']);
        $this->middleware('throttle:60,1')->only(['index']);
    }
}
```

---

## Policies & Gates

### Creating Policies

```bash
php artisan make:policy PostPolicy --model=Post
```

### Policy Class

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\HandlesAuthorization;

class PostPolicy
{
    use HandlesAuthorization;

    /**
     * Pre-authorization check (runs before all policy methods).
     */
    public function before(User $user, string $ability): ?bool
    {
        if ($user->isSuperAdmin()) {
            return true; // Allow everything
        }

        return null; // Continue to specific policy method
    }

    /**
     * Determine if the user can view any models.
     */
    public function viewAny(User $user): bool
    {
        return true;
    }

    /**
     * Determine if the user can view the model.
     */
    public function view(User $user, Post $post): bool
    {
        return $post->isPublished() || $user->id === $post->author_id;
    }

    /**
     * Determine if the user can create models.
     */
    public function create(User $user): bool
    {
        return $user->can('create-posts');
    }

    /**
     * Determine if the user can update the model.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->author_id || $user->isEditor();
    }

    /**
     * Determine if the user can delete the model.
     */
    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->author_id;
    }

    /**
     * Determine if the user can restore the model.
     */
    public function restore(User $user, Post $post): bool
    {
        return $user->isAdmin();
    }

    /**
     * Determine if the user can permanently delete the model.
     */
    public function forceDelete(User $user, Post $post): bool
    {
        return $user->isSuperAdmin();
    }
}
```

### Registering Policies

```php
<?php

namespace App\Providers;

use App\Models\Post;
use App\Models\User;
use App\Policies\PostPolicy;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     */
    protected $policies = [
        Post::class => PostPolicy::class,
    ];

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        $this->registerPolicies();

        // Define Gates
        Gate::define('access-admin', function (User $user) {
            return $user->isAdmin() || $user->isEditor();
        });

        Gate::define('manage-users', function (User $user) {
            return $user->hasPermission('manage-users');
        });

        // Gate with policy class method
        Gate::define('update-post', [PostPolicy::class, 'update']);

        // Resource gates
        Gate::resource('posts', PostPolicy::class);
    }
}
```

### Using Authorization

```php
// Via Gate facade
use Illuminate\Support\Facades\Gate;

if (Gate::allows('update-post', $post)) {
    // Authorized
}

if (Gate::denies('update-post', $post)) {
    abort(403);
}

if (Gate::any(['update-post', 'delete-post'], $post)) {
    // Has at least one
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // Has neither
}

// Via user
if ($user->can('update', $post)) {
    // Authorized
}

// In controller
public function update(Request $request, Post $post)
{
    $this->authorize('update', $post);
    // Or: Gate::authorize('update', $post);

    $post->update($request->validated());
    return redirect()->route('posts.show', $post);
}

// In Blade
@can('update', $post)
    <a href="{{ route('posts.edit', $post) }}">Edit</a>
@endcan

@cannot('delete', $post)
    <p>You cannot delete this post.</p>
@endcannot

@canany(['update', 'delete'], $post)
    <div class="actions">...</div>
@endcanany

// Policy responses (for JSON responses)
public function update(Request $request, Post $post)
{
    return $this->authorize('update', $post)
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

---

## Blade & Views

### Layouts

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title') - {{ config('app.name') }}</title>

    @stack('styles')
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    @include('partials.navbar')

    <main class="container">
        @yield('content')
    </main>

    @include('partials.footer')

    @stack('scripts')
</body>
</html>
```

### Extending Layouts

```blade
{{-- resources/views/posts/index.blade.php --}}
@extends('layouts.app')

@section('title', 'All Posts')

@push('styles')
    <link rel="stylesheet" href="{{ asset('css/posts.css') }}">
@endpush

@section('content')
    <h1>Posts</h1>

    @forelse($posts as $post)
        <article>
            <h2>{{ $post->title }}</h2>
            <p>{{ $post->excerpt }}</p>
            <a href="{{ route('posts.show', $post) }}">Read more</a>
        </article>
    @empty
        <p>No posts found.</p>
    @endforelse

    {{ $posts->links() }}
@endsection

@push('scripts')
    <script src="{{ asset('js/posts.js') }}"></script>
@endpush
```

### Components

```php
<?php

namespace App\View\Components;

use Closure;
use Illuminate\Contracts\View\View;
use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * Create a new component instance.
     */
    public function __construct(
        public string $type = 'info',
        public ?string $title = null,
        public bool $dismissible = false,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View|Closure|string
    {
        return view('components.alert');
    }

    /**
     * Get the alert color classes.
     */
    public function colorClasses(): string
    {
        return match ($this->type) {
            'success' => 'bg-green-100 text-green-800 border-green-200',
            'warning' => 'bg-yellow-100 text-yellow-800 border-yellow-200',
            'danger' => 'bg-red-100 text-red-800 border-red-200',
            default => 'bg-blue-100 text-blue-800 border-blue-200',
        };
    }
}
```

```blade
{{-- resources/views/components/alert.blade.php --}}
<div {{ $attributes->merge(['class' => 'alert ' . $colorClasses()]) }}>
    @if($title)
        <h4 class="font-bold">{{ $title }}</h4>
    @endif

    <div>
        {{ $slot }}
    </div>

    @if($dismissible)
        <button type="button" class="close" data-dismiss="alert">&times;</button>
    @endif
</div>
```

```blade
{{-- Using the component --}}
<x-alert type="success" title="Success!" :dismissible="true">
    Your changes have been saved.
</x-alert>

<x-alert type="danger" class="mb-4">
    Something went wrong.
</x-alert>
```

---

## Testing

### Feature Tests

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Post;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostControllerTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function guest_cannot_access_posts()
    {
        $response = $this->get('/posts');

        $response->assertRedirect('login');
    }

    /** @test */
    public function authenticated_user_can_view_posts()
    {
        $user = User::factory()->create();
        $posts = Post::factory()->count(3)->create();

        $response = $this->actingAs($user)->get('/posts');

        $response->assertOk();
        $response->assertViewIs('posts.index');
        $response->assertViewHas('posts', fn($viewPosts) => $viewPosts->count() === 3);
    }

    /** @test */
    public function user_can_create_post()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post('/posts', [
            'title' => 'Test Post',
            'content' => 'Test content',
        ]);

        $response->assertRedirect(route('posts.index'));
        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'user_id' => $user->id,
        ]);
    }

    /** @test */
    public function job_is_dispatched()
    {
        Queue::fake();

        $user = User::factory()->create();
        $this->actingAs($user)->post('/posts', [
            'title' => 'Test',
            'content' => 'Content',
        ]);

        Queue::assertPushed(ProcessPost::class);
    }

    /** @test */
    public function mail_is_sent()
    {
        Mail::fake();

        // Trigger mail
        Mail::to('test@example.com')->send(new WelcomeMail());

        Mail::assertSent(WelcomeMail::class, function ($mail) {
            return $mail->hasTo('test@example.com');
        });
    }
}
```

---

## Common Commands Reference

```bash
# Artisan commands
php artisan serve
php artisan tinker

# Make commands
php artisan make:model Post -mfsc    # Model + migration + factory + seeder + controller
php artisan make:controller PostController --resource
php artisan make:middleware CheckRole
php artisan make:policy PostPolicy --model=Post
php artisan make:command SendReport --command=report:send
php artisan make:job ProcessPodcast
php artisan make:event UserRegistered
php artisan make:listener SendWelcome --event=UserRegistered
php artisan make:mail WelcomeEmail --markdown=emails.welcome
php artisan make:notification InvoicePaid
php artisan make:component Alert

# Queue commands
php artisan queue:work
php artisan queue:listen
php artisan queue:restart
php artisan queue:retry all
php artisan queue:failed
php artisan queue:flush

# Schedule commands
php artisan schedule:run
php artisan schedule:list
php artisan schedule:test

# Cache commands
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
php artisan optimize:clear

# Production optimization
php artisan optimize
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Database
php artisan migrate
php artisan migrate:fresh --seed
php artisan migrate:rollback
php artisan db:seed
php artisan db:show
```

---

## Quick Reference

### HTTP Status Codes
| Code | Use |
|------|-----|
| 200 | Success |
| 201 | Created |
| 204 | No Content (delete) |
| 301 | Permanent redirect |
| 302 | Temporary redirect |
| 400 | Bad request |
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Not found |
| 419 | CSRF token mismatch |
| 422 | Validation error |
| 429 | Too many requests |
| 500 | Server error |

### Environment Variables
```bash
# .env
APP_NAME=Laravel
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=

QUEUE_CONNECTION=redis
CACHE_DRIVER=redis
SESSION_DRIVER=redis

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
```
