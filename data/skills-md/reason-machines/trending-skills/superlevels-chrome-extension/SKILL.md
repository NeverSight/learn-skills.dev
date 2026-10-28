---
name: superlevels-chrome-extension
description: Open-source Chrome extension replacing 12+ browser extensions with privacy-respecting tools including tab cleaner, cookie editor, dark mode, JS toggle, GDPR dismisser, and more.
triggers:
  - "add superlevels extension"
  - "customize superlevels feature"
  - "add new feature to superlevels"
  - "how to install superlevels"
  - "debug superlevels extension"
  - "configure superlevels tab cleaner"
  - "superlevels music recognizer setup"
  - "fork and modify superlevels"
---

# SuperLevels Chrome Extension

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

SuperLevels is an open-source Chrome extension that consolidates 12+ browser tools into one auditable, privacy-respecting package. Features include tab cleaning, cookie editing, dark mode, JS toggle, GDPR consent dismissal, live CSS editing, YouTube unhooking, music recognition, Picture-in-Picture, and JSON formatting — all stored locally with zero telemetry.

## Installation (Developer Mode)

```bash
git clone https://github.com/levelsio/superlevels.git
cd superlevels
```

1. Open Chrome → `chrome://extensions/`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `superlevels` folder
4. The 🚀 icon appears in your toolbar

No build step required — pure JavaScript, loads directly.

## Project Structure

```
superlevels/
├── manifest.json          # Extension manifest (permissions, content scripts)
├── popup.html             # Main popup UI
├── popup.js               # Popup logic and feature coordination
├── background.js          # Service worker (tab events, redirects, storage)
├── content.js             # Injected into pages (dark mode, CSS, GDPR, etc.)
├── features/              # Individual feature modules (if separated)
├── icons/                 # Extension icons
└── demo.gif               # Demo animation
```

## manifest.json Key Patterns

```json
{
  "manifest_version": 3,
  "name": "SuperLevels",
  "version": "1.0",
  "permissions": [
    "tabs",
    "cookies",
    "storage",
    "scripting",
    "webNavigation",
    "activeTab"
  ],
  "host_permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_start"
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon48.png"
  }
}
```

## Storage Pattern (All Features)

SuperLevels uses `chrome.storage.local` exclusively — no external storage:

```javascript
// Save a setting
async function saveSetting(key, value) {
  await chrome.storage.local.set({ [key]: value });
}

// Load a setting with default
async function loadSetting(key, defaultValue) {
  const result = await chrome.storage.local.get([key]);
  return result[key] !== undefined ? result[key] : defaultValue;
}

// Per-domain settings pattern
async function saveDomainSetting(feature, domain, value) {
  const storageKey = `${feature}_${domain}`;
  await chrome.storage.local.set({ [storageKey]: value });
}

async function loadDomainSetting(feature, domain, defaultValue) {
  const storageKey = `${feature}_${domain}`;
  const result = await chrome.storage.local.get([storageKey]);
  return result[storageKey] !== undefined ? result[storageKey] : defaultValue;
}
```

## Feature: Tab Cleaner

```javascript
// background.js — track tab activity
const tabLastActive = {};

chrome.tabs.onActivated.addListener(({ tabId }) => {
  tabLastActive[tabId] = Date.now();
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
  if (changeInfo.status === 'complete') {
    tabLastActive[tabId] = Date.now();
  }
});

async function cleanInactiveTabs() {
  const settings = await chrome.storage.local.get(['tabTimeout', 'excludedHosts']);
  const timeoutMs = (settings.tabTimeout || 5) * 60 * 1000;
  const excludedHosts = settings.excludedHosts || [];

  const tabs = await chrome.tabs.query({});
  const now = Date.now();

  for (const tab of tabs) {
    if (tab.active || tab.pinned) continue;

    const tabHost = new URL(tab.url).hostname;
    if (excludedHosts.some(h => tabHost.includes(h))) continue;

    const lastActive = tabLastActive[tab.id] || tab.lastAccessed || 0;
    if (now - lastActive > timeoutMs) {
      // Save to recently closed before removing
      await saveRecentlyClosed(tab);
      chrome.tabs.remove(tab.id);
    }
  }
}

async function saveRecentlyClosed(tab) {
  const { recentlyClosed = [] } = await chrome.storage.local.get(['recentlyClosed']);
  recentlyClosed.unshift({ url: tab.url, title: tab.title, closedAt: Date.now() });
  const trimmed = recentlyClosed.slice(0, 20); // keep last 20
  await chrome.storage.local.set({ recentlyClosed: trimmed });
}

// Run cleaner on interval
setInterval(cleanInactiveTabs, 60 * 1000);
```

## Feature: Dark Mode (Content Script)

