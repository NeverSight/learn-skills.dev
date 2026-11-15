---
name: wp-admin-ui-development
description: WordPress admin UI review and development guidance. Use when reviewing admin pages, settings screens, menu pages, notices, list tables, metabox-like interfaces, screen options, capability checks, admin scripts or styles, or when user mentions "admin UI", "settings page", "wp-admin", "admin screen", "options page", "list table", "admin menu", "admin notice", "screen options", or "dashboard page". Detects capability issues, Settings API misuse, admin-only performance problems, and UX mistakes in WordPress admin interfaces.
---

# WordPress Admin UI Development Skill

## Overview

Systematic review for WordPress admin interfaces. **Core principle:** Admin UIs should be capability-aware, predictable, and aligned with WordPress admin patterns instead of custom app-style behavior. Review covers menu registration, screen architecture, Settings API usage, notices, script and style loading, list-table patterns, and admin-side UX stability.

## When to Use

**Use when:**
- Reviewing settings pages or plugin dashboards
- Auditing `add_menu_page()` / `add_submenu_page()` usage
- Checking admin forms, notices, and data-entry screens
- Reviewing admin script loading and screen targeting
- Analyzing capability checks for admin pages

**Don't use for:**
- Frontend UI review
- Full security-only audits (use wp-security-review)
- General plugin architecture without admin surface focus (use wp-plugin-development)

## Code Review Workflow

1. **Identify admin surface**
   - Settings page
   - Dashboard widget or tools page
   - Custom list table
   - Modal-heavy admin workflow

2. **Review screen registration**
   - Menu slug, parent slug, capability
   - Dedicated callbacks
   - Screen-specific enqueue logic

3. **Review form and state flow**
   - Settings API or deliberate alternative
   - Nonces and capability checks
   - Stable success/error messaging

4. **Review UX and maintainability**
   - Avoid giant single-screen forms
   - Respect WordPress admin layout and component conventions
   - Load scripts only on relevant screens

5. **Apply severity**
   - **CRITICAL:** Missing capability checks, unrestricted admin actions, admin screens accessible to wrong roles
   - **WARNING:** Global admin asset loading, bypassed Settings API, unstable notice UX, oversized screens
   - **INFO:** Could use core components or cleaner screen split

## File-Type Specific Checks

### Admin Menu Registration

- CRITICAL: Missing capability requirement
- WARNING: Menu callback mixes routing, rendering, and form handling
- INFO: Could move large screens into separate classes or modules

### Settings Forms

- CRITICAL: Missing nonce or capability check on save
- WARNING: Manual `update_option()` everywhere without Settings API structure
- WARNING: No sanitization callback for settings
- INFO: Could split settings into sections/tabs for maintainability

### Admin Scripts and Styles

- WARNING: Scripts loaded on every admin screen
- WARNING: Inline JS for large features
- INFO: Could use screen IDs and conditional enqueues

### Notices and Feedback

- WARNING: Persistent notices without dismissal handling
- WARNING: Success/error states are not tied to actual action outcome
- INFO: Could use clearer empty/loading states

## Search Patterns for Quick Detection (ADM-21)

Use these `rg` commands for quick admin UI scanning.

### CRITICAL Patterns

```bash
# Admin page registration
rg -n "add_menu_page|add_submenu_page|add_options_page|add_management_page" . -g '*.php'

# Admin-post handlers and nonces
rg -n "admin_post_|check_admin_referer|wp_verify_nonce|current_user_can" . -g '*.php'
```

### WARNING Patterns

```bash
# Global admin enqueues
rg -n "admin_enqueue_scripts|wp_enqueue_script|wp_enqueue_style" . -g '*.php'

# Direct option updates in admin pages
rg -n "update_option|add_option" . -g '*.php'

# Admin notices
rg -n "admin_notices|notice-|is-dismissible" . -g '*.php'
```

### INFO Patterns

```bash
# Settings API usage
rg -n "register_setting|add_settings_section|add_settings_field" . -g '*.php'

# Screen targeting helpers
rg -n "get_current_screen|current_screen|\$hook_suffix" . -g '*.php'
```

## Reference Files

- `references/settings-and-screens.md` - Settings pages, screen registration, and admin screen structure
- `references/admin-ux-patterns.md` - Notices, admin scripts, tabs, list tables, and UX expectations

## Output Format (ADM-23)

For each finding include severity, file reference, issue summary, admin impact, and a concrete fix suggestion. Call out where a problem is primarily security, architecture, or UX so follow-up reviews are easy to route.

