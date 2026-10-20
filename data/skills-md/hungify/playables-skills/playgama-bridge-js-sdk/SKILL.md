---
name: playgama-bridge-js-sdk
description: Complete reference for integrating the Playgama Bridge JS SDK into HTML5 games. Use when working with cross-platform publishing, ads, IAP, leaderboards, achievements, storage, social features, or remote config via the JS SDK.
---

# Playgama Bridge JS SDK

Playgama Bridge is a unified JS SDK that lets a single HTML5 build run on 20+ platforms (Playgama, Yandex Games, Crazy Games, Facebook Gaming, YouTube Playables, Telegram, Poki, Y8, Lagged, MSN, Microsoft Store, Discord, GameSnacks, Xiaomi, Huawei, JioGames, BitQuest, Reddit, Game Distribution, Playhop, Aha Games, etc.).

When the game runs on a supported platform, Bridge auto-loads that platform's native scripts and routes API calls to it. In unsupported environments (local dev, unknown hosts) Bridge uses a `mock` platform that returns safe defaults (`false`, `reject`, etc.) instead of throwing — the same code works everywhere.

The JS SDK (JS Core) is the foundation; engine packages (Unity, Godot, Construct, GDevelop, GameMaker, Defold, Cocos Creator, Scratch) are thin wrappers. Use JS Core directly for web engines such as PlayCanvas, Phaser, LayaAir, Three.js, Babylon.js.

## Installation

Add the script tag to the `<head>` of your `index.html` before any game code:

```html
<html>
    <head>
        <script src="https://bridge.playgama.com/v1/stable/playgama-bridge.js"></script>
    </head>
    <body>
        ...
    </body>
</html>
```

CDN options:

| URL                                                        | When to use                           |
| ---------------------------------------------------------- | ------------------------------------- |
| `https://bridge.playgama.com/v1/stable/playgama-bridge.js` | **Recommended.** Latest stable v1.x.x |
| `https://bridge.playgama.com/latest/playgama-bridge.js`    | Bleeding edge — for testing only      |
| `https://bridge.playgama.com/v1.27.0/playgama-bridge.js`   | Pin a specific version                |

The SDK exposes a global `bridge` object after the script loads.

## Configuration file

