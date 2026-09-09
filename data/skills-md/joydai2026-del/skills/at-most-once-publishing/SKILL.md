---
name: at-most-once-publishing
description: >-
  Durable send state machine for anything an agent publishes outward: at-most-once across crashes, timeouts, retries. Use when: "make sure it doesn't post twice", "idempotent publish", "duplicate posts", "the request timed out, did it go through", "publish state machine", "safe retry", "exactly-once", "outbox pattern", "at-most-once", "recovery is resending things", "crash during send". Applies to any side effect that cannot be undone.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
gotchas_count: 1
---

# At-Most-Once Publishing

## Plain English first

The hard case is not the request that fails. It is the request that you never got an answer
to. The bot sent the bytes, the connection died, and now nobody knows whether the post
exists. Almost every naive system retries here, and that is how an account posts the same
thing three times.

The rule this skill enforces: **an unknown outcome stays unknown.** It is reconciled by
going and LOOKING at the platform, exactly once, and it is never automatically resent.
You choose at-most-once over at-least-once, because a missing post is recoverable by a
human and a duplicate post is not.

## Two rows, not one

Almost every broken version of this collapses two different things into one row, and then
cannot express a retry without either blocking it or losing identity. Keep them separate:

| Row | Cardinality | Identity | Mutable |
|---|---|---|---|
| **delivery intent** | ONE per logical thing you intend to deliver | the delivery key, stable forever | its STATE moves; the key never changes |
| **attempt** | append-only, N per intent | a fresh attempt token per attempt | never; attempts are immutable facts |

The delivery key is what makes "did I already do this" answerable. The attempt rows are what
make "what happened each time I tried" auditable. A retry re-opens the SAME intent and the
next `begin()` appends the next attempt, which is exactly why the two must not be one row.
`begin()` is the only thing in the system that creates an attempt.

**The delivery key must include the action kind and the canonical request, not just the
text.** A like, a repost, and a follow on the same target carry no outgoing text at all, so
a key of `account + text + target` collides across all three. Use:

```
delivery_key = hash(account_id, action_kind, target_identity, canonical_request_projection)
```

where `canonical_request_projection` is the normalized request you will actually send (for a
post that includes the text; for a like it is essentially empty; for a quote it includes both
the text AND the linkage). Every verb then gets a distinct key on the same target.

## The state machine (of the delivery intent)

```
   pending
      |  begin()  -> opens a new ATTEMPT against this intent, atomically.
      |              Fresh attempt token. Restart-protected.
      v
   authorized / in_flight        <- authorize_dispatch(): the LAST checkpoint before any
      |                             byte leaves. One database authorization, or nothing
      |                             sends. Written BEFORE the bytes, carrying a worker
      |                             lease with a deadline.
      |
      +-- transport returns success --> read-back --> published        [TERMINAL]
      +-- transport returns definitive-not-sent -----> failed
      +-- transport returns unknown -----------------> indeterminate
      +-- worker never returns AT ALL (crash, OOM, host loss):
             the LEASE EXPIRES and a sweeper moves the intent to indeterminate.
             It NEVER moves it back to pending and never re-sends.

   failed  --(policy allows, and ONLY from failed)--> pending
      |     Retry moves the INTENT back to pending and creates nothing itself. `begin()`
      |     stays the single atomic creator of attempt rows, so there is exactly one code
      |     path that can mint an attempt. Retry is legal here and ONLY here, because
      |     "definitive not sent" is the one outcome that proves zero bytes landed. The
      |     delivery key is unchanged; the next `begin()` mints a new attempt token.
      |     Cap the attempts on the intent and park on exhaustion.

   indeterminate
      |  reconcile(): at most ONE lookup against the platform.
      |  -> found       => published
      |  -> not found   => STILL indeterminate (see below). Never pending. Never resent.
      v
   parked   <- terminal, human-owned. Reached from indeterminate when reconciliation is
               unavailable or exhausted, from failed when the attempt cap is hit, or
               whenever the operator says stop. A machine never leaves this state.
```

