---
name: lagged-js-sdk
description: Use when integrating the Lagged JavaScript SDK into an HTML5 game published on Lagged.com, adding Lagged leaderboards, handling Lagged ad placements, or setting up user authentication via the Lagged API. Initializes the Lagged SDK (window.LaggedAPI), retrieves player profile data, submits scores to native leaderboards, unlocks achievements, and integrates interstitial and rewarded ads for games on the Lagged.com game portal.
---

# Lagged JavaScript SDK

`window.LaggedAPI` is exposed after its loader script finishes. Initialization, player lookup, ads, leaderboards and achievements all hang off `LaggedAPI`.

## Overview

Supported features: initialization handshake, player profile lookup, interstitial ads, rewarded ads, leaderboard score submission, and achievement unlocks.

## Integration Checklist

1. **Load SDK** — inject `lagged.js` and wait for `window.LaggedAPI`
2. **Init with credentials** — call `sdk.init(devId, publisherId)` with ids from the Lagged dashboard
3. **Check player auth** — call `sdk.User.get`; `id > 0` means signed-in, `id = 0` means guest
4. **Wire ads at scene transitions** — show interstitials between levels; gate rewarded ads on player action
5. **Submit scores on game over** — call `sdk.Scores.save` with the board id and final score
6. **Unlock achievements** — call `sdk.Achievements.save` when criteria are met

## Installation

The SDK URL is `https://lagged.com/api/rev-share/lagged.js`. Dynamically inject the script tag, then poll for `window.LaggedAPI` before proceeding.

```javascript
const SDK_URL = 'https://lagged.com/api/rev-share/lagged.js';

async function loadLaggedSDK(timeoutMs = 10000) {
    await new Promise((resolve, reject) => {
        const s = Object.assign(document.createElement('script'), {
            src: SDK_URL,
            async: true,
            onload: resolve,
            onerror: () => reject(new Error('Failed to load Lagged SDK'))
        });
        document.head.appendChild(s);
    });
    const started = Date.now();
    while (typeof window.LaggedAPI === 'undefined') {
        if (Date.now() - started > timeoutMs)
            throw new Error('LaggedAPI did not appear within ' + timeoutMs + 'ms');
        await new Promise((r) => setTimeout(r, 50));
    }
    return window.LaggedAPI;
}
```

## Initialization

`LaggedAPI.init` requires both a developer id and a publisher id from the Lagged dashboard. Right after `init`, query the current player to read their id, name and avatar.

Wrap `initLagged` in a try/catch at the call site — on failure, disable leaderboard, achievement and ad calls so the game remains playable without SDK support.

```javascript
async function initLagged(devId, publisherId) {
    if (!devId || !publisherId) throw new Error('devId and publisherId are required');

    const sdk = await loadLaggedSDK();
    sdk.init(devId, publisherId);

    const player = await new Promise((resolve) => {
        sdk.User.get((response) => {
            resolve(response && response.user ? response.user : {});
        });
    });

    // id > 0 = signed-in player; id = 0 = guest
    const profile = {
        isAuthorized: player.id > 0,
        id: player.id || null,
        name: player.name || null,
        avatar: player.avatar || null
    };

    console.debug('[Lagged] init complete', profile);
    return { sdk, profile };
}
```

## Player

Player data is read once during initialization via `LaggedAPI.User.get(callback)`. The callback receives `{ user: { id, name, avatar } }`. The full retrieval logic is demonstrated in the `initLagged` function above. If you need a guest fallback, generate a local id and persist it in `localStorage`.

## Advertisement

### Interstitial

`LaggedAPI.APIAds.show(onClosed)` displays an interstitial. Pause simulation and mute audio before the call; resume in `onClosed`.

```javascript
function showInterstitial(sdk, { onOpened, onClosed } = {}) {
    onOpened?.();
    sdk.APIAds.show(() => {
        onClosed?.();
    });
}
```

### Rewarded

`LaggedAPI.GEvents.reward(canShowReward, rewardSuccess)` runs a two-phase rewarded ad:

1. `canShowReward(success, showAdFn)` — if `success` is `true`, call `showAdFn()` to display the ad; otherwise surface a fallback.
2. `rewardSuccess(success)` — `true` means the player earned the reward; `false` means dismissed early or failed.

```javascript
function showRewarded(sdk, { onOpened, onRewarded, onClosed, onFailed } = {}) {
    onOpened?.();
    sdk.GEvents.reward(
        (success, showAdFn) => {
            if (success) showAdFn();
            else onFailed?.('unavailable');
        },
        (success) => {
            if (success) {
                onRewarded?.();
                onClosed?.();
            } else onFailed?.('not_completed');
        }
    );
}
```

## Leaderboards

Each board is identified by a string id configured on the Lagged dashboard. There is no API to fetch entries or open a native popup.

```javascript
function submitScore(sdk, boardId, score) {
    return new Promise((resolve, reject) => {
        sdk.Scores.save({ score, board: boardId }, (response) => {
            if (response && response.success) resolve(response);
            else reject((response && response.errormsg) || 'leaderboard_failed');
        });
    });
}
```

## Achievements

`LaggedAPI.Achievements.save(achievements, callback)` unlocks one or many achievements in a single call. Display state is owned by Lagged — there is no list/get API.

```javascript
function unlockAchievement(sdk, achievement) {
    if (!achievement) return Promise.reject(new Error('achievement is required'));
    return new Promise((resolve, reject) => {
        const payload = Array.isArray(achievement) ? achievement : [achievement];
        sdk.Achievements.save(payload, (response) => {
            if (response && response.success) resolve(response);
            else reject((response && response.errormsg) || 'achievement_failed');
        });
    });
}
```
