---
name: flipoff-split-flap-display
description: Expert skill for building, customizing, and embedding the FlipOff split-flap display emulator — a free, offline-capable web app that turns any browser/TV into a retro airport departure board.
triggers:
  - add split flap display to my site
  - customize flipoff messages or quotes
  - embed retro flip board display
  - change flipoff grid size or colors
  - how do I use flipoff split flap emulator
  - add keyboard controls to flipoff
  - flipoff sound and animation configuration
  - turn TV into flip board display
---

# FlipOff Split-Flap Display Emulator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

FlipOff is a pure vanilla HTML/CSS/JS web app that emulates classic mechanical split-flap (flip-board) airport displays. No frameworks, no npm, no build step — open `index.html` and you have a full-screen retro display with authentic scramble animations and clacking sounds.

---

## Installation

```bash
git clone https://github.com/magnum6actual/flipoff.git
cd flipoff

# Option 1: Open directly
open index.html

# Option 2: Serve locally (recommended for audio)
python3 -m http.server 8080
# Visit http://localhost:8080
```

> **Audio note:** Browsers block autoplay. The user must click once to enable the Web Audio API context. After that, sound plays automatically on each message transition.

---

## File Structure

```
flipoff/
  index.html               — Single-page app entry point
  css/
    reset.css              — CSS reset
    layout.css             — Header, hero, page layout
    board.css              — Board container and accent bars
    tile.css               — Tile styling and 3D flip animation
    responsive.css         — Media queries (mobile → 4K)
  js/
    main.js                — Entry point, wires everything together
    Board.js               — Grid manager, transition orchestration
    Tile.js                — Per-tile animation logic
    SoundEngine.js         — Web Audio API playback
    MessageRotator.js      — Auto-rotate timer
    KeyboardController.js  — Keyboard shortcut handling
    constants.js           — All configuration lives here
    flapAudio.js           — Base64-encoded audio data
```

---

## Key Configuration — `js/constants.js`

Everything you'd want to change lives in one file:

```js
// js/constants.js (representative structure)

export const GRID_COLS = 26;        // Characters per row
export const GRID_ROWS = 8;         // Number of rows

export const SCRAMBLE_DURATION = 600;  // ms each tile scrambles before settling
export const STAGGER_DELAY = 18;       // ms between each tile starting its scramble
export const AUTO_ROTATE_INTERVAL = 8000; // ms between auto-advancing messages

export const SCRAMBLE_COLORS = [
  '#FF6B35', '#F7C59F', '#EFEFD0',
  '#004E89', '#1A936F', '#C6E0F5'
];

export const ACCENT_COLORS = ['#FF6B35', '#004E89', '#1A936F'];

export const MESSAGES = [
  "HAVE A NICE DAY",
  "ALL FLIGHTS ON TIME",
  "WELCOME TO THE FUTURE",
  // Add your own here
];
```

---

## Adding Custom Messages

Edit `MESSAGES` in `js/constants.js`. Each message is a plain string. The board wraps text across the grid automatically.

```js
export const MESSAGES = [
  "DEPARTING GATE 7",
  "YOUR COFFEE IS READY",
  "BUILD THINGS THAT MATTER",
  "FLIGHT AA 404 NOT FOUND",    // max GRID_COLS * GRID_ROWS chars
];
```

**Padding rules:** Messages shorter than the grid are padded with spaces. Messages longer than the grid are truncated. Keep messages at or under `GRID_COLS × GRID_ROWS` characters.

---

## Changing Grid Size

```js
// Compact 16×4 ticker-style board
export const GRID_COLS = 16;
export const GRID_ROWS = 4;

// Wide cinema board
export const GRID_COLS = 40;
export const GRID_ROWS = 6;

// Tall info kiosk
export const GRID_COLS = 20;
export const GRID_ROWS = 12;
```

After changing grid dimensions, tiles re-render automatically on next page load.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` / `Space` | Next message |
| `Arrow Left` | Previous message |
| `Arrow Right` | Next message |
| `F` | Toggle fullscreen |
| `M` | Toggle mute |
| `Escape` | Exit fullscreen |

---

## Programmatic API

### Board

```js
// Board.js exposes a class you can instantiate directly
import Board from './js/Board.js';

const board = new Board(document.getElementById('board-container'));

// Display a specific string
board.setMessage('GATE CHANGE B12');

// Advance to next message in the rotation
board.next();

// Go back
board.previous();
```

### MessageRotator

```js
import MessageRotator from './js/MessageRotator.js';

const rotator = new MessageRotator(board, messages, AUTO_ROTATE_INTERVAL);

rotator.start();   // begin auto-advancing
rotator.stop();    // pause rotation
rotator.next();    // manual advance
rotator.previous(); // manual back
```

### SoundEngine

```js
import SoundEngine from './js/SoundEngine.js';

const sound = new SoundEngine();

// Must call after a user gesture (click/keypress)
await sound.init();

sound.play();    // play the flap transition sound
sound.mute();    // silence
sound.unmute();
sound.toggle();  // flip mute state
```

### KeyboardController

```js
import KeyboardController from './js/KeyboardController.js';

