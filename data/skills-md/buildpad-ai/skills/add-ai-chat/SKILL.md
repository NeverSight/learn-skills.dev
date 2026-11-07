---
name: add-ai-chat
description: Scaffold the Buildpad AI Chat module — a ready-made chat with a Chocolate Factory agent (AiChatPanel docked on the right, AiChatWidget floating bubble, AiChatButton "Ask AI" header button, AiChat for a custom shell) with streaming Markdown answers, recent chats, image attachments and screenshots. Installed with the CLI target ai-chat-routes (browser-direct) or ai-chat-proxy-routes (server proxy). Use when the user wants a chat, chatbot, AI assistant, "Ask AI" button, help assistant, Chocolate Factory chat or agent chat in the app. Never hand-build a chat UI or an SSE parser for it.
argument-hint: "[--cwd path/to/project]"
---

# Add the AI Chat Module

A ready-made chat with a Chocolate Factory (CF) agent, installed via the Buildpad CLI (Copy & Own — the code is copied into your project). The agent itself (its model, system prompt, knowledge base and tools) is configured in the CF Portal; the module streams its answers into a chat. It talks only to the CF agent: it reads and writes nothing in the project's data service, so it works the same on every kind of Buildpad project.

What the user gets: streaming Markdown answers (code blocks with copy, tables, links), one "working" word while the agent searches or thinks, Stop, Try again, Copy answer, starter suggestions, new chat, a recent-chats list, image attachments (paper clip, paste, drag and drop; PNG, JPEG, WebP or GIF; up to 4), Take a screenshot (drag over a region of the page, then draw on it), keyboard support (Enter sends, Shift+Enter adds a line, Esc closes, ⌘I / Ctrl+I toggles), and English and Bahasa Indonesia strings.

The pieces:

- **`AiChatPanel`** — a panel docked to the right edge at full height. On a wide screen (from `75em`, the `dockFrom` prop) the page makes room for it; narrower it overlays the page; on a phone it fills the screen.
- **`AiChatWidget`** — a launcher bubble in a bottom corner that opens a chat window, for customer-facing apps.
- **`AiChatButton`** — the header "Ask AI" button that opens and closes the chat, with the shortcut in its tooltip.
- **`AiChatProvider`** / **`useAiChat`** — the open state shared by the button and the panel, and the keyboard shortcut.
- **`AiChat`** — the chat itself (header, thread, question box), for a shell of your own.
- **`AiChatContextChip`** — a chip for the `context` slot that shows what the agent is told about the page.

## CRITICAL: Never Create These Manually

Like all Buildpad UI, the AI Chat module is CLI-installed and owned as source. Do **not** hand-write a chat component, a message thread, a composer, or a parser for CF's `text/event-stream` responses, and do **not** copy the hand-rolled `ChocolateFactoryChat` example from the Chocolate Factory reference of [create-service](../create-service/SKILL.md). Do not hand-write `components/ui/ai-chat/*`, `app/api/ai-chat/*` or `lib/ai-chat/server.ts` either — scaffold them. Do not add a CF SDK or wrapper package: the module calls CF's run endpoint itself.

## Prerequisites Check

```bash
node --version && pnpm --version && npx --version
```

Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md) for install guidance), a Next.js app with Mantine (`buildpad init` sets it up), and the Buildpad i18n provider for the app-wide strings (see [add-i18n](../add-i18n/SKILL.md)).

Chocolate Factory must be connected to the project on the Buildpad Platform's Connectors page. Check `get_project_detail`'s `connectors[]` before you install anything: it carries `CHOCOLATE_FACTORY_BASE_URL` and `CHOCOLATE_FACTORY_API_KEY`. If it is not connected, ask the user to connect it first. The user also needs an agent in the CF Portal: Buildpad does not create one.

## Step 1: Choose the Backend

The chat reaches the agent in one of two ways. The choice decides where the CF key lives and whether answers can stream. **Choose before you install: each backend has its own CLI target.**

