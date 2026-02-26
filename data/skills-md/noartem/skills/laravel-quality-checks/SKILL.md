---
name: laravel-quality-checks
description: Unified quality gates for Laravel projects; Pint, static analysis (PHPStan/Psalm), Insights (optional), and JS linters; Sail and non-Sail pairs provided
---

# Quality Checks (Laravel)

Run automated checks before handoff or completion. Keep output clean.

## PHP Style & Lint

```
# Check
vendor/bin/pint --test

# Fix
vendor/bin/pint
```

## Static Analysis (choose your tool)

```
# PHPStan example
vendor/bin/phpstan analyse --memory-limit=1G

# Psalm example
vendor/bin/psalm
```

## Insights (optional, if installed)

```
php artisan insights --no-interaction --format=json --flush-cache
```

## Tests

```
php artisan test --parallel
```
