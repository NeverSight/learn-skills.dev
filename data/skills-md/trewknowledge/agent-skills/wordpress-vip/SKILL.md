---
name: wordpress-vip
description: Develop and deploy code for WordPress VIP environments following platform requirements, coding standards, and best practices. Use when working with WordPress VIP projects, VIP-CLI, VIP-hosted sites, or when the user mentions WordPress VIP, WPVIP, VIP Go, or enterprise WordPress.
---

# WordPress VIP Development

You are a **WordPress VIP** developer working on enterprise WordPress applications. You follow strict platform requirements for coding standards, deployment, performance, security, and architecture.

## Quick Reference

**WordPress VIP** is an enterprise hosting platform with specific requirements you must follow:

- **Prohibited**: file system writes, uncached external requests, certain plugins/functions
- **Required**: code review, automated scanning, performance optimization
- **Deployment**: via **GitHub** integration or **VIP-CLI**
- **Local Dev**: VIP Local Dev Environment or Docker
- **Search**: Enterprise Search powered by **Elasticsearch** via **ElasticPress**

## Coding Standards

### File System Restrictions

You work with a read-only file system in production. The platform blocks direct file writes to ensure security and scalability.

**Prohibited operations:**
- Direct file writes (`file_put_contents()`, `fwrite()`)
- Image uploads to local filesystem
- Cache writes to files
- Log writes to files

**You must use these VIP-approved alternatives:**
- `wpcom_vip_download_image()` for remote images
- VIP's **object storage** for uploads
- **Persistent object cache** (**Memcached**) for caching
- `error_log()` for logging (auto-streamed to logs)

### Restricted Functions

You must avoid functions that are blocked or discouraged by the platform:

```php
// Prohibited - direct database queries
$wpdb->query("DELETE FROM...");

// Use instead - WordPress functions
wp_delete_post($post_id);

// Prohibited - uncached remote requests
file_get_contents('https://api.example.com');
wp_remote_get('https://api.example.com'); // without caching

// Use instead - cached requests
$response = wp_cache_get($cache_key);
if (false === $response) {
    $response = vip_safe_wp_remote_get('https://api.example.com');
    wp_cache_set($cache_key, $response, 'api', HOUR_IN_SECONDS);
}
```

### Required Prefixes

You must prefix all custom functions, classes, and constants to avoid conflicts:

```php
// Good - prefixed
function clientname_custom_function() {}
class ClientName_Custom_Class {}
define('CLIENTNAME_CONSTANT', 'value');

// Bad - no prefix (can conflict with plugins)
function custom_function() {}
class Custom_Class {}
```

### Database Queries

You must follow **WordPress VIP** query patterns for security and performance:

```php
// Bad - direct query without prepare
$results = $wpdb->get_results("SELECT * FROM $wpdb->posts WHERE post_status = 'publish'");

// Good - use WP_Query
$query = new WP_Query([
    'post_status' => 'publish',
    'posts_per_page' => 100,
]);

// If direct query needed - use prepare
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM $wpdb->posts WHERE post_status = %s",
        'publish'
    )
);
```

## Plugin Management

### Prohibited Plugins

You cannot use caching plugins (**VIP** provides caching), security plugins that modify `.htaccess`, backup plugins (**VIP** handles backups), or plugins that write to filesystem.

Before using any plugin, you must verify it meets these criteria: no file system writes, no uncached external requests, no restricted functions, performance tested, and security reviewed.

## Performance Requirements

### Query Optimization

**Batch Processing:**
```php
// Bad - queries in loop
foreach ($post_ids as $post_id) {
    $post = get_post($post_id); // N queries
}

// Good - batch query
$posts = get_posts([
    'post__in' => $post_ids,
    'posts_per_page' => -1,
]);
```

**Object Caching:**
```php
function clientname_get_expensive_data($id) {
    $cache_key = 'expensive_data_' . $id;
    $data = wp_cache_get($cache_key, 'clientname');
    
    if (false === $data) {
        // Expensive operation
        $data = perform_expensive_operation($id);
        wp_cache_set($cache_key, $data, 'clientname', HOUR_IN_SECONDS);
    }
    
    return $data;
}
```

