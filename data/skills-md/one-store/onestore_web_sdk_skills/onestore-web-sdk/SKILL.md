---
name: onestore-web-sdk
description: 'Integrate the ONE store H5 Game SDK (Web SDK) into an HTML5 web game, check the integration status, and review the code before release. Use when the conversation mentions ONE store, OneStore, 원스토어, web game, 웹게임, HTML5 game, H5, WebView game, in-app purchase, 인앱결제, ads, 광고, rewarded or interstitial ads, createSDK, ONEstoreH5, initializeAsync, startGameAsync, purchase, getProductDetailsAsync, showRewardedAsync, or an iframe-hosted game, or when the user sends a command word such as doctor, integrate, iap, ads, embed, fix, or check to this skill. Covers loading the SDK, the boot flow (init, loading, start), lifecycle handling, ad and purchase code, iframe embedding requirements, error (reason) diagnosis, a blank screen in the app, and pre-release checks. When asked to write ad, purchase, or lifecycle code for a ONE store web game, use this skill instead of writing it from scratch, because it contains reference code based on the official sample.'
---

# ONE store H5 Game SDK integration

Helps HTML5 game developers add the ONE store H5 Game SDK, diagnose problems, and check the
game before release. The ONE store app (Android WebView) loads the game page in an iframe, and
the SDK handles all communication with the app.

> [!IMPORTANT]
> **Answer in the user's language.** This skill is written in English, but most users write in
> Korean. Answer in the language the user writes in, and translate everything you show: table
> headers, verdict words, fill-in forms, and the suggested messages at the end. Keep only the
> structure. Keep code identifiers, SDK constants, and `reason` strings unchanged. Menu paths in
> this skill are given as `Korean label (English label)`; use the one that matches the user's
> language. Before sending, check that the first sentence, the table headers, and the closing
> suggestion are in the user's language.

## What this skill does

If the user asks what the skill can do, or invokes it with no request, show the table below and
run the status check right away. Users can ask in plain language; they do not need to know the
procedure names.

| Command | Plain-language example | What to do |
|---|---|---|
| `doctor` | "How far along is the ONE store integration?" / "지금 어디까지 됐어?" | **Status check.** Report what is present and what is missing in a table. Do not edit files |
| `integrate` | "Add the ONE store SDK so I can publish this game" / "원스토어 SDK 붙여줘" | Load the SDK, wire the boot flow (init → loading → start), place the lifecycle listeners |
| `ads` | "Add a rewarded ad" / "리워드 광고 붙여줘" | Place ad code, including `requestId` and the reward policy |
| `iap` | "Add in-app purchase" / "결제 붙여줘" | Place purchase and product lookup code, including the hook for server-side `purchaseToken` verification |
| `embed` | "It only fails inside the app" / "앱에서만 안 떠" | Check the iframe embedding requirements (`references/embed-requirements.md`) |
| `fix <reason or symptom>` | "The screen is blank" / "reason is no_fill" | **Diagnose.** Cause, reproduction, fix, and what to verify (`references/diagnose.md`) |
| `check` | "Run the pre-release check" / "릴리즈 전에 점검해줘" | The full pre-release checklist. Do not edit files |

### Command words

A user can call a procedure directly with a command word. In Claude Code the form is
`/onestore-web-sdk <command>` (for example `/onestore-web-sdk doctor`), and the word arrives as the
skill argument (`ARGUMENTS: doctor`). Other tools invoke skills differently, and some users just
type `onestore doctor` or `/원스토어 진단` in chat. Treat all of these the same way.

- **A command word alone means: run that procedure now.** Do not ask what they want. Ask only if
  the target file is unclear (rule 3)
- The skill invoked with no command word → run the status check and show the table above
- When you suggest the next step, give the plain-language request first, because it works in every
  tool, and add the Claude Code form after it

