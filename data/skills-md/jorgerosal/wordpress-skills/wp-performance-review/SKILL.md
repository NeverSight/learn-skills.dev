---
name: wp-performance-review
description: WordPress performance code review and optimization analysis. Use when reviewing WordPress PHP code for performance issues, auditing themes/plugins for scalability, optimizing WP_Query, analyzing caching strategies, checking code before launch, or detecting anti-patterns, or when user mentions "performance review", "optimization audit", "slow WordPress", "slow queries", "high-traffic", "scale WordPress", "code review", "timeout", "500 error", "out of memory", or "site won't load". Detects anti-patterns in database queries, hooks, object caching, AJAX, template loading, and editor-side performance.
---

# WordPress Performance Review Skill

## Overview

Systematic performance code review for WordPress themes, plugins, and custom code. **Core principle:** Scan critical issues first (OOM, unbounded queries, cache bypass), then warnings, then optimizations. Report with line numbers and severity levels.

## When to Use

**Use when:**
- Reviewing PR/code for WordPress theme or plugin
- User reports slow page loads, timeouts, or 500 errors
- Auditing before high-traffic event (launch, sale, viral moment)
- Optimizing WP_Query or database operations
- Investigating memory exhaustion or DB locks

**Don't use for:**
- Security-only audits (use wp-security-review when available)
- Gutenberg block development patterns (use wp-block-development when available)
- General PHP code review not specific to WordPress
- Product or UX review that does not involve WordPress performance behavior

## Code Review Workflow

1. **Identify file type** and apply relevant checks below
2. **Scan for critical patterns first** (OOM, unbounded queries, cache bypass)
3. **Check warnings** (inefficient but not catastrophic)
4. **Note optimizations** (nice-to-have improvements)
5. **Report with line numbers** using output format below

## File-Type Specific Checks

### Plugin/Theme PHP Files (`functions.php`, `plugin.php`, `*.php`)
Scan for:
- `query_posts()` → CRITICAL: Never use - breaks main query
- `posts_per_page.*-1` or `numberposts.*-1` → CRITICAL: Unbounded query
- `session_start()` → CRITICAL: Bypasses page cache
- `add_action.*init.*` or `add_action.*wp_loaded` → Check if expensive code runs every request
- `update_option` or `add_option` in non-admin context → WARNING: DB writes on page load
- `wp_remote_get` or `wp_remote_post` without caching → WARNING: Blocking HTTP

### WP_Query / Database Code
Scan for:
- Missing `posts_per_page` argument → WARNING: Defaults to blog setting
- `'meta_query'` with `'value'` comparisons → WARNING: Unindexed column scan
- Large `post__not_in` arrays with pagination/sorting → WARNING: Can generate expensive SQL; review case-by-case
- `LIKE '%term%'` (leading wildcard) → WARNING: Full table scan
- Missing `no_found_rows => true` when not paginating → INFO: Unnecessary count

### AJAX Handlers (`wp_ajax_*`, REST endpoints)
Scan for:
- `admin-ajax.php` usage → INFO: Consider REST API instead
- POST method for read operations → WARNING: Bypasses cache
- `setInterval` or polling patterns → CRITICAL: Self-DDoS risk
- Missing nonce verification → Security issue (not performance, but flag it)

### Template Files (`*.php` in theme)
Scan for:
- Custom queries, uncached `get_post_meta()`, or remote calls inside loops → WARNING: Repeated work / N+1 risk
- Database queries inside loops (N+1) → CRITICAL: Query multiplication
- `wp_remote_get` in templates → WARNING: Blocks rendering

### JavaScript Files
Scan for:
- `$.post(` for read operations → WARNING: Use GET for cacheability
- `setInterval.*fetch\|ajax` → CRITICAL: Polling pattern
- `import _ from 'lodash'` → WARNING: Full library import bloats bundle
- Inline `<script>` making AJAX calls on load → Check necessity