### Page Cache Compatibility

You must ensure your code works with full-page caching:

```php
// Bad - will show same content to all users
echo 'Welcome, ' . wp_get_current_user()->display_name;

// Good - JavaScript for user-specific content
echo '<span class="user-name" data-user-id="' . get_current_user_id() . '"></span>';
// Populate via AJAX or REST API
```

### External Requests

You must always cache external API calls to prevent performance issues:

```php
function clientname_fetch_api_data($endpoint) {
    $cache_key = md5('api_' . $endpoint);
    $data = wp_cache_get($cache_key, 'api');
    
    if (false === $data) {
        $response = vip_safe_wp_remote_get(
            $endpoint,
            '',
            3,
            3,
            20
        );
        
        if (is_wp_error($response)) {
            return false;
        }
        
        $data = json_decode(wp_remote_retrieve_body($response), true);
        wp_cache_set($cache_key, $data, 'api', 15 * MINUTE_IN_SECONDS);
    }
    
    return $data;
}
```

## Security Requirements

### Input Validation

You must always validate and sanitize user input:

```php
// User input
$user_input = sanitize_text_field($_POST['field_name']);
$email = sanitize_email($_POST['email']);
$url = esc_url_raw($_POST['url']);

// Output escaping
echo esc_html($user_input);
echo esc_url($url);
echo esc_attr($attribute);
```

### Nonce Verification

You must protect forms and AJAX requests with nonces:

```php
// Form with nonce
wp_nonce_field('clientname_action', 'clientname_nonce');

// Verify nonce
if (!isset($_POST['clientname_nonce']) || 
    !wp_verify_nonce($_POST['clientname_nonce'], 'clientname_action')) {
    wp_die('Security check failed');
}
```

### SQL Injection Prevention

You must always use `$wpdb->prepare()` for database queries:

```php
// Correct
$results = $wpdb->get_results($wpdb->prepare(
    "SELECT * FROM $wpdb->posts WHERE post_title LIKE %s",
    '%' . $wpdb->esc_like($search) . '%'
));
```

## Local Development

You should use the **VIP Local Dev Environment** for local development.

**Setup VIP Local Dev Environment:**
```bash
npm install -g @automattic/vip
vip dev-env create --slug=mysite
vip dev-env start
```

**Sync from production:**
```bash
vip @mysite.production media pull
vip @mysite.production db pull
```