State the boundary as well: the game company's server work (receiving postbacks, verifying
`purchaseToken`, consuming purchases) and ONE store registration (placement IDs, products, test
URL) are the user's job, and this skill does not cover the ONE store hosting page or app.

### Values you need from the user

**There are only four: three come from the ONE store side, and one is the game company's server design.** Many users start without knowing
what is needed, so **tell them up front and say where to get each one.**

| Value | Where it comes from | If missing |
|---|---|---|
| **SDK version** | The user's ONE store contact, or the [release notes](https://onestore-dev.gitbook.io/dev/tools/web-sdk/releasenote). Starts with `v`. **If they were not told otherwise, recommend the latest, `v1.1.0`** | You can proceed with `v1.1.0` |
| **Ad placement ID (`placementId`)** | Requested in ONEconsole: Apps > (the game) > 수익화 > 인앱 광고 (Monetization > In-App Ads), one per ad type (rewarded, interstitial). See [ONEconsole: 인앱 광고 (In-App Ads)](https://onestore-dev.gitbook.io/dev/docs/apps/product/monetization/iaa) | Every ad request fails, with no fallback |
| **In-app product ID (`productId`)** | ONEconsole: Apps > (the game) > 수익화 > 인앱 상품 (Monetization > In-App Products). Managed products only | Purchases fail with `invalid_request` |
| **How `requestId` is issued** | The game company's server design. Issuing it on the server and mapping it to the user is recommended | You cannot tell whose reward a postback belongs to |

#### When you ask for values, give a form to fill in

**Saying only "X is missing" leaves the user unsure what to fetch and from where.** Send the form
below as is, translated into the user's language, so they can copy it, fill it in, and paste it back.

```text
SDK version: (leave blank to use the latest, v1.1.0)
        Fill this in only if ONE store gave you a specific version. It starts with v.
        It goes into the {{version}} part of the CDN URL.

Ad placement ID: (write it here, e.g. rewarded rew_xxxx, interstitial int_xxxx)
        Request it in ONEconsole: Apps > (the game) > 수익화 > 인앱 광고
        (Monetization > In-App Ads). Rewarded and interstitial
        IDs are issued separately, so say which one this is.

In-app product ID: (write it here, e.g. gem_100, gem_1000)
        The product ID registered in ONEconsole under 수익화 > 인앱 상품 (Monetization > In-App Products).
        If there are several, list them all separated by commas. (Managed products only.)

requestId issuing: (server-issued / generated on the client)
        The tracking key for rewarded ad rewards. The postback must tell you which user
        the reward belongs to, so issuing it on your server and mapping it to the user
        is recommended.
```

- **Leave the value slots empty.** If you pre-fill example values, some users leave them as is
- **Do not use real values as examples.** Do not put IDs you found in the project into the form.
  Mention values you already know in a sentence, and leave the form empty
- If something is not registered or issued yet, say that **the ONE store side has to be done first**
- When you receive values, **say which file you put them in**

**Integration can start without the values.** Load the SDK, wire the boot flow, and place the
listeners, leave the value slots as TODOs, then give the form and stop. **Do not block progress
while waiting for values.**

### When the next step is yours, give the words to say

**When the remaining work is yours, the only thing the user has to do is ask for it.** If you
describe the work instead, the user thinks they have to do it and gets stuck. **Give the words,
not the task:** a request they can copy and send, in a code block so it stands out.

```text
Send this next:

  Add a ONE store rewarded ad to the game

I will wire it with the reward policy (show the reward only on rewarded, grant it through
the server postback). In Claude Code you can also send /onestore-web-sdk ads.

After that:

  Run the ONE store pre-release check
```

- **Pair each request with its result**, so the user can see what each one does and choose
- **If more than one step remains, list them all in order.** Giving only the current one leaves
  the user stuck again at every step
- If the user's work (ONE store registration, server code) and yours are mixed, **list them separately**

## Core rules

1. **Do not invent SDK APIs.** Use only the methods, fields, events, and `reason` values in
   `references/sdk-context.md`. If something is not there, say it needs confirmation. Do not map
   names from other platforms' game SDKs (such as Facebook Instant Games) even if they look alike.
2. **Take the integration code from `references/game-template.html.txt`.** It is reference code,
   based on the official sample, for the boot flow, ads, purchase, and lifecycle. When adding it to an existing game,
   move the relevant parts but **keep the call order and branch structure**, especially the `err`
   branch, the reward branch (`rewarded` only), and the `reason` branches. Adjust after placing it
   if it does not fit.
3. **Decide the target from evidence.** If there is no evidence of where the game's entry HTML and
   boot code are, or there are several candidates, ask instead of guessing.
4. **Answer definitely or ask. Do not hedge.** Do not dodge with "probably" or "usually". If you
   lack information needed for a verdict, ask for that specific information.
5. **Cite evidence as `path:line`.** Use the path relative to the project root plus the line number
   (for example `index.html:47`). Tools render links differently, so this form reads everywhere and
   is clickable in most tools. Do not use absolute paths or `file://` links. Fix any verdict that
   has no evidence location. Point to public guide URLs for further reading; the reference files
   are for you, not for the user.
6. **End with the next step.** Do not end with what you did. If the next step is the user's, make
   it concrete enough to do on the spot (menu path, complete command). If it is yours, give a
   request they can send. If you stopped for missing values, say what to provide to continue. If
   nothing is left, say so. **Hearing "what do I do now?" means this rule was not followed.**
7. **Do not overwrite existing files.** Show what is there and ask.
8. **The scope is the game client code.** For the game company's server (postback and PNS
   reception, `purchaseToken` verification, consumption), create the hook only and say the
   implementation is the user's. Do not set up a server framework.