### Block Editor / Gutenberg Files (`block.json`, `*.js` in blocks/)
Scan for:
- Heavy editor-side data fetching or preview logic → WARNING: Slows editor load
- `wp_kses_post($content)` in render callbacks → WARNING: Breaks InnerBlocks
- Large editor bundles or broad imports → WARNING: Bloats editor runtime

### Asset Registration (`functions.php`, `*.php`)
Scan for:
- `wp_enqueue_script` without version → INFO: Cache busting issues
- `wp_enqueue_script` without `defer`/`async` strategy → INFO: Blocks rendering
- Missing `THEME_VERSION` constant → INFO: Version management
- `wp_enqueue_script` without conditional check → WARNING: Assets load globally when only needed on specific pages

### Transients & Options
Scan for:
- `set_transient` with dynamic keys (e.g., `user_{$id}`) → WARNING: Table bloat without object cache
- `set_transient` for frequently-changing data → WARNING: Defeats caching purpose
- Large data in transients on shared hosting → WARNING: DB bloat without object cache

### WP-Cron
Scan for:
- Missing `DISABLE_WP_CRON` constant → INFO: Cron runs on page requests
- Long-running cron callbacks (loops over all users/posts) → CRITICAL: Blocks cron queue
- `wp_schedule_event` without checking if already scheduled → WARNING: Duplicate schedules

## Search Patterns for Quick Detection

```bash
# Critical issues - scan these first
rg -n "posts_per_page\s*.*-1|numberposts\s*.*-1" .
rg -n "query_posts\s*\(" .
rg -n "session_start\s*\(" .
rg -n "setInterval.*(fetch|ajax|\\$\\.)" .

# Database writes on frontend
rg -n "update_option|add_option" . -g '*.php'

# Uncached expensive functions
rg -n "url_to_postid|attachment_url_to_postid|count_user_posts" .

# External HTTP without caching
rg -n "wp_remote_get|wp_remote_post|file_get_contents\s*\(\s*['\"]https?://" .

# Cache bypass risks
rg -n "setcookie|session_start" .

# PHP code anti-patterns
rg -n "in_array\s*\(" . -g '*.php'    # Manually verify strict comparison
rg -n "<<<" .
rg -n "cache_results\s*=>\s*false|cache_results\s*,\s*false" .

# JavaScript bundle issues
rg -n "import\s+_\s+from\s+['\"]lodash['\"]" . -g '*.{js,jsx,ts,tsx}'

# Asset loading issues
rg -n "wp_enqueue_script|wp_enqueue_style" . -g '*.php'

# Transient misuse
rg -n "set_transient\s*\([^,]+\\$" . -g '*.php'
rg -n "set_transient" . -g '*.php'    # Manually confirm a preceding get_transient() check

# WP-Cron issues
rg -n "wp_schedule_event" . -g '*.php'  # Manually confirm wp_next_scheduled() guard
```

## Platform Context

Different hosting environments require different approaches:

**Managed WordPress Hosts** (WP Engine, Pantheon, Pressable, WordPress VIP, etc.):
- Often provide object caching out of the box
- May have platform-specific helper functions (e.g., `wpcom_vip_*` on VIP)
- Check host documentation for recommended patterns

**Self-Hosted / Standard Hosting**:
- Implement object caching wrappers manually for expensive functions
- Consider Redis or Memcached plugins for persistent object cache
- More responsibility for caching layer configuration

**Shared Hosting**:
- Be extra cautious about unbounded queries and external HTTP
- Limited resources mean performance issues surface faster
- May lack persistent object cache entirely

## Quick Reference: Critical Anti-Patterns

