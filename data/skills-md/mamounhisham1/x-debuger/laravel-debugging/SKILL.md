---
name: laravel-debugging
description: >-
  Debugs Laravel applications with Xdebug integration. Activates when setting breakpoints,
  stepping through code, inspecting variables, analyzing dd() output, debugging routes,
  controllers, queues, or Eloquent queries; or when user mentions debug, breakpoint,
  step into, inspect variables, Xdebug, or troubleshooting errors.
version: 1.0.0
---

# Laravel Debugging with Xdebug

## When to Apply

Activate this skill when:
- Debugging application errors or unexpected behavior
- Investigating 500 errors, exceptions, or fatal errors
- Inspecting variables during code execution
- Tracing request flow through routes, controllers, middleware
- Debugging queue jobs, listeners, or workers
- Analyzing Eloquent query performance and N+1 problems
- Testing API endpoints interactively
- Troubleshooting authentication, authorization, or validation issues
- User mentions: debug, breakpoint, step through, Xdebug, inspect variables, dd(), dump()

## Prerequisites

Before debugging, ensure:
1. Xdebug is installed and configured in PHP
2. Xdebug is listening on port 9003 (Xdebug 3.x)
3. Laravel project has Xdebug enabled in php.ini
4. MCP server is running and connected

Verify Xdebug installation:
```bash
php -v | grep Xdebug
```

Configure Xdebug in php.ini:
```ini
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.client_host=127.0.0.1
xdebug.client_port=9003
```

## Debugging Features

### Breakpoint Management

Set breakpoints to pause code execution at specific lines:

**Add Breakpoint:**
```
Set breakpoint at DealController.php line 88
```

**Conditional Breakpoint:**
```
Add breakpoint at UserController.php line 45 if $user->id === 1
```

**List Breakpoints:**
```
Show all breakpoints
List active breakpoints
```

**Remove Breakpoint:**
```
Remove breakpoint bp_123abc
Clear all breakpoints
```

### Execution Control

Control code execution flow:

**Step Operations:**
- Step into - Enter function calls
- Step over - Skip function internals, go to next line
- Step out - Exit current function
- Continue - Run until next breakpoint

```
Step into the function
Step over to the next line
Step out of this method
Continue execution
Stop debugging
```

### Variable Inspection

Inspect variables at breakpoints:

**Local Variables:**
```
Show local variables
Inspect variables in current scope
Get all local variables
```

**Global Variables:**
```
Show global variables
Display superglobals
```

**Evaluate Expression:**
```
Evaluate $user->id
Check if request->has('token')
Run expression: config('app.debug')
```

**Watch Variables:**
```
Watch variable $userData
Add $errors to watch list
```

### dd() Capture & Analysis

Capture and analyze dump output:

```
Capture the last dump
Show dd() output history
Analyze the most recent dump
Get dump with ID dump_12345
```

The skill provides:
- Non-blocking dump capture
- Historical dump analysis
- Pattern detection (null values, empty arrays, exceptions)
- Laravel-specific insights (Eloquent models, Collections)

## Laravel-Specific Debugging

### Debugging Controllers

**Workflow:**
1. Set breakpoint in controller method
2. Trigger request via browser, Postman, or curl
3. Inspect request data, headers, authenticated user
4. Step through query execution
5. Check validation errors
6. Verify response construction

**Example:**
```
Set breakpoint at DealController@store line 88
Trigger POST /api/v1/deals with test data
Show me the request payload
Inspect the $deal variable
Step through validation
```

### Debugging Routes

**List Routes:**
```
Run: php artisan route:list
Show routes matching /api/deals
```

**Debug Route Matching:**
```
Why is this route not matching?
Check middleware stack for this route
```

### Debugging Queue Jobs

**Launch Configuration:**
Use "Laravel Queue Worker" configuration in VS Code

**Common Issues:**
- Job not processing: Check queue connection and worker status
- Job failing: Set breakpoint in job handle() method
- Memory issues: Inspect large datasets or Eloquent relationships

**Debugging Steps:**
```
Start queue worker with Xdebug
Set breakpoint in ProcessDealJob handle()
Dispatch job with test data
Inspect job payload
Step through processing
```

### Debugging Eloquent Queries

**Enable Query Log:**
```php
DB::enableQueryLog();
// Run queries
dd(DB::getQueryLog());
```

**N+1 Query Detection:**
```
Show me the N+1 problem
Analyze Eloquent relationships
Check for eager loading opportunities
```

**Inspect Query Builder:**
```
Evaluate: Deal::where('status', 'active')->toSql()
Show the bindings for this query
```

## Common Debugging Workflows

### Debug 500 Error

1. Check Laravel logs: `tail -f storage/logs/laravel.log`
2. Set breakpoint in suspected controller/method
3. Trigger the error
4. Inspect exception message and stack trace
5. Check environment: `APP_DEBUG`, database connection
6. Step through code to identify root cause

