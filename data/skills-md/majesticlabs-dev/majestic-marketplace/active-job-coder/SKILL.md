---
name: active-job-coder
description: Use when creating or refactoring Active Job background jobs. Applies Rails 8 conventions, Solid Queue patterns, error handling, retry strategies, and job design best practices.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Active Job Coder

## Job Design Principles

### 1. Single Responsibility

```ruby
# Good: Focused job
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default

  def perform(user)
    UserMailer.welcome(user).deliver_now
  end
end
```

### 2. Pass IDs, Not Objects

```ruby
# Good: Pass identifiers
class ProcessOrderJob < ApplicationJob
  def perform(order_id)
    order = Order.find(order_id)
    # Process order
  end
end
```

### 3. Queue Configuration

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

## Error Handling & Retry Strategies

```ruby
class ExternalApiJob < ApplicationJob
  queue_as :default

  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError

  def perform(record_id)
    record = Record.find(record_id)
    ExternalApi.sync(record)
  end
end
```

### Custom Error Handling

```ruby
class ImportantJob < ApplicationJob
  rescue_from StandardError do |exception|
    Rails.logger.error("Job failed: #{exception.message}")
    ErrorNotifier.notify(exception, job: self.class.name)
    raise # Re-raise to trigger retry
  end
end
```

## Concurrency Control (Solid Queue)

```ruby
class ProcessUserDataJob < ApplicationJob
  limits_concurrency key: ->(user_id) { user_id }, duration: 15.minutes

  def perform(user_id)
    user = User.find(user_id)
    # Process user data safely
  end
end

class ContactActionJob < ApplicationJob
  limits_concurrency key: ->(contact) { contact.id },
                     duration: 10.minutes,
                     group: "ContactActions"
end
```

## Scheduling & Delayed Execution

```ruby
SendReminderJob.perform_later(user)                              # Immediate
SendReminderJob.set(wait: 1.hour).perform_later(user)            # Delayed
SendReminderJob.set(wait_until: Date.tomorrow.noon).perform_later(user)  # Scheduled

# Bulk enqueue
ActiveJob.perform_all_later(users.map { |u| SendReminderJob.new(u.id) })
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Fat jobs | Hard to test and maintain | Extract logic to model classes |
| Serializing objects | Expensive, stale data | Pass IDs, fetch fresh data |
| No retry strategy | Silent failures | Use `retry_on` with backoff |
| Synchronous calls | Blocks request | Always use `perform_later` |
| No idempotency | Duplicate processing | Design jobs to be re-runnable |
| Ignoring errors | Silent failures | Use `rescue_from` with logging |
| Monolithic steps | Can't resume after failure | Use Continuable pattern with state |

## Output Format

When creating or refactoring jobs, provide:

1. **Job Class** - The complete job implementation
2. **Queue Strategy** - Recommended queue and priority
3. **Error Handling** - Retry and failure strategies
4. **Testing** - Example test cases
5. **Considerations** - Concurrency, idempotency notes
