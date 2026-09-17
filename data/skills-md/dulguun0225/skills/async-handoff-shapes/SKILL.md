---
name: async-handoff-shapes
description: The six rules for shapes assembled out of asynchronous handoffs rather than out of one publish and one subscription, in any language — a committed flow definition with at most one irreversible step and it is last, a compensating destination per reversible step that tolerates the forward effect never having happened, a bounded timeout on every waiting step carried on its own timer destination, an outbound webhook as a signed consumer with an allowlisted host and no redirects, an inbound webhook that writes to the outbox and does no work in the request, and a claim check whose object outlives the message. ALWAYS load before writing a saga, a process manager, an orchestration across services, a compensation or undo path, a business timer or timeout, an outbound or inbound webhook, or a payload too large for the transport. Install alongside async-handoff, whose thirty directives every rule here builds on; states the kind of check each rule needs, with the tool named in the matching stack skill (async-handoff-java).
---
# Asynchronous handoff: the composite shapes

**Install skill `async-handoff` first.** Every rule here sit on top of that skill thirty directives, cite them by id — `E-1` … `E-28`, `E-32`, `E-33` — and **none of those ids defined here**. Six directives defined here: `E-29`, `E-30`, `E-31`, `E-34`, `E-35`, `E-36`.

**Each of three groups sleep until own condition true.** That why separate skill, not more sections in core one:

| Group | Directives | Dormant until |
| ----- | ---------- | ------------- |
| A flow that commits in more than one transaction | `E-29`, `E-30`, `E-31` | repo have flow whose steps commit in more than one transaction |
| HTTP across the organisation's boundary | `E-34`, `E-35` | repo send or receive webhook |
| A payload the transport will not carry | `E-36` | payload cannot meet subject committed max size |

**Two bans not here.** `E-32` (broker not store of record) and `E-33` (no stream-processing engine, no in-handler window aggregate) come from same research pass as these six, but live in `async-handoff` because **ban with precondition = ban agent argue way past**. They never dormant.

**Read marker ceiling before rules. Ceiling lower here than core skill.** All six = **convention**, dated 2026-07-29, **no production use anywhere** — pass = **one researcher vs primary sources, no panel, no steelman duel, no hostile audit.** Core skill pass at least had audit, planted defect caught. This one no. So these six weaker *in shape* than thirty they build on, even where individual facts firmer. **No marker here promote without new research pass.** See *Markers, dates, and what they mean*.

## Why this skill exists at all

**Rule set that name own gaps must still split two kinds of gap. Earlier version not do this.**

**Named gap** inside directive = property no check can decide — semantic duplication, swallowing catch, cross-repository union check. Naming it = whole requirement, because silence read as coverage. Every named gap in `async-handoff` still open by design.

**Absence** different: shape repo will build, no directive mention, so nothing read as anything. Five of them, all composite — patterns built *out of* publishes and subscriptions, so rule set written per-publish and per-subscription miss them:

1. **Flow whose steps commit in more than one transaction** — saga / process manager. Was *expressible* under original directives (consumer that publishes write outbox row in own transaction = process manager), so nothing forbid it, nothing govern compensation or wait. Now `E-29`, `E-30`, `E-31`.
2. **State rebuilt from message history** — event sourcing. Now banned by `E-32`, in `async-handoff`.
3. **Aggregate computed across messages** — stream processor, join, time window. Now banned by `E-33`, in `async-handoff`.
4. **HTTP across org boundary** — webhook, both directions. Outbound webhook named as async handoff from start, so general rules always bind it; missing part = every rule *specific* to it. Now `E-34`, `E-35`.
5. **Payload too big for transport** — claim check. `E-21` require committed max payload size, say nothing about what to do when payload cannot meet it — rule that fail closed on page, open silent in repo. Now `E-36`.

**What pass NOT do, said because same honesty rest of rule set carry:** close **no** named gap in `E-1` … `E-28`. Those undecidable by any check repo can host — that why named not solved. And pass add **seven named gaps of own**: five belong to six directives here (`E-29`, `E-31`, `E-34`, `E-35`, `E-36`), two to bans it also produce (`E-32`, `E-33`, in `async-handoff`). Count of open residues go **up**.

## The premise, and what carries over

**Code written by LLM agents, no human read line by line, repo hand work off asynchronously.** Same premise as `async-handoff`, plus per-group condition above.

