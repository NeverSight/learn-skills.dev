---
name: agentpulse-setup
description: |
  Set up AgentPulse in a React or Electron project. Use when the user wants to add AgentPulse,
  make their app MCP-controllable, or integrate with Claude Code/Claude Desktop.
  This is a ONE-TIME setup skill. For help writing useExpose hooks, use the "agentpulse" skill instead.
license: MIT
compatibility: React >=18. Optional Electron >=20 support.
metadata:
  author: agentpulse
  version: "1.0"
allowed-tools: Bash(npm*) Bash(npx*) Read Write Edit Glob
---

# AgentPulse Setup

Set up AgentPulse to make your React app controllable by AI agents via MCP.

## Prerequisites

- Node.js project with React
- Know if it's a **web app** (Next.js, Vite, CRA) or **Electron app**

## Step 1: Install

```bash
npm install agentpulse
```

## Step 2: Add Provider

Find the app's root component and wrap it with `AgentPulseProvider`.

**Vite / CRA** (`App.tsx` or `main.tsx`):
```tsx
import { AgentPulseProvider } from 'agentpulse';

function App() {
  return (
    <AgentPulseProvider endpoint="ws://localhost:3100/ws">
      <YourApp />
    </AgentPulseProvider>
  );
}
```

**Next.js App Router** (`app/layout.tsx`):
```tsx
'use client';
import { AgentPulseProvider } from 'agentpulse';

export default function RootLayout({ children }) {
  return (
    <html><body>
      <AgentPulseProvider endpoint="ws://localhost:3100/ws">
        {children}
      </AgentPulseProvider>
    </body></html>
  );
}
```

**Next.js Pages Router** (`pages/_app.tsx`):
```tsx
import { AgentPulseProvider } from 'agentpulse';

export default function App({ Component, pageProps }) {
  return (
    <AgentPulseProvider endpoint="ws://localhost:3100/ws">
      <Component {...pageProps} />
    </AgentPulseProvider>
  );
}
```

**Electron apps**: See `references/ELECTRON_SETUP.md`.

## Step 3: Add a Sample useExpose

Add one `useExpose` call to verify setup works. Find an interactive component:

```tsx
import { useExpose } from 'agentpulse';

function SomeInput() {
  const [value, setValue] = useState('');

  useExpose('test-input', { value, setValue }, {
    description: 'Test input for verifying AgentPulse setup.',
  });

  return <input value={value} onChange={e => setValue(e.target.value)} />;
}
```

## Step 4: Add npm Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "agentpulse": "agentpulse"
  }
}
```

Optional: run app and server together (requires `concurrently`):
```json
{
  "scripts": {
    "dev:agent": "concurrently \"npm run dev\" \"npm run agentpulse\""
  }
}
```

## Step 5: Configure MCP Client

**Claude Desktop**

macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agentpulse": {
      "url": "http://localhost:3100/mcp"
    }
  }
}
```

Restart Claude Desktop after editing.

**Claude Code**

Add to MCP settings (same JSON format as above).

## Step 6: Verify Setup

1. Start your app: `npm run dev`
2. Start AgentPulse: `npx agentpulse`
3. In MCP client, run: `discover()`

You should see your `test-input` component listed.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "WebSocket connection failed" | Is `npx agentpulse` running? |
| Components not in `discover()` | Is `AgentPulseProvider` at root? Refresh browser. |
| MCP tools not available | Check config file path, restart MCP client |

See `references/TROUBLESHOOTING.md` for more.

## Next Steps

Setup is complete. To expose more components, use the **agentpulse** skill:

```
"Help me expose my login form to AgentPulse"
```
