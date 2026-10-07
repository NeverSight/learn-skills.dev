---
name: provider-adapters
description: "Provider-specific auth sources, quota windows, endpoint shapes, error recovery, and quirks for the quota-axi providers with dedicated sections below; Muse is covered in the README provider notes."
user-invocable: false
---

# Provider Adapters & Quirks

This reference details the credential sources, endpoint contracts, quota window structures, error handling, and vendor-specific quirks for the providers with dedicated sections below. Muse has no section here; its specification lives in the README provider notes.

---

## 1. Anthropic Claude (`claude`)

- **Credential Sources** (evaluated in order):
  1. `env` (`CLAUDE_CODE_OAUTH_TOKEN`): Takes top precedence because Claude Code resolves environment tokens before opening local stores. It has no `expiresAt` or refresh token; never invent either and never route it through delegated refresh. `claudeEnvOauthToken` in `src/lib/claude-profile.ts` is the single reader. `claudeCredentialContextId` includes an env marker to prevent serving stored-credential cache snapshots for environment sessions.
  2. `oauth-file`: Reads the local profile credentials file.
  3. `keychain`: macOS Keychain item matching Claude Code's validated user account selector. Ambiguous service-only queries are forbidden. Value reads require an existing non-secret access marker (`0600`) or `--allow-keychain-prompt`. Keychain failures (including exit 44) must never retire the cache.
- **Quota Windows**:
  - Windows can include `five_hour`, `seven_day`, `seven_day_opus`, and `extra_usage`.
  - When the OAuth usage payload includes a `limits` array, that array is authoritative over top-level fields. It exposes active limits, including model-scoped limits (e.g. Fable) via `scope.model.display_name`, assigned window ID `model:<slug>`.
- **Soft Expiry**: A stored-expired, refreshable Claude token definitively rejected by the endpoint produces `authStatus: expired_refreshable` (a soft failure retaining cache), never `auth_required`.
- **Native Quota Probe**: Bounded opt-in native inference quota probe lives in `src/providers/claude-native-quota.ts`. Keep it distinct from delegated refresh.
- **Delegated Refresh**: Permitted via `claude doctor` only when no Claude Code process is running (`src/lib/running-processes.ts`).

---

## 2. OpenAI Codex (`codex`)

- **Credential Sources** (evaluated in order):
  1. Native `$CODEX_HOME/auth.json` or `~/.codex/auth.json` OAuth.
  2. Pi `openai-codex` and any sibling `openai-codex-*` entries in the same Pi `auth.json`.
  3. CLI fallback via the `app-server` JSON-RPC probe.
- **Multi-Account Lanes**:
  - `src/providers/accounts.ts` collects distinct Pi entries and the native `codex-home` lane.
  - Accounts are matched and deduplicated on the ChatGPT account ID reported by the probe/store, never on email or token strings.
  - If a native reading matches an existing Pi lane account ID, it collapses into that lane, publishing whichever reading is fresher; coalescing never removes the shared `codex-home` cache slot by name, so another account's snapshot cannot be discarded. Contract: [README Multiple accounts](../../README.md#multiple-accounts).
- **Authorization Rules**: OAuth access token is authoritative. An expired `id_token` alone must never mark `auth-json` expired or skip the bearer probe. Never send `OPENAI_API_KEY` to ChatGPT quota endpoints.
- **Bound Conflict**: Codex model windows are metered separately as `additional_rate_limits`/`rateLimitsByLimitId`. If an inherited base weekly window reads zero while a model window retains allowance, quota-axi publishes `effectiveAvailability[].boundConflict` and reports scope `unknown` rather than asserting exhaustion.
- **Delegated Refresh**: Codex `app-server` JSON-RPC probe acts as both CLI fallback and delegated refresh.

---

## 3. Cursor (`cursor`)

- **Credential Sources**:
  1. Editor `state-vscdb`: Reads `$CURSOR_STATE_DB` or local Cursor state database via `sqlite3 -readonly` for `cursorAuth` values. If `sqlite3` is missing, report `sqlite3_unavailable` without attempting package installation.
  2. Cursor CLI (`cursor-agent` in `src/providers/cursor-cli-credential.ts`): macOS uses `cli-keychain`; Linux uses `cli-authfile` reading `accessToken` from `$CURSOR_CLI_CONFIG` or XDG `cursor/auth.json`.
  - Both sources operate independently; Cursor Desktop is not required.
  - Never read `refreshToken` or `cursor-refresh-token`. No delegated refresh exists for Cursor.
