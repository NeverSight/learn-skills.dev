---
name: ti-guides
description: "Titanium SDK official fundamentals and configuration guide. Use when working with, reviewing, analyzing, or examining Titanium projects, Hyperloop native access, app distribution (App Store/Google Play), tiapp.xml configuration, CLI commands, memory management, bridge optimization, CommonJS modules, SQLite transactions, or coding standards. Applies to both Alloy and Classic projects."
argument-hint: "[topic]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(node *)
---

# Titanium SDK guide expert

Use this skill to keep Titanium projects aligned with TiDev standards for stability, performance, and cross-platform behavior.

## Project detection

:::info Auto-detects Titanium projects
This skill auto-detects Titanium projects. No manual command is needed.

Titanium project indicator:
- `tiapp.xml` file (definitive indicator)

Applies to both:
- Alloy projects (`app/` folder)
- Classic projects (`Resources/` folder)

Behavior:
- If a Titanium project is detected, provide official Titanium SDK guidance, memory management best practices, and app distribution help.
- If not detected, say this skill is only for Titanium projects.
:::

## Core workflow

1. Validate the project follows a modular pattern (CommonJS or Alloy).
2. Ensure global listeners are removed and heavy objects are nulled during cleanup.
3. Cache frequently accessed native properties to reduce bridge crossings.
4. Use Hyperloop for specialized native functionality and handle casting and threading correctly.
5. Use transactions for database work and manage image memory footprints.

## Procedural rules

- Always remove `Ti.App` and `Ti.Geolocation` listeners during controller cleanup.
- Do not access `Ti.Platform` or `Ti.DisplayCaps` inside loops. Store values in local variables.
- Concatenate Hyperloop selectors accurately (for example, `addAttribute:value:range:` -> `addAttributeValueRange`).
- Close resultsets and database handles after every transaction block.

## Reference guides

- Hello World (references/hello-world.md): project creation, structure, and getting started with Alloy or Classic Titanium.
- JavaScript Primer (references/javascript-primer.md): JavaScript fundamentals, learning resources, best practices, and ES6+ features.
- Application Frameworks (references/application-frameworks.md): Alloy vs Classic Titanium, architectural patterns, and framework selection.
- Coding Best Practices (references/coding-best-practices.md): memory leaks, bridge efficiency, event naming, security, and lazy loading.
- CommonJS Advanced (references/commonjs-advanced.md): stateful modules, caching, ES6+ support, and antipatterns.
- Advanced Data & Images (references/advanced-data-and-images.md): SQLite transactions and image memory optimization.
- Hyperloop Native Access (references/hyperloop-native-access.md): Objective-C/Swift/Java syntax, casting, debugging, XIB/Storyboards.
- Style & Conventions (references/style-and-conventions.md): naming standards and formatting rules.
- Reserved Words (references/reserved-words.md): ECMAScript, iOS, and Alloy reserved keywords to avoid.
- Android Manifest (references/android-manifest.md): custom AndroidManifest.xml, permissions, and manifest merge.
- App Distribution (references/app-distribution.md): Google Play (APK/AAB), App Store (IPA), certificates, provisioning, and deployment.
- tiapp.xml Configuration (references/tiapp-config.md): complete reference for tiapp.xml and timodule.xml, including all elements, properties, and platform-specific settings.
- CLI Reference (references/cli-reference.md): Titanium CLI commands, options, tasks, configuration, and build processes.
- Resources (references/resources.md): community support, modules, sample code, Slack, and learning materials.

## Related skills

For tasks beyond SDK fundamentals, use these complementary skills:

| Task | Use this skill |
| --- | --- |
| Project architecture, services, patterns | `ti-expert` |
| Native features (location, push, media) | `ti-howtos` |
| Alloy CLI, configuration, debugging | `alloy-howtos` |
| UI layouts, ListViews, gestures | `ti-ui` |

## Response format

1. Technical recommendation: cite the specific TiDev best practice.
2. Optimized implementation: provide modern ES6+ code without semicolons.
3. Rationale: briefly explain the performance or memory impact.
