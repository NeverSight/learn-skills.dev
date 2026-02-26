---
name: atomemo-plugin-development
description: >
  Use this skill for all Atomemo plugin development work — always consult it before
  answering, since it contains authoritative CLI commands, SDK patterns, and workflows
  that may differ from your general knowledge. Invoke whenever the user asks about:
  creating Atomemo plugin projects (atomemo plugin init, bun commands, project
  structure), implementing Tool plugins (ToolDefinition, external API wrappers),
  defining Model plugins (ModelDefinition, LLM integrations), defining Credential
  plugins (CredentialDefinition, API keys, OAuth tokens), configuring declarative
  parameters, debugging plugin hub connections, or publishing to the marketplace.
  Also invoke when developers want to expose their code or services to Atomemo users,
  even if they don't say "plugin". Do NOT invoke for: VS Code, Chrome, Obsidian,
  Figma, or Raycast plugins; npm package publishing; or general Atomemo workflow
  configuration (scheduling, triggers, node setup) that isn't about building plugins.
---

# Atomemo Plugin Development

You are helping a developer build an Atomemo plugin. Atomemo is Choiceform's workflow
automation platform. Plugins extend it with new Tools (external API calls, functions)
and Models (LLM definitions).

## Architecture Overview

```plain
Host (Atomemo App)
      ↕  (secure, decoupled)
  Plugin Hub              ← intermediary, handles security + comms
      ↕
  Your Plugin             ← SDK + your business logic
```

- **Plugin Hub**: Prevents direct host↔plugin contact; protects both sides
- **SDK** (`@choiceopen/atomemo-plugin-sdk-js`): Handles communication, types, i18n, lifecycle
- **CLI** (`@choiceopen/atomemo-plugin-cli`): Project scaffolding, dev server, build, publish

## Three Plugin Types

| Type | What it does | Source directory |
| ---- | ----------- | --------------- |
| **Tool** | Invokes external APIs or runs local logic | `src/tools/` |
| **Model** | Describes an LLM (capabilities, pricing, params) | `src/models/` |
| **Credential** | Defines auth requirements (API keys, OAuth tokens) | `src/credentials/` |

A single plugin can contain multiple Tools, Models, and Credentials.

## Identify the Scenario

**Scenario A — New project from scratch:**
Read `references/quick-start.md`, then the appropriate type guide.

**Scenario B — Adding to an existing project:**
Read the relevant guide directly:

- Adding a Tool → `references/tool-plugin.md`
- Adding a Model → `references/model-plugin.md`
- Adding Credentials → `references/credential.md`
- Configuring Parameters → `references/declarative-parameters.md`

**Scenario C — Publishing:**
Read `references/publishing.md`.

---

## Workflow

### Step 1: Clarify intent

Ask (or infer from context):

1. New project or adding to an existing one?
2. Tool plugin, Model plugin, or both?
3. Does it need credentials (API keys, tokens)?
4. Target language? (TypeScript strongly recommended)

### Step 2: Verify the Atomemo CLI

Before running any `atomemo` command, check that the CLI is installed and up to date.

**Check if installed:**

```bash
atomemo --version
```

If the command is not found, install it first:

```bash
npm install @choiceopen/atomemo-plugin-cli --global
```

**Check if up to date:**

```bash
# Get the currently installed version
atomemo --version

# Get the latest published version
npm view @choiceopen/atomemo-plugin-cli version
```

If the versions differ, upgrade before proceeding:

```bash
npm install @choiceopen/atomemo-plugin-cli@latest --global
```

Both of these checks are safe to run automatically. Confirm the upgrade with the user before running it — it modifies their global environment.

### Step 3: Set up the project (new projects only)

See `references/quick-start.md`. Key commands:

```bash
# atomemo auth login   ← user must run this manually (device auth flow, requires browser)
atomemo plugin init --no-interactive -n <plugin-name> -d "<description>" -l typescript
cd <plugin-name>
atomemo plugin refresh-key
bun install
bun run build
bun run ./dist             # connects to Plugin Hub
```

### Step 4: Check in with the developer (always required)

Project scaffolding is complete. Before writing any code, you must ask the developer what they want to do next.

**Do NOT continue to Step 5 until the developer has replied.**

Your message should (in whatever language the developer used when invoking this skill):

1. Confirm the project directory has been created
2. Recommend they `cd` into it and restart the Agent from that directory — this gives the Agent accurate working directory context for all subsequent work (planning, implementation, builds)
3. Ask them to choose:
   - **Plan mode first** (recommended for complex features) — map out the approach before writing code
   - **Implement directly** — if the feature is already well-defined and straightforward

This step is complete only when the developer has made their choice.

### Step 5: Implement plugin components

For each component:

1. Create the definition file in the appropriate directory
2. Implement the required interface (`satisfies ToolDefinition` / `ModelDefinition` / `CredentialDefinition`)
3. Register in `src/index.ts`

