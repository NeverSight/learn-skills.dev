---
name: access-travel-integration
description: |
  Integrate the Access Development Travel Platform into any web application.
  Guides you through server-side authentication, JavaScript SDK embedding, deep linking
  to all product lines (hotels, cars, theme parks, activities, flights), and
  event handling — in any backend language.
trigger: |
  Use when the developer wants to integrate the Access Development Travel Platform,
  embed the travel booking SDK, generate a session token, deep link to hotels/cars/
  theme-parks/attractions/activities/flights, or troubleshoot an existing Access
  travel integration.
---

# Access Development — Travel Platform Integration Skill

You are an expert integration engineer for the **Access Development Travel Platform**. Your job is to help developers embed the travel booking experience into their web applications regardless of their backend language or framework.

## How to use this skill

When a developer asks for help integrating the Access Travel Platform, follow the progressive disclosure pattern below. Start with the **Quick-Start Journey** that matches their need, then drill into the relevant reference sections as questions arise.

---

## 1 — Architecture Overview

```
┌─────────────────────┐         ┌──────────────────────────────┐
│  Client's Backend   │ ── 1 ──▶│  Access Authentication       │
│  (any language)     │ ◀── 2 ──│  Provider (auth.adcrws.com)  │
└────────┬────────────┘         └──────────────────────────────┘
         │ 3 (pass session_token)
         ▼
┌─────────────────────┐         ┌──────────────────────────────┐
│  Client's Frontend  │ ── 4 ──▶│  Travel Platform iframe      │
│  (browser / webview)│ ◀── 5 ──│  (booking.accessdevelopment  │
└─────────────────────┘         │         .com)                │
                                └──────────────────────────────┘
```

1. Backend POSTs to `/api/v1/tokens` with API key + member_key → receives `session_token`
2. Token is short-lived (5 min), single-use, and validated server-to-server
3. Backend passes `session_token` to the browser
4. Browser SDK (`travel.client.v2.js`) initialises an iframe with the token
5. The platform renders inside the iframe; events flow back via `postMessage`

---

## 2 — Quick-Start Journeys

### Journey A — "I want the full travel platform embedded"

Guide the developer through these steps in order:

1. **Server-side: obtain a session token** (see §3)
2. **Client-side: load the SDK and call `start()`** (see §4)
3. **Handle events** (see §6)
4. **Go live checklist** (see §9)

### Journey B — "I want to deep link to a specific product"

1. Complete Journey A steps 1–2
2. Use the `navigate_to` parameter in `start()` or call `navigateTo()` at runtime (see §5)

### Journey C — "I'm building a mobile app"

1. Build a thin server-rendered page that performs Journey A
2. Load that page inside a **WKWebView** (iOS) or **WebView** (Android)
3. Implement native ↔ webview bridge callbacks to detect SDK events
4. See §8 for mobile-specific guidance

---

## 3 — Server-Side: Session Token Retrieval

### Endpoint

| Field | Value |
|---|---|
| Method | `POST` |
| Production URL | `https://auth.adcrws.com/api/v1/tokens` |
| Staging URL | `https://auth.adcrws-stage.com/api/v1/tokens` |
| Auth | `Authorization: Bearer <API_KEY>` |
| Content-Type | `application/json` |

### Request body

| Parameter | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `member_key` | string | Yes | 1-255 chars, `^[a-zA-Z0-9\-_]{1,255}$` | Unique identifier for the end-user in your system |
| `scope` | string | Yes | `travel` &#124; `offer` &#124; `deals` | Set to `travel` for the travel platform |
| `first_name` | string | No | Max 255 chars | End-user's first name (used to create member record) |
| `last_name` | string | No | Max 255 chars | End-user's last name |
| `email` | string | No | Valid email (RFC 5322) | End-user's email |
| `click_id` | string | No | `^[a-zA-Z0-9]+$` | Affiliate/partner tracking ID |

### Response (200 OK)

```json
{
  "session_token": "ACCESS_SESSION_a1B2c3D4e5F6g7H8i9J0kLmNoPqRsTuV"
}
```

### Error responses

