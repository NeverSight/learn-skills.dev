---
name: esx-framework
description: ESX Legacy Framework for FiveM - Player management, jobs, economy, inventory, weapons. Use when creating ESX resources or working with xPlayer, PlayerData, ESX functions.
author: germanfndez
version: 1.0.0
mcp-server: projecthub
---

# ESX Framework Development

Complete guide for developing with ESX Legacy Framework — the most trusted FiveM roleplay framework since 2017.

## When to use

- Creating or editing ESX resources/scripts
- Working with player data (xPlayer, PlayerData)
- Implementing jobs, economy, inventory, or weapon systems
- Using ESX client/server functions, callbacks, or events
- Questions about ESX best practices and optimization

## How to use

Read individual rule files for detailed explanations and examples:

- **rules/core-concepts.md** — ESX architecture, PlayerData, xPlayer object, framework initialization
- **rules/client-functions.md** — Client-side ESX functions, UI systems, player state management
- **rules/server-functions.md** — Server-side functions, player retrieval, callbacks, triggers
- **rules/xplayer-methods.md** — xPlayer object methods: money, items, weapons, inventory, jobs, metadata
- **rules/jobs-economy.md** — Job system, salaries, accounts (money/bank), society management
- **rules/inventory-items.md** — Inventory system, item management, usable items, weight calculations
- **rules/weapons-loadout.md** — Weapon system, loadout, components, ammo, tints
- **rules/events-callbacks.md** — ESX events, server callbacks, client callbacks, secure net events
- **rules/best-practices.md** — ESX coding standards, optimization, security, naming conventions

- **rules/reference-links.md** — Official ESX documentation links

## Key principles

1. **Always check for nil** — `if xPlayer then ... end` before using xPlayer
2. **Use ESX.GetPlayerFromId** — Standard player retrieval: `local xPlayer = ESX.GetPlayerFromId(source)`
3. **Wait for player load** — Check `ESX.IsPlayerLoaded()` on client before accessing PlayerData
4. **Never trust client** — Validate all data server-side, use SecureNetEvent for client events
5. **Follow ESX patterns** — Use ESX functions instead of reinventing (callbacks, notifications, etc.)
6. **Optimize loops** — Cache player objects, avoid unnecessary GetPlayerFromId calls
7. **Use camelCase** — Follow Lua naming: `myVariable`, `MyGlobalFunction`, `MY_CONSTANT`
8. **Minimal globals** — Keep variables local unless they need global scope
9. **Use ox_lib for UI** — Prefer ox_lib for menus, dialogs, notifications, progress bars instead of ESX UI