- **Quota Windows**:
  - Windows from `GetCurrentPeriodUsage`: `included_usage`, `auto_usage`, `api_usage`, `spend_limit`.
  - Grok Bot from `GetSandUsageStatus`: Metered separately under scope `grok_bot`. Kept off the IDE `all_models` bound. Do not invoke trial, banked-reset, or machine registration RPCs.
- **Monthly Billing Cycle Calculation**:
  - Resets on subscription renewal date. `startsAt` is calculated from `billingCycleStart` or by stepping `billingCycleEnd` back one calendar month (clamped to the shorter month).
  - Never substitute a fixed 30-day duration.

---

## 4. GitHub Copilot (`copilot`)

- **Credential Sources** (`COPILOT_SOURCE_ORDER`):
  1. `api`: `$GITHUB_COPILOT_APPS_JSON` or local `github-copilot/apps.json`.
  2. `copilot-cli:keychain`: Native secure store for standalone Copilot CLI (macOS Keychain or Windows Credential Manager via `src/lib/windows-credential.ts`).
  3. `gh:hosts.yml`: Narrow block-mapping reader in `src/providers/gh-cli-credential.ts` that extracts only the `github.com` host `oauth_token`. Never read the `gh` keyring or `GH_TOKEN`/`GITHUB_TOKEN`.
- **Scope & Entitlement**:
  - Public GitHub tokens only. Enterprise tokens are treated as unavailable on the public endpoint.
  - Quota snapshot windows include `chat`, `completions`, and `premium_interactions`.
  - If the endpoint returns entitlement without numeric quota windows, return a fresh report with `windows: []` rather than inventing numbers or percentages.
  - Native CLI readings (`source: cli`) are never cached.

---

## 5. xAI Grok (`grok`)

- **Credential Sources**:
  1. Grok CLI session auth: `$GROK_AUTH_JSON`, inline `$GROK_AUTH`, `$GROK_AUTH_PATH`, or `~/.grok/auth.json`. Recognizes official Grok Build OIDC records scoped to `auth.x.ai` with `auth_mode: oidc`.
  2. Pi `xai` entry: `$PI_CODING_AGENT_DIR/auth.json` (OAuth or API key).
- **Usability & Fallback**:
  - Usable if either CLI or Pi source is usable. True sign-out requires all applicable sources unavailable or rejected.
  - Consumer credits are fetched via `GetGrokCreditsConfig`. If rejected by an official Build/Pi OAuth token, probe the no-spend model catalog (`cli-chat-proxy.grok.com/v1/models` for Build, `api.x.ai/v1/models` for Pi), discard the response body, and report `authStatus: usable` with empty windows. Never derive quota from model presence.
  - Pi API key establishes usable, unmeasurable model auth.
  - Delegated refresh: Permitted via `grok models`. Cache fallback accepts only `web` source snapshots.

---

## 6. Moonshot Kimi (`kimi`)

- **Quota Windows**:
  - `/usages` returns a map (`limit_5h`, `limit_7d`, `limit_month_total`, `limit_month_code`) or legacy `usage` + `limits[]`. Ratios are read strictly from `used_ratio`.
  - `limit_month_code` is the code-typed share of `limit_month_total`, not a separate cap. It carries `percentUsed` and `shareOf: month_total`. It never bounds a scope or derives a remaining allowance. Default TOON formats it as an attention `share` row; TUI displays percent used of parent.
  - Any declared entry lacking a usable ratio is marked in `state.untrustedWindowIds` (`usages:<key>`), degrading the bound to `partial`.
- **Dual Deployment Environments**:
  - `src/providers/kimi-code-config.ts` reads `config.toml` (`storage`, `key`, `oauth_host`, `base_url`).
  - Region allowlist restricts requests to Kimi Code's two official deployments (global vs mainland China). Never pair one deployment's token with another's host origin.
  - If configuration cannot be parsed conclusively, mark `environment_unconfirmed` and open no credential to avoid cross-environment cache corruption.