**`failed` is the only retryable outcome, and that is the whole point.** It means the
transport proved nothing left. `indeterminate` is not retryable, ever, and the sole reason
this design exists is to keep those two apart. A system that treats every non-success as
retryable is an at-least-once system wearing this one's vocabulary.

**Six states, and the last three are the ones people collapse:** `pending`, `authorized`
(in flight), `published` (terminal), `failed` (the ONLY retryable one, nothing sent),
`indeterminate` (unknown, never retryable), `parked` (terminal, human-owned). Most bugs come from a system that has only success and
failure and therefore has to guess about the middle.

**The crash case is why `authorized` must be a durable state and not a variable.** A worker
that dies after authorization returns nothing, ever. If your only rule is "an authorized
worker must return an outcome", that row is stuck forever. The lease deadline is what makes
the crash representable: lease expiry moves the row to `indeterminate`, which is a state
that is safe to sit in, because nothing in the system resends from it.

## The seven mechanisms

### 1. Send intent is durable and written BEFORE the bytes

One ATTEMPT row per authorized dispatch, appended under a stable delivery intent (above).
It carries the account, the action kind, the exact wire request hash, the credential
version, the intent's delivery key, and its own fresh attempt token. If the process dies
after this row and before the response, the row is what makes the outcome knowable rather
than lost.

### 2. Before-byte authorization

The transport must obtain a database authorization at its FINAL checkpoint, immediately
before writing bytes. Not at the start of the flow. Everything expensive, every gate, every
model call happens earlier; this last call exists so that a stale worker, a revoked
credential, a kill switch flipped thirty seconds ago, or a changed platform contract can
still stop the send with zero bytes out.

**Re-check the same conditions here that you checked pre-flight.** A gate that only runs
pre-flight is a TOCTOU race. On the real system a cross-model review caught exactly this:
the contract gate ran pre-begin but not at final authorization.

### 3. Pre-authorization stale workers are rejected; post-authorization workers are NOT recovered

This asymmetry is the whole design and it is not obvious.

- A worker that expired BEFORE it was authorized never sent anything. Reject it, free the row.
- A worker that WAS authorized may still be mid-flight. It cannot be auto-recovered and it
  cannot be parked while its lease is live. Either it returns a transport outcome, or its
  lease expires and a sweeper moves the row to `indeterminate`. Both paths are one-way.

Getting this backwards produces the exact duplicate you built the system to prevent.

**Also disable the transport library's own automatic retries.** Most HTTP clients retry
idempotent-looking requests by default. That retry happens below your state machine and is
invisible to it, so your careful at-most-once design sits on top of a client that already
sent it twice. Turn it off explicitly and assert it in a test.

### 4. Read-back verification

`response_received` is not proof. Wrap the transport so that after a claimed success it
reads the object back from the platform by id and compares the canonical text. On the first
live write of this system the read-back is what upgraded "the API returned 200" into "the
post exists and says exactly what we approved".

**Read-back is also what limits reconciliation, and this is a real constraint.** A lookup
can prove PUBLISHED. It can rarely prove NOT-SENT, because most platforms are
read-after-write eventually consistent, do not expose a lookup keyed by your idempotency
key, and give you no way to distinguish "never arrived" from "arrived and is not indexed
yet". So:

- if the platform DOES offer an idempotency-status lookup keyed by your original request,
  use it, and you can resolve both ways;
- if it does not, a lookup that finds nothing resolves NOTHING. The row stays
  `indeterminate` and eventually `parked` for a human. Never treat "I could not find it"
  as "it was not sent".

**A browser-side abort route is not a safe dry run.** Client automation can report that a
network route was installed while the application's create request still reaches the platform.
Never click a real Publish/Post control merely to test click wiring unless that exact external
write is authorized and already owns the durable delivery identity. A non-publishing probe must
stop at DOM, selector, focus, and enabled-state inspection, or use a server-side test sink whose
zero-write behavior is independently proven. If a supposedly blocked diagnostic unexpectedly
returns a create success, stop immediately, treat it as a live side effect, reconcile and bind the
result to the existing intent, and never click again.

