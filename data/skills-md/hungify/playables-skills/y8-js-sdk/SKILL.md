---
name: y8-js-sdk
description: Integrates the Y8 JavaScript SDK into JavaScript and HTML5 games. Covers SDK loading and initialization handshake, player authentication via Y8 login, cloud-backed user data storage, interstitial and rewarded ads through Google AdSense, native achievement unlocking and listing, and in-game leaderboard score submission and retrieval. Use when the user mentions Y8 SDK, Y8 API, Y8 integration, Y8 leaderboard, Y8 achievements, Y8 login, or adding Y8 features to a JavaScript or HTML5 game.
---

# Y8 JavaScript SDK

## Integration Workflow

Follow these steps in order. Each step includes a validation checkpoint before proceeding.

1. **Load the SDK** — inject the script and poll for `window.ID`.
    - ✓ Verify: `typeof window.ID !== 'undefined'`
2. **Subscribe to `id.init`** before calling `ID.init({ appId })`.
    - ✓ Verify: the `id.init` callback fires; if it never fires, check the `appId`.
3. **Fetch login status** inside `id.init` to populate the player profile.
    - ✓ Verify: `data.status === 'ok'` means the player is signed in.
4. **Load AdSense** in parallel with login status inside `id.init`.
    - ✓ Verify: `adsbygoogle` script loads and `onReady` fires.
5. **Gate storage, achievements, and leaderboards** on `profile.isAuthorized === true`.
    - ✓ Verify before each API call: player is authorized or prompt login first.
6. **Invalidate `cachedUserData`** (set to `null`) after a successful `ID.login` call so the new session reads its own cloud state.

## Installation

```javascript
const SDK_URL = 'https://cdn.y8.com/api/sdk.js';

function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load ' + src));
        document.head.appendChild(script);
    });
}

function waitFor(globalName, timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
        const started = Date.now();
        const tick = () => {
            if (typeof window[globalName] !== 'undefined') {
                resolve(window[globalName]);
                return;
            }
            if (Date.now() - started > timeoutMs) {
                reject(new Error(globalName + ' is not available'));
                return;
            }
            setTimeout(tick, 50);
        };
        tick();
    });
}
```

## Initialization

Subscribe to `id.init` first, then call `ID.init({ appId })`. The `appId` (a.k.a. Game API Key) is issued by Y8 when you register the game. Once `id.init` fires, fetch login status and load AdSense in parallel.

```javascript
async function initY8({ gameId, adSenseId, channelId }) {
    if (!gameId) {
        throw new Error('gameId (Y8 appId) is required');
    }

    await loadScript(SDK_URL);
    const sdk = await waitFor('ID'); // ✓ checkpoint: window.ID exists

    return new Promise((resolve, reject) => {
        sdk.Event.subscribe('id.init', () => {
            // ✓ checkpoint: id.init fired — SDK is ready
            loadAdsByGoogle({ adSenseId, channelId })
                .then((showAd) => {
                    sdk.getLoginStatus((data) => {
                        const profile = readPlayerInfo(data);
                        resolve({ sdk, showAd, profile });
                    });
                })
                .catch(reject);
        });

        sdk.init({
            appId: gameId
        });
    });
}
```

## Player / Authorization

`ID.getLoginStatus(callback)` returns the current session without prompting. `ID.login(callback)` opens Y8's login dialog. Both deliver the same payload shape.

```javascript
function readPlayerInfo(data) {
    const profile = {
        isAuthorized: false,
        id: null,
        name: null,
        locale: null,
        photos: []
    };

    if (!data || data.status !== 'ok') {
        return profile;
    }

    const details = data.authResponse.details;
    const { pid, locale, nickname, first_name: firstName, last_name: lastName, avatars } = details;

    profile.isAuthorized = true;
    profile.id = pid || null;
    profile.locale = locale || null;
    profile.name = [firstName, lastName].filter((x) => !!x).join(' ') || nickname || null;

    const { thumb_url: photoSmall, medium_url: photoMedium, large_url: photoLarge } = avatars || {};

    if (photoSmall) profile.photos.push(photoSmall);
    if (photoMedium) profile.photos.push(photoMedium);
    if (photoLarge) profile.photos.push(photoLarge);

    return profile;
}

function authorizePlayer(sdk) {
    return new Promise((resolve, reject) => {
        sdk.login((response) => {
            const profile = readPlayerInfo(response);
            if (response && response.status === 'ok') {
                resolve(profile);
            } else {
                reject(new Error('Y8 login was cancelled or failed'));
            }
        });
    });
}
```