| | Browser-direct (default) | Server proxy |
|---|---|---|
| CLI target | `ai-chat-routes` | `ai-chat-proxy-routes` |
| Files | `app/api/ai-chat/config/route.ts` (`GET /api/ai-chat/config`) | `app/api/ai-chat/route.ts` (`POST /api/ai-chat`), `app/api/ai-chat/history/route.ts` (`GET /api/ai-chat/history`), `lib/ai-chat/server.ts` |
| Backend object | `chocolateFactoryBackend(config)`, with `useChocolateFactoryConfig()` | `routeBackend()` |
| The key | Visible to the browser | Stays on the server |
| Key it can use | The project key (`cf_…`) only, today | The project key or an agent key (`agk_…`) |
| Streams on Amplify Hosting | Yes | **No** — the route is a buffered Lambda (about 30 s): answers arrive all at once, and long ones time out |
| Streams on a long-lived Node server (self-hosted, EC2, a container) | Yes | Yes |
| Conversations kept | In the browser (local storage, without image data); not shown as threads in CF Monitoring | In CF, bound to the browser or user by a signed token |

A Buildpad app is hosted on Amplify by default, so **browser-direct is the default**. Use the server proxy only when the app runs on a long-lived Node server. On Amplify the proxy works in `pnpm dev` and then breaks in production.

**Browser-direct shows the key to anyone who loads the page, and today that key reaches every agent in the CF project.** CF's agent keys (`agk_…`) reach only one agent, but CF's CORS headers do not yet allow their `x-agent-key` header from a browser, so a browser call needs the project key (`cf_…`). Tell the user this plainly before you go on: it is a real security trade-off, not a formality. Reduce it in one or more of these ways:

- Protect the config route with the app's sign-in: behind auth, make `GET /api/ai-chat/config` return 401 to anonymous visitors.
- Keep the CF project's other agents harmless (no tools or data that a stranger with the key must not reach).
- Where the app runs on a long-lived Node server, use the server proxy instead.

## Installation

The AI Chat module is **opt-in** — it is not part of `bootstrap`. Install **one** route target, for the backend chosen in Step 1. Each one pulls in the `ai-chat` components.

```bash
# Browser-direct (default): the config route + components/ui/ai-chat/
npx @buildpad/cli@latest add ai-chat-routes --cwd /path/to/project

# Server proxy (a long-lived Node server only): the chat and history routes,
# lib/ai-chat/server.ts + components/ui/ai-chat/
npx @buildpad/cli@latest add ai-chat-proxy-routes --cwd /path/to/project
```

To install only the components (no routes) — for an app that writes its own:

```bash
npx @buildpad/cli@latest add ai-chat --cwd /path/to/project
```

The components add these npm packages: `ai`, `@ai-sdk/react`, `react-markdown`, `remark-gfm`, `use-stick-to-bottom` and `@zumer/snapdom`.

> The docs use the shorthand `buildpad add ai-chat-routes` when the CLI is installed globally; `npx @buildpad/cli@latest add …` is the equivalent no-install form used across these skills.

> **If the CLI command fails, `@buildpad/cli` IS published to npm** — verify with `npm view @buildpad/cli version` before assuming otherwise. The CLI fetches its registry from `raw.githubusercontent.com`, so confirm the environment can reach **both** npm and the GitHub raw CDN. If `add ai-chat-routes` or `add ai-chat-proxy-routes` reports an unknown target, the installed CLI predates this module: use `@latest`.

## Step 2: Set the Environment Variables

| Variable | Where the value comes from | Needed for |
|---|---|---|
| `CHOCOLATE_FACTORY_BASE_URL` | `connectors[]` (the Chocolate Factory connector) | both |
| `CHOCOLATE_FACTORY_API_KEY` | `connectors[]` — the project key (`cf_…`) | both |
| `CHOCOLATE_FACTORY_AGENT_ID` | **Ask the user.** They copy it from the agent's page in the CF Portal | both |
| `CHOCOLATE_FACTORY_AGENT_KEY` | Optional. An agent key (`agk_…`) from the agent's Integrations section in the CF Portal | server proxy only, for now |
| `AI_CHAT_SECRET` | Generate it: 32 or more random characters, for example `openssl rand -base64 32`. It signs the conversation tokens; the proxy routes refuse to run without it | server proxy only |

The routes read exactly these names, at request time: do not rename them.

