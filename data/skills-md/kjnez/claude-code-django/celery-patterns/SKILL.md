---
name: celery-patterns
description: Celery task patterns including task definition, retry strategies, periodic tasks, and best practices. Use when implementing background tasks, scheduled jobs, or async processing.
---

# Celery Patterns for Django

## Core Philosophy

- **Idempotent tasks**: Running a task twice must produce the same result
- **Pass IDs, not objects**: Arguments must be JSON-serializable
- **Always handle failures**: Log errors, never swallow exceptions silently
- **Proper retry strategies**: Use exponential backoff for external services

## Task Design

### Structure
- Place tasks in `apps/<app>/tasks.py`
- Use `@shared_task` for reusable tasks across projects
- Use `bind=True` when needing access to task instance (retries, task ID, state updates)
- Add type hints to task signatures
- Log task start, completion, and failures

### Arguments
- Pass model primary keys, not model instances
- Keep arguments simple and serializable (str, int, dict, list)
- Validate that referenced objects exist at task start

## Retry Strategies

### When to Use Each Approach
- **Fixed delay**: Internal operations with predictable recovery (database locks)
- **Exponential backoff**: External APIs that may rate-limit or have variable recovery
- **No retry**: Validation errors, business logic failures, permanent errors

### Configuration
- Set `max_retries` based on acceptable total wait time
- Use `retry_jitter=True` to prevent thundering herd
- Set `retry_backoff_max` to cap maximum wait time
- Use `autoretry_for` tuple for automatic retry on specific exceptions

## Idempotency Patterns

### Check-Before-Process
Query current state before processing; skip if already complete

### Status Field Tracking
Use status transitions (pending → processing → complete/failed) with `select_for_update()` for race condition safety

### Unique Constraints
Use database constraints to prevent duplicate processing

## Periodic Tasks (Beat)

- Configure schedules in `config/celery.py` using `beat_schedule`
- Use `crontab()` for time-based schedules
- Use float values for interval-based schedules (seconds)
- Keep periodic tasks lightweight; spawn subtasks for heavy work

## Anti-Patterns to Avoid

- Passing model instances instead of IDs
- Non-idempotent operations (incrementing without checks)
- Silent exception handling (bare `except: pass`)
- Missing logging for task lifecycle
- Long-running tasks without progress updates
- Retry on permanent failures (validation, business logic errors)

## Commands

- Worker: `uv run celery -A config worker -l info`
- Beat: `uv run celery -A config beat -l info`
- Monitoring: `uv run celery -A config flower`
