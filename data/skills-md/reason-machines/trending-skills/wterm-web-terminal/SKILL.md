---
name: wterm-web-terminal
description: Web terminal emulator with Zig/WASM core, DOM rendering, and React/vanilla JS bindings
triggers:
  - add a terminal to my web app
  - embed a terminal emulator in the browser
  - use wterm in my React app
  - connect a WebSocket PTY terminal
  - render a terminal in the DOM
  - build a web-based shell interface
  - integrate wterm terminal component
  - display terminal output in a Next.js app
---

# wterm Web Terminal Emulator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

wterm ("dub-term") is a web terminal emulator with a Zig/WASM core (~12 KB binary) for near-native VT100/VT220/xterm parsing. It renders to the DOM — giving you native text selection, copy/paste, browser find, and accessibility for free. Supports WebSocket PTY backends, alternate screen buffers, 24-bit color, scrollback, and themes.

## Packages

| Package | Purpose |
|---|---|
| `@wterm/core` | Headless WASM bridge + WebSocket transport |
| `@wterm/dom` | DOM renderer + input handler (vanilla JS) |
| `@wterm/react` | React component + `useTerminal` hook |
| `@wterm/just-bash` | In-browser Bash shell |
| `@wterm/markdown` | Render Markdown in the terminal |

## Installation

```bash
# React
npm install @wterm/react @wterm/core

# Vanilla JS
npm install @wterm/dom @wterm/core

# In-browser bash (no backend needed)
npm install @wterm/just-bash @wterm/core
```

Copy the WASM binary to your public directory:

```bash
cp node_modules/@wterm/core/wterm.wasm public/
```

## React Usage

### Basic Terminal Component

```tsx
import { Terminal } from '@wterm/react';

export default function App() {
  return (
    <div style={{ width: '800px', height: '500px' }}>
      <Terminal
        wsUrl={`ws://${window.location.host}/pty`}
        theme="default"
      />
    </div>
  );
}
```

### useTerminal Hook

```tsx
import { useTerminal } from '@wterm/react';
import { useEffect, useRef } from 'react';

export default function CustomTerminal() {
  const containerRef = useRef<HTMLDivElement>(null);

  const { terminal, connect, disconnect, write, resize } = useTerminal({
    wsUrl: process.env.NEXT_PUBLIC_PTY_WS_URL,
    wasmUrl: '/wterm.wasm',
    theme: 'monokai',
    scrollback: 1000,
    onData: (data) => console.log('Terminal output:', data),
    onConnect: () => console.log('Connected to PTY'),
    onDisconnect: () => console.log('Disconnected'),
  });

  useEffect(() => {
    if (containerRef.current && terminal) {
      terminal.mount(containerRef.current);
      connect();
    }
    return () => disconnect();
  }, [terminal]);

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '400px', background: '#1e1e1e' }}
    />
  );
}
```

### Programmatic Input/Output

```tsx
import { useTerminal } from '@wterm/react';

export default function ProgrammaticTerminal() {
  const { terminal, write } = useTerminal({
    wasmUrl: '/wterm.wasm',
  });

  const runCommand = () => {
    // Write VT100 escape sequences or plain text
    write('\x1b[32mHello, world!\x1b[0m\r\n');
    write('\x1b[1mBold text\x1b[0m\r\n');
  };

  return (
    <>
      <div ref={(el) => el && terminal?.mount(el)} style={{ height: 300 }} />
      <button onClick={runCommand}>Write to terminal</button>
    </>
  );
}
```

## Vanilla JS Usage

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="node_modules/@wterm/dom/dist/wterm.css" />
</head>
<body>
  <div id="terminal" style="width:800px;height:500px"></div>
  <script type="module">
    import { createTerminal } from '@wterm/dom';

    const term = await createTerminal({
      container: document.getElementById('terminal'),
      wasmUrl: '/wterm.wasm',
      wsUrl: 'ws://localhost:3001/pty',
      theme: 'solarized-dark',
      scrollback: 2000,
    });

    term.connect();

    // Write directly
    term.write('\x1b[33mWelcome!\x1b[0m\r\n');

    // Resize programmatically
    term.resize(120, 40); // cols, rows
  </script>
</body>
</html>
```

## In-Browser Bash (No Backend)

```tsx
import { Terminal } from '@wterm/react';
import { JustBashTransport } from '@wterm/just-bash';

export default function BrowserShell() {
  return (
    <Terminal
      transport={new JustBashTransport()}
      wasmUrl="/wterm.wasm"
      theme="default"
      style={{ width: '100%', height: '500px' }}
    />
  );
}
```

## Themes

Built-in themes: `default`, `solarized-dark`, `monokai`, `light`

```tsx
// Via prop
<Terminal theme="monokai" wasmUrl="/wterm.wasm" wsUrl="..." />
```

### Custom Theme via CSS Custom Properties

```css
#terminal {
  --wterm-bg: #0d1117;
  --wterm-fg: #c9d1d9;
  --wterm-cursor: #58a6ff;
  --wterm-selection-bg: rgba(88, 166, 255, 0.3);

  /* ANSI colors */
  --wterm-color-0: #161b22;   /* black */
  --wterm-color-1: #ff7b72;   /* red */
  --wterm-color-2: #3fb950;   /* green */
  --wterm-color-3: #d29922;   /* yellow */
  --wterm-color-4: #58a6ff;   /* blue */
  --wterm-color-5: #bc8cff;   /* magenta */
  --wterm-color-6: #39c5cf;   /* cyan */
  --wterm-color-7: #b1bac4;   /* white */
  /* bright variants: --wterm-color-8 through --wterm-color-15 */
}
```