```javascript
// content.js — dark mode via CSS filter
function applyDarkMode(brightness = 90) {
  let style = document.getElementById('superlevels-darkmode');
  if (!style) {
    style = document.createElement('style');
    style.id = 'superlevels-darkmode';
    document.head.appendChild(style);
  }
  style.textContent = `
    html {
      filter: invert(1) hue-rotate(180deg) brightness(${brightness}%) !important;
    }
    img, video, canvas, iframe, svg, picture {
      filter: invert(1) hue-rotate(180deg) !important;
    }
  `;
}

function removeDarkMode() {
  const style = document.getElementById('superlevels-darkmode');
  if (style) style.remove();
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'setDarkMode') {
    if (msg.enabled) {
      applyDarkMode(msg.brightness || 90);
    } else {
      removeDarkMode();
    }
    sendResponse({ ok: true });
  }
});

// Auto-apply on load if enabled for this domain
(async () => {
  const domain = location.hostname;
  const { [`darkmode_${domain}`]: enabled, [`darkmode_brightness_${domain}`]: brightness }
    = await chrome.storage.local.get([`darkmode_${domain}`, `darkmode_brightness_${domain}`]);
  if (enabled) applyDarkMode(brightness || 90);
})();
```

## Feature: Live CSS Editor

```javascript
// content.js — inject and update custom CSS
function applyCustomCSS(css) {
  let style = document.getElementById('superlevels-custom-css');
  if (!style) {
    style = document.createElement('style');
    style.id = 'superlevels-custom-css';
    document.head.appendChild(style);
  }
  style.textContent = css;
}

// popup.js — save and send CSS as user types
const cssTextarea = document.getElementById('css-editor');
const domain = new URL((await chrome.tabs.query({ active: true, currentWindow: true }))[0].url).hostname;

cssTextarea.addEventListener('input', async () => {
  const css = cssTextarea.value;
  await chrome.storage.local.set({ [`css_${domain}`]: css });

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (css) => {
      let style = document.getElementById('superlevels-custom-css');
      if (!style) {
        style = document.createElement('style');
        style.id = 'superlevels-custom-css';
        document.head.appendChild(style);
      }
      style.textContent = css;
    },
    args: [css]
  });
});

// Handle Tab key for indentation
cssTextarea.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    e.preventDefault();
    const start = cssTextarea.selectionStart;
    const end = cssTextarea.selectionEnd;
    cssTextarea.value = cssTextarea.value.substring(0, start) + '  ' + cssTextarea.value.substring(end);
    cssTextarea.selectionStart = cssTextarea.selectionEnd = start + 2;
  }
});
```

## Feature: Music Recognizer (ACRCloud)

Requires your own ACRCloud API credentials — sign up free at https://www.acrcloud.com/sign-up/

```javascript
// popup.js — capture tab audio and identify
async function recognizeMusic() {
  const settings = await chrome.storage.local.get(['acrcloud_host', 'acrcloud_key', 'acrcloud_secret']);

  if (!settings.acrcloud_host || !settings.acrcloud_key || !settings.acrcloud_secret) {
    showError('Add your ACRCloud API credentials in settings first.');
    return;
  }

  // Capture audio from current tab (10 seconds)
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const stream = await chrome.tabCapture.capture({ audio: true, video: false });

  const audioContext = new AudioContext();
  const source = audioContext.createMediaStreamSource(stream);
  const processor = audioContext.createScriptProcessor(4096, 1, 1);
  const chunks = [];

  processor.onaudioprocess = (e) => {
    chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
  };

  source.connect(processor);
  processor.connect(audioContext.destination);

  await new Promise(resolve => setTimeout(resolve, 10000)); // record 10s

  stream.getTracks().forEach(t => t.stop());
  processor.disconnect();

  // Convert to WAV and send to ACRCloud
  const wavBlob = float32ArrayToWav(chunks, audioContext.sampleRate);
  const result = await queryACRCloud(wavBlob, settings);

  // Save to history
  if (result?.metadata?.music?.[0]) {
    const song = result.metadata.music[0];
    const { recognitionHistory = [] } = await chrome.storage.local.get(['recognitionHistory']);
    recognitionHistory.unshift({
      title: song.title,
      artist: song.artists?.[0]?.name,
      album: song.album?.name,
      recognizedAt: Date.now()
    });
    await chrome.storage.local.set({ recognitionHistory: recognitionHistory.slice(0, 50) });
  }
}

async function queryACRCloud(audioBlob, { acrcloud_host, acrcloud_key, acrcloud_secret }) {
  const timestamp = Math.floor(Date.now() / 1000);
  const stringToSign = `POST\n/v1/identify\n${acrcloud_key}\naudio\n1\n${timestamp}`;

  // HMAC-SHA1 signature (use SubtleCrypto)
  const encoder = new TextEncoder();
  const keyData = encoder.encode(acrcloud_secret);
  const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-1' }, false, ['sign']);
  const signature = btoa(String.fromCharCode(...new Uint8Array(
    await crypto.subtle.sign('HMAC', cryptoKey, encoder.encode(stringToSign))
  )));

  const formData = new FormData();
  formData.append('sample', audioBlob, 'sample.wav');
  formData.append('access_key', acrcloud_key);
  formData.append('data_type', 'audio');
  formData.append('signature_version', '1');
  formData.append('signature', signature);
  formData.append('sample_bytes', audioBlob.size);
  formData.append('timestamp', timestamp);

  const response = await fetch(`https://${acrcloud_host}/v1/identify`, {
    method: 'POST',
    body: formData
  });
  return response.json();
}
```

## Adding a New Feature

Follow this pattern to add a feature:

```javascript
// 1. Add toggle in popup.html
// <div class="feature" id="my-feature">
//   <label>My Feature</label>
//   <input type="checkbox" id="my-feature-toggle">
// </div>

