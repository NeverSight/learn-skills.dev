---
name: abto
description: Map frontend and backend repository boundaries, inventory LLM API call sites for approval, install and wire the minimum ABTO Browser, App, or Server SDKs, preserve device_id and trace correlation, recommend opt-in system or custom events, and verify the resulting ABTO integration. Use for ABTO setup, updates, troubleshooting, Gateway calling, event collection, key placement, or end-to-end integration checks across browser JavaScript, Node.js, Python, Flutter/Dart, Android/Kotlin, and iOS/macOS.
---

# ABTO

Use this as the single public ABTO integration skill.
Map the application before editing, obtain approval for exact model-call targets, wire only the smallest required core, and leave every event opt-in.
Deliver the smallest integration that unlocks the customer's selected ABTO outcomes while preserving existing product behavior.
When multiple designs provide the same ABTO value, choose the one with fewer changed files, dependencies, endpoints, and new abstractions.
If a change cannot be tied to an approved customer outcome, do not make it.

## Load the relevant references

1. Always read [SDK selection](references/sdk-selection.md) and [Discovery and reporting](references/discovery-and-reporting.md).
2. When an ABTO-specific term, behavior, API, supported field, version, event rule, Dashboard meaning, or troubleshooting step is missing or uncertain, consult the official [ABTO Docs](https://docs.abto.app/) before proposing code.
   Follow the documentation, installed-version, and conflict procedure in [SDK selection](references/sdk-selection.md) instead of guessing or generating compatibility glue.
3. Read only the implementation reference for each confirmed runtime:
   - Browser JavaScript: [Browser JavaScript](references/browser-javascript.md)
   - Node.js or Python backend: [Server](references/server.md)
   - Flutter/Dart, Android/Kotlin, or iOS/macOS: [Mobile](references/mobile.md)
4. Read [SDK defect handling](references/sdk-defect-handling.md) only when an installed public SDK appears to behave contrary to its released contract.
5. Read [Verification](references/verification.md) before declaring the integration complete.
6. Read [Skill installation](references/skill-installation.md) only when installing, updating, removing, or troubleshooting this agent skill itself.

## Integration workflow

### 1. Map and confirm the repositories

- Read repository instructions, Git roots, workspace manifests, lockfiles, deployment entry points, application entry points, existing telemetry, and environment-variable conventions.
- Distinguish frontend, backend, worker, and native runtimes even when they share a monorepo.
- When the product uses split repositories, inspect every available repository that participates in the client-to-model path.
  If a required counterpart is unavailable, report the evidence and ask for its path or access instead of guessing.
- Check for existing ABTO dependencies, initialization, event schemas, and request context before proposing another integration.
- Present the repository map under `## 1. Core · LLM API wiring`, ask the user to confirm it, then stop before editing any file.
- Preserve package managers, framework lifecycles, formatting, test commands, and unrelated user changes.

### 2. Inventory every LLM call and obtain approval

- After the repository map is confirmed, inspect every confirmed runtime using the inventory in [Discovery and reporting](references/discovery-and-reporting.md).
- Account for direct SDK calls, raw provider HTTP calls, shared wrappers, framework adapters, API routes, serverless functions, background workers, queues, cron jobs, batch jobs, and streaming paths.
- Trace each provider call back to its user-facing capability and, when one exists, its client request trigger.
- Present every candidate with an ID, capability, repository/runtime, exact call site, API surface, device path, proposed dot-separated `featureId`, compatibility, and intended action.
- Mark only confirmed OpenAI Chat Completions calls as automatically wireable.
  Inventory OpenAI Responses, embeddings, images, audio, native Anthropic or Gemini calls, and ambiguous framework abstractions, but do not rewrite them into a different API or invent an adapter.
- Propose a `featureId` only when existing product or route language makes the capability unambiguous.
  Otherwise mark the candidate ambiguous and ask what capability and stable key the user wants.
- Ask one batch question that lets the user approve all eligible IDs or name inclusions and exclusions.
  Stop before adding dependencies, initialization, context, or feature IDs.

### 3. Install and wire the approved core

- Treat approval of the inventory as authorization only for the selected SDK dependencies, minimal initialization, and the approved LLM call sites and `featureId` values.
- Use [SDK selection](references/sdk-selection.md) as the public availability source of truth.
  Never import a Server SDK into a client bundle or install multiple SDKs for the same runtime responsibility.
- Prefer an existing configuration or provider-client module.
  Create one small ABTO initialization module only when no suitable module exists; do not create demonstrations, sample endpoints, generic wrappers, or future-facing abstractions.
- For a new Browser integration, use the Browser reference's minimal initialization and confirm it emits no events on its own.
  Never add broad automatic DOM collection for a new integration.
  Preserve and disclose any existing automatic event collection behavior instead of changing live collection behavior silently.
- Use the Event SDK identity and trace helpers without emitting events.
  Starting a trace or reading trace headers does not authorize `submitPrompt`, `markResponseRendered`, `captureResponseInteraction`, or a custom `capture` call.
- Pass the same client `device_id` and trace through the existing request path, validate client-supplied context with the application's existing validation, and apply it to the approved Calling context.
- For server-only work, reuse a clearly established stable product identifier.
  If none exists, ask the user instead of minting a separate server identity or using a per-request random value.
- Keep Event Keys in public client configuration and Calling/provider keys in server-only secret storage.
  Never invent, print, or commit credentials.
- Preserve the Calling SDK's resolved direct-fallback behavior unless the user approves an availability-policy change.
  Inventory and report every Gateway and direct provider path, including which path lacks ABTO telemetry and `request_id`.
- Preserve the customer's native OpenAI `maxRetries` or `max_retries` setting and SDK default.
  Do not add a separate fallback attempt counter or change retry policy merely to wire ABTO.
- Preserve every other native OpenAI client option unless the installed Calling SDK explicitly documents it as ABTO-owned routing, credential, or transport state.
  Report each composed, overridden, or rejected option; treat an undocumented silent discard as an SDK defect instead of deleting the customer's configuration.
- Do not create an event schema, event call, response-ID bridge, or unrelated product-code change during core wiring.
- If an installed SDK appears to violate its documented contract, pause only the affected path and follow [SDK defect handling](references/sdk-defect-handling.md).
  Prefer the smallest compatible public SDK update that already fixes the defect, apply it with the customer's existing package manager and lockfile, re-verify the original path, and continue wiring when it passes.
  Do not patch dependency directories or generate a wrapper to hide the suspected defect.

### 4. Discover events and obtain selection

- Verify the core first, then inspect every confirmed client runtime for meaningful user actions and product outcomes around the approved capabilities.
- Find broadly, deduplicate aggressively, and present evidence-backed system and custom event candidates using [Discovery and reporting](references/discovery-and-reporting.md).
- Offer only explicit trace-helper or custom-capture candidates; do not offer automatic DOM collection.
  The customer must select the exact event and the product trigger where its direct SDK call will be added.
  Preserve and disclose any existing automatic collection behavior.
- Treat no events as the default.
  Ask one batch question that allows multiple candidate IDs or `none`, then stop before editing.
- Add only the selected system-event calls at their approved triggers.
- For response-interaction helpers, use only a value exposed by the installed SDK's canonical interaction type.
  Propose a custom event when the product action has no exact canonical value; never pass an invented string to a system-event helper.
- Create or extend the product event schema only when at least one custom event is selected, and add only the selected `capture` calls.
- Use the Gateway `x-abto-request-id` only through a currently supported selected event path.
  Do not claim that an arbitrary custom event is request-correlated when the SDK does not establish that link.
- If the user selects no events, retain the core integration with no event-related code or schema file.
- If a selected Event path exposes an SDK defect, follow [SDK defect handling](references/sdk-defect-handling.md) and retry it on the smallest compatible fixed public version before marking that Event ID `blocked-sdk-defect`.
  Do not silently substitute a custom event or different trigger.

### 5. Verify and report

- Follow [Verification](references/verification.md) for each changed runtime and for the final change ledger.
- Run one bounded live event or model call only when credentials, target environment, and any paid call are explicitly authorized.
- At every confirmation checkpoint and in the final response, use exactly these three sections:
  - `## 1. Core · LLM API wiring`
  - `## 2. Event candidates · selection result`
  - `## 3. Final integration flow`
- Mark later sections as pending at an earlier checkpoint instead of omitting them.
- In the final section, separate Core and Event changes and draw a Mermaid diagram from the actual repositories and code paths.
- Report every discovered LLM candidate as wired, already wired, incompatible, ambiguous, user-excluded, or blocked-sdk-defect.
  Never claim full coverage while an unexplained candidate remains.
- Do not mark `blocked-sdk-defect` as wired merely because an SDK source fix merged.
  Require a fixed public artifact, customer lockfile update, and successful re-verification of the original path.
