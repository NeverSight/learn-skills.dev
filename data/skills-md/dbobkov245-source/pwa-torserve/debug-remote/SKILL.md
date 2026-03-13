---
name: debug-remote
description: Specialist in debugging TV apps remotely (logs, telemetry).
---

# Remote Debugging for TV

Debugging a TV app is hard. `console.log` is invisible on the TV screen.
Use this skill to capture logs and errors from the TV environment.

## 📡 Remote Logging Strategy

### 1. The "On-Screen Console" Overlay
For quick debugging without a laptop connection.
- **Trigger:** Konami Code (Up, Up, Down, Down, Left, Right, Left, Right, B, A) or hidden button.
- **UI:** A simple fixed-position `<div>` with `overflow-y: scroll`, semi-transparent background, high contrast text.

```javascript
/* Simple Logger Utility */
const originalLog = console.log;
console.log = (...args) => {
  originalLog(...args);
  if (window.debugOverlay) {
    window.debugOverlay.innerHTML += `<div>${args.join(' ')}</div>`;
  }
};
```

### 2. Network Logging (Remote Spy)
Send logs to a remote server or simple webhook (e.g., `webhook.site` for temp debugging).

```javascript
const LOG_ENDPOINT = 'https://your-log-drain.com/ingest';

function remoteLog(level, message) {
  fetch(LOG_ENDPOINT, {
    method: 'POST',
    body: JSON.stringify({ level, message, timestamp: Date.now() })
  }).catch(() => {}); // Fire and forget
}
```

### 3. ADB Logcat (The Gold Standard)
If you have ADB access:
- **Command:** `adb logcat | grep "Chromium"`
- **Filter:** Use a unique prefix in your logs: `console.log("[PWA]", ...)` -> `grep "\[PWA\]"`

## 🐛 Common TV Bugs to Watch
- **Focus Traps:** Focus goes to an invisible element or gets stuck.
- **Memory Leaks:** Large images not being garbage collected. Monitor heap size if possible.
- **Network Timeouts:** TV WiFi is often worse than phone WiFi.
- **Clock Skew:** TV system time might be wrong (SSL errors).

## 🛠 Usage
Implements a global `window.__DEBUG__` object to toggle modes:
- `window.__DEBUG__.enableOverlay()`
- `window.__DEBUG__.disableOverlay()`
- `window.__DEBUG__.setRemoteServer(url)`
