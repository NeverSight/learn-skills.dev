---
name: remix-shop-items
description: Create and manage in-game shop items for a Remix game
---

# Manage Shop Items Workflow

## Overview

This skill guides you through creating, managing, and integrating shop items
for games on the Remix platform.

## Prerequisites

- A game must be created on the Remix platform (you need a game ID).
- The `REMIX_API_KEY` environment variable must be set.

## Steps

### 1. Check for Existing Game ID

Read `.remix-settings.json` in the current directory. If it exists and contains
a `gameId`, use that value.

Only if `.remix-settings.json` does not exist or has no `gameId` should you
follow the **upload-game** workflow to create one.

### 2. Manage Shop Items

#### List All Items

```
GET https://api.remix.gg/v1/games/{gameId}/items
Authorization: Bearer $REMIX_API_KEY
```

#### Create an Item

```
POST https://api.remix.gg/v1/games/{gameId}/items
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{
  "name": "Speed Boost",
  "description": "Doubles player speed for 30 seconds",
  "price": 100,
  "type": "consumable",
  "imageUrl": "https://asset-url.png",
  "metadata": { "duration": 30 }
}
```

- `type` can be `"consumable"` (can be purchased multiple times) or `"permanent"` (one-time purchase)
- `imageUrl` and `metadata` are optional

#### Update an Item

```
POST https://api.remix.gg/v1/games/{gameId}/items/{itemId}
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{ "price": 150 }
```

Accepts a partial body -- only include fields you want to change.

#### Delete an Item

```
DELETE https://api.remix.gg/v1/games/{gameId}/items/{itemId}
Authorization: Bearer $REMIX_API_KEY
```

### 3. Integrate Shop Items in Game Code

Add the RemixSDK shop integration to your game:

```js
const sdk = window.RemixSDK

// Check if player has a permanent item
const hasItem = sdk.hasItem('item-id')

// Get purchase count for a consumable item
const count = sdk.getItemPurchaseCount('item-id')

// Trigger the purchase flow (opens platform purchase UI)
sdk.singlePlayer.actions.purchase({ item: { id: 'item-id' } })

// Listen for purchase completion
sdk.onPurchaseComplete(({ item }) => {
  // Grant the item in-game
})
```

## Wrong Patterns

Do NOT do any of the following:

- **Granting items without listening to `onPurchaseComplete`.** Always wait for
  the callback before giving the player anything. The purchase may fail or be
  cancelled.

- **Using `localStorage` to track purchases.** The platform handles purchase
  state. Use `hasItem()` and `getItemPurchaseCount()` to check ownership.

- **Hardcoding prices in game code.** Always read prices from the API. If you
  change a price on the server, hardcoded values in the game will be wrong.

## Tips

- Use `"consumable"` for items players buy repeatedly (lives, boosts, ammo).
- Use `"permanent"` for one-time unlocks (characters, levels, cosmetics).
- Always check `hasItem()` on game load to restore permanent purchases.
