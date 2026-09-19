---
name: ae-migrate-tracking-code
description: "Migrate existing third-party SDK tracking code (Firebase, Amplitude, Sensors Data, Mixpanel, GA4) to the AE SDK (数数 / ThinkingAI / Agentic Engine / AE SDK) — switch (replace) or add alongside existing tracking (dual-write). Trigger words: 埋点迁移、埋点切换、第三方埋点迁移、第三方埋点切换、迁移埋点到数数、把 xx SDK 切换到数数、把已有埋点用数数实现一遍、用数数替换 xx SDK、集成数数并参考已有 xx SDK 埋点、Firebase 迁移、Amplitude 迁移、Mixpanel 迁移、神策迁移、Sensors Data 迁移、GA4 迁移、gtag 迁移、双写、tracking migration、migrate Firebase/Amplitude/Mixpanel/Sensors Data/GA4 to AE、switch xx SDK to ThinkingAI、replace xx SDK with AE、replace logEvent with track、re-implement existing tracking with ThinkingAI、add AE tracking alongside existing analytics、dual-write. Provider-agnostic core with per-provider adapters; reuses ae-generate-tracking-plan and ae-generate-tracking-code."
---

# ae-migrate-tracking-code

> **Conversation language**: This skill document is in English, but **all output to the user MUST be in the user's input language**.
> English input → English reply; Chinese input → Chinese reply; Japanese input → Japanese reply.
> If uncertain, default to English.
> This applies to all output: section titles, phase names, prompts, code comments, etc.
> **⚠️ CRITICAL: Many provider adapter docs contain Chinese glossary notes. When reading them to answer an English/Japanese user, translate headings and comments to the user's language.**
> Do NOT copy Chinese text verbatim from this document into English/Japanese replies.

## Terminology Glossary

| 中文 | English | Notes |
|------|---------|-------|
| 埋点迁移 | Tracking Migration | Convert existing third-party SDK tracking calls to AE SDK |
| 源 SDK | Source SDK / Provider | The third-party SDK already in the project (Firebase, Amplitude, ...) |
| 调用点 | Call Site | A source-SDK invocation (`logEvent` / `setUserId` / `setUserProperty` / Identify) |
| 归一化中间表示 | IR (Intermediate Representation) | Provider-neutral dump of extracted call sites |
| 映射 | Mapping | Source event/property → AE event/property translation |
| 切换 | Switch | Replace source calls with AE `track()` and remove source SDK |
| 双写 / 新增 | Add / Dual-write | Keep source SDK and add AE `track()` alongside |
| 依赖标识 | Dependency Identifier | Package/module name used to remove the source SDK in switch mode |
| 自动采集事件 | Auto-track Event | Events the source SDK collects automatically (e.g. `session_start`) |
| 公共属性 | Super Property | Property attached to every event automatically. ⚠️ The correct Chinese AE term is "公共属性" or "公共事件属性". Never translate "Super Property" as "超级属性" — that is NOT a valid AE term. |
| 用户属性 | User Property | Property set on the user profile |
| 用户体系 | User Identity System | distinct_id / account_id strategy in AE |

## When to Trigger

Trigger when user says: "migrate Firebase tracking to AE / replace Amplitude with ThinkingAI / my project already has Firebase/Amplitude tracking, switch it to AE SDK / add AE tracking alongside existing analytics" etc. — e.g. 把当前工程里的 xx SDK 切换到数数、把已有埋点用数数实现一遍、用数数替换 xx SDK、集成数数并参考已有的 xx SDK 埋点.

The **target AE SDK** may be referred to by any of: 数数 / 数数 SDK / ThinkingAI / ThinkingAI SDK / Agentic Engine / Agentic Engine SDK / AE / AE SDK — they are one SDK. The trigger signal is "an **existing third-party source SDK** + 迁移/切换/替换/实现一遍", or "集成/接入数数 **并参考已有的 xx SDK 埋点**". A bare 接入数数 SDK / 加数数埋点 with no source SDK is greenfield — it belongs to `ae-generate-tracking-code`, not this skill.

