---
name: crazy-games-js-sdk
description: Integrates the CrazyGames JavaScript SDK (v3) into a browser or HTML5 game. Handles SDK initialization, user authentication and profile retrieval, persistent key/value storage, interstitial and rewarded ad breaks, adblock detection, responsive banner ads, gameplay lifecycle hooks (loadingStart/Stop, gameplayStart/Stop, happytime), and optional Xsolla Pay Station in-app purchases with analytics order tracking. Use when the user mentions CrazyGames, wants to publish or integrate a game on CrazyGames, or needs to add SDK features like ads, user accounts, game events, storage, or in-game purchases to a browser/HTML5/JavaScript game.
---

# CrazyGames JavaScript SDK

## Integration Checklist

Follow this order when integrating the SDK into a game:

1. **Load SDK** — add the CDN `<script>` tag before your game bootstraps
2. **Init** — call `SDK.init()` and await resolution before touching any SDK module
3. **Lifecycle hooks** — wire `loadingStart/Stop` and `gameplayStart/Stop` throughout the game loop
4. **Ads** — add interstitial and/or rewarded ad calls at natural break points
5. **Optional: Auth & Storage** — add sign-in and persistent key/value storage if needed
6. **Optional: Payments** — Xsolla Pay Station integration (separate concern; skip if not applicable)

---

## Installation

Load the SDK from the official CDN before bootstrapping the game.

```html
<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>
```

If you load it dynamically, wait until `window.CrazyGames.SDK.init` is defined before calling it. If the script is blocked (e.g. by CSP), the `window.CrazyGames` global will be undefined — add `sdk.crazygames.com` to your `script-src` directive.

## Initialization

Call `SDK.init()` once. It resolves when the SDK is ready. Only after resolution are `SDK.user`, `SDK.data`, `SDK.ad`, `SDK.banner`, `SDK.game`, and `SDK.analytics` safe to use.

```javascript
async function initCrazyGames() {
    if (!window.CrazyGames?.SDK) {
        throw new Error('CrazyGames SDK script not loaded');
    }
    const sdk = window.CrazyGames.SDK;
    try {
        await sdk.init();
    } catch (err) {
        throw new Error(`CrazyGames SDK init failed: ${err.message}`);
    }

    const isUserAccountAvailable = sdk.user.isUserAccountAvailable;

    if (isUserAccountAvailable) {
        const language = sdk.user.systemInfo.countryCode.toLowerCase();
        const deviceType = sdk.user.systemInfo.device.type.toLowerCase(); // 'desktop' | 'mobile' | 'tablet'
        console.log('lang/device', language, deviceType);
    }

    return sdk;
}
```

## Verification

After calling `initCrazyGames()`, confirm the SDK is working before proceeding:

- **Console check** — no `CrazyGames SDK init failed` error should appear; `sdk.user.isUserAccountAvailable` should return a boolean without throwing.
- **Lifecycle hooks** — open the CrazyGames sandbox URL for your game and verify that `loadingStart` / `loadingStop` / `gameplayStart` / `gameplayStop` calls appear in the CrazyGames developer dashboard event log.
- **Ad callbacks** — use the CrazyGames sandbox environment (append `?crazygames_sandbox=1` to the URL) to trigger test ads and confirm `adStarted` and `adFinished` fire correctly.
- **Adblock** — call `sdk.ad.hasAdblock()` while running with an ad blocker enabled and confirm it resolves `true`.

---

## Player / Authorization

Use `showAuthPrompt()` to ask the player to sign in, then `getUser()` to read profile data, and optionally `getUserToken()` for a signed JWT to verify on your backend.

```javascript
async function authorizePlayer(sdk, { useUserToken = false } = {}) {
    if (!sdk.user.isUserAccountAvailable) {
        // Guest session — no auth possible on this domain
        return null;
    }

    await sdk.user.showAuthPrompt();

    const user = await sdk.user.getUser();
    if (!user) {
        return null;
    }

    const profile = {
        name: user.username || null,
        photo: user.profilePictureUrl || null,
        extra: user
    };

    if (useUserToken) {
        profile.extra.jwt = await sdk.user.getUserToken();
    }

    return profile;
}
```

## Storage

CrazyGames provides synchronous key/value storage via `SDK.data`. Values are strings; serialize JSON yourself.

```javascript
function storageSet(sdk, key, value) {
    const data = typeof value === 'string' ? value : JSON.stringify(value);
    sdk.data.setItem(key, data);
}

function storageGet(sdk, key, tryParseJson = true) {
    const raw = sdk.data.getItem(key);
    if (!tryParseJson || raw == null) {
        return raw;
    }
    try {
        return JSON.parse(raw);
    } catch (_) {
        return raw;
    }
}

function storageRemove(sdk, key) {
    sdk.data.removeItem(key);
}

// Batch helpers — just iterate, the SDK has no native multi-key API
function storageSetMany(sdk, keys, values) {
    for (let i = 0; i < keys.length; i++) {
        storageSet(sdk, keys[i], values[i]);
    }
}
```