## Storage

Cloud-backed user data is accessed through `ID.api()`. Store all game data as a single JSON blob under one key — read once, mutate locally, write back.

> **After login:** set `cachedUserData = null` so the newly authorized player reads their own cloud state.

```javascript
const USERDATA_KEY = 'userData';
const NOT_FOUND_ERROR = 'Key not found';

let cachedUserData = null;

function loadUserData(sdk) {
    return new Promise((resolve, reject) => {
        if (cachedUserData) {
            resolve(cachedUserData);
            return;
        }

        sdk.api('user_data/retrieve', 'POST', { key: USERDATA_KEY }, (response) => {
            if (response.error && response.error !== NOT_FOUND_ERROR) {
                reject(response);
                return;
            }

            let userData = {};
            try {
                if (response.jsondata) {
                    userData = JSON.parse(response.jsondata);
                }
            } catch (e) {
                // Leave userData as an empty object on parse failure
            }

            cachedUserData = userData;
            resolve(userData);
        });
    });
}

function saveUserData(sdk, userData) {
    return new Promise((resolve, reject) => {
        const payload = { key: USERDATA_KEY, value: JSON.stringify(userData) };
        sdk.api('user_data/submit', 'POST', payload, (response) => {
            if (response.status === 'ok') {
                cachedUserData = userData;
                resolve();
            } else {
                reject(response);
            }
        });
    });
}

function getStorageValue(sdk, key) {
    return loadUserData(sdk).then((userData) => userData[key] ?? null);
}

function setStorageValue(sdk, key, value) {
    return loadUserData(sdk).then((userData) => {
        const next = { ...userData, [key]: value };
        return saveUserData(sdk, next);
    });
}

function deleteStorageValue(sdk, key) {
    return loadUserData(sdk).then((userData) => {
        const next = { ...userData };
        delete next[key];
        return saveUserData(sdk, next);
    });
}
```

## Advertisement

`adsbygoogle.push` exposes an `adBreak` API with `type: 'start'` for interstitials and `type: 'reward'` for rewarded ads. Use `data-ad-channel` if Y8 provided a channel id, otherwise fall back to your AdSense client id.

```javascript
const ADS_ID = '6129580795478709';

function loadAdsByGoogle({ adSenseId, channelId }) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';
        script.setAttribute('crossorigin', 'anonymous');
        script.setAttribute('data-ad-frequency-hint', '180s');

        script.setAttribute('data-ad-client', channelId ? `ca-pub-${ADS_ID}` : adSenseId);
        if (channelId) {
            script.setAttribute('data-ad-channel', channelId);
        } else {
            script.setAttribute('data-ad-host', `ca-host-pub-${ADS_ID}`);
        }

        script.addEventListener('load', () => {
            window.adsbygoogle = window.adsbygoogle || [];
            window.adsbygoogle.push({
                preloadAdBreaks: 'on',
                sound: 'on',
                onReady: () => {}
            });
            resolve((adOptions) => window.adsbygoogle.push(adOptions));
        });

        script.addEventListener('error', () => reject(new Error('adsbygoogle failed to load')));
        document.head.appendChild(script);
    });
}
```

### Interstitial

