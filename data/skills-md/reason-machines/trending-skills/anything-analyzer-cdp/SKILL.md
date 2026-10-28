---
name: anything-analyzer-cdp
description: Electron desktop app that captures web traffic via Chrome DevTools Protocol and uses AI to generate protocol analysis reports
triggers:
  - analyze web protocol with AI
  - capture network requests with CDP
  - use anything-analyzer
  - generate protocol documentation from browser traffic
  - hook javascript fetch xhr with electron
  - analyze authentication flow with AI
  - capture SSE websocket traffic electron
  - reverse engineer web API protocol

---

# Anything Analyzer CDP Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Anything Analyzer is an Electron desktop application that embeds a browser, captures all network traffic via Chrome DevTools Protocol (CDP), injects JS hooks, snapshots storage, and feeds the data to an AI (OpenAI/Anthropic/custom) to generate protocol analysis reports — useful for documenting registration flows, 2API reverse engineering, and general browser protocol analysis.

## Installation & Setup

```bash
git clone https://github.com/MouseWW/anything-analyzer.git
cd anything-analyzer
pnpm install
pnpm dev        # development mode
pnpm build      # production build
```

**Windows native module build requirement:**
```bash
# Install Visual Studio Build Tools first, then:
pnpm install
# If better-sqlite3 fails:
pnpm rebuild
```

**Package as installer:**
```bash
pnpm run build && npx electron-builder --win
```

## Core Architecture

```
src/
├── main/                    # Electron main process
│   ├── ai/                  # AI analysis pipeline
│   │   ├── ai-analyzer.ts   # orchestrator
│   │   ├── data-assembler.ts# data preparation
│   │   ├── prompt-builder.ts# prompt generation
│   │   └── scene-detector.ts# rule-based scene classification
│   ├── capture/             # Capture engine
│   │   ├── capture-engine.ts# data sink → SQLite + renderer
│   │   ├── js-injector.ts   # hook script injection
│   │   └── storage-collector.ts # periodic storage snapshots
│   ├── cdp/
│   │   └── cdp-manager.ts   # CDP manager
│   ├── db/                  # SQLite via better-sqlite3
│   ├── session/
│   │   └── session-manager.ts # session lifecycle
│   ├── tab-manager.ts       # Multi-tab WebContentsView
│   ├── window.ts            # Main window layout
│   └── ipc.ts               # IPC handlers
├── preload/                 # Context bridge + hook script
├── renderer/                # React 19 + Ant Design 5 UI
└── shared/types.ts          # Shared TypeScript types
```

## Key Concepts

### Sessions
A **Session** scopes all captured data. Each session has a name, target URL, and contains all requests, JS hook events, and storage snapshots captured during that session.

### Capture Engine
The capture engine:
1. Attaches CDP to `WebContentsView` tabs
2. Enables `Fetch.enable` for request interception
3. Injects JS hooks via `Page.addScriptToEvaluateOnNewDocument`
4. Collects storage snapshots periodically

### AI Analysis Pipeline
1. **Scene detection** — rule-based classification (registration, OAuth, API auth, etc.)
2. **Data assembly** — selects relevant requests, deduplicates, truncates large bodies
3. **Prompt building** — constructs structured prompt with scene context
4. **LLM call** — streams response back to renderer

## Configuration

### LLM Provider Setup (Settings UI)
Configure via the Settings panel (bottom-left gear icon):

```typescript
// Config shape (stored in SQLite settings table)
interface LLMConfig {
  provider: 'openai' | 'anthropic' | 'custom';
  apiKey: string;      // from env or user input
  model: string;       // e.g. 'gpt-4o', 'claude-sonnet-4-20250514'
  baseUrl?: string;    // for custom OpenAI-compatible endpoints
}
```

**OpenAI:**
- API Key: `$OPENAI_API_KEY`
- Model: `gpt-4o` or `gpt-4o-mini`

**Anthropic:**
- API Key: `$ANTHROPIC_API_KEY`
- Model: `claude-sonnet-4-20250514`

**Custom (OpenAI-compatible):**
- Base URL: e.g. `https://api.deepseek.com/v1`
- API Key: your provider key
- Model: provider-specific model name

## IPC API (Main ↔ Renderer)

### Session Management
```typescript
// Create a session
const session = await window.electron.ipcRenderer.invoke('session:create', {
  name: 'My Analysis Session',
  url: 'https://example.com'
})

// List sessions
const sessions = await window.electron.ipcRenderer.invoke('session:list')

// Delete session
await window.electron.ipcRenderer.invoke('session:delete', sessionId)
```