**Scope**: this skill is codebase-only — it scans existing third-party tracking calls (Phase 0/1). If there is no source code with third-party tracking (only product docs / descriptions), do NOT use this skill; route to `ae-generate-tracking-plan` + `ae-generate-tracking-code` instead. Historical data import into AE is offline data-migration work, **out of scope** — this skill only switches the live client/server SDK, preserving user IDs and event/property names so new data joins the imported data.

This skill orchestrates the migration end-to-end but **does not duplicate** the two existing skills:

- Plan generation/upload → hand off to `ae-generate-tracking-plan` (codebase path).
- AE SDK code insertion → hand off to `ae-generate-tracking-code` (insert mode), with insertion sites supplied from the migration mapping instead of grep-discovered business triggers.

## Provider Registry (extensible)

The core is provider-agnostic. Each third-party platform is one adapter file. **To support a new provider, add one adapter under `references/providers/` and one row below — do not modify this SKILL.md.**

| Provider | Adapter | Platforms covered | Detect pattern (summary) |
|---|---|---|---|
| Firebase Analytics | `references/providers/firebase.md` | Web v8/v9, Android, iOS, Flutter, React Native, Unity, C++ | `firebase/analytics`, `firebase.analytics()`, `FirebaseAnalytics`, `FIRAnalytics`, `Analytics.logEvent` (iOS Swift), `FirebaseAnalytics.instance` |
| Amplitude | `references/providers/amplitude.md` | Web legacy (`amplitude-js`), Browser 2.x, Node, Python, Go, Java, Android, iOS, React Native, Flutter, Unity | `amplitude-js`, `@amplitude/analytics-browser`, `@amplitude/analytics-node`, `amplitude.init`, `amplitude.getInstance()`, `amplitude.logEvent`, `amplitude.track`, `Identify`, server imports (`from amplitude import`, `analytics-go`, `com.amplitude:java-sdk`) |
| Sensors Data (神策) | `references/providers/sensors-data.md` | Web, Android, iOS, Harmony, macOS/tvOS, C++, React Native, Flutter, Unity, Unreal, Cocos2d-x, mini-programs (WeChat/other), QuickApp, APICloud, uni-app, Weex, Egret, LayaAir + server SDKs (Java/Python/Go/Node/PHP/Ruby/C/.NET/Lua) | `sensorsdata.min.js`, `sensors.init`, `sensors.track`, `SensorsDataAPI`, `SensorsAnalyticsSDK`, `profileSet`, `setProfile` (legacy), server `sa-sdk-*` (Python/Go/Node/PHP/Ruby/C/.NET/Lua) |
| Mixpanel | `references/providers/mixpanel.md` | JavaScript, Node, Python, Go, Java, Ruby, PHP, Android, iOS, Swift, React Native, Flutter, Unity | `mixpanel-browser`, `mixpanel.init`, `mixpanel.track`, `mixpanel.identify`, `mixpanel.people`, `MixpanelAPI`, `mixpanel.NewApiClient` (Go), `Mixpanel::Tracker` (Ruby), `Mixpanel::getInstance` (PHP), `mp.track` / `people_set` (Python) |
| Google Analytics 4 | `references/providers/ga4.md` | Web (gtag.js / dataLayer), Measurement Protocol (server) | `gtag('event'`, `gtag('config'`, `gtag('set'`, `dataLayer` (GA4 only when `gtag(`/`G-` also present), `G-XXXXXXX`, Measurement Protocol `mp/collect` |

Adapter contract (required fields per adapter) is defined in `references/providers/README.md`.

