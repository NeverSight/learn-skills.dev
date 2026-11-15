---
name: wp-plugin-development
description: WordPress plugin architecture review and WordPress.org submission standards. Use when reviewing WordPress plugin code, auditing plugin architecture, preparing WordPress.org plugin submission, checking plugin best practices, analyzing custom post types, taxonomies, Settings API, hooks system, internationalization, or when user mentions "plugin review", "plugin development", "plugin best practices", "WordPress.org submission", "Plugin Check", "plugin headers", "activation hook", "deactivation hook", "uninstall", "custom post type", "taxonomy", "Settings API", "hooks", "actions", "filters", "i18n", "text domain", "prefixing", "namespacing". Detects issues in plugin architecture, lifecycle hooks, WordPress.org compliance, and API integration.
---

# WordPress Plugin Development Review Skill

## Overview

Systematic plugin architecture review for WordPress plugins targeting WordPress 6.x+. **Core principle:** WordPress plugins extend functionality through a standardized API ecosystem—lifecycle hooks (activation/deactivation/uninstall), Settings API, hooks system (actions/filters), custom post types/taxonomies, and internationalization. Review validates plugin architecture, naming conventions, WordPress.org compliance standards, and cross-references wp-security-review for security-specific patterns (nonces, capabilities, sanitization). Report findings grouped by file with line numbers, severity labels (CRITICAL/WARNING/INFO), and BAD/GOOD code pairs showing proper implementations.

## When to Use

**Use when:**
- Plugin code architecture review
- Pre-submission check for WordPress.org Plugin Directory
- Auditing plugin lifecycle hooks (activation/deactivation/uninstall)
- Reviewing custom post type or taxonomy registration
- Validating Settings API implementation
- Checking hooks system usage (actions/filters, priority, removal)
- Internationalization (i18n/l10n) audit
- WordPress Plugin Check (PCP) compliance verification
- Prefixing and namespace collision detection

**Don't use for:**
- Theme development (use wp-theme-development when available)
- Gutenberg block development (use wp-block-development when available)
- WooCommerce extension development (use wp-woocommerce-dev when available)
- Security-only audits (use wp-security-review for comprehensive security analysis)
- Performance-only audits (use wp-performance-review)

## Code Review Workflow

Follow this six-step workflow for systematic plugin reviews:

1. **Identify plugin type and context**
   - WordPress.org submission → Apply strictest standards (Plugin Check compliance)
   - Private/enterprise plugin → More flexibility on naming, no readme.txt required
   - Must-use plugin (mu-plugin) → Different loading (no activation hooks needed)
   - Drop-in plugin → Special files (object-cache.php, db.php) with different patterns

2. **Check plugin header completeness and metadata**
   - Required: `Plugin Name` field present
   - Recommended: Version, Description, Author, Text Domain, Requires at least, Requires PHP, License
   - Verify text domain matches plugin slug exactly (lowercase, dashes not underscores)

3. **Scan for CRITICAL patterns** (breaks functionality or causes WordPress.org rejection)
   - Missing `defined( 'ABSPATH' ) || exit;` check in PHP files
   - Unprefixed functions/classes in global scope (namespace collision risk)
   - Missing activation/deactivation hooks for setup/cleanup
   - Text domain mismatch between header and i18n function calls
   - No uninstall cleanup (uninstall.php or register_uninstall_hook missing)
   - `flush_rewrite_rules()` called on `init` hook (expensive operation on every page load)
   - Direct database table creation with `$wpdb->query()` instead of `dbDelta()`
   - Filter callbacks missing return statement
   - REST API routes without `permission_callback` (WordPress 5.5+ requirement)
   - Post type keys exceeding 20 characters
   - Taxonomy names exceeding 32 characters

4. **Check WARNING patterns** (non-standard but functional)
   - Missing internationalization (i18n) on user-facing strings
   - `__()` or `_e()` calls without text domain parameter
   - Hardcoded WordPress paths (`/wp-content/plugins/`)
   - Missing `sanitize_callback` in `register_setting()`
   - Missing `show_in_rest` for Gutenberg compatibility
   - Admin code loading on frontend (missing `is_admin()` check)

5. **Note INFO improvements** (best practices and optimizations)
   - Could use PHP namespaces instead of prefixing
   - Missing version requirements in plugin header (`Requires at least`, `Requires PHP`)
   - Could add `show_in_rest` for Block Editor support
   - Admin assets enqueueing globally (should conditionally load)
   - Missing `Domain Path` in header

6. **Apply context-aware severity** and report
   - WordPress.org context: Strictest enforcement (Plugin Check failures = CRITICAL)
   - Private plugin context: More flexible (prefixing still important, readme.txt optional)
   - Must-use plugin: Adjust expectations (activation hooks not applicable)
   - Report using output format below
   - If security concerns found, add note: "Security issues detected. Run `/wp-sec-review` for comprehensive security analysis."

## File-Type Specific Checks

### Main Plugin File (e.g., `my-plugin.php`)

**Plugin headers (PLG-02):**
- CRITICAL: Missing `Plugin Name` field → WordPress won't recognize plugin
- WARNING: Missing `Text Domain` → Breaks internationalization
- WARNING: Text domain doesn't match plugin slug → WordPress.org rejection
- INFO: Missing `Requires at least` or `Requires PHP` → Can't enforce version requirements

**ABSPATH check (PLG-03):**
- CRITICAL: Missing `defined( 'ABSPATH' ) || exit;` at top → Direct file access possible
- Pattern to detect: PHP file without ABSPATH check in first 10 lines

**Prefixing (PLG-04):**
- CRITICAL: Unprefixed function in global scope → Namespace collision with other plugins
- CRITICAL: Unprefixed class in global scope → Fatal error if another plugin uses same name
- CRITICAL: Unprefixed global variables → Variable collision risk
- WARNING: Options/transients without prefix → Database key collision
- Pattern: `function [a-z_]+\(` without plugin prefix (4-5 char minimum)
- Alternative: PHP namespaces eliminate need for prefixing

