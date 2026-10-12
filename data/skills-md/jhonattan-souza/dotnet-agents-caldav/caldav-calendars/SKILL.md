---
name: caldav-calendars
description: Use dotnet-agents-caldav MCP tools to inspect or manage CalDAV Calendars, Events, To-dos, recurring Occurrences, and exact Calendar Object Resources.
---

# CalDAV Calendars

Translate the user's Calendar intent into the fewest safe `dotnet-agents-caldav` MCP calls. The live tool catalog, descriptions, input schemas, and structured outcomes are authoritative; use this skill for routing and sequencing, not as a cached schema. If a referenced tool is absent, report the catalog limitation.

## Resolve intent once

Before calling a tool, determine the Entity Kind, Calendar Scope, time window, and whether the request is a read, a proposal, or a mutation. Preserve only facts the user supplied or the configured defaults establish.

- Resolve relative dates from the current date and the user's known time zone. For every To-do query Start and every bounded Entity or Occurrence query Start, pass the known user or harness IANA zone explicitly, or rely on a validated configured IANA zone. Omit `evaluationTimeZone` from an unbounded Entity query, where it is unused. Ask for a zone only when it is genuinely unknown.
- Send a `zonedDateTime` with an IANA zone such as `Europe/Paris`; a Windows zone name is accepted and stored as its IANA equivalent. Keep every returned `timeZoneId` exactly as read, and send it back unchanged in a recurrence identity. A `timezone_reference_unresolved` diagnostic means the resource's own `TZID` cannot be resolved; a different evaluation zone will not fix it.
- A query success may carry `temporallyUnresolved`: resources whose own times could not be placed, left out of `items` rather than guessed into or out of the window. Tell the user the answer excludes `count` resources and, when the task needs them, read the listed hrefs with `calendar_resources.get`. Do not retry with another evaluation zone.
- Never send a one-sided time filter. For example, “due this week” maps to `dueFrom` at the requested week's start and `dueTo` at its exclusive end. “Due through Friday” also needs a lower bound; use the current evaluation instant when that matches the intent, or clarify whether older overdue items belong in the result.
- Establish an **authorized destination selection** before creating or moving an Event or To-do. It exists only when the user explicitly supplies a Calendar Name or canonical href, a prior trusted result provides the canonical href, or the existence and Entity Kind binding of a configured default are already established in context. A Calendar Name is a selector, not identity, and need not be unique; if selection returns `ambiguous`, ask the user to choose from its authorized candidates. Generic phrases such as “my calendar”, “my task list”, “agenda”, “calendário”, “lista”, or “lista de tarefas” express purpose, not a destination selection.
- For a create or move with no authorized destination selection, call `calendars.list` once and retain only Calendars whose relevant Entity Kind Support is `advertised`. For a move, also remove the source Calendar's canonical href from the candidates. Select the sole remaining Calendar by its returned canonical href. If more than one Calendar remains, ask the user to choose before the first write. If none remains, report that no compatible destination Calendar is available and ask whether the user wants to create one. Use `default` only when its configuration is already established; the schema permitting `default` does not establish one.
- A simple request such as an Event tomorrow at 18:00 can be one `events.create` call once it has an authorized destination selection; omit an unspecified end or duration. The server stores `PT1H` for a timed Event when neither is supplied, while a date-only Event remains one nominal day.
- For a recurring Event or To-do, `start` is required and must be the first occurrence of `rrule`. When a To-do has both `start` and `due`, `due` uses the same temporal kind and time zone as `start` and is later than it; a date `due` is an exclusive boundary, so a To-do due on day D uses `start` D and `due` D+1. A rejected create names each field in `violations[].pointer` with a `violations[].code`; correct that field and retry rather than dropping the recurrence.
- Ask one concise clarification when different answers would materially change stored data: which of several matching resources, one recurring Occurrence versus the series, or what “organize next week” should change. Gather related missing choices together. For an open-ended organization request, read the relevant week once, propose a concrete plan, then mutate only the plan the user accepts.
- Before `calendars.create`, resolve a user-authorized display name and component set: Events, To-dos, or both. Ask for the name before any tool call when the request supplies only a generic purpose, and never invent one. Infer the component set only from explicit intent, and ask once for any missing field before the first write. When both are known, create the Calendar and use its returned canonical href for the requested resource without intervening discovery.
- Before a broad or destructive request, resolve Calendar scope, Entity Kinds, temporal cutoff, and selection criteria. Query one bounded set, present its finite targets, get the user's agreement to that set, and then mutate each target with its own call. Do not turn an open-ended result or pagination stream into an automatic deletion loop.
- Before any exact write, require the user's message to supply the complete caller-authored Calendar Object Resource body. If it does not, ask for that body before every tool call. Do not read the existing resource and turn it into supposedly caller-authored replacement content.

