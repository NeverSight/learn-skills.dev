---
name: java-backend-api
description: HTTP contract rules for a Java backend on Spring Boot Web MVC. Load before adding or changing an endpoint, a request or response field, a list or paging parameter, an error shape, a cursor or the API version, and before wiring the contract's generation, lint, diff or fuzz gates.
---
# Java backend — the HTTP contract rules

These rules govern the HTTP contract of a Java backend on Spring Boot Web MVC: the committed OpenAPI document, errors, lists and paging, wire temporals, request bodies, versioning and concurrency on the wire. Each directive is a `###` heading, and that heading is its citation — *the single conformance oracle*, *the keyset pager*, *the PATCH ban*. There are no rule ids, deliberately: nothing in this skill set numbers these rules, so an invented number resolves only for a repo that installed this skill, while the skill name plus the subject resolves either way.

## The premise

**The code is written by LLM agents, and no human reads it line by line.** This skill adds one condition: **the backend exposes an HTTP API described by an OpenAPI document.** Both halves are load-bearing. A verdict is portable exactly as far as its premise: in a repo where a human reviews every endpoint diff, the regenerate-and-diff gate and the error-catalog snapshot drop from mandatory to merely useful.

The contract is machine-read. No human reads the generated handlers, and the committed document is the only place a contract change becomes visible. That is why this area has its own gates, not a review convention.

One more condition applies to exactly one directive, and is stated there: the breaking-change diff binds only where the contract crosses the build boundary — where a consumer that is not rebuilt in the same pull request binds to it.

**Without an OpenAPI document, what goes dormant is the set of gates, not the set of rules.** [gates.md](gates.md) lists which gates go dormant and which stay live; know the split before working in such a repo.

## When to read which file

| When you are about to | Read |
| --- | --- |
| add or change an endpoint | [contract-document.md](contract-document.md) and [errors.md](errors.md); also [lists-and-paging.md](lists-and-paging.md) if it returns a list, [request-bodies.md](request-bodies.md) if it takes a body, [concurrency.md](concurrency.md) if it updates a resource, and *Wire temporals*, below, for a time or date field |
| wire or change the document's generation, normalizer or conformance-fuzz gate; add or change the API version; change a released contract; choose the HTTP method of an update | [contract-document.md](contract-document.md) — *The document*, *Versioning and change* |
| add or change an error shape, an error code, or the refusal of any input — a body member, path variable, query parameter or header | [errors.md](errors.md) — *Errors*; for a body member, also [request-bodies.md](request-bodies.md) |
| add or change a list or paging parameter, a cursor, a list response or a sort | [lists-and-paging.md](lists-and-paging.md) — *Lists and paging*; [errors.md](errors.md) for a refused query parameter |
| add or change a request body, a request field or request type, a create or update operation, or the body size limit | [request-bodies.md](request-bodies.md) — *Request bodies*, and [errors.md](errors.md) for the entry each refusal is recorded in |
| add or change a response field | [contract-document.md](contract-document.md) — *Breaking-change diff where a contract crosses the build boundary*; *Wire temporals*, below, for a time or a date; *What is here and what is elsewhere* for a decimal |
| write an update's version-column guard, an `ETag` or `If-Match` handling | [concurrency.md](concurrency.md) — *Concurrency on the wire* |
| wire the contract's generation, lint, diff or fuzz gates, or work in a repo with no OpenAPI document | [gates.md](gates.md) — *Wiring the gates*, and the check line of each directive a step wires, in the file listed above for its subject |
| add or change a request or response field that holds a time or a date | *Wire temporals*, below |

A reference file whose directives have named gaps ends with them. An unwired gate is a rule described as enforced that is not: wire the gates in the first pull request that exposes or changes the HTTP contract.

## What is here and what is elsewhere

This skill is one of three for this stack. A repo exposing an HTTP API installs all three:

- **`java-backend-rules`** — the platform rules: persistence, the transaction seam, the concurrency model, the runtime-silent ban list, the test toolchain. **Install it with this skill**: several directives here are built in the shape of a rule there — the codegen-diff job, the ArchUnit predicate style, the excluded generated packages — and the rules listed in *Wiring the gates* step 5 are ArchUnit bans hosted on that skill's ban-list test class.
- **`java-backend-observability`** — logging, metrics, alerting, including the rule that makes an error response's correlation id retrievable (below).

What a reader will look for here and not find:

