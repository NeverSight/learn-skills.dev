---
name: new-agent
description: Add or change a capability of a Boring app - an agent, a job, a chat, a tool, a view or a page - and decide whether to expose it in boring.json. Use when a task asks for a new agent or output field, a change to an agent's prompt, rules, model or output, work that runs several agents, a chat, a tool an agent or the hub calls, or a view the hub frames. Lists the files to create, the contracts to keep, the tests to run and the feature-map entry to update.
---

# Add a capability to a Boring app

An app is a capability provider (hachej/boring-app). Every capability folder is
optional; `boring.json` declares what the hub may use. **Add a definition; add
it to `boring.json` only if the hub must be able to call it.** An undeclared
definition is internal: it works inside the app and is absent from the manifest.

## Which capability

| The need | Create | Declare in boring.json `exposes` |
|---|---|---|
| One model call with a contract | `agents/<name>/agent.md` (+ `rules.md`, `tool.json`) | `agents.<name>: "<one line>"` if the hub calls it |
| Several agents with a lifecycle (a result produced from parts) | `agents/<name>/JOB.md` + `index.mjs` (`plan`, `collect`) | `jobs.<name>` |
| A chat with history over one agent | `agents/<name>/CHAT.md` (+ optional `index.mjs` `context`) | `chats.<name>` |
| A pure function an agent or the hub calls | `tools/<name>/tool.json` (`runtime: sandbox`) + `tools/<name>/index.js` | `tools.<name>: { runtime, description }` |
| A function that needs the database, the network or a secret | `tools/<name>/tool.json` (`runtime: server`) + `server/src/tools/<name>.ts` | `tools.<name>` |
| A component bound to data that the hub can frame | `web/src/views/<name>/index.tsx` (+ register it in `web/src/main.tsx`) | `views.<name>: { shows, description }` |
| The app's own screen | `web/src/pages/<name>/index.tsx` | `pages.<name>` |

An agent alone suffices for most features. Add a job only when the feature
coordinates several agents with a lifecycle, a chat only when people talk to
the agent over turns. Names are unique across `agents/`.

## An agent

```
agents/<name>/
  agent.md     front matter + system prompt (the body)
  rules.md     the owner's rules, read-only in Settings; they change by pull request
  tool.json    only when output: tool: { name, description, input: JSON schema } (the output schema)
  index.mjs    optional: buildMessage(input), validate(output), asText(output); then the agent needs server/
```

`agent.md` front matter: `name` (the folder), `title`, `description`, `model`
(`openai-codex/<model>`), `effort`, `max_tokens`, `output` (`tool` or
`markdown`), `helper_tools: [<tool names>]` (only declared tools), `inputs:`
(`name: { type, description, required }`).

- **Declarative** (no `index.mjs`): the message is the rules and the inputs;
  a markdown output must be non-empty, a tool output must carry `tool.json`'s
  required fields. The hub can run it from the files alone.
- **With code**: `validate(output)` is the contract the runtime applies before
  anything is stored (APP-B4); refuse with `fail("…")` from
  `agents/_shared/validate.mjs`, a message addressed to the model.
- Fake models (`server/src/fake-models.ts`) answer markdown agents; add a
  scripted reply for a tool agent, or its tests cannot run.
- **A Cloudflare app** (`project.md` `runtime: cloudflare`) does not run the
  agent runtime: its agents stay declarative and the hub runs them. No
  `index.mjs` on an agent or chat, no job; `verify check` refuses them.

## A tool

- **Sandbox**: `tools/<name>/index.js` defines `function run(input, ops)`, plain
  JavaScript with no import, no Node or network API, and only the `ops.<name>`
  its `tool.json` lists under `operations`. `verify check` refuses anything else.
- **Server**: `server/src/tools/<name>.ts` exports
  `handler(input, { db })`; validate the input with zod, and `await` every
  query (the same code runs on SQLite and on D1). On a Cloudflare app it uses
  no Node API (the `worker-portable` rule).
- `tool.json`: `description`, `runtime`, `input` and `output` JSON schemas.

## Data, routes, the web

- A table: `server/src/db/schema.ts`, then `npm run db:generate`, commit
  `server/drizzle/` (never `drizzle-kit push`). A write that edits names the
  revision it read (APP-B3, `server/src/routes/memories.ts` is the example).
- A route: `server/src/routes/<name>.ts` (Hono + `zValidator`), mounted in
  `server/src/app.ts`.
- The web reaches the server only through `web/src/lib/api.ts`
  (`web/src/lib/model.ts` holds the calls).

## Tests and verification

1. Unit (`npm test`): the route and the tool through the app
   (`test/unit/app.test.mjs`), an agent's contract when it has code.
2. End-to-end (`test/e2e/journey.spec.mjs`) when a person sees something new.
3. `node scripts/verify.mjs check`, then drive it with the **verify-app** skill.
4. The feature map: the area file in `docs/verify/` for what a person can do.

## Never

- Expose something by accident: declare it, or keep it internal.
- Call a model outside the runtime, or give a sandbox tool an import.
- Edit `vendor/`.
