---
name: laravel-migrations-and-factories
description: Safe database change patterns; when to modify vs add migrations; always pair models with migrations and factories; seeding guidance
---

# Migrations and Factories

Keep schema changes safe, testable, and reversible.

## Commands

```
php artisan make:model Post -mfc

# Run/rollback
php artisan migrate
php artisan migrate:rollback --step=1

# Fresh DB (dangerous; dev only)
php artisan migrate:fresh --seed
```

## Rules

- Pair each new model with a migration and a factory
- If a migration was merged to `main`, never edit it—add a new one
- On feature branches, you may amend migrations created on that branch (if not merged)
- Seed realistic but minimal datasets in seeder classes; keep huge datasets external

## Factories

- Prefer state modifiers (e.g., `->state([...])`) over boolean flags
- Use relationships (e.g., `belongsTo`) in factories to build realistic graphs
- Keep factories fast; move expensive setup to seeds where possible

## Testing

- Use factories in tests; avoid manual inserts
- For integration tests touching DB, use transactions or `RefreshDatabase`
