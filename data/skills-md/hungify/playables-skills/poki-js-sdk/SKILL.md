---
name: poki-js-sdk
description: Integrates the Poki JavaScript SDK (PokiSDK) into JavaScript browser games. Initializes PokiSDK, configures interstitial and rewarded ad breaks (commercialBreak, rewardedBreak), manages gameplay lifecycle events (gameplayStart, gameplayStop), and sets up loading progress tracking (gameLoadingFinished). Use when the user mentions Poki, PokiSDK, web game monetization, game portal integration, ad breaks in browser games, or distributing an HTML5 game on the Poki platform.
---

# Poki JavaScript SDK

## Integration Workflow

1. **Add the SDK script** — embed or dynamically inject the Poki script tag.
2. **Initialize** — call `PokiSDK.init()` and resolve `gameLoadingFinished` when the game is ready.
3. **Verify init** — check the browser console for Poki SDK handshake messages; use the Poki Inspector dev tool to confirm the session started.
4. **Add lifecycle hooks** — call `gameplayStart` / `gameplayStop` around every play session.
5. **Add ad breaks** — insert `commercialBreak` at natural pause points; add `rewardedBreak` where the player can opt in.
6. **Test in Poki Inspector** — open `https://inspector.poki.io`, load your game URL, and trigger each ad break to confirm the flow.

## Installation

Add the official Poki SDK script to your page:

```html
<script src="https://game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>
```

Or inject it dynamically:

```js
function loadPokiSdk() {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://game-cdn.poki.com/scripts/v2/poki-sdk.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}
```

## Initialization

```js
loadPokiSdk()
    .then(() => window.PokiSDK.init())
    .then(() => {
        // SDK is ready
        window.PokiSDK.gameLoadingFinished();
    })
    .catch(() => {
        // SDK init failed - continue without Poki integration
        window.PokiSDK && window.PokiSDK.gameLoadingFinished();
    });
```

Call `gameLoadingFinished` when the game is ready for the player. If your loader has discrete phases, bracket them with `gameLoadingStart` and `gameLoadingFinished`.

## Advertisement

### Interstitial

Use the `isOpened` flag to detect whether an ad was actually delivered — the callback is not invoked when no ad is shown.

```js
function showInterstitial() {
    let isOpened = false;

    window.PokiSDK.commercialBreak(() => {
        isOpened = true;
        // Pause game, mute audio
    })
        .then(() => {
            if (isOpened) {
                // Resume game, unmute audio
            } else {
                // Ad was not shown
            }
        })
        .catch(() => {
            // Ad request failed
        });
}
```

### Rewarded

`rewardedBreak` resolves with a boolean — grant the reward only when both `isOpened` is true and the resolved value is truthy.

```js
function showRewarded() {
    let isOpened = false;

    window.PokiSDK.rewardedBreak(() => {
        isOpened = true;
        // Pause game, mute audio
    })
        .then((success) => {
            if (isOpened) {
                if (success) {
                    // Grant reward to the player
                }
                // Resume game, unmute audio
            } else {
                // Ad was not shown
            }
        })
        .catch(() => {
            // Ad request failed
        });
}
```

## Lifecycle

Call `gameplayStart` when the player gains control (level start, level resume) and `gameplayStop` when control is taken away (level paused, completed, failed, or returning to a menu). Pair every `gameplayStart` with a matching `gameplayStop`.

```js
function onLevelStart() {
    window.PokiSDK.gameplayStart();
}

function onLevelEnd() {
    window.PokiSDK.gameplayStop();
}
```

## Testing & Verification

- Open **Poki Inspector** at `https://inspector.poki.io` and load your game URL to get a developer session.
- The browser console will print Poki SDK handshake and event messages — confirm `init` resolves and `gameLoadingFinished` is acknowledged.
- Trigger `commercialBreak` and `rewardedBreak` via the Inspector UI to simulate ad delivery and verify pause/resume logic fires correctly.
- Confirm `gameplayStart` and `gameplayStop` events appear in the Inspector timeline at the correct moments.

---

Notes on omitted features: this skill does not cover server time, ad-block detection, `happyTime`, or `gameInteractive`; keep the implementation focused on the Poki SDK features listed above.
