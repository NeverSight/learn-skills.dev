---
name: game-distribution-js-sdk
description: Integrates the GameDistribution JavaScript SDK (GD SDK) into a JavaScript or HTML5 game, covering SDK initialization, interstitial and rewarded ad display, banner ads, ad callback handling, and game lifecycle events. Use when the user asks about GameDistribution, GD SDK, game ads, HTML5 game monetization, ad integration, or wiring up ads and lifecycle events in a JavaScript or HTML5 game.
---

# GameDistribution JavaScript SDK

## Overview

GameDistribution exposes a single browser SDK (`window.gdsdk`) configured via a global `window.GD_OPTIONS` object. The SDK loads, fires lifecycle events through a single `onEvent` callback, and exposes promise-returning methods to preload and show ads. The native SDK supports:

- Initialization with a `gameId` and a single `onEvent` callback
- Interstitial ads (`gdsdk.showAd()`)
- Rewarded ads (`gdsdk.preloadAd('rewarded')` + `gdsdk.showAd('rewarded')`)
- Display banners (`gdsdk.showAd('display', { containerId })`)
- Lifecycle pause/resume signals via `SDK_GAME_PAUSE` / `SDK_GAME_START` events

No player auth, storage, payments, leaderboards, or social APIs. External-link navigation should also be avoided on this platform.

## Installation

Append the SDK script to the page after defining `window.GD_OPTIONS`. The script URL is fixed:

```js
const SDK_URL = 'https://html5.api.gamedistribution.com/main.min.js';

function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}
```

The SDK exposes itself as `window.gdsdk` once the `SDK_READY` event fires.

## Initialization

GameDistribution is configured by assigning `window.GD_OPTIONS` BEFORE the SDK script is appended. The only required field is `gameId` — your GameDistribution game GUID. All lifecycle and ad events arrive through the single `onEvent(event)` callback.

```js
const options = {
    gameId: 'YOUR_GAME_ID'
};

let platformSdk = null;
let isInitialized = false;
let currentAdvertisementIsRewarded = false;

const listeners = {
    interstitialStateChanged: [],
    rewardedStateChanged: [],
    bannerStateChanged: [],
    pauseStateChanged: [],
    audioStateChanged: []
};

function emit(name, payload) {
    listeners[name].forEach((cb) => cb(payload));
}

function initialize() {
    return new Promise((resolve, reject) => {
        if (isInitialized) {
            resolve();
            return;
        }

        if (typeof options.gameId !== 'string') {
            reject(new Error('Game params are not found'));
            return;
        }

        window.GD_OPTIONS = {
            gameId: options.gameId,
            onEvent(event) {
                switch (event.name) {
                    case 'SDK_READY':
                        platformSdk = window.gdsdk;
                        isInitialized = true;

                        // Optional: show an interstitial immediately once the SDK is ready
                        showInterstitial();
                        resolve();
                        break;
                    case 'SDK_GAME_START':
                        // Ad finished — game should resume
                        if (currentAdvertisementIsRewarded) {
                            emit('rewardedStateChanged', 'closed');
                            // Preload the next rewarded ad right away
                            platformSdk.preloadAd('rewarded');
                        } else {
                            emit('interstitialStateChanged', 'closed');
                        }
                        emit('pauseStateChanged', false);
                        emit('audioStateChanged', true);
                        break;
                    case 'SDK_GAME_PAUSE':
                        // Ad started — game should pause
                        if (currentAdvertisementIsRewarded) {
                            emit('rewardedStateChanged', 'opened');
                        } else {
                            emit('interstitialStateChanged', 'opened');
                        }
                        emit('pauseStateChanged', true);
                        emit('audioStateChanged', false);
                        break;
                    case 'SDK_REWARDED_WATCH_COMPLETE':
                        // Reward must be granted here
                        emit('rewardedStateChanged', 'rewarded');
                        break;
                    case 'SDK_GDPR_TRACKING':
                    case 'SDK_GDPR_TARGETING':
                    default:
                        break;
                }
            }
        };

        loadScript(SDK_URL).catch(reject);
    });
}
```

Key event names emitted by the SDK through `onEvent`:

