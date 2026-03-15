---
name: line-liff
version: 0.1.0
description: Comprehensive reference for LINE Front-end Framework (LIFF) SDK — building web apps inside LINE with authentication, messaging, QR scanning, permanent links, pluggable SDK, and LIFF plugin development. This skill should be used when the user asks to "build a LIFF app", "initialize liff.init()", "send messages from LIFF", "use Share Target Picker", "scan a QR code in LIFF", "create a permanent link", "develop a LIFF plugin", or mentions LIFF SDK, LINE Front-end Framework, CDN/npm integration, pluggable SDK tree-shaking, LIFF-to-LIFF transitions, LIFF browser vs external browser, Endpoint URL configuration, or server-side ID token verification from LIFF. Always use this skill whenever the user mentions LIFF, web apps inside LINE, or LINE Front-end Framework, even if they don't explicitly say "LIFF SDK".
---

# LINE LIFF (Front-end Framework)

**Do not answer LIFF questions from memory — LINE updates APIs frequently and training data is unreliable. Always consult the references below.**

Reference for building, reviewing, and debugging LIFF web apps inside LINE.

## Workflow

### Build
1. Read [references/guidelines.md](references/guidelines.md) (registration, endpoint URL rules, environment compatibility)
2. Load the relevant reference for the feature being implemented
3. For architecture or design choices, consult [references/experts.md](references/experts.md) for directional guidance
4. Write code following specs and constraints from references

### Review / Debug
1. Read [references/guidelines.md](references/guidelines.md) (URL constraints, authentication flow, API availability)
2. Load relevant references for the code being reviewed
3. Cross-check code against specs (endpoint URL rules, scope requirements, environment limitations, init order)
4. For design pattern concerns, consult [references/experts.md](references/experts.md)
5. Report violations with reference to specific constraints

## Environment Variables

```
LIFF_ID=LIFF app ID (from LINE Developers Console)
LINE_LOGIN_CHANNEL_ID=LINE Login Channel ID (for server-side JWT verification)
LINE_LOGIN_CHANNEL_SECRET=Channel secret (server-side only)
CHANNEL_ACCESS_TOKEN=Channel access token (for LIFF Server API — manage LIFF apps programmatically)
```

## SDK

Install via CDN or npm. For tree-shaking (reduce ~34% bundle size), use pluggable SDK.

SDK installation, CDN/npm setup, pluggable SDK → **[references/api.md § Pluggable SDK](references/api.md)**

## Initialization

```javascript
liff.init({ liffId: 'YOUR_LIFF_ID', withLoginOnExternalBrowser: true })
  .then(() => { /* use LIFF APIs */ })
  .catch(err => console.error(err.code, err.message));
```

- Must be called before all LIFF APIs (except pre-init methods)
- `withLoginOnExternalBrowser: true` — auto-trigger login in external browser
- `liff.ready` — Promise that resolves when init completes

## Getting Started

1. Create a **LINE Login channel** in [LINE Developers Console](https://developers.line.biz/console/)
2. Add a **LIFF app** and set the **Endpoint URL** (HTTPS required)
3. Integrate SDK, call `liff.init()`
4. Or scaffold with `npx @line/create-liff-app` (React/Vue/Svelte/Next.js/Nuxt/vanilla)

## Core API Summary

### Authentication & Profile
| Method | Description | Scope |
|--------|-------------|-------|
| `liff.isLoggedIn()` | Check login status | — |
| `liff.login()` | Trigger login (external browser only) | — |
| `liff.logout()` | Log out | — |
| `liff.getProfile()` | Get userId, displayName, pictureUrl | `profile` |
| `liff.getDecodedIDToken()` | Get decoded JWT (email, etc.) | `openid` + `email` |
| `liff.getIDToken()` | Get raw JWT (for server verification) | `openid` |
| `liff.getFriendship()` | Check friendship with linked OA | `profile` |

### Messaging
| Method | Description | Restriction |
|--------|-------------|------------|
| `liff.sendMessages([...])` | Send to current chat (max 5) | LIFF browser only |
| `liff.shareTargetPicker([...])` | Pick friends/groups to share | Check `isApiAvailable` first |

### Device & Navigation
| Method | Description |
|--------|-------------|
| `liff.scanCodeV2()` | QR code scanner (enable in Console) |
| `liff.openWindow({url, external})` | Open URL |
| `liff.closeWindow()` | Close LIFF (unreliable in external browser) |

### Context
| Method | Description |
|--------|-------------|
| `liff.getContext()` | Get type, userId, groupId, roomId, viewType |
| `liff.getOS()` | `'ios'`, `'android'`, `'web'` |
| `liff.isInClient()` | Whether running in LINE app |
| `liff.permanentLink.createUrlBy(url)` | Create permanent link |

## View Sizes

| Type | Coverage |
|------|----------|
| Full | 100% screen |
| Tall | ~75% |
| Compact | ~50% |

## Key Constraints

- **Endpoint URL**: `liff.init()` only works at or below the registered Endpoint URL
- **URL handling**: modify URLs only after `liff.init()` resolves
- **Universal Links**: use `https://liff.line.me/{liffId}` as primary entry point
- **Token security**: send raw ID Token to server for verification, never expose decoded token → see [server-auth.md](references/server-auth.md)
- **Login behavior differs**: auto in LIFF browser, manual in external browser
- **Deprecated APIs**: `liff.scanCode()` → use `scanCodeV2()`; `liff.getLanguage()` → use `getAppLanguage()`; `liff.permanentLink.createUrl()` → use `createUrlBy()` (may be removed in v3)

## Reference Index

| File | Topic |
|------|-------|
| [references/api.md](references/api.md) | LIFF v2 API complete reference, pluggable SDK modules, error codes |
| [references/guidelines.md](references/guidelines.md) | Registration, endpoint URL rules, authentication flow, UI/UX, environment compatibility |
| [references/navigation.md](references/navigation.md) | LIFF URLs, liff.state, permanent links, LIFF-to-LIFF transitions, browser minimization |
| [references/plugins.md](references/plugins.md) | LIFF plugin development, hooks system, official plugins (Inspector, Mock) |
| [references/server-api.md](references/server-api.md) | LIFF Server API (v1) — programmatic LIFF app CRUD (create, update, list, delete) |
| [references/server-auth.md](references/server-auth.md) | Server-side ID Token (JWT) verification |
| [references/cli.md](references/cli.md) | LIFF CLI — local HTTPS dev server, app CRUD, Inspector debugging, ngrok |
| [references/experts.md](references/experts.md) | LIFF domain experts for architecture guidance |

## SDK & Tools

- **npm**: [@line/liff](https://www.npmjs.com/package/@line/liff)
- **Pluggable SDK**: `@line/liff/core` + individual modules
- **Official plugins**: [@line/liff-inspector](https://www.npmjs.com/package/@line/liff-inspector) | [@line/liff-mock](https://www.npmjs.com/package/@line/liff-mock)
- **LIFF CLI**: [CLI tool](https://developers.line.biz/en/docs/liff/cli-tool-introduction/) (create, serve, deploy, HTTPS dev server)
- **Create LIFF App**: `npx @line/create-liff-app` — scaffolding (React/Vue/Svelte/Next.js/Nuxt/vanilla, JS/TS)
- **LIFF Playground**: [liff-playground.netlify.app](https://liff-playground.netlify.app/) — online API testing
- **Starter app**: [line/line-liff-v2-starter](https://github.com/line/line-liff-v2-starter) (vanilla/Next.js/Nuxt)