```javascript
function showInterstitial(showAd, { onOpened, onClosed, onFailed } = {}) {
    if (!showAd) {
        onFailed?.('ads_not_ready');
        return;
    }

    showAd({
        type: 'start',
        name: 'start-game',
        beforeAd: () => {
            onOpened?.();
        },
        afterAd: () => {
            onClosed?.();
        },
        adBreakDone: (placementInfo) => {
            if (placementInfo.breakStatus !== 'viewed') {
                onFailed?.(placementInfo.breakStatus);
            }
        }
    });
}
```

### Rewarded

`beforeReward(showAdFn)` gates the ad — call `showAdFn(0)` to display it. `adViewed` fires when the player completes the ad; `adDismissed` means they exited early.

```javascript
function showRewarded(showAd, { onOpened, onRewarded, onClosed, onFailed } = {}) {
    if (!showAd) {
        onFailed?.('ads_not_ready');
        return;
    }

    showAd({
        type: 'reward',
        name: 'rewarded Ad',
        beforeAd: () => {
            onOpened?.();
        },
        afterAd: () => {
            onClosed?.();
        },
        beforeReward: (showAdFn) => {
            showAdFn(0);
        },
        adDismissed: () => {
            onFailed?.('dismissed');
        },
        adViewed: () => {
            onRewarded?.();
        },
        adBreakDone: (placementInfo) => {
            if (
                placementInfo.breakStatus === 'frequencyCapped' ||
                placementInfo.breakStatus === 'other'
            ) {
                onFailed?.(placementInfo.breakStatus);
            }
        }
    });
}
```

## Achievements

Y8 native achievements live under `ID.GameAPI.Achievements`. Both `achievement` (display name) and `achievementkey` (stable id) are required.

### Unlock

```javascript
function unlockAchievement(sdk, options) {
    if (!options || !options.achievement || !options.achievementkey) {
        return Promise.reject(new Error('achievement and achievementkey are required'));
    }

    return new Promise((resolve) => {
        sdk.GameAPI.Achievements.save(options, (data) => {
            resolve(data);
        });
    });
}
```

### List achievements (custom query)

`listCustom` returns achievements with a nested `player` object. Flatten it for easier consumption.

```javascript
function getAchievementsList(sdk, options = {}) {
    return new Promise((resolve, reject) => {
        sdk.GameAPI.Achievements.listCustom(options, (data) => {
            if (!data.success) {
                reject(new Error(data.errorcode));
                return;
            }

            const list = data.achievements.map(({ player, ...achievement }) => ({
                ...achievement,
                playerid: player.playerid,
                playername: player.playername,
                lastupdated: player.lastupdated,
                date: player.date,
                rdate: player.rdate
            }));
            resolve(list);
        });
    });
}
```

### Native popup

`ID.GameAPI.Achievements.list(options)` opens Y8's built-in achievements UI and returns nothing.

```javascript
function showAchievementsPopup(sdk, options = {}) {
    sdk.GameAPI.Achievements.list(options);
}
```

## Leaderboards

Each board is identified by a string `table` id configured in the Y8 dashboard.

### Submit a score

```javascript
function submitScore(sdk, tableId, score) {
    return new Promise((resolve, reject) => {
        const options = {
            table: tableId,
            points: score
        };

        sdk.GameAPI.Leaderboards.save(options, ({ success, errormessage }) => {
            if (success) {
                resolve();
            } else {
                reject(new Error(errormessage || 'leaderboard_save_failed'));
            }
        });
    });
}
```

### Fetch entries

Valid `mode` values: `'alltime'` (default), `'daily'`, `'weekly'`, `'monthly'`.

```javascript
function getLeaderboardEntries(sdk, tableId) {
    return new Promise((resolve, reject) => {
        const options = {
            table: tableId,
            mode: 'alltime'
        };

        sdk.GameAPI.Leaderboards.listCustom(options, ({ scores, success, errormessage }) => {
            if (!success) {
                reject(new Error(errormessage || 'leaderboard_list_failed'));
                return;
            }

            const entries = scores.map((entry) => ({
                id: entry.playerid,
                name: entry.playername,
                score: entry.points,
                rank: entry.rank,
                photo: null
            }));
            resolve(entries);
        });
    });
}
```
