---
name: surface-recon
version: 0.8.0
description: "Map an authorized target into evidence-backed contracts and produce a recon report an implementer can build from. Use for web or mobile APIs, login portals, desktop apps, CLIs, SDKs, MCP servers, local daemons, file and project formats, USB/BLE/serial/HID devices, firmware packages, runtimes, and accelerators. Trigger when the user says recon, reverse engineer, map the interface or protocol, inspect an undocumented integration, discover what a device actually supports, or wants to build a client, CLI, MCP, SDK, adapter, or compatible implementation before its contract is verified."
---

# surface-recon

Map what a target exposes, what it demands of you, and what will bite you. Produce a report someone else can build from without repeating your work.

This skill investigates. It does not design a command surface or write code: that is `cli-build`'s job. Stopping at a report is the point: recon tells you whether building is worth it.

## The one rule

**Every claim in the report is either observed or labeled as unverified.** A recon report that guesses without saying so is worse than no report, because the implementer trusts it and loses a day. Mark inference as inference.

Concretely: an evidence row states its plane, claim, provenance, acceptance proof, and receipt. Anything inferred names the exact step that would verify it.

**Open `recon/friction.md` before Phase 0 and append to it as you go.** Every time a playbook is thin, a command fails for a reason its help text did not predict, or a gate does or does not hold, that is one line written at the moment it happens. It ships with the report and it is the only input that improves this skill. See [friction-log.md](references/friction-log.md).

## Instrument router

Choose instruments after classifying the plane. A target can expose several planes, and each plane needs its own evidence.

| Plane | Start with |
|---|---|
| Network or web UI | Official specs, then `agent-browser` capture and independent replay |
| Desktop or mobile UI | Screenshot and accessibility, then network, logs, and disposable artifacts |
| CLI, SDK, MCP, daemon | Help or schema enumeration, controlled calls, exit/status and state fixtures |
| File or project format | Real samples, metadata, schema inference, normalized round-trip |
| USB, BLE, serial, HID | OS enumeration, descriptors, passive capture, differential sessions |
| Firmware | Official update packages, hashes, extraction, trust-chain inventory |
| Runtime or accelerator | Accepted and rejected workloads, tracing, per-unit placement metrics |

For network and interactive browser planes, `agent-browser` ships version-matched guides. Load them rather than guessing commands from memory:

```bash
agent-browser skills get core           # the workflow: snapshot, refs, waits, sessions, mocking
agent-browser skills list               # what else is available
```

Two specialized ones carry most of the recon weight:

- **`derive-client`** turns a recorded session into a working client. For a website with an internal JSON API, it often does the whole of Terrain B better than hand-rolling: `agent-browser skills get derive-client`
- **`electron`** automates desktop apps over their debugging port, which beats unpacking them: `agent-browser skills get electron`

This skill deliberately does not restate what those cover. When a capability is documented there, [agent-browser-recon.md](references/agent-browser-recon.md) points at it instead of copying it, so the two cannot drift apart.

## When an instrument says the element is not there

**Screenshot first, and look at it with your own eyes.** If a page the user sees working reports "element not found", the capture comes before exhausting selectors, not after.

Three times in one project an indirect instrument said "does not exist" and the screenshot showed the element on screen: a login panel, a set of showtimes, a buy button. Each time the tooling was correctly built and pointed at the wrong thing. A login panel generates no traffic and contains no domain keywords, so it is invisible to a network tab and a DOM grep at the same time.

Two specifics worth knowing:

- **An open modal invalidates the entire accessibility tree.** A cookie banner returns as the whole snapshot, which reads as "the page has no content". Dismissing it is a precondition of any structural read, not a cleanup step.
- **Match on substrings, not equality.** A selector comparing against `19:20` finds nothing on a page rendering `19:20hs`.

The failure mode this prevents is not a missing tool. It is reaching for the instrument that represents you as someone who reads systems, over the one that answers the question.

