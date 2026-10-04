---
name: browser-agent
description: >
  Run a Deepgram voice agent in the browser with the four Browser Agent SDK packages:
  @deepgram/agents (core WebSocket session, mic, player), @deepgram/react (AgentProvider
  and hooks), @deepgram/ui (pre-built React components), and @deepgram/agents-widget
  (drop-in, no framework). Use when a task says "browser voice agent", "voice widget",
  "embed a voice agent", "react voice agent", "@deepgram/react", "@deepgram/ui",
  "agents-widget", "AgentProvider", "useAgentState", "useDeepgramAgent", "AgentSession",
  "tokenFactory", "Orb", "voice agent on my website", or asks how to keep a Deepgram API
  key out of client-side code. Picks the layer, gets one path running, and routes to the
  voice-agent skill for the WebSocket contract underneath.
---

# Deepgram Browser Agent SDK

Deepgram runs listen, think, and speak behind one WebSocket and handles the turn-taking between them. These four packages get a browser onto that socket; each wraps the one below. Pick a layer by how much UI you want to build yourself, not by package name. [1]

## Pick the layer first

| Package | When | Install |
|---|---|---|
| `@deepgram/agents-widget` | You want a voice agent on a page today, with no framework and no build step, and you can live with its UI. It ships six layouts (`sidebar`, `floating`, `inline`, `button`, `embedded`, `orb`), themed with CSS custom properties. | `@deepgram/agents-widget` |
| `@deepgram/ui` | React app, and the conversation view, orb, waveform, and mic/speaker buttons listed below are close enough to your design. Retheme them with CSS custom properties. | `@deepgram/ui` only. See Common mistakes 3 |
| `@deepgram/react` | React app, you build every pixel. Provider plus focused hooks manage the connection, mic, playback, transcript, and client tools. | `@deepgram/react @deepgram/agents` |
| `@deepgram/agents` | You are on Vue, Svelte, Angular, vanilla JS, or another non-React runtime. `AgentSession`, `AgentMicrophone`, and `AgentPlayer` give you the pieces; you wire the events. | `@deepgram/agents` |

Each layer re-exports the layer below, so `@deepgram/ui` alone gives you `AgentProvider`, the `@deepgram/agents` types, and all ten hooks: `useAgentClientTool`, `useAgentContext`, `useAgentControls`, `useAgentConversation`, `useAgentMicrophone`, `useAgentMode`, `useAgentPlayer`, `useAgentSession`, `useAgentState`, and `useDeepgramAgent`. [7]

## Versions and stability

All four are pre-1.0, and `latest` is the only dist-tag on each. `@deepgram/ui`'s README puts it plainly: "This library is pre-1.0. Interfaces may change between minor versions, and releases are cut as the library evolves rather than on a fixed schedule." So resolve the versions against the registry before you install, and resolve them again before you trust a version-specific statement anywhere below:

```bash
for p in @deepgram/agents @deepgram/agents-widget @deepgram/react @deepgram/ui; do npm view "$p" version; done
npm view @deepgram/ui dependencies   # and @deepgram/agents-widget, to check the ranges below
```

Where the registry disagrees with this skill, the registry wins. The table below is the pinned set the export names and dependency ranges in this skill describe. [3][4][5]

| Package | Version | Repo |
|---|---|---|
| `@deepgram/agents` | 0.1.2 | `deepgram/agent` (`packages/sdk`) |
| `@deepgram/agents-widget` | 0.1.8 | `deepgram/agent` (`packages/widget`) |
| `@deepgram/react` | 0.2.0 | `deepgram/react` |
| `@deepgram/ui` | 0.1.6 | `deepgram/ui` |

