---
name: pipa-manage
description: "Use when the user wants to manage Pipa configuration across profile setup, connectors, company brain or memory, permissions, automations, triggers, loops, or access audits. Route profile setup to pipa-setup and connector setup/status to pipa-connectors. Do not use for business work or an already-connected app action."
metadata:
  version: 0.3.0
---

# Pipa Manage

Route Pipa configuration and maintenance to one focused operation.

## Use For

- Business profile, company brain, memory, permissions, and access review.
- Automations, triggers, loops, scheduled workflows, and recurring work setup.

## Selection

- First-time setup, incomplete setup, or global profile review/update -> `pipa-setup`.
- Connected-tool setup, connector status/troubleshooting, or global connector-map maintenance -> `pipa-connectors`.
- Company brain, memory, permissions, access audits, automations, triggers, loops, and recurring work remain in `pipa-manage` unless a specialized capability applies.
- For recurring rituals, report that self-installed Pipa has no scheduler and do not imply that a schedule was created. Offer manual ritual use or hosted Pipa, then route to hosted setup only after the user chooses it.
- If the selected operation is unavailable, name that missing skill and stop. Do not imply a fallback or run an inline copy.

## Output Contract

- Configuration objective.
- Current setup state or `TBD`.
- Needed inputs, access, or decisions.
- Safety/permission check.
- Next setup action.

## Boundaries

- If the user is doing business work now, route to the relevant business lane.
- If the user wants a standalone utility output, route to `pipa-tools`.
- Do not create automations, connect tools, or write memory without explicit confirmation when the action changes external state.

## Gotchas

- Profile setup and connector status are owned by their operation skills; do not reproduce their workflows here.
- Company brain writes need user intent and a clear destination.