**Activation/deactivation hooks (PLG-04):**
- WARNING: Missing `register_activation_hook()` but plugin has setup needs → No way to initialize
- WARNING: Missing `register_deactivation_hook()` but plugin has temp data → No cleanup on deactivation
- Pattern: Look for `register_activation_hook( __FILE__, 'callback' )`

### Uninstall File (`uninstall.php`)

**WP_UNINSTALL_PLUGIN constant check (PLG-05):**
- CRITICAL: `uninstall.php` without `WP_UNINSTALL_PLUGIN` check → Can be executed directly
- Pattern: `if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) { exit; }`

**Cleanup completeness (PLG-05):**
- WARNING: No option cleanup (`delete_option()`) → Leaves plugin data in database
- WARNING: No transient cleanup (`delete_transient()`) → Database bloat
- WARNING: No custom table cleanup (`DROP TABLE`) → Orphaned tables
- WARNING: No user meta cleanup (`delete_metadata( 'user', ... )`) → User data remains
- Context: Only applies if plugin creates these data types

### Custom Post Type Files

**register_post_type() usage (PLG-06):**
- CRITICAL: Post type key exceeds 20 characters → Truncation issues, permalink problems
- CRITICAL: Post type key not prefixed → Query var conflict with WordPress core or other plugins
- WARNING: Missing `show_in_rest => true` → Not accessible in Block Editor
- WARNING: `flush_rewrite_rules()` called on `init` → Performance issue (expensive DB write on every page load)
- Pattern: `register_post_type( 'key', array( ... ) )` hooked to `init`
- Best practice: Post type key max 20 chars, lowercase alphanumeric + dash/underscore

**Rewrite flush timing (PLG-06):**
- CRITICAL: `flush_rewrite_rules()` on `init` hook → DB write on every page load
- Correct pattern: Only call in activation hook after registering post type

### Taxonomy Files

**register_taxonomy() usage (PLG-07):**
- CRITICAL: Taxonomy name exceeds 32 characters → Database error
- CRITICAL: Taxonomy name not prefixed → Collision with core taxonomies or other plugins
- WARNING: Missing `show_in_rest => true` → Not accessible in Block Editor
- Pattern: `register_taxonomy( 'name', 'post_type', array( ... ) )` hooked to `init`
- Best practice: Taxonomy name max 32 chars, lowercase letters + underscore only

### Settings API Files

**register_setting() usage (PLG-08):**
- CRITICAL: `add_settings_field()` without corresponding `register_setting()` → Field won't save
- WARNING: `register_setting()` without `sanitize_callback` → Unsanitized data stored
- WARNING: `register_setting()` without `type` parameter → Type inference unreliable
- Pattern: `register_setting( 'option_group', 'option_name', array( ... ) )` on `admin_init`

**Settings API workflow (PLG-09):**
- WARNING: `add_settings_section()` page slug doesn't match `do_settings_sections()` call → Section won't render
- WARNING: `add_settings_field()` section ID doesn't match `add_settings_section()` ID → Field won't render
- WARNING: Form missing `settings_fields()` call → No nonce protection, options won't save
- WARNING: Form missing `do_settings_sections()` call → Fields won't render
- Pattern: Complete workflow requires `register_setting()` → `add_settings_section()` → `add_settings_field()` → form HTML with `settings_fields()` and `do_settings_sections()`

### Hooks Usage Files

**add_action/add_filter patterns (PLG-10):**
- WARNING: Hook priority not specified when order matters → May run in wrong sequence
- WARNING: `accepted_args` not specified when callback needs multiple parameters → Parameters truncated
- INFO: Could specify priority explicitly for clarity (even when using default 10)
- Pattern: `add_action( 'hook_name', 'callback', $priority, $accepted_args )`

**Filter return requirement (PLG-10):**
- CRITICAL: Filter callback doesn't return value → Breaks filter chain, causes fatal error
- Pattern: `add_filter( 'hook', 'callback' )` where callback has no return statement
- Check: Every filter callback MUST return a value

**Hook removal (PLG-10):**
- WARNING: `remove_action()` or `remove_filter()` params don't match registration → Won't remove hook
- Pattern: Priority and accepted_args must EXACTLY match the original `add_action()`/`add_filter()` call
- Example: `add_action( 'init', 'callback', 15 )` requires `remove_action( 'init', 'callback', 15 )`

**Custom hooks for extensibility (PLG-10):**
- INFO: Plugin could provide custom hooks with `do_action()` or `apply_filters()` for extensibility
- Pattern: `do_action( 'myplugin_after_save', $data )` or `apply_filters( 'myplugin_modify_output', $output )`

### Internationalization (i18n) Files

**Text domain matching (PLG-11):**
- CRITICAL: Text domain in plugin header doesn't match text domain in i18n calls → Translation loading fails
- CRITICAL: Text domain uses underscores instead of dashes → WordPress.org rejection
- CRITICAL: Text domain doesn't match plugin slug → Plugin Check fails
- Pattern: `Text Domain: my-plugin` must match plugin folder/file name exactly

**i18n function usage (PLG-11):**
- WARNING: `__()` or `_e()` without text domain parameter → Falls back to core translations (incorrect)
- WARNING: Variables embedded in translatable strings → Breaks translation extraction
- Pattern: ALWAYS `__( 'Text', 'text-domain' )` never `__( 'Text' )`
- Pattern: Use `sprintf( __( 'Text %s', 'domain' ), $var )` not `__( "Text $var", 'domain' )`