Everything in core skill still bind. Two consequences worth say, because each = rule agent try make exception to:

- **Compensation, timer, webhook delivery, claim-check publish = all ordinary messages.** Go through outbox and relay (`E-5`), carry deterministic identity (`E-7`), consumed through deduplicated port (`E-13`), declare failure policy (`E-16`), appear as catalog rows (`E-26`). Nothing here side channel.
- **Money step inside flow keep every money obligation.** `M-17` in published `money-api` skill still require idempotency record in money effect own transaction. `M-20` in `money` still require catalog event — which is **telemetry**, metric-and-log entry, NOT broker message. So emit it not satisfy `E-30` compensating destination, and `E-30` not satisfy `M-20`. **Irreversible money capture = exact case `E-29` last-step rule exist for.**

## The defaults these rules override, by name

Each = what agent produce when asked for one of these shapes. Naming it = the point.

- **Orchestrator with try/catch around steps.** *Steelman:* read exactly like requirement, happy path obvious, catch = where reviewer eye go — look like most careful version available. Rejected by `E-29` and `E-30`: catch run in process that maybe already gone, so compensation conditional on surviving; it compensate effects in other services by sync call, so failure mid-compensation leave part-compensated flow with no record; no committed list of steps, so `E-29` ordering rule and `E-26` catalog have nothing to read.
- **Scheduled scan for stale flow rows, as timeout mechanism.** *Steelman:* no timer destination, no scheduling infra, one method, cannot lose timer because re-derive from state every time. Rejected by `E-31`: scan interval silently become timeout real resolution, no committed value record it; scheduled scan that find rows in state and act on them **IS async handoff by `E-1` own predicate**, so sit outside allow-list; make every flow timing property of one cron expression nobody review.
- **Shared secret in webhook URL instead of signature.** *Steelman:* receiver need no verification code, work with any HTTP endpoint, URL known only to two parties. Rejected by `E-34`: secret travel in request target, **the one part of HTTP request logged by default at every hop**; no replay protection, captured URL work forever; rotation = re-register endpoint. All of that invisible to sender.
- **Do work inside inbound webhook request.** *Steelman:* sender get truthful status code — 500 mean really failed — no extra hop or table. Rejected by `E-35`: couple external caller timeout to our transaction, so sender retry arrive while first attempt still committing and effect happen twice; and "sender get truthful status" worth less than look, because at-least-once senders retry on timeout they *caused*.
- **Presigned URL as claim check.** *Steelman:* consumer need no storage credentials, no adapter — genuinely less machinery. Rejected by `E-36`: presigned URL have bounded lifetime, so **pointer expire while message still valid, still retained, still redrivable** — exact failure `E-36` exist to prevent, arriving through convenient option — and it free text, so egress destination taken from message field, which `E-34` ban.

Full steelman for each, standards evidence, and wordings that must not come back = in [evidence.md](evidence.md).

## A flow whose steps commit in more than one transaction

**E-29 — A flow that commits in more than one transaction has a committed flow
definition: an ordered list of named steps, each declaring the destination it
publishes, the destination it waits for if any, and whether its effect is
`reversible` or `irreversible`. A lint asserts at most one `irreversible` step per
flow and that it is the last step. The flow's own state is a row in the initiating
service's transactional store carrying the flow identity and the current step as a
value of an enumerated type; no code decides which step a flow is on by looking at
business data.**

Two failures. First structural, not operational. **Irreversible step in middle of flow mean later failure have nothing to undo it** — money captured, message sent to counterparty, third-party booking confirmed — so flow end part-done, every service internally consistent, business fact wrong. Nothing throw: each step succeed. Nothing compare across services, because no gate in this design can. **Put irreversible step last = only structural fix available, and it *decidable* moment reversibility is declared field** — whole reason declaration exist.

**Decide current step from business data = ambient modifier at flow level.** "If payment row exist we must be past step 2" = rule whose answer depend on writes by other steps, other flows, repair scripts. Same code reach different conclusion over time, retry re-run step already run. Explicit column make flow position a fact, not inference.
*Schema lint over the committed flow definition — the
at-most-one-irreversible-and-last rule, and that every named destination exists in
the `E-26` catalog — plus type design (the step enumeration, the flow-state row)
plus a static rule (the flow module decides its step from the state column only).
Convention, 2026-07-29.*

