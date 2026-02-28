---
name: laravel-data-chunking-large-datasets
description: Process large datasets efficiently using chunk(), chunkById(), lazy(), and cursor() to reduce memory consumption and improve performance
---

# Data Chunking for Large Datasets

Process large datasets efficiently by breaking them into manageable chunks to reduce memory consumption and improve performance.

## The Problem: Memory Exhaustion

```php
// BAD: Loading all records into memory
$users = User::all(); // Could be millions of records!

foreach ($users as $user) {
    $user->sendNewsletter();
}

// BAD: Even with select, still loads everything
$emails = User::pluck('email'); // Array of millions of emails

foreach ($emails as $email) {
    Mail::to($email)->send(new Newsletter());
}
```

## Solution: Chunking Methods

### 1. Basic Chunking with `chunk()`

```php
// Process 100 records at a time
User::chunk(100, function ($users) {
    foreach ($users as $user) {
        $user->calculateStatistics();
        $user->save();
    }
});

// With conditions
User::where('active', true)
    ->chunk(200, function ($users) {
        foreach ($users as $user) {
            ProcessUserJob::dispatch($user);
        }
    });
```

### 2. Chunk By ID for Safer Updates

```php
// Prevents issues when modifying records during iteration
User::where('newsletter_sent', false)
    ->chunkById(100, function ($users) {
        foreach ($users as $user) {
            $user->update(['newsletter_sent' => true]);
            Mail::to($user)->send(new Newsletter());
        }
    });

// With custom column
Payment::where('processed', false)
    ->chunkById(100, function ($payments) {
        foreach ($payments as $payment) {
            $payment->process();
        }
    }, 'payment_id'); // Custom ID column
```

### 3. Lazy Collections for Memory Efficiency

```php
// Uses PHP generators, minimal memory footprint
User::where('created_at', '>=', now()->subDays(30))
    ->lazy()
    ->each(function ($user) {
        $user->recalculateScore();
    });

// With chunking size control
User::lazy(100)->each(function ($user) {
    ProcessRecentUser::dispatch($user);
});

// Filter and map with lazy collections
$results = User::lazy()
    ->filter(fn($user) => $user->hasActiveSubscription())
    ->map(fn($user) => [
        'id' => $user->id,
        'revenue' => $user->calculateRevenue(),
    ])
    ->take(1000);
```

### 4. Cursor for Forward-Only Iteration

```php
// Most memory-efficient for simple forward iteration
foreach (User::where('active', true)->cursor() as $user) {
    $user->updateLastSeen();
}

// With lazy() for additional collection methods
User::where('verified', true)
    ->cursor()
    ->filter(fn($user) => $user->hasCompletedProfile())
    ->each(fn($user) => SendWelcomeEmail::dispatch($user));
```

## Real-World Examples

### Export Large CSV

```php
class ExportUsersCommand extends Command
{
    public function handle()
    {
        $file = fopen('users.csv', 'w');

        // Write headers
        fputcsv($file, ['ID', 'Name', 'Email', 'Created At']);

        // Process in chunks to avoid memory issues
        User::select('id', 'name', 'email', 'created_at')
            ->chunkById(500, function ($users) use ($file) {
                foreach ($users as $user) {
                    fputcsv($file, [
                        $user->id,
                        $user->name,
                        $user->email,
                        $user->created_at->toDateTimeString(),
                    ]);
                }

                // Optional: Show progress
                $this->info("Processed up to ID: {$users->last()->id}");
            });

        fclose($file);
        $this->info('Export completed!');
    }
}
```

### Batch Email Campaign

```php
class SendCampaignJob implements ShouldQueue
{
    public function handle()
    {
        $campaign = Campaign::find($this->campaignId);

        // Process subscribers in chunks
        $campaign->subscribers()
            ->where('unsubscribed', false)
            ->chunkById(50, function ($subscribers) use ($campaign) {
                foreach ($subscribers as $subscriber) {
                    SendCampaignEmail::dispatch($campaign, $subscriber)
                        ->onQueue('emails')
                        ->delay(now()->addSeconds(rand(1, 10)));
                }

                // Prevent rate limiting
                sleep(2);
            });
    }
}
```

### Data Migration/Transformation

```php
class MigrateUserData extends Command
{
    public function handle()
    {
        $bar = $this->output->createProgressBar(User::count());

        User::with(['profile', 'settings'])
            ->chunkById(100, function ($users) use ($bar) {
                DB::transaction(function () use ($users, $bar) {
                    foreach ($users as $user) {
                        // Complex transformation
                        $newData = $this->transformUserData($user);

                        NewUserModel::create($newData);

                        $bar->advance();
                    }
                });
            });

        $bar->finish();
        $this->newLine();
        $this->info('Migration completed!');
    }
}
```

### Cleanup Old Records