## First: status check (doctor)

For open-ended requests ("add it", "how far along is it?", "what now?"), when the skill is invoked
with no request, or when you do not know the project state yet, **run the status check first**. Do
this even in the middle of an integration: read the files to decide, do not answer from memory.

- Follow **list A** in `references/checks.md`
- **Read only. Do not edit any file**
- Use exactly four verdicts: **present / missing / not applicable / needs confirmation**. Cite
  evidence as `path:line` (rule 5)
- **Show the full table.** The point is to show what is already done too (the pre-release check is
  the opposite: only what needs fixing)
- Under the table, give the next step (rule 6). If values are missing, give the form (only the
  missing values); if the next step is yours, give the request to send
- Unless the user already told you to proceed, stop here and let them choose

## Integration steps

Do only what the status check found missing.

### 1. Load the SDK

Put it at the **top level of the game's entry HTML document**, **before the game scripts**.

```html
<script type="module">
  import { createSDK } from "https://h5sdk.onestore.net/lib/v1.1.0/onestore-h5-sdk.min.js";
</script>
```

- The version starts with `v`. Use the one the user was given, otherwise **the latest, `v1.1.0`**.
  Do not stop progress over the version
- Initialization fails inside an iframe the game creates itself. It must be the game document's
  top level
- If the game uses a bundler (webpack etc.), put the import at the very top of the game entry and
  check that it runs in the same order as loading it directly from HTML
- **Tag order alone does not guarantee execution order.** `type="module"` runs after the document
  is parsed, so a game script loaded with a plain `<script src>` runs **before** the SDK even if its
  tag comes later. Add `type="module"` or `defer` to the game script so it runs after the SDK, and
  start the game only after `startGameAsync()` succeeds

### 2. Boot flow and lifecycle

Place the script part of `references/game-template.html.txt` to fit the game's boot code. The
required call order and rules are defined in `references/sdk-context.md`. After placing it, always tell
the user:

- **Register the listeners (`pause` / `resume` / `exit`) before `initializeAsync()`.** Events can
  arrive right after initialization
- **In `exit`, only save, synchronously, within 0.5 seconds.** No need to call `quit()` again. When
  the game calls `quit()` itself, `exit` does not fire, so save before calling it