### Capture Control
```typescript
// Start capturing for current tab
await window.electron.ipcRenderer.invoke('capture:start', { sessionId, tabId })

// Stop capturing
await window.electron.ipcRenderer.invoke('capture:stop', { sessionId, tabId })

// Get captured requests
const requests = await window.electron.ipcRenderer.invoke('capture:getRequests', sessionId)
```

### AI Analysis
```typescript
// Trigger AI analysis (streams back via IPC events)
await window.electron.ipcRenderer.invoke('analyze:start', { sessionId })

// Listen for streaming chunks
window.electron.ipcRenderer.on('analyze:chunk', (_, chunk: string) => {
  setReport(prev => prev + chunk)
})

// Listen for completion
window.electron.ipcRenderer.on('analyze:done', () => {
  setAnalyzing(false)
})
```

## Real Code Examples

### Extend the Scene Detector
```typescript
// src/main/ai/scene-detector.ts
import { CapturedRequest } from '../../shared/types'

export type Scene =
  | 'registration'
  | 'oauth'
  | 'api-auth'
  | 'websocket'
  | 'general'

export function detectScene(requests: CapturedRequest[]): Scene {
  const urls = requests.map(r => r.url.toLowerCase())
  const bodies = requests.map(r => r.requestBody?.toLowerCase() ?? '')

  // OAuth detection
  if (urls.some(u => u.includes('oauth') || u.includes('authorize') || u.includes('callback'))) {
    return 'oauth'
  }

  // Registration detection
  if (
    bodies.some(b => b.includes('password') && (b.includes('email') || b.includes('username'))) &&
    urls.some(u => u.includes('register') || u.includes('signup') || u.includes('sign-up'))
  ) {
    return 'registration'
  }

  // WebSocket upgrade detection
  if (requests.some(r => r.isWebSocket)) {
    return 'websocket'
  }

  // Auth token patterns
  if (urls.some(u => u.includes('/auth') || u.includes('/token') || u.includes('/login'))) {
    return 'api-auth'
  }

  return 'general'
}
```

### Custom Prompt Builder
```typescript
// src/main/ai/prompt-builder.ts
import { Scene } from './scene-detector'
import { AssembledData } from './data-assembler'

export function buildPrompt(scene: Scene, data: AssembledData): string {
  const sceneInstructions: Record<Scene, string> = {
    registration: `Analyze this registration flow. Extract:
1. Required fields and validation rules
2. Password requirements  
3. Captcha/bot protection mechanisms
4. Email verification flow
5. Reproducible curl commands for each step`,

    oauth: `Analyze this OAuth flow. Extract:
1. OAuth provider and grant type
2. Authorization URL with all parameters
3. Token exchange endpoint and parameters
4. Token refresh mechanism
5. Scopes requested`,

    'api-auth': `Analyze this authentication protocol. Extract:
1. Auth endpoint and method
2. Request payload schema
3. Response token format (JWT/session/etc)
4. Token usage in subsequent requests (header name, format)
5. Expiry and refresh strategy`,

    websocket: `Analyze this WebSocket protocol. Extract:
1. Upgrade request headers
2. Initial handshake messages
3. Message format (JSON/binary/custom)
4. Heartbeat/ping-pong mechanism
5. Event types and schemas`,

    general: `Analyze this web protocol. Extract:
1. Core API endpoints and their purposes
2. Authentication mechanism
3. Request/response schemas
4. Error handling patterns
5. Rate limiting signals`,
  }

  return `You are a protocol reverse engineer. ${sceneInstructions[scene]}

## Captured Data

### Network Requests (${data.requests.length} total)
${data.requests.map(r => `
**${r.method} ${r.url}**
Status: ${r.statusCode}
Request Headers: ${JSON.stringify(r.requestHeaders, null, 2)}
Request Body: ${r.requestBody ?? '(empty)'}
Response Headers: ${JSON.stringify(r.responseHeaders, null, 2)}
Response Body: ${r.responseBody ?? '(empty)'}
`).join('\n---\n')}

### JS Hook Events
${JSON.stringify(data.hookEvents, null, 2)}

### Storage Snapshots
${JSON.stringify(data.storageSnapshots, null, 2)}

Generate a comprehensive protocol analysis report in Markdown.`
}
```

### Adding a Custom JS Hook
```typescript
// src/main/capture/js-injector.ts
export function buildHookScript(): string {
  return `
