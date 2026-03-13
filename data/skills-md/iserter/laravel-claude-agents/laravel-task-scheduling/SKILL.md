---
name: laravel-task-scheduling
description: Best practices for Laravel task scheduling including defining schedules, frequency constraints, overlap prevention, and monitoring hooks.
---

# Task Scheduling

## Defining Schedules in routes/console.php

```php
<?php

use Illuminate\Support\Facades\Schedule;

// Schedule an Artisan command
Schedule::command('reports:generate')->daily();

// Schedule a job
Schedule::job(new ProcessDailyMetrics)->dailyAt('01:00');

// Schedule a closure
Schedule::call(function () {
    Cache::flush();
})->weekly();

// Schedule a shell command
Schedule::exec('node /home/forge/script.js')->daily();
```

## Schedule Types

### Artisan Commands

```php
// With arguments and options
Schedule::command('emails:send', ['--force'])->daily();
Schedule::command('reports:generate --type=weekly')->sundays();

// Using command class
Schedule::command(SendEmailsCommand::class, ['--force'])->daily();
```

### Queued Jobs

```php
// Dispatch a job
Schedule::job(new CleanUpExpiredTokens)->daily();

// Dispatch to a specific queue and connection
Schedule::job(new ProcessAnalytics, 'analytics', 'redis')->hourly();
```

### Closures

```php
Schedule::call(function () {
    DB::table('sessions')
        ->where('last_activity', '<', now()->subHours(24))
        ->delete();
})->hourly()->description('Clean expired sessions');
```

### Shell Commands

```php
Schedule::exec('pg_dump mydb > /backups/db.sql')->daily();
```

## Frequency Methods

```php
// Common frequencies
Schedule::command('task')->everyMinute();
Schedule::command('task')->everyTwoMinutes();
Schedule::command('task')->everyFiveMinutes();
Schedule::command('task')->everyTenMinutes();
Schedule::command('task')->everyFifteenMinutes();
Schedule::command('task')->everyThirtyMinutes();
Schedule::command('task')->hourly();
Schedule::command('task')->hourlyAt(17);            // At :17 past each hour
Schedule::command('task')->everyOddHour();
Schedule::command('task')->everyTwoHours();
Schedule::command('task')->everyThreeHours();
Schedule::command('task')->everyFourHours();
Schedule::command('task')->everySixHours();
Schedule::command('task')->daily();
Schedule::command('task')->dailyAt('13:00');
Schedule::command('task')->twiceDaily(1, 13);       // At 1:00 and 13:00
Schedule::command('task')->twiceDailyAt(1, 13, 15); // At 1:15 and 13:15
Schedule::command('task')->weekly();
Schedule::command('task')->weeklyOn(1, '8:00');     // Monday at 8:00
Schedule::command('task')->monthly();
Schedule::command('task')->monthlyOn(4, '15:00');   // 4th of month at 15:00
Schedule::command('task')->twiceMonthly(1, 16);     // 1st and 16th
Schedule::command('task')->lastDayOfMonth('17:00');
Schedule::command('task')->quarterly();
Schedule::command('task')->quarterlyOn(4, '14:00'); // 4th day of quarter
Schedule::command('task')->yearly();
Schedule::command('task')->yearlyOn(6, 1, '17:00'); // June 1st at 17:00

// Cron expression
Schedule::command('task')->cron('0 */6 * * *');     // Every 6 hours
```

## Constraints

### Time Constraints

```php
// Between specific times
Schedule::command('task')->hourly()->between('8:00', '17:00');

// Outside specific times
Schedule::command('task')->hourly()->unlessBetween('23:00', '04:00');
```

### Day Constraints

```php
Schedule::command('task')->daily()->weekdays();
Schedule::command('task')->daily()->weekends();
Schedule::command('task')->daily()->sundays();
Schedule::command('task')->daily()->mondays();
Schedule::command('task')->daily()->tuesdays();
Schedule::command('task')->daily()->wednesdays();
Schedule::command('task')->daily()->thursdays();
Schedule::command('task')->daily()->fridays();
Schedule::command('task')->daily()->saturdays();
Schedule::command('task')->daily()->days([0, 3]);   // Sunday and Wednesday
```

### Environment Constraints

```php
// ✅ Only run in production
Schedule::command('analytics:process')->daily()->environments(['production']);

// ✅ Skip in testing
Schedule::command('reports:send')->daily()->environments(['production', 'staging']);
```

### Conditional Constraints

```php
// Run only when condition is true
Schedule::command('emails:send')
    ->daily()
    ->when(function () {
        return config('services.email.enabled');
    });

// Skip when condition is true
Schedule::command('maintenance:run')
    ->daily()
    ->skip(function () {
        return app()->isDownForMaintenance();
    });
```

## Overlap Prevention

```php
// ✅ Prevent overlapping: skip if previous instance is still running
Schedule::command('reports:generate')
    ->hourly()
    ->withoutOverlapping();

// With custom expiration (default is 24 hours)
Schedule::command('reports:generate')
    ->hourly()
    ->withoutOverlapping(expiresAt: 60); // Lock expires after 60 minutes
```

## Distributed Environments (onOneServer)

```php
// ✅ Only run on a single server (requires memcached, redis, or database cache driver)
Schedule::command('reports:generate')
    ->daily()
    ->onOneServer();

// Combine with overlap prevention
Schedule::command('analytics:process')
    ->hourly()
    ->onOneServer()
    ->withoutOverlapping();
```

## Schedule Groups

