---
name: laravel-task-scheduling
description: Schedule tasks with safety; use withoutOverlapping, onOneServer, and visibility settings for reliable cron execution
---

# Task Scheduling

Run scheduled tasks predictably across environments.

## Commands

```
// routes/console.php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::command('reports:daily')
    ->dailyAt('01:00')
    ->withoutOverlapping()
    ->onOneServer()
    ->runInBackground()
    ->evenInMaintenanceMode();
```

## Patterns

- Guard long-running commands with `withoutOverlapping()`
- Use `onOneServer()` when running on multiple nodes
- Emit logs/metrics for visibility; consider notifications on failure
- Feature-flag risky jobs via config/env