- **`onBackPressed` must be a synchronous function.** The app waits 200 ms for the answer
- An unsupported environment resolves with `err` instead of rejecting. Do not remove the
  `if (info.err)` branch. In that branch, keep the game playable without the SDK (turn off only
  ad and purchase UI), so it still runs in a regular browser during development
- Connect the loading progress to real asset loading. The demo timer in the template is a placeholder
- **When the game keeps an object in a global, do not give it the same name as an element `id`.**
  Browsers expose elements with an `id` as `window` properties of the same name. With
  `<canvas id="game">`, `window.game` is the canvas until the game code overwrites it, and boot code
  that runs first breaks with `window.game.start is not a function`. Use a global named after the
  game (for example `window.StarCatcher`), and have the boot code check that the object is ready
  before calling it
- **When the SDK code and the game code are in separate scripts, wait for the game object before
  calling it.** The SDK script runs first, and the `initializeAsync()` result can arrive before the
  game script has run (in a regular browser it resolves almost at once). Calling the game object
  then throws, and the game never starts. Route every call from SDK code into the game through a
  helper like this (the `err` branch, after `startGameAsync`, `pause` / `resume`, `ringerSilent`):

  ```js
  // Game scripts load with type="module" or defer, so they have all run by DOMContentLoaded
  function whenGame(fn) {
    if (window.MyGame) fn(window.MyGame);
    else document.addEventListener("DOMContentLoaded", () => fn(window.MyGame), { once: true });
  }
  // whenGame((game) => game.start());
  ```

  This works when the game object is created at the top level of its script. If the game creates
  it later (after loading assets, for example), have the game send its own "ready" signal instead

### 3. Ads

Check that `placementId` exists before placing the code. If it does not, place the code with TODOs
and ask for the value with the form. After placing it, always tell the user these three things,
because each one causes incidents:

- **Show the reward only when `status === "rewarded"`.** `dismissed` and `failed` (including
  `no_fill`) are not rewarded
- **Do not grant rewards from the client-side `rewarded` result.** The grant is confirmed through
  SSV → verification → the game company's server postback, and the game asks its own server whether
  the reward was granted. Say separately that receiving the postback is the user's job
- **`requestId` is required for rewarded ads.** The SDK does not generate it. Issuing it on the
  server and mapping it to the user is recommended

