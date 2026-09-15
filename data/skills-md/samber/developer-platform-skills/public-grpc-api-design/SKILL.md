---
name: public-grpc-api-design
description: Design a public gRPC surface for external developers - the when-gRPC-at-all gate (most platforms keep gRPC internal and publish REST or transcoded JSON), AIP proto package and versioning conventions, buf breaking-change gates and their google.api.http blind spot, unary-by-default streaming decisions, the google.rpc.Status error model with its HTTP-mapping traps, transcoding and gateway architecture (Connect-RPC, grpc-gateway, Envoy), and external auth and TLS. Use whenever the user mentions gRPC, protobuf or .proto files, buf, Connect-RPC, grpc-gateway, or gRPC-JSON transcoding at a public edge - even if they never say "gRPC API design". Design layer only, not language-specific server implementation.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Public gRPC API Design

You are a public gRPC surface designer. Decide whether gRPC belongs at a platform's public edge at all, and - when it does - design the proto governance, streaming posture, error model, transcoding architecture, and external auth that let developers you have never met consume it safely.

The framing question is never "how do we design the best public gRPC API" but "does this workload belong on public gRPC, and through what edge". Sibling `samber/developer-platform-skills@api-integration-surface-strategy` partially owns that umbrella decision; re-ask it here anyway, because teams arrive having assumed "public gRPC" without validating it.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Does gRPC already run internally, or is this greenfield? If internal: the service definition likely contains admin/debug/monitoring RPCs never designed for external eyes - that is what makes step 7's closing exposure audit mandatory rather than optional.
2. Who are the external consumers: engineers wiring up your generated SDKs (control-plane/infrastructure audience), raw-proto integrators generating their own stubs, or browser-based clients? (drives the step 1 gate and the step 6 menu)
3. Do browser clients need to call this surface directly? Browsers structurally cannot speak gRPC's HTTP/2 framing - a yes deletes raw public gRPC from step 6's menu.
4. Does a public REST surface already exist, and must the gRPC surface stay consistent with it (same resources, same versioning story)?
5. Is any workload genuinely streaming-shaped (push, tail, telemetry ingestion), or is "streaming because gRPC has it" the only driver? (drives step 4)
6. Re-rank inputs: by when must the surface ship, is this a one-off exposure or a contract several products will share for years, and what is the effort ceiling (team hours, new runtimes you may operate, appetite for consumer-visible migration)? (re-ranks step 6's menu)

If your harness has persistent memory, store the design's settled decisions (the gate's verdict and its trigger, proto package and version scheme, streaming posture, chosen transcoding rung with its promotion condition, auth flow per caller type) so later runs - a new RPC, a proto review, the docs pass - start from the design instead of re-deriving it.

## Consumer types

The split that changes the design is how the consumer meets the contract:

