---
name: shopware-phpunit
description: Best practices for writing PHPUnit tests in Shopware 6 projects, including integration tests, unit tests, and common testing patterns for plugins and apps.
license: MIT
metadata:
  author: FriendsOfShopware
  version: "1.0.0"
  organization: FriendsOfShopware
  date: February 2026
  abstract: Comprehensive guide for writing effective PHPUnit tests in Shopware 6, covering integration test setup, repository testing, storefront and API testing, mocking services, and common pitfalls.
---

# Shopware PHPUnit Best Practices

## When to Apply

- Writing new PHPUnit tests for a Shopware 6 plugin or app
- Setting up test infrastructure for a Shopware project
- Testing repositories, services, commands, or event subscribers
- Writing integration tests that require the Shopware kernel
- Testing Storefront controllers or Store API / Admin API routes
- Debugging failing tests in a Shopware context

## Rule Categories by Priority

| Priority | Category | Prefix | Description |
|----------|----------|--------|-------------|
| CRITICAL | Test Setup | `setup-` | Kernel bootstrap, base test classes, PHPUnit configuration |
| HIGH | Integration Testing | `integration-` | Repository tests, service tests, database transactions |
| HIGH | API Testing | `api-` | Store API and Admin API endpoint testing |
| MEDIUM | Mocking | `mock-` | Service mocking, dependency injection in tests |
| MEDIUM | Data | `data-` | Test data creation, fixtures, cleanup |
| LOW | Performance | `perf-` | Test execution speed, parallel testing |

## How to Use

Read relevant reference files from the `references/` directory based on the task at hand. Files are prefixed by category for easy discovery.

## External References

- [Shopware Developer Documentation - Testing](https://developer.shopware.com/docs/guides/plugins/plugins/testing)
- [PHPUnit Documentation](https://docs.phpunit.de/)