(function() {
  // Hook fetch
  const _fetch = window.fetch.bind(window)
  window.fetch = async function(...args) {
    const [input, init] = args
    const url = input instanceof Request ? input.url : String(input)
    
    // Pre-request hook
    window.__cdpHook?.({ type: 'fetch:request', url, init: JSON.stringify(init) })
    
    const response = await _fetch(...args)
    const clone = response.clone()
    
    // Post-response hook (non-blocking)
    clone.text().then(body => {
      window.__cdpHook?.({ type: 'fetch:response', url, status: response.status, body })
    }).catch(() => {})
    
    return response
  }

  // Hook XHR
  const _open = XMLHttpRequest.prototype.open
  const _send = XMLHttpRequest.prototype.send
  
  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    this.__hookData = { method, url }
    return _open.apply(this, [method, url, ...rest])
  }
  
  XMLHttpRequest.prototype.send = function(body) {
    this.addEventListener('load', function() {
      window.__cdpHook?.({
        type: 'xhr:complete',
        method: this.__hookData?.method,
        url: this.__hookData?.url,
        requestBody: body,
        status: this.status,
        responseBody: this.responseText
      })
    })
    return _send.apply(this, [body])
  }

  // Hook crypto.subtle for key detection
  if (window.crypto?.subtle) {
    const _sign = crypto.subtle.sign.bind(crypto.subtle)
    crypto.subtle.sign = async function(algorithm, key, data) {
      window.__cdpHook?.({ type: 'crypto:sign', algorithm: JSON.stringify(algorithm) })
      return _sign(algorithm, key, data)
    }
  }

  // Hook document.cookie
  const cookieDesc = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie')
  Object.defineProperty(document, 'cookie', {
    get: function() { return cookieDesc.get.call(this) },
    set: function(val) {
      window.__cdpHook?.({ type: 'cookie:set', value: val })
      return cookieDesc.set.call(this, val)
    }
  })
})()
`
}
```

### Database Schema Access
```typescript
// src/main/db/ — SQLite via better-sqlite3
import Database from 'better-sqlite3'
import path from 'path'
import { app } from 'electron'

const DB_PATH = path.join(app.getPath('userData'), 'analyzer.db')

export function getDb(): Database.Database {
  const db = new Database(DB_PATH)
  db.pragma('journal_mode = WAL')
  return db
}

// Typical schema
export function initSchema(db: Database.Database) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      url TEXT NOT NULL,
      created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS requests (
      id TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      url TEXT NOT NULL,
      method TEXT NOT NULL,
      status_code INTEGER,
      request_headers TEXT,
      request_body TEXT,
      response_headers TEXT,
      response_body TEXT,
      is_sse INTEGER DEFAULT 0,
      is_websocket INTEGER DEFAULT 0,
      timestamp INTEGER NOT NULL,
      FOREIGN KEY (session_id) REFERENCES sessions(id)
    );

    CREATE TABLE IF NOT EXISTS hook_events (
      id TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      type TEXT NOT NULL,
      data TEXT NOT NULL,
      timestamp INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS storage_snapshots (
      id TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      cookies TEXT,
      local_storage TEXT,
      session_storage TEXT,
      timestamp INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );
  `)
}
```

### Shared Types Reference
```typescript
// src/shared/types.ts
export interface Session {
  id: string
  name: string
  url: string
  createdAt: number
}

export interface CapturedRequest {
  id: string
  sessionId: string
  url: string
  method: string
  statusCode?: number
  requestHeaders?: Record<string, string>
  requestBody?: string
  responseHeaders?: Record<string, string>
  responseBody?: string
  isSSE: boolean
  isWebSocket: boolean
  timestamp: number
}

export interface HookEvent {
  id: string
  sessionId: string
  type: 'fetch:request' | 'fetch:response' | 'xhr:complete' | 'crypto:sign' | 'cookie:set'
  data: Record<string, unknown>
  timestamp: number
}

export interface StorageSnapshot {
  id: string
  sessionId: string
  cookies: string
  localStorage: Record<string, string>
  sessionStorage: Record<string, string>
  timestamp: number
}

export interface LLMConfig {
  provider: 'openai' | 'anthropic' | 'custom'
  apiKey: string
  model: string
  baseUrl?: string
}
```

## Common Patterns

### Pattern: Capture a Full Registration Flow
1. Click **New Session** → enter name + target URL (e.g. `https://example.com/register`)
2. Click **Start Capture**
3. In the embedded browser, complete the full registration flow
4. Click **Stop Capture**
5. Click **Analyze** → AI generates a report with extracted fields, validation rules, and curl commands