- **SDK-mediated consumers** - engineers using your published, generated client libraries (Temporal's model: protos on GitHub and a schema registry, SDKs wrapping gRPC directly). The one audience for which raw public gRPC is a proven fit; they absorb stub regeneration as normal tooling.
- **Raw-proto integrators** - third parties generating their own stubs from your protos. They inherit every breaking change directly, need `protoc`/buf fluency you cannot assume, and debug binary payloads with tooling most do not have installed. Proto governance (steps 2-3) is designed for them.
- **Browser and generic HTTP clients** - cannot speak gRPC's raw HTTP/2 framing at all, so a proxy layer is mandatory the moment one of them is a consumer. They reach the surface only through transcoding, gRPC-Web, or Connect - step 6 exists for them.

Design for the least-equipped consumer type actually present. A surface only the SDK-mediated audience can use silently excludes the other two - that is a business-reach decision, not a technical default; make it consciously in step 1.

## Workflow

1. Run the when-gRPC gate - decide what the public edge actually speaks.
2. Set proto package and versioning conventions.
3. Install breaking-change gates - buf plus the annotation blind-spot check.
4. Decide the streaming posture, unary by default.
5. Design the error model on `google.rpc.Status`.
6. Choose the transcoding/gateway architecture (ranked menu).
7. Design external auth and TLS, and audit the surface for exposure.

Each step has a section below, in order.

## 1. The when-gRPC gate

Practitioner consensus favors dual-stack, not either/or: gRPC for internal service-to-service traffic where you control both ends, REST or transcoded JSON at the edge where you do not. REST still carries the large majority of public APIs per tracked estimates (roughly 83% in the most recent count). See [references/public-grpc-case-studies.md](references/public-grpc-case-studies.md) for the sourced detail and the precision caveats on each:

- Google dual-publishes: a REST facade plus native gRPC stubs where latency matters.
- Square, Dropbox, and Cloudflare run gRPC internally while their public developer surfaces stay REST-fronted.

Why REST wins the public edge by default - concrete mechanisms, not preference:

- Browsers cannot speak gRPC's raw HTTP/2 framing; a proxy layer is mandatory the moment any consumer is browser-based.
- Protobuf is binary: nothing to read in a network tab, and traffic inspection needs `grpcurl`-class tooling third parties rarely have.
- Every external caller pays the `protoc`/stub-regeneration cost that an internal fleet amortizes.
- Google Cloud's own engineering blog names the operational cost: gRPC in place of REST/OpenAPI leaves "much more limited opportunity to augment or remediate the API's behaviors in proxies, especially API management tools".
- gRPC services built internal-first carry admin and debug RPCs never audited for public discovery.

The genuine triggers that justify public gRPC anyway - all three worth checking, any one may suffice:

- Consumers are confirmed SDK-mediated or proto-fluent (question 2). Temporal.io is the clean named precedent: its Cloud Ops API is "an open source, public HTTP API and gRPC API", viable precisely because its audience is control-plane engineers already fluent in generated-SDK tooling - and even Temporal ships an HTTP API alongside.
- The workload is genuinely streaming-shaped, where REST would need polling or a separate WebSocket layer (validate against step 4's costs first).
- Performance is the measured bottleneck and consumers can absorb the client-tooling cost. Binary Protobuf is commonly cited at 3-11x smaller and 8-12x faster to serialize than JSON - vendor/blog benchmarks, directional only, never cite as exact.

When the gate says "gRPC inside, JSON outside", Google's Apigee team supplies the reach argument to put in the design doc: "not all developers are equipped or experienced enough to consume gRPC services. API providers would therefore risk missing out on a potential audience by limiting themselves to exposing gRPC services only." The gate's output feeds step 6: it decides which rungs of the transcoding menu are even in play.

## 2. Proto package and versioning conventions

A public proto package becomes part of every generated client's import path - convention mistakes here are breaking changes once external consumers depend on them. Google's AIP corpus is the closest thing gRPC has to a canonical public style guide; adopt it rather than inventing house rules:

- One proto package per API, ending in a major-version component (`example.library.v1`) - AIP-215.
- Directory structure mirrors the package exactly (`example/library/v1/`); never put the version in a filename (`v1.proto` produces bizarre generated imports) - AIP-191.
- Major version only - `v1`, never `v1.0` or SemVer minors - encoded in the package and mirrored as the first URI segment of the transcoded surface. `v1` means stable; `v1beta`/`v1alpha` are the pre-stable channels, and claiming beta functionality under `v1` is the review finding to flag - AIP-185.
- Model the surface resource-oriented (AIP-121): named resources, standard List/Get/Create/Update/Delete methods, custom methods only where a standard verb genuinely fails, with the `:verb` suffix.
- One dedicated `<Method>Request`/`<Method>Response` wrapper message per RPC, never a bare scalar or a shared message - a shared message ripples every field change across every RPC referencing it, and a wrapper can always gain optional fields without breaking wire compatibility.
- Field discipline as absolutes for a public surface:
  - Never reuse or renumber a tag.
  - `reserved` every removed field.
  - Every enum zero value is `_UNSPECIFIED`.
  - Prefer well-known types (`google.protobuf.Timestamp`, `FieldMask`, `google.rpc.*`) over hand-rolled equivalents.
- Set per-language package options (`java_package` and friends) so generated code stays idiomatic instead of leaking the raw proto path.

Boundary: sibling `samber/developer-platform-skills@api-versioning-policy` owns notice windows, sunset communication, and governance generics across paradigms. This skill owns how a version is encoded and enforced gRPC-natively - the package-suffix rule above and step 3's gates. A new major version must not depend on the previous one, and stable resources keep identical resource names across majors so a v2 client can address what a v1 client created.

See [references/proto-governance-reference.md](references/proto-governance-reference.md) for file-content ordering, the buf lint rule names that operationalize each convention, channel-based vs release-based version evolution, and deprecation mechanics.

## 3. Breaking-change gates

Protobuf's encoding only guarantees wire compatibility, not client-code compatibility (AIP-180's distinction) - so the gate must be tooling, not reviewer vigilance:

1. Run `buf breaking --against <main>` on every PR as a hard CI gate, plus `buf lint` with the STANDARD set. Default to the strictest rule category (FILE) for a public surface; it catches generated-import breakage that package-level checks forgive.
2. Know the traps the tooling catches that human reviewers miss:
   - A rename is semantically remove-and-add (always breaking).
   - Moving a field into or out of a `oneof` breaks generated Go stubs.
   - Moving a message to a different file breaks generated imports - the file path is part of the contract.
3. **The blind spot buf leaves open:** `buf breaking` does not inspect custom options like `google.api.http`, so a team can break its REST-facing URL/verb mapping while every proto gate stays green. Add a dedicated check: snapshot the annotation-derived HTTP surface (paths, verbs, body mappings) and diff it in CI, or contract-test the transcoded routes - a named failure mode, not a theoretical one.
4. Test both directions across a version boundary: old client against new server and new client against old server - "does the schema parse" is not "does the cross-version RPC succeed".
5. Promote to a Buf Schema Registry review flow once public surface area justifies a human backstop: a breaking push enters an approve/reject queue with a paper trail, the proto-native equivalent of a review-board gate. Teams not on buf can use Salesforce's `proto-backwards-compat-maven-plugin` against a checked-in `proto.lock`.

Deprecation is proto-native too: `deprecated = true` (available on messages, enums, enum values, and services) plus an AIP-192 comment saying why and what replaces it. Channel expectations differ sharply:

- Alpha may vanish without notice.
- Beta may be removed after a recommended 180 days deprecated.
- An in-place breaking change to a stable component is "an extreme course of action" reserved for security or regulatory necessity.

The notice windows themselves are `samber/developer-platform-skills@api-versioning-policy`'s territory.

## 4. Streaming posture: unary by default

gRPC's four call types are not equally priced on a public surface. Expose unary RPCs by default; every streaming method is a deliberate, recorded decision with its costs accepted - never a free feature.

- **Server-streaming** is the one streaming mode to reach for first when a push/tail use case is real: it maps cleanly onto SSE through a gateway and onto Connect's streaming encoding. Notifications, log tailing, progressive results.
- **Client- and bidirectional streaming** carry named costs for external consumers: Microsoft's own guidance warns that "replacing unary calls with bidirectional streaming for performance reasons is an advanced technique and is not appropriate in many situations".
  - A stream fails mid-flight after partial data, so every external SDK consumer needs restart/resume bookkeeping a unary retry never requires.
  - Retries stop being transparently client-library-managed.
  - Browsers cannot do client or bidi streaming over HTTP/1.1 at all - a protocol wall, not a tooling gap (Connect over HTTP/2 is the exception).
- Load balancing degrades under streaming: HTTP/2 multiplexing pins all of a client's streams to one backend for the connection's life under an L4 balancer. A public gRPC edge needs L7, HTTP/2-aware balancing, and client keepalive intervals set below the load balancer's idle timeout - concrete vendor timeout numbers in [references/public-grpc-case-studies.md](references/public-grpc-case-studies.md).
- AIP-127 requires an HTTP mapping for every RPC _except_ bidirectional streaming, which HTTP/1.1 cannot carry - so every bidi method also needs a documented non-streaming alternative, or it is invisible to the transcoded surface.

Enforce the decision, don't just document it: when the surface commits to unary-only, enable buf's `UNARY_RPC` lint category so a future PR cannot silently introduce a streaming method the gateway, SDKs, or transport cannot carry. Sibling `samber/developer-platform-skills@api-idempotency-retry` owns retry mechanics, deadline propagation, and backoff generics; this step only decides which call shapes the public contract offers.

## 5. Error model: google.rpc.Status mechanics

Sibling `samber/developer-platform-skills@api-error-design` owns taxonomy philosophy - code catalogs, message writing, retryability signaling. This step owns the gRPC-native mechanics and the two traps that bite public surfaces:

1. Use `google.rpc.Status`:
   - `code`: one of the 17 canonical codes.
   - `message`: developer-facing English, never localized user text.
   - `details`: typed extras from `google/rpc/error_details.proto` (`ErrorInfo` first, `BadRequest` for field violations, `RetryInfo` paired with `RESOURCE_EXHAUSTED`).
2. Return the most specific applicable code (`OUT_OF_RANGE` over `FAILED_PRECONDITION` when both apply). Defaulting everything to `UNKNOWN`/`INTERNAL` as a defensive habit is the named anti-pattern: it flattens every status dashboard into one bucket.
3. Sanitize outbound errors structurally, not just prose: `DebugInfo` is documented as internal-only - filter it from `details` before the response leaves; sanitizing `message` alone is insufficient.
4. **Trap one - the mapping table's direction.** The gRPC project's own documentation is explicit: "servers must not use this table to determine an HTTP status code to use... the mappings are neither symmetric nor 1-to-1." The canonical gRPC↔HTTP table exists for clients interpreting responses that arrived without a `grpc-status`; a gateway translating errors outward needs its own deliberate mapping, confirmed against the transcoding implementation actually in use.
5. **Trap two - HTTP collapses distinctions.** In the common gateway mapping, three codes (`INVALID_ARGUMENT`, `FAILED_PRECONDITION`, `OUT_OF_RANGE`) all land on 400, and `CANCELLED` maps to the non-standard 499. Document for consumers that the HTTP status line is lossy and the structured envelope in the body is the source of truth.
6. Verify the envelope survives your gateway:
   - Envoy needs `convert_grpc_status: true` _and_ every detail type present in the proto descriptor (missing types drop silently).
   - Connect serializes errors as JSON natively.
   - grpc-gateway's default handler flattens the message and drops `details` entirely - a custom error handler is mandatory there if structured detail matters.

Only `UNAVAILABLE` is generally safe to auto-retry without extra signal (AIP-194); everything else needs an explicit `RetryInfo` or caller judgment. The full 17-code table, gateway mapping, details catalog, and per-gateway survival mechanics are in [references/grpc-error-http-mapping.md](references/grpc-error-http-mapping.md).

## 6. Transcoding and gateway architecture

The design decision this step owns is what edge serves non-gRPC consumers and how the mapping is expressed - AIP-127's `google.api.http` annotation is the convention every implementation converged on ("APIs must provide HTTP definitions for each RPC except bi-directional streaming RPCs"). The menu, ranked:

- effort: `raw public gRPC edge > grpc-gateway == Envoy transcoder > Connect-RPC`
- value: `Connect-RPC > Envoy transcoder > grpc-gateway > raw public gRPC edge`
- efficiency: `Connect-RPC > Envoy transcoder > grpc-gateway > raw public gRPC edge`

Effort here is what the team operates and regenerates; value is audience reached per proto contract, with error and streaming fidelity preserved. The `grpc-gateway == Envoy` effort tie is genuine: regenerating a Go proxy on every proto change and keeping a descriptor set plus filter config in sync are different work at the same order of magnitude - and "you already run Envoy" is exactly the condition that breaks it.

- **Default rung: Connect-RPC.** One server speaks Connect, gRPC, and gRPC-Web:
  - No proxy required.
  - Browsers served natively.
  - Full streaming over HTTP/2.
  - Errors are JSON out of the box.
  - Wire-compatible with gRPC (validated against Google's interop suite).

  Entered CNCF Sandbox in April 2024, already in production at CrowdStrike, PlanetScale, RedPanda, Chick-fil-A, Bluesky, and Dropbox. Buf's framing when launching it: "conceptually, the gRPC protocol is HTTP with Protobuf-encoded bodies" - Connect collapses the pick-a-gateway decision for most new surfaces.

- **Promote Envoy's gRPC-JSON transcoder** when Envoy is already your mesh data plane and a second runtime is the real cost - descriptor-driven, no generated glue code, the common approach in Kubernetes environments. Not because Envoy is inferior; "you already operate this" is a legitimate reason.
- **Keep grpc-gateway** where an existing Go investment already carries it with a custom error handler; it pays a codegen step plus a double JSON↔protobuf parse on every request, and its default error handling is the weakest of the three (step 5.6).
- **Raw public gRPC edge is the starved option:** highest fidelity (binary end-to-end, full streaming, zero transcoding loss) and highest effort (a gRPC-aware edge with L7 balancing, WAF, and TLS termination - Cloudflare ships this as a product - plus a full internal-RPC exposure audit and every consumer bearing Protobuf tooling). It loses every efficiency round; the one condition that promotes it anyway is step 1's Temporal trigger, a confirmed SDK-mediated, control-plane audience. Even then, dual-publish an HTTP surface alongside, as Temporal does.
- **Ruled out, not demoted:** raw public gRPC as the _only_ surface when question 3 said browser clients call directly. Browsers structurally cannot speak gRPC framing; keeping the option parked at the bottom of the menu silently reappears as scope. Delete it and choose among the three above.

This ranking is a default, not a law. Re-rank against question 6 and what you know about the team:

- An Envoy-fluent platform team gets the transcoder nearly free.
- A hard ship date promotes whatever the team already operates.
- A contract several products will share for years weighs error-fidelity (value axis) over this quarter's effort.

Performance-critical consumers should be steered to native gRPC or Connect's binary mode regardless of rung - every JSON-transcoding path pays a real parse cost.

Mechanics table (streaming support, browser path, proxy requirements per option) and sourced quotes: [references/public-grpc-case-studies.md](references/public-grpc-case-studies.md).

## 7. External auth, TLS, and the exposure audit

The internal-auth instinct is the wrong one: mTLS authenticates _workloads_ and scales fine inside a mesh, but issuing and revoking client certificates for developers you have never met is operationally impractical. The public edge authenticates apps and users instead - the mesh does not disappear; it starts one hop further in. Order of operations:

1. TLS first, non-negotiable: credentials travel as gRPC metadata, plaintext without transport security; most implementations refuse to send credentials over an unencrypted channel at all.
2. OAuth2 flow by caller type: Client Credentials for machine/service callers, Authorization Code + PKCE where a human authenticates interactively. Token as `authorization: Bearer <token>` metadata, validated in a server interceptor.
3. Token mechanics:
   - JWT as token format, strongly signed (RS256), with expiry claims.
   - Token introspection against the authorization server, cached so it does not tax every call.
   - An established identity provider over a hand-rolled issuer once external caller count justifies it.
4. Enforce scopes at the method level - not "is this caller authenticated" but "is this token scoped for this RPC".
5. API keys complement, never replace, authentication (Google's own Endpoints distinction): a key identifies a project/consumer for quota attribution and coarse gating, not an authenticated identity.
6. Rate limiting signals over-quota with `RESOURCE_EXHAUSTED` (429 once transcoded) paired with a `RetryInfo` detail so callers back off instead of hammering the same limit.
7. The exposure audit, mandatory for any internal-first service: disable server reflection in production (it is an API-discovery tool for attackers once the port is public), then enumerate the full method surface for admin, debug, and monitoring RPCs that were never designed for external visibility. TLS and auth switched on do not close this hole.

The reference architecture to diagram: TLS termination + token validation + per-method authZ + rate limiting at the public gateway (Apigee, Cloudflare, Envoy are named vendor instances), fronting the internal mesh where mTLS resumes.

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- The server or gateway derives HTTP status codes from the client-side gRPC↔HTTP mapping table the gRPC project explicitly forbids servers to use.
- `buf breaking` green while a `google.api.http` annotation change broke the public REST mapping - the blind spot with no dedicated check.
- grpc-gateway in production with the default error handler, silently dropping every `details` payload.
- Server reflection enabled on a publicly reachable service.
- Two RPCs sharing a request or response message; a bare scalar as a request type.
- A version number in a proto filename, or a directory that does not mirror the package.
- A streaming method added to a browser-facing surface with no non-streaming alternative and no recorded tradeoff decision.
- Everything failing as `UNKNOWN` or `INTERNAL`; `DebugInfo` reaching external callers.
- An L4 balancer in front of streaming RPCs, pinning every client's streams to one backend.
- Client keepalive interval longer than the load balancer's idle timeout, so the balancer drops connections before keepalive fires.
- Beta functionality shipped inside a `v1` package.

## Measurement

Pass gates, self-set from the sourced rules above (no industry-standard thresholds exist for this surface; each gate is binary and auditable):

- Breaking-change gate: zero breaking proto changes reach the default branch outside a new major version - `buf breaking` (FILE category) green in CI on 100% of merges.
- Annotation coverage: 100% of RPCs carrying `google.api.http` annotations covered by a dedicated mapping diff or contract test, because buf does not check them.
- Streaming discipline: `UNARY_RPC` lint enabled on a unary-only surface, or every streaming method paired with a recorded accepted-tradeoff decision and (for bidi) a non-streaming alternative.
- Exposure: reflection disabled in production and the internal-RPC audit completed before launch - both binary.

Iterate the design until all four pass. Afterwards, watch as trends (not thresholds): the share of support tickets caused by transcoded-error confusion, and cross-version compatibility test results per release.

## Invocation examples

- "Our platform team wants to expose our internal gRPC services to partners - design the public surface and tell us whether that's even the right move."
- "Design proto package and versioning conventions for a public API we'll publish protos for, with CI gates against breaking changes."
- "We're putting Connect-RPC in front of our gRPC backend for browser clients - review the error model and the transcoding architecture."
- "Audit this gRPC service before we open it to external developers."

## References

- [references/proto-governance-reference.md](references/proto-governance-reference.md) - AIP file/package rules in detail, buf lint rule names, AIP-180 compatibility traps, channel vs release versioning, deprecation mechanics.
- [references/grpc-error-http-mapping.md](references/grpc-error-http-mapping.md) - the 17 canonical codes, the full gateway HTTP mapping with its collapse points, the error-details catalog, and per-gateway envelope-survival mechanics.
- [references/public-grpc-case-studies.md](references/public-grpc-case-studies.md) - Google, Square, Dropbox, Cloudflare, Temporal case studies with precision caveats; the transcoding-option mechanics table; Connect-RPC adoption facts; load-balancer keepalive numbers.

See also, same collection:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella decision of which surfaces to offer at all; this skill re-validates its gRPC branch and executes it.
- `samber/developer-platform-skills@public-api-design-review` - whole-surface consistency review for the REST/JSON side; it hands gRPC-specific design here.
- `samber/developer-platform-skills@public-graphql-api-design` - the structural analogue for a public GraphQL surface; same gate-first shape, different paradigm.
- `samber/developer-platform-skills@api-versioning-policy` - notice windows, sunset communication, and governance generics; this skill owns only the gRPC-native version encoding and gates.
- `samber/developer-platform-skills@api-error-design` - error taxonomy philosophy, message writing, retryability signaling; this skill owns only `google.rpc.Status` mechanics and the HTTP-mapping traps.
- `samber/developer-platform-skills@api-idempotency-retry` - client retry mechanics, deadline propagation, and backoff generics consumed by step 4's streaming decision.
