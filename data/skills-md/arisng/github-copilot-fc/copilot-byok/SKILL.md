---
name: copilot-byok
description: Configure and switch between BYOK (Bring Your Own Key) LLM providers for both GitHub Copilot CLI and VS Code Chat. Use when setting up OpenAI, Azure OpenAI, Anthropic, Ollama, Moonshot, OpenCode Go, OpenRouter, or other OpenAI-compatible endpoints; creating or switching reusable provider profiles for CLI; switching between multiple accounts (API keys) for the same provider; configuring chatLanguageModels.json for VS Code; calculating max prompt or output token overrides; configuring wire API and reasoning effort; or troubleshooting COPILOT_PROVIDER_BASE_URL, COPILOT_PROVIDER_TYPE, COPILOT_PROVIDER_API_KEY, COPILOT_MODEL, COPILOT_PROVIDER_WIRE_API, COPILOT_PROVIDER_MAX_PROMPT_TOKENS, COPILOT_PROVIDER_MAX_OUTPUT_TOKENS, COPILOT_OFFLINE, and VS Code language model settings.
metadata:
  author: arisng
  version: 0.17.0
  lastVerified: 2026-08-09
---

# Copilot BYOK Provider Configuration

Use this skill to configure BYOK (Bring Your Own Key) LLM providers for **both GitHub Copilot CLI and VS Code Chat**. Manage repeatable CLI provider profiles and VS Code `chatLanguageModels.json` from a single source of truth.

## Follow this workflow

1. Determine the **provider** (OpenCode Go, OpenRouter, …) and the **harness** (Copilot CLI or VS Code Chat) the user needs.
2. Read the reference file that matches the current need:
   - Provider-specific content is grouped by LLM provider under `references/provider/<provider>/` (each provider has harness-specific files).
   - Universal/shared mechanisms (env vars, API-key storage, VS Code file rules, reasoning-effort lookup, CLI account switching) live under `references/shared/`.