### Debug Validation Failure

1. Set breakpoint in controller after `validate()` call
2. Inspect `$errors` object
3. Check request data: `$request->all()`
4. Review validation rules in FormRequest
5. Verify expected vs actual data types

### Debug Authentication Issues

1. Set breakpoint in auth middleware
2. Inspect session data
3. Check authenticated user: `Auth::user()`
4. Verify token/credentials
5. Review guards and providers

### Fix N+1 Query Problem

1. Enable query logging
2. Set breakpoint in controller/relationship method
3. Trigger request
4. Inspect query log for repeated queries
5. Add eager loading: `User::with('posts')->get()`
6. Verify queries reduced

## Troubleshooting

### Xdebug Not Connecting

**Symptoms:** Breakpoints not hit, "connection refused" errors

**Solutions:**
1. Verify Xdebug is installed: `php -v | grep Xdebug`
2. Check port: `netstat -an | grep 9003`
3. Verify php.ini configuration
4. Restart PHP-FPM or web server
5. Check firewall settings
6. Ensure Xdebug mode includes "debug"

### Breakpoints Not Hitting

**Symptoms:** Debugger doesn't stop at breakpoints

**Solutions:**
1. Verify file path mappings in VS Code launch.json
2. Check breakpoint line numbers match actual code
3. Ensure code is actually being executed
4. Verify Xdebug is receiving connection: Check `/tmp/xdebug.log`
5. Try stopping and restarting debugging session

### Variable Inspection Not Working

**Symptoms:** Can't see variable values, empty variables

**Solutions:**
1. Ensure execution is paused at breakpoint
2. Check variable scope (local vs global)
3. Verify Xdebug max_depth and max_data settings
4. Try: `evaluate '$variableName'` instead of locals
5. Check for opcache issues: Clear opcache

### dd() Blocking Execution

**Symptoms:** Script terminates at dd(), can't continue

**Solutions:**
1. Use `dump()` instead of `dd()` to continue execution
2. Use breakpoint instead of dd()
3. Check dump capture is enabled
4. Verify write permissions in `/tmp/xdebug-dumps/`

### MCP Server Not Starting

**Symptoms:** Tools not available, connection errors

**Solutions:**
1. Check PHP version: `php -v` (requires 8.2+)
2. Verify required extensions: `php -m | grep -E "xml|sockets"`
3. Check server.php is executable
4. Review MCP server logs
5. Verify .mcp.json configuration

## Best Practices

1. **Use breakpoints instead of dd()** - Non-blocking inspection
2. **Set specific breakpoints** - Avoid stopping everywhere
3. **Use conditional breakpoints** - Only stop when condition is true
4. **Inspect variables at breakpoints** - Better than dump statements
5. **Clear dump history** - Prevent disk space issues
6. **Enable query logging** - For database debugging
7. **Use watch variables** - Track specific values across execution
8. **Review Xdebug logs** - `/tmp/xdebug.log` for connection issues

## Advanced Techniques

### Remote Debugging

Debug production or staging environments:
1. Configure Xdebug to connect to remote IDE
2. Set up SSH tunnel for DBGp connection
3. Use appropriate IDE key
4. Ensure firewall allows Xdebug port

### CLI Debugging

Debug Artisan commands:
```
php artisan migrate --verbose
```
Use "Laravel Artisan Command" launch configuration

### Test Debugging

Debug Pest tests:
1. Set breakpoint in test or application code
2. Run specific test: `vendor/bin/pest --filter test_name`
3. Use "Laravel Tests (Pest)" configuration

### Profiling

Use Xdebug profiling for performance analysis:
```ini
xdebug.mode=profile
```
Analyze cachegrind files with QCacheGrind or similar tools

## Quick Reference

| Task | Command |
|------|---------|
| List breakpoints | `list_breakpoints()` |
| Add breakpoint | `add_breakpoint($file, $line)` |
| Step over | `step_over()` |
| Continue | `continue_execution()` |
| Get locals | `get_locals()` |
| Evaluate | `evaluate_expression($expr)` |
| Capture dump | `capture_last_dump()` |

## Additional Resources

- **Xdebug Documentation:** https://xdebug.org/docs
- **DBGp Protocol:** https://xdebug.org/docs/dbgp
- **Laravel Debugging:** https://laravel.com/docs/12.x/debugging
- **VS Code PHP Debug:** https://github.com/xdebug/vscode-php-debug

For specific debugging scenarios, see:
- `references/xdebug-setup.md` - Xdebug installation guide
- `references/laravel-debugging-patterns.md` - Framework-specific patterns
- `examples/debugging-controller.md` - Controller debugging examples
- `examples/debugging-queue-job.md` - Queue debugging examples