Declared runtime dependencies, as published. `@deepgram/agents` depends on `@deepgram/sdk` 5.9.0. `@deepgram/react@0.2.0` depends on `@deepgram/agents ^0.1.2` and takes `react` and `react-dom` `>=18.0.0` as peers. `@deepgram/ui@0.1.6` depends on `@deepgram/react ^0.1.0`, `@deepgram/agents ^0.1.1`, and Radix and Tailwind helpers. `@deepgram/agents-widget@0.1.8` depends on `@deepgram/react ^0.1.0`, `@deepgram/ui ^0.1.4`, `@deepgram/agents ^0.1.2`, and `preact`, all bundled into its own build. Those `^0.1.0` ranges exclude `@deepgram/react@0.2.0`, which is what makes mistake 3 below possible. [6]

## Browser auth: never the API key

A browser `WebSocket` cannot set request headers, so the SDK sends a short-lived bearer token as the `Sec-WebSocket-Protocol` handshake value. You supply that token through `tokenFactory`, which the SDK calls before every connect and every reconnect, so a few seconds of TTL is enough. The token only has to be valid at the handshake: once the socket is open, the token expiring does not close it, and a 30-second token is fine for an hour-long call. `AgentSession` wraps `tokenFactory` in an expiry-aware cache: it reads the JWT `exp` claim and refreshes 5 seconds before it, falls back to 25 seconds for a token that is not a JWT, and is invalidated before every connection and reconnection attempt, so each handshake gets a fresh token. The default 30-second token from `/v1/auth/grant` works as is; no `ttl_seconds` change is needed. [1][2][3]

Mint them on your own server. `POST https://api.deepgram.com/v1/auth/grant` needs an API key with Member or higher authorization and returns `{"access_token":"...","expires_in":30}`. Its tokens work on the voice APIs but not on the Manage APIs:

```js
// Server. The API key never leaves this process.
app.get("/api/deepgram-token", async (_req, res) => {
  const r = await fetch("https://api.deepgram.com/v1/auth/grant", {
    method: "POST",
    headers: { Authorization: `Token ${process.env.DEEPGRAM_API_KEY}`,
               "Content-Type": "application/json" },
    body: JSON.stringify({ ttl_seconds: 30 }),
  });
  const { access_token } = await r.json();
  res.set("Cache-Control", "no-store").send(access_token);
});
```

Pass it as `auth: { tokenFactory: () => fetch("/api/deepgram-token").then(r => r.text()) }` in React and the SDK, or as a top-level `tokenFactory` in the widget. Put your own session check in front of that route: anyone who can call it can open an agent session billed to you. The `apiKey` auth mode exists for server-side use and local experiments only; in a browser bundle it is a published credential. [1][2]

## `@deepgram/agents-widget`: one call

```js
import { init } from "@deepgram/agents-widget";

const teardown = init({
  tokenFactory: () => fetch("/api/deepgram-token").then((r) => r.text()),
  agent: "YOUR_AGENT_ID", // a Reusable Agent Configuration UUID, or a full settings object
  layout: "floating",
  placement: "bottom-right",
});
// teardown() unmounts and removes injected styles; call it on SPA route change
```

`init` is the package's only function export; everything else it ships is type declarations. For a no-build page, load the UMD bundle and call `DeepgramAgent.init(...)`; the global is `DeepgramAgent`. `https://cdn.deepgram.com/widgets/v0.1.8/widget.umd.js` serves the same bundle as npm 0.1.8, 414,517 bytes minified and roughly 91 KB gzipped. The same CDN answers a `latest` path, which moves with each release, so pin the `v`-prefixed version in production. [2][8]

## `@deepgram/react`: provider and hooks

```tsx
import { AgentProvider, useAgentState, useAgentConversation } from "@deepgram/react";

const config = {
  auth: { tokenFactory: () => fetch("/api/deepgram-token").then((r) => r.text()) },
  agent: { think: { provider: { type: "open_ai" as const, model: "gpt-4o-mini" } } },
};

export default function App() {
  return <AgentProvider config={config}><Agent /></AgentProvider>;
}

function Agent() {
  const { state, start, stop } = useAgentState();       // idle | connecting | connected | reconnecting | disconnected
  const { conversation } = useAgentConversation();
  const onStart = async () => { try { await start(); } catch (e) { console.error(e); } };
  return (
    <>
      <button onClick={state === "idle" ? onStart : stop}>{state === "idle" ? "Start" : "Stop"}</button>
      {conversation.map((e) => <p key={e.id}><b>{e.role}:</b> {e.content}</p>)}
    </>
  );
}
```

