---
name: react-native-reusables
description: Agent skill for React Native Reusables — shadcn-style components for React Native (Expo) with Nativewind/Uniwind, RN Primitives, and CLI-driven scaffolding.
metadata:
  author: Hairy
  version: "2026.2.26"
  source: Generated from https://github.com/founded-labs/react-native-reusables, scripts located at https://github.com/hairyf/skills
---

> The skill is based on React Native Reusables (docs as of 2026-02-26), generated at 2026-02-26.

React Native Reusables brings the shadcn/ui experience to React Native: copy-paste or CLI-scaffolded components, theming via CSS variables, and RN Primitives under the hood. It supports Nativewind and Uniwind, requires a root `PortalHost` for overlays, and uses a `Text` inheritance system and an `Icon` wrapper for Lucide.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | What RNR is, differences from shadcn/ui (portals, no cascade, icons, etc.) | [core-overview](references/core-overview.md) |
| Installation | CLI init vs manual setup, adding components, PortalHost, dependencies | [core-installation](references/core-installation.md) |
| Customization | components.json, global.css, tailwind.config, theme.ts | [core-customization](references/core-customization.md) |

## Features

### Components and patterns

| Topic | Description | Reference |
|-------|-------------|-----------|
| Components overview | Button, Input, Dialog, variants, asChild, compound components | [features-components-overview](references/features-components-overview.md) |
| Text and icons | TextClassContext inheritance, Icon wrapper with Lucide | [features-text-and-icons](references/features-text-and-icons.md) |
| Forms & controls | Label, Input, Select, Checkbox, RadioGroup, compound pattern | [features-forms-controls](references/features-forms-controls.md) |
| Overlays & portals | PortalHost, Dialog/Popover/SelectContent, contentInsets | [features-overlays-portals](references/features-overlays-portals.md) |
| Registry and CLI | init, add, doctor; custom registry and registryDependencies | [features-registry-cli](references/features-registry-cli.md) |
| Blocks | Auth blocks, Clerk integration, adding blocks via CLI | [features-blocks](references/features-blocks.md) |

### Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Adding components | Prefer CLI, PortalHost placement, path aliases, cn helper, manual copy | [best-practices-adding-components](references/best-practices-adding-components.md) |
| Troubleshooting | doctor, --log-level all, PortalHost, aliases, dependencies | [best-practices-troubleshooting](references/best-practices-troubleshooting.md) |