**Pluralization (PLG-11):**
- WARNING: Plural forms handled with if/else instead of `_n()` → Breaks languages with complex plural rules
- Pattern: Use `_n( 'singular', 'plural', $count, 'domain' )` for count-dependent strings

**Context-aware translation (PLG-11):**
- INFO: Could use `_x()` for disambiguation when same English word has different translations
- Pattern: `_x( 'Post', 'noun', 'domain' )` vs `_x( 'Post', 'verb', 'domain' )`

**Escaped translation variants (PLG-11):**
- INFO: Use `esc_html__()` or `esc_attr__()` for combined translation + escaping
- Pattern: `echo esc_html__( 'Text', 'domain' )` instead of `echo esc_html( __( 'Text', 'domain' ) )`

**Translation loading (PLG-11):**
- INFO: `load_plugin_textdomain()` optional for WordPress 4.6+ (auto-loads from translate.wordpress.org)
- Pattern: Hook to `init` if called: `add_action( 'init', 'load_textdomain_callback' )`

### REST API Endpoints (PLG-13, surface-level)

**register_rest_route() usage:**
- CRITICAL: Missing `permission_callback` → WordPress 5.5+ error, endpoint blocked
- CRITICAL: `permission_callback => '__return_true'` on write operations → Unauthenticated access allowed
- Pattern: `register_rest_route( 'namespace/v1', '/route', array( ... ) )` on `rest_api_init` hook
- Note: `__return_true` is CORRECT for public read-only endpoints

**Namespace and versioning:**
- WARNING: Missing version in namespace → No API evolution path
- Pattern: Use `myplugin/v1` not just `myplugin`

**Parameter validation:**
- WARNING: Missing `sanitize_callback` in args → Unsanitized input
- WARNING: Missing `validate_callback` in args → Invalid input accepted
- For security depth: See wp-security-review skill

### AJAX Handlers (PLG-14, surface-level)

**Hook registration:**
- WARNING: Using `admin-ajax.php` for high-frequency calls → Consider REST API for better performance
- Pattern: `add_action( 'wp_ajax_action_name', 'callback' )` for authenticated
- Pattern: `add_action( 'wp_ajax_nopriv_action_name', 'callback' )` for public

**Security checks:**
- Brief reminder: AJAX handlers need nonce verification (`check_ajax_referer()`) and capability checks
- For security depth: See wp-security-review skill

### Admin Menus (PLG-15, surface-level)

**add_menu_page/add_submenu_page:**
- WARNING: Missing capability parameter → No access control
- WARNING: Page callback doesn't verify `current_user_can()` → Capability param insufficient alone
- Pattern: `add_menu_page( $title, $menu_title, 'manage_options', $slug, $callback )`

### Database Tables (PLG-16, surface-level)

**Table creation:**
- CRITICAL: Using `$wpdb->query( "CREATE TABLE..." )` instead of `dbDelta()` → No upgrade path, charset issues
- Pattern: `require_once( ABSPATH . 'wp-admin/includes/upgrade.php' ); dbDelta( $sql );`
- Pattern: `$wpdb->prefix` for table names (not hardcoded `wp_`)
- Pattern: `$wpdb->get_charset_collate()` for charset/collation

**dbDelta SQL formatting requirements:**
- WARNING: SQL not formatted for dbDelta → Table creation fails silently
- Requirements: Two spaces after PRIMARY KEY, no spaces around =, each field on own line

### Cron Jobs (PLG-17, surface-level)

**wp_schedule_event() usage:**
- WARNING: `wp_schedule_event()` without checking `wp_next_scheduled()` → Duplicate schedules
- WARNING: Scheduled event not cleared on deactivation → Cron job continues after plugin disabled
- Pattern: Check `if ( ! wp_next_scheduled( 'hook' ) )` before `wp_schedule_event()`
- Pattern: `wp_clear_scheduled_hook( 'hook' )` in deactivation hook

### Transients (PLG-18, surface-level)

**set_transient() usage:**
- WARNING: Transient keys not prefixed → Key collision with other plugins
- WARNING: Transients without expiration → Behaves like persistent option
- Pattern: `set_transient( 'mypl_key', $value, HOUR_IN_SECONDS )`

## Search Patterns for Quick Detection (PLG-21)

Use these `rg` commands for quick plugin scanning. Organized by severity.

### CRITICAL Patterns

```bash
# Main plugin file should contain "Plugin Name" header
# If this returns nothing, the plugin likely lacks a valid main header.
rg -n "Plugin Name:" . -g '*.php'

# PHP files missing ABSPATH check (direct file access possible)
rg -L --iglob '*.php' "defined\s*\(\s*['\"]ABSPATH['\"]\s*\)|defined\s*\(\s*'ABSPATH'\s*\)" .

# Unprefixed function declarations in global scope (namespace collision risk)
rg -n "^function\s+[a-z_][a-z0-9_]*\s*\(" . -g '*.php'

# Text domain mismatch (compare header vs i18n calls)
# First: inspect the main plugin file header for the expected text domain
rg -n "Text Domain:" . -g '*.php'
# Then: compare that slug with translation calls across the plugin
rg -n "__\(|_e\(|_n\(|_x\(" . -g '*.php'

# flush_rewrite_rules outside activation/deactivation (expensive operation on every page load)
rg -n "flush_rewrite_rules" . -g '*.php'

# Filter callbacks missing return statement (manual follow-up required)
rg -n "add_filter\s*\(" . -g '*.php'

# register_rest_route without permission_callback (manual per-route review)
rg -n "register_rest_route\s*\(" . -g '*.php'
```

### WARNING Patterns

