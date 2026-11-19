---
name: descope-byos-builder
description: Use when building React "Bring Your Own Screen" (BYOS) custom UI on top of a Descope flow — takes exported flow JSONs, extracts the real interaction IDs and outputs, generates BYOS components that match hosted parity, and avoids the rediscovery-the-hard-way failure modes (silent form rejection, shared screen-name collisions, anonymous-session stickiness, nested-form hydration errors, wrong form keys, dead-end buttons, missing OAuth provider field).
---

# Descope BYOS Builder

Translate **Descope flow JSON exports** into working React BYOS screens that call `state.next(interactionId, form)`. The failures below are recorded from real BYOS sessions — every one cost 15–60 minutes the first time.

## When to Use

- Building custom UI over a Descope flow while keeping Descope's flow engine (no client-side JWT parsing, full flow logic intact)
- Modifying an existing BYOS implementation after the underlying flow changed in the Descope console
- Debugging "flow completes but session stays wrong" / "button does nothing" / "session is anonymous" / "passkey ceremony aborts" symptoms
- Auditing whether an existing BYOS matches hosted-screen parity
- Adding post-auth promotion subflows (e.g. `add-passkeys`) that run after `logged-in`

**Don't use for:** flows that fully work with the hosted `<Descope flowId=... />` widget (BYOS is a tradeoff — you give up flow edits propagating without code changes).

## The Iron Rule

**Ground every BYOS component in the exported flow JSON.** Do not guess interaction IDs, output key names, or screen names. Every failure in the catalog starts with someone making up a value that looked reasonable.

## Inputs Required (Ask the User First)

This skill cannot fetch flows from the Descope console — the agent has no console access. **Before doing any work, ask the user to provide:**

1. **Flow JSON files** — exported from Descope console for the main flow AND every subflow it invokes (LoadSubflow `arguments.flowId`), including post-auth promotion subflows (e.g. `add-passkeys`). Accept either file paths or pasted JSON.
2. **Project ID** + **base URL** (if not already configured) — needed for the `AuthProvider` / SDK init.
3. **Mount point** in the React app — file/component where the BYOS entry point should render.
4. **Existing BYOS code** (if modifying) — paths to current screen components and screen map.

If the user only provides the main flow JSON, **stop and ask for subflows** before generating components — missing subflow JSONs is the #1 cause of `[byos] no handler for screen "..."` runtime errors.

## Workflow

1. **Collect flow JSONs from the user.** Agent cannot reach the Descope console — user must export and paste/path them in. Need the **main** flow AND every subflow it invokes (LoadSubflow actions with `arguments.flowId`). This includes **post-auth promotion subflows** that run AFTER a `logged-in` action (e.g. `add-passkeys`) — easy to miss because the user is already authenticated by then. If only the main flow was provided, **scan it for `LoadSubflow` actions and ask the user to export each one** before proceeding. Missing subflow JSONs → undiscovered screens → `[byos] no handler for screen …` at runtime.

2. **Parse with `parse-flow.mjs`** (in this directory). Run `node parse-flow.mjs <path/to/flow.json>` — it prints every screen task with `screenName`, `allInputKeys`, `contextKeys`, next-rules (interactionId → taskId), UI node summaries (input `name` attrs, button labels), and subflow invocations.

3. **Build the screen-name map.** One React component per **unique screen name across all flows**. Watch for collisions — multiple tasks often share the name (e.g., "Welcome Screen" used for email-entry AND password-entry). When collisions exist, write a **router component** that dispatches based on `state.context.form.*` heuristics (see Gotchas → Screen name collisions).

4. **Write each component.** Every BYOS screen does the same four things:
   - Read context for display: `state.context.sentTo.maskedEmail`, `state.context.form.email`, etc.
   - Collect inputs into `form` (via `setForm({ ...form, key: value })`)
   - Fire `state.next(interactionId, payload)` on button click
   - Render `state.error?.text` when Descope reports errors

