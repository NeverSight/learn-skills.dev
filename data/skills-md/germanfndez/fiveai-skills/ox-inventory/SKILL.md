---
name: ox-inventory
description: "Trigger: ox_inventory, items, stash, AddItem, RemoveItem, metadata, item registration, inventory hooks, shops. Server and client exports for ox_inventory."
license: MIT
metadata:
  author: germanfndez
  version: "1.0.0"
---

# ox_inventory

Slot-based inventory with weight, metadata, stashes, shops and hooks. Supports ox_core, esx and qbx_core.

## Activation Contract

Load this skill when the user asks to give, take, count or check items, register a stash or shop, define a new item, react to inventory actions, or migrate from qb-inventory or esx inventory.

## Hard Rules

- Call everything through `exports.ox_inventory:<fn>(...)`. There is no global table.
- Grant, remove and count items on the SERVER only. Client exports are for display and UI decisions.
- `AddItem` can fail. Always check the return value: the player may be over weight or out of slots.
- Check `CanCarryItem` BEFORE taking payment or removing the traded item, never after.
- Never invent item names. An item must exist in `data/items.lua` or it silently fails.
- `inv` is a player source, an identifier, or a stash id. Passing the wrong one returns nil, not an error.
- Metadata makes items non-stackable when it differs. Do not put volatile data in metadata.

## Decision Gates

| Goal | Call |
|---|---|
| Give an item | `AddItem(inv, item, count, metadata, slot)` |
| Take an item | `RemoveItem(inv, item, count, metadata, slot)` |
| Check space first | `CanCarryItem(inv, item, count, metadata)` |
| How many does the player have | `GetItemCount(inv, item, metadata, strict)` |
| Read one slot | `GetSlot(inv, slot)` |
| Find items across slots | `Search(inv, 'slots'\|'count', item, metadata)` |
| Persistent storage | `RegisterStash(...)` |
| Short-lived storage | `CreateTemporaryStash(properties)` |
| React to a player action | `registerHook(event, cb, options)` |

## Execution Steps

1. Confirm `ox_inventory` starts after `ox_lib` and the framework core.
2. Decide the side: mutation is server, display is client.
3. For a trade or reward, order the calls: `CanCarryItem` -> take payment -> `AddItem` -> verify the return.
4. Define any new item in `data/items.lua` before referencing it. Read rules/items.md.
5. Use hooks instead of polling when reacting to moves, opens or purchases.

## Output Contract

Return runnable Lua using `exports.ox_inventory`, with the server/client split explicit. Include the `data/items.lua` entry whenever a new item is introduced.

## References

- rules/server-exports.md — item and inventory functions on the server.
- rules/client-exports.md — weight, current weapon, opening inventories.
- rules/items.md — defining items in data/items.lua.
- rules/stashes.md — stashes, shops and temporary storage.
- rules/hooks.md — registerHook and cancelling actions.

Upstream docs: https://overextended.dev/ox_inventory