```bash
# Missing register_activation_hook (no setup mechanism)
rg -n "register_activation_hook\s*\(" . -g '*.php'

# Missing uninstall cleanup (no uninstall.php and no register_uninstall_hook)
test -f uninstall.php || rg -n "register_uninstall_hook\s*\(" . -g '*.php'

# i18n functions without obvious text domain parameter (manual confirmation required)
rg -n "__\(|_e\(" . -g '*.php'

# Hardcoded /wp-content/plugins/ paths (breaks on custom WordPress installations)
rg -n "/wp-content/plugins/" . -g '*.php'

# Direct CREATE TABLE with $wpdb->query (should use dbDelta)
rg -n "wpdb->query\s*\(.*CREATE TABLE" . -g '*.php'

# Post type key length check (max 20 characters)
rg -n "register_post_type\s*\(" . -g '*.php'

# Missing show_in_rest in register_post_type (manual per-registration review)
rg -n "register_post_type\s*\(" . -g '*.php'
```

### INFO Patterns

```bash
# Missing "Requires at least" or "Requires PHP" in plugin header
rg -n "Requires at least:|Requires PHP:" . -g '*.php'

# Functions not using PHP namespaces (could modernize)
rg -n "^function\s+myprefix_" . -g '*.php'

# Admin code loading on frontend (manual context check)
rg -n "add_action\s*\(\s*['\"]admin_" . -g '*.php'

# Missing Domain Path in plugin header
rg -n "Domain Path:" . -g '*.php'
```

## Platform Context (PLG-12)

WordPress plugins operate in different distribution contexts. Adjust review severity based on context.

### WordPress.org Submission Context

**Strictest standards apply.** Plugin Check (PCP) tool enforces these requirements:

**Plugin Check (PCP) compliance:**
- Proper plugin headers (Plugin Name required, Text Domain recommended)
- Text domain must match plugin slug exactly (lowercase, dashes not underscores)
- All PHP files must have ABSPATH check (`defined( 'ABSPATH' ) || exit;`)
- All i18n functions must include text domain parameter
- No deprecated WordPress functions
- License compatibility (GPLv2+ required for WordPress.org)
- readme.txt with proper format (or readme.md)
- No hardcoded `/wp-content/` paths (use `WP_CONTENT_DIR` or helper functions)
- Proper prefixing on all global-scope functions/classes/options

**How to verify:** Run Plugin Check tool before submission:
```bash
# Via WP-CLI
wp plugin install plugin-check --activate
wp plugin check my-plugin.php

# Or via WordPress Admin
# Navigate to: Plugins > Add New > Search "Plugin Check"
# Then: Tools > Plugin Check > Select your plugin
```

**WordPress.org context severity escalation:**
- Missing text domain → CRITICAL (was WARNING)
- Text domain mismatch → CRITICAL (was WARNING)
- Missing ABSPATH check → CRITICAL (was WARNING)
- Deprecated functions → CRITICAL (was INFO)

### Private/Enterprise Plugin Context

**More flexibility.** No WordPress.org submission requirements.

**Relaxed requirements:**
- readme.txt not required (internal documentation acceptable)
- Can use proprietary license (no GPL requirement)
- Naming conventions more flexible (though prefixing still important to avoid collisions)
- Can use custom update mechanisms (no WordPress.org update system)

**Still important:**
- Prefixing to avoid conflicts with other plugins
- Lifecycle hooks for proper setup/cleanup
- Security best practices (see wp-security-review)

### Must-Use Plugins (mu-plugins) Context

**Different loading behavior.** Must-use plugins load automatically before regular plugins.