Bridge reads `playgama-bridge-config.json` from the build root. It declares platform IDs, IAP catalog, ad placements, leaderboards and other settings. Generate or edit it with the [config editor](https://playgama.github.io/bridge-config-editor/).

Skeleton:

```json
{
    "platforms": {
        "playgama": { "options": {} },
        "yandex": { "options": {} }
    },
    "advertisement": {
        "interstitial": { "minimumDelay": 60 },
        "advancedBanners": {/* see Advanced Banners */}
    },
    "payments": [
        {
            "id": "coins_100",
            "playgama": { "amount": 1 },
            "playdeck": { "amount": 1, "description": "100 Coins" }
        }
    ],
    "leaderboards": [{ "id": "high_score" }]
}
```

## Initialization

Call `bridge.initialize()` and **wait for the promise** before touching any other API.

```javascript
bridge
    .initialize()
    .then(() => {
        // SDK is ready, all bridge.* APIs are usable now
    })
    .catch((error) => {
        // Initialization failed — handle gracefully (the SDK still falls back to mock)
    });
```

After init, send `game_ready` once the game is fully loaded and the player can interact:

```javascript
bridge.platform.sendMessage('game_ready');
```

This dismisses the platform loader. **It is required** — without it most platforms keep showing their splash on top of the game.

## Required integration checklist

For every game:

1. Install SDK + create `playgama-bridge-config.json`.
2. Wait for `bridge.initialize()`.
3. Read `bridge.platform.language` and apply localization.
4. Load saved progress with `bridge.storage.get(...)`.
5. Send `bridge.platform.sendMessage('game_ready')` once the first playable frame is rendered.
6. React to `AUDIO_STATE_CHANGED` and `PAUSE_STATE_CHANGED` events.
7. Show **interstitial ads** at natural breakpoints (level transitions, game over, menu↔gameplay).

Interstitials are mandatory for revenue share. Without them games can be rejected during moderation.

## Platform module — `bridge.platform`

### Properties

| Property                                 | Type           | Description                                                                                                                                                                                                                                                                                         |
| ---------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bridge.platform.id`                     | string         | Current platform ID. One of: `playgama`, `vk`, `ok`, `yandex`, `facebook`, `crazy_games`, `game_distribution`, `playdeck`, `telegram`, `y8`, `lagged`, `msn`, `microsoft_store`, `poki`, `qa_tool`, `discord`, `gamepush`, `bitquest`, `huawei`, `jio_games`, `reddit`, `youtube`, `mock`, `xiaomi` |
| `bridge.platform.sdk`                    | object \| null | Native platform SDK (when Bridge exposes it). Use only for things Bridge doesn't wrap                                                                                                                                                                                                               |
| `bridge.platform.language`               | string         | ISO 639-1 user language (`en`, `ru`, ...). Falls back to browser language                                                                                                                                                                                                                           |
| `bridge.platform.payload`                | string \| null | URL launch payload (referral code, deep link). Format is platform-specific                                                                                                                                                                                                                          |
| `bridge.platform.tld`                    | string \| null | Top-level domain (`com`, `ru`, ...) when host provides it                                                                                                                                                                                                                                           |
| `bridge.platform.isAudioEnabled`         | boolean        | Whether the host platform currently allows game audio                                                                                                                                                                                                                                               |
| `bridge.platform.isGetAllGamesSupported` | boolean        | Capability flag for `getAllGames()`                                                                                                                                                                                                                                                                 |
| `bridge.platform.isGetGameByIdSupported` | boolean        | Capability flag for `getGameById()`                                                                                                                                                                                                                                                                 |

### Methods

```javascript
// Server time — UTC ms — use for daily rewards / cooldowns instead of local clock
bridge.platform
    .getServerTime()
    .then((utcMs) => console.log(utcMs))
    .catch((error) => {});

// All games by the same developer (for "More games" screens)
bridge.platform.getAllGames().then((games) => {
    // platform-specific shape, on yandex: { appID, title, url, coverURL, iconURL }
});

// One game by ID (cross-promotion)
bridge.platform.getGameById({ gameId: '111111' }).then((game) => {
    // { appID, title, url, coverURL, iconURL, isAvailable }
});

// Lifecycle messages — see table below
bridge.platform.sendMessage('game_ready');

// Custom messages — used by Advanced Banners config
bridge.platform.sendCustomMessage('shop_opened');
```

### Built-in lifecycle messages

| Message                   | Payload                       | When to send                                                         |
| ------------------------- | ----------------------------- | -------------------------------------------------------------------- |
| `game_ready`              | —                             | Game loaded, loading screen done, player can interact (**required**) |
| `in_game_loading_started` | —                             | Sub-loading begins (e.g. level load)                                 |
| `in_game_loading_stopped` | —                             | Sub-loading finished                                                 |
| `gameplay_started`        | —                             | Active gameplay begins                                               |
| `gameplay_stopped`        | —                             | Active gameplay ends (menu, pause, game over)                        |
| `player_got_achievement`  | —                             | Significant moment (boss defeated, record set)                       |
| `level_started`           | `{ world, level }` (optional) | Level begins                                                         |
| `level_completed`         | `{ world, level }`            | Level won                                                            |
| `level_failed`            | `{ world, level }`            | Level lost                                                           |
| `level_paused`            | `{ world, level }`            | Pause menu opened                                                    |
| `level_resumed`           | `{ world, level }`            | Resumed from pause                                                   |

These also trigger Advanced Banners placements automatically.

### Events

```javascript
// Audio mute/unmute requests from the host
bridge.platform.on(bridge.EVENT_NAME.AUDIO_STATE_CHANGED, (isEnabled) => {
    if (!isEnabled) muteGameAudio();
    else restoreGameAudio();
});

// Pause/resume requests (tab switch, platform overlay, etc.)
bridge.platform.on(bridge.EVENT_NAME.PAUSE_STATE_CHANGED, (isPaused) => {
    if (isPaused) pauseGame();
    else resumeGame();
});
```

Both events are **required** to handle — many platforms enforce this during moderation.

## Player module — `bridge.player`

Player identity and platform authorization.

| Property                                 | Type           | Description                                               |
| ---------------------------------------- | -------------- | --------------------------------------------------------- |
| `bridge.player.id`                       | string \| null | Platform player ID, only when authorized                  |
| `bridge.player.name`                     | string \| null | Display name from platform                                |
| `bridge.player.photos`                   | string[]       | Avatar URLs sorted by increasing resolution; `[]` if none |
| `bridge.player.extra`                    | object         | Platform-specific auth/verification data                  |
| `bridge.player.isAuthorizationSupported` | boolean        | Whether host supports a login flow                        |
| `bridge.player.isAuthorized`             | boolean        | Whether the player is currently authorized                |

```javascript
// Trigger only from a direct user action (button tap)
bridge.player
    .authorize({})
    .then(() => {
        // bridge.player.id, .name, .photos now populated
    })
    .catch((error) => {
        // Cancelled or failed
    });
```

Some platforms expose guest data even before authorization (`name`, partial `id`). Don't treat those as verified — only post-authorization data is trustworthy.

### Backend verification

Use `bridge.player.extra` to verify player identity from your server. Currently only `playgama`, `msn`, and `microsoft_store` are supported by Playgama's verification API:

```bash
curl -X POST 'https://playgama.com/api/bridge/v1/verify' \
  -H 'Content-Type: application/json' \
  -d '{"platform":"<PLATFORM_ID>","type":"authorization","data":{ <...bridge.player.extra> }}'

# Response: { success, errorMessage?, playerId?, publisherPlayerId? }
```

## Device module — `bridge.device`

```javascript
bridge.device.type; // 'mobile' | 'tablet' | 'desktop' | 'tv'
```

Use for broad UI adaptation — touch vs. keyboard input, asset quality, layout. Don't make business logic decisions on device type.

## Storage module — `bridge.storage`

Persistent player data (progress, settings, currency). **Almost every game needs this.**

### Two storage types

| Type                | Persistence            | Cross-device | When                                       |
| ------------------- | ---------------------- | ------------ | ------------------------------------------ |
| `local_storage`     | Browser localStorage   | No           | Default for offline single-device save     |
| `platform_internal` | Platform cloud servers | Yes          | Player is authorized + you want cloud sync |

```javascript
bridge.storage.defaultType;
// 'local_storage' or 'platform_internal' — host's preferred type

bridge.storage.isAvailable('local_storage');
bridge.storage.isAvailable('platform_internal');
// Check before forcing a specific type
```

### Load

```javascript
// Single key
bridge.storage.get('level').then((value) => {
    // value === null when key is missing — always have a default in your game state
});

// Multiple keys — returns array, same order
bridge.storage.get(['level', 'coins', 'settings']).then(([level, coins, settings]) => {});

// Force specific storage type (third arg)
bridge.storage.get('level', 'local_storage');
```

### Save

```javascript
bridge.storage.set('level', 'dungeon_3');

bridge.storage
    .set(['level', 'coins', 'tutorial_done'], ['dungeon_3', 42, true])
    .then(() => {
        /* persisted */
    })
    .catch((error) => {});

bridge.storage.set('level', 'dungeon_3', 'platform_internal');
```

Save on meaningful state change (level done, purchase, settings change). **Do not save every frame.**

### Delete

```javascript
bridge.storage.delete('level');
bridge.storage.delete(['level', 'coins']);
```

## Advertisement module — `bridge.advertisement`

`playgama-bridge-config.json` controls placements. **Never show ads during active gameplay** — only at natural pauses.

### Format overview

| Format           | Status       | When                                            |
| ---------------- | ------------ | ----------------------------------------------- |
| Interstitial     | **Required** | Level transitions, game over, menu↔gameplay     |
| Rewarded         | Recommended  | Player opts in for in-game reward               |
| Banner           | Recommended  | Idle screens (menu, lobby, pause)               |
| Advanced Banners | Recommended  | Custom multi-position responsive banner layouts |
| AdBlock check    | Optional     | Adapt UI when ads are blocked                   |

### Interstitial — required

```javascript
bridge.advertisement.isInterstitialSupported; // boolean

bridge.advertisement.minimumDelayBetweenInterstitial; // default 60 seconds
bridge.advertisement.setMinimumDelayBetweenInterstitial(30); // override

bridge.advertisement.interstitialState;
// 'loading' | 'opened' | 'closed' | 'failed'

bridge.advertisement.on(bridge.EVENT_NAME.INTERSTITIAL_STATE_CHANGED, (state) => {
    if (state === 'opened') {
        muteGameAudio();
        pauseGame();
    } else if (state === 'closed' || state === 'failed') {
        restoreGameAudio();
        resumeGame();
    }
});

// Optional placement string
bridge.advertisement.showInterstitial('level_complete');
```

**Do not** call `showInterstitial()` at game start — platforms that support a startup interstitial show it automatically. Calling it explicitly causes duplicate ads.

Also check `interstitialState` right after init: if it is already `opened`, mute and pause immediately.

### Rewarded

```javascript
bridge.advertisement.isRewardedSupported;

bridge.advertisement.rewardedState;
// 'loading' | 'opened' | 'closed' | 'rewarded' | 'failed'

bridge.advertisement.rewardedPlacement; // current placement string

bridge.advertisement.on(bridge.EVENT_NAME.REWARDED_STATE_CHANGED, (state) => {
    switch (state) {
        case 'opened':
            muteGameAudio();
            pauseGame();
            break;
        case 'rewarded':
            // ONLY here grant the reward
            grantReward(bridge.advertisement.rewardedPlacement);
            break;
        case 'closed':
        case 'failed':
            restoreGameAudio();
            resumeGame();
            break;
    }
});

bridge.advertisement.showRewarded('double_coins');
```

**Critical:** grant the reward only on the `rewarded` state. Granting on `closed` lets players claim rewards without watching the ad.

### Banner

```javascript
bridge.advertisement.isBannerSupported;

let position = 'bottom'; // 'top' | 'bottom', default 'bottom'
let placement = 'menu'; // optional
bridge.advertisement.showBanner(position, placement);

bridge.advertisement.hideBanner();

bridge.advertisement.bannerState;
// 'loading' | 'shown' | 'hidden' | 'failed'

bridge.advertisement.on(bridge.EVENT_NAME.BANNER_STATE_CHANGED, (state) => {});
```

### Advanced Banners

Multi-position, responsive banner layouts driven by config. Auto-hidden during interstitials/rewarded, auto-restored after. Re-evaluate on orientation/resize (200ms debounce).

```javascript
bridge.advertisement.isAdvancedBannersSupported;

// Method 1 — explicit
bridge.advertisement.showAdvancedBanners('main_menu');
bridge.advertisement.hideAdvancedBanners();

// Method 2 — automatic via platform messages (recommended)
bridge.platform.sendMessage('gameplay_stopped'); // shows if configured
bridge.platform.sendMessage('gameplay_started'); // hides if action: 'hide'
bridge.platform.sendCustomMessage('shop_opened');

// State
bridge.advertisement.advancedBannersState;
bridge.advertisement.on('advanced_banners_state_changed', (state) => {});
```

Config example:

```json
{
    "advertisement": {
        "advancedBanners": {
            "disable": false,
            "placementFallback": "main_menu",
            "main_menu": {
                "default": [{ "width": "20%", "height": "25%", "top": "10%", "right": "10%" }]
            },
            "gameplay_stopped": {
                "action": "show",
                "default": [{ "width": "20%", "height": "25%", "bottom": "10%", "right": "5%" }],
                "mobile:portrait": [
                    { "width": "100%", "height": "8%", "bottom": "0", "left": "0" }
                ],
                "desktop:landscape:w>1200": [
                    { "width": "10%", "height": "60%", "top": "10%", "left": "1%" },
                    { "width": "10%", "height": "60%", "top": "10%", "right": "1%" }
                ]
            },
            "gameplay_started": { "action": "hide" }
        }
    }
}
```

#### Condition keys

Colon-separated segments, all must match:

| Segment      | Examples                                     |
| ------------ | -------------------------------------------- |
| Device type  | `mobile`, `desktop`, `tablet`, `tv`          |
| Orientation  | `portrait`, `landscape`                      |
| Width        | `w>600`, `w<=1024`, `w>=768`                 |
| Height       | `h>400`, `h<=900`                            |
| Aspect ratio | `ar>1.5`, `ar>=1.78`, `ar<=1.0`              |
| Canvas mode  | `canvas` (use canvas size instead of window) |

Priority: device type +4, orientation +2, canvas +1, each w/h/ar condition +1. Ties broken by more segments → closer threshold to actual value. `default` is fallback (-1).

#### Banner object

CSS positioning: `width`, `height`, `top`, `bottom`, `left`, `right` — all strings (`"300px"`, `"100%"`, `"0"`).

### AdBlock detection

```javascript
bridge.advertisement.checkAdBlock().then((isBlocked) => {
    // true | false — informational only, doesn't suppress ads
});
```

## Payments module — `bridge.payments`

In-game purchases. Optional but often the highest-revenue feature.

### Product types

| Type       | Example             | Lifecycle                                                                                                                     |
| ---------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Permanent  | "Remove ads", DLC   | Bought once. Check ownership with `getPurchases()` on every launch                                                            |
| Consumable | Coins, gems, energy | Bought → granted → **must be consumed** with `consumePurchase(id)`. Until consumed, repeat purchases of the same product fail |

### API

```javascript
bridge.payments.isSupported;

// Catalog — localized prices, currencies, metadata
bridge.payments.getCatalog().then((items) => {
    items.forEach((item) => {
        console.log(item.id);
        console.log(item.price); // formatted string
        console.log(item.priceCurrencyCode); // ISO 4217
        console.log(item.priceValue); // numeric value
    });
});

// Purchase — only from a direct user action
bridge.payments
    .purchase('coins_100')
    .then((purchase) => {
        // Platform-specific shape, always has .id
        grantItems(purchase.id);
        // For consumables, immediately consume:
        return bridge.payments.consumePurchase(purchase.id);
    })
    .catch((error) => {
        // Cancelled or failed
    });

// Consume a consumable after granting items
bridge.payments.consumePurchase('coins_100').then((purchase) => {});

// Active purchases — call on every launch and after reconnect
// to recover items from purchases interrupted by disconnects
bridge.payments.getPurchases().then((purchases) => {
    purchases.forEach((p) => {
        // Permanent: check ownership here
        // Consumable: grant items + consume
    });
});
```

### Catalog config

```json
{
    "payments": [
        {
            "id": "coins_100",
            "playgama": { "amount": 1 },
            "playdeck": { "amount": 1, "description": "100 Coins" }
        }
    ]
}
```

`id` is your in-game identifier; per-platform keys carry platform-specific price/metadata.

### Backend verification

```bash
curl -X POST 'https://playgama.com/api/bridge/v1/verify' \
  -H 'Content-Type: application/json' \
  -d '{"platform":"<PLATFORM_ID>","type":"purchase","data":{ <...purchase> }}'

# Response: { success, errorMessage?, orderId?, productId?, externalId? }
```

Currently supports `playgama`, `msn`, `microsoft_store`.

## Leaderboards module — `bridge.leaderboards`

Optional. First check `bridge.leaderboards.type`:

| Type            | Action                                                          |
| --------------- | --------------------------------------------------------------- |
| `not_available` | Hide all leaderboard UI                                         |
| `in_game`       | Call `setScore(...)`, render your own UI from `getEntries(...)` |
| `native`        | Call `setScore(...)` only — platform renders the board          |
| `native_popup`  | Call `setScore(...)` and `showNativePopup(...)` to open overlay |

### API

```javascript
bridge.leaderboards.type;

bridge.leaderboards.setScore('high_score', 1000).then(() => {});

// Only when type === 'in_game'
bridge.leaderboards.getEntries('high_score').then((entries) => {
    entries.forEach((e) => {
        console.log(e.id);
        console.log(e.name);
        console.log(e.photo);
        console.log(e.score);
        console.log(e.rank);
    });
});

// Only when type === 'native_popup'
bridge.leaderboards.showNativePopup('high_score');
```

### Config

```json
{
    "leaderboards": [
        {
            "id": "high_score",
            "<PLATFORM_ID>": "<NATIVE_ID_FOR_PLATFORM>"
        }
    ]
}
```

Use the in-game `id` in code; per-platform overrides map to native leaderboard IDs when they differ.

## Achievements module — `bridge.achievements`

Optional. Achievement IDs are configured in **each platform's developer dashboard**, not in `playgama-bridge-config.json`.

```javascript
bridge.achievements.isSupported;
bridge.achievements.isGetListSupported;
bridge.achievements.isNativePopupSupported;

// Unlock — send each achievement only once
let options = {};
switch (bridge.platform.id) {
    case 'y8':
        options = { achievement: 'ACHIEVEMENT_NAME', achievementkey: 'ACHIEVEMENT_KEY' };
        break;
    case 'lagged':
        options = { achievement: 'ACHIEVEMENT_ID' };
        break;
}
bridge.achievements.unlock(options).then(() => {});

// List (platform-specific shape)
bridge.achievements.getList({}).then((list) => {});

// Native overlay
bridge.achievements.showNativePopup({});
```

Keep a constants file in your game that maps internal milestones to per-platform achievement IDs.

## Social module — `bridge.social`

All optional. Each method has an `is*Supported` flag — **always check it and hide the button** when unsupported. Trigger only from direct user action.

### Capability matrix

| Feature            | Flag                         | Typical platforms         |
| ------------------ | ---------------------------- | ------------------------- |
| Share              | `isShareSupported`           | VK, Facebook, MSN         |
| Join community     | `isJoinCommunitySupported`   | VK, OK, Facebook          |
| Invite friends     | `isInviteFriendsSupported`   | VK, OK, Facebook          |
| Create post        | `isCreatePostSupported`      | VK, OK                    |
| Add to favorites   | `isAddToFavoritesSupported`  | VK, Yandex                |
| Add to home screen | `isAddToHomeScreenSupported` | Yandex, GameSnacks        |
| Rate game          | `isRateSupported`            | VK, GameSnacks, Yandex    |
| External links     | `isExternalLinksAllowed`     | Most non-portal platforms |

### Share

```javascript
let options = {};
switch (bridge.platform.id) {
    case 'vk':
        options = { link: 'https://...' };
        break;
    case 'facebook':
        options = { image: 'base64...', text: 'Check this game!' };
        break;
    case 'msn':
        options = { title: '...', image: 'base64 or URL', text: '...' };
        break;
}
bridge.social.share(options).then(() => {});
```

### Join community

```javascript
let options = {};
switch (bridge.platform.id) {
    case 'vk':
    case 'ok':
        options = { groupId: 123456 };
        break;
    case 'facebook':
        options = { isPage: true };
        break; // false → group
}
bridge.social.joinCommunity(options);
```

### Invite friends

```javascript
let options = {};
switch (bridge.platform.id) {
    case 'ok':
        options = { text: 'Hello!' };
        break;
    case 'facebook':
        options = { image: 'base64...', text: 'Join me!' };
        break;
}
bridge.social.inviteFriends(options);
```

### Create post

```javascript
// OK example with mixed media
bridge.social.createPost({
    media: [
        { type: 'text', text: 'Hello!' },
        { type: 'link', url: 'https://...' },
        {
            type: 'poll',
            question: 'Like the game?',
            answers: [{ text: 'Yes' }, { text: 'No' }],
            options: 'SingleChoice,AnonymousVoting'
        }
    ]
});
```

### Other social

```javascript
bridge.social.addToFavorites().then(() => {});
bridge.social.addToHomeScreen().then(() => {});
bridge.social.rate().then(() => {});
```

## Remote Config module — `bridge.remoteConfig`

Optional. Read game settings (difficulty, drop rates, feature flags, A/B values) at runtime without rebuilding.

```javascript
bridge.remoteConfig.isSupported;

let options = {};
switch (bridge.platform.id) {
    case 'yandex':
        options = {
            clientFeatures: [{ name: 'levels', value: '5' }]
        };
        break;
}

bridge.remoteConfig
    .get(options)
    .then((data) => {
        // e.g. { showFullscreenAdOnStart: 'no', difficulty: 'hard' }
    })
    .catch((error) => {});
```

**Always have hardcoded defaults** for every key. The request can fail or return partial data.

## Event names

```javascript
bridge.EVENT_NAME.AUDIO_STATE_CHANGED;
bridge.EVENT_NAME.PAUSE_STATE_CHANGED;
bridge.EVENT_NAME.INTERSTITIAL_STATE_CHANGED;
bridge.EVENT_NAME.REWARDED_STATE_CHANGED;
bridge.EVENT_NAME.BANNER_STATE_CHANGED;
bridge.EVENT_NAME.ADVANCED_BANNERS_STATE_CHANGED;
```

`bridge.platform.on(...)` and `bridge.advertisement.on(...)` accept event-name strings as well.

## State value reference

| Module            | States                                               |
| ----------------- | ---------------------------------------------------- |
| Interstitial      | `loading`, `opened`, `closed`, `failed`              |
| Rewarded          | `loading`, `opened`, `closed`, `rewarded`, `failed`  |
| Banner            | `loading`, `shown`, `hidden`, `failed`               |
| Advanced Banners  | `loading`, `shown`, `hidden`, `failed`               |
| Leaderboards type | `not_available`, `in_game`, `native`, `native_popup` |
| Storage type      | `local_storage`, `platform_internal`                 |

## Best-practice checklist

1. Wait for `bridge.initialize()` before using any API.
2. Apply `bridge.platform.language` to localization.
3. Load saved state from `bridge.storage.get(...)` before showing gameplay.
4. Send `bridge.platform.sendMessage('game_ready')` when first playable frame is rendered.
5. Subscribe to `AUDIO_STATE_CHANGED` and `PAUSE_STATE_CHANGED` and react immediately.
6. Show interstitials at natural breakpoints — never during gameplay.
7. **Never** call `showInterstitial()` at game start.
8. Mute + pause on `opened`; restore on `closed`/`failed`/`rewarded`.
9. Grant rewarded rewards **only** on the `rewarded` state.
10. Save storage on meaningful events, not every frame.
11. After granting items for a consumable purchase, call `consumePurchase(id)`.
12. On launch and reconnect, call `getPurchases()` to recover interrupted purchases.
13. Check every `is*Supported` flag and hide UI for unsupported features.
14. Trigger social actions and `payments.purchase()` only from direct user input.
15. Provide hardcoded defaults for every Remote Config key.
16. Send platform messages (`level_started`, `gameplay_stopped`, etc.) — they drive analytics and Advanced Banners.

## Local development

In environments Bridge doesn't recognize it falls back to `mock`. APIs return safe defaults instead of throwing, so you can develop and debug locally before publishing. `bridge.platform.id === 'mock'` indicates this state.

## Resources

- Config editor: `https://playgama.github.io/bridge-config-editor/`
- Wiki: `https://wiki.playgama.com/`