The other hooks: `useAgentMode` (`idle`/`listening`/`thinking`/`speaking`), `useAgentMicrophone`, `useAgentPlayer`, `useAgentControls` (grouped lifecycle, messaging, runtime settings, mute), `useAgentClientTool` (register a function-call handler scoped to the component), `useAgentContext`, `useAgentSession` (the raw `AgentSession`), and `useDeepgramAgent` (no provider needed). `config`, `playerSampleRate`, and the initial `autoStart` are read once and pinned for the provider's lifetime. Change a connected agent with the runtime controls, not by mutating `config`. `useDeepgramAgent` does not support `useAgentClientTool`; give it `onFunctionCall` in its options, or use the provider pattern for per-component tool registration. [4]

## `@deepgram/ui`: components

```tsx
import { AgentProvider, AgentConversation, AgentTextInput, AgentStartButton, Orb } from "@deepgram/ui";
import "@deepgram/ui/styles.css";

<AgentProvider config={config}>
  <div data-dg-agent>
    <Orb size={120} />
    <AgentConversation />
    <AgentTextInput />
    <AgentStartButton />
  </div>
</AgentProvider>
```

Components: `AgentStatus`, `AgentConversation`, `AgentMessage`, `AgentTextInput`, `AgentMicrophoneButton`, `AgentSpeakerButton`, `AgentStartButton`, plus `VoiceButton`, `Orb`, `LiveWaveform`, `BarVisualizer`, `MicSelector`, and `Response`. Styling is Tailwind v4 compiled into `@deepgram/ui/styles.css` and scoped to `[data-dg-agent]`; tokens are shadcn `--color-*` names you override on any `[data-dg-agent]` ancestor. `data-dg-scheme="dark"` on the same element forces dark; without it, components follow `prefers-color-scheme`. Install from npm rather than through a shadcn registry: `deepgram/ui` builds one, but `@deepgram/ui-registry` is a private package and `ui.deepgram.com` serves no registry JSON, so `npx shadcn add` against it returns 404. Two release notes matter when pinning: `ui-v0.1.5` compiles the standalone `styles.css` export so bundlers receive regular CSS instead of Tailwind source directives, and `ui-v0.1.6` preserves the bundled TypeScript declarations after a `vite-plugin-dts` upgrade, so pin 0.1.6 or newer. [11]

## `@deepgram/agents`: any framework

```js
import { AgentSession, AgentMicrophone, AgentPlayer } from "@deepgram/agents";

const session = new AgentSession({
  auth: { tokenFactory: () => fetch("/api/deepgram-token").then((r) => r.text()) },
  agent: "YOUR_AGENT_ID",
});
const player = new AgentPlayer();                                  // default output 24000 Hz
const mic = new AgentMicrophone((data) => session.sendAudio(data)); // default capture 16000 Hz

session.on("audio", (chunk) => player.queue(chunk));
session.on("user-started-speaking", () => player.interrupt());      // barge-in
session.on("conversation-text", (m) => console.log(`${m.role}: ${m.content}`));

await session.connect();
await mic.start();
```