```php
// ✅ Apply shared configuration to multiple scheduled tasks
Schedule::command('analytics:aggregate')
    ->daily()
    ->onOneServer()
    ->withoutOverlapping()
    ->emailOutputOnFailure('admin@example.com');

Schedule::command('analytics:cleanup')
    ->daily()
    ->onOneServer()
    ->withoutOverlapping()
    ->emailOutputOnFailure('admin@example.com');

// Group with shared config (if using a helper)
collect([
    'analytics:aggregate',
    'analytics:cleanup',
    'analytics:summary',
])->each(function ($command) {
    Schedule::command($command)
        ->daily()
        ->onOneServer()
        ->withoutOverlapping()
        ->emailOutputOnFailure('admin@example.com');
});
```

## Hooks (before, after, onSuccess, onFailure, ping)

```php
Schedule::command('reports:generate')
    ->daily()
    ->before(function () {
        Log::info('Starting report generation...');
    })
    ->after(function () {
        Log::info('Report generation complete.');
    })
    ->onSuccess(function () {
        Notification::route('slack', '#ops')
            ->notify(new ScheduledTaskSucceeded('reports:generate'));
    })
    ->onFailure(function () {
        Notification::route('slack', '#alerts')
            ->notify(new ScheduledTaskFailed('reports:generate'));
    });
```

### Pinging URLs (Health Checks)

```php
// Ping a URL before and after
Schedule::command('reports:generate')
    ->daily()
    ->pingBefore('https://health.example.com/start')
    ->thenPing('https://health.example.com/end');

// Ping only on success or failure
Schedule::command('reports:generate')
    ->daily()
    ->pingOnSuccess('https://health.example.com/success')
    ->pingOnFailure('https://health.example.com/failure');

// Works with services like Oh Dear, Healthchecks.io, Cronitor
Schedule::command('reports:generate')
    ->daily()
    ->pingBefore('https://hc-ping.com/your-uuid/start')
    ->thenPing('https://hc-ping.com/your-uuid');
```

### Email Output

```php
Schedule::command('reports:generate')
    ->daily()
    ->sendOutputTo('/var/log/reports.log')
    ->emailOutputTo('admin@example.com');

// Only email on failure
Schedule::command('reports:generate')
    ->daily()
    ->emailOutputOnFailure('admin@example.com');
```

## Sub-Minute Scheduling

```php
// ✅ Run every second (Laravel 11+)
Schedule::call(function () {
    // Process real-time data
    MetricsCollector::capture();
})->everySecond();

// Every 10 seconds
Schedule::call(function () {
    QueueMonitor::check();
})->everyTenSeconds();

// Every 15 seconds
Schedule::command('queue:monitor')->everyFifteenSeconds();

// Every 20 / 30 seconds
Schedule::call(fn () => HealthCheck::ping())->everyTwentySeconds();
Schedule::call(fn () => HealthCheck::ping())->everyThirtySeconds();
```

## Output Management

```php
// Send output to a file
Schedule::command('reports:generate')
    ->daily()
    ->sendOutputTo('/var/log/schedule/reports.log');

// Append output to a file
Schedule::command('reports:generate')
    ->daily()
    ->appendOutputTo('/var/log/schedule/reports.log');

// Write output to storage
Schedule::command('reports:generate')
    ->daily()
    ->appendOutputTo(storage_path('logs/reports.log'));

// Discard output
Schedule::command('reports:generate')
    ->daily()
    ->sendOutputTo('/dev/null');
```

## Running in Maintenance Mode

```php
// ✅ Run even during maintenance mode
Schedule::command('queue:work --stop-when-empty')
    ->everyMinute()
    ->evenInMaintenanceMode();
```

## Running the Scheduler

```bash
# Add to crontab (required for scheduling to work)
* * * * * cd /path-to-project && php artisan schedule:run >> /dev/null 2>&1

# For sub-minute scheduling
* * * * * cd /path-to-project && php artisan schedule:run >> /dev/null 2>&1

# Local development - runs scheduler in the foreground
php artisan schedule:work

# List all scheduled tasks
php artisan schedule:list

# Test a specific scheduled command
php artisan schedule:test
```

## Best Practices

```php
// ✅ Always give scheduled closures a description
Schedule::call(function () {
    // ...
})->daily()->description('Clean expired sessions');

// ✅ Use onOneServer for distributed deployments
Schedule::command('sitemap:generate')->daily()->onOneServer();

// ✅ Use withoutOverlapping for long-running tasks
Schedule::command('import:products')->hourly()->withoutOverlapping();

// ✅ Monitor with hooks and pings
Schedule::command('billing:charge')
    ->daily()
    ->onSuccess(fn () => Log::info('Billing completed'))
    ->onFailure(fn () => Log::critical('Billing failed'))
    ->pingOnFailure('https://alerts.example.com/billing');

// ❌ Don't schedule heavy work without overlap prevention
Schedule::command('heavy:task')->everyMinute(); // Could stack up

// ❌ Don't forget to set the timezone if needed
Schedule::command('report:daily')
    ->dailyAt('09:00')
    ->timezone('America/New_York');
```

## Checklist

- [ ] Schedules defined in `routes/console.php`
- [ ] Frequency methods match actual business requirements
- [ ] `withoutOverlapping()` used for long-running tasks
- [ ] `onOneServer()` used in multi-server deployments
- [ ] Environment constraints applied where appropriate
- [ ] Hooks configured for monitoring (before, after, onSuccess, onFailure)
- [ ] Health check pings set up for critical tasks
- [ ] Output logged or emailed for debugging
- [ ] Closures have descriptions for `schedule:list`
- [ ] Crontab entry added to server for `schedule:run`
- [ ] Timezone set explicitly when time-sensitive
- [ ] `evenInMaintenanceMode()` used for essential tasks
