---
name: codex-oauth-automation-extension
description: Chrome extension for automating OpenAI OAuth registration flows with captcha retrieval, CPA callback verification, and auto-recovery across multiple rounds
triggers:
  - automate openai oauth registration
  - chrome extension oauth signup automation
  - batch chatgpt account registration
  - duckduckgo email automation openai
  - cpa oauth verification extension
  - automate signup verification code retrieval
  - multi-round oauth automation chrome
  - inbucket mailbox verification automation
---

# Codex OAuth Automation Extension

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Chrome extension that automates the full OpenAI OAuth registration/login flow including email verification, CPA callback handling, and multi-round batch execution. Supports DuckDuckGo, QQ Mail, 163 Mail, and Inbucket as verification code sources.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/QLHazyCoder/codex-oauth-automation-extension.git
cd codex-oauth-automation-extension
```

2. Load in Chrome:
   - Navigate to `chrome://extensions/`
   - Enable **Developer mode** (top right toggle)
   - Click **Load unpacked**
   - Select the project directory

3. Open the side panel from the Chrome toolbar to configure and run.

## Project Structure

```
background.js              # Main orchestrator: steps 1–9, tab management, state
manifest.json              # Extension manifest
data/names.js              # Random name/birthday data
content/utils.js           # Shared helpers: waitForElement, click, stop control
content/vps-panel.js       # CPA panel: Step 1 / Step 9
content/signup-page.js     # OpenAI signup/login: Steps 2/3/5/6/8
content/duck-mail.js       # DuckDuckGo @duck.com address generation
content/qq-mail.js         # QQ Mail OTP polling
content/mail-163.js        # 163 Mail OTP polling
content/inbucket-mail.js   # Inbucket mailbox OTP polling
sidepanel/                 # Sidebar UI (HTML/CSS/JS)
```

## Configuration (Side Panel Fields)

| Field | Description | Example |
|---|---|---|
| `CPA` | Your OAuth management panel URL | `https://your-host/management.html#/oauth` |
| `Mail` | Verification code source | `163 Mail`, `QQ Mail`, or `Inbucket` |
| `Email` | Registration email (or click Auto for @duck.com) | `user@duck.com` |
| `Password` | Custom password; leave blank to auto-generate | `MyPass123!` |
| `Inbucket` | Inbucket host (only when Mail=Inbucket) | `your-inbucket-host` |
| `Mailbox` | Inbucket mailbox name (only when Mail=Inbucket) | `tmp-mailbox` |

### Storage Behavior

- **`chrome.storage.session`** — runtime state (steps, OAuth link, email, password, callback URL, tab info). Cleared when browser closes.
- **`chrome.storage.local`** — persistent config (CPA URL, password, mail service, Inbucket settings). Survives browser restarts.

## The 9-Step Workflow

### Step 1: Get OAuth Link
Opens CPA panel → finds `Codex OAuth` card → clicks login → extracts authorization URL → saves to `OAuth` field.

### Step 2: Open Signup
Opens the OAuth authorization link → locates and clicks `Sign up / Register / 创建账户` button.

### Step 3: Fill Email / Password
Fills registration form with email and password. Auto-generates strong password if field is blank. Actual password used is written back to the sidebar.

### Step 4: Get Signup Code
Polls the configured mailbox for a 6-digit OTP. Handles `Operation timed out` errors by auto-clicking retry.

**Email matching rules:**
- Sender contains: `openai`, `noreply`, `verify`, `auth`, `duckduckgo`, `forward`
- Subject contains: `verify`, `verification`, `code`, `验证`, `confirm`

### Step 5: Fill Name / Birthday
Generates random name and birthday. Handles two page variants:
- Birthday mode: fills year/month/day
- Age mode: fills `input[name='age']` directly

### Step 6: Login via OAuth
Re-fetches latest CPA OAuth link, then logs in with the newly registered account.

### Step 7: Get Login Code
Same as Step 4 but with login-specific keyword matching.

### Step 8: Manual OAuth Confirm (Auto-attempts)
- Locates the "Continue/Authorize" button on the OAuth consent page
- Uses Chrome `debugger` API to dispatch input events for the click
- Monitors `chrome.webNavigation.onBeforeNavigate` for localhost callback
- Only accepts: `http(s)://localhost:<port>/auth/callback?code=...&state=...`
- Timeout: 120 seconds

### Step 9: CPA Verify
- Validates callback URL has both `code` and `state` params
- Submits callback to CPA panel
- Waits for exact `认证成功！` status badge
- Closes residual `http://localhost:1455/auth*` tabs

## Auto Mode

Click **Auto** in the sidebar to run all 9 steps sequentially for N rounds (set by the number input).

```
Auto flow:
  Step 1 → Step 2 → [Duck email auto-fetch, retry up to 5x]
    ↓ (if Duck fails) → Pause, wait for manual email input → Continue
  Step 3 → Step 4 → Step 5 → Step 6 → Step 7 → Step 8 → Step 9
  → Repeat for N rounds
```

### Resuming After Pause

When Auto is paused and you reopen the sidebar, two options appear:
- **重新开始** — Reset progress, start new round from Step 1
- **继续当前** — Treat completed/skipped steps as done, resume from first unhandled step

## Key Code Patterns

### Waiting for Elements (content/utils.js pattern)
```javascript
// Wait for a DOM element with stop-signal support
async function waitForElement(selector, timeout = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    // Check stop signal from background
    const { stopFlow } = await chrome.storage.session.get('stopFlow');
    if (stopFlow) throw new Error('STOPPED');

    const el = document.querySelector(selector);
    if (el) return el;
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`Timeout waiting for: ${selector}`);
}
```