| Status | Meaning | Action |
|---|---|---|
| 400 | Validation error (missing/invalid fields) | Fix request body per constraints above |
| 401 | Invalid or expired API key, wrong scope | Verify API key with your Access contact |
| 429 | Rate limited (default 200 req/min/key) | Respect `Retry-After` header (seconds) |
| 500 | Upstream service failure | Retry with exponential backoff |

### Token lifecycle

- Expires after **5 minutes** if unused
- **Invalidated after first use** (single-use)
- Each page load / SDK initialization requires a fresh token
- Tokens are opaque — do not parse or store them long-term

### Language-agnostic code templates

When generating code, adapt the following pattern to whatever language/framework the developer is using.

**Pattern (pseudocode):**

```
function getSessionToken(memberKey, apiKey):
    response = HTTP_POST(
        url   = "https://auth.adcrws.com/api/v1/tokens",
        headers = {
            "Authorization": "Bearer " + apiKey,
            "Content-Type":  "application/json"
        },
        body = {
            "member_key": memberKey,
            "scope":      "travel"
        }
    )

    if response.status == 429:
        wait(response.headers["Retry-After"] seconds)
        return getSessionToken(memberKey, apiKey)  // retry once

    if response.status != 200:
        raise Error("Token request failed: " + response.status)

    return response.body.session_token
```

**Example — Node.js (Express):**

```javascript
app.get("/travel-token", async (req, res) => {
  const response = await fetch("https://auth.adcrws.com/api/v1/tokens", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.ACCESS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      member_key: req.user.id,   // your authenticated user's unique ID
      scope: "travel",
    }),
  });

  if (!response.ok) {
    return res.status(502).json({ error: "Failed to obtain session token" });
  }

  const { session_token } = await response.json();
  res.json({ session_token });
});
```

> **Security reminder:** The API key must NEVER be exposed to the browser. Always proxy the token request through your backend.
>
> The pseudocode pattern and Node.js example above are sufficient to generate correct implementations in any language. Adapt the HTTP POST pattern to the developer's framework.

---

## 4 — Client-Side: SDK Embedding

### Step 1 — Include the script

```html
<script src="https://booking.accessdevelopment.com/scripts/travel.client.v2.js"></script>
```

### Step 2 — Add a container element

```html
<div id="travel-container"></div>
```

### Step 3 — Initialize the SDK

```javascript
// Fetch a fresh session token from YOUR backend
const { session_token } = await fetch("/travel-token").then(r => r.json());

window.travelClient.start({
  session_token,                   // required
  container: "#travel-container",  // required — CSS selector
  width: "100%",                   // optional (default "100%")
  height: "fit",                   // optional (default "fit" — auto-resize)
  language: "en",                  // optional (en|es|fr|pt|zh)
  navigate_to: {                   // optional — deep link on load
    view: "home",
    start_tab: "hotels"
  }
});
```

### `start()` parameter reference

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `session_token` | string | Yes | — | Token from §3 |
| `container` | string | Yes | — | CSS selector for target element |
| `width` | string/number | No | `"100%"` | Width of iframe (`"100%"`, `"fit"`, or pixels) |
| `height` | string/number | No | `"fit"` | Height of iframe (`"fit"` auto-resizes, or pixels) |
| `language` | string | No | `"en"` | `en`, `es`, `fr`, `pt`, `zh` |
| `navigate_to` | object | No | — | Deep link object (see §5) |

### Display requirements

| Context | Min Width | Min Height | Recommended |
|---|---|---|---|
| Desktop / Tablet | 95% device width | 80% viewport height | 100% available space |
| Mobile | 320px (95% width) | 600px (80% height) | 360px+ width |

> Use `height: "fit"` for responsive design. Some features (maps, checkout) require sufficient height to be usable.

---

## 5 — Deep Linking

Use `navigate_to` in `start()` or call `travelClient.navigateTo()` at runtime. For full parameter details (required/optional fields, defaults, formats), see `references/deep-link-quick-reference.md`.

### Examples by view