Intent is resolved when one call plan covers the whole request and every remaining uncertainty can safely be left absent or to a configured default.

## Discover only when discovery changes the call

Call `calendars.list` once for a stable selection intent, and only when the Calendar's name, canonical href, Event/To-do capability, or default identity is genuinely needed and unknown. Reuse that result while the intent and scope remain unchanged; list again only after the user changes them or a result proves the selection stale.

Skip discovery when:

- the request uses `all` scope;
- a configured default's existence and Entity Kind binding are already established;
- an authorized explicit Calendar Name selector or canonical href is already known;
- an absolute resource href can go directly to `calendar_resources.get`; or
- a preceding result already returned the Calendar identity.

Use a known Calendar name directly where the live schema accepts selection by name. If selection returns `ambiguous` with authorized candidates, ask the user to choose from those candidates rather than rediscovering them. Treat Calendar href as identity and display name as presentation.

Use `calendars.create` only for a new Calendar collection. Use `calendars.delete` only when the user intends to remove the whole collection and every resource in it; resolve its exact href first and continue the tool's own finite confirmation review. Unless the user asks for a separate preview, do not enumerate every contained resource before that review or list again after an uncommitted attempt. Event or To-do deletion is `calendar_resources.delete`.

Use `calendars.inspect` when standard Calendar metadata, report or privilege evidence matters. An absent advertisement does not prove an operation is unsupported. Use `calendars.patch` for Calendar display name, description, color, order or time zone changes, with explicit set/remove operations; omitted fields remain unchanged. Supply color only as `#RRGGBB`, order as a non-negative integer and time zone as an IANA identifier the user stated or confirmed; never infer one from the host or locale. `description` is the CalDAV calendar description; `davDescription` is a separate read-only WebDAV property. These metadata writes are unconditional and can overwrite concurrent changes to the addressed properties; a rejection names each unapplied property in `violations`. `calendars.create` accepts the same optional color, order and time zone. When creation finds multiple homes, use an explicit destination under the intended home.

Discovery is complete when the next operation has a schema-valid authorized scope or destination selection without a speculative write.

## Choose the narrow read

- `calendar_occurrences.query`: an agenda or schedule in a bounded half-open time window, including expanded recurring instances.
- `todos.query`: compact To-do lists, completion or due filters, and a projection limited to fields needed for the answer. Keep a To-do-list request on this path even when a result is recurring; switch to Occurrences only when the user asks for instances on a schedule. Its completion target can bind a later completion.
- `calendar_entities.query`: persisted Event or To-do resource snapshots, especially for inspection, search, or revision-bound edits of the containing resource.
- `calendar_resources.get`: one authoritative snapshot at an already confirmed absolute resource href.
- `calendars.free_busy`: busy periods for one exact Calendar and a whole-second UTC window, computed by the server without Event details. Periods from every returned busy component are merged per busy type. Preserve busy types; an error never means that the interval is free. If discovery cannot authorize a free/busy-only Calendar, its exact href must be configured in the Calendar allowlist.
- `calendar_resources.changes`: initial membership or changes since a previous synchronization checkpoint, with hrefs and observational ETags. Use it for change polling; read only changed resources whose content the task needs.
- `changeTag` on `calendars.list` or `calendars.inspect`, when present, is an opaque advisory Calendar Change Tag. Compare it only for exact equality as a cheap hint that a Calendar may have changed; never parse it or treat it as a revision, precondition, or checkpoint. Use `calendar_resources.changes` to learn what changed.

For changes, start with `calendarHref`, then copy the returned 36-character `checkpoint` exactly and pass optional `pageSize`. Apply the entire page before saving its checkpoint and continue while `hasMore` is true. Keep initial inventory separate from incremental changes. A removal means removal from view, including possible revoked access. Checkpoints expire with the MCP session, configuration, or eviction from its bounded state store; `sync_reset_required` requires a fresh initial inventory. Unchanged state reuses the same handle. They are distinct from query cursors and resource revisions. A page error supplies no replacement checkpoint: retain the prior one and follow the reported recovery action.

