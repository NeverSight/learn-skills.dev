---
name: api-idempotency-retry
description: Design idempotency-key support and client retry guidance for a public API so integrators retry safely - key derivation and per-caller scoping, storage TTL and replay windows, atomic claim mechanisms (DB unique constraint, SERIALIZABLE row lock, conditional writes), payload-mismatch rejection, in-flight duplicate handling, exponential backoff with jitter, retry budgets, timeout propagation, and SDK retry defaults. Use whenever the user mentions an Idempotency-Key header, duplicate or double-submitted requests, safe POST retries, backoff, or jitter - even if they never say "idempotency". Do NOT use for what the error response signals (samber/developer-platform-skills@api-error-design) or webhook delivery retries (samber/developer-platform-skills@webhook-platform-design).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Idempotency and Retry

You design the two halves of one guarantee: server-side idempotency keys that make a retried write safe, and client-side retry behavior that uses them responsibly. Shipping either half alone is the trap - Resilience4j's own docs state it as a hard constraint, not a suggestion: retried operations must be idempotent, so retry guidance without key support (or the reverse) leaves the guarantee open exactly where a dropped connection tests it.

Two facts frame everything below:

- Exactly-once delivery is impossible over an unreliable network (Tyler Treat's canonical argument, grounded in the FLP result). What a key actually buys is _effectively-once_: at-least-once delivery plus duplicate collapse, bounded to the scope where idempotency is actually implemented.
- There is no ratified standard behind the `Idempotency-Key` header. The IETF draft (`draft-ietf-httpapi-idempotency-key-header`) expired in April 2026 without ratification. The header name is consistent across the industry because Stripe popularized it, but the semantics (TTL, mismatch behavior, concurrency handling) are whatever each provider decided, so yours must be designed and documented, never assumed.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Paradigm: REST, gRPC, or both? (gRPC carries deadline propagation natively; REST needs the header convention and explicit deadline plumbing)
2. Which endpoints are non-idempotent? Request the endpoint list or OpenAPI spec and enumerate every state-changing operation.
3. What storage backs the key store - a relational DB with unique constraints and transactions, a conditional-write KV store, or only a cache? (rules atomic-claim options in or out - see step 4)
4. Do any requests call an external, non-rollbackable system mid-flight (a charge, an outbound email)? (drives recovery points - see step 5)
5. Which SDK languages do you ship, and do integrators also call raw HTTP? (drives how much of the retry mechanics you can default for them - see step 6)
6. What is the longest possible retry chain - dead-letter-queue replay windows, dispute windows, scheduled re-runs? (drives TTL - see step 3)
7. By when must the guarantee hold: a one-off fix (stop the duplicate charges one client is filing tickets about), or a compounding contract every future endpoint inherits? What is the effort ceiling on the claim mechanism - a ship date that rules out a schema or isolation-level migration, or existing fluency with SERIALIZABLE workloads? (re-ranks the claim menu - see step 4: a hard date promotes whatever the current store already supports, a compounding mandate promotes the richer claim lifecycle, and a ceiling that forbids a schema migration deletes the rungs it cannot reach rather than ranking them last)

## Who controls the retry loop

Every retry decision is made by a developer or a program, whoever bought the product. The design splits by who controls the retry loop:

- **First-party developers** - you control both ends; internal convention plus code review covers most of it. The cheapest audience to serve.
- **Third-party integrators calling raw HTTP** - they write their own retry loop from your docs alone. They need the full contract published: key semantics, TTL, mismatch and in-flight behavior, and a worked backoff example, because no standard fills the gaps for them.
- **SDK-mediated callers** - your SDK _is_ their retry loop. Its defaults (backoff, jitter, attempt caps, key auto-generation) are the contract most callers will never read past, so wrong defaults ship duplicates at fleet scale.

Design for raw-HTTP integrators first - a contract complete enough for them is what your own SDKs then automate - and treat SDK defaults as the highest-leverage artifact, since they decide behavior for the majority who never read the docs.

## Workflow

1. Identify retry-unsafe endpoints.
2. Design the key contract.
3. Set storage and TTL.
4. Claim the key atomically.
5. Design the response semantics.
6. Write client retry guidance and SDK defaults.
7. Document the contract for integrators.

Each step has a section below, in order.

## 1. Identify retry-unsafe endpoints

- RFC 9110 - the one ratified document relevant here - defines GET, PUT, and DELETE as idempotent methods and POST as not. It says nothing about the `Idempotency-Key` retrofit pattern.
- Enumerate every state-changing endpoint. Each must either accept an idempotency key or be explicitly documented as unsafe to retry - the review-level check `samber/developer-platform-skills@public-api-design-review` performs; this skill builds what makes the first option true.
- Verify claimed idempotency, don't trust the method: a PUT that appends to a log or a DELETE that decrements a counter is not idempotent whatever the method promises.

## 2. Design the key contract

- The client mints the key, the server never derives it. AWS's Builders' Library names the rejected alternative: a server-side hash of request parameters breaks when two genuinely identical requests are both intended (launching two identical instances on purpose) - a caller-provided key expresses intent an inferred one cannot. Stripe, AWS, Twilio, and Resend all put the client in charge.
- Scope keys per caller - `(account_id, idempotency_key)` - never globally. Stripe, AWS, and the standard Postgres reference implementation all key on the pair, so the same key string reused by different accounts never collides.
- Recommend a derivation to clients. Three work; rank them for the client rather than listing them (Resend's own recommendation order):
  - value: `event-derived > request-scoped > random UUID reused across retries`
  - effort: `event-derived > request-scoped > random UUID reused across retries`
  - efficiency: `event-derived > request-scoped > random UUID reused across retries` - value and effort rank identically here, so their spread decides the ratio: minutes wide on effort (name the key after an identifier the caller already holds) against the whole guarantee on value.
  - **Default rung: event-derived** (`order-confirm-${orderId}`) - deterministic by construction, so a retry cannot fail to reuse the key. Move down to request-scoped when no stable business identifier exists at call time, and to a reused random UUID when the caller is a stateless script. Nothing is starved here: every rung costs one line of client code.
  - Never rank a fourth rung below these: a fresh value per attempt (`Date.now()`, `randomUUID()` regenerated on retry) defeats the mechanism entirely, so document it as the anti-pattern instead.
- Guard the payload: the same key with a different request body is a client bug - reject it (409 is the field convention; Resend names it `409 invalid_idempotent_request`), never silently replay. The expired IETF draft generalizes this into an optional payload _fingerprint_ stored beside the key; a checksum of the payload is the simplest form.
- Store both outcomes. Stripe saves failures as well as successes - including 500s - so a retry replays the exact original result. Decide explicitly whether a stored failure replays verbatim (Stripe v1) or the operation may be re-attempted without side effects (Stripe v2); leaving it undecided is a design gap.

## 3. Set storage and TTL

- Retention is two separate concerns, not one TTL (Brandur Leach's reference implementation):
  - Replay window (~24h) - governs idempotent-replay correctness; also the documented convention at Stripe, Resend, and Twilio.
  - Reaper threshold (~72h) - a longer operational window that keeps records alive for human recovery, so a bad Friday deploy's failed requests survive the weekend for Monday's fix.
- Set the replay window from the longest retry chain (question 6), never from storage cost. A 24-hour TTL behind a 7-day DLQ replay is a duplicate waiting to happen. AWS retains EC2 run tokens for the resource's lifetime plus a grace period - which is what lets a late retry get a consistent answer even after the resource was deleted.
- After expiry, treat a reused key as a brand-new request - every provider surveyed does; none returns an error for post-TTL reuse.
- Store the full response verbatim (status, headers that matter, body), not a summary - the replay must be indistinguishable from the original.

## 4. Claim the key atomically

A check-then-insert is a TOCTOU race under concurrent retries: both callers see "absent" and both proceed. The claim must be a single atomic operation the storage layer arbitrates. Three mechanisms appear in production, ranked:

- efficiency: `DB unique constraint > conditional-write OCC > row lock + SERIALIZABLE`
- effort: `row lock + SERIALIZABLE > conditional-write OCC > DB unique constraint`
- value: `row lock + SERIALIZABLE > DB unique constraint == conditional-write OCC`

- **Default rung: a unique constraint on `(account_id, idempotency_key)`.** The database picks the single winner; the loser gets its 409 from the `INSERT` failure itself, not an application-level check. Nearly free - one index - and transaction isolation gives the fencing guarantee below at no extra cost.
- **Conditional-write OCC (DynamoDB-style)** delivers the same single-winner claim on stores without unique-constraint transactions - the tie on the value line is real: same guarantee, different storage family. Your answer to question 3 rules one of these two out rather than ranking it; a ruled-out option is deleted, not demoted.
- **Row lock + SERIALIZABLE transaction is the starved option.**
  - Value: a `locked_at` column inside a SERIALIZABLE transaction represents _in-flight_ as a first-class state, survives lock expiry, and anchors resumable recovery points.
  - Effort: isolation-level tuning, serialization-abort retry handling - so it loses every efficiency round.
  - Promote it when requests span foreign state mutations (question 4): multi-step requests need the richer claim lifecycle, not just a winner-picker.
- Whatever the mechanism: the claim and the business mutation must commit as one ACID unit - AWS states this as a hard requirement, not a best practice. A claim outside the transaction it guards can record a token for a resource that was never created, or the reverse.
- A bare Redis `SETNX` + TTL lock is not a fourth option. Kleppmann's analysis: without a fencing token, a client paused past its lease expiry can still write after the lock moved on - no timing assumption saves you. No surveyed vendor uses a distributed lock for the claim; if Redis is all you have, layer fencing tokens on top, and know the DB constraint sidesteps the problem entirely.
- This ranking is a default, not a law. Re-rank against the storage answer and the effort ceiling (questions 3 and 7): a team already running SERIALIZABLE workloads gets the starved option far cheaper than the effort line assumes. A ship date that forbids a schema migration promotes whichever mechanism their current store already supports.

## 5. Design the response semantics

The bug in most homegrown implementations is treating a key as binary - seen or not-seen. A key is a three-state machine: **absent**, **in-flight**, **complete**. The retry that hits an in-flight key is not the bug ("your client library did exactly what it was configured to do when the connection dropped"); the bug is a server with no way to say "seen, not finished."

| Outcome                  | What happened                            | Correct behavior                                                                                    |
| ------------------------ | ---------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Never received           | Network drop before processing           | Retry proceeds as a first attempt; the claim wins normally                                          |
| Received, not processed  | Claim held, no terminal result yet       | Return an in-flight conflict, or resume from the last recovery point once the original lock expired |
| Processed, response lost | Result committed; response never arrived | Replay the stored response verbatim - no re-execution                                               |

- For the in-flight case, pick one:
  - Reject with 409 (Resend's `409 concurrent_idempotent_requests`, documented advice "wait and retry") - simplest and safest default.
  - Block until the bounded result, when the caller needs it synchronously.
  - Return 202 plus a status URL, for long-running effects.

  Never let the second caller through because the first "seems stuck." The expired IETF draft deliberately made in-flight conflict and completed replay _different_ responses, not fallbacks of each other.

- For multi-step requests (question 4), decompose into atomic phases separated by each foreign state mutation, persisting a recovery point between phases - a retried request resumes exactly where it left off instead of re-running an external call already made. Record intent _before_ calling out, so a crash between call and response leaves evidence.
- Run recovery as active background jobs, not passive expiry (Brandur's model):
  - A _completer_ pushes abandoned in-flight requests through to completion.
  - A _reaper_ deletes expired keys and logs what it couldn't finish for a human.
- What the error responses look like - codes, envelope, `retryable` flag, `Retry-After` - is `samber/developer-platform-skills@api-error-design`'s territory; consume its signals, don't redesign them here. Distinguishing your two 409 meanings (payload mismatch vs in-flight) with distinct machine-readable codes is that skill's taxonomy applied to this skill's states.

See [references/key-lifecycle-walkthrough.md](references/key-lifecycle-walkthrough.md) for the full worked lifecycle: schema, claim query, all three states' responses, and a multi-step recovery-point example.

## 6. Write client retry guidance and SDK defaults

- Retry an explicit allowlist, never a blanket catch: 429 (honoring `Retry-After`), 502, 503, 504, connection timeouts and resets - 500 cautiously (some 500s are a real bug that retries identically). Never retry non-429 4xx, auth failures, or exceptions that are bugs. Four independent sources (tenacity, Resilience4j, Resend, and the response-signaling side) converge on this exact split - cite it as convergent practice, not one vendor's opinion.
- Never retry a read timeout on a non-idempotent operation without an idempotency key already in place. This is the exact boundary condition the server half of this skill exists to close.
- Backoff must carry jitter. Ranked (Marc Brooker's AWS analysis, the canonical source):
  - value: `full jitter > decorrelated jitter > equal jitter > no jitter`
  - effort: `full jitter == decorrelated jitter == equal jitter == no jitter` - a real tie, not a dodge: each is one formula or one library flag, identical to write, test, and reverse, so no rung buys its value with more of the reader's time.
  - efficiency: the value order unchanged, since equal effort cancels out of the ratio.
  - **Default rung: full jitter** (`sleep = random(0, min(cap, base * 2^attempt))`) - lowest total client work and lowest server load, at slightly more total time to completion.
  - Starved by that order: decorrelated jitter, which completes faster for more total work. Promote it when a user-facing call sits inside a tight deadline and time-to-success outweighs fleet load. Equal jitter is Brooker's "clear loser" among jittered options, and no jitter re-synchronizes the fleet into the exact spike that caused the failures - keep neither in the menu you hand an integrator.
  - Re-rank against what you know about the caller: a single-instance batch job pays none of the fleet synchronization cost this order assumes.
- Bound both attempt count and total duration, not attempts alone - a per-attempt-reasonable loop can blow past the caller's own budget. Log every retry (attempt, error, next wait); a silent retry loop hides an outage in the making.
- Add a fleet-wide retry budget, distinct from per-caller caps: stop retrying once retries exceed a set share of traffic over a sliding window. A hundred instances each retrying three times amplify load 300x while every instance looks reasonable in isolation. AWS's token bucket is the named implementation, tuned to engage the quota sooner in a real outage: 14 tokens per transient-error retry, 5 per throttle retry.
- Propagate the deadline: one overall deadline set at the top, per-attempt timeouts budgeted inside it - never a fresh overall timeout per attempt, which silently extends the caller's real wait. Set single timeouts at 2-3x measured p99, not an OS default. gRPC's relative-timeout-on-the-wire model is the citable mechanics for chains.
- Point integrators at their language's retry library (tenacity, Resilience4j, or equivalent) before describing formulas - the formula is a one-liner there, pre-debugged. When pairing with a circuit breaker, state the stacking order: `Retry → CircuitBreaker → RateLimiter → Bulkhead`.
- For SDKs you ship: default retries ON with backoff + jitter and a bounded attempt count (AWS defaults to 3 total), and auto-generate idempotency keys for unsafe operations where the SDK can. Defaults are the contract for callers who never read docs. How your retry defaults interact with the platform's rate-limit policy - whether SDK retries count against quota, adaptive throttling - is `samber/developer-platform-skills@api-rate-limit-policy` territory.

Formulas, budget mechanics, and deadline math: [references/backoff-jitter-formulas.md](references/backoff-jitter-formulas.md). Cross-vendor defaults to calibrate yours against: [references/vendor-sdk-retry-defaults.md](references/vendor-sdk-retry-defaults.md).

## 7. Document the contract for integrators

Because no standard defines the semantics, your documentation is the only normative source your integrators have. Document, per the audience split above:

- Which endpoints accept the key, the header name, max key length, and the recommended derivation.
- Scoping, the replay window as a concrete number, and what happens after it expires ("treated as a new request").
- Both conflict behaviors, each with its distinct error code: payload mismatch and in-flight duplicate.
- Whether a stored failure replays or re-attempts (the Stripe v1/v2 distinction, applied to your API).
- A worked retry loop with concrete numbers - schedule, cap, jitter - like Resend's documented `1s → 2s → 4s → 8s` capped at 30s.
- Never write "exactly-once delivery" - the claim is provably false across an open network. Write what is true instead: retries are safe within the documented key scope and window. Correct the claim wherever marketing already made it (Treat's steelman: Kafka's exactly-once holds only inside a closed transactional system; a public API is by definition not one).

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- A key accepted but never stored or honored - tells the client retrying is safe when it isn't; worse than no key at all.
- A fresh key value generated per attempt.
- Check-then-insert claiming (TOCTOU race).
- Binary key state with no in-flight representation.
- Same key, different payload, silently replayed.
- Replay window shorter than the longest retry chain (the 24h-TTL-behind-7-day-DLQ trap).
- A bare `SETNX` lock with no fencing token as the claim.
- No decision on whether stored failures replay or re-execute.
- Retry loop that resets its overall timeout each attempt.
- Backoff without jitter.
- "Exactly-once" anywhere in the docs.

## Measurement

- Concurrency gate: fire N identical concurrent requests with one key against a state-changing endpoint - exactly one side effect must execute; the other N-1 get the in-flight conflict or the stored replay. Binary pass; iterate the claim design until it holds. This is the definitional guarantee, testable directly.
- Crash-recovery gate: kill the server between atomic phases of a multi-step request, then retry - the request must resume from its recovery point with zero repeated external calls. Binary pass where question 4 answered yes.
- Duplicate side-effect rate in production: within the documented scope and window the design target is zero by definition - track it as the alarm that the gates regressed, not as a tunable threshold.
- Orphaned-key rate (claimed, never completed - the completer's queue): no published industry threshold exists, so set the baseline from your own first month and watch the trend, as with any unsourced operational metric.

## Invocation examples

- "Add Idempotency-Key support to our POST /payments and POST /orders endpoints - we're seeing duplicate charges when mobile clients retry on timeout."
- "Write the retry guidance section of our API docs, and pick the backoff defaults for the Python and Node SDKs we ship."
- "Two concurrent webhook handlers both created the same invoice - audit our idempotency implementation and find the race."

## References

- [references/key-lifecycle-walkthrough.md](references/key-lifecycle-walkthrough.md) - worked key lifecycle: schema, atomic claim, three-state responses with real 409 codes, recovery points, completer/reaper.
- [references/backoff-jitter-formulas.md](references/backoff-jitter-formulas.md) - the three jitter formulas with trade-offs, retry-budget mechanics, deadline propagation, timeout setting.
- [references/vendor-sdk-retry-defaults.md](references/vendor-sdk-retry-defaults.md) - how AWS, Stripe, Google Cloud, Twilio, and Resend default retry and idempotency behavior; what to copy and what to flag.
