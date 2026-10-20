---
name: msn-js-sdk
description: Integrates the MSN JavaScript SDK (`window.$msstart`) into JavaScript games running on Microsoft Start. Handles SDK initialization, player authentication, cloud save key/value storage, display banner and interstitial/rewarded ad lifecycles, native sharing, leaderboard score submission, and in-app purchases. Use when the user mentions MSN SDK setup, MSN ads integration, game monetization with MSN, adding MSN features to a JavaScript game, `$msstart`, `msstart` script, MSN cloud save, or MSN IAP.
---

# MSN JavaScript SDK

## Overview

Microsoft Start games expose a single global `window.$msstart` once the official `msstart` script has loaded. Every feature is invoked as `window.$msstart.<method>Async(...)` and returns a Promise.

**Key constraint**: The `msstart` script loading does not guarantee `window.$msstart` is ready — poll for the global before calling any API.

**Key constraint**: IAP is only available when `userAccountType === 'personal'`. Work/school accounts cannot purchase add-ons.

**Not exposed by msstart**: invite friends, join community, create post, add to home screen, rate, achievements, remote config, server time, lifecycle/pause/audio events — use standard browser `visibilitychange`/`blur`/`focus` events for pause/audio and `Date.now()` for non-authoritative timing.

## Integration Workflow

1. **Load script** — inject `<script src='https://assets.msn.com/staticsb/statics/latest/msstart-games-sdk/msstart-v1.0.0-rc.21.min.js'>` (or dynamically) and wait for `window.$msstart` to be defined.
2. **Verify `$msstart`** — `msstart = window.$msstart` must be truthy before any API call.
3. **Probe auth** — call `getSignedInUserAsync()`; if it resolves, `isPlayerAuthorized = true` and `playerId` is set. Catch silently for guests.
4. **Gate features** — cloud save and IAP require `isPlayerAuthorized`. IAP additionally requires `userAccountType === 'personal'`.
5. **Show first interstitial** — wait at least 60 seconds after initialization before the first interstitial.
6. **Validate cloud save** — do a test `getDataAsync` round-trip before relying on cloud save.

## Installation

Load the versioned CDN script and pin the version:

```html
<script src="https://assets.msn.com/staticsb/statics/latest/msstart-games-sdk/msstart-v1.0.0-rc.21.min.js"></script>
```

For dynamic injection, use `document.createElement('script')` with `onload`/`onerror` callbacks, then poll `window.$msstart` in a `setTimeout` loop until defined or a timeout elapses.

## Initialization

```js
const SDK_URL =
    'https://assets.msn.com/staticsb/statics/latest/msstart-games-sdk/msstart-v1.0.0-rc.21.min.js';

const options = {
    gameId: 'YOUR_MSN_GAME_ID',
    payments: [
        // { id: 'gem_pack_small', msn: { id: 'msstore-product-id' } }
    ]
};

let msstart = null;
let isInitialized = false;
let isPlayerAuthorized = false;
let playerId = null;
let playerName = null;
let playerExtra = null;
let isPaymentsSupported = false;

function updatePlayerInfo(data) {
    if (data) {
        isPlayerAuthorized = true;
        playerId = data.playerId;
        playerName = data.playerDisplayName;
        playerExtra = data;
        isPaymentsSupported = data.userAccountType.toLowerCase() === 'personal';
    } else {
        isPlayerAuthorized = false;
        playerId = null;
        playerName = null;
        playerExtra = null;
        isPaymentsSupported = false;
    }
}

function initialize() {
    if (isInitialized) return Promise.resolve();

    return addJavaScript(SDK_URL)
        .then(() => waitFor('$msstart'))
        .then(() => {
            msstart = window.$msstart;
            return msstart
                .getSignedInUserAsync()
                .then((data) => updatePlayerInfo(data))
                .catch(() => updatePlayerInfo(null));
        })
        .then(() => {
            isInitialized = true;
        });
}
```

## Player Auth

```js
function authorizePlayer() {
    if (isPlayerAuthorized) return Promise.resolve();

    return msstart
        .signInAsync()
        .then((data) => updatePlayerInfo(data))
        .catch((error) => {
            updatePlayerInfo(null);
            throw error;
        });
}
```