- **The rule that every decimal-valued field on the wire is a string** — rates, percentages, FX factors, not only money — **is `M-15` in `money-api`. There is no general directive for it here.** A repo that installs this skill and not the money skills has no decimal-string rule at all, including for a rate or percentage field that carries no money. The rules deciding the wire form of a decimal are filed under money, and so is the widening to every decimal field. A repo with a rate field and no money feature states the rule in its own text and owns it there.
- **Money-path refinements of two directives.** The conformance-fuzz gate's money edge cases are `M-19` in `money-api`. The conditional-request precondition becomes **required** rather than merely honored on a money-path mutation — `M-18` there, which reuses the version column of *The guarded version-column update* and says explicitly that a repo with no general rule of that kind must state one. **This skill is that general rule.**
- **The correlation id's other half.** *One advice builds every error body* requires the generic internal problem to carry only a correlation id. That is a dead end unless the id retrieves a log event, and the rule requiring that is in `java-backend-observability`, not here.
- **The storage half of immutability.** That a business number is never renumbered, and has no update path outside issuance, is `business-numbering`'s rule, restated in `primary-keys`. **This skill carries only the wire half**: a field that never changes is absent from every update body — *Request bodies*.

## The defaults these rules override

These are the picks an unbriefed agent statistically makes. **Naming the loser is the load-bearing half.**

- **Offset and page-number pagination** — the corpus-default paging. Rejected: under concurrent inserts and deletes between page fetches it silently skips and duplicates rows, giving a wrong but plausible page that no reader catches. Keyset with a unique final tiebreak has no such anomaly. Page-number paging is offset internally and loses the same way.
- **`PATCH` with JSON Merge Patch** — the corpus-default partial update. Rejected: the standard gives a `null` member the meaning *delete this field*, so a merge-patch body silently drops a field instead of setting it.
- **Tolerant reading of request bodies** — Spring Boot's own default (its Jackson auto-configuration disables `FAIL_ON_UNKNOWN_PROPERTIES`) and the robustness principle behind it. Rejected: a member the request type does not declare is dropped, the answer is 200, and the client's instruction — a misspelt field, a field the server never had — is lost with nothing recording it.
- **Last-wins on a repeated member** — Jackson's default: `StreamReadFeature.STRICT_DUPLICATE_DETECTION` off, so `{"name":"a","name":"b"}` binds `b` and the answer is 200. Rejected: two values for one field is a contradiction, and the value kept may be the one the caller did not mean, with nothing recording the other was sent.
- **Prose, or nothing, for an input outside the body** — Spring's `detail` for a path variable, query parameter or header that does not convert, which quotes the value sent; axum's plain-text rejection; an undeclared query parameter ignored, a repeated one resolved first-wins, a UUID trimmed and parsed leniently. Rejected: no machine-readable entry names the input, and a misspelt or doubled parameter is answered 200 under a value the caller did not mean.
- **No request-body limit** — Tomcat's `maxPostSize` limits form parameters only, Jackson's `maxDocumentLength` is unlimited by default, and axum's 2 MB `DefaultBodyLimit` binds axum's own extractors only. Rejected: a reader that buffers the body holds whatever arrives.
- **Echo the identifier, refuse a mismatch** — the update body carries the path's identifier, or a field that never changes, and a coded 409 (`*-immutable`) refuses a differing value; often reached by reusing one request type, or the whole representation, as the `PUT` body. Rejected: one value arrives through two channels, the contract grows a refusal for a request no client should be able to send, and the shape spreads by analogy to every later resource. What a spec's "an attempt to change it is refused" needs is the field's absence plus strict reading.
- **A header or date versioning pipeline** — the corpus-admired scheme, the one Stripe is famous for. Rejected: it selects the applied contract per request from ambient input and rewrites the response back through runtime version-change modules — a runtime-silent transformation — and the version never appears in the committed contract, which defeats regenerate-and-diff. URL-major versioning keeps each version a diffable committed file. A second scheme, GitHub's, is date-and-header-versioned too but ships separate dated contracts with no transformation modules; it is not the shape rejected.
- **Code-first with no committed document** — introspect the running app, serve the spec live, commit nothing. Rejected: with no committed artifact there is no diff to gate and no stable oracle for the fuzzer. The pick is code-first generation *with* a normalized document committed and diff-gated.
- **Response envelopes and HATEOAS** — a `{data, meta}` wrapper, `_links` hypermedia. Rejected: the absent human reader changes nothing about their stakes, so neither earns a place under this premise, and both add surface an agent must keep consistent for no machine-enforced payoff. The list shape is a flat `{items, nextCursor}`; navigation is the cursor, not embedded links.
- **Free-form error JSON** — ad-hoc `{error: "..."}` bodies per endpoint. Rejected: a machine consumer and model review cannot adapt to divergent shapes the way a human would. The contract is one problem shape through one advice, with a stable machine code.
- **Integer minor units for money on the wire** — Stripe and Adyen style. Rejected: it exports exponent arithmetic to every consumer, and a mishandled exponent is a silent 10× or 100× error; exponents vary by currency, and processor tables deviate from the ISO register — Adyen for CLP, CVE, IDR and ISK, PayPal for HUF. The directive deciding this is not here: it is `M-12` in `money-api`, and the widening to *every* decimal field (not only money) is `M-15` there. See *What is here and what is elsewhere*.