## WebSocket PTY Backend (Node.js)

```ts
// server.ts — example PTY backend using node-pty
import { WebSocketServer } from 'ws';
import * as pty from 'node-pty';

const wss = new WebSocketServer({ port: 3001, path: '/pty' });

wss.on('connection', (ws) => {
  const shell = pty.spawn(process.env.SHELL || 'bash', [], {
    name: 'xterm-256color',
    cols: 80,
    rows: 24,
    cwd: process.env.HOME,
    env: process.env as Record<string, string>,
  });

  // PTY → client (binary framing)
  shell.onData((data) => {
    if (ws.readyState === ws.OPEN) {
      ws.send(Buffer.from(data, 'binary'));
    }
  });

  // Client → PTY
  ws.on('message', (msg: Buffer) => {
    const text = msg.toString('binary');
    // wterm sends resize as JSON: {"type":"resize","cols":120,"rows":40}
    try {
      const parsed = JSON.parse(text);
      if (parsed.type === 'resize') {
        shell.resize(parsed.cols, parsed.rows);
        return;
      }
    } catch {}
    shell.write(text);
  });

  ws.on('close', () => shell.kill());
  shell.onExit(() => ws.close());
});
```

## Next.js Integration

```bash
# Install
npm install @wterm/react @wterm/core

# Copy WASM to public
cp node_modules/@wterm/core/wterm.wasm public/
```

```tsx
// components/Terminal.tsx
'use client';

import dynamic from 'next/dynamic';

// Must be client-only — no SSR
const WTerminal = dynamic(
  () => import('@wterm/react').then((m) => m.Terminal),
  { ssr: false }
);

export default function TerminalPage() {
  return (
    <WTerminal
      wsUrl={process.env.NEXT_PUBLIC_PTY_WS_URL}
      wasmUrl="/wterm.wasm"
      theme="monokai"
      style={{ width: '100%', height: '600px' }}
    />
  );
}
```

## Markdown in Terminal

```ts
import { renderMarkdown } from '@wterm/markdown';
import { createTerminal } from '@wterm/dom';

const term = await createTerminal({ container, wasmUrl: '/wterm.wasm' });

const md = `# Hello\n\n**Bold** and *italic* text.\n\n\`\`\`js\nconsole.log('hi');\n\`\`\``;
term.write(renderMarkdown(md));
```

## Configuration Reference

### `createTerminal` / `useTerminal` Options

| Option | Type | Default | Description |
|---|---|---|---|
| `wasmUrl` | `string` | `'/wterm.wasm'` | Path to WASM binary |
| `wsUrl` | `string` | — | WebSocket PTY endpoint |
| `transport` | `Transport` | — | Custom transport (overrides wsUrl) |
| `theme` | `string` | `'default'` | Built-in theme name |
| `scrollback` | `number` | `1000` | Scrollback buffer rows |
| `cols` | `number` | auto | Initial column count |
| `rows` | `number` | auto | Initial row count |
| `onData` | `(data: string) => void` | — | Raw output callback |
| `onConnect` | `() => void` | — | Connection established |
| `onDisconnect` | `() => void` | — | Connection closed |
| `onResize` | `(cols, rows) => void` | — | Resize event callback |

## Development Setup

```bash
# Prerequisites: Zig 0.15.2+, Node.js 20+, pnpm 10+
npm install -g portless

git clone https://github.com/vercel-labs/wterm
cd wterm
pnpm install

# Build WASM core
zig build                          # debug
zig build -Doptimize=ReleaseSmall  # ~12 KB release

# Build all packages
pnpm build

# Run Zig tests
zig build test

# Serve vanilla demo
cd web && python3 -m http.server 8000

# Run Next.js example
cp web/wterm.wasm examples/nextjs/public/
pnpm --filter nextjs dev
# Available at: nextjs-example.wterm.localhost
```

## Troubleshooting

**WASM file not found (404)**
```bash
# Ensure wterm.wasm is in your public directory
cp node_modules/@wterm/core/wterm.wasm public/
# In Next.js, verify it's at public/wterm.wasm
```

**Terminal not rendering / blank screen**
- Container must have explicit `width` and `height` (not `auto`)
- Wrap in `dynamic(..., { ssr: false })` in Next.js — WASM requires browser APIs
- Check browser console for WASM instantiation errors

**WebSocket connection refused**
- Verify PTY backend is running and `wsUrl` matches
- Check CORS headers if backend is on a different origin
- Use `wss://` for HTTPS-served apps

**Text selection / copy not working**
- wterm uses DOM rendering, so native browser selection should work
- Ensure the container does not have `user-select: none` in CSS

**Resize not working**
- wterm uses `ResizeObserver` automatically; ensure the container resizes with the page
- For manual resize: `terminal.resize(cols, rows)`

**Alternate screen apps (vim, htop) display incorrectly**
- Ensure your PTY backend sets `TERM=xterm-256color`
- Verify the WebSocket sends binary (not UTF-8 string) frames