- `SDK_READY` — SDK is ready, `window.gdsdk` is available.
- `SDK_GAME_PAUSE` — an ad is starting; pause gameplay and mute audio.
- `SDK_GAME_START` — an ad has ended (or none was shown); resume gameplay and unmute audio.
- `SDK_REWARDED_WATCH_COMPLETE` — the user completed a rewarded ad; grant the reward.
- `SDK_GDPR_TRACKING`, `SDK_GDPR_TARGETING` — GDPR consent signals (no action usually required).

## Advertisement

GameDistribution supports interstitial, rewarded, and display banner ads. All ad methods on `gdsdk` return promises and reject when an ad cannot be served.

You must remember which ad type is currently in flight (interstitial vs rewarded) so the shared `SDK_GAME_PAUSE` / `SDK_GAME_START` events can be routed to the right state.

### Interstitial

```js
function showInterstitial() {
    currentAdvertisementIsRewarded = false;

    if (!platformSdk) {
        emit('interstitialStateChanged', 'failed');
        return;
    }

    platformSdk.showAd().catch(() => {
        emit('interstitialStateChanged', 'failed');
    });
}
```

GameDistribution does not enforce a minimum delay between interstitials at the SDK level — call `showAd()` whenever your game logic requires.

### Rewarded

Rewarded ads must be preloaded before they can be shown. After every rewarded ad completes (`SDK_GAME_START`), preload the next one.

```js
function preloadRewarded() {
    if (platformSdk) {
        platformSdk.preloadAd('rewarded');
    }
}

function showRewarded() {
    currentAdvertisementIsRewarded = true;

    if (!platformSdk) {
        emit('rewardedStateChanged', 'failed');
        return;
    }

    platformSdk.showAd('rewarded').catch(() => {
        emit('rewardedStateChanged', 'failed');
    });
}
```

### Banner

Display banners are rendered into a DOM container whose id is passed to `gdsdk.showAd('display', { containerId })`. The example below uses the fixed id `'banner-container'`.

```js
const BANNER_CONTAINER_ID = 'banner-container';

function createBannerContainer(position) {
    const container = document.createElement('div');
    container.id = BANNER_CONTAINER_ID;
    container.style.position = 'fixed';
    container.style.left = '0';
    container.style.right = '0';
    container.style.zIndex = '9999';

    if (position === 'top') {
        container.style.top = '0';
    } else {
        container.style.bottom = '0';
    }

    document.body.appendChild(container);
    return container;
}

function showBanner(position) {
    let container = document.getElementById(BANNER_CONTAINER_ID);
    if (!container) {
        container = createBannerContainer(position);
    }

    container.style.display = 'block';

    platformSdk
        .showAd('display', { containerId: BANNER_CONTAINER_ID })
        .then(() => {
            emit('bannerStateChanged', 'shown');
        })
        .catch(() => {
            emit('bannerStateChanged', 'failed');
            container.style.display = 'none';
        });
}

function hideBanner() {
    const container = document.getElementById(BANNER_CONTAINER_ID);
    if (container) {
        container.style.display = 'none';
    }

    emit('bannerStateChanged', 'hidden');
}
```

`position` accepts `'top'` or `'bottom'`. Hiding a banner only toggles container visibility — it does not destroy the ad slot.

## Lifecycle / Audio / Pause

GameDistribution drives game pause/resume through the same `SDK_GAME_PAUSE` and `SDK_GAME_START` events that wrap every ad. There is no separate visibility or audio API — you derive both from these events:

- On `SDK_GAME_PAUSE`: pause gameplay, mute or duck audio.
- On `SDK_GAME_START`: resume gameplay, restore audio. This event also fires once after `SDK_READY` if no ad was served.

Combine this with the standard browser visibility events for tab-switch handling, since GameDistribution does not surface those itself:

```js
document.addEventListener('visibilitychange', () => {
    const isHidden = document.visibilityState === 'hidden';
    emit('pauseStateChanged', isHidden);
    emit('audioStateChanged', !isHidden);
});

window.addEventListener('blur', () => {
    emit('pauseStateChanged', true);
    emit('audioStateChanged', false);
});

window.addEventListener('focus', () => {
    emit('pauseStateChanged', false);
    emit('audioStateChanged', true);
});
```

## Storage

GameDistribution does not provide a platform storage API. Use `window.localStorage` directly for persisting player progress.