`AgentSession` handles the `Welcome`/`Settings`/`SettingsApplied` handshake, buffers mic frames until `SettingsApplied`, sends `KeepAlive` every `keepAliveInterval` ms (default 10,000), and reconnects with jittered exponential backoff: `reconnect.maxAttempts` default 8, `baseDelay` 500 ms, `maxDelay` 30,000 ms, `jitter` true for plus or minus 20%. Its other options are `audio.input` and `audio.output` (`encoding`, `sampleRate`) and `url`, which overrides the socket URL. Runtime methods mirror the protocol: `updateListen`, `updateSpeak`, `updateThink`, `updatePrompt`, `injectUserMessage`, `injectAgentMessage(message, behavior?)` with `behavior` one of `default`, `queue`, or `interrupt`, and `sendFunctionCallResponse`. Events are the protocol messages in kebab-case, among them `listen-updated`, `latency-report`, and `history`, plus `audio`, `connecting`, `connected`, `reconnecting`, `disconnected`, `sdk-error`. `AgentPlayer` decodes raw PCM Int16 (`linear16`) only and does not decode compressed output, so keep `audio.output.encoding` at `linear16` or supply your own decoder. `AgentMicrophone` and `AgentPlayer` expose `getInputVolume` and `getOutputVolume`, plus `getInputByteFrequencyData` and `getOutputByteFrequencyData`, for visualizers. [3]

## Upgrade `@deepgram/react` 0.1 to 0.2

0.2.0 shipped 2026-09-10 and is the only breaking release so far. Its five changes: [9]

1. `AgentMode` now includes `"thinking"`. Fix exhaustive `switch`es and mode-to-label maps.
2. `AgentContextValue` and the hook result types now require new members. Consuming components need no change; typed mocks, wrappers, and hand-written implementations of those interfaces do.
3. `registerClientTool()` now returns an unsubscribe function. Ignoring it still works; store and call it when registering outside a component lifecycle. `useAgentClientTool()` still unregisters on unmount.
4. `useDeepgramAgent().start()` now clears `conversation` before connecting. Keep any transcript that must outlive a restart outside the hook. Manual `start()` now rejects on failure, so handle the promise; automatic and reconnect failures go to `onSdkError`.
5. `useAgentControls()`, `useAgentConversation()`, and `useDeepgramAgent()` now expose runtime controls, among them `updatePrompt` and `sendAgentMessage`, that update a connected agent without recreating the provider. `onListenUpdated`, `onPromptUpdated`, `onSpeakUpdated`, and `onThinkUpdated` fire when the server acknowledges the change.

## Common mistakes