## Phase 0: profile the terrain

Before touching an instrument, classify four dimensions. Read [terrain-model.md](references/terrain-model.md).

| Dimension | Values | Why it matters |
|---|---|---|
| Access | `public`, `owned`, `granted`, `blocked`, `mixed` | Defines authority and whether meaningful observation can start |
| Planes | `network`, `interactive`, `command`, `artifact`, `device`, `firmware`, `runtime` | Routes instruments and keeps evidence separated |
| Acceptance | `enumeration`, `replay`, `state-transition`, `contract-conformance`, `round-trip`, `receipt-plus-poststate`, `execution-placement`, `boot-and-recovery` | Defines what proves the claim |
| Maximum consequence | `passive`, `reversible`, `creative`, `persistent`, `destructive`, `external` | Defines approval, audit, cleanup, and recovery gates |

Record a profile before probing:

```yaml
access: owned
planes: [device, network, artifact]
primary-plane: device
acceptance: [enumeration, replay, receipt-plus-poststate, round-trip]
maximum-consequence: persistent
```

**Done when:** access is established, all currently visible planes are listed, each intended claim has an acceptance proof, and the run has a consequence ceiling.

Two profiles are traps worth naming up front:

**A complete official surface is the one to hope for.** Always search official docs, specs, schemas, manuals, and SDKs first. Skipping this check and going straight to observation is the single most common waste of time.

**Blocked access usually should not start.** Missing credentials, entitlement, physical possession, or authorization yields an inventory of unknowns, not a map. Say that before starting and name the exact unblocker. See [gates.md](references/gates.md).

## Phase 1: check for an official surface

Run this before anything else, every time. Official surfaces are not limited to HTTP:

1. Search `{target} API documentation`, `{target} developer docs`, `{target} OpenAPI`, `{target} SDK`.
2. Try the conventional spec paths directly: `/openapi.json`, `/swagger.json`, `/.well-known/openapi.json`, `/api/schema`, `/llms.txt`.
3. For command planes, run help, version, schema, tool/resource enumeration, and inspect the official SDK or protocol package.
4. For artifacts and devices, find file specifications, user and service manuals, descriptor definitions, update packages, and public protocol references.
5. Record versions. Official behavior can drift by app build, OS, firmware, silicon, or toolchain.

If you find a spec, read it and jump to Phase 4. Note the spec's own limitations: official docs are often incomplete rather than wrong, and the gap is what you need to reverse.

**Done when:** either authoritative material is in hand, or the searched queries and surfaces are written down so the report can say what was not found.

## Phase 2: observe real traffic

For every listed network plane, watch what it actually does. Skip this phase when no network plane exists.

**If it is a website with an internal JSON API, `derive-client` covers this phase end to end.** Record, identify endpoints among the noise, extract shapes and auth, verify. Run it:

```bash
agent-browser skills get derive-client
```

The commands for capture and interception live in `agent-browser skills get core`. What belongs here is only what recon adds on top:

- **Verify the domain you captured is where the functionality lives.** Institutional landing pages are not the app. Capturing `example.gob/agency` when the service runs on `service.agency.gob` produces a report full of nothing. This mistake happened three separate times in the corpus behind this skill.
- **Drive the actual action, not just the home page.** The endpoint you need appears when you click the thing, not on load.
- **Run each flow twice with different inputs.** Diffing the recorded URLs is what separates a parameter from a path.
- **Use a headed browser for first contact.** Anti-bot layers block plain `curl` and headless far more often than a real browser profile. Once you have a session, plain fetch usually works for the rest.
- **Keep the HAR, and treat it as a secret.** It is the receipt for every claim, and it holds live cookies and tokens. Out of version control, deleted when done.

**Then go past observation.** A HAR tells you what the client sent; it does not tell you what it depends on. Aborting an endpoint reveals which calls are load-bearing, and mocking a response reveals which fields are decoration. That is where recon stops guessing. See [agent-browser-recon.md](references/agent-browser-recon.md).