### Database Queries
```php
// ❌ CRITICAL: Unbounded query.
'posts_per_page' => -1

// ✅ GOOD: Set reasonable limit, paginate if needed.
'posts_per_page' => 100,
'no_found_rows'  => true, // Skip count if not paginating.

// ❌ CRITICAL: Never use query_posts().
query_posts( 'cat=1' ); // Breaks pagination, conditionals.

// ✅ GOOD: Use WP_Query or pre_get_posts filter.
$query = new WP_Query( array( 'cat' => 1 ) );
// Or modify main query:
add_action( 'pre_get_posts', function( $query ) {
    if ( $query->is_main_query() && ! is_admin() ) {
        $query->set( 'cat', 1 );
    }
} );

// ❌ WARNING: Unvalidated ID can hide a logic bug and trigger needless queries.
$query = new WP_Query( array( 'p' => intval( $maybe_false_id ) ) );

// ✅ GOOD: Validate ID before querying.
$post_id = absint( $maybe_false_id );
if ( $post_id > 0 ) {
    $query = new WP_Query( array( 'p' => $post_id ) );
}

// ❌ WARNING: LIKE with leading wildcard (full table scan).
$wpdb->get_results( "SELECT * FROM wp_posts WHERE post_title LIKE '%term%'" );

// ✅ GOOD: Use trailing wildcard only, or use WP_Query 's' parameter.
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM wp_posts WHERE post_title LIKE %s",
    $wpdb->esc_like( $term ) . '%'
) );

// ❌ WARNING: Large NOT IN queries can become expensive, especially with pagination.
'post__not_in' => $excluded_ids

// ✅ GOOD: Prefer positive inclusion, smaller exclusion lists, or precomputed candidate IDs.
'post__in' => $candidate_ids
```

### Hooks & Actions
```php
// ❌ WARNING: Code runs on every request via init.
add_action( 'init', 'expensive_function' );

// ✅ GOOD: Check context before running expensive code.
add_action( 'init', function() {
    if ( is_admin() || wp_doing_cron() ) {
        return;
    }
    // Frontend-only code here.
} );

// ❌ CRITICAL: Database writes on every page load.
add_action( 'wp_head', 'prefix_bad_tracking' );
function prefix_bad_tracking() {
    update_option( 'last_visit', time() );
}

// ✅ GOOD: Use object cache buffer, flush via cron.
add_action( 'shutdown', function() {
    wp_cache_incr( 'page_views_buffer', 1, 'counters' );
} );

// ❌ WARNING: Using admin-ajax.php instead of REST API.
// Prefer: register_rest_route() - leaner bootstrap.
```

### PHP Code
```php
// ❌ WARNING: O(n) lookup - use isset() with associative array.
in_array( $value, $array ); // Also missing strict = true.

// ✅ GOOD: O(1) lookup with isset().
$allowed = array( 'foo' => true, 'bar' => true );
if ( isset( $allowed[ $value ] ) ) {
    // Process.
}

// ❌ WARNING: Heredoc prevents late escaping.
$html = <<<HTML
<div>$unescaped_content</div>
HTML;

// ✅ GOOD: Escape at output.
printf( '<div>%s</div>', esc_html( $content ) );
```

### Caching Issues
```php
// ❌ WARNING: Uncached expensive function calls.
url_to_postid( $url );
attachment_url_to_postid( $attachment_url );
count_user_posts( $user_id );
wp_oembed_get( $url );

// ✅ GOOD: Wrap with object cache (works on any host).
function prefix_cached_url_to_postid( $url ) {
    $cache_key = 'url_to_postid_' . md5( $url );
    $post_id   = wp_cache_get( $cache_key, 'url_lookups' );

    if ( false === $post_id ) {
        $post_id = url_to_postid( $url );
        wp_cache_set( $cache_key, $post_id, 'url_lookups', HOUR_IN_SECONDS );
    }

    return $post_id;
}

// ✅ GOOD: On WordPress VIP, use platform helpers instead.
// wpcom_vip_url_to_postid(), wpcom_vip_attachment_url_to_postid(), etc.

// ❌ WARNING: Large autoloaded options.
add_option( 'prefix_large_data', $data ); // Add: , '', 'no' for autoload.

// ❌ INFO: Missing wp_cache_get_multiple for batch lookups.
foreach ( $ids as $id ) {
    wp_cache_get( "key_{$id}" );
}
```

