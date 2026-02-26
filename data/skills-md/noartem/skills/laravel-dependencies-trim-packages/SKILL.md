---
name: laravel-dependencies-trim-packages
description: Remove unneeded Composer packages and assets to improve boot time, memory, and security surface
---

# Trim Dependencies

- Audit packages: `composer show --tree` and remove unused ones
- Prefer first-party or built-in features before adding new packages
- Regularly update; pin major versions via constraints and test

```
composer remove vendor/package
```