5. **Wire the flow.** The Descope React SDK provides `<Descope flowId="..." onScreenUpdate={handler} />` from `@descope/react-sdk` as the BYOS entry point — `onScreenUpdate` receives `(screenName, state, next)` and you dispatch to the matching screen component. A common pattern is to build a thin `FlowOrByos` wrapper that takes a `byosScreens` map and dispatches internally, but `FlowOrByos` is not an SDK export — you build it. Mount one instance at the entry point. On `onSuccess`, invalidate any auth-state caches (see Gotchas → Session stickiness).

6. **Verify end-to-end.** Walk every user journey the flow supports. Any screen that hits `[byos] no handler for screen "..."` in the console is missing from your map.

## Critical Rules

> **Note:** Several rules below (nested `<form>` tag behavior, WebAuthn ceremony ownership, `ctxKey` prefill, `componentsConditions` field name, E.164 silent rejection) are empirically derived from real BYOS sessions and are not explicitly documented in Descope's official docs — but have been validated in production and verified against flow JSON structure.

- **Form keys match the input node's `name` prop**, NOT `allInputKeys` or `inputsMetadata.key`. Task 40's Set Password input has `name="newPassword"` but `allInputKeys: ["newPassword_noPolicyOverrides"]`. Submit with `{ newPassword: "..." }`.
- **Send only the current screen's outputs** in `state.next` payloads. Spreading the full accumulated form across subflow boundaries can pollute context and cause silent failures.
- **Never nest `<form>` tags.** Descope's web component wraps children in a `<form>`. Use `<div>` + `onClick` + `onKeyDown={makeEnterHandler(submit)}`.
- **OAuth buttons must set `provider`** in the payload (`{ provider: 'google' }`), not only the interaction ID.
- **Phone numbers need E.164 format.** Non-E.164 gets silently rejected by the SMS connector — the flow completes but no session.
- **Invalidate auth caches on `onSuccess`.** Session upgrades (anonymous → verified) can reuse the same `sub`, so userId-keyed caches never auto-refresh.
- **Read `componentsConditions`** from screen JSON to mirror hide/show rules (e.g., hide "Sign in with code" when `unauthUser.verifiedPhone` is false).
- **WebAuthn flows: SDK runs the ceremony.** When an interaction routes to a webauthn action task (`webauthn-update-user-start/finish`, `Sign Up or In / Passkeys`), just fire `state.next(interactionId)`. **Never** call `navigator.credentials.create/get` from BYOS. **Never** import `@simplewebauthn/browser`, `startAuthentication`, `startRegistration`, or any WebAuthn helper library — the Descope SDK already does both ceremony halves. SDK observes the action on `onScreenUpdate` and runs the ceremony itself; cancel/error surfaces as `state.error.text`.
- **Read input `ctxKey` for prefill.** When an input node has `props.ctxKey="someKey"`, seed `form[name]` from `state.context[someKey]` on first render via `useEffect` keyed on the context value (only set if local field is empty).
- **Mirror `Device Not Supported` branches.** WebAuthn flows commonly branch on `deviceInfo.webAuthnSupport`. The unsupported branch is a real screen task — give it a BYOS component, otherwise hosted widget renders mid-promotion.

## Heuristics for Shared Screen Names

When two tasks share a screen name, you **cannot guess** a disambiguation signal. You must trace each path and build a "form field accumulation" table.

**The process (non-negotiable — skipping this produces silent bugs):**

1. For each task that uses the colliding screen name, trace backwards through `next.rules` until you hit the parent flow's entry point.
2. For each path, list every screen task along the way and its `allInputKeys` — those are the form fields the user writes into on that path.
3. Find a form field that is populated on exactly one path.
4. Use `Boolean(state?.context?.form?.<that field>)` as the heuristic.

**Common mistake:** picking a field that's populated on **both** paths because you didn't trace both paths fully.

> **Examples below are from one specific flow set — your task IDs, screen names, and subflow names will differ. They illustrate the method; always run `parse-flow.mjs` on your own flows.**
>
> Example: for "Verify OTP" shared between `sign-in-sms-otp` and `progressive-profile-sms`, `form.phone` looks attractive — but BOTH flows collect phone in a Phone-input screen before reaching Verify OTP. Pick `form.password` instead: the sign-in-sms-otp path is entered from the parent flow's password screen which writes `form.password`; the progressive-profile-sms path is entered post-magic-link where no password was ever typed.

