---
name: radix-to-baseui-migration
description: Migrate shadcn components and custom Radix UI primitives to Base UI with a manual, low-risk workflow. Use when users ask to move from Radix UI to Base UI, replace asChild patterns, fix migration TypeScript errors, update renamed props/types, or adapt dropdown/popover/dialog positioning to Base UI positioner patterns.
---

# Radix to Base UI Migration (shadcn)

Execute migration in four passes. Keep each pass small and compilable.

## 1) Remove Radix package surface and switch imports

1. Remove Radix primitive packages from dependencies.
2. Add Base UI package(s) used by the project.
3. Replace Radix imports with Base UI imports component-by-component.
4. Keep component names stable during this pass (use aliases if needed) to reduce diff size.

Use `references/checklist.md` for pass order and validation gates.

## 2) Replace `asChild` composition with Base UI render composition

1. Find trigger/content compositions that relied on `asChild`.
2. Replace `asChild` usage with Base UI render-based composition.
3. Preserve semantic HTML and avoid nested interactive elements.
4. Re-test keyboard and focus behavior for each migrated trigger.

Use `references/migration-map.md` for common `asChild` migration patterns.

## 3) Resolve type and API differences

1. Run type-check and build after each component family migration.
2. Replace Radix-flavored prop/type names with Base UI equivalents.
3. Treat TypeScript errors as the migration to-do list; fix from highest fan-out components first.
4. Check renamed slots/backdrop/overlay/content primitives and event prop naming differences.

Use `references/migration-map.md` to map common rename classes.

## 4) Migrate positioning to Positioner-based layout

1. For floating UI (dropdown, popover, tooltip, dialog-like overlays), introduce the Base UI Positioner pattern where required.
2. Move placement-related props from old content nodes to the new positioning layer.
3. Re-verify placement, collision handling, alignment, and animation origin.

Use `references/migration-map.md` for positioning conversion guidance.

## Migration operating rules

1. Migrate one primitive family at a time (dropdown, popover, dialog, tooltip, select).
2. Keep visual styles unchanged during API migration; separate style refactors to a later PR.
3. Prefer docs and shadcn Base UI examples when uncertain; do not guess prop parity.
4. Keep builds green between families to avoid compounded regressions.

## Completion criteria

1. No Radix primitive imports remain in source.
2. No migration-related TypeScript errors remain.
3. All floating components use valid Base UI positioning composition.
4. Keyboard/focus interactions pass for migrated components.
5. Existing UI snapshots or smoke tests pass.
