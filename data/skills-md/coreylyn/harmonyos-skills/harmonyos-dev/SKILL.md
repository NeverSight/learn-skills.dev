---
name: harmonyos-dev
description: >-
  HarmonyOS application development assistant based on ArkTS and ArkUI
  frameworks. Confirm API version (default API 20+) and target device type
  (default PC) before starting. Supports UI component development, data
  management, network communication, and system capability integration.
  Applicable for greenfield development, iterating existing projects, and
  architecture design. References official Huawei documentation including
  release notes, development guides, API references, best practices, and FAQ.
---

# HarmonyOS Application Development

## Pre-Development Checklist

Confirm before starting a new project or first-time development:

- **API version**: Default API 20+; state explicitly if backward compatibility needed
- **Target device**: PC / Phone / Tablet / Wearable / Multi-device
- **Scenario**: Greenfield / Iteration / Architecture design
- **Project structure**: HAP package layout, module organization

## Core Technology Stack

### ArkTS Language

- TypeScript-based extension
- State decorators: `@ObservedV2`, `@Trace`, `@Local`, `@Provider`
- Component decorators: `@Component`, `@ComponentV2`, `@Entry`, `@Builder`
- Rendering: on-demand updates, minimal re-renders

### ArkUI Component System

- Declarative UI construction
- Layout containers: Column / Row / Stack / Flex / Grid
- List rendering: ForEach / LazyForEach
- Animation: property animation, transition, shared element transition

## Common Patterns

### State Management

- Component-local: `@Local`
- Cross-component: `@Provider` + `@Consumer`
- Deep reactivity: `@ObservedV2` + `@Trace`

### Page Navigation

- `Router.pushUrl()` - push page
- `Router.replaceUrl()` - replace page
- `Router.back()` - go back

### Data Persistence

- Preferences: lightweight key-value storage
- RDB: relational database
- Distributed data: cross-device sync

### Network

- `@kit.NetworkKit` http - HTTP requests
- WebSocket - persistent connections
- Upload/Download: `@kit.BasicServicesKit` request

## Official Documentation

- **Release notes**: https://developer.huawei.com/consumer/cn/doc/harmonyos-releases/overview-allversion
- **Dev guide**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-dev-guide
- **API reference**: https://developer.huawei.com/consumer/cn/doc/harmonyos-references/development-intro-api
- **Best practices**: https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-best-practices-overview
- **FAQ**: https://developer.huawei.com/consumer/cn/doc/harmonyos-faqs/faqs-multi-device-scenario

## References

Load detailed docs as needed:

- **State management**: [references/state-management.md](references/state-management.md)
- **UI components**: [references/ui-components.md](references/ui-components.md)
- **Data persistence**: [references/data-persistence.md](references/data-persistence.md)
- **Network**: [references/network.md](references/network.md)
- **Permissions**: [references/permissions.md](references/permissions.md)
- **Performance**: [references/performance.md](references/performance.md)