The signed-in user object contains `playerId`, `playerDisplayName`, and `userAccountType` (`'personal'` for consumer accounts).

## Cloud Save

A per-game key/value bucket under `$msstart.cloudSave`, scoped by `gameId`. No per-key endpoint — read the whole object once, write the merged object on every save. Deletion is performed by writing `null` for the target keys. Requires an authorized player; fall back to `localStorage` for guests.

```js
let cachedData = null;

function isCloudSaveAvailable() {
    return isPlayerAuthorized;
}

function getStorageData(key) {
    if (!isPlayerAuthorized) return Promise.reject();

    const loadCache = cachedData
        ? Promise.resolve(cachedData)
        : msstart.cloudSave.getDataAsync({ gameId: options.gameId }).then((data) => {
              cachedData = data ?? {};
              return cachedData;
          });

    return loadCache.then((data) => (Array.isArray(key) ? key.map((k) => data[k]) : data[key]));
}

function setStorageData(key, value) {
    if (!isPlayerAuthorized) return Promise.reject();

    const data = cachedData ? { ...cachedData } : {};
    if (Array.isArray(key)) {
        key.forEach((k, i) => {
            data[k] = value[i];
        });
    } else {
        data[key] = value;
    }

    return msstart.cloudSave.saveDataAsync({ data, gameId: options.gameId }).then(() => {
        cachedData = data;
    });
}

function deleteStorageData(key) {
    if (!isPlayerAuthorized) return Promise.reject();

    const payload = {};
    const keys = Array.isArray(key) ? key : [key];
    keys.forEach((k) => {
        payload[k] = null;
        if (cachedData) delete cachedData[k];
    });

    return msstart.cloudSave.saveDataAsync({ data: payload, gameId: options.gameId });
}
```

## Advertisement

### Display Banners

Pass an array of placement strings (`'position:WxH'`) to `showDisplayAdsAsync`. At most 2 simultaneous placements are recommended. Hide all with `hideDisplayAdsAsync()`.

Allowed positions and sizes:

```js
const MSN_SIZES_BY_POSITION = {
    top: [
        [728, 90],
        [970, 250],
        [320, 50]
    ],
    bottom: [[320, 50]],
    left: [
        [300, 250],
        [300, 600],
        [320, 50],
        [160, 600]
    ],
    right: [
        [300, 250],
        [300, 600],
        [320, 50],
        [160, 600]
    ],
    topleft: [[300, 250]],
    topright: [[300, 250]],
    bottomleft: [[300, 250]],
    bottomright: [[300, 250]]
};
```

Simple usage:

```js
msstart.showDisplayAdsAsync(['top:728x90']);
msstart.showDisplayAdsAsync(['bottom:320x50']);
msstart.hideDisplayAdsAsync();
```

To pick the largest fitting size for a given pixel rectangle, filter `MSN_SIZES_BY_POSITION[position]` to sizes where `s[0] <= width && s[1] <= height`, then select the entry with the greatest area and format as `'position:WxH'`.

### Interstitial and Rewarded Ads

Shared lifecycle: `loadAdsAsync(isRewarded)` → `showAdsAsync(instanceId)` → `showAdsCompletedAsync`. Pass `false` for interstitial, `true` for rewarded. For rewarded ads, `showAdsCompletedAsync` resolving means the reward is earned. Pause gameplay and audio while the ad is open.

```js
function showInterstitial({ onOpened, onClosed, onFailed } = {}) {
    return msstart
        .loadAdsAsync(false)
        .then((adInstance) => msstart.showAdsAsync(adInstance.instanceId))
        .then((adInstance) => {
            if (onOpened) onOpened();
            return adInstance.showAdsCompletedAsync;
        })
        .then(() => {
            if (onClosed) onClosed();
        })
        .catch((error) => {
            if (onFailed) onFailed(error);
        });
}

function showRewarded({ onOpened, onRewarded, onClosed, onFailed } = {}) {
    return msstart
        .loadAdsAsync(true)
        .then((adInstance) => msstart.showAdsAsync(adInstance.instanceId))
        .then((adInstance) => {
            if (onOpened) onOpened();
            return adInstance.showAdsCompletedAsync;
        })
        .then(() => {
            if (onRewarded) onRewarded();
            if (onClosed) onClosed();
        })
        .catch((error) => {
            if (onFailed) onFailed(error);
        });
}
```