The server negotiates optional sync limits internally. Some servers require the entire inventory or delta to fit the client's bounded page. When the error identifies page-size overflow, retry with a larger `pageSize` up to 500 while retaining the prior checkpoint; a deadline or byte-limit failure requires its own reported recovery.

Start one query with its complete scope, filters, requested window, and optional page size. Temporal windows are complete pairs: supply both `from` and `to`, and both `dueFrom` and `dueTo`; never send only one endpoint. A bounded window must be non-empty and at most 366 days. Do not invent distant lower or upper bounds for an unbounded search; omit bounds the user did not request when the live schema permits it. For “next N”, use one reasonable horizon of at most 366 days and widen only if the result proves it insufficient. If more requested results are needed, Continue with only `cursor` and optional `pageSize`; copy the opaque cursor byte-for-byte, because changing even one character invalidates it. Repeating Start arguments creates an invalid continuation. Consume one snapshot traversal instead of rerunning the query. On `cursor_expired`, start a fresh query and disclose that the results were reevaluated.

Use only fields the answer needs. Do not add discovery, another query family, or an exact-resource read merely to enrich an already sufficient result. If a call fails, inspect its arguments and typed outcome before doing anything else; when `violations` is present, each item's `pointer` names the failing argument and its `code` and `message` say why, so correct that member. Make at most one materially corrected retry; never fan the same failing operation out across Calendars, repeat it unchanged, or describe a local argument failure as server unavailability.

For a title, keyword, or tag search, pass `text` and, when the user names tags, `categories` on the narrowest query: an unbounded `calendar_entities.query` for resources across Calendars, `calendar_occurrences.query` for a bounded agenda, or `todos.query` for To-dos. Every whitespace-separated term and every category must match, case-insensitively, the summary, description, location, or categories of one Event or To-do component, and an Occurrence matches only its own override's text. Use the user's distinctive words, not synonyms or wildcards. Do not page through an unfiltered result to search it yourself, guess a day, or query each Calendar separately.

A read is complete when the requested range is covered, the returned Temporal Evaluation Context is honored, and no extra projection or page was fetched.

## Bind every existing-resource write

Once a create has an authorized destination selection, call `events.create` or `todos.create` directly; it needs no preliminary Event, To-do, or resource read. To modify, complete, move, or delete an existing resource, first obtain its fresh strong revision through the narrowest query or `calendar_resources.get`, then pass the returned reference exactly as the live schema names it:

- `events.patch` or `todos.patch` for field changes and rescheduling;
- `todos.complete` for completion;
- `calendar_resources.move` to move the whole resource to another Calendar;
- `calendar_resources.delete` to delete the whole resource.

Entity and Occurrence snapshots expose `entityRevision`; compact `todos.query` results expose `completionTarget.entityRevision` when the target is writable. Use that returned reference as `snapshot` for patches, completion, and Occurrence mutations, and as `revision` for semantic move and delete. Summary, position, Calendar name, and time are not mutation identity. After a conflict, use an authorized complete `currentSnapshot` from the outcome or query again, then obtain renewed intent before another write.

For recurrence, preserve two identities:

- the resource revision identifies the containing Calendar Object Resource;
- the exact returned `recurrenceIdentity` identifies one Occurrence.

Never synthesize recurrence identity from a displayed time. Read Occurrences to distinguish one instance from `this-and-future` or `entire-set`. When a compact To-do completion target is `occurrence_required`, query the Occurrence; an `unavailable` target is not writable through `todos.complete`. Use the live patch target for ordinary changes and the `calendar_occurrences.*` tools for explicit add, exclude, cancellation, or restoration semantics.

Each call writes at most one Calendar Object Resource. An existing-resource write is ready only when the user-selected target, fresh revision, recurrence scope when applicable, and destination when applicable all refer to the same reviewed intent.

Accept a committed semantic mutation's structured outcome as completion. Do not add a verification read unless the outcome is indeterminate or committed-but-unverified and the user needs reconciliation.

Storage-only writes involving organizer or attendee data require evidence that the target does not perform automatic scheduling. Collection deletion requires the same evidence only when the tool's own bounded member scan finds organizer or attendee data, including in an alarm, or cannot finish; the scan is internal, so do not enumerate members for it. A `limit_exhausted` collection delete with `not_attempted` deleted nothing; report it instead of retrying. If the tool reports `unsupported_capability` for that boundary, report the limitation; stripping participation data or switching to an exact write can itself cause scheduling side effects and cannot bypass the restriction.