3. For CLI, prefer `scripts/byok-profile.ps1` for repeated use or quick switching between providers.
4. For VS Code, use the **Chat: Manage Language Models** UI command (see the provider's `vs-code.md`).
5. Keep secrets out of files. Prefer `${ENV_VAR}` placeholders and user-scoped environment variables.

## Choose the path

### Provider + harness matrix

Read the provider file first, then the harness file:

| Provider | Copilot CLI | VS Code Chat |
|----------|-------------|--------------|
| OpenCode Go | [`references/provider/opencode-go/cli.md`](references/provider/opencode-go/cli.md) | [`references/provider/opencode-go/vs-code.md`](references/provider/opencode-go/vs-code.md) |
| OpenRouter | [`references/provider/openrouter/cli.md`](references/provider/openrouter/cli.md) | [`references/provider/openrouter/vs-code.md`](references/provider/openrouter/vs-code.md) |
| Command Code | [`references/provider/commandcode/cli.md`](references/provider/commandcode/cli.md) | [`references/provider/commandcode/vs-code.md`](references/provider/commandcode/vs-code.md) |
| Moonshot | [`references/provider/moonshot/cli.md`](references/provider/moonshot/cli.md) | [`references/provider/moonshot/vs-code.md`](references/provider/moonshot/vs-code.md) |

### Shared references (any provider, any harness)

- **Env-var semantics / provider types / wire-format rules**: `references/shared/environment-variables.md` — read for manual one-off CLI setup or token-limit sizing.
- **API key storage or rotation**: `references/shared/api-key-storage.md`.
- **`chatLanguageModels.json` mechanism** (secret storage, per-agent model pinning, quick start, troubleshooting): `references/shared/chat-language-models-json.md` — read for VS Code BYOK setup.
- **Reasoning-level configuration**: read the grounded per-model lookup `references/shared/reasoning-effort-lookup.md`, then apply `--reasoning-effort` per invocation. Cross-surface mapping (CLI flag ↔ env var ↔ SDK API ↔ VS Code) lives in the `copilot-cli-subsession` skill's [`copilot-sdk-parity-matrix.md`](../copilot-cli-subsession/references/copilot-sdk-parity-matrix.md).
- **Multiple accounts for one provider (CLI)**: `references/shared/copilot-cli-accounts.md`.

> VS Code uses `chatLanguageModels.json` and **ignores** `COPILOT_PROVIDER_*` env vars.

### Other scenarios

- **New provider not yet documented**: create `references/provider/<provider>/` with `cli.md` + `vs-code.md` (mirroring `opencode-go/`), reuse `references/shared/*`, and register it in the matrix above. Keep the provider's model/reasoning-effort rows in the provider file, not in `shared/reasoning-effort-lookup.md`.

## Use the profile manager first

Use `scripts/byok-profile.ps1` when the user wants repeatable setup, named profiles, or quick switching.

Run the following commands from the installed `copilot-byok` skill folder (the folder that contains this `SKILL.md`).

Common commands:

```powershell
# List profiles
.\scripts\byok-profile.ps1 list

# Add a profile interactively
.\scripts\byok-profile.ps1 add

# Inspect a stored profile
.\scripts\byok-profile.ps1 show openai

# Run Copilot CLI with a profile for one session
.\scripts\byok-profile.ps1 run ollama

# Apply a profile to the current shell
. .\scripts\byok-profile.ps1 set-env openai
```

Pass extra Copilot CLI arguments through `run` (do not pass `--model`; model is sourced from the profile):

```powershell
.\scripts\byok-profile.ps1 run openai --help
```

Profiles are stored in `~/.copilot/byok-profiles.json` or `$env:COPILOT_HOME\byok-profiles.json`.

## Switch between multiple provider accounts

When you have multiple subscriptions for the same provider (for example, **two OpenCode Zen accounts** with separate API keys), register the accounts once and switch per session — no profile edits needed.

### 1. Register accounts in `~/.copilot/byok-profiles.json`

```json
{
  "accounts": {
    "opencode-home": { "keyEnv": "OPENCODE_API_KEY_HOME", "label": "OpenCode Zen (Home)" },
    "opencode-work": { "keyEnv": "OPENCODE_API_KEY_WORK", "label": "OpenCode Zen (Work)" }
  },
  "activeAccount": "opencode-home"
}
```

`keyEnv` holds the **name** of an environment variable with that account's key — never the raw key. `activeAccount` sets the default.

### 2. Opt profiles in with `accountGroup`

Add `"accountGroup": "opencode"` to each profile that should use the registry (the `add` wizard sets it automatically for the OpenCode Go preset). Profiles without `accountGroup` never participate.

### 3. Manage and switch accounts

```powershell
.\scripts\byok-profile.ps1 accounts
.\scripts\byok-profile.ps1 use opencode-work
.\scripts\byok-profile.ps1 run opencode-go-deepseek-v4-flash
.\scripts\byok-profile.ps1 run opencode-go-deepseek-v4-flash --account opencode-work
```

Resolution order: `--account` flag → profile `account` pin → `activeAccount`. If nothing resolves, the profile falls back to its legacy `apiKey` with a warning. For sub-sessions, pass `-ByokAccount opencode-work` to `Invoke-CopilotCliSubSession.ps1`.

### 4. Add the second account in VS Code Chat

VS Code ignores the CLI `accounts` registry — each account is a **separate provider entry** with its own key in secret storage. To add the second account:

1. **Chat: Manage Language Models → Add Models → Custom Endpoint**, name it `OpenCode Go (Work, OpenAI)`, paste the work key, API Type *Chat Completions*. This stores the key and writes a `${input:chat.lm.secret.*}` reference.
2. Run the helper from the skill's `scripts/` folder — it renames the existing `OpenCode Go (OpenAI|Responses|Anthropic)` providers to `(Home, …)` and clones them as `(Work, …)` using the new secret reference:

```powershell
.\scripts\opencode-vscode-add-work-account.ps1
```

3. Reload the window (**Developer: Reload Window**); both accounts appear in the model picker.

See `references/provider/opencode-go/vs-code.md` for the full manual table when you need more than two accounts, and `references/shared/copilot-cli-accounts.md` for the CLI registry semantics.

## Reference index

References are grouped by **provider** (under `references/provider/`) and by **universal/shared aspects** (under `references/shared/`).

- `references/provider/opencode-go/cli.md`
  - Read when configuring **OpenCode Go** for **Copilot CLI**: prerequisites and keys, base URL + endpoint per family, available-models table with reasoning-effort support, manual env-var examples, GPT-5.6 Luna wire-format matrix + grounded token overrides, profile-based setup.
- `references/provider/opencode-go/vs-code.md`
  - Read when configuring **OpenCode Go** for **VS Code Chat** (`chatLanguageModels.json`): full provider JSON per model family (chat-completions / responses / messages), multiple OpenCode Zen accounts (Home/Work) incl. the `opencode-vscode-add-work-account.ps1` helper.
- `references/provider/openrouter/cli.md`
  - Read when configuring **OpenRouter** for **Copilot CLI**. Covers environment variables, `:floor` / `:nitro` routing suffixes, CLI profile, manual env-var setup, and the empirical per-model audit.
- `references/provider/openrouter/vs-code.md`
  - Read when configuring **OpenRouter** for **VS Code Chat** (`chatLanguageModels.json`). Covers the UI quick-add path and the ready-to-use provider JSON.
- `references/provider/openrouter/README.md`
  - OpenRouter provider index: harness router + key provider facts.
- `references/provider/commandcode/cli.md`
  - Read when configuring **Command Code** for **Copilot CLI**: prerequisites and keys, base URL, available models with token overrides, manual env-var examples, CLI profiles, multiple accounts.
- `references/provider/commandcode/vs-code.md`
  - Read when configuring **Command Code** for **VS Code Chat** (`chatLanguageModels.json`): UI quick-add and the full 9-model provider JSON.
- `references/provider/commandcode/README.md`
  - Command Code provider index: harness router + key provider facts.
- `references/provider/moonshot/cli.md`
  - Read when configuring **Moonshot (Kimi AI)** for **Copilot CLI**: prerequisites, base URL, available models, proxy setup for `top_p` workaround, profile examples, troubleshooting.
- `references/provider/moonshot/vs-code.md`
  - Read when configuring **Moonshot (Kimi AI)** for **VS Code Chat** (`chatLanguageModels.json`): UI quick-add, full provider JSON with proxy support, VS Code tasks configuration.
- `references/provider/moonshot/README.md`
  - Moonshot provider index: key facts, model list, special requirements (`top_p` proxy).
- `references/shared/environment-variables.md`
  - Read when you need CLI env-var semantics, provider types, wire-format rules, model requirements, token-override calculation, or offline-mode notes (any provider).
- `references/shared/api-key-storage.md`
  - Read when the user needs secure key storage, persistent Windows environment variables, key rotation, or `${ENV_VAR}` placeholder guidance.
- `references/shared/chat-language-models-json.md`
  - Read when the user wants to configure BYOK models in **VS Code Chat**. Covers the config file, secret storage, shared model-configuration rules, per-agent model pinning via `.agent.md` frontmatter, agent-specific model settings, quick start, and troubleshooting.
- `references/shared/reasoning-effort-lookup.md`
  - Read when you need the per-model `--reasoning-effort` support lookup and verification workflow (the authoritative source that `copilot-cli-subsession` defers to).
- `references/shared/copilot-cli-accounts.md`
  - Read when the user holds multiple accounts for the same provider (CLI registry, `accounts`/`use`/`--account`, resolution order).
- `references/provider/opencode-go/README.md`
  - Provider index: harness router + key provider facts + usage limits.

## Apply these operating rules

- Prefer `${ENV_VAR}` placeholders over raw API keys in JSON.
- Treat `openai` as the default provider type for OpenAI-compatible endpoints (Ollama, vLLM, Foundry Local, Moonshot, Command Code).
- Set `COPILOT_PROVIDER_TYPE=azure` only for Azure OpenAI and `anthropic` only for Anthropic.
- For GPT-5 class OpenAI models, prefer `COPILOT_PROVIDER_WIRE_API=responses`.
- Use `COPILOT_OFFLINE=true` only when the user explicitly wants Copilot CLI isolated from GitHub services; note that full isolation still depends on the provider endpoint being local or private.
- If the model is not in Copilot CLI's built-in catalog, set explicit prompt and output token overrides instead of assuming Copilot will infer them correctly.
- Provider-specific rules (base URLs, model ID formats, proxy configuration, special requirements) are documented in each provider's `references/provider/<provider>/cli.md` file.

## Configure reasoning effort correctly

Use Copilot CLI's `--reasoning-effort` option for model reasoning level control. The authoritative per-model lookup — which levels a specific model supports and the recommended default — is `references/shared/reasoning-effort-lookup.md` (OpenCode Go focus; method applies to any BYOK model).

- Supported levels: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` (per-model subset may vary — e.g., DeepSeek V4 models on OpenCode Go only support `low`, `medium`, `high`; `minimal` is newer, verified in CLI 1.0.77).
- Apply it per run, for example:

```powershell
.\scripts\byok-profile.ps1 run dprocess-openai-gpt-54 --reasoning-effort medium
```

For OpenAI models, you may also enable summaries:

```powershell
.\scripts\byok-profile.ps1 run dprocess-openai-gpt-54 --reasoning-effort high --enable-reasoning-summaries
```

### Model compatibility warning

Not all models support Copilot CLI's `--reasoning-effort` levels. If you get an error like:

```
Model "glm-5.2" does not support reasoning effort configuration (requested: "high").
```

it means the model's API does not expose controllable reasoning effort levels. See `references/shared/reasoning-effort-lookup.md` for the authoritative per-model lookup.

When using models without reasoning-effort support, omit `--reasoning-effort` entirely. The model will use its built-in default reasoning behavior.

The profile system tracks this per model. Profiles for models that do not support reasoning effort set `"reasoningEffortSupported": false`. The `run` command detects incompatible `--reasoning-effort`/`--effort` arguments, **strips them before forwarding to Copilot CLI**, and displays a clear notice.

Do not claim a dedicated `COPILOT_*` environment variable exists for reasoning effort unless `copilot help environment` in the user's installed CLI version explicitly lists one.

## Grounding and evidence standard

When answering questions in this domain, always separate grounded facts from inference:

1. Cite authoritative evidence used (for example, `copilot --help`, `copilot help environment`, provider model docs).
2. State what is directly evidenced versus inferred operational guidance.
3. End with an explicit conclusion:
  - `Grounding status: evidence-backed` when all key claims are directly supported.
  - `Grounding status: mixed (evidence + inference)` when any recommendation is inferred.

Do not present inferred workarounds (for example wrapper aliases for sticky defaults) as first-class documented product features.

## Calculate token overrides conservatively

When the user asks for `COPILOT_PROVIDER_MAX_PROMPT_TOKENS` or `COPILOT_PROVIDER_MAX_OUTPUT_TOKENS`:

1. Get the model's documented context window.
2. Pick a realistic max output budget for the workload.
3. Reserve a safety buffer for tool calls, system instructions, and multi-turn variance.
4. Compute:

`maxPromptTokens = contextWindow - plannedMaxOutput - safetyBuffer`

Prefer stable values over theoretical maximums. If the user reports context-limit failures, reduce prompt tokens by 5-10% and retry.

### Provider-enforced limits vs theoretical context windows

Some gateway providers (notably **OpenCode Go**) enforce per-request token limits **lower than the model's theoretical context window**. The native DeepSeek V4 Flash model supports 1M context, but OpenCode Go's gateway enforces an effective limit around ~300K for prompt tokens. Using the theoretical 1M to calculate maxPromptTokens (840K) will cause compaction failures with `400 Error from provider (Console Go): Upstream request failed`.

**Empirical approach**: Test compaction at increasing context-usage levels. When compaction fails, derive the provider's effective limit:

```
maxPromptTokens = successfulCompactionTokens / 0.78
```

For OpenCode Go's DeepSeek V4 models, the empirically validated safe values are:
- `maxPromptTokens`: 325,000
- `maxOutputTokens`: 64,000

This same limit discovery process applies to any provider whose gateway enforces stricter limits than the model's published context window.

## Troubleshoot in this order

1. Confirm the base URL, provider type, model name, and API key source.
2. Confirm the model supports streaming and tool calling.
3. If using a stored profile, run `show` or `list` to verify the saved values.
4. If `${ENV_VAR}` placeholders are used, confirm the environment variable actually exists.
5. If long-context models fail, add or lower explicit max prompt and output token overrides.

## Related skill

For MCP server configuration rather than model-provider configuration, read `../copilot-cli-mcp-config/SKILL.md`.