### 5. Fencing with a monotonic generation, backed by a SEQUENCE

Any lease you hand out (a refresh lease, a worker lease) must carry a generation number,
and a completing worker must be rejected if its generation is not the current one.
Otherwise a SLOW worker completing late overwrites a NEWER result. On this build a slow
PASS overwrote a newer quarantine.

**Back the generation with a database SEQUENCE, not a row counter.** A row counter resets
to 1 on a TRUNCATE or restore, and a stale generation-1 worker then collides. A sequence
survives a TRUNCATE of the lease table, which is the case that actually bit this build.

**A sequence is better, not bulletproof.** A restore from backup, or a rebuilt instance,
resets it too. If your recovery story includes restoring the database while workers may
still be alive, pair the generation with a durable EPOCH (an instance or restore id bumped
on every restore) and fence on `(epoch, generation)`. Alternatively, document a restore
protocol that makes pre-restore workers unable to reconnect at all (rotate the credential
as part of the restore). Pick one and write it down; do not leave it implicit.

**A per-window lease is NOT execution serialization.** It serializes CLAIMS within a
cadence; a job running LONGER than a cadence still races. You need the fence as well.

### 6. Duplicate-text exclusion with a real window

Enforce it in the database, not in application memory. The proven rule is an exact
duplicate-text exclusion over a rolling seven-day window, so a re-captured story cannot
produce the same post twice.

### 7. Append-only history

Publication and event history are append-only. Recovery audit rows are immutable. A state
machine you can rewrite is a state machine that cannot be audited after an incident.

## Idempotency identity: what goes in the key, and what must NOT

The single most expensive class of bug on this project. Twice.

**Name your identities separately. There are at least four and they are not the same key.**

| Identity | Hashes | Never includes |
|---|---|---|
| source version | the source's stable id (canonical URL or object id) PLUS the normalized body | when you fetched it |
| claim | the source version it rests on PLUS the claim's own content | when you extracted it |
| delivery key | account, action kind, target identity, and the canonical request projection | anything per-attempt |
| attempt token | per attempt, unique, random | (it is not content-derived at all) |

"Hash the content" alone is wrong and will collide: two authors can post identical text,
one article can appear at two URLs, and the same sentence can be a claim about two
different events. **Stable object identity goes IN the hash; acquisition time stays OUT.**

**The timestamp rule, stated precisely.** If your identity check includes a wall-clock
timestamp (`recorded_at`, `retrieved_at`, `extracted_at`), then a retry of the same work
computes the same id with a different timestamp, and the store refuses it as a conflicting
reuse. The retry can then NEVER succeed. Two migrations were needed on this build to remove
timestamps from two different identity checks. Keep the timestamp as an ATTRIBUTE of the
row (first-seen time is genuinely useful); just keep it out of the identity comparison.

**Corollary: normalize before you hash.** Deriving a version id from raw bytes made a stable
article mint a brand new version on every fetch, because page chrome (scripts, tokens,
timestamps) changed every time. Result: a re-extraction on every poll, real money spent,
and genuinely fresh stories stranded behind the churn. Hash the NORMALIZED visible body;
keep the raw hash in capture metadata for forensics.

**Corollary: the in-memory implementation and the durable implementation must agree.** The
same identity bug existed in both a SQL function and an in-memory store that compared whole
dataclasses. Fix them in the same commit or your local tests and production disagree.

## Recovery is the dangerous half

- **The chain must follow the STORED head, not the computed one.** If an item's version
  supersedes a predecessor that was never stored (because an earlier extraction failed),
  the chain jams permanently. Resolve `supersedes` to whatever the store actually holds as
  head, and drop it from the identity check. That self-heals on the next capture.