### Pattern: OAuth Flow Analysis
1. Create session with the OAuth entry URL
2. Start capture
3. Authorize the OAuth flow including the redirect callback
4. Stop capture — the analyzer auto-detects OAuth and focuses prompt on token exchange

### Pattern: Adding a New LLM Provider
```typescript
// src/main/ai/ai-analyzer.ts
import Anthropic from '@anthropic-ai/sdk'
import OpenAI from 'openai'

export async function* callLLM(
  config: LLMConfig,
  prompt: string
): AsyncGenerator<string> {
  if (config.provider === 'anthropic') {
    const client = new Anthropic({ apiKey: config.apiKey })
    const stream = await client.messages.stream({
      model: config.model,
      max_tokens: 8192,
      messages: [{ role: 'user', content: prompt }]
    })
    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
        yield chunk.delta.text
      }
    }
  } else {
    // OpenAI or custom compatible
    const client = new OpenAI({
      apiKey: config.apiKey,
      baseURL: config.baseUrl  // undefined = default OpenAI
    })
    const stream = await client.chat.completions.create({
      model: config.model,
      messages: [{ role: 'user', content: prompt }],
      stream: true
    })
    for await (const chunk of stream) {
      yield chunk.choices[0]?.delta?.content ?? ''
    }
  }
}
```

### Pattern: Filter Requests Before Analysis
```typescript
// Useful for large sessions — filter to only auth-related requests
function filterRelevantRequests(requests: CapturedRequest[]): CapturedRequest[] {
  const AUTH_PATTERNS = [
    /\/auth/, /\/login/, /\/register/, /\/signup/, /\/token/,
    /\/oauth/, /\/session/, /\/verify/, /\/captcha/
  ]
  
  return requests.filter(r => {
    // Always include if has auth header
    if (r.requestHeaders?.['authorization'] || r.requestHeaders?.['x-auth-token']) {
      return true
    }
    // Include if URL matches auth patterns
    if (AUTH_PATTERNS.some(p => p.test(r.url))) return true
    // Include if response sets cookies
    if (r.responseHeaders?.['set-cookie']) return true
    // Exclude static assets
    if (/\.(js|css|png|jpg|gif|svg|woff|ico)(\?|$)/.test(r.url)) return false
    return false
  })
}
```

## Troubleshooting

### `better-sqlite3` build fails on Windows
```bash
npm install --global windows-build-tools
# or install Visual Studio Build Tools 2022 manually
pnpm rebuild
```

### `better-sqlite3` wrong Electron version
```bash
# Rebuild for current Electron version
./node_modules/.bin/electron-rebuild -f -w better-sqlite3
# or
npx @electron/rebuild -f -w better-sqlite3
```

### CDP not attaching to tab
- Ensure `WebContentsView` is fully loaded before calling `cdpManager.attach()`
- Check `webContents.getURL()` isn't `about:blank` before enabling Fetch
- For popups/OAuth windows, listen for `new-window` or `setWindowOpenHandler` and capture the new `WebContents`

### AI response truncated
- Increase `max_tokens` in the LLM call (default 8192, increase to 16384)
- Reduce request body size in `data-assembler.ts` — truncate large response bodies to first 2000 chars

### Requests missing response bodies
- CDP `Fetch.getResponseBody` must be called before `Fetch.continueRequest`
- Binary/gzip responses need base64 decoding: check `base64Encoded` field in CDP response
- Some streaming responses (SSE) can't have body captured synchronously — mark as SSE and capture chunks via `Network.eventSourceMessageReceived`

### HTTPS interception not working
- CDP Fetch interception works on all HTTPS by default in Electron's WebContentsView
- If a site uses certificate pinning, it may reject interception — look for `ERR_CERT_*` in request errors

### App window blank on startup
```bash
# Check renderer build
pnpm dev
# Look for Vite errors in terminal — usually missing env vars or import errors
```

## Development Tips

- **Hot reload**: `pnpm dev` uses electron-vite with HMR for renderer and restart for main
- **Devtools**: In dev mode, DevTools auto-opens for renderer; use `Ctrl+Shift+I` for embedded browser webview devtools
- **SQLite inspection**: Use [DB Browser for SQLite](https://sqlitebrowser.org/) on `%APPDATA%/anything-analyzer/analyzer.db` (Windows) or `~/Library/Application Support/anything-analyzer/analyzer.db` (macOS)
- **IPC debugging**: Add `console.log` in `ipc.ts` handlers — logs appear in Electron main process terminal
- **CDP raw events**: Enable `cdp.on('*', console.log)` in `cdp-manager.ts` during development to see all CDP events