**Project file layout:**

```plain
src/
  index.ts           ← entry point; register everything here
  tools/             ← one file per tool
  models/            ← one file per model
  credentials/       ← one file per credential type
  i18n/              ← translations (auto-generated by SDK)
```

**Registration pattern (index.ts):**

```typescript
import { createPlugin } from "@choiceopen/atomemo-plugin-sdk-js"
import { myTool } from "./tools/my-tool"
import { myModel } from "./models/my-model"
import { myCredential } from "./credentials/my-credential"

const plugin = await createPlugin({ /* manifest fields */ })
plugin.addTool(myTool)
plugin.addModel(myModel)
plugin.addCredential(myCredential)
plugin.run()
```

### Step 6: Internationalization

All user-facing strings support i18n. **Always use the `t()` helper** — it keeps
translations centralized and consistent across the project:

```typescript
import { t } from "../i18n/i18n-node"

display_name: t("WEATHER_TOOL_DISPLAY_NAME"),
description: t("WEATHER_TOOL_DESCRIPTION"),
```

Only fall back to inline `I18nText` objects `{ en_US: "...", zh_Hans: "..." }` when
the `t()` helper is not available (e.g., in one-off scripts or test fixtures).

To generate the i18n types, **ALWAYS** use the following command after adding new keys to the translation files:

```bash
bun typesafe-i18n --no-watch
```

### Step 7: Test locally

```bash
bun run build        # build the plugin
bun run ./dist       # connect to Plugin Hub
```

`bun run dev` is watch mode for rebuilding on file changes, but it does **not** connect to the Hub. You must run `bun run ./dist` (the built output) to establish the Hub connection.

Successful connection shows: `status: ok, response: { success: true }`

### Step 8: Publish (when ready)

See `references/publishing.md`. Key steps:

1. Ask the user to run `bun run release` — this is interactive (prompts for version selection) and must be run by the user, not the agent
2. Fork `atomemo-official-plugins` repo
3. Add plugin to `plugins/<your-plugin-name>/`
4. Open PR with title `feat(plugin): add <your-plugin-name>`

---

## Reference Files

Load these on demand based on what the developer needs:

| File | When to read |
| ---- | ----------- |
| `references/quick-start.md` | New project setup |
| `references/tool-plugin.md` | Building Tool plugins |
| `references/model-plugin.md` | Building Model plugins |
| `references/credential.md` | Defining credentials |
| `references/declarative-parameters.md` | Parameter types and UI config |
| `references/declarative-parameters-examples.md` | Ready-to-copy parameter examples |
| `references/publishing.md` | Publishing to the marketplace |

---

## CLI Automation

When helping a developer set up a new project, you can execute CLI commands on their behalf using the Bash tool — except for `atomemo auth login`, which requires the user to complete OAuth in a browser.

**What you can run automatically:**

```bash
# CLI environment check — always run these before any atomemo command:
atomemo --version                                  # check if installed; install if missing
npm view @choiceopen/atomemo-plugin-cli version    # check latest version

# Install or upgrade (confirm with user before running — modifies global environment):
npm install @choiceopen/atomemo-plugin-cli --global
npm install @choiceopen/atomemo-plugin-cli@latest --global

# Non-interactive project init — provide all flags to skip prompts:
atomemo plugin init --no-interactive -n <plugin-name> -d "<description>" -l typescript

# These are always non-interactive:
atomemo plugin refresh-key
bun install
bun run build
bun run ./dist    # connects to Plugin Hub; bun run dev only rebuilds, does not connect
```

**What you must NEVER run — `atomemo auth login`:**

This command uses a device authorization flow that requires a human to interact
with a browser. Running it in an automated context will block indefinitely or
terminate before the user can complete authorization.

Instead, follow this protocol:

1. Tell the user they need to authenticate and ask them to run the command themselves:

   ```bash
   atomemo auth login
   ```

2. Explain what will happen: the command prints a verification URL and a short
   code; they must open the URL in their browser and enter the code to approve
   the device.
3. Wait for the user to confirm they have completed the login.
4. Once they confirm, verify the result yourself:

   ```bash
   atomemo auth status
   ```

   A successful response confirms the login is active. If it fails, walk the user
   through the login step again.

Always confirm with the user before running CLI commands that create files or
modify their environment.

## Common Mistakes to Avoid

- **Plugin naming**: Must match `/^[a-z][a-z0-9_-]{2,62}[a-z0-9]$/` — lowercase only, 4–64 chars, starts with a letter, ends with a letter or digit, no consecutive special chars
- **Hardcoded secrets**: Never hardcode API keys; always use the Credentials system
- **Model naming**: Must follow `provider/model_name` format (4–64 chars, alphanumeric/underscore/hyphen/slash only)
- **Dev key expiry**: Debug API key expires after 24 hours; run `atomemo plugin refresh-key` to renew
- **Missing registration**: Every tool/model/credential must be registered in `src/index.ts`
