---
name: wp-rest-api-development
description: WordPress REST API review and development guidance. Use when reviewing custom REST routes, permission_callback logic, schema design, WP_REST_Request handling, response structure, versioning, controller classes, nonce or auth usage, or when user mentions "REST API review", "register_rest_route", "permission_callback", "WP_REST_Request", "REST endpoint", "custom API", "API schema", "REST controller", "headless WordPress", or "API auth". Detects route registration issues, authorization mistakes, schema drift, input validation gaps, and response design problems in WordPress REST API code.
---

# WordPress REST API Development Skill

## Overview

Systematic REST API review for WordPress plugins, themes, and custom code. **Core principle:** Every route needs a clear contract, explicit authorization, validated input, and predictable output. Review covers route registration, controller patterns, request parsing, schema and argument validation, response formatting, caching implications, and compatibility concerns. Report findings with line numbers, severity labels, and BAD/GOOD code pairs where helpful.

## When to Use

**Use when:**
- Reviewing `register_rest_route()` usage
- Auditing custom API endpoints or controller classes
- Checking `permission_callback` logic
- Validating `WP_REST_Request` input handling
- Reviewing response shape, status codes, and schema
- Designing versioned endpoints for headless or block-driven apps

**Don't use for:**
- General plugin architecture without REST focus (use wp-plugin-development)
- Security-only review across the whole plugin (use wp-security-review)
- Full WooCommerce endpoint review (use wp-woocommerce-dev when WC-specific)
- GraphQL-specific guidance

## Code Review Workflow

1. **Identify REST context**
   - Route callbacks in plugin bootstrap
   - Controller classes extending `WP_REST_Controller`
   - Headless frontend integration
   - Internal admin-only API usage

2. **Check route registration first**
   - Namespace and version format
   - HTTP methods match operation intent
   - `permission_callback` present and specific
   - `args` definitions for request validation

3. **Review request handling**
   - Use `$request->get_param()` or typed getters instead of raw globals
   - Validate and sanitize all user input
   - Reject malformed input with meaningful `WP_Error`

4. **Review response design**
   - Consistent response shape
   - Proper status codes
   - `rest_ensure_response()` where helpful
   - Avoid leaking internal details

5. **Check for CRITICAL/WARNING/INFO patterns**
   - **CRITICAL:** Missing `permission_callback`, write routes with `__return_true`, raw globals, unsanitized DB queries
   - **WARNING:** Inconsistent schema, weak validation, mixed response shapes, missing pagination info
   - **INFO:** Could use controller class, schema reuse, versioning cleanup

6. **Report with cross-references**
   - If auth or nonce issues dominate, suggest `/wp-sec-review`
   - If route logic is plugin-architecture-heavy, suggest `/wp-plugin-review`

## File-Type Specific Checks

### Route Registration (`register_rest_route`)

- CRITICAL: Missing `permission_callback`
- CRITICAL: `'permission_callback' => '__return_true'` on write endpoints
- WARNING: Namespace without version segment
- WARNING: Route registered outside `rest_api_init`
- INFO: Repeated inline callbacks that should use controller methods

### Permission Callbacks

- CRITICAL: Capability checks missing on private data
- WARNING: Callback always returns true for admin-like actions
- WARNING: No ownership check for user-specific resources
- INFO: Could centralize repeated permission logic

### Request Args and Validation

- CRITICAL: Raw `$_GET`/`$_POST` used inside endpoint callback
- WARNING: Missing `sanitize_callback` or `validate_callback`
- WARNING: Missing enum/format constraints for known values
- INFO: Could define reusable item schema

### Response Handling

- WARNING: Mixed success response shape across routes
- WARNING: `wp_send_json()` inside REST callbacks instead of returning response data
- INFO: Could use `WP_REST_Response` for headers/status control

## Search Patterns for Quick Detection (API-21)

Use these `rg` commands for quick REST API scanning. Organized by severity.

### CRITICAL Patterns

```bash
# register_rest_route candidates
rg -n "register_rest_route\s*\(" . -g '*.php'

# permission_callback returning true
rg -n "permission_callback.*__return_true" . -g '*.php'

# Raw superglobals inside REST callbacks
rg -n "\$_GET|\$_POST|\$_REQUEST" . -g '*.php'
```

### WARNING Patterns

```bash
# WP_REST_Request usage without obvious validation helpers
rg -n "WP_REST_Request|get_param\s*\(" . -g '*.php'

# REST callbacks using wp_send_json
rg -n "wp_send_json|wp_send_json_success|wp_send_json_error" . -g '*.php'

# Route namespaces to inspect for versioning
rg -n "register_rest_route\s*\(\s*['\"][^'\"]+" . -g '*.php'
```

### INFO Patterns

```bash
# WP_REST_Controller classes
rg -n "extends\s+WP_REST_Controller" . -g '*.php'

# rest_ensure_response usage
rg -n "rest_ensure_response|new\s+WP_REST_Response" . -g '*.php'
```

## Reference Files

- `references/route-patterns.md` - Route registration, controller structure, and namespace design
- `references/schema-and-auth-guide.md` - Args schema, permission callbacks, input validation, and response design

## Output Format (API-23)

For each finding include:

1. Severity: `CRITICAL`, `WARNING`, or `INFO`
2. File and line number
3. Issue summary
4. Why it matters for WordPress REST API behavior
5. Recommended fix

If no issues are found, say so clearly and mention any residual gaps such as missing tests, inconsistent schema documentation, or limited versioning strategy.