**Named gap:** whether step effect **actually** reversible = semantic claim, no tool decide. Declare refund-capable capture `reversible` = judgement; lint enforce only *consequence* of declaration. This residue belong in front of human at plan gate, and `E-28` citation obligation = where it land.

**E-30 — Every `reversible` step declares a compensating destination in the flow
definition. Compensation is a published message like any other — an outbox row,
the relay, the broker — consumed by the service that owns the effect, through the
deduplicated port. A compensation handler may not require that the forward effect
succeeded: it is correct when the effect never happened and correct when it has
already been compensated. No compensation is a synchronous call, and none is a
write to another service's data.**

**Framework own documentation = reason this need directive.** Transaction guidance agent will read tell application to "take remedial action … to compensate for the committed primary transaction" and **supply no mechanism**. Without rule, what get written = `catch` around orchestration that log, and committed effects of every earlier step stay committed forever with nothing record they should not have.

**Tolerate-absence clause = half that get missed, and it NOT idempotence.** `E-13` already make handler run-once-per-identity. This different property: compensation may arrive for forward effect that **never committed** — because step own state change succeed and confirmation never come back, or because `E-31` timer fire first. So compensation = **"cancel if present"**, never "undo row I know is there". Compensation that throw on missing row burn attempt budget, land on terminal destination, where message that correctly had nothing to do now look like failure.
*Schema lint (every `reversible` step names a compensating destination that
exists in the catalog) plus a static rule (the compensation handler registers
through the deduplicated port; no outbound synchronous client is reachable from
the flow module) plus an integration test per reversible step — compensate with no
forward effect, and compensate twice; one observable outcome in both. Convention,
2026-07-29.*

**E-31 — Every step that waits declares a timeout in the flow definition, and
there is no unbounded wait. The timeout is a message on a committed timer
destination that is **not** the retry delay destination; its due time is computed
inside the timer adapter from event time carried in the message, never from a
clock read in flow or handler code; and its maximum is a committed value. Where
the transport's own delay primitive is shorter than a declared timeout, the timer
is a committed re-publish schedule owned by the relay and the schedule is a
committed value a lint reads. A timeout that fires after the awaited message
arrived is a no-op decided by the flow-state row.**

**This = `E-16` absent-signal failure in worst form.** Subscription that stop produce lag, `E-16` staleness alert catch it. **Flow waiting for reply that never come produce *nothing*:** no lag, because message it wait for never published; no terminal-destination arrival, because nothing failed; no error anywhere. Only trace = row sitting in one step, and rows = what nobody read. **Every other alert in this rule set watch message that exist.**

**Transport force re-publish clause, not design taste.** Amazon SQS cap message timer at **15 minutes** (own quota page, read 2026-07-29), so business timeout of hours or days cannot be delay primitive at all, must be schedule — thing that can be forgotten, hence committed value.

**Separate-destination clause not tidiness:** share `E-17` retry delay destination make normal business wait look same as retry backlog, so `E-16` terminal-arrival alert fire on healthy traffic and get muted — **that how both signals die.**
*Schema lint (every awaiting step has a timeout at or below the committed
maximum; the timer destination differs from every retry delay destination) plus a
static rule (no clock read in the flow module) plus an integration test — let the
timeout fire and assert a terminal flow state, then deliver the awaited message
after the timeout and assert exactly one outcome. Convention, 2026-07-29.*

**Named gap:** flow whose timeout committed but absurd — thirty days on checkout — not decidable. Committed max bound it; whether number right = spec-and-review.

## HTTP across the organisation's boundary

**E-34 — An outbound webhook is a consumer, never a call from application code.
It is a subscription whose handler performs the HTTP call, so every consume-path
rule already binds it. The call is signed with a committed algorithm over a
committed component set including a timestamp and the message identity; the
destination host comes from a committed allowlist, never from a message field or
any user-supplied value; the client follows no redirects, and resolves the host
and checks the resolved address against a committed deny list — private,
loopback, link-local and the cloud metadata address — before connecting; every
call has a committed timeout; and the receiver's response body is never parsed as
authority for anything, only its status code decides success.**

Four failures, two of them security failures.