1. Shipping the API key to the browser. `{ auth: { apiKey } }` in client-side code publishes a credential anyone can bill against. Use `tokenFactory` against a route you gate. [1]
2. Setting the token lifetime with `ttl` in the `/v1/auth/grant` body. The field is `ttl_seconds`. A body of `{"ttl":300}` is accepted and ignored, and the response comes back `expires_in: 30`; `{"ttl_seconds":300}` returns `expires_in: 300`. The endpoint ignores any field it does not recognize and still answers HTTP 200, so read `expires_in` in the response rather than trusting the field name you sent. [2]
3. Installing `@deepgram/react@0.2.0` next to `@deepgram/ui@0.1.6` and importing the provider from one and the hooks from the other. `@deepgram/ui` declares `@deepgram/react ^0.1.0`, so npm nests a second copy at 0.1.0 and the two packages build separate React contexts: `AgentProvider` from `@deepgram/ui` is not the same function as `AgentProvider` from `@deepgram/react`, and a hook that reads the other context throws `useAgentContext must be used inside <AgentProvider>`. The install line in the `deepgram/ui` repository README, `npm install @deepgram/ui @deepgram/react @deepgram/agents`, produces exactly this tree (the npm README's `npm install @deepgram/ui react react-dom` does not). Either import everything from `@deepgram/ui` alone, or pin one copy with `"overrides": { "@deepgram/react": "0.2.0" }` in npm, `overrides` in pnpm, or `resolutions` in yarn, which dedupes the tree and makes both imports resolve to one module. [6]
4. Forgetting `import "@deepgram/ui/styles.css"` or the `data-dg-agent` attribute on a wrapper. Every `@deepgram/ui` token is scoped to `[data-dg-agent]`, so without it the components render unstyled. [5]
5. Never calling `player.interrupt()` on `user-started-speaking` in a raw-SDK build. Deepgram stops generating, but your queued audio keeps talking over the caller. Only the raw SDK leaves this to you: `@deepgram/react`'s provider already interrupts the player on that event, and the UI and widget layers inherit it. [3][4]
6. Mismatching sample rates. `AgentPlayer`'s `sampleRate` (default 24000) must equal the session's `audio.output.sampleRate` (the SDK key; on the wire it is `audio.output.sample_rate`), and `AgentMicrophone`'s (default 16000) must equal `audio.input.sampleRate`. [3]
7. Leaving `latest` in a production CDN `<script>` tag. Pin the `v`-prefixed version; these packages are pre-1.0 and minor releases may change interfaces. [8]
8. Expecting client-side voice activity detection. `@deepgram/agents` 0.1.2 ships no VAD export and `MicrophoneOptions` carries no VAD setting; its options are `sampleRate`, `echoCancellation`, `noiseSuppression`, and `autoGainControl`. Turn detection and barge-in are server-side with any listen model: the default is a `v1` Nova model, and a Flux STT model with `version: "v2"` adds model-integrated end-of-turn detection. Either way the server emits `user-started-speaking` and the client's only job is `player.interrupt()`. The `voice-agent` skill covers it. [3]

## Use a different skill when

- You need the WebSocket contract these packages wrap, meaning `Settings` fields, message lifecycle, barge-in, function calling, and telephony: `voice-agent` skill.
- You need the full schema for any field or endpoint, including `/v1/auth/grant`: `api` skill (`references/agent.md`, `references/auth.md`).
- You want a runnable app to clone, not a package to add: `starters` skill (feature `voice-agent`), or `examples` skill for third-party platforms. The `deepgram/agent` repository also ships 17 runnable SDK examples, with a hosted build. [10]
- You want a one-feature snippet: `recipes` skill.
- You are writing the token-minting server in Python, Go, Java, .NET, or Rust: that SDK's own skills, shipped from its repository.
- You want to find a docs page: `docs` skill. You want Deepgram docs queryable in your editor: `setup-mcp` skill.

## Sources

1. https://developers.deepgram.com/docs/browser-agent-overview (layer choice, token factory, `Sec-WebSocket-Protocol`)
2. https://developers.deepgram.com/reference/auth/tokens/grant and https://developers.deepgram.com/guides/fundamentals/token-based-authentication (`ttl_seconds`, 30-second default, Member-scope requirement)
3. https://github.com/deepgram/agent (`packages/sdk`), `npm view @deepgram/agents readme`, `dist/index.js` in the published `@deepgram/agents@0.1.2` tarball (token cache), and https://developers.deepgram.com/docs/browser-agent-javascript (`@deepgram/agents` exports, session options, events, mic and player options)
4. https://github.com/deepgram/react (`packages/react/src/context.ts` throws the `useAgentContext` error) and https://developers.deepgram.com/docs/browser-agent-react (provider, hooks, barge-in handling, `useDeepgramAgent` limits)
5. https://github.com/deepgram/ui and https://developers.deepgram.com/docs/browser-agent-react-ui (components, `[data-dg-agent]` tokens, pre-1.0 statement)
6. `npm view <pkg> version dist-tags dependencies peerDependencies` for all four packages
7. `@deepgram/ui` export list: `import * as ui from "@deepgram/ui"; Object.keys(ui)`
8. https://developers.deepgram.com/docs/browser-agent-widget (CDN URL, six layouts, teardown, UMD global)
9. https://github.com/deepgram/react/blob/main/MIGRATION.md
10. https://github.com/deepgram/agent/tree/main/examples (17 runnable examples: widget 01-07, React 10-15, UMD 20-23) and the hosted build at https://deepgram-agent-examples.fly.dev
11. https://github.com/deepgram/ui/releases (`ui-v0.1.5` compiled `styles.css`; `ui-v0.1.6` bundled TypeScript declarations) and https://github.com/deepgram/ui/blob/main/README.md (three-package install line)
