---
name: analyze
description: Analyze the project and recommend the most relevant Shift to run
---

# Shift Analyze

Analyze the project and recommend the most relevant Shift to run, following a strict priority order. Read all needed files upfront, then work through each priority in sequence. At the first applicable priority, summarize what was found and suggest running `/shift:run` as the next step — never invoke it automatically.

## Step 1 — Gather project information

Read both of the following (they may not both exist — that's fine):
- `composer.json` — PHP dependencies (Laravel, Livewire, PHPUnit versions)
- `package.json` — JS dependencies (Tailwind version)

Also check for the existence of these files to detect a pre-Laravel 11 folder structure:
- `app/Http/Kernel.php`
- `app/Console/Kernel.php`
- `app/Exceptions/Handler.php`

And check whether any test files exist under `tests/` (files ending in `Test.php`).

## Step 2 — Priority 1: Laravel upgrade

From `composer.json`, find `laravel/framework` under `require`. Extract the major version number — the leading integer, stripping any prefix characters (`^`, `~`, `>=`) and suffix wildcards (`.*`). Treat `^12.0`, `~12.3`, `12.*`, and `^12` all as major version `12`.

- If the major version is **less than 13**, recommend the Laravel upgrade Shift and stop:

  > Your app is on Laravel {current}. The next step is the **Laravel {next}.x Shift**.
  > https://laravelshift.com/upgrade-laravel-{current}-to-laravel-{next}

  Then suggest running `/shift:run` as the next step.

- If Laravel is **13 or higher**, continue to the next priority.

## Step 3 — Priority 2: Livewire and Tailwind upgrades

Evaluate both independently; recommend any that apply before moving on.

**Livewire:** Find `livewire/livewire` under `require` or `require-dev` in `composer.json`. If present, extract the major version using the same stripping rules.
- Major **2**: recommend the **Livewire 3.x Shift** — https://laravelshift.com/upgrade-livewire-2-to-livewire-3
- Major **3**: recommend the **Livewire 4.x Shift** — https://laravelshift.com/upgrade-livewire-3-to-livewire-4
- Major **4+**: Livewire is current — nothing to do.
- Not present: skip.

**Tailwind:** Find `tailwindcss` under `dependencies` or `devDependencies` in `package.json`. If present, extract the major version.
- Major **1**: recommend the **Tailwind 2.x Shift** — https://laravelshift.com/upgrade-tailwind-css-1-to-tailwind-css-2
- Major **2**: recommend the **Tailwind 3.x Shift** — https://laravelshift.com/upgrade-tailwind-css-2-to-tailwind-css-3
- Major **3**: recommend running **Tailwind's official upgrade tool** (`npx @tailwindcss/upgrade`) — this migration is handled by Tailwind directly, not a Shift.
- Major **4+**: Tailwind is current — nothing to do.
- Not present: skip.

If either Livewire or Tailwind needs upgrading, present the applicable recommendation(s) and suggest running `/shift:run` as the next step.

## Step 4 — Priority 3: PHPUnit upgrade

Find `phpunit/phpunit` under `require` or `require-dev` in `composer.json`. If present, extract the major version using the same stripping rules.

- Major **≤5**: recommend the **PHPUnit 6 Shift** — https://laravelshift.com/upgrade-phpunit-6
- Major **6**: recommend the **PHPUnit 8 Shift** — https://laravelshift.com/upgrade-phpunit-8 (no Shift exists for 7)
- Major **7**: recommend the **PHPUnit 8 Shift** — https://laravelshift.com/upgrade-phpunit-8
- Major **8**: recommend the **PHPUnit 9 Shift** — https://laravelshift.com/upgrade-phpunit-9
- Major **9**: recommend the **PHPUnit 10 Shift** — https://laravelshift.com/upgrade-phpunit-10
- Major **10**: recommend the **PHPUnit 11 Shift** — https://laravelshift.com/upgrade-phpunit-11
- Major **11**: recommend the **PHPUnit 12 Shift** — https://laravelshift.com/upgrade-phpunit-12
- Major **12**: recommend the **PHPUnit 13 Shift** — https://laravelshift.com/upgrade-phpunit-13
- Major **13+**: PHPUnit is current — nothing to do.
- Not present: skip.

If PHPUnit needs upgrading, present the recommendation and suggest running `/shift:run` as the next step.

## Step 5 — Priority 4: Laravel Slimmer

If any of the following files exist, the project still uses the pre-Laravel 11 folder structure:
- `app/Http/Kernel.php`
- `app/Console/Kernel.php`
- `app/Exceptions/Handler.php`

If so, recommend the **Laravel Slimmer** and suggest running `/shift:run` as the next step:

> Your app still has a pre-Laravel 11 folder structure. The **Laravel Slimmer** will modernize it.
> https://laravelshift.com/slim-laravel-application

## Step 6 — Priority 5: Tests Generator

If no files ending in `Test.php` are found under `tests/` (or `tests/` does not exist), recommend the **Tests Generator** and suggest running `/shift:run` as the next step:

> Your app has no tests. The **Tests Generator** will scaffold model factories and tests to get you started.
> https://laravelshift.com/laravel-test-generator

## Step 7 — Fallback: Laravel Fixer or individual refactors

If all previous checks passed, the app is up to date. Offer these options:

> Your app is fully up to date! To continue improving code quality:
>
> - **Laravel Fixer** — applies a curated set of modernizations to make your code more idiomatic Laravel ($19)
>   https://laravelshift.com/laravel-code-fixer
> - **Individual refactors** — run `/shift:refactor` to apply specific modernizations one at a time.

## Shift Codes

When suggesting `/shift:run`, always include the corresponding code from this table.

| Code | Shift |
|------|-------|
| `50` | Laravel 5.0 |
| `51` | Laravel 5.1 |
| `52` | Laravel 5.2 |
| `53` | Laravel 5.3 |
| `54` | Laravel 5.4 |
| `55` | Laravel 5.5 |
| `56` | Laravel 5.6 |
| `57` | Laravel 5.7 |
| `58` | Laravel 5.8 |
| `60` | Laravel 6.x |
| `70` | Laravel 7.x |
| `80` | Laravel 8.x |
| `90` | Laravel 9.x |
| `10` | Laravel 10.x |
| `11` | Laravel 11.x |
| `12` | Laravel 12.x |
| `13` | Laravel 13.x |
| `PU6` | PHPUnit 6 |
| `PU8` | PHPUnit 8 |
| `PU9` | PHPUnit 9 |
| `PU10` | PHPUnit 10 |
| `PU11` | PHPUnit 11 |
| `PU12` | PHPUnit 12 |
| `PU13` | PHPUnit 13 |
| `L3` | Livewire 3.x |
| `L4` | Livewire 4.x |
| `T2` | Tailwind 2.x |
| `T3` | Tailwind 3.x |
| `LS` | Laravel Slimmer |
| `TG` | Tests Generator |
| `LF` | Laravel Fixer |

## Notes

- Only check `laravel/framework` for the Laravel version — not `laravel/laravel` or any other package.
- Do not parse versions from `composer.lock` — always use `composer.json`.
- If `package.json` does not exist, skip all Tailwind checks.
- Checks are evaluated in strict priority order — at the first applicable check, summarize the finding and suggest `/shift:run` as the next step. Never invoke `/shift:run` automatically.
- For Livewire and Tailwind (Step 3), both are evaluated together; if both apply, present both before suggesting `/shift:run`.
- If `phpunit/phpunit` is not in `composer.json`, skip the PHPUnit check.
