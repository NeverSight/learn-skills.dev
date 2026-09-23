---
name: kiosk
description: >
  Sui Kiosk and NFT trading primitives. Use when writing, reviewing, or debugging
  Move code that uses Kiosk for commerce, NFT trading, asset listing, TransferPolicy
  enforcement, or building Kiosk Apps and extensions. Also use when the user asks
  about asset states (PLACED, LOCKED, LISTED), borrowing patterns, purchase flows,
  or the kiosk_extension permissioned apps API.
---

# Sui Kiosk Skill

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/standards/kiosk](https://docs.sui.io/standards/kiosk). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

Kiosk is a decentralized system for commerce applications on Sui, providing shared objects that store assets with built-in trading functionality including custom trade mechanisms like auctions. This skill covers Kiosk creation, asset management, listing and purchase flows, TransferPolicy enforcement, borrowing patterns, and the Kiosk Apps extension API. Common mistakes include forgetting that a TransferPolicy is required before items can be traded, attempting to mutably borrow listed items, and misunderstanding the permissions bitmap for Kiosk Apps.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/standards/kiosk

If unsure about any API, fetch the relevant page before answering.
Do not guess or extrapolate from other protocols or NFT standards.

---

## Reference files

### core -- Core Kiosk Operations
**Path:** `core.md`
**Load when:** the user needs to create a Kiosk, place or take assets, list or delist items, purchase items, understand TransferPolicy and the purchase flow, understand asset states (PLACED, LOCKED, LISTED, LISTED EXCLUSIVELY), borrow assets, or withdraw sale proceeds.
**Covers:** Kiosk creation, KioskOwnerCap, placing and taking items, locking items, listing and delisting, purchase flow with TransferRequest, TransferPolicy, asset states, immutable and mutable borrowing, the borrow_val hot potato pattern, access control, withdrawal.

### apps -- Kiosk Apps and Extensions
**Path:** `apps.md`
**Load when:** the user needs to build basic Kiosk apps using dynamic fields, build permissioned apps with the kiosk_extension module, understand the permissions bitmap, manage app lifecycle (install, enable, disable, remove), or use app-isolated storage.
**Covers:** basic apps via UID dynamic fields, uid_mut_as_owner, the Kiosk Name app example, permissioned apps via kiosk_extension, app lifecycle, permissions bitmap (place, lock), protected functions, permission checking, app storage (bag-type isolated storage).

---

## Routing guide

| Task | Load |
|------|------|
| Creating a Kiosk | core |
| Placing, taking, or locking items | core |
| Listing or delisting items | core |
| Purchasing items and satisfying TransferPolicy | core |
| Understanding asset states | core |
| Borrowing assets (immutable, mutable, PTB-friendly) | core |
| Withdrawing sale proceeds | core |
| Building a basic Kiosk app with dynamic fields | apps |
| Building a permissioned Kiosk extension | apps |
| Understanding permissions bitmap | apps |
| Managing app lifecycle (install, enable, disable, remove) | apps |
| Using app-isolated storage | apps |
| Full Kiosk integration | **all reference files** |
| Code review of Kiosk code | **all reference files** |

---

## Skill Content

### Key concepts

- **Kiosk.** A shared object that stores assets with built-in trading functionality. Created via `kiosk::default`, which shares the Kiosk and transfers the `KioskOwnerCap` to the creator.

- **KioskOwnerCap.** The capability that grants ownership over a Kiosk. Only the cap owner can place, take, list, borrow, or modify assets in the Kiosk.

- **TransferPolicy.** A shared object associated with asset type `T` that defines the rules all trades of that type must satisfy. Without an associated TransferPolicy, items of type `T` cannot be traded (storage is still possible). Policy changes apply instantly and globally across all platform trades.

- **TransferRequest.** A hot potato returned by `kiosk::purchase` that must be resolved by satisfying all TransferPolicy terms before the transaction completes.

- **Asset states.** Items in a Kiosk exist in one of four states: PLACED (withdrawable, borrowable, listable), LOCKED (non-withdrawable but mutable-borrowable and listable), LISTED (immutably borrowable only, no modifications), and LISTED EXCLUSIVELY (extension-managed via `kiosk::list_with_purchase_cap`).

- **MIST.** The smallest unit of SUI. 1 SUI = 10^9 MIST. Listing prices are specified in MIST.

### Rules

1. **A TransferPolicy must exist for type `T` before items of that type can be traded.** Without one, `kiosk::purchase` cannot complete. Items can still be stored (placed) without a TransferPolicy.
2. **Listed items cannot be mutably borrowed.** Only immutable borrows are available for items in the LISTED state.
3. **Locked items cannot be withdrawn.** Items placed via `kiosk::lock` require an associated TransferPolicy and cannot be taken out of the Kiosk, only listed and sold.
4. **The `borrow_val` hot potato must be returned via `return_val`.** Failure to return causes a transaction abort.
5. **Only the KioskOwnerCap holder can modify Kiosk contents.** All place, take, list, borrow, and withdrawal operations require the cap.

### Common mistakes

- **Forgetting the TransferPolicy.** Attempting to purchase an item type that has no associated TransferPolicy causes the transaction to fail. Ensure a TransferPolicy is created and shared before trading.
- **Mutably borrowing a listed item.** Items in the LISTED state only support immutable borrows. Attempting `borrow_mut` on a listed item fails.
- **Confusing PLACED and LOCKED states.** PLACED items can be withdrawn with `kiosk::take`; LOCKED items cannot. Use `kiosk::lock` only when you want to enforce that items can only leave the Kiosk through a sale.
- **Not satisfying all TransferPolicy terms.** The `TransferRequest` returned by `kiosk::purchase` must satisfy every rule in the TransferPolicy. Missing even one causes the transaction to abort.
- **Using SUI instead of MIST for listing prices.** `kiosk::list` expects prices in MIST (1 SUI = 10^9 MIST). Passing a price of `1` means 1 MIST, not 1 SUI.