**Done when:** every network flow the implementer needs has been driven at least twice, each captured request is attributable to an action, an independent replay proves requirements, and secret-bearing evidence is stored outside version control.

## Phase 3: dig where traffic is not enough

Route each non-network plane to its acceptance boundary:

- **Introspection disabled on GraphQL** (403 on `__schema`): the schema is still in the client bundle. Grep the chunks for operation names and field selections.
- **Request signing or custom headers**: the algorithm is in the bundle. Find the function that builds the header, then **verify by replaying a signed request outside the browser**. A signing algorithm you have not replayed is a hypothesis.
- **Desktop app**: connect to it rather than unpacking it. Every Electron app exposes a debugging port, so its private API becomes observable with the same workflow as a web page (`agent-browser skills get electron`). Keep `asar list` and `strings` for what never runs: dead paths, embedded source layout, endpoints the UI does not reach.
- **Mobile app**: correlate owned UI actions with proxy traffic, app logs, local artifacts, and static package inspection. Authentication by Google or Apple is not permission to extract or reuse third-party tokens. Banking and financial mutations remain outside an observational recon unless separately and explicitly authorized.
- **React SPA**: `react tree` and `react inspect` give you the data model the client believes in, which is often cleaner than the API response. Needs `--enable react-devtools` at launch. **Check that the tree is not empty before relying on it**: a server-rendered app with few client components returns almost nothing, and a production build has mangled component names. It is a fast path, not a guarantee.
- **Client-held state**: before deobfuscating a bundle, `eval` the framework globals. Hydration payloads and public config are frequently right there.
- **CLI, SDK, MCP, or daemon**: enumerate commands, methods, tools, resources, schemas, exit/status behavior, error envelopes, and state changes. A listed operation is enumeration evidence; a controlled call plus its resulting state is conformance evidence.
- **Artifact**: inspect multiple real samples, optional fields, size, encodings, and version drift. Round-trip only through a disposable copy and compare normalized semantics rather than bytes alone.
- **USB, BLE, serial, or HID**: enumerate first, observe passively, correlate one human action at a time, then replay one known read. A transport write proves delivery, not command acceptance. Mutations require a protocol receipt plus coherent post-state. Use the context matrix and mutation ladder in [hardware-protocol-recon.md](references/hardware-protocol-recon.md).
- **Firmware**: begin with official update packages and offline extraction. Inventory signatures, encryption, compression, partitions, versions, and boot trust. Do not flash until image identity, backup, rollback, and recovery are independently verified.
- **Runtime or accelerator**: export a real workload, count rejection or fallback, and measure per unit to prove where it ran. Aggregate success and aggregate power do not prove placement.
- **BaaS client**: the bundle names the tables, columns, and views directly.

Beware of large artifacts. A single minified file can be megabytes on one line; pipe to a file and grep the file rather than reading it into context.

**Done when:** every intended claim has the acceptance receipt selected in Phase 0 or is listed under "Needs verification" with the exact confirming action.

## Phase 4: write the outputs

Write to the path the user asks for. Absent one, ask once, then default to `./recon/` in the current project.

**The report** is the deliverable every recon produces. The template, including the per-terrain variants for a file format and for hardware, is in [report-template.md](references/report-template.md).

**The IR** is a second artifact, written when the target has an HTTP surface and the verdict is "build it" or "build it narrowly". `surfacer` is a compiler that reads one `.surfacer.json` descriptor and emits six interfaces from it (a Rust shim, just-bash, help text, a TypeScript CLI, OpenAPI 3.1, and an MCP server) and does no recon of its own, so this skill is the producer of that file. Same findings, shaped for a machine instead of a reader.