If the user has no placement ID yet, tell them what to do in ONEconsole, in this order (source:
[ONEconsole: 인앱 광고 (In-App Ads)](https://onestore-dev.gitbook.io/dev/docs/apps/product/monetization/iaa), English
<https://onestore-dev.gitbook.io/dev/eng/docs/apps/product/monetization/iaa>):

Both menus are in the game's sidebar after choosing the game under Apps.

1. Set 광고 적용 여부 (use ads) to 예 (Yes) under 상품관리 > Web 상품관리 > 기본정보
   (Product Mgmt. > Web App Mgmt. > Main Info)
2. In 수익화 > 인앱 광고 (Monetization > In-App Ads), press
   ID 발급 요청 (request ID) for each ad type. One ID per type; issuance takes about one business day
3. For rewarded ads, once the ID is issued, register the callback URL and API key on the same screen.
   The server postback (SSV) that confirms rewards goes to that URL. Not needed for interstitial only
4. No test placement IDs are provided. If the user needs one, they ask devhelper@onestore.net

Place the preload calls (`loadRewarded` / `loadInterstitial`) **early, for example right after
`startGameAsync` succeeds**, so the ad shows immediately when the button is pressed. Without them it
still works, but the first ad takes longer.

Ad support has not yet been verified end to end on a device with this skill. Tell the user to test
ads on a device before release.

#### When the user provides a placement ID later

If the ad code was placed with an empty ID, receiving the ID means more than filling in one value.
Do all of the following:

1. **Put each ID in its own slot.** The rewarded ID goes where `loadRewarded` / `showRewardedAsync`
   use it; the interstitial ID goes where `loadInterstitial` / `showInterstitialAsync` use it. If it
   is unclear which one the user sent, ask. The two are issued separately, and a placement type
   mismatch fails with `invalid_request`
2. **Turn back on what was turned off because the ID was empty**: a disabled ad button, a skipped
   preload, an early `return`, a "not set" label. Filling in the constant alone often leaves the
   button disabled
3. Keep the order: feature check (`sdk.ads.isSupported(...)`) after init → preload → enable the button
4. **Say which files and lines changed** (`path:line`)
5. Tell the user how to check it: ads show only inside the ONE store app (a regular browser always
   returns `platform_not_supported`), with the test URL and test ID registered. A `no_fill` result
   during testing means there is no ad inventory right now, not that the integration is broken

### 4. Purchase

Check that `productId` exists before placing the code. If it does not, place the code with TODOs and
ask for the value with the form. After placing it, always tell the user:

- **A success response is not a reason to grant the item.** The game company's server confirms the
  purchase by verifying `purchaseToken`. The payment notification (PNS) also goes to the server, so
  grant items based on the server
- **Consumption is the server's job.** Without it, buying the same product again fails with
  `already_owned`
- **Put the information needed to grant the item in `developerPayload`.** It is optional but very
  important: the purchase result and the PNS notification are matched to the user and purchase by
  this value, so leaving it empty removes the way to match them. Suggest what to put in it (such as a
  user identifier) based on the game's structure, but do not decide it by guessing
- Do not show an error popup for `user_cancelled`
- Purchase requests trigger `pause` (`reason: "payment"`) and `resume` events. Do not pause the game
  separately at the purchase call site; handle it in the one `pause` listener
- Web products support **managed products only** (no subscriptions)

### 5. Embedding requirements

These are outside the code and easy to miss. Check them with `references/embed-requirements.md`, and
hand over server settings (frame-allow headers, HTTPS, redirects) as needs confirmation, with how to
check them (`curl -sI`). Tell the user that **any frame-busting code must be removed**.

## Error diagnosis

| What you received | Where to start |
|---|---|
| A `reason` string or console log | Look it up in the `reason` tables in `references/sdk-context.md`, and point to where the project handles that path |
| **Only a symptom, such as "it doesn't show up"** | **`references/diagnose.md`**, which says what to collect and how to narrow it down |

Do not start reading code with only a symptom. The cause is often outside the code (server headers,
ONE store registration, app version). Check what you can yourself (`curl -sI`, reproducing in the
console); if you cannot run it, give the command and steps and ask for the result. **Do not present
a guess as the answer.**

Answer with **cause, reproduction, fix (with code), and what to verify**. For reasons the code
cannot fix (`no_fill`, `platform_not_supported`, and so on), say so and give the right handling
(hide the UI, provide another path).

## Pre-release check

Follow **list B** in `references/checks.md`. Read only. For items that depend on the server or ONE
store registration, check only that the code has the hook, and say the rest is outside the project.

**List only what needs fixing.** Show passed items as a count. Order: blockers → non-blockers →
needs confirmation → passed count.

## Reference files

Read only what you need.

- `references/sdk-context.md`: the full public API, call order, events, `reason` tables, CDN URL,
  and granting rules (the source of truth)
- `references/game-template.html.txt`: the reference integration code (replace `__SDK_VERSION__`,
  fill in the TODOs)
- `references/embed-requirements.md`: iframe embedding requirements (frame allowance, URL, storage,
  forbidden calls, screen)
- `references/checks.md`: list A (status check) and list B (pre-release check)
- `references/diagnose.md`: how to narrow down a problem from a symptom

Public docs: Web SDK Integration Guide <https://onestore-dev.gitbook.io/dev/tools/web-sdk> (English
<https://onestore-dev.gitbook.io/dev/eng/tools/web-sdk>)
