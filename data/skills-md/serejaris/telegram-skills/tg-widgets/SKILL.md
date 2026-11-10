---
name: tg-widgets
description: "Use when building or sending a Telegram message widget (HTML bubble, HTMLBubbles, `sendWidget`, `messageMediaWidget`, Bot API 10.4): an interactive HTML, CSS and JS program inside a chat bubble, such as a game, poll, calculator or live ticker. Teaches everything needed to write one: size, bubble, input, sandbox rules, state and requests, sending, and where live delivery differs from the documentation. Not for Mini Apps or Rich Messages."
license: MIT
---

# tg-widgets

A widget is one self-contained HTML document with inline CSS and JS. A bot sends it as a message, and it runs in the chat bubble with no window, no server and no network. The HTML never changes after sending; only the bot changes the widget's state.

Everything needed to write a widget is below. The rules follow Telegram's [`widget-sandbox`](https://github.com/TelegramMessenger/widget-sandbox) documentation, v0.6.0, checked on 2026-11-06. Telegram has not announced widgets, the public Bot API docs stop at 10.3, and names may change until 10.4 ships. For a detail not covered here, see `docs/sdk-v1.md` and `docs/profile-v1.md` in that repository.

## Steps

1. Write the widget by the rules below.
2. Measure as the server does:

   ```bash
   python3 scripts/widget_tool.py check widget.html
   ```

3. Send it to your private chat with the bot. The tool sends once and never retries: after a timeout the message may already be delivered.

   ```bash
   TELEGRAM_BOT_TOKEN=... python3 scripts/widget_tool.py send widget.html --chat CHAT_ID --caption "Tap the water to feed"
   ```

4. Open it on a phone. A successful `sendWidget` proves only that the server accepted it: clients below layer 233 show an unsupported-media stub with the caption, so write a caption that makes sense alone.

## Size

The server compresses the HTML with zlib level 9 and refuses anything over 4096 bytes, or over 32768 bytes raw, with `INPUT_MEDIA_WIDGET_TOO_LARGE`. Aim for 3800 if you cannot measure.

- Repeated CSS and markup compress well. `data:` images and long unique text do not.
- Non-ASCII text compresses badly: cutting Russian strings saved more than renaming identifiers.
- Generate scenes in code instead of storing them.
- No comments, no dead code. Minify with terser.

## Bubble

- 200–600 px wide, phones about 320–430: design for 320. Up to 600 px tall; the rest is clipped and nothing scrolls inside. Split long content into pages or tabs.
- `width` and `height` in `sendWidget` set the size, `0` means auto. Lay out with `%`, flex, grid or `vw`, never `vh`.
- `html` has no background: the bubble's colour shows through, and a background on `html` or `body` paints the whole bubble. `body` has a margin of about `8px 12px`; `body{margin:0}` goes edge to edge.
- Colours: `--tg-theme-bg-color`, `--tg-theme-text-color`, `--tg-theme-hint-color`, `--tg-theme-link-color`, `--tg-theme-button-color`, `--tg-theme-button-text-color`, `--tg-theme-secondary-bg-color`; `--tg-color-scheme` is light or dark. Build on them so both themes work, or paint the whole bubble yourself.
- Without a caption below, the client draws the message time over the bottom corner. Keep `env(safe-area-inset-bottom)` clear, and set `body{padding:0}` if you pad for it yourself.
- Text is not selectable unless you set `user-select:text` and `-webkit-user-select:text`.

## Input

Taps (`click`) and pointer events only. No touch events, keyboard, focus, text input, wheel or scroll events. A double tap is always the widget's.

Vertical drags belong to the chat, whatever `touch-action` says. So no vertical sliders, wheel pickers or free drawing: use horizontal controls or buttons.

| `touch-action` on the element | Use for | Hold | Horizontal drag |
|---|---|---|---|
| `auto` (default) | everything else | chat's message menu | chat's swipe-to-reply |
| `pan-y` | slider, carousel, paddle | chat's menu | widget's |
| `none` | canvas, game control, held button | widget's | widget's |