```javascript
// Home
{ view: "home", start_tab: "hotels" }

// Hotels
{ view: "hotels", destination: "Orlando, FL, US", lat: 28.5383, lon: -81.3792,
  check_in: "2026-04-01", check_out: "2026-04-05", adults: 2, children: 1, child_ages: "8", rooms: 1 }

// Cars
{ view: "cars", destination: "MCO - Orlando International Airport - Orlando United States",
  pickup_date_time: "2026-04-01T_12:00", return_date_time: "2026-04-05T_12:00" }

// Theme park (direct)
{ view: "parks", attraction_id: "attr_0C25GYH4G9QA7" }

// Theme park (search)
{ view: "parks_search", destination: "Orlando, FL, US", lat: 28.5383, lon: -81.3792, category: "Amusement%20Park" }

// Activities
{ view: "activities", destination: "Orlando, FL, US", lat: 28.5383, lon: -81.3792,
  start_date: "2026-04-01", end_date: "2026-04-05" }

// Flights (no additional params)
{ view: "flights" }
```

> **Attraction IDs:** Run `bash scripts/fetch-attractions.sh` to refresh `references/attractions-and-identifiers.json`, then read it to look up the correct `attraction_id`.

### Runtime navigation

```javascript
travelClient.navigateTo({ view: "hotels", destination: "Portland, OR, US", lat: 45.5231, lon: -122.6765 });
travelClient.updateLanguage("es");  // en, es, fr, pt, zh — reloads the current view
```

---

## 6 — Event Handling

Register listeners with `travelClient.on(type, callback)`.

### 6.1 Error events

```javascript
travelClient.on("error", (event) => {
  console.error(event.error_code, event.error_message);
  // event.error_type: "error" (fatal) | "warn" (non-fatal)
  // event.status: HTTP-like status code (e.g. 400)
});
```

Example error:
```json
{
  "error_code": "MISSING_SESSION_TOKEN",
  "error_message": "Required: session_token property is required for start method.",
  "error_type": "error",
  "status": 400
}
```

### 6.2 Update events

```javascript
travelClient.on("update", (event) => {
  switch (event.update_code) {
    case "TRAVEL_CLIENT_LOADED":
      // SDK authenticated and visual loading started
      break;
    case "ACTIVE_SESSION_PING":
      // User interaction detected — use to track activity
      break;
    case "SESSION_NOT_FOUND":
      // No active session — re-authenticate
      break;
    case "TRAVEL_CLIENT_SESSION_EXPIRED":
      // Idle for 60 minutes — prompt re-login
      break;
  }
});
```

### 6.3 User interaction events

```javascript
travelClient.on("event", (event) => {
  // event.event_code — e.g. "FLIGHT_SEARCH"
  // event.event_detail — JSON object with event specifics
  // event.event_dts — ISO 8601 timestamp
});
```

### Session management best practice

The platform expires sessions after **60 minutes of inactivity**. Use `ACTIVE_SESSION_PING` to track user activity and implement your own shorter timeout if desired. When `SESSION_NOT_FOUND` or `TRAVEL_CLIENT_SESSION_EXPIRED` fires, request a new token from your backend and re-initialize the SDK.

---

## 7 — CSP & Domain Whitelisting

> **Common blocker:** Your domain must be whitelisted in Access Development's CSP before the integration will work (wildcard subdomains are supported). Coordinate with your Access Integration Manager. If your site uses a CSP, allowlist `*.accessdevelopment.com`, `*.adcrws.com`, and payment/map provider domains (`*.mapbox.com`, `js.stripe.com`, `*.braintreegateway.com`). The SDK does **not** load on `localhost` — use a custom local domain (e.g. `dev.yoursite.com` pointed to 127.0.0.1) and have it whitelisted for development.

---

## 8 — Mobile App Integration

For native iOS/Android apps:

1. Build a server-rendered page on your backend that performs the SDK initialization (§3 + §4)
2. Load that page in a **WKWebView** (iOS) or **WebView** (Android)
3. The SDK works identically inside webviews — all methods (`start`, `navigateTo`, `on`) function normally
4. Use your platform's native ↔ JavaScript bridge (iOS: `WKScriptMessageHandler` / `evaluateJavaScript`; Android: `addJavascriptInterface`) to listen for SDK events
5. Ensure the webview is fully loaded before displaying it to the user

---

## 9 — Go-Live Checklist