## Advertisement

### Interstitial ad (`midgame`)

Call `SDK.ad.requestAd('midgame', callbacks)`. The callbacks fire synchronously as the ad lifecycle progresses.

```javascript
function showInterstitial(sdk) {
    sdk.ad.requestAd('midgame', {
        adStarted: () => {
            // Mute audio and pause the game here
        },
        adFinished: () => {
            // Resume audio and gameplay here
        },
        adError: (error) => {
            console.warn('interstitial failed', error);
        }
    });
}
```

### Rewarded ad

Same API, pass `'rewarded'` as the type. `adFinished` means the user watched to completion and should receive the reward.

```javascript
function showRewarded(sdk, onReward) {
    sdk.ad.requestAd('rewarded', {
        adStarted: () => {
            // Pause the game
        },
        adFinished: () => {
            onReward();
        },
        adError: (error) => {
            console.warn('rewarded failed', error);
        }
    });
}
```

### Adblock detection

```javascript
async function isAdblockActive(sdk) {
    return sdk.ad.hasAdblock();
}
```

### Responsive banners

Banners are bound to existing DOM containers by id. CrazyGames renders into them and picks an appropriate size.

```javascript
async function showBanner(sdk, containerId) {
    // The container must already be in the DOM and visible
    try {
        await sdk.banner.requestResponsiveBanner([containerId]);
    } catch (e) {
        console.warn('banner failed', e);
    }
}

async function showAdvancedBanners(sdk, containerIds) {
    // Request several banners in parallel
    await Promise.all(containerIds.map((id) => sdk.banner.requestResponsiveBanner(id)));
}

function hideBanners(sdk) {
    sdk.banner.clearAllBanners();
}
```

## Lifecycle / gameplay events

CrazyGames REQUIRES the host game to call gameplay and loading hooks at the right moments — they drive ad pacing, in-game UI dimming, and analytics.

Map generic game lifecycle events to SDK calls as follows:

| Game event                                                            | SDK call                   |
| --------------------------------------------------------------------- | -------------------------- |
| `level_started`, `level_resumed`, `gameplay_started`                  | `sdk.game.gameplayStart()` |
| `level_paused`, `level_completed`, `level_failed`, `gameplay_stopped` | `sdk.game.gameplayStop()`  |
| `in_game_loading_started`                                             | `sdk.game.loadingStart()`  |
| `in_game_loading_stopped`                                             | `sdk.game.loadingStop()`   |
| `player_got_achievement`                                              | `sdk.game.happytime()`     |

There are no separate `audio` / `pause` / `visibility` callbacks on the CrazyGames SDK — drive your audio and pause state from the ad callbacks (`adStarted` / `adFinished`) and the standard `document.visibilitychange` event.

---

## Payments (optional, via Xsolla Pay Station)

> **Skip this section entirely if you do not have an Xsolla project ID.** CrazyGames itself does not sell IAPs; this integration uses CrazyGames-issued Xsolla user tokens with the Xsolla Pay Station widget and Xsolla Store API.

Key constants:

```javascript
const XSOLLA_PAYSTATION_EMBED_URL =
    'https://cdn.xsolla.net/payments-bucket-prod/embed/1.5.0/widget.min.js';
const XSOLLA_SDK_URL = 'https://store.xsolla.com/api/v2/project';
```

Obtain the Xsolla user token via `sdk.user.getXsollaUserToken()`. Use it as a `Bearer` token for all Xsolla Store API requests (catalog, purchase, inventory, consume).

**Catalog** — `GET /{projectId}/items?limit=50`

**Purchase flow**:

1. `POST /{projectId}/payment/item/{sku}` → returns `{ token, order_id }`
2. Load `XSOLLA_PAYSTATION_EMBED_URL` dynamically if not already present
3. `XPayStationWidget.init({ access_token: token, sandbox: isSandbox })` then `.open()`
4. Listen for `XPayStationWidget.eventTypes.STATUS`; when `paymentInfo.status` matches `/done|charged|success/i`, fetch `GET /{projectId}/order/{orderId}` and call `sdk.analytics.trackOrder('xsolla', order)` to record the purchase
5. Listen for the `'close'` event to handle cancellation

**Inventory** — `GET /{projectId}/user/inventory/items`

**Consume** — `POST /{projectId}/user/inventory/item/consume` with `{ sku, quantity }`

All fetch calls must include `Authorization: Bearer <xsollaToken>`. Throw on non-OK responses. Use `isSandbox: true` during development.
