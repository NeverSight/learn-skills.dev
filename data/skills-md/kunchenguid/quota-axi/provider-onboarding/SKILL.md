---
name: provider-onboarding
description: "Rules, checklist, credential selection machinery, multi-source handover, delegated refresh contract, and test discipline for onboarding new quota providers or modifying existing provider adapters in quota-axi."
user-invocable: false
---

# Provider Onboarding & Credential Architecture

This document defines the requirements, shared machinery, and safety invariants for onboarding new quota providers or modifying existing adapters in quota-axi.

## Clean-Room & Dependency Policy

- **Clean-room implementation**: Adapter behavior (retry-after handling, snake/camel field tolerance, window parsing) must be an original implementation derived solely from the vendor's own HTTP/OAuth behavior. quota-axi carries no vendored third-party adapter code. The Z.AI adapter is the single attribution exception (derived from opencode-glm-quota, MIT) credited in `src/providers/zai.ts`.
- **HTTP & proxy handling**: Remote HTTP requests must route through `src/lib/http.ts` (`providerFetch`) so standard `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` policies apply consistently without leaking proxy credentials in logs. Do not use global `fetch` directly.
  - Node 26 compatibility: `src/lib/http.ts` pairs the installed `undici` build's `ProxyAgent` with that same build's `fetch` because Node's built-in global fetch only accepts dispatchers from its bundled `undici`, and Node 26 rejects external `ProxyAgent` instances with `InvalidArgumentError: invalid onError method`.
- **Process table reads**: Any process-table inspection (e.g. Antigravity loopback detection or Claude process checks) must route through `currentUserProcessListArgs` in `src/lib/process.ts` to handle platform flag differences portably (Linux procps rejects BSD `-x` alongside `-u`).

---

## Provider Onboarding Checklist

When adding a new provider or migrating an existing adapter:

1. **Enumerate every source in ownership-stability order**:
   - Declare source priority via a named constant (e.g. `COPILOT_SOURCE_ORDER`).
   - Distinguish `absent`, `structurally_invalid`, `unsupported`, `read_error`, and `resolved` (`stored-valid` or `stored-expired`) at the typed local resolution boundary.
   - Route Pi agent entries through `classifyPiAuthEntry` in `src/lib/pi-auth-store.ts`.
   - Derive `credentialPresent` once from local resolution rather than ad hoc at call sites.

2. **Separate local resolution from the bounded read-only liveness probe**:
   - Enroll stored-expired credentials instead of skipping them.
   - Never infer liveness from presence alone.
   - Classify probe outcomes as `usable`, `live_no_quota`, `definitively_rejected`, or `transient`.
   - Only a first-party HTTP 401 or 403 is an authentication verdict. Server errors, rate limits, network timeouts, or schema mismatches are request failures, not auth verdicts.

3. **Handover only after definitive credential failure**:
   - An absent source is never marked degraded.
   - A present-but-broken source superseded by a working sibling is marked degraded on fresh readings only (`state.degradedSources`).
   - Stale means last-known cache.
   - Never exchange a refresh token, and never retain, log, render, cache, or send its value. Delegated refresh checks presence only; Pi brokers may read a stored refresh value only to classify it as a usable literal, then discard it.

4. **Add comprehensive adapter regression tests**:
   - Test cases: primary healthy, stored-expired plus live sibling, structurally invalid present, absent source, all rejected, refreshable expired, and transient failure stops handover.
   - Extend the cross-provider invariant table in `test/credential-contract.test.ts`.

---

## Credential Selection Machinery

Credential selection is shared in `src/providers/credential-selection.ts`:

- **Advisory stored expiry**: Stored `expiresAt` or `expired` fields are advisory only within a source, never a verdict or a reason to reorder declared sources.
- **Empirical testing**: Stored-expired credentials are tested in that source's fixed priority position before any sign-in or expired verdict. An empirically live credential always wins.
- **Transient failures**: Network errors, 5xx responses, or timeouts must never switch candidates within one source or become auth verdicts.
- **Adapters using selection**: Grok, Codex, Kimi, Command Code, Copilot, OpenCode Go, Devin, and Muse route through `selectCredential`. Codex, Kimi, Copilot, and Devin call it once per source so each provider's ownership-stability order remains authoritative.
- **Probe token safety**: A broker's `expired` resolution carries the stored token for probe use only; it must never be logged, cached, or rendered.
- **Profile-only mode**: `--profile-only` is the fail-closed single-account quota probe for Claude and Codex: it requires `CLAUDE_CONFIG_DIR` or `CODEX_HOME`, reads only that profile's native credential file, and bypasses alternate sources, delegated refresh, and quota cache access (full JSON keeps non-secret account/source/attempt evidence; ordinary output stays redacted). Omitting the flag must preserve legacy discovery and cache behavior. Contract: [README Profile-only quota reads](../../README.md#profile-only-quota-reads).