1. **Ask the user for the Agent ID.** It is not in `connectors[]`: Buildpad never stores or provisions a CF agent. Do not guess one and do not take one from another project.
2. **The agent key is read first when it is set.** On the server proxy, recommend one: it narrows the key to this agent. On browser-direct, **leave `CHOCOLATE_FACTORY_AGENT_KEY` unset** until CF allows the `x-agent-key` header from browsers: while it is set, the config route hands the browser the agent key, and every browser call is refused.
3. **Local development:** the connector's `envVars` carries the real values of `CHOCOLATE_FACTORY_BASE_URL` and `CHOCOLATE_FACTORY_API_KEY`. Write them, the Agent ID and (server proxy only) `AI_CHAT_SECRET` and the optional agent key into `.env.local`. Do not commit, log or print them. Restart `pnpm dev`: Next.js reads `.env.local` only at start.
4. **Deployed app:** connecting CF on the Connectors page does **not** push anything to the deployed app. Push the same values with `amplify_set_env_vars`, then `amplify_redeploy` (see the [amplify-env-vars](../amplify-env-vars/SKILL.md) skill). Include the Agent ID (and, for the proxy, `AI_CHAT_SECRET`) in that same call — they are not in the connector's `envVars`. Without this step the chat works locally and finds no configuration once deployed.

**Set up the agent in the CF Portal: keep its Memory off.** Every user of the app reaches the agent with the same key, so CF sees them all as one user. With Memory on, what one user tells the agent can come back in another user's answers. Ask the user to switch Memory off on the agent, and to give it a knowledge base or an MCP server with the app's docs, so that its answers are grounded in them.

## Step 3: Mount the Chat

### Docked panel (browser-direct)

`AiChatProvider` holds the open state that `AiChatButton` and `AiChatPanel` share, and registers the shortcut (`hotkey` prop, default `mod+I`; `null` turns it off; `defaultOpened` sets the first state). Put it around the authenticated layout (in a starter, `components/layout/AuthenticatedShell.tsx`), the button in the header, and the panel at the layout's edge.

```tsx
// components/layout/assistant.tsx
'use client';

import { AiChatPanel, chocolateFactoryBackend, useChocolateFactoryConfig } from '@/components/ui/ai-chat';

export function Assistant({ userId }: { userId: string }) {
  const config = useChocolateFactoryConfig(); // GET /api/ai-chat/config
  if (!config) return null; // not configured: no chat
  return (
    <AiChatPanel
      backend={chocolateFactoryBackend(config)}
      title="Ask Acme"
      storageKey={userId}
      suggestions={['How do I invite a teammate?']}
    />
  );
}
```

```tsx
// In the authenticated layout (a client component):
<AiChatProvider>
  <header>… <AiChatButton /> …</header>
  <main style={{ marginInlineEnd: 'var(--bp-ai-chat-offset, 0)', transition: 'margin 200ms ease' }}>
    {children}
  </main>
  <Assistant userId={user.id} />
</AiChatProvider>
```

**Make room for the docked panel.** While it is open and docked, `AiChatPanel` sets `--bp-ai-chat-offset` on `<html>`. Give the app's main area `margin-inline-end: var(--bp-ai-chat-offset, 0)` (in a Mantine `AppShell`, on `AppShell.Main`), or the panel covers the right side of the page. If the header is not 60 px tall, set `--bp-ai-chat-header-height` so the panel's header lines up with it. Without `opened` and `onClose`, the panel follows `AiChatProvider`; pass them to control it yourself. `width` (default 420) and `dockFrom` (default `75em`) tune it.

### Floating widget

```tsx
<AiChatWidget backend={chocolateFactoryBackend(config)} title="Acme Support" greeting="Hi! How can we help today?" storageKey={userId} />
```

It keeps its own open state, or shares `AiChatProvider`'s with an `AiChatButton`. It adds `opened`, `onOpenChange`, `defaultOpened`, `position` (`'bottom-right'` or `'bottom-left'`), `launcherLabel` and `width` (default 400).

### Server proxy

```tsx
<AiChatPanel backend={routeBackend()} title="Ask Acme" storageKey={userId} />
```

No `useChocolateFactoryConfig()` is needed. `lib/ai-chat/server.ts` binds each conversation to its owner with a token signed by `AI_CHAT_SECRET`, so a leaked conversation id cannot be read or continued by anyone else. By default the owner is a random id in an HttpOnly cookie, so the proxy works without sign-in. **Behind the app's auth, make `chatOwner` in `lib/ai-chat/server.ts` return the signed-in user's id, and reject anonymous requests in both routes** (`app/api/ai-chat/route.ts` and `app/api/ai-chat/history/route.ts`).