State machine values — interstitial: `'loading' | 'opened' | 'closed' | 'failed'`; rewarded: adds `'rewarded'`.

## Social — Share

```js
function share(shareOptions) {
    // shareOptions: typically { title, text, url } — see msstart docs
    return msstart.shareAsync(shareOptions);
}
```

## Leaderboards

Write-only — `submitGameResultsAsync(score)`. The host UI renders the leaderboard; there is no client-side read-back endpoint.

```js
function leaderboardsSetScore(score) {
    return msstart.submitGameResultsAsync(score);
}
```

## In-App Purchases

All four operations are under `$msstart.iap`. Map local product ids to msstart product ids in your catalog. **IAP requires `userAccountType === 'personal'`** — check `isPaymentsSupported` before calling.

**Important**: Failure responses are returned in-band as `{ code: 'IAP_*_FAILURE', description }` resolutions, not rejections — always inspect `code` before treating a response as success.

### Get Catalog

```js
function paymentsGetCatalog() {
    if (!options.payments) return Promise.reject();

    return msstart.iap.getAllAddOnsAsync({ productId: options.gameId }).then((msnProducts) => {
        if (msnProducts.code === 'IAP_GET_ALL_ADD_ONS_FAILURE') {
            throw new Error(msnProducts.description);
        }
        return options.payments.map((product) => {
            const platformId = product.msn?.id ?? product.id;
            const p = msnProducts.find((m) => m.productId === platformId);
            return {
                id: product.id,
                title: p.title,
                description: p.description,
                publisherName: p.publisherName,
                inAppOfferToken: p.inAppOfferToken,
                isConsumable: p.isConsumable,
                price: `${p.price.listPrice} ${p.price.currencyCode}`,
                priceCurrencyCode: p.price.currencyCode,
                priceValue: p.price.listPrice
            };
        });
    });
}
```

### Purchase

Host returns `{ receipt, receiptSignature }` or `{ code: 'IAP_PURCHASE_FAILURE', description }`.

```js
const purchases = [];

async function paymentsPurchase(id) {
    const product = options.payments.find((p) => p.id === id);
    if (!product) return Promise.reject();
    if (!isPlayerAuthorized) await authorizePlayer();

    const platformProductId = product.msn?.id ?? product.id;
    const purchase = await msstart.iap.purchaseAsync({ productId: platformProductId });

    if (purchase.code === 'IAP_PURCHASE_FAILURE') throw new Error(purchase.description);

    const merged = { id, ...purchase.receipt, receiptSignature: purchase.receiptSignature };
    purchases.push(merged);
    return merged;
}
```

### Consume Purchase

Consume by msstart `productId` (from cached purchase). Returns `{ consumptionReceipt, consumptionSignature }` or `{ code: 'IAP_CONSUME_FAILURE', description }`.

```js
async function paymentsConsumePurchase(id) {
    const idx = purchases.findIndex((p) => p.id === id);
    if (idx < 0) return Promise.reject();
    if (!isPlayerAuthorized) await authorizePlayer();

    const response = await msstart.iap.consumeAsync({ productId: purchases[idx].productId });
    if (response.code === 'IAP_CONSUME_FAILURE') throw new Error(response.description);

    purchases.splice(idx, 1);
    const result = {
        id,
        ...response.consumptionReceipt,
        consumptionSignature: response.consumptionSignature
    };
    delete result.productId;
    return result;
}
```

### Get Purchases

`IAP_GET_ALL_PURCHASES_FAILURE` should be treated as an empty list.

```js
async function paymentsGetPurchases() {
    if (!isPlayerAuthorized) await authorizePlayer();

    try {
        const response = await msstart.iap.getAllPurchasesAsync({ productId: options.gameId });
        purchases.length = 0;
        response.receipts.forEach((purchase) => {
            const product = options.payments.find(
                (p) => (p.msn?.id ?? p.id) === purchase.productId
            );
            purchases.push({
                id: product ? product.id : purchase.productId,
                ...purchase,
                receiptSignature: response.receiptSignature
            });
        });
        return purchases.slice();
    } catch (error) {
        if (error?.code === 'IAP_GET_ALL_PURCHASES_FAILURE') return [];
        throw error;
    }
}
```