| Step | Details |
|---|---|
| Obtain API key | Contact your Access Integration Manager |
| Whitelist domains | All production + staging domains (wildcard subdomains supported) |
| Implement token endpoint | Server-side, never expose API key to browser |
| Embed SDK | Load `travel.client.v2.js`, call `start()` |
| Handle errors & session expiry | Listen for `error` and `update` events |
| Verify display sizing | Min 320px wide, 600px tall on mobile |
| Provide branding assets | Logo and program name for confirmation emails |
| BIN configuration (optional) | Restrict accepted card types for hotels/cars |
| Test end-to-end | Use staging environment first (`auth.adcrws-stage.com`) |
| Coordinate go-live | With Access Integration Manager |

---

## 10 — Supported Languages

| Code | Language |
|---|---|
| `en` | English (default) |
| `es` | Spanish |
| `fr` | French |
| `pt` | Portuguese |
| `zh` | Chinese (Traditional) |

---

## 11 — Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| SDK not loading | CSP blocking `booking.accessdevelopment.com` | Add to `script-src` and `frame-src` |
| SDK not loading on localhost | Localhost not supported | Use a custom local domain and whitelist it |
| `MISSING_SESSION_TOKEN` error | Token not passed to `start()` | Verify backend is returning token and frontend is forwarding it |
| 401 on `/api/v1/tokens` | Invalid/expired API key | Verify key with Access Integration Manager |
| 429 on `/api/v1/tokens` | Rate limited (200 req/min) | Implement `Retry-After` header backoff |
| Token expired before SDK loads | Token TTL is 5 minutes | Generate token just before calling `start()`, not at page load |
| Session expired unexpectedly | 60-min inactivity timeout | Listen for `TRAVEL_CLIENT_SESSION_EXPIRED`, re-initialize |
| iframe too short / features unusable | Insufficient height | Use `height: "fit"` or ensure min 600px |
| Deep link not working | Missing required parameters | Check §5 — e.g. hotels requires `destination` + `lat` + `lon` |
| Attraction not found | Wrong ID format | Use `attr_<ID>` format from the identifiers page |

---

## 12 — Complete Integration Example

A full minimal example bringing everything together:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Travel Benefits</title>
  <script src="https://booking.accessdevelopment.com/scripts/travel.client.v2.js"></script>
  <style>
    #travel-container { width: 100%; min-height: 80vh; }
  </style>
</head>
<body>
  <div id="travel-container"></div>

  <script>
    async function initTravel() {
      // 1. Get a fresh token from YOUR backend
      const res = await fetch("/travel-token");
      if (!res.ok) {
        console.error("Failed to get session token");
        return;
      }
      const { session_token } = await res.json();

      // 2. Initialize the SDK
      window.travelClient.start({
        session_token,
        container: "#travel-container",
        height: "fit",
        navigate_to: { view: "home", start_tab: "hotels" }
      });

      // 3. Handle events
      travelClient.on("error", (e) => {
        console.error("Travel SDK error:", e.error_code, e.error_message);
      });

      travelClient.on("update", (e) => {
        if (e.update_code === "TRAVEL_CLIENT_SESSION_EXPIRED") {
          // Re-initialize with a fresh token
          initTravel();
        }
      });
    }

    initTravel();
  </script>
</body>
</html>
```

---

## Instruction to the LLM

When helping a developer with this integration:

1. **Ask what product lines they need** (hotels, cars, parks, activities, flights, all) and what backend language they use.
2. **Generate server-side token code** in their language using the patterns in §3.
3. **Generate client-side embedding code** per §4, including only the deep links they need from §5.
4. **Always include error/event handling** from §6.
5. **Warn about CSP and domain whitelisting** — these are the most common blockers.
6. **Never expose the API key to the browser** — always proxy through the backend.
7. **For attraction deep links**, run `bash scripts/fetch-attractions.sh` to ensure the local reference is current, then read `references/attractions-and-identifiers.json` to look up the correct `attraction_id`.
8. **For mobile**, always recommend the webview approach from §8.
9. **Use staging URLs** (`auth.adcrws-stage.com`) during development, production URLs (`auth.adcrws.com`) for go-live.