An installation may opt into server-managed scheduling. Its confirmation reviews then carry a scheduling notice, and affected outcomes carry `schedulingSideEffects`. Before a write that adds, changes, or removes organizer or attendee data, or deletes a resource or Calendar that may hold meetings, tell the user that the server may email invitations, updates, or cancellations to participants. When an outcome reports `schedulingSideEffects: possible`, tell the user that the server may have contacted participants; the server does not report whether it sent anything. `none` means that call admitted no write on a server that advertised automatic scheduling. Never add, remove, or rewrite participation data or scheduling parameters to avoid or cause delivery unless the user explicitly asked for that data change.

## Continue confirmations faithfully

The installation's Confirmation Policy decides which mutations open a confirmation round, so call each mutation the same way and let its result show which path it took. A call the policy exempts commits without a round, and its committed or unknown outcome carries `confirmation: skipped_by_policy`: report it like any other write, with that outcome. A call the policy protects returns MCP `input_required`. Present the returned review, obtain the requested input, and continue the same tool with its opaque `requestState` and `inputResponses`. Keep `requestState` unchanged, single-use, and paired with the original arguments and revision.

A harness connected through the `initialize` handshake on MCP `2025-06-18` or `2025-11-25` receives the same review as a classic elicitation request while the original call is still open; answering it completes that call, and there is no `requestState` to carry. The server does not bound that wait, but the user must answer within 10 minutes of the review or the call ends as `confirmation_expired` with nothing attempted. A `2024-11-05` or `2025-03-26` session, or one that did not declare form-capable `elicitation`, gets typed `unsupported_capability` in phase `mrtr` with `mutationState` `not_attempted` for every protected mutation: report that harness limitation instead of repeating the call.

On MCP `2026-07-28`, a JSON-RPC error `-32021` carrying `data.requiredCapabilities` means the harness did not declare form-capable `elicitation` for that request, so the server opened no confirmation and attempted nothing. A blank `elicitation` declaration counts as form support; one that names only `url` does not. Report that harness limitation instead of repeating the call unchanged.

Expiry, mismatch, decline, a changed revision, or a continuation failure ends that exchange without a new write. A confirmed continuation can also return typed `busy` with `mutationState` `not_attempted` when the server is saturated; nothing was written, and a later attempt starts over with a new review and confirmation. If the active harness cannot continue MCP Multi Round-Trip Requests, report that limitation and leave the mutation uncommitted. A typed `confirmation_mismatch` whose message says the client accepted without sending `confirm=true` is the same harness limitation: the harness approved the review without filling in its form, so the user's approval never reached the server. Do not call the protected mutation or a verification query again to work around a missing continuation. A client hint such as `allow_input_required` is not a CalDAV tool argument unless the live input schema explicitly includes it.

Treat `structuredContent` as authoritative. Report `outcome`, `mutationState`, `no_change`, `confirmation_declined`, and typed failures accurately; `confirmation_declined` means the user refused the review or the harness cancelled it unanswered. A transport-level success does not prove a mutation committed, and an indeterminate or committed-but-unverified result needs explicit disclosure rather than an automatic retry.

## Reserve exact tools for exact resources

Semantic tools are the normal path. Use `calendar_resources.exact_get`, `calendar_resources.exact_create`, `calendar_resources.exact_replace`, or `calendar_resources.exact_move` only when the exact catalog is exposed and the user explicitly needs byte-preserving access. For an exact read, follow its returned MCP resource link once; a saved local path is the completed read, not another MCP resource to fetch. A `-32602` read error means the linked href or revision is no longer readable; call `calendar_resources.exact_get` again only if the user still needs the current bytes. Caller-authored complete Calendar Object Resource content is a precondition for every exact create or replace: obtain it before the first exact write call, and never fabricate it from a partial change request or retry with invented content. Exact writes also require explicit absolute hrefs, applicable strong revisions, and MRTR confirmation unless the Confirmation Policy is `never`. Stored URI values remain inert; these tools do not fetch attachments or send invitations.

## Completion criteria

Finish only when:

- every requested read range or mutation is accounted for;
- every create and move had an authorized destination selection before the first write and unique resolution before commit;
- discovery and query calls were not repeated without new information;
- each existing-resource write used the latest returned revision and exact recurrence identity when applicable;
- every MRTR exchange reached a confirmed terminal outcome or a clearly reported harness limitation; and
- the response distinguishes committed, unchanged, declined, failed, and indeterminate outcomes.
