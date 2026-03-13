---
name: tracekit-session-replay
description: Set up TraceKit Session Replay to record and replay user sessions with linked distributed traces. Covers privacy settings, sampling rates, and GDPR compliance. Use when the user asks to record sessions, replay user interactions, or debug user-reported issues visually.
---

# TraceKit Session Replay

## When To Use

Use this skill when the user asks to:
- Record user sessions for debugging
- Replay what a user did before an error
- Set up visual debugging or session recording
- See what users did on the page
- Debug user-reported issues visually
- Add session replay to a frontend app

**Session replay is a browser-only feature.** It records DOM mutations, user interactions, and network requests to reconstruct a video-like replay of user sessions. Replays are linked to distributed traces so you can see the full backend context for any user action.

## Non-Negotiable Rules

1. **Never hardcode API keys** in code. Always use environment variables or build-time injection.
2. **Always enable privacy settings by default** -- `maskAllText: true` and `blockAllMedia: true` must be the starting configuration.
3. **Always include a verification step** confirming replays appear in `https://app.tracekit.dev/replays`.
4. **Always discuss GDPR/privacy implications** before enabling replay -- session recordings capture user behavior and may be subject to data protection regulations.

## Prerequisites

Session replay requires a frontend SDK to be installed and initialized. Complete **one** of the following SDK skills first:

- `tracekit-browser-sdk` -- Vanilla JavaScript/TypeScript
- `tracekit-react-sdk` -- React applications
- `tracekit-vue-sdk` -- Vue applications
- `tracekit-angular-sdk` -- Angular applications
- `tracekit-nextjs-sdk` -- Next.js applications
- `tracekit-nuxt-sdk` -- Nuxt applications

**Session replay is a BROWSER-ONLY feature.** It does not apply to backend SDKs (Node.js, Go, Python, etc.). If the user is working on a backend project, this skill does not apply.

## Detection

Before applying this skill, verify a frontend TraceKit SDK is installed:

1. **Check `package.json`** for any TraceKit frontend package:
   - `@tracekit/browser` -- vanilla JS/TS
   - `@tracekit/react` -- React
   - `@tracekit/vue` -- Vue
   - `@tracekit/angular` -- Angular
   - `@tracekit/nextjs` -- Next.js
   - `@tracekit/nuxt` -- Nuxt
2. If **none found**, redirect to `tracekit-browser-sdk` skill (or the appropriate framework skill) to install the SDK first.
3. **Check if replay is already configured** -- search for `@tracekit/replay` in `package.json` or `replayIntegration` in source files.

## Step 1: Install Replay Integration

```bash
npm install @tracekit/replay
```

The replay integration is a separate package that adds session recording capabilities to your existing TraceKit browser SDK.

## Step 2: Add Replay to SDK Init

Add the replay integration to your TraceKit initialization:

```javascript
import { init } from '@tracekit/browser';
import { replayIntegration } from '@tracekit/replay';

const replay = replayIntegration({
  // Privacy defaults -- ALWAYS start with these enabled
  maskAllText: true,
  blockAllMedia: true,
  maskAllInputs: true,
  networkCaptureBodies: false,
  networkDetailAllowUrls: [],
});

init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  addons: [replay],
});
```

## Step 3: Privacy Configuration

This is the most critical section. Session replay records user interactions, so privacy must be configured carefully before deploying to production.

### Text Masking

| Setting | Default | Description |
|---|---|---|
| `maskAllText: true` | **true** | Replaces all text content with asterisks (`****`). **Strongly recommended.** |
| `maskAllInputs: true` | **true** | Masks form input values (passwords, emails, search queries). |
| `unmask: ['.public-content']` | `[]` | CSS selectors for elements safe to show unmasked. Use sparingly. |
| `mask: ['.sensitive-class']` | `[]` | CSS selectors for additional elements to mask (supplements `maskAllText`). |

### Media Blocking

| Setting | Default | Description |
|---|---|---|
| `blockAllMedia: true` | **true** | Blocks images, videos, canvas elements from recording. **Strongly recommended.** |
| `block: ['.private-element']` | `[]` | CSS selectors for elements to block entirely (removed from recording). |

### Network Capture

| Setting | Default | Description |
|---|---|---|
| `networkCaptureBodies: false` | **false** | Capture HTTP request/response bodies. **Enable with extreme caution** -- may capture sensitive data. |
| `networkDetailAllowUrls: []` | `[]` | URLs to capture request/response details for. Empty array means none. |

**Example: Selective network capture for your own API only:**

```javascript
const replay = replayIntegration({
  maskAllText: true,
  blockAllMedia: true,
  maskAllInputs: true,
  networkCaptureBodies: true,
  networkDetailAllowUrls: [
    'https://api.myapp.com',  // Only capture bodies for your own API
  ],
});
```

### GDPR Considerations

Session replay records user behavior and may be subject to GDPR, CCPA, or other data protection regulations:

1. **Consent required** -- Display a consent banner before enabling session replay. Only start recording after the user consents.
2. **Data retention** -- Configure retention in the dashboard (Settings > Data Retention). Default is 30 days.
3. **Right to deletion** -- Users can request deletion of their session data. Use the TraceKit API to delete sessions by user ID.
4. **Data processing agreement** -- Ensure your TraceKit DPA covers session replay data.
5. **Privacy policy** -- Update your privacy policy to mention session recording.

