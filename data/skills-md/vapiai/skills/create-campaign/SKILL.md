---
name: create-campaign
description: Create, schedule, duplicate, inspect, cancel, archive, and troubleshoot Vapi outbound Campaigns. Use for persistent multi-contact calling, CSV or API contact personalization, campaign concurrency, campaign webhooks, pre-dial eligibility, contact outcomes, or rerunning an audience. Do not use for a single call or a simple one-off /call batch.
license: MIT
compatibility: Internet access is recommended for current Vapi schema verification; VAPI_API_KEY is required for live campaign operations.
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Outbound Campaigns

Use Campaigns for a persistent outbound run whose contacts, lifecycle, and results must be managed together. Creating a campaign launches it immediately or schedules it; there is no draft or separate start action.

The current public API uses `/v2/campaign`. The unversioned `/campaign` endpoints are legacy and have different behavior. Use `/v2/campaign` for new integrations, and touch `/campaign` only when the user explicitly asks to maintain an existing legacy integration.

## Source and Safety Rules

- Verify live payloads against the current Vapi documentation MCP, [Campaigns documentation](https://docs.vapi.ai/outbound-campaigns/overview), or public API reference. Do not silently fall back from `/v2/campaign` to legacy `/campaign` behavior.
- Use a private API key only on a trusted server. Read it from `VAPI_API_KEY`; never print it, request it in chat, or put it in client-side code, examples, logs, or committed files.
- Treat phone numbers, names, contact variables, call records, transcripts, and recordings as sensitive. Report counts and redacted samples unless the user needs specific records.
- Never invent resource IDs, recipients, consent, schedules, time zones, campaign state, counters, or call outcomes. Resolve saved resources by exact ID or an unambiguous API result.
- Launching can place real, chargeable calls. Before a live create or duplicate, review the exact target, outbound number, audience count, timing, concurrency, and webhook behavior. Obtain confirmation unless the user's current instruction already unambiguously authorizes that exact launch.
- Do not make a legal determination. Tell the user to verify the consent, caller-identification, recording, opt-out, quiet-hours, and telemarketing requirements that apply to every recipient and destination. Use Vapi's [TCPA consent guidance](https://docs.vapi.ai/tcpa-consent) when relevant.
- A timeout or ambiguous response to `POST /v2/campaign` does not prove failure. Search for the intended campaign before retrying so the audience is not called twice.

## Procedure

1. Choose the API and execution mode.
   - Use `POST /call` and the `create-call` skill for one call or a simple one-off batch that does not need campaign-level lifecycle, reporting, cancellation, duplication, or webhooks.
   - Return a plan, CSV, payload, or implementation without calling Vapi when the user asks to draft, explain, review, or prepare.
   - Use live API operations only when the user asks to create, duplicate, cancel, or archive and `VAPI_API_KEY` is available.

2. Resolve the caller and outbound number.
   - Select exactly one saved `assistantId` or `squadId`. Do not use deprecated Workflows for a new campaign.
   - Resolve one outbound-capable `phoneNumberId`. Vapi Free Numbers cannot launch campaigns. The current `/v2/campaign` API does not support legacy `dialPlan` routing across multiple outbound numbers.
   - Inspect the assistant or squad before launch. Ensure its prompt, tools, variables, call-ending behavior, and published configuration match this outbound use case.
   - Configure one voicemail approach on every assistant that may handle a campaign call: the assistant-driven voicemail tool or built-in voicemail detection, never both. Test representative voicemail and call-screening paths before scaling.

3. Prepare and validate contacts.
   - Allow 1 to 10,000 contacts. Prefer E.164 numbers such as `+14155550100`. In an API request, an intentional non-E.164 SIP-trunk destination requires `numberE164CheckEnabled: false` on that customer; the number must still contain only an optional leading `+` followed by letters or digits. The Dashboard CSV importer cannot set this customer-level flag, so use E.164 numbers for that path.
   - For a Dashboard CSV, require lowercase `number`; lowercase `name` is optional. Every other populated column becomes a case-sensitive dynamic variable. Prefer lowercase `snake_case` headers.
   - Keep CSV files within the documented 5 MB Dashboard limit. Reject blank or malformed rows and surface duplicates for review; do not silently drop or merge recipients.
   - For API requests, place per-contact values in `assistantOverrides.variableValues` for an assistant campaign or `squadOverrides.variableValues` for a squad campaign. Do not copy arbitrary source columns into unrelated configuration fields.
   - Keep each contact's combined serialized variable data below 100,000 characters. Confirm that every variable referenced by the caller is present or has intentional fallback behavior.

4. Set timing and concurrency.
   - Omit `schedulePlan` for a new campaign that should dispatch as soon as capacity is available.
   - For a scheduled window, send `schedulePlan.earliestAt` and optional `latestAt` as ISO 8601 date-times. When the user gives local time, establish the IANA time zone, convert it, and show both local and ISO values.
   - Confirm `latestAt` is later than `earliestAt`. The Dashboard schedules up to seven days ahead in 15-minute increments; recheck current API constraints when implementing outside the Dashboard.
   - Choose `maxConcurrency` at or below the organization's available concurrency. It limits this campaign but does not reserve slots or increase the organization's shared call capacity.
   - Leave enough time for the audience. Contacts waiting for capacity may be retried for up to one hour, but retries stop earlier when `latestAt` is reached.

5. Configure campaign webhooks only when needed.
   - Set `server` before using `predialPlan` or `serverMessages`. Prefer a saved credential over inline secrets and use an intentional timeout and backoff plan.
   - Use `predialPlan: { "enabled": true }` for a blocking check immediately before each contact is dialed. The endpoint must return JSON containing Boolean `eligible`; false skips the contact, while timeout, non-2xx, or invalid JSON produces `contact.predial-failed`.
   - Use `serverMessages` for selected asynchronous campaign and contact lifecycle events. Make the receiver idempotent and do not depend on event ordering.
   - Campaign events do not contain the full call artifact. Configure `end-of-call-report` on the relevant assistant when the integration also needs transcripts, recordings, or analysis, and join records by `callId`.

6. Build and review the request.
   - For a fresh campaign, include `name`, exactly one of `assistantId` or `squadId`, `phoneNumberId`, a non-empty `customers` array, and `maxConcurrency`.
   - For a duplicate, include `name` and `duplicateFromCampaignId`, then send only intentional replacements. Omit `customers` to inherit the source audience; a supplied `customers` array replaces it.
   - Add campaign-level `assistantOverrides` or `squadOverrides`, `schedulePlan`, `server`, `serverMessages`, and `predialPlan` only when intentional.
   - Read [Campaign API Reference](references/api-reference.md) for validated REST shapes, duplicate semantics, pagination, and lifecycle requests.
   - Before a live launch, show the resolved caller and phone number, audience count with a redacted sample, local and ISO timing, max concurrency, webhook side effects, and whether calling starts now. Do not expose the full contact payload in routine confirmation output.

7. Create once and verify.
   - Send one `POST /v2/campaign`. Treat the returned campaign ID as the durable identifier.
   - Re-fetch it with `GET /v2/campaign/{id}?includeCounters=true` before claiming creation succeeded. Report the actual status and schedule; creation does not prove any contact was reached.
   - If creation returns an ambiguous timeout or 5xx, use `GET /v2/campaign` with narrow supported filters and creation-time context to look for the campaign. Do not automatically repeat the POST.

8. Inspect and diagnose from contact evidence.
   - Fetch the campaign with `includeCounters=true`. Use `contactCounters` for pending, dispatched, completed, failed, skipped, and pre-dial-failed totals; use `callMetrics.dialed` and `callMetrics.connected` for pickup analysis.
   - Fetch `GET /v2/campaign/{id}/contacts` and paginate when needed. Contact status is the source of truth for each audience member.
   - A skipped or pre-dial-failed contact may have no call ID because no call was placed. When a real `callId` exists, retrieve that call and inspect its ended reason, transcript, recording, analysis, and logs before proposing a root cause.
   - Separate campaign dispatch problems, pre-dial eligibility failures, telephony connection failures, voicemail outcomes, and assistant behavior. Counters alone do not identify the cause.

9. Duplicate to rerun or replace compatible configuration.
   - Campaigns are immutable after creation. Do not patch the caller, contacts, schedule, concurrency, or webhook configuration.
   - Create a new campaign with `duplicateFromCampaignId` and a new `name`. Omitted configuration and contacts are copied from the source; provided fields override the source, and provided `customers` replace copied contacts. The source must also use the current `/v2/campaign` API.
   - Duplication cannot unset every inherited field. In particular, switching between `assistantId` and `squadId` inherits the old mutually exclusive caller and produces an invalid request. Create a fresh campaign when changing caller type or when an inherited option must be removed rather than replaced.
   - Review every inherited field before launch. To run a duplicate near-immediately instead of inheriting an expired schedule, generate `schedulePlan.earliestAt` immediately before the request with enough future margin to remain valid during transport and server validation, such as current UTC time plus 60 seconds. State the resulting delay.
   - Treat a duplicate as another live launch with the same authorization and double-dial safeguards as a fresh campaign.

10. Cancel or archive deliberately.
   - To stop a scheduled or running campaign, send `PATCH /v2/campaign/{id}` with only `{ "status": "cancelled" }`. Pending work stops; calls already in progress may finish. Cancellation is final for that campaign.
   - Re-fetch and verify the terminal state and `endedReason`. Do not describe cancellation as reversing calls already placed.
   - `DELETE /v2/campaign/{id}` archives rather than permanently erases campaign records. If active, the campaign is cancelled first. Archive only when the user separately asks to remove it from active campaign views.

## Failure Handling

- `400`: report the rejected field and compare it with the current `/v2/campaign` schema. Correct one unambiguous request-shape issue before at most one safe retry.
- `401` or `403`: stop for authentication, scope, entitlement, frozen subscription, or permission failure.
- `404`: report the exact missing campaign, assistant, squad, or phone number ID.
- `409`: re-fetch the campaign; an immutable or terminal lifecycle conflict requires a duplicate or no further action, not a repeated patch.
- `429` or `5xx`: report the service condition. Never retry campaign creation until duplicate creation has been ruled out.
- Partial completion: preserve the campaign and report actual contact outcomes. Do not delete, redial, or replace the remaining audience automatically.

## Output Contract

Return only what the request needs:

- Mode: plan, payload, launch, inspect, duplicate, cancel, archive, or diagnose
- Resolved caller, outbound number, contact count, and redacted sample
- Local and ISO schedule, max concurrency, and shared-capacity caveat
- Consent and calling-window assumptions that still require user verification
- Webhook and pre-dial behavior, including remaining live side effects
- Save-ready CSV, JSON, or code when requested
- Campaign ID, verified status, counters, contact outcomes, and call IDs after live operations
- Unresolved failures, evidence, and the smallest safe next action

## Public Sources

- [Campaigns overview](https://docs.vapi.ai/outbound-campaigns/overview)
- [Campaigns quickstart](https://docs.vapi.ai/outbound-campaigns/quickstart)
- [Campaign contact data](https://docs.vapi.ai/outbound-campaigns/contact-data)
- [Campaign scheduling and lifecycle](https://docs.vapi.ai/outbound-campaigns/scheduling-and-lifecycle)
- [Campaign voicemail and call screening](https://docs.vapi.ai/outbound-campaigns/voicemail-and-call-screening)
- [Campaign webhooks](https://docs.vapi.ai/outbound-campaigns/webhooks)
- [Campaign API reference](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-create-v-2)
