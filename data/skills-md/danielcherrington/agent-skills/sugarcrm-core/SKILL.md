---
name: sugarcrm-core
description: SugarCRM 25 (Sugar 25.x) development best practices. Use when customizing or building on Sugar (Sugar Sell, Sugar Serve, Sugar Enterprise)—PHP backend, Sidecar frontend, REST API, logic hooks, Module Loadable Packages (MLP), and upgrade-safe patterns. Follows official Developer Guide and Developer Policy.
license: MIT
metadata:
  author: danielcherrington
  version: "1.0.0"
  target: Sugar 25.x
---

# SugarCRM 25 Development Best Practices

Procedural knowledge for developing and customizing SugarCRM version 25 (Sugar 25.x). Use this skill when writing or reviewing Sugar customizations, new modules, logic hooks, Sidecar UI, REST integrations, or MLPs.

## When to Apply

- Customizing Sugar (new fields, modules, layouts, or business logic)
- Writing PHP logic hooks, API integrations, or backend code
- Building or extending Sidecar (Backbone.js) views and components
- Designing or packaging Module Loadable Packages (MLPs) or Marketplace add-ons
- Reviewing code for upgrade safety, security, or policy compliance
- Integrating with Sugar via REST API or headless access

## Quick Principles

1. **Prefer configuration and extension over core edits** — Use Studio, logic hooks, and MLPs; never persist changes in core `modules/`, `include/`, or core Sidecar assets.
2. **Target Sidecar for UI** — Sugar 25 uses the Sidecar (Backbone.js) client; build new UI there and use versioned [Sidecar API](https://apidocs.sugarcrm.com/Sidecar/25.2.0/) and [DB Schema](https://apidocs.sugarcrm.com/schema/25.2.0/ent/) for your 25.x release.
3. **Package with MLP for distribution** — Use Module Loadable Packages for installable, upgrade-safe customizations; follow [Marketplace Package Guidelines](https://support.sugarcrm.com/smartlinks/developer_guide/architecture/module_loader/sugar_exchange_package_guidelines/) if publishing.
4. **Stay on supported platforms** — Use [Supported Platforms](https://support.sugarcrm.com/Resources/supported_platforms) for your 25.x release (PHP, DB, OS).
5. **Follow Developer Policy** — No forking, no prohibited licenses (e.g. GPL/AGPL), no stripping Critical Control Software or Sugar notices; respect [Developer Policy](https://support.sugarcrm.com/Resources/Developer_Policy/) and [SugarCloud Policy](https://support.sugarcrm.com/Resources/sugar_cloud_policy_guide/) when applicable.

## Reference Sections

For detailed rules and examples, read as needed:

| Topic | File | Use when |
|-------|------|----------|
| Architecture & platform | [references/architecture.md](references/architecture.md) | Choosing stack, Sidecar, MLP, supported platforms |
| Customization | [references/customization.md](references/customization.md) | Studio, logic hooks, REST API, Sidecar UI, upgrade safety |
| Code standards | [references/code-standards.md](references/code-standards.md) | PHP/JS conventions, security, upgrade-safe patterns |
| Developer policy | [references/developer-policy.md](references/developer-policy.md) | Policy, IP, SugarCloud, Marketplace/MLP requirements |

## Official Links

- [Sugar Developer Guide 25.1](https://support.sugarcrm.com/documentation/sugar_developer/sugar_developer_guide_25.1/)
- [API Docs (Sidecar, Schema, REST)](https://apidocs.sugarcrm.com/)
- [Developer Policy](https://support.sugarcrm.com/Resources/Developer_Policy/)
- [Supported Platforms](https://support.sugarcrm.com/Resources/supported_platforms)
- [Marketplace Package Guidelines](https://support.sugarcrm.com/smartlinks/developer_guide/architecture/module_loader/sugar_exchange_package_guidelines/)