- **Pi Source & Expiry**:
  - Pi `kimi-coding` entry (api_key or oauth). Refreshable expired credentials produce non-definitive failures preserving cache. Refresh token values are never read or exchanged.

---

## 7. Z.AI GLM (`zai`)

- **Credential Sources**: Pi `auth.json` `zai` `api_key` first (source `pi:zai`), then opencode `auth.json` (`zai-coding-plan` or alias).
- **Endpoint**: Single GET to `/api/monitor/usage/quota/limit` with the key in a Bearer `Authorization` header.
- **Window Decoding**: Tolerant schema mapping using magic numbers:
  - `TOKENS_LIMIT` / `CREDIT_LIMIT`: `unit: 3, number: 5` -> `five_hour`; `unit: 6, number: 1` -> `weekly`.
  - `TIME_LIMIT` -> `mcp_month`.
  - Unrecognized or duplicate limits degrade to `kind: "unknown"` windows named in `state.untrustedWindowIds`.
- **Bound Separation**: `zaiSemantics` keeps usage windows under `all_models` bound and `mcp_month` under `tools` bound.

---

## 8. OpenCode Go (`opencode-go`)

- **Quota Semantics**: Rolling 5-hour ($12), weekly ($30), and monthly ($60) stacked plan caps jointly bind `all_models`. Requests are blocked when any cap is hit.
- **Limitations**: The endpoint supplies no cycle duration of its own, so plan-declared cycle lengths fill in when the payload carries none (a payload-supplied duration still wins) and pace, runway, and selection are measurable. The endpoint provides no Zen balance. An exhausted plan window with balance fallback reports plan-exhausted with fallback named in prose.
- **Sources**: `defaultOpenCodeGoCredentialSources` (supports opt-in Pi auth). Read-only; no refresh delegate.

---

## 9. Google Antigravity (`agy`)

- **Discovery & Transport**: Prefers installed CLI command `agy -p "/quota" --output-format json` (bounded read, not an agent session). Falls back to active loopback endpoint.
- **CSRF Handling**: Loopback 401 with `missing CSRF token` is treated as `unavailable`, preserving disk cache.
- **Stale Resets**: Readings with `resetsAt` in the past are marked stale.
- **Safety**: Antigravity is strictly read-only: never reads memory, signs in, mutates config, or contacts unowned ports.

---

## 10. Command Code (`commandcode`)

- **Credential Sources**: Pi `commandcode`, `$COMMAND_CODE_API_KEY`, `$COMMANDCODE_API_KEY`, `~/.commandcode/auth.json`, `~/.omp/agent/auth.json`.
- **Endpoints**: `GET /alpha/whoami?limits=1` and `GET /alpha/billing/credits` via `providerFetch`.
- **Bound Interpretation**: Exact `credits.remaining` plus `five_hour`/`weekly` form `included_credits` bound only when both windows are present and trusted. A credit-only reading reports balance as an attention `credits` row, never `no_quota` or derived percentage.
- **Context Scoping**: Reuses stale snapshots only after successful `whoami` matches the source/account context.

---

## 11. ElevenLabs (`elevenlabs`)

- **Credential Source**: `$ELEVENLABS_API_KEY` (sent as `xi-api-key`). CLI OAuth bundle is not read.
- **Endpoint**: `GET /v1/user/subscription` via `providerFetch`.
- **Quota Windows**: Single `characters` window (`character_count`/`character_limit`). Reset derived by stepping `next_character_count_reset_unix` back by `character_refresh_period`.
- **Permissions**: HTTP 401 with `detail.status: missing_permissions` or HTTP 403 indicates a valid key lacking quota scope; reported as `authStatus: usable` without clearing cache.
- **Context Scoping**: Snapshots scoped by source plus SHA-256 digest of the API key.

---

## 12. DeepSeek & OpenRouter (`deepseek`, `openrouter`)

- **Credential Skeleton**: Shared env + Pi credential handling in `src/providers/env-pi-credential.ts` on top of `src/lib/pi-agent-dir.ts`.
- **Semantics**: Expose key caps or balances as raw credits with unknown effective semantics, never invented model headroom.

---

## 13. Alibaba Cloud (`alibaba`)

- **CLI Fallback**: Uses read-only `bl` usage command. Maintains established account bounds without own-window overrides unless empirical evidence exists.

---