- **Unsigned delivery indistinguishable at receiver from anyone else POST**, so whatever receiver do on trust = unfounded, and nothing in either system report absence of signature.
- **Destination taken from data = server-side request forgery.** Enumerated defences = ones OWASP name for exactly this case: allowlist host by strict comparison, disable redirect following in client, resolve name and verify resolved addresses before connect (vs DNS rebinding), block private, loopback, link-local ranges **and cloud metadata endpoint, where prize = cloud credentials.** Enumerated not summarised as "prevent SSRF", because general wording = wish and each of these = committed value or client setting.
- **Follow redirect defeat allowlist by construction** — that why separate clause, not implementation detail.
- **Parse receiver body make outside party output an input to our state** with no schema gate anywhere: `E-18` and `E-19` govern broker payloads, not HTTP response.

**Two named standards exist. Which one repo sign with = per-stack pick, not directive here** — RFC 9421 sign HTTP message components, survive transformation by intermediaries; Standard Webhooks specify three headers, sign identity-dot-timestamp-dot-payload with HMAC-SHA256 or ed25519, carry several signatures at once so secret rotate with no downtime. **No skill here name winner**, and stack skill say why instead of picking: pass that produced these rules never check what maintained implementations either standard have on any stack, so pick made here rest on belief nobody verified. Repo commit one, record which and why in plan, re-check implementation availability at adoption. **What IS directive:** one of them committed, secret rotatable without downtime, and **tolerance = committed number** — spec require receiver check timestamp and **name no window**, so uncommitted tolerance = unbounded replay window.
*Static rule (no HTTP client reachable from application or flow modules; the
handler registers through the deduplicated port; no redirect-following
configuration) plus a schema lint (the allowlist, the deny list, the timeout, the
algorithm, the tolerance) plus an integration test — a redirect toward a private
address is refused; a delivery with a stale timestamp or a broken signature is
rejected by the repo's own verifier fixture; a host absent from the allowlist is
refused. Convention, 2026-07-29.*

**Named gap:** whether receiver verify anything = outside this repo. **Signing prove we signed, never that anyone checked.**

**E-35 — An inbound webhook is a message, not a request that does work. The
endpoint verifies the signature and the timestamp against a committed tolerance,
rejects on failure with no side effect, writes the payload inside one transaction
to the outbox — or to a committed ingress table that only the relay reads — and
returns. It performs no business effect in the request. The sender's own message
identity is the deduplication key, retained for the window `E-14` requires. The
payload is decoded against a committed schema for that sender under `E-20`'s
asymmetry, and an unverifiable sender is a terminal failure, never a default.**

**Inbound webhook = at-least-once delivery from system nobody here control or can ask.** Senders retry, so duplicates **certain**, not possible; nothing guarantee order; signed payload captured earlier accepted forever unless timestamp checked — **that what make tolerance a correctness rule, not hardening.**

**Do work inside request couple external caller timeout to our transaction:** sender give up, retry, effect run second time while first still committing — and each run = well-formed write, so trace in data and nowhere else.
*Static rule (the ingress module may depend on the outbox port and on no effect
port) plus an integration test — the same signed delivery twice yields one effect;
a tampered signature is rejected with no row written; a stale timestamp is
rejected — plus a schema lint (the tolerance, the per-sender schema, the identity
field). Convention, 2026-07-29.*

**Named gap:** sender retry policy = sender problem. **Ingress can be made idempotent; cannot be made guaranteed.** Sender that give up after one attempt = fact no check here can see.

## A payload the transport will not carry

**E-36 — Where a payload cannot meet its subject's committed maximum size, the
message carries a claim check under committed conditions, or the design changes.
The pointer is a nominal type and never free text; it names an immutable object
written and committed **before** the outbox row commits; it resolves through one
storage adapter that follows no redirects. The object's committed retention is
strictly longer than the destination's retention plus the terminal destination's
redrive window, and a lint compares the committed values. The message still
carries the semantic fields the consumer branches on — only bulk content moves.
The consuming handler's module may depend on the storage adapter and still may not
depend on any client for the producing service.**

**Pattern manufacture this rule set signature failure unless constrained: message decode perfectly and payload gone.** Two retentions decide that, configured independently — transport one, and object-lifecycle rule usually written in another repo by someone else — nothing compare them. **That why comparison = lint, not advice.** Amazon SQS retain message up to 14 days; object lifecycle rule of 7 days silently win, symptom = terminal failure weeks later on redrive.

**Write object after outbox row commit = dual write one layer down**, same shape `E-5` exist for: row commit, process die, object never written, message undeliverable forever with no record of what it should carry.