**Supported scope**: only the providers/platforms listed above (and the per-platform tables in each adapter's Recognition section) are supported. Anything not listed is out of scope and not supported by this skill — do not fabricate a mapping for unlisted platforms.

---

## Phase 0 — Detect source SDK and version

1. Locate the project and its package/dependency manifest (`package.json`, `build.gradle`, `Podfile`, `pubspec.yaml`, `*.csproj`, ...) plus source imports.
2. Match against the registry above. Read the matching adapter's **Recognition** section to confirm the provider and pin the version variant:
   - Firebase: v8 namespaced vs v9 modular (web), plus Android/iOS/Flutter native forms.
   - Amplitude: legacy (`getInstance().logEvent`) vs SDK 2.x (`amplitude.track` / `@amplitude/analytics-browser`).
3. If multiple providers are present, list them and ask which to migrate first (one provider per run keeps mapping clean). **Exception — GA4 and Firebase Analytics are the same data stream**: GA4 is Firebase's web layer (one measurement ID is both a GA4 property and a Firebase project). If `gtag(...)` and `logEvent(...)` coexist in one project, they are **not two providers** — merge them into a single migration run: one scan, one `draft.json` / `mapping.json`, one dedup pass over the shared event / property / user-id names. Never produce two drafts for one Google data stream.
4. If no registry match but tracking code exists → show the found calls, ask the user for the provider name, and (per `references/providers/README.md`) collect a minimal adapter from the user-provided docs/snippet before continuing.

## Phase 1 — Extract call sites into IR

Scan the project for four call categories, using the adapter's **Recognition** patterns:

1. **Event** calls: `logEvent(...)` / `track(...)` and their params/properties.
2. **Identity** calls: `setUserId(...)` / `identify(...)` / `login(...)`.
3. **User property** calls: `setUserProperty(...)` / `setUserProperties(...)` / `Identify` operations.
4. **Super property** calls (common event properties): `register(...)` / `registerSuperProperties(...)` (Mixpanel, Sensors Data) / `setDefaultEventParameters(...)` (Firebase). Record them as `kind: super_property` with the full `props` map — do not misread them as user properties (see `mapping-framework.md` §6). Amplitude and GA4 have no such API.

Record each site as `file:line`, call kind, event/param values (literals, or variable names to resolve by reading the surrounding code). Write the normalized dump to `.ae-cli/migration/scan.json` following `references/ir.md`.

**Wrapper-layer resolution (reverse call-graph tracing)** — real projects almost never call the source SDK directly at every business event; they wrap it in an analytics helper (`trackEvent(name, props)` → `mixpanel.track(name, props)`). A naive grep sees only the wrapper's single SDK call (event name = parameter → would be `resolved:false`) and misses every real business event. So when an SDK call's event name is a **function parameter** (a runtime variable flowing from an enclosing function's argument), do **not** immediately record `resolved:false`:

- Identify the enclosing function `F` — it is an **analytics wrapper** only when `F`'s sole role is forwarding that parameter into the SDK call. If the event name comes from local logic/expressions rather than a parameter, it is NOT a wrapper — record the site as `resolved:false` as usual.
- Grep for every caller of `F`. Resolve each caller with a static event name into a normal call site: `kind` is inferred from the SDK call `F` delegates to (event / identity / user_property), `event_name` from the caller's literal or constant argument, `source_call` = the caller's invocation line, `file` = the caller's file, and `via_wrapper` = `F`'s name.
- Callers with a dynamic event name stay `resolved:false`. If no callers are found (an exported wrapper used externally, or dynamic dispatch), fall back to recording the wrapper's own SDK call as a single `resolved:false` site.
- Record `F` itself in scan.json's top-level `wrappers` array (see `references/ir.md`) — it is the pivot for tracing, not a migration target.

**Auto-track note**: source SDK auto-collected events (e.g. Firebase `session_start`, `first_open`, `screen_view`) are not call sites. Handle them per the adapter's **Auto-track decision** table in Phase 2, not here.

## Phase 2 — Map to AE (write draft.json + mapping.json)

1. Read `references/mapping-framework.md` (generic algorithm) + the provider adapter (differences).
2. For each extracted event call: map to an AE event (snake_case name, or **verbatim** when forward compatibility is required — `mapping-framework.md` §1; `display_name` in the user's language), map each param to an AE property with a type, and apply naming constraints from the adapter (reserved prefixes, special characters, length caps).
3. Apply dedup + promotion rules: same property on 3+ events → common event property (super property); preset `#` properties never become super properties. Explicit super-property call sites (`register` / `setDefaultEventParameters`) also land in `draft.json`'s `common_event_properties` pool — see `mapping-framework.md` §6.
4. Map identity → AE `login(accountId)` (account_id_source `user_account`); plus visitor-id continuity (`setDistinctId` / `identify`, init-time) when forward compatibility with imported historical data is in scope — see `mapping-framework.md` §4. User property ops → AE `user_set` / `user_setOnce` / `user_add` / `user_append` / `user_unset` per the adapter's mapping table. Super property calls → AE `setSuperProperties({...})` (static common event property), per `mapping-framework.md` §6.
5. Decide each event's `platform` (client / server) from where the call site lives (app code → client; backend → server).
6. Ask the user to confirm the **migration mode** (see Modes below) and whether **historical source-platform data** has been (or will be) imported into AE **offline** — drives forward-compatible naming per `mapping-framework.md` §1 and visitor-id continuity per §4. The import itself is offline data-migration work, out of scope; this skill only switches the live SDK — then:
   - Write `.ae-cli/migration/mapping.json` (source site → AE event + mode decision, schema in `references/ir.md`).
   - Write `.ae-cli/draft.json` in the AE plan schema (same schema `ae-generate-tracking-plan` produces) so the plan skill can consume it directly.

Show the mapping summary table and get user `ok` before proceeding.

## Phase 3 — Generate and upload the tracking plan

Hand off to `ae-generate-tracking-plan` using the codebase/draft already produced:

1. `ae-cli tracking plan draft --in .ae-cli/draft.json --out .ae-cli/draft.xlsx`
2. `ae-cli tracking plan validate --in .ae-cli/draft.json --fix`
3. Resolve AE host/login/projectId per the plan skill, then `ae-cli tracking plan upload ...` (ask the user before uploading; append vs replace per that skill's conflict detection).

## Phase 4 — Insert AE SDK code (switch or add)

Hand off to `ae-generate-tracking-code` (insert mode), but **insertion sites come from `.ae-cli/migration/mapping.json`, not from grep business-trigger discovery**:

- Client/server platform + language are already in `draft.json` meta; resolve APP_ID / SERVER_URL as that skill does.
- For each mapped AE event, the insertion point is the original call site recorded in mapping.json.

**Mode `switch`** (replace) — **high-risk, confirm before deleting**:
- Before any deletion, explicitly list what will be removed (the source call sites and the source SDK dependency from the adapter's **Dependency identifiers**) and get the user's confirmation to delete.
- Replace the source `logEvent`/`track` call with the AE `track(...)` call at the same site; remove now-unused source imports.
- **Inline event names that came from a module constant**: emit the literal snake_case name in the AE `track(...)` call (it must match the `// @tracking <event_name>` marker). **Before deleting the constant definition, grep the whole project for its name** — a module constant is often imported by multiple files, fed to a server-side report, or asserted in tests. Only remove it when the migrated call sites are its sole references (then it is dead code); otherwise keep it. Do not keep a constant that only feeds the migrated call.
- Remove the source SDK dependency using the adapter's **Dependency identifiers** (e.g. `firebase/analytics`, `@amplitude/analytics-browser`).
- **Remove dead wrappers**: when every call site resolved through a wrapper is `replace`d, the wrapper function is dead code — delete it (and its now-unused source import). If the wrapper's file holds nothing else, remove the file. (`add` mode keeps the wrapper — it still feeds the source SDK — and adds the AE call at each business call site.)
- Convert identity/user-property calls to `login(...)` / user-property calls similarly; super-property calls → `setSuperProperties({...})` **in place at the original call site** (never hoisted — the source's `register` position encodes when the values become available, e.g. after login; see `mapping-framework.md` §6).

**Mode `add`** (dual-write):
- Keep the source call untouched; add the AE `track(...)` call immediately adjacent (before or after, matching surrounding style).
- **Keep the two SDKs independent — in both directions.** Dual-write means two independent writes, for **every provider / every SDK** (Firebase, Amplitude, Sensors Data, Mixpanel, GA4, …), not a source-guarded AE write:
  - The AE `track()` / `login()` / user-property / `setSuperProperties()` call must NOT be nested inside the source SDK's availability guard, early-return, or error path — e.g. after `if (!analytics) return`, behind `isSupported()`, or inside the source's `try/catch`. If the source call sits behind such a guard, lift the AE call out so it runs unconditionally.
  - Give **each SDK its own `try/catch`** around its write: a source-SDK failure (unavailable, `isSupported() === false`, or a thrown error) must never suppress the AE write, and an AE failure must never suppress (or crash) the source write.
  - The guard must cover the source SDK's **full failure surface, not a single exception type**. A pre-existing narrow catch (e.g. Python `except ValueError` for 400 validation, Java `catch (IllegalArgumentException)`) is **not** the independence guard — other failures (unconfigured API key → `RuntimeError`, network/timeout) still escape and crash before the AE write. Broaden the catch to all exceptions, run the AE write, then re-raise the source exception so the original status/error semantics (400/503) are unchanged.
  - Give **each SDK's init its own `try/catch`** too, so that one SDK being unloaded or disabled at load time (init throws / module missing) does not take down the other SDK. Both writes must keep working no matter which SDK is unloaded or disabled.
  - This applies to every `add` / `add_after` / `add_before` entry in mixed runs too.
- Keep the source SDK dependency; only add the AE SDK dependency.

**Async call sites** — a source call that is `await`ed (React Native / Flutter `await analytics().logEvent(...)`, some `await mixpanel.track(...)`) returns a Promise, but the AE client `track()` / `login()` / user-property / `setSuperProperties()` calls are synchronous:
- **`switch`**: drop the `await` on the replaced call — awaiting a synchronous AE call is a lint warning and changes nothing. If the source call sat inside a `try/catch` whose `catch` handled the source SDK's **Promise rejection** (network retry, offline fallback, error reporting), that rejection branch dies with the source SDK: remove the now-dead `catch` logic; if the `try` block then holds only the AE call, collapse the `try/catch` into the bare AE call (AE sync failures then follow the code skill's Code Style — loud in `switch`). Never wrap the AE call in a made-up `async`/`await` to keep the shapes matching.
- **`add`**: keep the source call's `await` and its `try/catch` exactly as-is, and place the AE call **outside** that block, un-`await`ed, in its own `try/catch` per the independence rule above.

Both modes follow the code skill's insert rules: SDK init from the wiki main doc (never guess imports), git-status pre-check, batched Edit with language-style check, `// @tracking <event_name>` comment prefix.

**User-property `append` / `unset`** (`ae_call` = `user_append` / `user_unset`): these two are not in the plan's `update_type` enum (only `user_set` / `user_setOnce` / `user_add` are), so they do not enter `draft.json` — in the draft their `update_type` is written `user_set` (placeholder). At code-insertion time, emit the AE SDK call directly per the mapping's `ae_call` (`user_append` → `userAppend`, `user_unset` → `userUnset`), reading the real method signature from the wiki main doc (never guess).

**⚠️ `add` mode overrides the code skill's "Do NOT add try/catch" Code Style.** That rule is a single-SDK rule (greenfield insert / `switch` after cut-over): with one SDK a loud failure is the point, so init/track failures must surface rather than be swallowed. Dual-write is the opposite — the "each SDK its own `try/catch`" rule above applies to the generated AE code too:
- The AE init must be guarded the same way (its own `try/catch` / availability check), so an AE-SDK load failure never throws at load time and never takes down the source SDK.
- Never emit a load-time SDK capture that becomes a permanently-`undefined` reference and throws on every call (e.g. `var ta = window.TA;` in a wrapper) — a missing AE SDK must be a per-call no-op, not a crash of business logic or the source write.
- `switch` mode does NOT get this override: after cut-over AE is the only SDK, so it follows the code skill's Code Style as-is (failures stay loud).

## Phase 5 — Verify

Reuse the code skill's validation flow:

1. `ae-cli auth status` / confirm active host; debug device add/select.
2. Trigger the migrated events and query `ae-cli tracking debug-data list`.
3. In `add` mode, verify AE data alongside the still-running source SDK; in `switch` mode, confirm the source SDK is fully removed and AE data flows.

## Modes

| Mode | Source SDK kept? | AE call placement | Dependency change |
|---|---|---|---|
| `switch` | removed | replaces source call | remove source dep, add AE dep |
| `add` | kept | added alongside | add AE dep only |

Ask the user once in Phase 2 which mode to use. **Default to `add` (dual-write): present `add` as the recommended option in the confirmation prompt.** Treat `switch` as the non-default, destructive choice — offer it only when the user has explicitly expressed wanting a full cut-over, and never mark it recommended.

**Staged / mixed runs**: `mode` is the run-level default, but each mapping entry carries its own `action` (`replace` vs `add_after`/`add_before`), and the per-entry `action` is authoritative. A `switch` run may still keep selected entries as `add_after` for a staged roll-out (e.g. cut over identity + sign-up now, keep `purchase` dual-writing while its data is validated). In that case: replaced files drop the source SDK, dual-write files keep it, and the source SDK dependency is removed **only** on a full cut-over (every entry `replace`). See `references/ir.md` §mapping.json and `mapping-framework.md` §8.

> **⚠️ `switch` is destructive (high-risk)**: it deletes source tracking calls, their imports, and the source SDK dependency. Never delete old code by default. Before deleting anything, explicitly tell the user what will be removed (call sites + dependencies) and get their confirmation; re-confirm again at Phase 4 immediately before deletion, even if `switch` was already chosen in Phase 2.

## Prohibitions

- Guessing AE SDK imports/package names — always read the wiki main doc via `ae-generate-tracking-code` (`references/sdk-index.md`).
- Modifying event/property names away from the AE plan (`snake_case`, registered names).
- Migrating source SDK auto-track events as manual `track()` calls — map them to AE auto-track switches or drop them per the adapter.
- Nesting the AE `track()` / `login()` / user-property calls inside the source SDK's availability guard, early-return, or `try/catch` in `add` mode, or leaving either SDK's init unguarded, or guarding the source write with a narrow exception-type catch that still lets a source failure crash before the AE write — for every provider, dual-write must stay two independent writes (each SDK its own `try/catch`, init included, covering the full failure surface), so one SDK failing or being unloaded never takes down the other.
- Skipping the mapping summary confirmation in Phase 2.
- Writing `user_append` / `user_unset` into `draft.json`'s `update_type` (the plan enum is `user_set` / `user_setOnce` / `user_add` only) — append/unset stay in `mapping.json` `ae_call` and are emitted directly at Phase 4.
- Translating "Super Property" as "超级属性" in any user-facing output.
- Writing source or AE code before the git-status pre-check (insert mode).
- Editing the provider adapters to add provider-specific logic into the core — new providers are new adapter files only.
- Deleting source tracking code or removing the source SDK dependency (`switch` mode) without explicitly warning the user and getting their confirmation immediately before deletion.

## Internal Reference

- `references/ir.md` — normalized IR schema (`scan.json` / `mapping.json`).
- `references/mapping-framework.md` — provider-agnostic mapping algorithm.
- `references/ae-preset-properties.md` — authoritative AE `#` preset-property list + system fields (only these `#` names ingest).
- `references/providers/README.md` — adapter contract + how to add a provider.
- `references/providers/firebase.md` — Firebase adapter.
- `references/providers/amplitude.md` — Amplitude adapter.
- `references/providers/sensors-data.md` — Sensors Data (神策) adapter.
- `references/providers/mixpanel.md` — Mixpanel adapter.
- `references/providers/ga4.md` — Google Analytics 4 (gtag.js / Measurement Protocol) adapter.