See [VIP Local Development documentation](https://docs.wpvip.com/local-development/) for complete setup instructions.

## Deployment Workflow

### Using GitHub Integration

You deploy code automatically using **GitHub** branches. **VIP** monitors your repository and deploys changes automatically.

1. **Development**: Push to `develop` branch → deploys to `develop` environment
2. **Staging**: Push to `master`/`main` branch → deploys to staging
3. **Production**: Manually promote via **VIP Dashboard**

**Commit and push your changes:**
```bash
git add .
git commit -m "feat: add custom post type"
git push origin develop
```

You can monitor deployment progress in the **VIP Dashboard**.

### Using VIP-CLI

You can also deploy using **VIP-CLI**:
```bash
# Deploy to environment
vip @mysite.develop deploy

# Check deployment status
vip @mysite.develop deploy list
```

**Run WP-CLI commands:**
```bash
# Clear cache
vip @mysite.production wp cache flush

# Run custom command
vip @mysite.production wp post list --post_type=page
```

### Pre-Deployment Checklist

You must verify these items before deploying:

- [ ] Code passes **PHPCS** with WordPress VIP ruleset
- [ ] No restricted functions used
- [ ] All external requests are cached
- [ ] Database queries are optimized
- [ ] User inputs are sanitized
- [ ] Outputs are escaped
- [ ] No file system writes
- [ ] Tested in local **VIP** environment
- [ ] No `var_dump()` or debugging code
- [ ] Error logging uses `error_log()` only

## Code Review Process

You must pass automated code review before deploying to production.

**VIP** runs automated scans (`vip-go-ci`) on every commit. These scans check for restricted functions, direct database queries, uncached external requests, and security issues.

You should submit pull requests with clear descriptions, address automated findings, and wait for approval before merging.

## Code Scanning

You should run **PHPCS** with **WordPress VIP Coding Standards** locally before committing:

```bash
composer require --dev automattic/vipwpcs
phpcs --standard=WordPress-VIP-Go .
```

## Common Patterns

### Custom Post Types

```php
function clientname_register_cpt() {
    register_post_type('clientname_resource', [
        'labels' => [
            'name' => 'Resources',
            'singular_name' => 'Resource',
        ],
        'public' => true,
        'has_archive' => true,
        'supports' => ['title', 'editor', 'thumbnail'],
        'show_in_rest' => true,
    ]);
}
add_action('init', 'clientname_register_cpt');
```

### REST API Endpoints

```php
function clientname_register_api_routes() {
    register_rest_route('clientname/v1', '/data/(?P<id>\d+)', [
        'methods' => 'GET',
        'callback' => 'clientname_get_data',
        'permission_callback' => '__return_true',
        'args' => [
            'id' => [
                'validate_callback' => function($param) {
                    return is_numeric($param);
                }
            ],
        ],
    ]);
}
add_action('rest_api_init', 'clientname_register_api_routes');

function clientname_get_data($request) {
    $id = $request['id'];
    // Return data
    return rest_ensure_response(['data' => $data]);
}
```

### Cron Jobs

```php
// Register cron event
function clientname_schedule_cron() {
    if (!wp_next_scheduled('clientname_daily_task')) {
        wp_schedule_event(time(), 'daily', 'clientname_daily_task');
    }
}
add_action('wp', 'clientname_schedule_cron');

// Cron callback
function clientname_run_daily_task() {
    // Task logic
}
add_action('clientname_daily_task', 'clientname_run_daily_task');
```

## Enterprise Search

You have access to **Enterprise Search** powered by **Elasticsearch** via the **ElasticPress** plugin.

**Enterprise Search** provides fast, scalable search with features like weighted search, faceted filtering, fuzzy matching, related posts, and autosuggest. Once you enable it in the **VIP Dashboard**, **ElasticPress** automatically handles WordPress search queries.

For complete documentation on indexing, configuration, advanced features, and performance optimization, see [references/ENTERPRISE_SEARCH.md](references/ENTERPRISE_SEARCH.md)

## Troubleshooting

### Common Issues

**White screen/500 error:**
You should check PHP error logs first: `vip @mysite.env logs php`. Verify no fatal errors in recent code and check for memory limit issues.

**Performance degradation:**
You should review **New Relic** in the **VIP Dashboard**. Check for N+1 queries, verify **object caching** is working, and look for uncached external requests.

**Cache not clearing:**
You can manually clear caches using these commands:

```bash
# Clear all caches
vip @mysite.production wp cache flush

# Purge page cache for specific URL
vip @mysite.production wp vip-go purge-url "https://example.com/page"
```

**Plugin conflicts:**
You should deactivate recent plugins, test in your local environment, and verify plugin compatibility with **VIP** requirements.

## Additional Resources

You can find more detailed information in these reference documents:

- Complete **WordPress VIP** function reference: [references/VIP_FUNCTIONS.md](references/VIP_FUNCTIONS.md)
- Deployment examples and workflows: [references/DEPLOYMENT_EXAMPLES.md](references/DEPLOYMENT_EXAMPLES.md)
- Performance optimization patterns: [references/PERFORMANCE.md](references/PERFORMANCE.md)
- **Enterprise Search** details and advanced patterns: [references/ENTERPRISE_SEARCH.md](references/ENTERPRISE_SEARCH.md)

## Key Reminders

You must follow these critical requirements:

1. **No file system writes** - use **object cache** or **VIP's** storage
2. **Cache external requests** - always use transients or **object cache**
3. **Prefix everything** - functions, classes, constants
4. **Prepare queries** - always use `$wpdb->prepare()`
5. **Test locally** - use **VIP Local Dev Environment**
6. **Monitor scans** - address automated findings before review
7. **Follow standards** - **WordPress VIP Coding Standards** (**PHPCS**)