The first move past 10 px decides the whole press: a drag that starts sideways on a claimed element stays with the widget on both axes, and one that starts up or down goes to the chat, and the widget gets `pointercancel` and no `click`. On `pointercancel`, undo what `pointerdown` started. The leading 20 px never take a claim because of the system back gesture: keep controls away from that edge.

## What works

- **HTML:** text elements, lists, tables, `details`, `a`, `button` (unstyled, it looks like the client's own), `canvas`, `img` with `data:` PNG, JPEG, GIF or WebP up to 1024×1024, inline SVG with shapes, paths, text, `use` and gradients.
- **CSS:** flex, grid, positioning, shadows, gradients, 2D transforms, `opacity`, `filter` and `backdrop-filter` with `blur()`, `brightness()` and `drop-shadow()` only, transitions, `@keyframes`, custom properties, `calc`, `@media` on width, `prefers-color-scheme`, `@supports`. Fonts: `system-ui`, `sans-serif`, `serif`, `monospace`, `ui-*` only.
- **JS:** ES2023 in an interpreter without JIT, timers, `requestAnimationFrame`, the DOM, canvas 2D (paths, arcs, `fillText`, gradients, `setTransform`, `clip`, `drawImage`), `el.animate`, `Intl`, `crypto.getRandomValues`, `localStorage`, `sessionStorage`. Use `document.getElementById('x')`: ids are not global variables.

## Not available

Removed silently while the rest keeps running, so a removed feature is a bug you will not see.

- **Network:** `fetch`, `XMLHttpRequest`, `WebSocket` throw `NetworkDisabledError`; nothing external loads.
- **Canvas:** WebGL, `OffscreenCanvas`, `getImageData`, `putImageData`, `createImageData`, `toDataURL`, `shadowBlur`, `globalCompositeOperation`, `ctx.filter`, `createPattern` from a canvas.
- **CSS:** 3D transforms, `perspective`, `vh`, `overflow:auto|scroll`, `position:sticky`, `text-shadow`, `clip-path`, `mask`, `mix-blend-mode`, `background-clip:text`, `color-mix`, `oklch`, `@font-face`, named fonts, `@container`, `:has`, CSS nesting.
- **HTML:** form controls, `audio`, `video`, `iframe`, `dialog`, `progress`.
- **JS:** libraries, `Worker`, `alert`, `confirm`, `navigator.clipboard`, `window.open`, `location` changes, `Blob`, `customElements`.

## `TelegramWidget`

`window.TelegramWidget` is undefined outside Telegram, so guard it.

| Member | Purpose |
|---|---|
| `ready()` | optional, first state drawn |
| `colorScheme`, `themeParams`, `onEvent('themeChanged', fn)` | theme |
| `HapticFeedback.impactOccurred('light')`, `.notificationOccurred('success')`, `.selectionChanged()` | haptics: free during a touch and 5 s after it, otherwise one short series per 10 s |
| `openLink(url)`, `openTelegramLink(url)`, `copyText(text)`, `request(data)` | need a real tap: call in a `click` handler, one per tap, not after `await` or a timer |
| `chatData`, `publicData`, `onEvent('chatDataChanged', fn)`, `onEvent('publicDataChanged', fn)` | state written by the bot, up to 1024 bytes of text or `null` |
| `watchPublicData()` | poll the shared state live while on screen |
| `viewer`, `isForward`, `chatType`, `isPreview` | who looks and where; `viewer` is `null` where the widget may not ask the bot |
| `wallet` | Gram Wallet; `null` where unavailable. See `docs/sdk-v1.md` §2.18 |

## State and requests

- `chatData` belongs to this message in its chat: a game in progress, whose turn it is. A forward never gets it.
- `publicData` is seen wherever the widget is shown: poll results, a price. A forward gets a frozen copy, or the live value if the bot sent the widget with `is_shared`.
- `localStorage` is this user's own, per message and device, 4 KB; catch `QuotaExceededError`. Use it for a best score or a seed.
- `request(data)` works like a callback button: 1–64 bytes, resolves with `{result}` up to 1024 bytes, rejects with `error.code`: `NOT_ALLOWED`, `BUSY`, `RATE_LIMITED`, `TIMEOUT`, `FAILED`, `INVALID_ANSWER`. It needs `allow_queries` at sending. The answer does not change the state: have the bot edit it, or return the new state in `result`.

## Lifecycle and limits

The widget can be destroyed and recreated at any time: restore from `localStorage` and the state, and draw the first frame synchronously. Off screen there are no animation frames and timers fire at most once per second.

| Limit | Value |
|---|---|
| CPU | 300 ms per second; one task up to 500 ms, longer stops the widget |
| Memory, nodes | 8 MB, 2000 nodes |
| Canvas | 4000 commands per canvas per task, 2048×2048 pixels in total |
| Paint | 16 elements with blurred shadow, filter or opacity below 1; 2 with `backdrop-filter`. Mute with colour instead of `opacity` |
| Layout reads | 128 per task; cache them and never read every frame |
| Other | 64 timers, 400 CSS rules, 32 `@keyframes`, 64 script animations |

Past a limit the widget stops on its last frame with a "Widget stopped" badge.

## Skeleton

```html
<style>body{margin:0}canvas{display:block;width:100%;touch-action:none;image-rendering:pixelated}</style>
<canvas id="c"></canvas>
<script>
const T=window.TelegramWidget,c=document.getElementById('c'),x=c.getContext('2d');
const W=c.clientWidth||360,H=Math.round(W*9/16),S=3;
c.style.height=H+'px';c.width=W/S|0;c.height=H/S|0;
let last=0;
function frame(t){requestAnimationFrame(frame);if(t-last<33)return;last=t;
  x.fillStyle='#024';x.fillRect(0,0,c.width,c.height)}
c.addEventListener('click',e=>{const r=c.getBoundingClientRect();
  T&&T.HapticFeedback.selectionChanged()});
requestAnimationFrame(frame);T&&T.ready();
</script>
```

## Delivery: documentation and live check

The documentation allows more than the live API accepted. Live means real requests on 2026-11-06 with production bots. Recheck before you plan around it.

| Target | Documentation | Live |
|---|---|---|
| `api.telegram.org/bot<token>/sendWidget` | beta path only | 404 |
| `api.telegram.org/beta/bot<token>/sendWidget` | works | works with a normal token |
| Private chat with the bot | allowed | works, rendered on an iPhone |
| Group or supergroup with the bot | allowed | supergroup and a channel's discussion group refused: `INPUT_MEDIA_WIDGET_NOT_ALLOWED` |
| Channel, direct | not allowed yet | refused, same error |
| Inline mode | allowed | refused in a channel, and for a query from the private chat with the bot |
| `forwardMessage` | allowed to any chat | refused: `the message can't be forwarded` |
| `copyMessage` | refused | refused |

To put a widget in front of a channel audience today, publish a post with a video and a `t.me/<bot>?start=...` link, and let the bot send the widget in the private chat.

## Bot API

| Method | Purpose |
|---|---|
| `sendWidget` | `chat_id`, `html`, `width`, `height` (0 = auto), `chat_data`, `public_data`, `caption`, `allow_queries`, `is_shared`, `reply_markup` |
| `sendSharedWidget` | post an existing shared widget again by `widget_id` |
| `editMessageWidgetData` | change `chat_data` or `public_data` of one message silently; `message is not modified` counts as done |
| `editSharedWidgetData` | change the state of a shared widget everywhere, `cache_time` 5–3600 s |
| `answerWidgetQuery` | answer the `widget_query` or `shared_widget_query` update, always, or the widget gets `TIMEOUT` |

## Examples

`examples/` holds widgets built with this skill and opened on an iPhone. They show one author's look. Sizes after zlib level 9:

| File | Bytes |
|---|---|
| [`aquarium-pixel.html`](examples/aquarium-pixel.html) | 4080 |
| [`night-deploy-pixel.html`](examples/night-deploy-pixel.html) | 4086 |
| [`night-deploy-textmode.html`](examples/night-deploy-textmode.html) | 4071 |
| [`textmode-panel.html`](examples/textmode-panel.html) | 2134 |
