---
name: solid-queue-coder
description: Use when configuring or working with Solid Queue for background jobs. Applies Rails 8 conventions, database-backed job processing, concurrency settings, recurring jobs, and production deployment patterns.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Solid Queue Coder

## Overview

Solid Queue is Rails 8's default job backend—a database-backed Active Job adapter that eliminates the need for Redis. Jobs are stored in your database with ACID guarantees.

## Configuration

### Database Setup

```yaml
# config/database.yml
production:
  primary:
    <<: *default
    url: <%= ENV["DATABASE_URL"] %>
  queue:
    <<: *default
    url: <%= ENV["QUEUE_DATABASE_URL"] %>
    migrations_paths: db/queue_migrate
```

### Queue Configuration

```yaml
# config/solid_queue.yml
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 500

  workers:
    - queues: [critical, default]
      threads: 5
      processes: 2
      polling_interval: 0.1
    - queues: [low_priority]
      threads: 2
      processes: 1
      polling_interval: 1
```

### Application Configuration

```ruby
# config/application.rb
config.active_job.queue_adapter = :solid_queue

# config/environments/production.rb
config.solid_queue.connects_to = { database: { writing: :queue } }
```

## Queue Design

### Priority Strategy

```ruby
class CriticalNotificationJob < ApplicationJob
  queue_as :critical
  queue_with_priority 1  # Lower = higher priority
end

class ReportGenerationJob < ApplicationJob
  queue_as :low_priority
  queue_with_priority 50
end
```

### Concurrency Control

```ruby
class ProcessUserDataJob < ApplicationJob
  limits_concurrency key: ->(user_id) { user_id }
end

class SyncContactJob < ApplicationJob
  limits_concurrency key: ->(contact) { contact.id },
                     duration: 15.minutes,
                     group: "ContactOperations"
end
```

## Recurring Jobs

```yaml
# config/solid_queue.yml
recurring:
  cleanup_old_records:
    class: CleanupJob
    schedule: every day at 3am
    queue: low_priority

  sync_external_data:
    class: SyncExternalDataJob
    schedule: every 15 minutes
    queue: default
```

## Deployment

### Procfile

```yaml
web: bundle exec puma -C config/puma.rb
worker: bundle exec rake solid_queue:start
```

### Docker Compose

```yaml
services:
  web:
    command: bundle exec puma -C config/puma.rb
  worker:
    command: bundle exec rake solid_queue:start
```

## Error Handling

```ruby
class ExternalApiJob < ApplicationJob
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  rescue_from StandardError do |exception|
    if executions >= 5
      FailedJob.create!(job_class: self.class.name, error_message: exception.message)
    else
      raise exception
    end
  end
end
```

## Database Maintenance

```ruby
namespace :queue do
  task vacuum: :environment do
    ActiveRecord::Base.connected_to(database: :queue) do
      %w[solid_queue_ready_executions solid_queue_claimed_executions].each do |table|
        ActiveRecord::Base.connection.execute("VACUUM ANALYZE #{table}")
      end
    end
  end
end
```

## Solid Queue vs Sidekiq

| Feature | Solid Queue | Sidekiq |
|---------|-------------|---------|
| Infrastructure | Database only | Requires Redis |
| ACID guarantees | Yes | No |
| Transactional enqueue | Yes | No |
| Concurrency control | Built-in | Requires sidekiq-unique-jobs |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Wildcard queue `*` in prod | Unpredictable priority | Specify queue order |
| Single database | Contention with app | Separate queue database |
| Too many threads | Database exhaustion | Match pool size |

## Output Format

When configuring Solid Queue, provide:

1. **Database Setup** - Multi-database configuration
2. **Queue Config** - solid_queue.yml settings
3. **Worker Setup** - Procfile/Docker configuration
4. **Jobs** - Example job classes with error handling