```php
class CleanupOldLogs extends Command
{
    public function handle()
    {
        $deletedCount = 0;

        ActivityLog::where('created_at', '<', now()->subMonths(6))
            ->chunkById(1000, function ($logs) use (&$deletedCount) {
                $ids = $logs->pluck('id')->toArray();

                // Batch delete for efficiency
                ActivityLog::whereIn('id', $ids)->delete();

                $deletedCount += count($ids);

                $this->info("Deleted {$deletedCount} records so far...");

                // Give database a breather
                usleep(100000); // 100ms
            });

        $this->info("Total deleted: {$deletedCount}");
    }
}
```

## Choosing the Right Method

| Method        | Use Case                 | Memory Usage     | Notes                                          |
| ------------- | ------------------------ | ---------------- | ---------------------------------------------- |
| `chunk()`     | General processing       | Moderate         | May skip/duplicate if modifying filter columns |
| `chunkById()` | Updates during iteration | Moderate         | Safer for modifications                        |
| `lazy()`      | Large result processing  | Low              | Returns LazyCollection                         |
| `cursor()`    | Simple forward iteration | Lowest           | Returns Generator                              |
| `each()`      | Simple operations        | High (loads all) | Avoid for large datasets                       |

## Performance Optimization Tips

### 1. Select Only Needed Columns

```php
User::select('id', 'email', 'name')
    ->chunkById(100, function ($users) {
        // Process with minimal data
    });
```

### 2. Use Indexes

```php
// Ensure indexed columns in where clauses
User::where('status', 'active') // status should be indexed
    ->where('created_at', '>', $date) // created_at should be indexed
    ->chunkById(200, function ($users) {
        // Process efficiently
    });
```

### 3. Disable Eloquent Events When Appropriate

```php
User::withoutEvents(function () {
    User::chunkById(500, function ($users) {
        foreach ($users as $user) {
            $user->update(['processed' => true]);
        }
    });
});
```

### 4. Use Raw Queries for Bulk Updates

```php
// Instead of updating each record
User::chunkById(100, function ($users) {
    $ids = $users->pluck('id')->toArray();

    // Bulk update with raw query
    DB::table('users')
        ->whereIn('id', $ids)
        ->update([
            'last_processed_at' => now(),
            'processing_count' => DB::raw('processing_count + 1'),
        ]);
});
```

### 5. Queue Large Operations

```php
class ProcessLargeDataset extends Command
{
    public function handle()
    {
        User::chunkById(100, function ($users) {
            ProcessUserBatch::dispatch($users->pluck('id'))
                ->onQueue('heavy-processing');
        });
    }
}

class ProcessUserBatch implements ShouldQueue
{
    public function __construct(
        public Collection $userIds
    ) {}

    public function handle()
    {
        User::whereIn('id', $this->userIds)
            ->get()
            ->each(fn($user) => $user->process());
    }
}
```

## Testing Chunked Operations

```php
test('processes all active users in chunks', function () {
    // Create test data
    User::factory()->count(150)->create(['active' => true]);
    User::factory()->count(50)->create(['active' => false]);

    $processed = [];

    User::where('active', true)
        ->chunkById(50, function ($users) use (&$processed) {
            foreach ($users as $user) {
                $processed[] = $user->id;
            }
        });

    expect($processed)->toHaveCount(150);
    expect(count(array_unique($processed)))->toBe(150);
});

test('handles empty datasets gracefully', function () {
    $callCount = 0;

    User::where('id', '<', 0) // No results
        ->chunk(100, function ($users) use (&$callCount) {
            $callCount++;
        });

    expect($callCount)->toBe(0);
});
```

## Common Pitfalls

1. **Modifying filter columns during chunk()**

   ```php
   // WRONG: May skip records
   User::where('processed', false)
       ->chunk(100, function ($users) {
           foreach ($users as $user) {
               $user->update(['processed' => true]); // Changes the WHERE condition!
           }
       });

   // CORRECT: Use chunkById()
   User::where('processed', false)
       ->chunkById(100, function ($users) {
           foreach ($users as $user) {
               $user->update(['processed' => true]);
           }
       });
   ```

2. **Not handling chunk callback returns**

   ```php
   // Return false to stop chunking
   User::chunk(100, function ($users) {
       foreach ($users as $user) {
           if ($user->hasIssue()) {
               return false; // Stop processing
           }
           $user->process();
       }
   });
   ```

3. **Ignoring database connection limits**

   ```php
   // Consider connection timeouts for long operations
   DB::connection()->getPdo()->setAttribute(PDO::ATTR_TIMEOUT, 3600);

   User::chunkById(100, function ($users) {
       // Long running process
   });
   ```

Remember: When dealing with large datasets, always think about memory usage, query efficiency, and processing time. Chunk your data appropriately!
