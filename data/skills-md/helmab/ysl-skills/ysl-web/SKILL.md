---
name: ysl-web
description: "Laravel 12 public website: API gateway pattern, Guzzle HTTP client, Blade templates, device token management."
color: "#129748"
---

# Web Public Skill

You are working on the **E-commerce Public Website** — a Laravel 12 + PHP 8.3 public-facing web application that serves product pages, user accounts, and referral features.

## Tech Stack

- Laravel 12, PHP 8.3
- Guzzle HTTP Client
- Intervention Image
- Simple QRCode

## Architecture Overview

See @references/architecture.md for the full directory map.

## Key Pattern: API Gateway

This app acts as a frontend gateway to `young_sia_api`. Controllers call external API endpoints using Guzzle/HTTP facade.

## Workflow

When building a new feature:

1. Create controller → `app/Http/Controllers/{Name}Controller.php` extending `BaseController`
2. Add route file → `routes/web/{feature}.php`
3. Create Blade views → `resources/views/{feature}/`
4. Configure API endpoint → `config/custom.php` or `.env`

## References

- @references/architecture.md — Directory structure and key folders
- @references/controllers.md — BaseController pattern, API calls
- @references/routing.md — Modular route loading