---

## Multi-Source Handover & Degraded Sources

- **Working store precedence**: A broken store must never speak for a provider whose sibling store still answers. Consult sources in priority order.
- **Handover boundaries**: Handover happens on credential problems only, never on transport, decoding, or server failures.
- **Tracking attempts**: `src/lib/source-attempts.ts` classifies attempts as `status: "failed"` or `skipped` with `credentialPresent`. Adapters set `degraded: false` on non-credential attempts (e.g. Grok's live model catalog probe).
- **Reporting degradation**: `withQuotaSemantics` in `src/interpretation.ts` publishes `state.degradedSources` on fresh readings only. `src/render.ts` emits the `degraded_source` attention row.

---

## Delegated Credential Refresh

Shared machinery lives in `src/providers/delegated-refresh.ts`. It is the **single carve-out** to quota-axi's read-only boundary:

- **Eligibility criteria**: A delegate is eligible ONLY when:
  1. The same stored access token is expired,
  2. The stored credential carries a refresh token, and
  3. The token was definitively rejected (HTTP 401/403) by the vendor's quota/user endpoint.
- **Mechanism**: quota-axi executes the vendor CLI's own smallest non-interactive rotation command (e.g. `claude doctor`, `grok models`) and re-reads the file/store that CLI updated.
- **Never exchange tokens**: quota-axi must never perform an OAuth refresh-token exchange itself. These tokens rotate on use; a second exchange signs the user out of the measured tool.
- **Presence only**: Delegated refresh inspects the refresh token's presence only (`Object.hasOwn(credential, "refresh_token")`). quota-axi never retains, logs, renders, caches, or sends its value. Pi brokers may read a stored refresh value only to classify it as a usable literal, then discard it.
- **Never signal the child**: Quota-axi never signals or force-kills a delegated child process. The budget bounds only how long quota-axi waits. The child runs in its own process group (`detached: true`) so Ctrl+C on a live TUI does not abort it. If the command exceeds budget, resolve as `unconfirmed`/`refresh_timed_out` (reported as unmeasured or stale, never as sign-out, and never retiring cache).
- **Claude safety check**: Before delegating Claude refresh, `src/lib/running-processes.ts` must confirm no Claude Code process is running, since Claude Code owns that session's refresh. If the process table cannot be listed, stay read-only. The check and spawn are not atomic - the check only narrows the common repeated `--tui` versus live-session collision; together with never signaling the delegate it is strictly safer than force-killing without adding a failure mode. Contract: [README Delegated credential refresh](../../README.md#delegated-credential-refresh).
- **Approved delegates**: Only commands whose rotation behavior is empirically established from the vendor CLI are permitted:
  - Claude: `claude doctor`
  - Grok: `grok models`
  - Codex: `app-server` JSON-RPC probe

  All other providers (Cursor, Copilot, Kimi, Z.AI, Alibaba, OpenCode Go, Antigravity, Command Code, MiniMax, MiMo, DeepSeek, OpenRouter, ElevenLabs, Devin, Muse, Higgsfield) remain strictly read-only.

- **Option gating**: Delegated refresh is gated by `ProviderOptions.refreshCredentials`. `--no-credential-refresh` disables it; the `auth` command always passes `false`. Tests must specify it explicitly to prevent accidental CLI spawning.

---

## Test & Mocking Discipline

- **Synthetic credentials**: All tests must use synthetic credentials and fixtures located in `test/fixtures/`. Never use real secrets or developer tokens.
- **Mock all boundaries**: Mock Keychain (`security`), Windows Credential Manager (`CredReadW`), process table (`ps`), and remote HTTP requests.
- **No live network or execution**: Tests and CLI runs during validation must never contact live provider endpoints or execute real credential refresh commands.