**Conditional initialization based on consent:**

```javascript
import { init } from '@tracekit/browser';
import { replayIntegration } from '@tracekit/replay';

// Only add replay if user has consented
const addons = [];
if (userHasConsentedToRecording()) {
  addons.push(replayIntegration({
    maskAllText: true,
    blockAllMedia: true,
    maskAllInputs: true,
  }));
}

init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  addons,
});
```

## Step 4: Sampling Configuration

Control how many sessions are recorded to manage storage costs and volume.

```javascript
const replay = replayIntegration({
  // Sampling
  replaysSessionSampleRate: 0.1,   // Record 10% of all sessions
  replaysOnErrorSampleRate: 1.0,   // Record 100% of sessions with errors

  // Privacy
  maskAllText: true,
  blockAllMedia: true,
  maskAllInputs: true,
});
```

### Two-Tier Sampling Strategy

| Setting | Default | Purpose |
|---|---|---|
| `replaysSessionSampleRate` | `0.1` (10%) | General session recording for understanding user behavior. |
| `replaysOnErrorSampleRate` | `1.0` (100%) | Always record sessions where errors occur -- these are the most valuable for debugging. |

**How it works:**
- A session starts as a "general" session, sampled at `replaysSessionSampleRate`
- If an error occurs during the session, it is promoted to an "error" session and always captured (if `replaysOnErrorSampleRate` allows)
- Error sessions include a replay buffer of events before the error, so you see what led up to it

**Cost implications:**
- Higher `replaysSessionSampleRate` = more storage = higher bill
- Start with `0.1` (10%) for general sessions and `1.0` (100%) for error sessions
- Adjust based on traffic volume and budget

### Additional Replay Settings

| Setting | Default | Description |
|---|---|---|
| `minReplayDuration` | `5000` (5s) | Minimum session duration to record. Short sessions are discarded. |
| `maxReplayDuration` | `3600000` (1h) | Maximum recording duration. Long sessions are split. |

## Step 5: Linking Replays to Traces

When both session replay and distributed tracing are enabled, they are linked automatically. No additional configuration needed.

### View a Replay from a Trace

1. Open a trace in `https://app.tracekit.dev/traces`
2. If the trace originated from a browser session with replay, a **"View Replay"** button appears in the trace detail header
3. Click to jump to the replay at the exact moment the traced request occurred

### View a Trace from a Replay

1. Open a replay in `https://app.tracekit.dev/replays`
2. The replay timeline shows **event markers** for errors, network requests, and console logs
3. Click any event marker to see details, including the **Trace ID**
4. Click the Trace ID to jump to the full distributed trace waterfall

### Filter Replays

Use the replay list to find specific sessions:
- **By error type** -- find all sessions where a specific error occurred
- **By user** -- find all sessions for a specific user (requires `setUser()` in SDK)
- **By time range** -- find sessions during an incident window
- **By URL** -- find sessions that visited a specific page

## Step 6: Verification

Verify session replay is working:

1. **Start your application** with replay configured
2. **Navigate through a few pages** and interact with the UI (clicks, form inputs, page transitions)
3. **Visit** `https://app.tracekit.dev/replays`
4. **Find your session** in the replay list (most recent, filtered by your user or time)
5. **Click to play** the replay
6. **Verify privacy settings:**
   - Text should appear as `****` (if `maskAllText: true`)
   - Images and videos should be blocked (if `blockAllMedia: true`)
   - Form inputs should be masked (if `maskAllInputs: true`)
7. **Click an error marker** (if any) to verify it links to a distributed trace

## Troubleshooting

### Replays not appearing

- **Check sampling rate** -- `replaysSessionSampleRate: 0.1` means only 10% of sessions are recorded. Set to `1.0` during testing.
- **Check replay integration is added** -- verify `@tracekit/replay` is in `package.json` and `replayIntegration()` is passed to `addons`.
- **Check browser console** for errors from the TraceKit SDK. Enable `debug: true` in init config for verbose logging.
- **Check Content Security Policy** -- CSP must allow connections to `https://app.tracekit.dev`.

### All text visible (not masked)

- **Verify `maskAllText: true`** is set in the replay integration config.
- **Check for `unmask` selectors** -- elements matching `unmask` patterns are shown in clear text.
- **Rebuild and redeploy** -- config changes require a new deployment to take effect.

### Replay too short or cutting off

- **Check `minReplayDuration`** -- sessions shorter than this threshold are discarded (default 5 seconds).
- **Check `maxReplayDuration`** -- sessions longer than this are split into segments.
- **Check if user navigated away** -- replay stops when the user closes the tab or navigates to an external site.

### Large replay file sizes

- **Lower `replaysSessionSampleRate`** to reduce total recorded sessions.
- **Enable `blockAllMedia: true`** to exclude images and videos from recordings.
- **Reduce `networkCaptureBodies`** to `false` if enabled -- request bodies add significant size.

## Next Steps

Once session replay is working, consider:
- **Source Maps** (`tracekit-source-maps` skill) -- See readable stack traces in replay error markers instead of minified code
- **Alerts** (`tracekit-alerts` skill) -- Get notified when replay-captured errors spike

## References

- Session replay docs: `https://app.tracekit.dev/docs/frontend/session-replay`
- TraceKit docs root: `https://app.tracekit.dev/docs`
- Dashboard: `https://app.tracekit.dev`