### AJAX & External Requests
```javascript
// ❌ WARNING: AJAX POST request (bypasses cache).
$.post( ajaxurl, data ); // Prefer: $.get() for read operations.

// ❌ CRITICAL: Polling pattern (self-DDoS).
setInterval( () => fetch( '/wp-json/...' ), 5000 );
```

```php
// ❌ WARNING: Synchronous external HTTP in page load.
wp_remote_get( $url ); // Cache result or move to cron.

// ✅ GOOD: Set timeout and handle errors.
$response = wp_remote_get( $url, array( 'timeout' => 2 ) );
if ( is_wp_error( $response ) ) {
    return get_fallback_data();
}
```

### WP Cron
```php
// INFO: On high-traffic or cron-heavy sites, request-driven cron may not be enough.
// Consider adding to wp-config.php:
define( 'DISABLE_WP_CRON', true );
// Run via server cron: * * * * * wp cron event run --due-now

// ❌ CRITICAL: Long-running cron blocks entire queue.
add_action( 'my_daily_sync', function() {
    foreach ( get_users() as $user ) { // 50k users = hours.
        sync_user_data( $user );
    }
} );

// ✅ GOOD: Batch processing with rescheduling.
add_action( 'my_batch_sync', function() {
    $offset = (int) get_option( 'sync_offset', 0 );
    $users  = get_users( array( 'number' => 100, 'offset' => $offset ) );

    if ( empty( $users ) ) {
        delete_option( 'sync_offset' );
        return;
    }

    foreach ( $users as $user ) {
        sync_user_data( $user );
    }

    update_option( 'sync_offset', $offset + 100 );
    wp_schedule_single_event( time() + 60, 'my_batch_sync' );
} );

// ❌ WARNING: Scheduling without checking if already scheduled.
wp_schedule_event( time(), 'hourly', 'my_task' ); // Creates duplicates!

// ✅ GOOD: Check before scheduling.
if ( ! wp_next_scheduled( 'my_task' ) ) {
    wp_schedule_event( time(), 'hourly', 'my_task' );
}
```

### Cache Bypass Issues
```php
// ❌ CRITICAL: Plugin starts PHP session on frontend (bypasses ALL page cache).
session_start(); // Check plugins for this - entire site becomes uncacheable!

// ❌ WARNING: Unique query params create cache misses.
// https://example.com/?utm_source=fb&utm_campaign=123&fbclid=abc
// Each unique URL = separate cache entry = cache miss.
// Solution: Strip marketing params at CDN/edge level.

// ❌ WARNING: Setting cookies on public pages.
setcookie( 'visitor_id', $id ); // Prevents caching for that user.
```

### Transients Misuse
```php
// ❌ WARNING: Dynamic transient keys create table bloat (without object cache).
set_transient( "user_{$user_id}_cart", $data, HOUR_IN_SECONDS );
// 10,000 users = 10,000 rows in wp_options!

// ✅ GOOD: Use object cache for user-specific data.
wp_cache_set( "cart_{$user_id}", $data, 'user_carts', HOUR_IN_SECONDS );

// ❌ WARNING: Transients for frequently-changing data defeats purpose.
set_transient( 'visitor_count', $count, 60 ); // Changes every minute.

// ✅ GOOD: Use object cache for volatile data.
wp_cache_set( 'visitor_count', $count, 'stats' );

// ❌ WARNING: Large data in transients on shared hosting.
set_transient( 'api_response', $megabytes_of_json, DAY_IN_SECONDS );
// Without object cache = serialized blob in wp_options.

// ✅ GOOD: Check hosting before using transients for large data.
if ( wp_using_ext_object_cache() ) {
    set_transient( 'api_response', $data, DAY_IN_SECONDS );
} else {
    // Store in files or skip caching on shared hosting.
}
```