The rule that governs it is the skill's own, made stricter: **only what you observed goes in the IR.** The report can carry inference because it has a column saying so; the IR has no such column, and everything in it is read as fact by six emitters and by `surfacer check`, which re-probes endpoints from the IR to detect drift. An inferred path there makes the drift check fire on something that never existed. Inference and "Needs verification" stay in the markdown.

The full field-by-field mapping, which terrains produce an IR and which cannot, and how the two runs from Phase 2 fill the `varies` and `observations` fields on parameters, are in [ir-target.md](references/ir-target.md).

**Done when:** every evidence row names plane, provenance, proof, and receipt; every blocker names what got past it or that nothing did; and every "Needs verification" item names the step that would confirm it. Run [gates.md](references/gates.md) against the finished draft. If an IR was written, `surfacer lint recon/{siteName}.surfacer.json` passes and its endpoint count matches the observed network rows of the report.

## Phase 5: verdict

Close with a recommendation, not just data. One of:

- **Build it.** The surface is stable and documented enough.
- **Build it, narrowly.** Only these endpoints are solid; the rest are a maintenance risk.
- **Do not build yet.** Blocked on credentials, or the surface is too unstable. Name what would unblock it.

State the maintenance risk plainly. An undocumented endpoint has no contract and no deprecation notice; it can break on any deploy. If the plan depends on coordinate-clicking a captcha or on a minified signing function, say that it will break and roughly when.

**Done when:** one of the three verdicts is stated, a reader could act on it without re-deriving your judgment, and `recon/friction.md` is handed over with the report. An empty friction log is a valid outcome; a missing one means it was never opened.

**Hand over `recon/friction.md` with the report.** Whatever slowed you down goes to whoever maintains the skill, and terrain friction in particular is what corrects a playbook.

## References

- [terrain-playbooks.md](references/terrain-playbooks.md): per-terrain technique, with what worked on real targets
- [terrain-model.md](references/terrain-model.md): access, planes, acceptance proofs, consequence classes, and A-H migration
- [practice-backlog.md](references/practice-backlog.md): ranked exercises across CLI, MCP, artifacts, apps, devices, firmware, and runtimes
- [anti-bot.md](references/anti-bot.md): what blocks recon and what gets through
- [agent-browser-recon.md](references/agent-browser-recon.md): interception, client state, React trees, desktop apps, session persistence
- [hardware-protocol-recon.md](references/hardware-protocol-recon.md): USB, BLE, serial, Wi-Fi, storage, pairing, mutation gates, parsing, and evidence hygiene
- [report-template.md](references/report-template.md): the report shape, with per-terrain variants
- [ir-target.md](references/ir-target.md): the surfacer IR contract, field by field, and which terrains can produce one
- [gates.md](references/gates.md): when to stop, and what to check before claiming a finding
- [friction-log.md](references/friction-log.md): capturing where the skill itself slowed you down

## Boundaries

**Stop at the report and the IR.** Implementation is `cli-build`'s work; recon's product is the verdict and, when there is a surface to compile, the descriptor of what was observed. The IR names commands because `lint_ir` demands a unique `commandPath` per operation, and that naming follows `cli-build`'s noun-verb convention rather than inventing a second one.

**Report the rate limit you measured.** "No limit headers observed, not measured" is a complete answer.

**Say what blocked access yields before starting it.** Without credentials, entitlement, authority, or the physical target, the output is a list of unknowns.

**Map a surface the user is entitled to use.** Recon works on services the user has access to and documentation they may read. A paywall, an authentication boundary you were not given, or personal data belonging to third parties marks the edge of the skill: the verdict there is "blocked", and that is a legitimate outcome.

**Evidence does not transfer across planes.** A USB descriptor does not prove BLE semantics. A socket write does not prove a command was accepted. A command receipt does not prove a file was created. Correlate planes explicitly.

**Discovery does not authorize mutation.** Stay within the maximum consequence declared in Phase 0. Ask before media creation, pairing, persistent settings, external actions, deletion, or firmware work. Firmware writes additionally require a verified recovery path.