## 14. MiniMax & MiMo (`minimax`, `mimo`)

- **Endpoints (MiniMax only)**: Balance and quota inspection endpoints. Context-scoped cache via SHA-256 context hashing of credential source and host. Read-only.
- **MiMo**: `MIMO_API_KEY` alone establishes usable auth; no endpoint is probed (quota display is dashboard/cookie based), nothing is cached, and windows stay empty.

---

## 15. Devin (`devin`)

- **Credential Sources** (evaluated in order):
  1. `env:WINDSURF_API_KEY`: non-blank `$WINDSURF_API_KEY` (optional `$WINDSURF_API_SERVER_URL`). A blank value selects nothing.
  2. `file:credentials.toml`: `$XDG_DATA_HOME/devin/credentials.toml`, `~/.local/share/devin/credentials.toml`, or `%APPDATA%\devin\credentials.toml` on Windows, reading the `windsurf_api_key` key.
  - The session token never expires and carries no refresh token: there is no delegated refresh, `devin` is never launched, and `devin auth login` appears only as sign-out advice after a definitive 401/403.
- **Endpoint**: One read-only Connect-JSON `POST` of `SeatManagementService/GetUserStatus` through `providerFetch`. The token is sent only to `https://server.codeium.com`; any other `api_server_url` origin is a skipped `unsupported_server` attempt and never receives the token.
- **Quota Windows**: `weekly` (`week`, 604,800s) plus `daily` only when `planInfo.hideDailyQuota` is explicitly `false` (it reuses the `session` kind: id `daily`, label `day`, 86,400s). Both bound `included_quota` jointly when both are trusted (weekly alone when `hideDailyQuota` is explicitly `true`), never `all_models`. A `billingStrategy` other than `BILLING_STRATEGY_QUOTA` publishes no windows, and a proto3-omitted percent with a present reset reads 0 remaining.
- **Context Scoping**: Snapshots carry an opaque SHA-256 of the answering source and first-party host plus a one-way digest of the token (`devinReadingContextId` in `src/providers/devin-cache-context.ts`); a definitive rejection retires only a snapshot whose identity matches the rejected token.

---

## 16. Higgsfield (`higgsfield`)

- **Credential Source**: The installed `higgsfield` CLI (`higgsfield-cli`). `inspectAuth` reports the command present or missing without probing quota; quota-axi never reads Higgsfield credential files, never runs `higgsfield auth token`, and never publishes the account email the status payload includes.
- **Fixed argv**: `higgsfield account status --json`, `higgsfield account transactions --json --size 100`, and `higgsfield generate list --json --size 20`, each bounded to 15 seconds. The transactions and jobs aux commands run concurrently; a failure omits that aux rather than failing the status reading and is additionally surfaced as a `degraded_source` attention row (`higgsfield-transactions` or `higgsfield-jobs`).
- **Quota Windows**: The status payload has no limit or reset field, so a `credits` window (scope `included_credits`) is published only when the first `account transactions` page holds a `subscription credits` grant as its only positive-credit entry and the balance reconciles with that grant plus the on-page entries newer than it (within floating-point slack); otherwise the raw `credits.remaining` balance is reported with no percentage. The grant must be on the first page. No cycle is invented: pace stays `unknown`, and runway reads `exhausted_now` at zero balance and `unknown` otherwise, naming `credits` in `unmeasurableWindowIds`.
- **Jobs rollup**: `generate list` entries are reduced to `jobs.{sampled,completed,failed,other}` counts; job ids, prompts, URLs, and model names are discarded. Those counts are stored with the snapshot the same way `credits` is; a snapshot that never carried jobs stays without them. Higgsfield is excluded from `--max-age` reuse because a CLI login switch is not a traced file and the status payload has no stable non-email account discriminator.
- **Fresh reuse**: `--max-age` / `QUOTA_AXI_MAX_AGE` never serves a Higgsfield reading; every Higgsfield quota call live-reads the vendor CLI.
- **Error handling**: A status failure classifies only from the closed sentinel set (`higgsfield_cli_unavailable`, `higgsfield_sign_in_required`, `higgsfield_status_malformed_json`, wrapped `higgsfield_status_failed`); never re-run keyword regexes over wrapped stderr.
- **Delegated Refresh**: None; `ProviderOptions.refreshCredentials` is ignored.
