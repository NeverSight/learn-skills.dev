---
name: wp-debug
description: >
  Start and stop WordPress debug mode from inside a theme or plugin folder.
  Safely enables WP_DEBUG, WP_DEBUG_LOG, SCRIPT_DEBUG, and SAVEQUERIES in
  wp-config.php, tails debug.log in real time, and cleanly restores the
  original config when done. Use when the user says "start debugging",
  "debug WordPress", "enable debug mode", "stop debugging", or
  "turn off debug". Designed for working directories inside
  wp-content/themes/<theme> or wp-content/plugins/<plugin>.
---

# WordPress Debug Mode

Enable and disable WordPress debug mode safely from inside a theme or plugin directory.

## Path Resolution

Before any debug operation, resolve the WordPress root paths. The working directory is assumed to be inside `wp-content/themes/<theme>/` or `wp-content/plugins/<plugin>/`.

1. Check if `../../../wp-config.php` exists (standard depth from theme/plugin root).
2. If not, check `../../../../wp-config.php` (nested projects like `plugin/src/`).
3. If still not found, run:
   ```bash
   find / -maxdepth 5 -name wp-config.php -not -path '*/vendor/*' 2>/dev/null | head -5
   ```
   and ask the user to confirm the correct path.
4. Store the resolved path as `WP_CONFIG`.
5. Derive `WP_CONTENT` — the `wp-content/` directory (parent of `themes/` or `plugins/`).
6. Derive `DEBUG_LOG` as `$WP_CONTENT/debug.log`.

## Start Debugging

When the user says "start debugging", "debug WordPress", or "enable debug mode":

### Step 1 — Check for existing session

If `${WP_CONFIG}.pre-debug-backup` already exists, warn the user that a debug session may already be active and ask whether to continue or restore first.

### Step 2 — Backup

```bash
cp "$WP_CONFIG" "${WP_CONFIG}.pre-debug-backup"
```

### Step 3 — Comment out existing debug constants

In `$WP_CONFIG`, find and comment out (prefix with `// `) any existing `define()` lines for:
- `WP_DEBUG`
- `WP_DEBUG_LOG`
- `WP_DEBUG_DISPLAY`
- `SCRIPT_DEBUG`
- `SAVEQUERIES`

Use `sed` or in-place editing. Never duplicate a `define()` for the same constant.

### Step 4 — Insert debug block

Add the following block **above** the line `/* That's all, stop editing! */` in `$WP_CONFIG`:

```php
// >>> WP DEBUG MODE — added by wp-debug skill
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', true );
define( 'SAVEQUERIES', true );
@ini_set( 'display_errors', 0 );
// <<< END WP DEBUG MODE
```

If the `/* That's all, stop editing! */` marker is not found, insert the block after the last existing `define()` statement instead.

### Step 5 — Prepare log

```bash
truncate -s 0 "$WP_CONTENT/debug.log" 2>/dev/null || touch "$WP_CONTENT/debug.log"
```

### Step 6 — Tail log

```bash
tail -f "$WP_CONTENT/debug.log"
```

### Step 7 — Confirm

Tell the user:
> ✅ Debug mode is ON. Reproduce the issue in your browser — errors will appear here in real time. Say "stop debugging" when you're done.

## Stop Debugging

When the user says "stop debugging", "turn off debug", or "disable debug mode":

### Step 1 — Check for backup

If `${WP_CONFIG}.pre-debug-backup` does NOT exist:
- Check `$WP_CONFIG` for the `// >>> WP DEBUG MODE` marker.
- If found, warn the user there's no backup but debug mode appears active. Offer to manually remove the debug block.
- If not found, inform the user that debug mode does not appear to be active.

### Step 2 — Restore

```bash
cp "${WP_CONFIG}.pre-debug-backup" "$WP_CONFIG"
```

### Step 3 — Remove backup

```bash
rm "${WP_CONFIG}.pre-debug-backup"
```

### Step 4 — Verify

Read `$WP_CONFIG` and confirm:
- The `// >>> WP DEBUG MODE` block is gone.
- No `'WP_DEBUG', true` exists.

### Step 5 — Confirm

Tell the user:
> ✅ Debug mode is OFF. Original wp-config.php has been restored. The debug.log file is preserved at `wp-content/debug.log` in case you still need it.

## Analyzing the Log

When the user asks to "analyze the log", "check errors", or "what went wrong":

1. Read the last 100 lines of `$WP_CONTENT/debug.log`.
2. Group errors by type (PHP Fatal, Warning, Notice, Deprecated).
3. Highlight errors originating from the current theme/plugin directory.
4. Suggest specific fixes for each error.

## Safeguards

- Always use `wp-config.php.pre-debug-backup` as the backup filename, stored next to the original `wp-config.php`.
- Before enabling, always check if a backup already exists.
- Never commit a debug-enabled `wp-config.php` to version control.
- Do NOT delete `debug.log` when stopping — the user may still need it.
- `WP_DEBUG_DISPLAY` is set to `false` so errors are never shown in the browser (safe for staging/live sites).

## What the Debug Block Does

| Constant                | Effect                                                        |
|-------------------------|---------------------------------------------------------------|
| `WP_DEBUG = true`       | Enables WordPress error reporting                             |
| `WP_DEBUG_LOG = true`   | Writes errors to `wp-content/debug.log`                       |
| `WP_DEBUG_DISPLAY = false` | Hides errors from the browser (safe for live/staging)      |
| `SCRIPT_DEBUG = true`   | Uses unminified core CSS/JS files for easier debugging        |
| `SAVEQUERIES = true`    | Stores DB queries in `$wpdb->queries` for analysis            |