### Reading/Writing Session State (background.js pattern)
```javascript
// Save OAuth link to session
await chrome.storage.session.set({ oauthLink: extractedUrl });

// Read current email and password
const { currentEmail, currentPassword } = await chrome.storage.session.get([
  'currentEmail',
  'currentPassword'
]);

// Update step status
await chrome.storage.session.set({
  stepStatus: { ...existingStatus, step3: 'done' }
});
```

### Sending Messages to Content Scripts
```javascript
// background.js → content script
const [tab] = await chrome.tabs.query({ url: '*://chat.openai.com/*' });
const result = await chrome.tabs.sendMessage(tab.id, {
  action: 'FILL_EMAIL',
  email: 'user@duck.com',
  password: 'GeneratedPass1!'
});
```

### Inbucket Mailbox Polling (content/inbucket-mail.js pattern)
```javascript
// Only targets unread messages
const unseenEntries = document.querySelectorAll('.message-list-entry.unseen');
// From 2nd poll onwards, click the refresh button
if (pollCount > 1) {
  const refreshBtn = document.querySelector('[data-action="refresh"]');
  if (refreshBtn) refreshBtn.click();
  await sleep(1000);
}
// After reading, delete the email to avoid re-matching
```

### Chrome Debugger Click (content/signup-page.js pattern)
```javascript
// Attach debugger to tab for synthetic input events
await chrome.debugger.attach({ tabId }, '1.3');
const { x, y } = buttonBounds;
await chrome.debugger.sendCommand({ tabId }, 'Input.dispatchMouseEvent', {
  type: 'mousePressed', x, y, button: 'left', clickCount: 1
});
await chrome.debugger.sendCommand({ tabId }, 'Input.dispatchMouseEvent', {
  type: 'mouseReleased', x, y, button: 'left', clickCount: 1
});
await chrome.debugger.detach({ tabId });
```

### OAuth Callback Listener (background.js pattern)
```javascript
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only main frame, only the auth tab
  if (details.frameId !== 0) return;
  if (details.tabId !== authTabId) return;

  const url = details.url;
  // Strict: must be localhost /auth/callback with code + state
  if (/^https?:\/\/localhost:\d+\/auth\/callback\?/.test(url)) {
    const parsed = new URL(url);
    if (parsed.searchParams.get('code') && parsed.searchParams.get('state')) {
      await chrome.storage.session.set({ callbackUrl: url });
    }
  }
});
```

### Stop Signal Broadcasting
```javascript
// From sidebar: send stop
await chrome.runtime.sendMessage({ action: 'STOP_FLOW' });

// In background.js: set flag and broadcast to all content scripts
await chrome.storage.session.set({ stopFlow: true });
const tabs = await chrome.tabs.query({});
for (const tab of tabs) {
  chrome.tabs.sendMessage(tab.id, { action: 'STOP_FLOW' }).catch(() => {});
}
```

### DuckDuckGo Email Auto-Fetch
```javascript
// Triggered by sidebar "Auto" button next to Email field
// content/duck-mail.js opens:
// https://duckduckgo.com/email/settings/autofill
// Looks for existing private address or generates new one
const generateBtn = document.querySelector('[data-testid="generate-address"]');
if (generateBtn) generateBtn.click();
await waitForElement('.address-display');
const newAddress = document.querySelector('.address-display').textContent.trim();
```

## Persistent Config (chrome.storage.local)

```javascript
// Save config
await chrome.storage.local.set({
  cpaUrl: 'https://your-host/management.html#/oauth',
  mailService: 'Inbucket',        // '163 Mail' | 'QQ Mail' | 'Inbucket'
  inbucketHost: 'your-inbucket-host',
  inbucketMailbox: 'tmp-mailbox',
  customPassword: '',              // empty = auto-generate
});

// Load config
const config = await chrome.storage.local.get([
  'cpaUrl', 'mailService', 'inbucketHost', 'inbucketMailbox', 'customPassword'
]);
```

## Troubleshooting

### Step 8 timeout (120s exceeded)
- The OAuth consent page structure may have changed
- Manually click the "Continue" button and observe what URL the redirect hits
- Check the button selector in `content/signup-page.js`

### Step 4/7: OTP never arrives
- Verify the mail service tab is open and logged in before running
- For Inbucket: confirm `https://<host>/m/<mailbox>/` is accessible
- Check sender/subject filters — OpenAI sometimes changes sender addresses
- For QQ/163: ensure the webmail tab is the correct account

### Duck email auto-fetch fails (retries 5x then pauses)
- DuckDuckGo extension must be installed and logged in
- The autofill settings page URL may have changed
- Fall back to manual email entry in the sidebar

### CPA panel not detected (Step 1/9)
- Confirm your CPA URL matches `management.html#/oauth` path structure
- The `content/vps-panel.js` selectors are hardcoded to a specific panel layout
- Try running Step 1 manually to see console errors

### "Operation timed out" on signup (Step 4)
- This is handled automatically — the script clicks the retry button and re-submits
- If it loops, the OpenAI signup endpoint may be rate-limiting your IP

### Tab cleanup issues
- Old localhost tabs accumulate: Step 9 only cleans `http://localhost:1455/auth*`
- If your CPA uses a different port, update the cleanup filter in `background.js`

## Recommended Workflow

```
1. Configure sidebar (CPA URL, Mail service, credentials)
2. Run Step 1 manually → verify OAuth link appears
3. Run Steps 2-4 manually → confirm email + OTP flow works
4. If successful, enable Auto with N=5 for a test batch
5. Scale up rounds once flow is stable
```

> **Note:** Always test single-step flow before enabling Auto. The most fragile steps are Step 8 (OAuth consent click) and Step 4/7 (OTP timing). Use Inbucket for most reliable OTP delivery in automated runs.