## Wire temporals

### Instants on the wire

**Instants on the wire are RFC 3339 date-times, serialized in UTC with the `Z` designator, and their field names end in `At`.** The wire type is `java.time.Instant` through one pinned time module, so a non-UTC offset and an epoch-number timestamp are both unwritable. Numeric or epoch time never appears.

*Bespoke — the pinned serialization time module plus a serialization test. **Confirmed** 2026-07-25: RFC 3339 date-time carries a mandatory offset, and `Z` means UTC; JSON numbers are exact only within roughly ±2^53.*

### Business dates on the wire

**Business dates on the wire are strict `uuuu-MM-dd`, and their field names end in `Date`.** The wire type is `java.time.LocalDate` parsed strictly, so a value carrying a time component fails to parse and returns 400 — a datetime is never silently narrowed to a date across time zones.

*Off-the-shelf — strict `ISO_LOCAL_DATE` on a `LocalDate` field rejects trailing text, the stack maps the parse failure to 400, and a deserialization test pins it. **Confirmed** 2026-07-25 for the rejection; the 400 comes from the Spring and Jackson stack, not from `java.time` itself. The `uuuu`-versus-`yyyy` era rationale is **uncertain**.*

### Temporal naming and declared format agree both ways

**Lint the committed document so that `format: date-time` implies a name ending in `At` and a name ending in `At` implies `format: date-time`, and the same for `format: date` and a name ending in `Date`.**

*vacuum lint — off-the-shelf host, bespoke ruleset. **Convention**, 2026-07-25. The lint governs the contract's internal consistency, not runtime strictness: in JSON Schema 2020-12 `format` is an annotation, not an assertion, by default, so runtime strictness comes from the typed parser above, never from the `format` keyword. Reading a green format lint as runtime validation is this rule's specific misreading.*

## Named gaps — where no check reaches

Silence reads as coverage, so each gap is stated. The gaps of the directives in each reference file are at the end of that file.

1. **No decimal-string directive exists in this skill.** The rule covering every decimal field is filed under money, so a repo with a rate or percentage field and no money feature is uncovered by this skill set — see *What is here and what is elsewhere*. The rejected-alternatives record for this stack asserts that the contract rules extend the string-decimal choice to every decimal field; the general contract directives do not carry that rule.

## Markers, dates, and what they mean

Confidence, per claim:

- **confirmed** — normally, the claim survived three independent refutation votes against primary sources on the stated date. **No vote was ever cast in this area**: here it is the pass's own usage, carried rather than re-marked, and means checked against a published standard or vendor documentation by one researcher. Read the gap between it and *primary-source verified* as source quality, not scrutiny.
- **primary-source verified** — one researcher checked the claim against a primary source, no panel.
- **convention** — the research did not, or could not, confirm the claim from independent sources; the rule is kept because it is enforceable, cheap and fails toward safety.
- **uncertain** — the claim was examined and left unsettled; nothing here rests on one.

Enforcement, per rule: **off-the-shelf** — a tool does it with configuration; **bespoke** — the check must be written; **convention** — a human or agent asserting it is all there is.

**Marker ceiling.** Every directive comes from one pass, 2026-07-25, one researcher against primary sources and no panel, except *Request bodies* (2026-09-25, from one observed failure with no research pass, amended 2026-10-07 by an owner's decision, *A member given twice is refused*) and four directives decided later that day — *A refusal names its input*, *A refused input gets one code wherever it travels*, *An undeclared member's refusal lists the members allowed*, *A request body has a size limit* — on one researcher's primary-source reads and one canaried hostile audit, no vote. Tool facts are well sourced and policy choices are not: rejecting an over-cap `limit`, banning `PATCH` repo-wide and snapshotting the error catalog are this rule set's calls, marked convention, and each deliberately overrides a framework or industry default; read the marker beside a rule before treating it as settled.

Status tier: **decided, not yet validated** — researched and decided, with no production use yet behind the enforcement shapes. *Request bodies* holds the same tier on different ground: decided from a failure, not researched, and its enforcement shapes have been built and run in one service repo, not in production — except the duplicate-member refusal, built and run in both templates and in no service repo yet, and the four directives of 2026-10-07 later, built and run in both templates that day and ported to one service repo, in production nowhere.

**Lapse rule:** past `review-by` **2027-01-21**, every *confirmed* marker here reads as *convention* until a new pass re-dates it. No maintainer action is needed.

The ground behind each claim, with its source, the claims that must not be cited, and the conditions that reopen a rule are in [evidence.md](evidence.md).
