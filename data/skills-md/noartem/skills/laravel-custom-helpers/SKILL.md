---
name: laravel-custom-helpers
description: Create and register small, pure helper functions when they improve clarity; keep them organized and tested
---

# Custom Helpers

## Create a helper file

```php
// app/Support/helpers.php
function money(int $cents): string { return number_format($cents / 100, 2); }
```

## Autoload

Add to `composer.json`:

```json
{
  "autoload": { "files": ["app/Support/helpers.php"] }
}
```

Run `composer dump-autoload`.

## Guidelines

- Keep helpers small and pure; avoid hidden IO/state
- Prefer static methods on value objects when domain-specific