### Asset Loading
```php
// ❌ WARNING: Assets load globally when only needed on specific pages.
add_action( 'wp_enqueue_scripts', function() {
    wp_enqueue_script( 'contact-form-js', ... );
    wp_enqueue_style( 'contact-form-css', ... );
} );

// ✅ GOOD: Conditional enqueue based on page/template.
add_action( 'wp_enqueue_scripts', function() {
    if ( is_page( 'contact' ) || is_page_template( 'contact-template.php' ) ) {
        wp_enqueue_script( 'contact-form-js', ... );
        wp_enqueue_style( 'contact-form-css', ... );
    }
} );

// ✅ GOOD: Only load WooCommerce assets on shop pages.
add_action( 'wp_enqueue_scripts', function() {
    if ( ! is_woocommerce() && ! is_cart() && ! is_checkout() ) {
        wp_dequeue_style( 'woocommerce-general' );
        wp_dequeue_script( 'wc-cart-fragments' );
    }
} );
```

### External API Requests
```php
// ❌ WARNING: No timeout set (default is 5 seconds).
wp_remote_get( $url ); // Set timeout: array( 'timeout' => 2 ).

// ❌ WARNING: Missing error handling for API failures.
$response = wp_remote_get( $url );
echo $response['body']; // Check is_wp_error() first!
```

### Sitemaps & Redirects
```php
// ❌ WARNING: Generating sitemaps for deep archives (crawlers hammer these).
// Solution: Exclude old post types, cache generated sitemaps.

// ❌ CRITICAL: Redirect loops consuming CPU.
// Debug with: x-redirect-by header, wp_debug_backtrace_summary().
```

### Post Meta Queries
```php
// ❌ WARNING: Searching meta_value without index.
'meta_query' => array(
    array(
        'key'   => 'color',
        'value' => 'red',
    ),
)
// Better: Use taxonomy or encode value in meta_key name.

// ❌ WARNING: Binary meta values requiring value scan.
'meta_key'   => 'featured',
'meta_value' => 'true',
// Better: Presence of 'is_featured' key = true, absence = false.
```

**For deeper context on any pattern:** Load `references/anti-patterns.md`

## Severity Definitions

| Severity | Description |
|----------|-------------|
| **Critical** | Will cause failures at scale (OOM, 500 errors, DB locks) |
| **Warning** | Degrades performance under load |
| **Info** | Optimization opportunity |

## Output Format

Structure findings as:

```markdown
## Performance Review: [filename/component]

### Critical Issues
- **Line X**: [Issue] - [Explanation] - [Fix]

### Warnings  
- **Line X**: [Issue] - [Explanation] - [Fix]

### Recommendations
- [Optimization opportunities]

### Summary
- Total issues: X Critical, Y Warnings, Z Info
- Estimated impact: [High/Medium/Low]
```

## Common Mistakes

When performing performance reviews, avoid these errors:

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Flagging `posts_per_page => -1` in admin-only code | Admin queries don't face public scale | Check context - admin, CLI, cron are lower risk |
| Missing the `session_start()` buried in a plugin | Cache bypass affects entire site | Always grep for `session_start` across all code |
| Ignoring `no_found_rows` for non-paginated queries | Small optimization but adds up | Flag as INFO, not WARNING |
| Recommending object cache on shared hosting | Many shared hosts lack persistent cache | Check hosting environment first |
| Only reviewing PHP, missing JS polling | JS `setInterval` + fetch = self-DDoS | Review `.js` files for polling patterns |

## Deep-Dive References

Load these references based on the task:

| Task | Reference to Load |
|------|-------------------|
| Reviewing PHP code for issues | `references/anti-patterns.md` |
| Optimizing WP_Query calls | `references/wp-query-guide.md` |
| Implementing caching | `references/caching-guide.md` |
| High-traffic event prep | `references/measurement-guide.md` |

**Note**: For standard code reviews, `anti-patterns.md` contains all patterns needed. Other references provide deeper context when specifically optimizing queries, implementing caching strategies, or preparing for traffic events.
