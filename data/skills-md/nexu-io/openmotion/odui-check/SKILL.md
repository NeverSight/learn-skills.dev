---
name: odui-check
description: Audit Open Design UI usage and component contributions before review. Use when checking design tokens, component boundaries, native controls, registry adoption, theme parity or a component PR.
---

# Check Open Design UI compliance

This Skill is read-only unless a failing check is being fixed. Read [AGENTS.md](../../../AGENTS.md), the [component guide](../../../packages/open-design-ui/README.md), `registry.json` and the affected source files.

1. Run `npm run design:check`. It checks token freshness, theme parity, contrast, import boundaries, native-control baselines and registry adoption.
2. For component changes also run `npm run components:build`, `npm run typecheck:studio` and the focused tests. Use `npm run check` for the repository gate when the change touches shared rules or configuration.
3. Inspect the real catalogue route in both themes. Check focus, disabled/loading, keyboard behavior, accessible names, narrow widths and console errors. A green static check does not replace browser inspection.
4. Confirm every registry item has a source, alias, example, API notes, real Studio consumer and an adoption decision. An opt-in item needs a review condition. An enforced item needs a matching native rule.
5. Report each finding with the file, the violated rule, the smallest repair and the exact check that remains.

Do not lower a baseline to hide an un-migrated control. Do not mark a component enforced before a real consumer has been verified.