**Reference heuristics (example from the flow set this skill was born from — not universal):**

| Collision | Path A collects before this screen | Path B collects before this screen | Signal |
|-----------|------------------------------------|------------------------------------|--------|
| "Welcome Screen" (email-entry vs password-entry) | — | `email` | `state.context.form.email` |
| "Verify OTP" (sign-in-sms-otp vs progressive-profile-sms) | `email`, `password`, `phone` | `email`, `phone` | `state.context.form.password` (NOT `phone` — both collect it!) |

Three-way collision example (Magic Link Sent across main and two subflow variants):

| Path | Collects before this screen | |
|------|----------------------------|---|
| Main flow | `email` | no password |
| Subflow new-user | `email`, `password`, `fullName` | password + fullName |
| Subflow existing-user | `email`, `password` | password, no fullName |

Predicate: `supportsChooseOther = !hasPassword || hasFullName`.

Document the chosen heuristic at the top of the router component with the full trace. If the Descope console could rename one screen, ask — unique names beat heuristics forever.

**Real success case:** Two `User Information` tasks (verify-email-magic-link existing-user vs new-user branches) were renamed in console to `User Information - Unverified - Email Only` and `User Information - Unverified - Email and Name`. Heuristic was possible (presence of `fullName` output); rename was cheaper, clearer, and survives flow edits. **Default toward rename.**

## Gotchas Reference

Full failure catalog (problem → symptom → fix): **see `references/gotchas.md`**. Before blaming BYOS code for a silent failure, scan that file — most "doesn't work" symptoms match a known gotcha.

## Verification

End-to-end test each user journey the flow supports:

- Flow JSON says the main flow starts at `task N` and ends at `task M` with `action=logged-in`?
- Every screen task in the flow has either a BYOS component OR a conscious "fallback to hosted" decision?
- `onSuccess` fires and the app reaches the expected authenticated state (not stuck anonymous)?
- `onError` fires and surfaces the Descope error message (not silent)?
- Post-auth promotion subflows (passkey promotion, etc.) walked end-to-end including the `Device Not Supported` branch?
- WebAuthn screens fire `state.next(interaction)` only — no `navigator.credentials.*` calls in BYOS code?

Console should show **no** `[byos] no handler for screen "..."` warnings during a full journey walk.

## Parser

`parse-flow.mjs` (this dir) — Node script. Input: flow JSON path(s). Output: a summary table per flow showing screen tasks, their inputs, their exit interactions, their UI node names, and subflow loaders. Run it, paste the output into your screen-map comment header, and you have the source of truth for every constant the BYOS components need.

## Red Flags

If you find yourself:

- Hardcoding an interaction ID you didn't see in the flow JSON — **stop, parse first**
- Spreading `{ ...form }` into `state.next` across a subflow boundary — **send only the outputs**
- Adding the same button to every "Verify OTP" variant without checking each flow's rules — **gate by context**
- Writing a `<form>` tag inside your BYOS component — **use `<div>`**
- Calling `navigate()` in `onSuccess` without invalidating auth caches — **call invalidate first**
- Calling `navigator.credentials.create/get` from a BYOS click handler — **the SDK does it; just fire the interaction**
- Importing `@simplewebauthn/browser` or any WebAuthn helper — **same trap, third-party-lib variant; SDK does it**
- Skipping subflow export because "the user is already logged in by then" — **post-auth promotion subflows render real screens**

All of these mean: pause, re-read `references/gotchas.md`, verify against the flow JSON.

## References

- `references/byos-component-patterns.md` — positive code patterns: core wiring (`onScreenUpdate` → `ByosState`), screen router, screen skeleton, and complete examples for email, OTP, phone, OAuth, collision router, and ctxKey prefill. Start here when bootstrapping.
- `references/gotchas.md` — failure catalog: 19 real BYOS failure modes, each with symptom → root cause → fix. Also contains a pre-ship checklist.
- `parse-flow.mjs` — Node parser: `node parse-flow.mjs <flow.json> [more.json ...]`. Prints screen tasks, real form-key `name` props, interaction IDs, subflow loaders, and collision warnings. Run before writing any component.
