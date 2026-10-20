---
name: yandex-js-sdk
description: Integrates the Yandex Games JavaScript SDK (YaGames) into JavaScript games. Initializes the SDK and lifecycle hooks, manages player authentication and authorization, handles per-player cloud storage, controls ad placements (interstitial, rewarded video, sticky banner), implements in-app purchases and leaderboards, retrieves remote config flags, and supports social features such as review prompts and home-screen shortcuts. Use when the user mentions Yandex Games, YaGames, yandex sdk, deploying a game to the Yandex.Games platform, or integrating features like ads, leaderboards, in-app purchases, or player authentication into a Yandex-hosted JavaScript game.
---

# Yandex Games JavaScript SDK

## Overview

Yandex Games loads games inside a frame on `yandex.<tld>/games`. The host injects the `YaGames` global once the SDK script is loaded. Key capability areas:

- **Lifecycle & environment**: init, `LoadingAPI.ready()`, `GameplayAPI.start/stop`, pause/resume events, device info, language/TLD
- **Player & storage**: authorization, profile data, per-player key/value cloud storage
- **Monetization**: fullscreen interstitial, rewarded video, sticky banner ads, in-app purchases
- **Engagement**: leaderboards, remote config flags, review prompt, add-to-home-screen shortcut, server time, clipboard write, cross-promotion via `GamesAPI`

The SDK does NOT expose social share, invite-friends, community-join, add-to-favorites, achievements, or stat counters.

## Installation

```html
<script src="https://yandex.ru/games/sdk/v2"></script>
```

If loaded dynamically, poll until `window.YaGames && window.YaGames.init` is defined before calling `init()`.

## Quick Start / Integration Workflow

Follow this sequence when wiring up the SDK for the first time. Verify each step before proceeding to the next.

```javascript
async function bootstrap() {
    // 1. Ensure SDK script has loaded
    if (!window.YaGames?.init) {
        throw new Error('YaGames SDK not available — check that the script tag loaded');
    }

    // 2. Initialize — all subsequent SDK calls require ysdk
    const ysdk = await window.YaGames.init();

    // 3. Bind host-driven pause / resume before anything else
    ysdk.on('game_api_pause', () => {
        /* mute audio, pause gameplay */
    });
    ysdk.on('game_api_resume', () => {
        /* unmute, resume */
    });

    // 4. Signal that the loading screen is gone
    ysdk.features.LoadingAPI?.ready();

    // 5. Read environment (language, device type)
    const env = readEnvironment(ysdk);

    // 6. Fetch player — fall back to guest mode if not authorized
    let player = null;
    let storageCache = {};
    try {
        const info = await getPlayer(ysdk);
        player = info.raw;
        if (info.isAuthorized) {
            storageCache = await loadStorage(player);
        }
    } catch (err) {
        console.warn('Player init failed, continuing as guest:', err);
    }

    // 7. Start gameplay tracking
    onGameplayStarted(ysdk);

    return { ysdk, player, storageCache, env };
}
```

```javascript
function readEnvironment(ysdk) {
    return {
        language: ysdk.environment.i18n.lang.toLowerCase(),
        tld: ysdk.environment.i18n.tld.toLowerCase(),
        deviceType: ysdk.deviceInfo.type // 'desktop' | 'mobile' | 'tablet' | 'tv'
    };
}
```

## Player / Authorization

```javascript
async function getPlayer(ysdk, { useSignedData = false } = {}) {
    const player = await ysdk.getPlayer({ signed: useSignedData });

    return {
        raw: player,
        id: player.getUniqueID(),
        name: player.getName() || null,
        photos: ['small', 'medium', 'large'].map((size) => player.getPhoto(size)).filter(Boolean),
        isAuthorized: player.isAuthorized(),
        payingStatus: player.getPayingStatus(),
        signature: useSignedData ? player.signature : null
    };
}

async function authorizePlayer(ysdk, options) {
    const current = await getPlayer(ysdk, options);
    if (current.isAuthorized) {
        return current;
    }

    await ysdk.auth.openAuthDialog();
    return getPlayer(ysdk, options);
}
```

## Storage

Every call writes the full document — there is no per-key API. Cache the latest snapshot client-side and merge before each save. Fall back to `localStorage` for guests.

```javascript
async function loadStorage(player) {
    return player.getData();
}

async function setStorage(player, cache, key, value) {
    const data = { ...(cache || {}) };
    if (Array.isArray(key)) {
        for (let i = 0; i < key.length; i++) {
            data[key[i]] = value[i];
        }
    } else {
        data[key] = value;
    }
    await player.setData(data);
    return data;
}

async function deleteStorage(player, cache, key) {
    const data = { ...(cache || {}) };
    if (Array.isArray(key)) {
        for (let i = 0; i < key.length; i++) {
            delete data[key[i]];
        }
    } else {
        delete data[key];
    }
    await player.setData(data);
    return data;
}

function getCached(cache, key) {
    if (Array.isArray(key)) {
        return key.map((k) => (typeof cache?.[k] === 'undefined' ? null : cache[k]));
    }
    return typeof cache?.[key] === 'undefined' ? null : cache[key];
}
```

## Advertisement

### Fullscreen interstitial

`onClose(wasShown)` fires on both normal close and SDK-skipped ads. Treat `wasShown === false` as a failure.

```javascript
function showInterstitial(ysdk, handlers = {}) {
    ysdk.adv.showFullscreenAdv({
        callbacks: {
            onOpen: () => handlers.onOpen?.(),
            onClose: (wasShown) => handlers.onClose?.(wasShown),
            onError: (err) => handlers.onError?.(err)
        }
    });
}
```

### Rewarded video

Grant the reward inside `onRewarded`. `onClose` fires after the ad UI is dismissed.