const kb = new KeyboardController({
  onNext:       () => rotator.next(),
  onPrevious:   () => rotator.previous(),
  onFullscreen: () => toggleFullscreen(),
  onMute:       () => sound.toggle(),
});

kb.attach();   // start listening
kb.detach();   // stop listening
```

---

## Embedding FlipOff in Another Page

### As an iframe

```html
<iframe
  src="/flipoff/index.html"
  width="1280"
  height="400"
  style="border:none; background:#000;"
  allowfullscreen
></iframe>
```

### Inline embed (pull in just the board)

```html
<!-- In your page -->
<div id="flip-board"></div>

<script type="module">
  import Board from '/flipoff/js/Board.js';
  import SoundEngine from '/flipoff/js/SoundEngine.js';
  import { MESSAGES, AUTO_ROTATE_INTERVAL } from '/flipoff/js/constants.js';

  const board = new Board(document.getElementById('flip-board'));
  const sound = new SoundEngine();

  let idx = 0;
  board.setMessage(MESSAGES[idx]);

  document.addEventListener('click', async () => {
    await sound.init();
  }, { once: true });

  setInterval(() => {
    idx = (idx + 1) % MESSAGES.length;
    board.setMessage(MESSAGES[idx]);
    sound.play();
  }, AUTO_ROTATE_INTERVAL);
</script>
```

---

## Custom Color Themes

```js
// js/constants.js — dark blue terminal theme
export const SCRAMBLE_COLORS = [
  '#0D1B2A', '#1B2838', '#00FF41',
  '#003459', '#007EA7', '#00A8E8'
];

export const ACCENT_COLORS = ['#00FF41', '#007EA7', '#00A8E8'];
```

```css
/* css/board.css — override tile background */
.tile {
  background-color: #0D1B2A;
  color: #00FF41;
  border-color: #003459;
}
```

---

## Common Patterns

### Show real-time data (e.g., a flight API)

```js
import Board from './js/Board.js';
import SoundEngine from './js/SoundEngine.js';

const board = new Board(document.getElementById('board'));
const sound = new SoundEngine();

async function fetchAndDisplay() {
  const res = await fetch('/api/departures');
  const data = await res.json();
  const message = `${data.flight}  ${data.destination}  ${data.gate}`;
  board.setMessage(message.toUpperCase());
  sound.play();
}

document.addEventListener('click', () => sound.init(), { once: true });
setInterval(fetchAndDisplay, 30_000);
fetchAndDisplay();
```

### Cycle through a custom message list

```js
const promos = [
  "SALE ENDS SUNDAY",
  "FREE SHIPPING OVER $50",
  "NEW ARRIVALS THIS WEEK",
];

let i = 0;
setInterval(() => {
  board.setMessage(promos[i % promos.length]);
  sound.play();
  i++;
}, 5000);
```

### React/Vue wrapper (import as a module)

```jsx
// FlipBoard.jsx
import { useEffect, useRef } from 'react';
import Board from '../flipoff/js/Board.js';
import { MESSAGES } from '../flipoff/js/constants.js';

export default function FlipBoard({ messages = MESSAGES, interval = 8000 }) {
  const containerRef = useRef(null);
  const boardRef = useRef(null);

  useEffect(() => {
    boardRef.current = new Board(containerRef.current);
    let idx = 0;
    boardRef.current.setMessage(messages[idx]);

    const timer = setInterval(() => {
      idx = (idx + 1) % messages.length;
      boardRef.current.setMessage(messages[idx]);
    }, interval);

    return () => clearInterval(timer);
  }, []);

  return <div ref={containerRef} className="flip-board-container" />;
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No sound | User must click/interact first; Web Audio requires a user gesture |
| Sound works locally but not deployed | Ensure `flapAudio.js` (base64) is served; check MIME types |
| Tiles don't animate | Verify CSS `tile.css` is loaded; check for JS console errors |
| Grid overflows on small screens | Reduce `GRID_COLS`/`GRID_ROWS` in `constants.js` or add CSS `overflow: hidden` |
| Fullscreen not working | `F` key calls `requestFullscreen()` — some browsers require the page to be focused |
| Messages cut off | String length exceeds `GRID_COLS × GRID_ROWS`; shorten or increase grid size |
| Audio blocked by CSP | Add `media-src 'self' blob: data:` to your Content-Security-Policy |
| CORS error loading modules | Serve with a local server (`python3 -m http.server`), not `file://` |

---

## Tips for TV / Kiosk Deployment

```bash
# Serve with a simple static server
npx serve .              # Node
python3 -m http.server   # Python

# Auto-launch fullscreen in Chromium kiosk mode
chromium-browser --kiosk --app=http://localhost:8080

# Hide cursor after idle (add to index.html)
document.addEventListener('mousemove', () => {
  document.body.style.cursor = 'default';
  clearTimeout(window._cursorTimer);
  window._cursorTimer = setTimeout(() => {
    document.body.style.cursor = 'none';
  }, 3000);
});
```