**Why this not violate `E-21` dereference ban, said because it look like it do.** That ban exist because consumer that read producer *current* state get different answer on replay. Immutable object written **before** fact published = state **at event time**, so replay read same bytes and `E-23` property survive. Clause carrying that distinction = dependency ban in last sentence: **object storage yes, producer API no.**

**Transport facts make rule necessary, not defensive — and first of them is a correction.** Amazon SQS max message size = **1 MiB**, raised from 256 KiB in 2025 — **so figure any agent supply from memory is wrong**, and repo pinning old one under-use transport and reach for claim check it not need. Above that limit vendor own answer *is* this pattern: extended client that store payload in object storage and put reference in message, capped at 2 GB, documented as working only for synchronous clients — real constraint. Self-hosted NATS server default max payload = 1 MB, values above 8 MB not recommended by own docs.
*Type design (the pointer type; no free-text URL) plus a schema lint (the
per-subject maximum, the retention comparison, the storage adapter's redirect and
allowlist settings) plus a static rule (the dependency ban) plus an integration
test — the object is present when the message is processed, and a claim check whose
object is absent is a terminal failure and not a silent skip. Convention,
2026-07-29.*

**Named gap:** object store actual lifecycle config = infrastructure — same class as `E-5` durability gap and `E-14` retention gap. Lint read repo *declaration* of it, and declaration can be lie.

## Interlocks these rules must not break

- **`E-30` compensation must not become one generic undo handler taking any message type.** Compensation is per step and per destination, else `E-29` flow definition have nothing to lint and `E-26` catalog have nothing to enumerate. Single `CompensationHandler` satisfy prose and destroy both checks.
- **`E-31` timer destination is not `E-17` retry delay destination. Stack must not economise by sharing one.** Different alerts: arrival at retry destination mean something failed; arrival at timer destination mean time passed. Merged, only surviving alert = one nobody can act on.
- **`E-34` webhook handler not exception to `E-5`.** If it need record delivery outcome as fact other services consume, it write outbox row in own transaction like any other consumer. **"It already made HTTP call, so publish here same kind of thing" = reasoning to refuse.**
- **`E-36` pointer type not licence to reintroduce dereference.** Permitted dependency = storage adapter and nothing else; handler that gain API client for producing service re-create `E-21` hazard with pointer as excuse.
- **`E-33` ban on in-handler cross-message state bind flow module too.** No mutable field, no static collection, no accumulating buffer — and scheduled read-model refresh = adapter concern with committed schedule, never scheduling annotation in flow or service class.
- **Money step keep every money obligation.** See *The premise, and what carries over* above. `E-30` and `M-20` not substitute for each other in either direction.

## Markers, dates, and what they mean

**All six directives above = convention, dated 2026-07-29**, and that ceiling on whole group, not per-rule accident. None survive three independent refutation votes against primary sources, because each = **design argument, not execution result**. **No production use of this rule set anywhere.**

**Pass behind these six = weakest behind any skill in this set. That first thing to know.** One researcher, vs primary sources — vendor licence announcements and licence files, framework reference docs and javadoc, design-proposal pair, queue-quota page, server-configuration reference, OWASP prevention guidance — with **no panel, no steelman duel, no hostile audit.** Core skill pass fall short of three refutation votes but DID have audit, and planted canary caught. This one have nothing standing in for votes at all. Where fact quoted above firmer than core skill — SQS quotas, signing standards, OWASP enumeration — that property of *facts*, not of pass shape.

- **confirmed** — survive three independent refutation votes vs independent sources. **No directive here carry it.**
- **primary-source verified** — one researcher check vs primary source, no panel. No directive carry it; several *facts* quoted above do, dated in [evidence.md](evidence.md).
- **convention** — defensible practice research not or could not confirm from independent sources. All six.

**Do not promote marker here without new research pass.** Specific condition in [evidence.md](evidence.md): steelman duel plus hostile audit over this pass output. Same trigger the two bans in `async-handoff` carry, because same pass.

**Lapse rule.** These rules last dated for review by **2027-01-29**. Past that date every **confirmed** marker read as **convention** until new pass re-date it. Need no maintainer action, and here change nothing, because nothing confirmed.

Pass, sources, full steelman for each rejected shape, wordings that must not come back, and conditions that reopen a decision = in [evidence.md](evidence.md).