// 2. popup.js — wire up the toggle
const myFeatureToggle = document.getElementById('my-feature-toggle');
const domain = await getCurrentDomain();

// Load saved state
myFeatureToggle.checked = await loadDomainSetting('myfeature', domain, false);

myFeatureToggle.addEventListener('change', async () => {
  const enabled = myFeatureToggle.checked;
  await saveDomainSetting('myfeature', domain, enabled);

  // Send message to content script
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.sendMessage(tab.id, { action: 'setMyFeature', enabled });
});

// 3. content.js — handle the message
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action === 'setMyFeature') {
    if (msg.enabled) enableMyFeature();
    else disableMyFeature();
  }
});

// 4. Auto-apply on page load
(async () => {
  const domain = location.hostname;
  const enabled = await loadDomainSetting('myfeature', domain, false);
  if (enabled) enableMyFeature();
})();
```

## Feature: GDPR Consent Banner Dismisser

```javascript
// content.js — auto-dismiss consent banners
const GDPR_SELECTORS = [
  // OneTrust
  '#onetrust-accept-btn-handler',
  '.onetrust-accept-btn-handler',
  // CookieBot
  '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
  // Didomi
  '#didomi-notice-agree-button',
  // Quantcast
  '.qc-cmp2-summary-buttons button:last-child',
  // Generic
  '[id*="cookie"] [id*="accept"]',
  '[class*="cookie-consent"] button',
  '[aria-label*="Accept cookies"]',
  '[aria-label*="accept all"]',
];

const GDPR_HIDE_SELECTORS = [
  '#onetrust-consent-sdk',
  '.cookiebot-widget',
  '#didomi-host',
  '.qc-cmp2-container',
  '[class*="cookie-banner"]',
  '[id*="cookie-banner"]',
  '[class*="gdpr-banner"]',
];

function dismissGDPRBanners() {
  // Click accept buttons
  for (const selector of GDPR_SELECTORS) {
    const btn = document.querySelector(selector);
    if (btn) { btn.click(); break; }
  }

  // Hide banner containers
  for (const selector of GDPR_HIDE_SELECTORS) {
    const el = document.querySelector(selector);
    if (el) el.style.setProperty('display', 'none', 'important');
  }
}

// Run on load and watch for dynamically injected banners
dismissGDPRBanners();
const observer = new MutationObserver(dismissGDPRBanners);
observer.observe(document.body, { childList: true, subtree: true });
```

## Common Patterns

### Get Current Tab Domain
```javascript
async function getCurrentDomain() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try {
    return new URL(tab.url).hostname;
  } catch {
    return null;
  }
}
```

### Send Message to Content Script
```javascript
async function sendToContentScript(action, data = {}) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try {
    return await chrome.tabs.sendMessage(tab.id, { action, ...data });
  } catch (e) {
    // Content script not yet loaded — inject it
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js']
    });
    return chrome.tabs.sendMessage(tab.id, { action, ...data });
  }
}
```

### Reload Tab After Permission Change
```javascript
async function applyAndReload(settingKey, value) {
  await chrome.storage.local.set({ [settingKey]: value });
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.reload(tab.id);
}
// Used by JS Toggle, since disabling JS requires a content settings reload
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Extension not appearing | Check Developer mode is on, reload at `chrome://extensions/` |
| Content script not running | Verify `manifest.json` `matches` includes the site's URL pattern |
| Storage not persisting | Use `chrome.storage.local` not `localStorage` (unavailable in service workers) |
| `chrome.tabCapture` fails | Music Recognizer needs `tabCapture` permission in manifest and only works on HTTP/HTTPS pages |
| GDPR dismisser breaking a site | Toggle it off per-domain via popup; the site may use a non-standard framework |
| Dark mode looks wrong on images | Ensure the double-invert rule targets `img, video, canvas, iframe, svg, picture` |
| `chrome.scripting` blocked | Add the target URL's origin to `host_permissions` in manifest |
| MV3 service worker sleeping | Move persistent state to `chrome.storage` not in-memory variables |

## Security Audit

To audit before using:
```bash
# Clone and inspect
git clone https://github.com/levelsio/superlevels.git

# Ask your AI tool:
# "Analyze this Chrome extension for security vulnerabilities,
#  malware, spyware, data exfiltration, and suspicious behavior"
```

Key things to verify: no `fetch`/`XMLHttpRequest` to unexpected hosts, no `eval()` usage, no external scripts loaded, all storage is `chrome.storage.local` only.
