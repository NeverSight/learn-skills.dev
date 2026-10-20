---
name: youtube-playables-js-sdk
description: Use this skill to initialize and integrate the YouTube Playables JavaScript SDK into an HTML5 game. Covers SDK bootstrapping, game lifecycle signaling, persistent save data management, interstitial and rewarded ads, leaderboard score submission, player language detection, and audio/pause lifecycle hooks. Use when the user asks about YouTube Playables, building or embedding games for YouTube, the YT game SDK, YT Playables integration, or making an interactive playable game on YouTube.
---

# YouTube Playables JavaScript SDK

## Installation

The `ytgame` global is injected by the YouTube host — there is nothing to install. Poll until it appears, then resolve:

```js
function waitForYtgame(timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
        if (window.ytgame) {
            resolve(window.ytgame);
            return;
        }

        const deadline = Date.now() + timeoutMs;
        const intervalId = setInterval(() => {
            if (window.ytgame) {
                clearInterval(intervalId);
                resolve(window.ytgame);
            } else if (Date.now() >= deadline) {
                clearInterval(intervalId);
                reject(new Error('ytgame SDK not available — running outside YouTube Playables?'));
            }
        }, 100);
    });
}
```

## Initialization

Sequence: wait for `ytgame` → read language + load saved data in parallel → call `firstFrameReady()` → call `gameReady()` once fully interactive.

```js
let ytgame = null;
let platformLanguage = 'en';
let savedData = {};

waitForYtgame()
    .then((sdk) => {
        ytgame = sdk;

        const getLanguagePromise = ytgame.system.getLanguage().then((language) => {
            platformLanguage = language.length > 2 ? language.slice(0, 2) : language;
        });

        const getDataPromise = ytgame.game.loadData().then((data) => {
            if (typeof data === 'string' && data !== '') {
                try {
                    savedData = JSON.parse(data);
                } catch (e) {
                    console.error('Failed to parse saved data, starting fresh', e);
                    savedData = {};
                }
            }
        });

        ytgame.system.onAudioEnabledChange((isEnabled) => {
            // Mute or unmute the game audio based on isEnabled
        });

        ytgame.system.onPause(() => {
            // Pause the game loop and audio
        });

        ytgame.system.onResume(() => {
            // Resume the game loop and audio
        });

        return Promise.all([getLanguagePromise, getDataPromise]);
    })
    .then(() => {
        ytgame.game.firstFrameReady();
    })
    .catch((err) => {
        console.error('YouTube Playables SDK initialization failed', err);
        // Fall back to a non-Playables code path if needed
    });
```

When the game is fully interactive:

```js
function notifyGameReady() {
    ytgame.game.gameReady();
}
```

## Storage (saved data)

Saved data is a single JSON-serializable blob per player. Always read → merge → write to avoid clobbering unrelated keys. After writing, re-read to confirm persistence.

```js
// Read one or many keys from saved data
function getDataFromStorage(key, tryParseJson) {
    return ytgame.game.loadData().then((data) => {
        if (typeof data === 'string' && data !== '') {
            try {
                savedData = JSON.parse(data);
            } catch (e) {
                console.error('loadData parse error', e);
            }
        }

        const readOne = (k) => {
            let value = typeof savedData[k] === 'undefined' ? null : savedData[k];
            if (typeof value === 'string' && tryParseJson) {
                try {
                    value = JSON.parse(value);
                } catch (e) {
                    /* keep as-is */
                }
            }
            return value;
        };

        return Array.isArray(key) ? key.map(readOne) : readOne(key);
    });
}

// Write one or many keys, then verify by reloading
function setDataToStorage(key, value) {
    const data = savedData !== null ? { ...savedData } : {};

    if (Array.isArray(key)) {
        for (let i = 0; i < key.length; i++) data[key[i]] = value[i];
    } else {
        data[key] = value;
    }

    return ytgame.game
        .saveData(JSON.stringify(data))
        .then(() => {
            savedData = data;
            return ytgame.game.loadData();
        })
        .then((persisted) => {
            if (persisted !== JSON.stringify(data)) {
                console.warn(
                    'saveData verification mismatch — persisted value differs from written value'
                );
            }
        })
        .catch((err) => {
            console.error('saveData failed', err);
        });
}

// Delete one or many keys
function deleteDataFromStorage(key) {
    const data = savedData !== null ? { ...savedData } : {};

    if (Array.isArray(key)) {
        for (const k of key) delete data[k];
    } else {
        delete data[key];
    }

    return ytgame.game
        .saveData(JSON.stringify(data))
        .then(() => {
            savedData = data;
        })
        .catch((err) => {
            console.error('deleteData (saveData) failed', err);
        });
}
```

## Advertisement

### Interstitial

`ytgame.ads.requestInterstitialAd()` resolves when the ad flow ends. Pause before requesting; resume after resolution or rejection.

```js
function showInterstitial() {
    // Pause game and mute audio before requesting
    ytgame.ads
        .requestInterstitialAd()
        .then(() => {
            // Resume game and unmute audio
        })
        .catch(() => {
            // Ad failed to deliver — resume game and continue
        });
}
```

### Rewarded

`ytgame.ads.requestRewardedAd(placement)` resolves with a boolean. Grant the reward only when the resolved value is truthy.

```js
function showRewarded(placement) {
    // Pause game and mute audio before requesting
    ytgame.ads
        .requestRewardedAd(placement)
        .then((isRewardEarned) => {
            if (isRewardEarned) {
                // Grant reward to the player
            }
            // Resume game and unmute audio
        })
        .catch(() => {
            // Ad failed to deliver — resume game and continue
        });
}
```

## Leaderboards

Submit integer scores via `ytgame.engagement.sendScore({ value })`. Coerce strings to integers before sending.

```js
function submitScore(score) {
    const value = typeof score === 'string' ? parseInt(score, 10) : score;
    return ytgame.engagement.sendScore({ value });
}
```
