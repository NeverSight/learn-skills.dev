---
name: shopware-admin-crud-module
description: Creates a standalone CRUD administration module for a Shopware DAL entity with list page, detail/create page, ACL, filters, search, and snippets.
license: MIT
metadata:
  author: FriendsOfShopware
  version: "1.0.0"
  organization: FriendsOfShopware
  date: March 2026
  abstract: Step-by-step guide for scaffolding a complete Shopware Administration CRUD module including module registration, list and detail pages, ACL privileges, search configuration, filters, and i18n snippets.
---

# Shopware Administration CRUD Module

## When to Apply

- Creating a new admin module for a Shopware DAL entity
- Adding list, detail, and create pages for an entity in the administration
- Setting up ACL privileges for an admin module
- Adding search, filters, and inline editing for entity listings
- Scaffolding administration i18n snippets for a new module

## Rule Categories by Priority

| Priority | Category | Prefix | Description |
|----------|----------|--------|-------------|
| CRITICAL | Module Setup | `module-` | Module registration, file structure, naming conventions |
| CRITICAL | Pages | `page-` | List page and detail/create page patterns |
| HIGH | ACL & Search | `acl-` | ACL privilege mapping and search configuration |
| MEDIUM | Snippets & Filters | `snippet-` | i18n snippet structure and filter setup |

## How to Use

When the user invokes this skill, ask them for:
1. The **entity name** (DAL entity, e.g. `webhook`) -- if not provided as argument
2. Which **fields** to show in the list and detail (or read from the EntityDefinition PHP class automatically)
3. The **module prefix** to use (default: `frosh-tools-<entity>`)

Then read the relevant reference files from the `references/` directory and generate all files following the patterns described there. The admin source root is `src/Resources/app/administration/src/`.

### Naming Conventions

- Module name: `frosh-tools-<entity>` (hyphenated)
- Route prefix: `frosh.tools.<entity>` (dotted) -- derived from module name by replacing hyphens with dots
- ACL key: `frosh_tools_<entity>` (underscored)

### File Structure

```
module/<module-name>/
  index.js                          # Module registration + search type + lazy component loading
  default-search-configuration.js   # Search ranking config
  acl/
    index.js                        # ACL privilege mapping
  snippet/
    en-GB.json
    de-DE.json
  page/
    <module-name>-list/
      index.js
      template.html.twig
    <module-name>-detail/
      index.js
      template.html.twig
```

Also add `import './module/<module-name>';` to `main.js`.

## External References

- [Shopware Developer Documentation - Admin Module](https://developer.shopware.com/docs/guides/plugins/plugins/administration/add-custom-module)