**Key differences:**
- Loaded alphabetically from `wp-content/mu-plugins/` directory
- Load before regular plugins
- Cannot be deactivated via admin UI
- **No activation/deactivation hooks** (they don't activate/deactivate, they just load)
- Can't be updated via WordPress admin (manual file replacement)

**Review adjustments for mu-plugins:**
- WARNING (not CRITICAL): Missing `register_activation_hook()` → Expected for mu-plugins
- WARNING (not CRITICAL): Missing `register_deactivation_hook()` → Expected for mu-plugins
- Still need: Proper prefixing, ABSPATH checks, i18n, security practices

**Pattern to detect mu-plugin context:**
```php
// Check if plugin is loaded as must-use
if ( strpos( __FILE__, WPMU_PLUGIN_DIR ) !== false ) {
    // Running as must-use plugin - skip activation hooks
}
```

### Drop-In Plugins Context

**Special files with specific names.** Drop-ins replace WordPress core functionality.

**Common drop-ins:**
- `object-cache.php` → Object caching backend (Redis, Memcached)
- `db.php` → Custom database class
- `advanced-cache.php` → Page caching system
- `db-error.php` → Custom database error page
- `maintenance.php` → Custom maintenance mode page

**Review adjustments for drop-ins:**
- Skip standard plugin header checks (drop-ins don't use plugin headers)
- Skip activation hook checks (drop-ins load automatically)
- Skip text domain checks (usually internal, not user-facing)
- Focus on: Compatibility with WordPress core expectations for that drop-in type

**Pattern to detect drop-in:**
```php
// Drop-ins are in wp-content/ root, not plugins/
// Check filename against known drop-in names
$drop_ins = array( 'object-cache.php', 'db.php', 'advanced-cache.php', 'db-error.php', 'maintenance.php' );
```

## Quick Reference: Plugin Architecture Patterns

Common plugin patterns organized by concern. All examples use WordPress PHP Coding Standards (spaces inside parentheses, `array()` not `[]`, Yoda conditions).

### Plugin Headers

Complete header block with all recommended fields:

**❌ BAD: Minimal header**
```php
<?php
/**
 * Plugin Name: My Plugin
 */
```

**✅ GOOD: Complete header with all recommended fields**
```php
<?php
/**
 * Plugin Name: My Awesome Plugin
 * Plugin URI: https://example.com/my-awesome-plugin
 * Description: Does amazing things with WordPress
 * Version: 1.0.0
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author: John Doe
 * Author URI: https://example.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: my-awesome-plugin
 * Domain Path: /languages
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly
}
```

### Prefixing and Namespacing

Avoid global namespace pollution:

**❌ BAD: No prefix (namespace collision risk)**
```php
<?php
function save_settings() {
    update_option( 'plugin_settings', $_POST['data'] );
}

class Plugin_Settings {
    // ...
}

add_action( 'admin_init', 'save_settings' );
```

**✅ GOOD: Prefixed functions and classes**
```php
<?php
function mypl_save_settings() {
    update_option( 'mypl_settings', $_POST['data'] );
}

class MyPL_Settings {
    // ...
}

add_action( 'admin_init', 'mypl_save_settings' );
```

**✅ BETTER: Use PHP namespaces**
```php
<?php
namespace MyPlugin\Admin;

function save_settings() {
    update_option( 'mypl_settings', $_POST['data'] ); // Still prefix option names
}

class Settings {
    // ...
}

add_action( 'admin_init', __NAMESPACE__ . '\save_settings' );
```

### Activation/Deactivation/Uninstall Lifecycle

Proper plugin lifecycle management:

**❌ BAD: No lifecycle hooks**
```php
<?php
// Plugin registers CPT on init but never flushes rewrites
add_action( 'init', 'mypl_register_cpt' );

function mypl_register_cpt() {
    register_post_type( 'mypl_book', array( /* args */ ) );
}
```

**✅ GOOD: Complete lifecycle with activation/deactivation/uninstall**
```php
<?php
// Main plugin file: my-plugin.php

// Activation hook
register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_activate() {
    // Set default options
    add_option( 'mypl_version', '1.0.0' );

    // Register CPT before flushing
    mypl_register_cpt();

    // Flush rewrite rules ONLY on activation
    flush_rewrite_rules();
}

// Deactivation hook
register_deactivation_hook( __FILE__, 'mypl_deactivate' );

function mypl_deactivate() {
    // Clear transients
    delete_transient( 'mypl_cache' );

    // Flush rewrite rules
    flush_rewrite_rules();
}

// Init hook for normal operation
add_action( 'init', 'mypl_register_cpt' );

function mypl_register_cpt() {
    register_post_type( 'mypl_book', array( /* args */ ) );
}

// Uninstall file: uninstall.php
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

// Delete all plugin data
delete_option( 'mypl_version' );
delete_option( 'mypl_settings' );

// Drop custom table
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}mypl_data" );
```

### Custom Post Types and Taxonomies

Proper CPT/taxonomy registration with rewrite rule management:

**❌ BAD: Flushes rewrites on every page load**
```php
<?php
add_action( 'init', 'mypl_register_cpt' );

function mypl_register_cpt() {
    register_post_type( 'book', array( // Missing prefix, no show_in_rest
        'public' => true,
    ) );

    flush_rewrite_rules(); // CRITICAL: Runs on EVERY page load
}
```

**✅ GOOD: Prefixed, Gutenberg-ready, flushes only on activation**
```php
<?php
add_action( 'init', 'mypl_register_cpt_and_taxonomy' );

function mypl_register_cpt_and_taxonomy() {
    // Register custom post type (max 20 chars, prefixed)
    register_post_type(
        'mypl_book',
        array(
            'labels'       => array(
                'name'          => __( 'Books', 'my-plugin' ),
                'singular_name' => __( 'Book', 'my-plugin' ),
            ),
            'public'       => true,
            'has_archive'  => true,
            'rewrite'      => array( 'slug' => 'books' ),
            'supports'     => array( 'title', 'editor', 'thumbnail' ),
            'show_in_rest' => true, // Gutenberg support
        )
    );

    // Register custom taxonomy (max 32 chars, prefixed)
    register_taxonomy(
        'mypl_genre',
        'mypl_book',
        array(
            'labels'       => array(
                'name'          => __( 'Genres', 'my-plugin' ),
                'singular_name' => __( 'Genre', 'my-plugin' ),
            ),
            'hierarchical' => true,
            'public'       => true,
            'show_in_rest' => true, // Gutenberg support
        )
    );
}

// Flush rewrites ONLY on activation
register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_activate() {
    mypl_register_cpt_and_taxonomy(); // Register first
    flush_rewrite_rules(); // Then flush (only once)
}

register_deactivation_hook( __FILE__, 'mypl_deactivate' );

function mypl_deactivate() {
    flush_rewrite_rules(); // Clean up rewrite rules
}
```

### Settings API

Complete Settings API workflow:

**❌ BAD: add_settings_field without register_setting (won't save)**
```php
<?php
add_action( 'admin_init', 'mypl_settings_init' );

function mypl_settings_init() {
    add_settings_section( 'mypl_section', 'Settings', null, 'mypl-settings' );

    add_settings_field(
        'mypl_api_key',
        'API Key',
        'mypl_api_key_callback',
        'mypl-settings',
        'mypl_section'
    );
    // Missing register_setting() - field won't save!
}
```

**✅ GOOD: Complete Settings API workflow**
```php
<?php
add_action( 'admin_init', 'mypl_register_settings' );

function mypl_register_settings() {
    // 1. Register setting (declares option name and sanitization)
    register_setting(
        'mypl_options_group',    // Option group
        'mypl_settings',          // Option name
        array(
            'type'              => 'array',
            'sanitize_callback' => 'mypl_sanitize_settings',
            'default'           => array(
                'api_key' => '',
                'enabled' => false,
            ),
        )
    );

    // 2. Add settings section
    add_settings_section(
        'mypl_main_section',
        __( 'Main Settings', 'my-plugin' ),
        'mypl_section_callback',
        'mypl-settings'
    );

    // 3. Add settings fields
    add_settings_field(
        'mypl_api_key',
        __( 'API Key', 'my-plugin' ),
        'mypl_api_key_callback',
        'mypl-settings',
        'mypl_main_section'
    );

    add_settings_field(
        'mypl_enabled',
        __( 'Enable Feature', 'my-plugin' ),
        'mypl_enabled_callback',
        'mypl-settings',
        'mypl_main_section'
    );
}

function mypl_section_callback() {
    echo '<p>' . esc_html__( 'Configure your plugin settings below.', 'my-plugin' ) . '</p>';
}

function mypl_api_key_callback() {
    $options = get_option( 'mypl_settings' );
    $value = isset( $options['api_key'] ) ? $options['api_key'] : '';
    ?>
    <input type="text"
           name="mypl_settings[api_key]"
           value="<?php echo esc_attr( $value ); ?>"
           class="regular-text">
    <?php
}

function mypl_enabled_callback() {
    $options = get_option( 'mypl_settings' );
    $checked = isset( $options['enabled'] ) && $options['enabled'];
    ?>
    <input type="checkbox"
           name="mypl_settings[enabled]"
           value="1"
           <?php checked( $checked, true ); ?>>
    <?php
}

function mypl_sanitize_settings( $input ) {
    $sanitized = array();

    if ( isset( $input['api_key'] ) ) {
        $sanitized['api_key'] = sanitize_text_field( $input['api_key'] );
    }

    $sanitized['enabled'] = isset( $input['enabled'] ) && $input['enabled'] ? true : false;

    return $sanitized;
}

// Settings page HTML
function mypl_settings_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <form method="post" action="options.php">
            <?php
            // Output nonce, action, option_page fields
            settings_fields( 'mypl_options_group' );

            // Output sections and fields
            do_settings_sections( 'mypl-settings' );

            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```

### Hooks System

Actions and filters with priority management:

**❌ BAD: Filter without return statement (fatal error)**
```php
<?php
add_filter( 'the_content', 'mypl_modify_content' );

function mypl_modify_content( $content ) {
    if ( is_single() ) {
        $content .= '<p>Footer text</p>';
    }
    // Missing return! Fatal error.
}
```

**✅ GOOD: Complete hooks usage with priority and return**
```php
<?php
// Action with priority (runs before core at priority 10)
add_action( 'init', 'mypl_register_cpt', 9 );

function mypl_register_cpt() {
    register_post_type( 'mypl_book', array( /* args */ ) );
}

// Filter with return (CRITICAL)
add_filter( 'the_content', 'mypl_modify_content', 10, 1 );

function mypl_modify_content( $content ) {
    if ( is_single() ) {
        $content .= '<p>Footer text</p>';
    }
    return $content; // ALWAYS return in filters
}

// Multiple parameters with accepted_args
add_filter( 'wp_mail', 'mypl_modify_email', 10, 1 );

function mypl_modify_email( $args ) {
    $args['from'] = 'Custom <custom@example.com>';
    return $args;
}

// Removing hooks (MUST match exact registration params)
add_action( 'wp_footer', 'mypl_footer_code', 15 );

// To remove: priority must match
remove_action( 'wp_footer', 'mypl_footer_code', 15 );

// Create custom hooks for extensibility
function mypl_process_data( $data ) {
    // Allow other plugins to modify data
    $data = apply_filters( 'mypl_before_process', $data );

    // Process data
    $result = process( $data );

    // Allow other plugins to hook after processing
    do_action( 'mypl_after_process', $result );

    return $result;
}
```

### Internationalization

Text domain matching and placeholder usage:

**❌ BAD: Variable embedded in translatable string**
```php
<?php
$count = 5;
echo __( "You have $count messages", 'my-plugin' ); // Breaks translation extraction

// Missing text domain
echo __( 'Save Settings' );

// Text domain mismatch
// Plugin folder: my-awesome-plugin
echo __( 'Save', 'my_plugin' ); // Underscore instead of dash
```

**✅ GOOD: Placeholders with sprintf, correct text domain**
```php
<?php
// Basic translation with text domain
echo __( 'Settings saved successfully', 'my-awesome-plugin' );

// Translation with echo
_e( 'Click here to continue', 'my-awesome-plugin' );

// Placeholders with sprintf (NOT embedded variables)
$count = 5;
echo sprintf(
    __( 'You have %d messages', 'my-awesome-plugin' ),
    $count
);

// Pluralization with _n()
echo sprintf(
    _n(
        'One post found',
        '%d posts found',
        $count,
        'my-awesome-plugin'
    ),
    number_format_i18n( $count )
);

// Context-aware translation with _x()
echo _x( 'Post', 'noun - blog post', 'my-awesome-plugin' );
echo _x( 'Post', 'verb - submit', 'my-awesome-plugin' );

// Escaped output + translation
echo '<h1>' . esc_html__( 'Welcome', 'my-awesome-plugin' ) . '</h1>';
echo '<input placeholder="' . esc_attr__( 'Enter your name', 'my-awesome-plugin' ) . '">';

// Load text domain on init (optional in WP 4.6+)
add_action( 'init', 'mypl_load_textdomain' );

function mypl_load_textdomain() {
    load_plugin_textdomain(
        'my-awesome-plugin',
        false,
        dirname( plugin_basename( __FILE__ ) ) . '/languages'
    );
}
```

### REST API Registration (surface-level)

**❌ BAD: Missing permission_callback (WordPress 5.5+ error)**
```php
<?php
add_action( 'rest_api_init', 'mypl_register_routes' );

function mypl_register_routes() {
    register_rest_route( 'mypl/v1', '/posts', array(
        'methods'  => 'GET',
        'callback' => 'mypl_get_posts',
        // Missing: 'permission_callback' (WordPress 5.5+ blocks this)
    ) );
}
```

**✅ GOOD: Complete REST endpoint with permission_callback and validation**
```php
<?php
add_action( 'rest_api_init', 'mypl_register_routes' );

function mypl_register_routes() {
    // Public read-only endpoint
    register_rest_route(
        'mypl/v1', // Namespace with version
        '/posts',
        array(
            'methods'             => 'GET',
            'callback'            => 'mypl_get_posts',
            'permission_callback' => '__return_true', // Explicitly public (OK for read-only)
            'args'                => array(
                'per_page' => array(
                    'default'           => 10,
                    'sanitize_callback' => 'absint',
                    'validate_callback' => function( $param ) {
                        return is_numeric( $param ) && $param > 0 && $param <= 100;
                    },
                ),
            ),
        )
    );

    // Protected write endpoint
    register_rest_route(
        'mypl/v1',
        '/posts/(?P<id>\d+)',
        array(
            'methods'             => 'DELETE',
            'callback'            => 'mypl_delete_post',
            'permission_callback' => function() {
                return current_user_can( 'delete_posts' );
            },
            'args'                => array(
                'id' => array(
                    'validate_callback' => function( $param ) {
                        return is_numeric( $param );
                    },
                ),
            ),
        )
    );
}

function mypl_get_posts( $request ) {
    $per_page = $request->get_param( 'per_page' );
    $posts = get_posts( array( 'posts_per_page' => $per_page ) );
    return rest_ensure_response( $posts );
}

function mypl_delete_post( $request ) {
    $post_id = $request->get_param( 'id' );
    $result = wp_delete_post( $post_id, true );

    if ( ! $result ) {
        return new WP_Error(
            'delete_failed',
            __( 'Failed to delete post', 'my-plugin' ),
            array( 'status' => 500 )
        );
    }

    return rest_ensure_response( array( 'deleted' => true, 'id' => $post_id ) );
}
```

**Note:** For security depth on REST endpoints (nonce validation, capability checks, input sanitization), see wp-security-review skill.

### AJAX Handlers (surface-level)

**✅ GOOD: AJAX handler registration**
```php
<?php
// Authenticated users
add_action( 'wp_ajax_mypl_save_data', 'mypl_save_data_callback' );

// Public (non-authenticated)
add_action( 'wp_ajax_nopriv_mypl_save_data', 'mypl_save_data_callback' );

function mypl_save_data_callback() {
    // Security checks (see wp-security-review for depth)
    check_ajax_referer( 'mypl_nonce', 'nonce' );

    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_send_json_error( 'Insufficient permissions' );
    }

    $data = sanitize_text_field( $_POST['data'] );

    // Process data
    update_option( 'mypl_data', $data );

    wp_send_json_success( 'Data saved' );
}
```

### Conditional Loading (PLG-20)

Separate admin from public code:

**❌ BAD: Admin code loading on every page**
```php
<?php
add_action( 'wp_enqueue_scripts', 'mypl_enqueue_admin_assets' );

function mypl_enqueue_admin_assets() {
    // Admin assets loading on public pages (unnecessary)
    wp_enqueue_script( 'mypl-admin', plugin_dir_url( __FILE__ ) . 'admin.js' );
}
```

**✅ GOOD: Conditional admin loading**
```php
<?php
// Only load admin code in admin context
if ( is_admin() ) {
    require_once plugin_dir_path( __FILE__ ) . 'admin/class-admin.php';
}

// Admin-specific assets
add_action( 'admin_enqueue_scripts', 'mypl_enqueue_admin_assets' );

function mypl_enqueue_admin_assets() {
    wp_enqueue_script(
        'mypl-admin',
        plugin_dir_url( __FILE__ ) . 'admin/admin.js',
        array( 'jquery' ),
        '1.0.0',
        true
    );
}

// Public-facing assets
add_action( 'wp_enqueue_scripts', 'mypl_enqueue_public_assets' );

function mypl_enqueue_public_assets() {
    wp_enqueue_script(
        'mypl-public',
        plugin_dir_url( __FILE__ ) . 'public/public.js',
        array( 'jquery' ),
        '1.0.0',
        true
    );
}
```

### Function/Class Existence Checks (PLG-19)

Prevent fatal errors from conflicts:

**✅ GOOD: Existence checks for functions and classes**
```php
<?php
// Function existence check
if ( ! function_exists( 'mypl_init' ) ) {
    function mypl_init() {
        // Plugin initialization
    }
}

// Class existence check
if ( ! class_exists( 'MyPL_Plugin' ) ) {
    class MyPL_Plugin {
        // Plugin class
    }
}
```

## Severity Definitions (PLG-23)

| Severity | Definition | Examples |
|----------|------------|----------|
| **CRITICAL** | Will cause WordPress.org rejection OR breaks plugin functionality OR causes fatal errors | Missing `Plugin Name` header, unprefixed global functions causing namespace collision, text domain mismatch, missing ABSPATH check, direct DB table creation without dbDelta, filter callback without return statement, post type key > 20 chars, taxonomy name > 32 chars, `flush_rewrite_rules()` on init hook, REST route without permission_callback (WP 5.5+) |
| **WARNING** | Non-standard patterns causing maintainability or compatibility issues, but plugin still functions | Missing internationalization (i18n), `__()` without text domain, hardcoded `/wp-content/` paths, missing `sanitize_callback` in `register_setting()`, missing `show_in_rest` for Gutenberg support, `wp_schedule_event()` without checking for existing schedule, transients without expiration |
| **INFO** | Best practice improvements and modernization opportunities | Could use PHP namespaces instead of prefixing, missing version requirements in header (`Requires at least`, `Requires PHP`), admin code loading on frontend, missing `Domain Path` in header, could use `_x()` for context-aware translation |

## Output Format (PLG-23)

Report findings grouped by FILE, with line numbers and severity labels. Use BAD/GOOD code pairs for each finding.

```
# WordPress Plugin Review: my-awesome-plugin

## FILE: my-awesome-plugin.php

### Line 15: CRITICAL - Missing ABSPATH check
Direct file access possible. Add ABSPATH check at top of all PHP files.

❌ BAD:
<?php
/**
 * Plugin Name: My Plugin
 */

function mypl_init() { ... }

✅ GOOD:
<?php
/**
 * Plugin Name: My Plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function mypl_init() { ... }

### Line 45: WARNING - Missing text domain in i18n call
Translation won't work. Always include text domain parameter.

❌ BAD:
echo __( 'Save Settings' );

✅ GOOD:
echo __( 'Save Settings', 'my-awesome-plugin' );

## FILE: includes/class-cpt.php

### Line 23: CRITICAL - flush_rewrite_rules on init hook
Expensive DB write on every page load. Move to activation hook.

❌ BAD:
add_action( 'init', 'mypl_register_cpt' );

function mypl_register_cpt() {
    register_post_type( 'book', array( /* ... */ ) );
    flush_rewrite_rules(); // Runs on EVERY request
}

✅ GOOD:
add_action( 'init', 'mypl_register_cpt' );

function mypl_register_cpt() {
    register_post_type( 'mypl_book', array( /* ... */ ) );
}

register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_activate() {
    mypl_register_cpt();
    flush_rewrite_rules(); // Only on activation
}

## SUMMARY

**Total issues: 15**
- CRITICAL: 4 (must fix for WordPress.org submission)
- WARNING: 8 (non-standard patterns)
- INFO: 3 (best practice improvements)

**WordPress.org readiness:** NOT READY - 4 critical issues block submission

**Security note:** This review focused on plugin architecture and WordPress.org compliance. Security issues detected (missing nonce in AJAX handler, unsanitized input in form). Run `/wp-sec-review` for comprehensive security analysis.
```

## Common Mistakes (PLG-24)

Patterns that look like issues but are NOT problems:

| Pattern | Why It's NOT a Problem | Context |
|---------|------------------------|---------|
| **mu-plugin without activation hooks** | Must-use plugins load automatically, don't activate/deactivate | Normal for mu-plugins in `wp-content/mu-plugins/` |
| **Drop-in plugin without standard header** | Drop-ins use special filenames, not plugin headers | Valid for `object-cache.php`, `db.php`, `advanced-cache.php`, etc. |
| **Private plugin without readme.txt** | readme.txt only required for WordPress.org submissions | Private/enterprise plugins use internal docs |
| **`__return_true` in REST permission_callback for GET** | Public read-only endpoints don't need authentication | Correct pattern for public REST API reads |
| **Settings API sanitize_callback changing type** | Can convert checkbox string to boolean, text to array, etc. | Valid transformation, not a bug |
| **No text domain for core WordPress strings** | Core strings already translated | Valid when passing strings to `wp_die()`, `__()` with core strings |
| **Short prefix (3 chars) with namespace** | PHP namespace provides collision protection | Acceptable when using `namespace MyPlugin\Feature;` |
| **No activation hook when plugin has no setup** | Not all plugins need database tables, options, or rewrite flushes | Valid for simple plugins (shortcodes, filters only) |
| **`flush_rewrite_rules()` in admin settings save** | Acceptable when user explicitly changes permalink structure | Valid in settings pages when slug/rewrite changes |
| **Direct `$wpdb->query()` for DROP TABLE** | `dbDelta()` is for CREATE/ALTER, not DROP | Correct pattern in `uninstall.php` |
| **Missing i18n on internal debug strings** | Developer-facing strings don't need translation | Valid for `error_log()`, internal comments |
| **`register_taxonomy()` without show_in_rest** | Not all taxonomies need Gutenberg UI | Valid for backend-only taxonomies |

## WordPress.org Compliance Checklist (PLG-12)

Quick checklist for Plugin Check standards before WordPress.org submission:

- [ ] Plugin Name header present in main plugin file
- [ ] Text Domain matches plugin slug exactly (lowercase, dashes not underscores)
- [ ] All PHP files have ABSPATH check (`defined( 'ABSPATH' ) || exit;`)
- [ ] All i18n functions include text domain parameter
- [ ] No deprecated WordPress functions used
- [ ] License header present (GPLv2 or later recommended)
- [ ] readme.txt with proper format (or readme.md)
- [ ] No hardcoded `/wp-content/` or `/wp-content/plugins/` paths
- [ ] Proper prefixing on all global-scope functions/classes/options/transients
- [ ] uninstall.php or register_uninstall_hook present for cleanup
- [ ] No `eval()`, `base64_decode()`, or obfuscated code
- [ ] Version requirements specified (`Requires at least`, `Requires PHP`)

**Verification command:**
```bash
wp plugin install plugin-check --activate
wp plugin check my-plugin.php
```

## Deep-Dive References

For advanced plugin development patterns, load these companion reference documents:

| Task | Reference to Load |
|------|-------------------|
| Plugin file structure, singleton patterns, autoloading, dependency injection, main plugin class architecture | `references/architecture-patterns.md` |
| Action/filter lifecycle, priority system, hook removal, custom hooks, pluggable functions, hook naming conventions | `references/hooks-guide.md` |
| Class-based plugin architecture, PHP namespaces, PSR-4 autoloading, trait usage, abstract classes, service containers | `references/oop-patterns.md` |
| Settings API workflow, Options API best practices, REST API schema validation, Transients API, custom database tables with dbDelta | `references/api-patterns.md` |

**Note:** Reference docs provide deep-dive content. This SKILL.md is self-sufficient for standard plugin reviews.

**Security crossover:** When encountering security-relevant patterns (form handlers without nonces, AJAX without capability checks, REST endpoints without permission validation), this skill provides brief reminders but defers to wp-security-review for comprehensive security analysis. The three-step security pattern (nonce + capability + sanitize) applies to all state-changing operations. Use `/wp-sec-review` command for detailed security audit.
