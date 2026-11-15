---
name: wp-test-strategy
description: WordPress testing strategy and review guidance. Use when planning or reviewing PHPUnit coverage, integration tests, block tests, e2e tests, Playwright flows, WooCommerce test coverage, fixture design, or when user mentions "test strategy", "WordPress tests", "PHPUnit", "integration tests", "Playwright", "e2e", "test coverage", "testing plan", or "regression tests". Helps decide what to test, how deeply to test, and where to focus coverage in WordPress plugins, themes, blocks, and WooCommerce extensions.
---

# WordPress Test Strategy Skill

## Overview

Systematic testing strategy guidance for WordPress projects. **Core principle:** Test depth should match risk, and the test pyramid should reflect the WordPress surface area involved. Review covers unit tests, WordPress integration tests, REST endpoint tests, block tests, browser or E2E flows, WooCommerce regressions, fixtures, and release-risk prioritization.

## When to Use

**Use when:**
- Deciding what tests to add for a feature or fix
- Reviewing missing coverage in a plugin or theme
- Planning regression tests before release
- Choosing between unit, integration, and E2E coverage
- Mapping block, REST, admin, or WooCommerce behavior to tests

**Don't use for:**
- Code review that does not involve testing decisions
- CI system debugging only
- Performance benchmarking alone

## Code Review Workflow

1. **Identify the change surface**
   - Pure PHP logic
   - WordPress integration behavior
   - REST or AJAX flow
   - Block editor behavior
   - Admin screen workflow
   - WooCommerce order/cart/checkout behavior

2. **Map the risk**
   - User-facing breakage
   - Data corruption or migration risk
   - Auth/security-sensitive flow
   - Browser interaction complexity

3. **Choose test depth**
   - Unit tests for isolated logic
   - Integration tests for WordPress APIs and DB state
   - E2E tests for UI workflows or editor interactions

4. **Report recommendations**
   - What should be tested
   - What level of test is appropriate
   - What can be skipped or covered indirectly

## Test Selection Heuristics

### Unit Tests

Use for:
- Pure transformation logic
- Small helpers
- Formatting and parsing logic
- Validation rules decoupled from WP runtime

### Integration Tests

Use for:
- Hooks and filters
- Option/meta persistence
- REST endpoints
- Custom queries
- Role/capability behavior

### E2E or Browser Tests

Use for:
- Block editor flows
- Admin forms with JS behavior
- Checkout, cart, and frontend interactions
- Accessibility-sensitive interaction flows

## Search Patterns for Quick Detection (TST-21)

Use these `rg` commands to understand current test coverage and likely gaps.

### Coverage Discovery

```bash
# Test directories and files
rg -n "class .*Test|extends .*TestCase|describe\\(|test\\(" . -g '*.{php,js,jsx,ts,tsx}'

# PHPUnit config or bootstrap
rg -n "phpunit|tests/bootstrap|WP_UnitTestCase" .

# Playwright or E2E indicators
rg -n "playwright|@wordpress/e2e-test-utils|page\.goto|test\\(" . -g '*.{js,ts}'
```

### Gap Signals

```bash
# High-risk surfaces with no obvious tests nearby
rg -n "register_rest_route|add_action|add_filter|wp_ajax_|admin_post_|dbDelta|WC_" . -g '*.php'

# Block editor files
rg -n "block.json|edit\\(|save\\(|registerBlockType" . -g '*.{json,js,jsx}'
```

## Reference Files

- `references/test-layer-guide.md` - Choosing unit vs integration vs E2E coverage in WordPress projects
- `references/wordpress-test-scenarios.md` - Recommended test scenarios for plugins, blocks, themes, REST APIs, and WooCommerce

## Output Format (TST-23)

When reporting, organize by:

1. Surface area under review
2. Recommended test types
3. Highest-priority missing coverage
4. Nice-to-have coverage

If the existing tests are already sufficient, say that clearly and mention any residual risk or missing edge-case coverage.