```javascript
function showRewarded(ysdk, handlers = {}) {
    ysdk.adv.showRewardedVideo({
        callbacks: {
            onOpen: () => handlers.onOpen?.(),
            onRewarded: () => handlers.onRewarded?.(),
            onClose: () => handlers.onClose?.(),
            onError: (err) => handlers.onError?.(err)
        }
    });
}
```

### Sticky banner

```javascript
async function getBannerStatus(ysdk) {
    return ysdk.adv.getBannerAdvStatus(); // { stickyAdvIsShowing: boolean, reason?: string }
}

async function showBanner(ysdk) {
    const data = await ysdk.adv.showBannerAdv();
    return data.stickyAdvIsShowing === true;
}

async function hideBanner(ysdk) {
    const data = await ysdk.adv.hideBannerAdv();
    return data.stickyAdvIsShowing === false;
}
```

## Payments / IAP

Obtain the payments object once after init. Pass `signed: true` for backend signature validation.

```javascript
async function initPayments(ysdk, { signed = true } = {}) {
    return ysdk.getPayments({ signed });
}
```

### Catalog

```javascript
async function getCatalog(payments) {
    const products = await payments.getCatalog();
    return products.map((p) => ({
        id: p.id,
        title: p.title,
        description: p.description,
        imageURI: p.imageURI,
        price: p.price,
        priceValue: p.priceValue,
        priceCurrencyCode: p.priceCurrencyCode,
        priceCurrencyImage: p.getPriceCurrencyImage?.('medium')
    }));
}
```

### Purchase

```javascript
async function purchase(payments, productId, payload) {
    const result = await payments.purchase({ id: productId, developerPayload: payload });
    if (!result?.purchaseData?.purchaseToken) {
        throw new Error(
            `Purchase succeeded but returned no purchaseToken for product ${productId}`
        );
    }
    return { id: productId, ...result.purchaseData };
}
```

### Owned purchases

```javascript
async function getPurchases(payments) {
    const list = await payments.getPurchases();
    return list.map((purchase) => ({ id: purchase.productID, ...purchase.purchaseData }));
}
```

### Consume

Verify the item was granted before consuming. A failed consume leaves the token intact for retry.

```javascript
async function consumePurchase(payments, purchaseToken) {
    if (!purchaseToken) {
        throw new Error('consumePurchase: purchaseToken is required');
    }
    await payments.consumePurchase(purchaseToken);
}
```

## Leaderboards

Boards are configured in the developer console and referenced by string id. Setting a score requires an authorized player.

```javascript
async function setLeaderboardScore(ysdk, leaderboardId, score) {
    const lb = await ysdk.getLeaderboards();
    await lb.setLeaderboardScore(leaderboardId, score);
}

async function getLeaderboardEntries(ysdk, leaderboardId, { isPlayerAuthorized = false } = {}) {
    const lb = await ysdk.getLeaderboards();

    const options = { quantityTop: 20 };
    if (isPlayerAuthorized) {
        options.includeUser = true;
        options.quantityAround = 3;
    }

    const result = await lb.getLeaderboardEntries(leaderboardId, options);
    if (!result || result.entries.length === 0) {
        return [];
    }

    return result.entries.map((e) => ({
        id: e.player.uniqueID,
        name: e.player.publicName,
        score: e.score,
        rank: e.rank,
        photo: e.player.getAvatarSrc('large')
    }));
}
```

## Remote config

`ysdk.getFlags(options)` returns a flat `{ key: stringValue }` map.

```javascript
async function getRemoteConfig(ysdk, options = {}) {
    const params = { clientFeatures: [], ...options };
    return ysdk.getFlags(params);
}
```

## Server time

```javascript
function getServerTime(ysdk) {
    // Returns Unix timestamp in milliseconds
    return ysdk.serverTime();
}
```

## Social

### Review prompt

```javascript
async function requestReview(ysdk) {
    const can = await ysdk.feedback.canReview();
    if (!can.value) {
        throw new Error(can.reason || 'review not available');
    }
    const { feedbackSent } = await ysdk.feedback.requestReview();
    return feedbackSent;
}
```

### Add to home screen (shortcut)

```javascript
async function canAddToHomeScreen(ysdk) {
    const prompt = await ysdk.shortcut.canShowPrompt();
    return prompt.canShow === true;
}

async function addToHomeScreen(ysdk) {
    const result = await ysdk.shortcut.showPrompt();
    return result.outcome === 'accepted';
}
```

## Clipboard

```javascript
async function clipboardWrite(ysdk, text) {
    await ysdk.clipboard.writeText(text);
}
```

## Gameplay lifecycle, pause and audio

Bracket every active gameplay session with `GameplayAPI.start()` / `GameplayAPI.stop()` to drive ad pacing and analytics.

```javascript
function onGameplayStarted(ysdk) {
    ysdk.features.GameplayAPI?.start();
}

function onGameplayStopped(ysdk) {
    ysdk.features.GameplayAPI?.stop();
}
```

```javascript
function bindPauseHandlers(ysdk, { onPause, onResume }) {
    ysdk.on('game_api_pause', () => onPause?.());
    ysdk.on('game_api_resume', () => onResume?.());
}
```

Visibility/focus changes not announced by Yandex should still be handled with `document.visibilitychange`, `window.blur`, and `window.focus` alongside these SDK callbacks.

## Catalog of other Yandex Games (optional)

`features.GamesAPI` is gated on availability per game; check for the namespace before calling it.

```javascript
async function getAllGames(ysdk) {
    const { games } = await ysdk.features.GamesAPI.getAllGames();
    return games;
}

async function getGameById(ysdk, gameId) {
    const { game, isAvailable } = await ysdk.features.GamesAPI.getGameByID(gameId);
    return { ...game, isAvailable };
}
```