- **Put a freshness fence in FRONT of the expensive work.** Skip an item whose source version
  is not the current head BEFORE spending budget or calling the model. This both prevents
  out-of-order head reversal and makes a poisoned backlog fail cheaply. On this build a
  612-item poisoned backlog was made harmless by exactly this.
- **Do not take the "reject when a head already exists" alternative** that reviewers will
  propose. It reintroduces a jam that never self-heals. Resolve-to-head plus a publish-time
  source gate is strictly better.
- **Know which failures are retryable, and map every internal outcome onto a DECLARED
  state.** On the reference build a budget-stop failure ended `failed` (retryable, nothing
  spent) while a publish-time block (global kill, unverified identity, expired contract)
  ended in that system's own terminal, immutable outcome. In this vocabulary that outcome is
  `parked`: the machine is finished with it and only a human can move it. A plan of "let it
  block, then fix and retry" was therefore a permanent kill of the exact item it needed.
  Write the retryable-versus-terminal table down before planning a run, and make sure every
  internal outcome name in your codebase maps onto one of the six declared states. An
  outcome that has no declared state is a state you cannot reason about.
- **A recovery tick fires the whole backlog the moment you raise a cap.** See
  /programmable-account-policy.

## Verification: prove it on a real database

Contract-harness receipts and adapter matrices do not prove any of this. The proof lane is
a REAL ephemeral database instance, replayed from migration 1, running the concurrency
cases:

- atomic attempt creation and restart protection
- before-byte authorization
- pre-authorization stale-worker rejection
- post-authorization recovery REFUSAL
- indeterminate reconciliation, exactly once
- exact duplicate-text exclusion at the window edge
- request-hash binding
- append-only history, unique delivery keys, unique attempt tokens
- fenced recovery: worker A claims generation 1 slow, worker B claims generation 2, A's
  late write is rejected
- `retry()` on a `failed` intent creates ZERO rows by itself, and the following `begin()`
  creates EXACTLY ONE attempt, carrying the unchanged delivery key and a new attempt token
- retry from any state other than `failed` is rejected
- attempt-cap exhaustion parks the intent instead of looping

**Give every concurrent agent or reviewer its OWN test database.** Two background reviewers
sharing one test database produced 18 phantom failures that were nearly chased as real bugs.

**Mutation-test every guard, at the layer the guard lives in.** Delete the guard, confirm
the test goes red, restore. This caught two tests that proved nothing: one varied two
dimensions so a deleted term was masked, and one tested a pure planning function while the
actual fail-open lived in the caller.

## Checklist

- [ ] Delivery intent and attempt are SEPARATE rows; `begin()` is the ONLY creator of attempts
- [ ] Retry re-opens the intent and creates no row itself; the next `begin()` appends one attempt
- [ ] Delivery key includes action kind and the canonical request, so zero-text verbs do not collide
- [ ] `failed` is the only retryable state; `indeterminate` never is
- [ ] Attempt cap defined, and exhaustion parks rather than loops
- [ ] Attempt row written durably before any byte
- [ ] Final before-byte authorization, re-checking every pre-flight condition
- [ ] Unknown outcomes are a real state; a failed lookup resolves nothing and never means not-sent
- [ ] `authorized` is a durable state with a lease; lease expiry moves the row to indeterminate
- [ ] Pre-auth stale workers rejected; post-auth workers never auto-recovered
- [ ] Transport library auto-retry explicitly disabled and asserted in a test
- [ ] Read-back verification of the canonical text
- [ ] Fencing generation backed by a sequence, plus a restore epoch or a documented restore protocol
- [ ] Four identities named separately; the three CONTENT-DERIVED ones include stable object
      identity and exclude acquisition time (the attempt token is random by design)
- [ ] In-memory and durable implementations share the identity rule
- [ ] Chain resolves to the stored head; freshness fence before expensive work
- [ ] Retryable vs terminal failure table written down
- [ ] Proven on a real ephemeral database, mutation-tested, one database per agent