### Props that matter

`AiChat`, `AiChatPanel` and `AiChatWidget` share these props:

| Prop | Purpose |
|---|---|
| `backend` (required) | `chocolateFactoryBackend(config)` or `routeBackend()` |
| `storageKey` | Scopes the recent chats kept in local storage (default `"default"`). **Pass the signed-in user's id**, so that two people on one browser do not see each other's chats |
| `vars` | CF template variables sent with every message: an object, or a function that returns one (or `undefined`) at send time. See below |
| `context` | A slot above the question box; put an `AiChatContextChip` there |
| `onNavigate` | `(href) => void` — client-side navigation for links that open in place. Pass `router.push` (the app's locale-aware router), so a link in an answer does not reload the app |
| `linkTarget` | `(href) => '_self' \| '_blank'` — default: app pages in place, other sites in a new tab |
| `imageHosts` | Hosts an answer may show images from (default none). An image from any other host shows its alt text instead |
| `title` / `badge` / `greeting` / `description` | Header title (default "Assistant"), a badge such as "Beta", and the empty-state heading (default "How can I help?") and text |
| `suggestions` | Starter questions |
| `placeholder` / `disclaimer` | The question box's placeholder and the line under it |
| `features` | `{ attachments?, screenshot?, recentChats? }` — all on by default; set one to `false` to turn it off |
| `translations` | Per-instance strings. App-wide strings come from the `chat` namespace through `BuildpadI18nProvider` |
| `onError` | Called with each error (default `console.error`) |

### Tell the agent where the user is

`vars` are sent with every message as CF template variables, so the agent's system prompt can use them (`{{page}}`, `{{user_name}}`, …): add the matching variables to the agent's prompt in the CF Portal. Pair them with an `AiChatContextChip`, so the user sees what is shared and can stop sharing:

```tsx
const pathname = usePathname();
const [share, setShare] = useState(true);

<AiChatPanel
  backend={backend}
  storageKey={user.id}
  onNavigate={(href) => router.push(href)}
  vars={() => (share ? { page: 'Settings › Members', page_path: pathname } : undefined)}
  context={
    share ? (
      <AiChatContextChip label="Settings › Members" title={pathname} onRemove={() => setShare(false)} removeLabel="Don't share this page" />
    ) : null
  }
/>
```

Send only what the agent needs, as strings, numbers or booleans (the server proxy drops anything else): every variable goes to CF with every message. Never put a token, a key or a password in `vars`.

## Post-Install Validation

```bash
npx @buildpad/cli@latest status --cwd /path/to/project
npx @buildpad/cli@latest validate --cwd /path/to/project
cd /path/to/project && pnpm build
```

Then run `pnpm dev`, open a page that mounts the chat, press ⌘I (Ctrl+I) or the "Ask AI" button, and ask a question. The answer streams in word by word. In the browser's network panel:

- **Browser-direct:** `GET /api/ai-chat/config` answers, then a request goes to `{CHOCOLATE_FACTORY_BASE_URL}/api/agents/{agentId}/run`. A 503 from the config route means a variable is missing. A CORS error on the run request usually means `CHOCOLATE_FACTORY_AGENT_KEY` is set: unset it (Step 2). A 401 or 403 means a wrong key, a 404 a wrong Agent ID, and a 400 can mean the agent is inactive.
- **Server proxy:** requests go to `/api/ai-chat` only, and no response holds the key. A 503 means a variable is missing or `AI_CHAT_SECRET` is shorter than 32 characters.

After deploying, ask one long question on the deployed app: the answer must stream, not arrive all at once. If it arrives all at once on Amplify, the app uses the server proxy — install `ai-chat-routes` and switch to browser-direct.

## Related

- [create-service](../create-service/SKILL.md) — its Chocolate Factory reference covers CF calls other than a chat: one-off server-side calls and structured output for charts and documents.
- [amplify-env-vars](../amplify-env-vars/SKILL.md) — push the environment variables to the deployed app.
- [add-i18n](../add-i18n/SKILL.md) — the i18n provider that supplies the chat's app-wide strings.
- [add-buildpad](../add-buildpad/SKILL.md) — the underlying CLI.
- [buildpad-reference](../buildpad-reference/SKILL.md) — full component catalog.
