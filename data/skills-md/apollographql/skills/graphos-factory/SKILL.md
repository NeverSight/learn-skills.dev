---
name: graphos-factory
description: Build and iterate on an Apollo Connectors subgraph for a GraphOS supergraph from a REST API, with or without an OpenAPI or Swagger spec, in a dedicated git workspace that records what the API offers, the user's operation and field selection, every design decision, and the evidence each verification layer produced. Use whenever the user wants to wrap a REST API as a GraphQL subgraph for their supergraph, add or remove operations or fields from an existing connector subgraph, refresh one against a new spec, or record live API traffic as test fixtures, even if they do not say "connector", "subgraph" or "Apollo".
license: MIT
compatibility: macOS or Linux (WSL on Windows) with bash, curl, git and jq; Java 17+ for the end-to-end and live layers. Any Agent Skills host (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and others) that can run shell commands.
metadata:
  version: "0.12.2"
---

# graphos-factory

You turn a REST API into an Apollo Connectors **subgraph** for the user's
GraphOS supergraph, and keep it maintainable. The subgraph is the
deliverable: a schema the user composes with their other subgraphs.
**You are the generator**: no tool writes the schema for you. The `graphos-factory`
binary (the shared references write `graphos-factory-core <command>`; here that is
`graphos-factory`, installed beside it as the same binary) and the shell wrappers under
`graphos-factory-core/scripts/` do the mechanical work — reading a source into an inventory,
rendering placeholders, running rover, checking the invariants — and make no design
decisions at all.

**Source kinds.** `workspace.yaml`'s `source_kind` names the source. Only
`rest` is built: a REST API wrapped with Apollo Connectors, with or without
an OpenAPI document. gRPC / protobuf, databases and existing GraphQL APIs are
planned, not built: if a user asks for one, say so plainly and stop — never
approximate one with the REST path. The workspace contract is
source-agnostic; each kind adds its own intake reference and key grammar.

Everything durable lives in the **workspace**, a git repo you create per
subgraph: `inventory.json` is what the source offers, `selection.yaml` is
what the user chose, `<name>.graphql` is the subgraph schema the engineer
edits, the decision log (the calls, each with its alternatives:
`decisions.json`, then one file per decision under `decisions/`, written only
via `graphos-factory decisions`), the findings log (settled facts, likewise, via
`graphos-factory findings`) and `memory.md` are what you and your predecessors
learned. Read
[`workspace-contract.md`](graphos-factory-core/references/workspace-contract.md) once for the full
layout. The core's references are in `graphos-factory-core/references/`, this target's in `references/`.

**Never regenerate the schema wholesale after the first commit.** Compute the
delta and edit only what changed. Losing hand edits to a regeneration is the
specific failure this skill exists to avoid — and a hand edit you have not
codified (see "Hand edits" below) blocks an `apply` until you have.

**This target's contract** is the subgraph's place in the user's supergraph;
what the references leave open is listed under their "Open" headings. What
holds today, enforced by the binary: `{{BASE_URL}}` and `{{AUTH_EXPR}}` are the
only placeholders, with the scheme prefix *outside* the placeholder, and
`template.yaml` gives each a local test value (`export` renders them with the
production values, [`export-graphos.md`](references/export-graphos.md)); the Federation
directives the schema may import are `@key`, `@shareable`, `@requires`, `@provides`,
`@external`, `@inaccessible`, `@listSize`, `@cost` and `@tag`
([`federation-subgraph.md`](references/federation-subgraph.md)); one `@source` is the shape the
layers model, and a second is a lint warning (unmodelled, not forbidden); a type another subgraph owns keeps its owner's exact name, unprefixed, only once the user's resolved decision declares it (`decisions add --foreign-type NAME`, federation-subgraph.md § Entities another subgraph owns). **`@tag` is
for GraphOS Contracts, and off by default**: apply it only when the user's supergraph
uses contracts, with the names their contracts already filter on, recorded as a
decision. Never invent a tag; this target imposes no tag names, so `unknown-tag` never fires.

**Setup, before the first command.** `<skill>` below is the directory that holds this file. Whatever installed it (`npx skills add`, `gh skill install`, a Claude Code plugin, a copied directory) and whatever the agent (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI or any other), check with `bash <skill>/scripts/bootstrap.sh --check`, and on exit 127 run `bash <skill>/scripts/bootstrap.sh` once (about 3 MB into `~/.cache/graphos-factory-core/`); a session-start hook that already did it (`scripts/session-start.sh`, in a clone used as a plugin) makes the check pass. Then run `. <skill>/scripts/env.sh` in your shell, or at the start of every command when your shell keeps no state between commands: it puts `graphos-factory`, its `graphos-factory-core` link and rover on `PATH` and sets `GRAPHOS_FACTORY_CORE_SCRIPTS` (the `$S` below). The toolchain (`toolchain.sh`) is installed only once the user agrees, whatever the host. **First subgraph in a new workspace:** follow [`first-subgraph.md`](references/first-subgraph.md), the steps from `init` to `export` in order, each with its commands, its checks and the expected non-zero exits.

<!-- core:begin -->
## Before anything else

1. If a workspace exists, read the decision log (`graphos-factory-core decisions list .`,
   including `--open` for questions still awaiting the user), the findings
   (`graphos-factory-core findings list .`) and `.factory/memory.md` **in full**. Do not re-open a
   `resolved` decision unless the user asks. When they want to revise an answer to the
   same question, `graphos-factory-core decisions reopen . --id D-id` clears it and puts the record
   back to `open`, then settle it again with `decisions resolve`; when the question
   itself has changed, record a new decision instead. Never edit a record in place — the
   file is written only through that command. If the workspace still carries a legacy
   `.factory/decisions.md` and no `decisions.json`, run `graphos-factory-core decisions migrate .`
   once to import it (it preserves the `D-nnnn` ids and removes the `.md`), then
   continue. A `decisions.json` in the older format (provenance records titled `Hand
   edit codified:` or `Source patch:`, prose with no alternative) is split once with
   `graphos-factory-core decisions migrate . --split`: sort each record it lists by the test under
   "Write it down", then run it with `--sorted` (workspace-contract.md § `decisions.json`).
2. Read the target's contract (named above and under References) and
   `naming.md`. Violating them breaks the schema a router can run
   rather than a test: the target's `@source` and placeholder rules, and
   `{Service}_Type` / `{service}_field` with snake_case for multi-word names.
3. For new intake or before `select` / `apply`, make the cheap call first: does the
   user want customer-/tenant-specific fields the spec does not define (analytics
   fields, CRM custom objects, CMS content types)? If not, it is a generic wrapper —
   record `context_mode: generic` in `workspace.yaml` and move on (an unrecorded mode
   also reads as generic, so nothing blocks on it); a `modelId` argument or a JSON field
   alone does not make it specialized, and no `context.yaml` is needed. Do not ask for a
   tenant model, metadata export or credential merely because the endpoint accepts an
   identifier or JSON. Only if it is specialized or you are unsure, read
   `customer-context.md` (under References) and assess there — record `context_mode`
   and any dependencies before authoring.
4. Pick the verb the user needs (the target's verbs, `init` among them, follow
   this table) and read the reference it names.

## Verbs

| Verb | Read first | What you do |
|---|---|---|
| `discover` | spec-intake **or** api-discovery | build/refresh `inventory.json`; assess customer context and update its records/snapshots within the authorized scope; report the diff; never edit schema or selection |
| `select` | naming, schema-authoring | agree operations, roots, names, field exclusions, tags, pagination; surface every `[read?]` POST and confirm with the user which are reads before giving one `root: query`; write `selection.yaml` (each included operation with `include: true` and its `graphql` root and name — nothing writes this file for you); then `graphos-factory-core selection draft` proposes a `response.envelope` per included operation — **confirm each one with the user** and set `confirmed: true`, because a draft nobody agreed to must never become the schema's shape; it also drafts one `links:` entry per `candidate_entity_link` fact (`graphos-factory-core inventory links .` lists them) — **confirm each link with the user too** (`confirmed: true`, or `include: false` with a `reason`), because a relationship field is one request per parent and only the authored schema knows whether it would be circular; record each design question as a decision — `graphos-factory-core decisions add . --title T --question Q --choice LABEL … [--multiple]` (choices are numbered 1, 2, 3…; ids are kept only when every `--choice` is `id:label`) — and settle each with the user via `graphos-factory-core decisions resolve . --id D-id --chosen N --note …`, never as loose chat messages; record what the references settle for you as a finding (`graphos-factory-core findings add . … --cites REF`) when an instrument needs it, and otherwise do not record it; to revise a settled answer, `graphos-factory-core decisions reopen . --id D-id` and resolve it again. |
| `apply` | schema-authoring, mapping-language, testing | `graphos-factory-core lock --check` (stop on uncodified hand edits; the provenance drift it lists is not a stop); `graphos-factory-core context check` (resolve build gaps before authoring); `graphos-factory-core reconcile --baseline HEAD` names the delta (on a first apply the schema is not in HEAD yet, and every span reads as `added`); edit the schema for exactly those spans, keeping every override's assertions true; for each confirmed link, `graphos-factory-core links apply . --dry-run` prints the field-level `@connect` keyed by `$this` (no `@key`; no header and no argument unless the by-id root field carries a per-call credential, which it mirrors — same argument, same header or query parameter; for a nullable fk, the `isSuccess` and selection null guards, because the router still sends `GET …/` for a null parent) to paste into the host type — it refuses `circular`, `self`, `no-fk-field`, `field-exists`, `nullable-fk`, `no-host`, `no-root-field` and `target-refused` (a stale entry whose keep-or-drop decision is not resolved `keep`) (connectors-language § Relationship fields) and exits 1 whenever any entry is refused, even with others printed; `graphos-factory-core scaffold` drafts the case, stub and unit entry of every operation that has none (the notes say what the unit entry could not carry) — audit every placeholder, then `e2e.sh --generate`; run it again (clean; `changed since HEAD` ⊆ the delta); `graphos-factory-core source-coverage . OP-KEY --check` on every operation you touched, and `graphos-factory-core source-coverage . --check` (no OP-KEY: every selected operation, each failing one named) before `lock` — zero `unaccounted` and zero `unresolved` in both directions, and no `unaccounted` behaviour row (an optional argument's doc comment must carry the source's omission sentence, or a `behaviour` omit says why not — a finding's `not-applicable`, a decision's `editorial`), is the bar (`--check` fails closed); each path you meant to leave off is recorded, not a silence: one you chose not to expose is a decision whose alternative is exposing it, `graphos-factory-core decisions add . --title T --question Q --choice omit:L --choice expose:L --resolved --chosen omit --note WHY --omit 'op\|direction\|path\|editorial'`, and one an expression consumes is a finding, `graphos-factory-core findings add . --title T --body TEXT --cites REF --omit 'op\|direction\|path\|consumed'` (quote each and type plain pipes: each backslash here is only this table's escape; `findings add` refuses `editorial`); an `unresolved` row from the classifier's own grammar (a request `->map(…)->first`, a request-side `->match`, a chained method such as `->match->first`) (or a `...` spread that is not the `disc->match(…)` abstract-type form) is recorded and reported as not verified by this layer, never cleared by editing `inventory.json` (schema-authoring.md § Coverage); `graphos-factory-core lock`; validate; commit `apply:` |
| `codify` | workspace-contract, mapping-language | a hand edit **to the schema** was detected: learn why from the engineer or the diff, then `graphos-factory-core codify --key K --reason R` with `--expressed` (after moving the intent into `selection.yaml`) or `--assert kind=value`…, and `--context TEXT` for the why the diff cannot show (codify records no decision); for an edit to a pinned spec, `graphos-factory-core codify --source PATH --reason R`, then, in a spec-backed workspace, rebuild the inventory (`graphos-factory-core inventory build PATH`; an `intake: mixed` workspace re-runs `infer --update-inventory` after it) so the correction and its patch marks reach `inventory.json`, and re-run `reconcile`; commit `decide:`. `--key` refuses a span that is in sync with the lock: a correction to something the tool *inferred* is not a hand edit — see the first policy below |
| `validate` | testing, customer-context | check context with `--phase live` before live requests; report live-only gaps as `not_run` without blocking offline layers; compose → unit → e2e → write-body proof → conformance → lint → json-accounting → live (the write-body proof and json-accounting layers are non-gating: a `fail` is printed as open findings, never as a pass; `evidence/latest.json` is `contract_version: 2`); write `evidence/latest.json`; report skipped layers as skipped; a unit run with zero cases is `not_run`, never a pass; every suite with zero cases fails unless its header's first sentence cites its decision (`D-0019` or `D-k7m2qx`), and a `skip: true` case fails; every selected operation is a live case or a live `exclusions:` entry with its reason; lint's `link-untested` warns on each relationship field that no unit entry targets (`<Type>.<field>`) or no e2e case selects, and evidence's report names each one; `link-null-untested` warns when a nullable fk has no null-parent e2e case (a mapping for the empty-segment GET serving a case that selects the field), and, when `tests/live.yaml` exists, `link-live-unaccounted` when no live case selects the field and no `exclusions:` entry `field: "<Type>.<field>"` names it; a field with neither unit nor e2e, with no null-parent case, or excluded live is not validated; say so (scaffold does not draft link-field tests yet: write the unit entry and e2e case by hand, connectors-language § Relationship fields); a conformance body the oracle could not judge is `unchecked` (no documented shape) or `unmatched` (no such operation, unreadable body — this one fails), never a pass; an accepted gap is `graphos-factory-core codify --waive TARGET --status S --reason R`; before reporting, `graphos-factory-core lock --check --provenance`; when it exits 3, relock (`graphos-factory-core lock`) only when a plain `graphos-factory-core lock --check` reports no changed or unattributed span, pinned-source problem or edited inventory (it then prints the relock advice, and `--json` sets `relock_advisable`) — the drift is provenance alone (a case, a stub, a `memory.md` line), or a document `sources.lock.yaml` no longer pins, which a relock stops watching on purpose. Otherwise the schema, a pinned document or `inventory.json` changed under the lock: stop and follow "Hand edits" (codify a span or pinned source, rebuild an edited inventory), because a relock would erase the only record of the edit |
| `record <op>…` | api-discovery, testing | `graphos-factory-core probe` each request (GET only unless told otherwise; scrubbed before it touches disk); `graphos-factory-core infer --update-inventory` for the oracle; `graphos-factory-core fixtures` for the stubs; note spec-vs-reality findings in `memory.md` |
<!-- core:end -->

This target's verbs, `init` first (it records the target, `skill.name: graphos-factory`; `--target` is optional):

| Verb | Read first | What you do |
|---|---|---|
| `init <name>` | workspace-contract | decide the subgraph name (snake_case or kebab-case, naming.md) and `context_mode` (step 3 above), fetch the description document yourself, then `graphos-factory init <dir> --name N --spec FILE [--url U] --context-mode generic\|specialized` — it writes `.factory/workspace.yaml` (`skill.name: graphos-factory`), the working copy and its pinned vendor copy, `sources.lock.yaml` and `inventory.json` exactly as `sources pin` + `inventory build` would, plus four skeletons: `<directory>.graphql` (the spec links and the one `@source`, no root field, so compose fails until the first apply), `template.yaml` (`BASE_URL` = the document's first absolute server, else a local stand-in its comment asks you to complete; `AUTH_EXPR` = `{$env.<SERVICE>_TOKEN}` with the scheme named; local test values only, never the production host, which is given at export), `supergraph.yaml` (rover's compose config for this one subgraph, not the user's supergraph) and `tests/router.yaml` (the e2e `override_url`); act on every comment in them, and one that already exists is left alone. It refuses a directory that already holds a workspace; `--dry-run --json` lists every file's path, content and sha256 without writing. It never runs git: **standalone**, `git init` the directory; **already inside a repo** (a monorepo, one folder per subgraph), let the enclosing repo track `<name>/` and do not nest a second repo. Then commit. A no-spec workspace (`intake: discovered`) has no document to pin: write `workspace.yaml` (with `skill.name: graphos-factory`) and `sources.lock.yaml` by hand, as workspace-contract shows |
| `export` | export-graphos | only after `validate`: `graphos-factory export . --out DIR --base-url URL` (DIR outside the workspace; URL the production host, which the user gives you) renders `DIR/<directory>.graphql` and prints the rover commands, the router's credential variables and minimums, and what is not verified. It refuses an unvalidated workspace (no evidence, a file the layers read changed since `evidence` ran, which it names, a layer not `pass`, an operation with no executed evidence, a lint error) and a base URL that is not an absolute http(s) URL, carries userinfo or is local, and says why, in `evidence`'s terms: fix that (then `evidence`) and re-run, never work around it. It also refuses a `supergraph_check` that ran and failed, naming rover's errors. Hand the user its output. Never run `rover subgraph check` or `publish` by hand, never handle, ask for or print a GraphOS key, and report `supergraph_check` (when not `pass`) and anything else it lists as not verified |

`validate` on this target also runs its evidence layer, `supergraph_check`: `rover subgraph check` against the user's
published variant, only with `APOLLO_KEY` in their environment (the key is theirs: never ask for, set or print it) and a graph ref:
ask once per session which `<graph>@<variant>`, then set `GRAPHOS_FACTORY_GRAPH_REF` on the commands you run; their own
`GRAPHOS_FACTORY_SUPERGRAPH_CHECK=auto` uses `$APOLLO_GRAPH_REF` (never set it for them). Else `not_run` (references/verification.md). The compose layer composes the subgraph alone. Report a `not_run` or `skipped`
check as not run, never as a pass, and say plainly the subgraph has not been checked against the user's supergraph.

<!-- core:begin -->
## Instruments

One binary, the product's, plus the shell wrappers in `graphos-factory-core/scripts/` around rover, Java
and curl for the validation layers. It is downloaded from the skill's GitHub releases (the rolling
`edge` pre-release until a versioned release exists) by the skill's own `scripts/bootstrap.sh` (the
product's session-start hook may run it; otherwise run it yourself), which also links it as `graphos-factory-core`; it is built from
`crate/` only when developing the skill itself (`bootstrap.sh --build`). Every wrapper takes
the binary from `$GRAPHOS_FACTORY_CORE_BIN`, then that link in the bootstrap cache, then PATH, prints which
one and its version to stderr, and exits **78** (a `fail`, never a skip) when it is
older than the pin (`crate/Cargo.toml`, an installed skill's `release.env`, or `$GRAPHOS_FACTORY_CORE_VERSION`); `evidence` hands the
wrappers its own binary. On 78, re-run `bootstrap.sh` (`--build` in a checkout) or set
`GRAPHOS_FACTORY_CORE_BIN` — never lower the pin to get past it. Run everything from the workspace
root. `graphos-factory-core <command> [verb] --help` (or `-h`) prints that command's usage and reads
or writes nothing. A flag the verb does not declare — a typo, or two flags
quoted into one argument — is refused with exit 2 and nothing runs; fix the
spelling, never drop the flag. `rover` is needed for compose, unit, e2e and live; Java for
e2e's WireMock; nothing is ever installed into a workspace. rover's composition plugin is under the Elastic License v2, which only the user accepts, by setting `APOLLO_ELV2_LICENSE=accept`: until then those four layers are `not_run`. Ask once: show the link, and only on an explicit yes set `APOLLO_ELV2_LICENSE=accept` for the commands you run this session (record the consent in memory.md); never set it unasked, and tell them `export` in their shell profile makes it permanent.

```bash
S=path/to/graphos-factory-core/scripts
export GRAPHOS_FACTORY_CORE_SCRIPTS=$S                    # evidence needs to find the wrappers
# If the host supplies a model identifier, set GRAPHOS_FACTORY_CORE_LLM_MODEL to that exact value.
# Never infer or guess a model identifier. The lock records unknown when this value is absent,
# and `lock` prints a one-line warning for that and for a skill source of binary-build.

graphos-factory-core inventory build openapi.json          # description document (OpenAPI 3.x or Swagger 2.0) -> .factory/inventory.json (refuses to overwrite a hand-edited one)
graphos-factory-core inventory list --tag Incidents        # page the inventory, grouped by tag; 50 a page. --json: total, offset, limit, next_offset (null on the last page) — a loop over every operation follows next_offset
graphos-factory-core inventory list --support needs_review # what still needs a decision
graphos-factory-core inventory describe get:/v2/incidents  # one operation, shapes expanded
graphos-factory-core inventory links . [--json]            # every candidate_entity_link fact flat: shape, property path (album_id / []>album_id / songs[]>album_id), the canonical GET-by-id operation, whether the host is a list item and whether that operation is selected, then every GET-by-id refused as a target because its response does not carry its key — a hint, never a finding; judge each and record the call with `graphos-factory-core decisions add`
graphos-factory-core inventory diff old.json new.json      # what a spec refresh changed

graphos-factory-core context check . [--phase build|live] [--json]   # declared customer requirements; exit 2 for missing context, 1 for invalid records
graphos-factory-core context capture . (--requirement ID|--input) --id ID --from FILE --representation raw|derived|transcribed …   # copy one local non-secret artifact and record its provenance
graphos-factory-core decisions list . [--open] [--causal] [--json]    # the decision log: decisions only — calls with their alternatives, resolved, and open questions awaiting the user. The records of `.factory/decisions.json` (numbered `D-nnnn`, never added to), then one file per record added since under `.factory/decisions/` (random `D-k7m2qx`); --causal orders by after/amends and shared affects, a `via:` line per edge
graphos-factory-core decisions add . --title T [--question Q] [--choice LABEL]… [--multiple] [--phase P] [--affects PATH]… [--resolved --chosen N --note TEXT --decision TEXT --by user|agent] [--omit 'operation|direction|path|reason']… (a resolved request omit also removes an optional source body member from the write-body proof; a member the source requires stays a gap, `required_member_omitted`, and `decisions add` warns when an omit targets one) [--json-reason 'Type.field|reason']… [--null-handling 'operation|argument|behavior']… [--secret-field 'Type.field|disposition|reason']… [--foreign-type NAME]… [--slug S] [--after D-id]… [--amends D-id]…   # record a decision, as its own file with a random id, printing `N  label` per choice (choices numbered 1, 2, 3… in flag order; ids are kept only when every `--choice` is `id:label`, else each value is a whole label; a duplicate id, or an invalid one when every value looks like `id:label`, is refused at the flag) (--after names decisions it presumes, --amends ones whose answer it changes where their affects overlap): an open question, or with --resolved a call already made (`resolution.by` defaults to agent; --note says why you did not ask); refuses, exit 1 `no-alternative`, a record that names its alternative none of three ways — a --question, two or more --choice, or an --omit with reason `editorial` — a settled fact is `findings add`; --omit records a structured scope exclusion `source-coverage` reads, only on a resolved record, and an `editorial` omit lives only here; path `.` omits the whole direction for that operation, which is how to record an EmptyResponse 204's empty root row; --json-reason records why a response field is left typed as the workspace's JSON scalar, from `crate::json_accounting::REASONS`, read only on a resolved record — never a selection.yaml field or a schema doc comment; --null-handling records what the connector sends for an explicit null argument (behavior: send_null or omit), read only on a resolved record; --secret-field records a reviewed credential-shaped response field (disposition expose or exclude) that lint's secret-field-exposed rule reads, only on a resolved record; --foreign-type declares a type another subgraph owns, which the schema may then declare under its owner's exact name, read only on a resolved record and only by a target that allows it (that target's references say where); direction `behaviour` waives an omission sentence an argument's doc comment leaves out, path `query:NAME`/`path:NAME`/`header:NAME`/`body:KEY.PATH`, reason `editorial` or `not-applicable`
graphos-factory-core decisions resolve . --id D-id [--chosen N|LABEL]… [--note TEXT] [--decision TEXT] [--by user|agent] [--force]   # settle an open decision (with --force it replaces the whole resolution: pass the old --decision and the old note plus what you add, to amend a record without losing it); the same command a headless agent and a host UI both use
graphos-factory-core decisions reopen . --id D-id [--json]   # revise a decision: clear a resolved/superseded record's resolution and set it back to open (everything else kept); refuses an unknown id, an open record, or a missing/invalid log
graphos-factory-core decisions supersede . --id D-id [--json]   # mark a resolved decision replaced: status only, its answer kept; it stops counting as resolved everywhere (its omits, json_reasons and null_handling, its affects, a links: decision: naming it), so re-record what still applies; the fix for lint's `stale-omit` (a finding's: `findings supersede`)
graphos-factory-core decisions link . --id D-id (--after D-id | --amends D-id)… [--json]   # edges on a decision recorded as its own file, the fix for lint's `decision-overlap`; an old D-nnnn record never gains a field, so put the edge on the newer record
graphos-factory-core decisions migrate . [--keep-md] [--force] [--dry-run] [--json]   # one-time: import a legacy .factory/decisions.md into decisions.json (preserves D-nnnn ids, parses fenced Omits: blocks into structured omits), then remove the .md
graphos-factory-core decisions migrate . --split [--sorted FILE] [--dry-run] [--json]   # one-time, an older-format log (FILE: YAML/JSON mapping each listed D-nnnn to `{as: decision, question, choices, chosen, by, note}` | `{as: finding, cites, body, …}` | `{as: memory, line}` | `{as: drop}`; without it the unassigned records are listed and nothing is written, exit 1 `unsorted`): codify records move onto the override, waiver or patch they shadow, refresh records become findings, a record with a question, choices or an editorial omit stays a decision; lists every other record for you to sort by hand and refuses to write without --sorted until each is assigned
graphos-factory-core findings list . [--json]             # the findings log (`.factory/findings.json`, then one file per finding added since under `.factory/findings/`): facts a reference or the wire settled, `F-nnnn` or random `F-9k2wde`, current until superseded; every omits/affects reader takes these with the resolved decisions
graphos-factory-core findings add . --title T --body TEXT [--cites REF] [--source agent|codify|sources] [--affects PATH]… [--omit 'operation|direction|path|reason']… [--evidence E]… [--related D-id|F-id]…   # record a fact an instrument needs, or the next session does; omit reason `consumed` or `not-applicable` — refuses `editorial`, which is a decision
graphos-factory-core findings supersede . --id F-id       # a later finding replaces it; it stops counting
graphos-factory-core source-coverage . [OP-KEY] [--json] [--check]   # source coverage: every fact the source offers is covered by the schema, or a resolved decision or current finding says why not (`spans obligations` is the old spelling); every request-body and response path the source offers (parameters are not classified), classified as mapped / consumed / omitted-decided / unaccounted / unresolved, plus unverified-default and transport-expansion-missing at an `x-expansion` boundary, plus a behaviour section when an optional argument's source says what omitting it does (documented / waived / unaccounted); zero of those four in both directions and zero unaccounted behaviour is the completion bar, and --check fails closed on any; with no OP-KEY it checks every operation selection.yaml includes, one counts line each, --json wraps each operation's object in `operations` with `totals` and `failing`, an operation it cannot classify counts failing, and nothing selected exits 1; a resolved omit no row needs any more (the path is now mapped, envelope-read for an `editorial` entry, or no longer offered) is a `stale-omit`, counted and listed with its decision id but not part of the bar, and lint warns on it
graphos-factory-core spans json-accounting . [--json] [--check]   # every response field the current SDL still types as the workspace's JSON scalar, nested and list-wrapped fields included, matched against a `json_reasons` entry on a resolved decisions.json record (never selection.yaml or a schema doc comment — the decisions-only rule) for a reason from a closed vocabulary (free-form-object, recursive, vendor-undocumented, polymorphic-without-discriminator, depth-cap) whose predicate is re-checked against inventory.json every run — accounted / unaccounted / stale (recorded reason no longer holds) / recoverable (inventory is now fully typed there, overrides the rest) / unresolved (reason recorded, but no shape located for the type: by name, root-field operation or parent property); `defaults.fields: all` is never itself a reason, and --check fails closed on anything but accounted
graphos-factory-core serialization . [--json]   # read-only: the standalone CLI for the write_body_proof evidence layer; per body-sending write, each argument's value proven at its own body pointer / query key / path or header placeholder by an executed e2e case (needs the run log), omission at its pointer, explicit null per selection.yaml `defaults.null_handling` (state `omit`) or a per-argument null_handling decision; an argument the connector spells in a way the reader cannot place is placed by an executed case whose stub demands its value at one body pointer (`ambiguous_value` when the value is not distinctive; `--json` lists `placements`, static or executed); unproven_mapping and null_handling_undecided are open findings, never passes; replaces list-arg-unproven / mutation-cases / loose-write-body / unit-no-body
graphos-factory-core reconcile . --baseline HEAD           # schema <-> selection <-> inventory delta; overrides; hand edits; what moved since HEAD; exits 2 with the URLs to compare when not one connector pairs (a base-URL split)
graphos-factory-core sources pin . --path openapi.json [--url URL]   # keep the vendor's bytes as .factory/sources/*.upstream.*; record kind/version/hashes
graphos-factory-core sources status . [--json]             # every pinned document: kind, upstream integrity, hand edits, patches; plus every recorded docs/probe source (url, retrieved_at, sha256, operations, note)
graphos-factory-core sources refresh . --path openapi.json --from FILE [--url URL] --reason R   # a newer vendor document: re-apply patches[] (re-applied / obsolete / conflict), rebuild + diff the inventory; both shas and each patch's fate go to a finding (source: sources)
graphos-factory-core lock . [--check [--provenance]] [--skill-dir DIR] [--model MODEL]   # record applied hashes plus skill, binary, toolchain, input and output provenance; --check also lists provenance drift, --provenance fails on it; a write warns on stderr when the model is unknown or the skill source is binary-build, naming --model / GRAPHOS_FACTORY_CORE_LLM_MODEL and --skill-dir / GRAPHOS_FACTORY_CORE_SCRIPTS
graphos-factory-core codify . --key K --reason R [--context TEXT] --assert contains=…   # turn a hand edit into an override (reason, context, assertions), or --expressed (a finding only when --context is given); no decision record — --decision D-id (numbered or random) only attaches a real one
graphos-factory-core codify . --source openapi.json --reason R [--context TEXT]   # turn a hand edit to a pinned spec into patches[] carrying reason and context; no decision record
graphos-factory-core probe . --key "get:/x/{id}/" --url URL  # one recorded, scrubbed live request -> .factory/samples/
graphos-factory-core infer . --update-inventory            # samples -> shapes (the no-spec conformance oracle)
graphos-factory-core fixtures .                            # recordings -> case-scoped WireMock stubs (.factory/recordings.yaml)
graphos-factory-core scaffold . [--op KEY] [--force] [--dry-run]   # draft a case, a stub and a unit entry per selected operation from the connector + shapes (a sparse-fieldsets GET: an omitted and a `_fields_narrowed` case, no unit entry for a comma default); audit before --generate
graphos-factory-core scaffold . --op KEY --status CODE|all-missing  # error cases: per documented non-2xx status a case with `# expect-upstream-status: CODE` and a stub answering it (the documented body, if any); refuses a stub equal to an existing one, or to another case planned in the same run
graphos-factory-core error-statuses .   # one line per included operation: root field, documented non-2xx statuses, the statuses the last evidence run saw answer its own request, operation key (`-` for none); for e2e.sh, and to see what is still owed
graphos-factory-core selection draft . [--links|--envelopes] [--op KEY] [--force] [--dry-run]   # propose a response.envelope per included operation and a links: entry per candidate_entity_link fact; every block lands `confirmed: false` for you to confirm
graphos-factory-core links apply . --dry-run [--link "<shape> > <path>"] [--json]   # print the field-level @connect for each confirmed links: entry (the by-id selection verbatim, {$this.<fk>}, the one @source, no @key, the root connector's static headers and queryParams, and the by-id root field's per-call credential mirrored or none; a nullable fk gets the isSuccess and selection null guards); refuses circular / self / no-fk-field / field-exists / nullable-fk / no-host / no-root-field / target-refused (a stale entry lint flags link-target-refused, until its keep-or-drop decision is resolved `keep`); never writes the schema
graphos-factory-core selection set . --op KEY… --include true|false [--dry-run] [--json]  # toggle an operation's include flag in place, block or one-line flow entry, comments and anchors preserved (drives a UI toggle)
graphos-factory-core selection review . [--candidate FILE --expect-input TOKEN] [--expect-review TOKEN]  # read-only JSON snapshot/review; never saves or applies
graphos-factory-core batch find . [--json] [--all-types] [--check]   # per keyed type (graphql.entity), the operations returning an array of it and whether one takes a list of its key: batchable / partial-shape / needs-scope / style-conflict / paginated / list-no-key-filter / none (reads only: GET, an inventory read, or a selection root: query); with graphql.batch: true it prints a paste-ready type-level $batch connector (you paste it; nothing writes the schema); --check exits 1 when a batchable keyed type has no type-level $batch connector and no graphql.batch: false (lint batchable-entity-unbatched); 2 when the schema does not parse
graphos-factory-core scaffold . --op batch:<Shape>   # for a type with a $batch connector: a case through a root whose selection maps the key alone, its root stub and an `x-required` lookup stub demanding the exact key list — e2e fails unless the router makes that request

bash $S/compose.sh .                                 # rover supergraph compose            (layer 1)
bash $S/unit.sh . [--only PATTERN]                   # rover connector test                (layer 2)
bash $S/e2e.sh . [--generate] [--only PATTERN]        # WireMock (java) + real Apollo Router; every stub loads once, for the whole suite — a stub's request matcher must be unique workspace-wide (layer 3); a case's `# expect-upstream-status: CODE` fails it unless the operation's own request was answered CODE (a status served to a nested lookup or side call is not the operation's), an error case without one on an operation documenting several statuses is UNPROVEN, never a pass, and a documented status no passing case saw answer its own request is `not_run` in `error_coverage` and leaves the operation `unchecked`
graphos-factory-core validate .                            # fixture/request bodies vs the spec  (layer 4)
graphos-factory-core lint .                                # contract + coverage invariants, incl. fixture-collision (two stubs matching the identical request) and fixture-overlap (a stub matching every request a sibling matches: add the `absent` matchers it names, or a priority), sparse-fieldsets (a GET's `fields` default derived and forwarded; `sparse_fieldsets: {enabled: false}` opts out), and undocumented-root-field / argument-constraints-undocumented (a root field or constrained argument with no doc comment, or an optional argument whose doc comment drops the source's omission sentence, "If not passed, …" or "Defaults to …", traced through headers and nested write bodies too; the finding quotes the text to write), and argument-required-optional-in-source (an argument made `!` over an optional source parameter, error); secret-field-exposed (a response field named like a credential — token/secret/password/passcode/credential(s), or an api/private/client/secret/encryption/signing/access `*Key` compound; exclude it or `decisions add --secret-field 'Type.field|expose|reason'`); decision-without-alternative (a decision record with neither a question nor choices, warning); decision-id-duplicate, decision-link-unresolved and decision-link-cycle (a merge kept one id twice, or an after/amends dangles or loops, errors) and decision-overlap (two resolved decisions, at least one recorded as its own file, decide the same span and neither names the other: `decisions link`, warning); entity rules for every @key type: entity-without-lookup (per resolvable key; `resolvable: false` stubs exempt) and entity-key-not-embedded (read through the selection) (errors), entity-without-consumer and entity-field-unresolved (warnings); and two more warnings: unknown-tag (a `@tag` outside the target's vocabulary) and failure-case-missing (per operation, the documented non-2xx statuses no e2e case exercises, meaning the operation's own request was answered with it, not a nested one) (layer 5)
bash $S/live.sh .                                    # tests/live.yaml against the real API (layer 6)
graphos-factory-core evidence . --scripts $S               # run every layer, write .factory/evidence/latest.json (includes write_body_proof, in-process, same-run against wiremock_e2e's own current results — never a stale latest.json)
graphos-factory-core render . --out /tmp/x                 # the placeholder-free copies the wrappers `eval`: stdout is shell assignments (RENDERED_SCHEMA, COMPOSE_CONFIG; ROUTER_CONFIG and its router.yaml only with a --wiremock-port, --router-port or --health-port flag); not a hand-off: the user-facing render is a target's `export`, where it has one

bash skills/<skill>/scripts/bootstrap.sh [--build]   # install this skill's binary and its graphos-factory-core link (download; --build from crate/)
cargo test --manifest-path path/to/crate/Cargo.toml  # the instruments' own tests
```

`inventory list` and `describe` exist so you never read a large raw spec:
page through the inventory and expand one operation at a time. A page holds
50 operations unless `--limit` says otherwise; `operations` alone is not the
whole inventory — keep calling with `--offset <next_offset>` until
`next_offset` is null.
<!-- core:end -->

This target's instruments:

```bash
graphos-factory init <dir> --name N --spec FILE [--url U] [--retrieved-at T] [--created-at T] [--context-mode generic|specialized|undecided] [--dry-run] [--json]   # a new spec-backed workspace: workspace.yaml (skill.name graphos-factory), working + vendor copy, sources.lock.yaml, inventory.json; refuses an existing workspace; never runs git
graphos-factory export . --out DIR [--base-url URL] [--json]   # the gate over evidence/latest.json, then DIR/<directory>.graphql rendered with the production host and the rover hand-off (link fields lint leaves not validated among what it did not verify); exit 1 refused, 2 usage; never runs rover
GRAPHOS_FACTORY_GRAPH_REF=<graph>@<variant> bash "$GRAPHOS_FACTORY_TARGET_SCRIPTS/supergraph-check.sh" .   # what evidence's supergraph_check runs (APOLLO_KEY from the user's environment): exit 0 pass, 1 fail, 3 not_run, 127 skipped
```

`export` is the target's one command; every other instrument above is the core's. One validated workspace shows the path end to end: [`gitea`](https://github.com/apollographql/graphos-factory/tree/main/pilots/graphos/gitea/) (Swagger 2.0, pinned and patched; `supergraph_check` recorded `not_run`: no key in CI). Every layer, the write and a live run against a seeded Gitea included, is executed upstream before a snapshot is published; this repository's CI re-runs only the offline checks (`lint`, `validate`, `reconcile`, `lock --check --provenance`).

<!-- core:begin -->
## Policies you apply every time (the why is in the references)

- **Query vs Mutation is semantic, and a POST is a write until the user
  says otherwise.** The inventory records every POST as `write` and marks
  the ones whose name suggests a read with a `read_hint` (`[read?]` in
  `inventory list`). At `select`, list every hinted POST and ask the user
  which are reads before writing `root: query` for any; `selection.yaml`
  carries the explicit `graphql.root`, and a POST selected as a Query needs
  its reason recorded as a decision (the resolution of the open question
  you raised at `select`, or `graphos-factory-core decisions add . --resolved …`
  with its `query` and `mutation` choices): a write under `Query` is one
  callers, caches and retries treat as safe, so the choice has to be
  reviewable.
- **The inventory is facts; the selection is judgements.** `inventory.json` is a
  straight reading of the source: every field is checkable against the document, it is
  regenerable at any time, it is **never hand-edited**, and it never governs the schema.
  Every judgement that changes the schema or the tests — the GraphQL root, the field
  name, the response envelope, what is exposed of the pagination, tags, exclusions — is
  in `selection.yaml`, where the tool drafts it as a hint and you confirm it with the
  user. When an inference is wrong, do not correct the inventory (the lock hashes it;
  `lint` reports `unacknowledged-inventory-edit` and `inventory build` refuses to
  overwrite it): fix the **document** in the pinned working copy and `codify --source`,
  or write the **judgement** you want into `selection.yaml` and re-run `reconcile`.
  `codify --key` is for neither — it records a hand edit to the schema and refuses a
  span that is in sync.
- **A relationship link is a judgement in `links:`.** The inventory's
  `candidate_entity_link` fact only proposes; `selection draft` writes the
  entry `confirmed: false`, and an unconfirmed draft never governs — no
  field is applied, reconcile notes it, lint warns. A confirmed link is a
  field-level `@connect` keyed by `$this`, no `@key`, mirroring its by-id
  root connector's credential — none under `@source` auth (connectors-language.md
  § Relationship fields) — and, for a nullable fk, guarded so a null
  parent resolves to null instead of failing on `GET …/`; the entity form is the cross-subgraph and `$batch`
  exception and needs a decision. A confirmed link whose target the
  current rules refuse or whose fact is gone is stale and raises an open
  decision for the field — choices `keep` and `drop`, the refusal as its
  context; run the `decisions add` command reconcile and lint print and
  name the record in the entry's `decision:`. While it is open
  the link is reconcile drift, `link-target-refused` and a
  `target-refused` refusal from `links apply`. Resolved `keep`
  exempts it; resolved `drop`: set `include: false` citing the
  decision and remove only that field and its hand-written tests on the
  next apply — never regenerate.
- **Never an executable SDL default.** `pageLimit: Int = 5` is a value the router sends
  when the caller omits the argument and a consuming agent copies as "the value to use".
  Write `pageLimit: Int` and put the provider's default — with its `minimum`, `maximum`
  and `enum`, whenever the inventory carries them — in the argument's doc comment
  (schema-authoring.md § Argument
  constraints). No offline layer sees the difference. The one exception is a
  sparse-fieldsets argument (`fields: String = "…"`), whose default lint derives and
  requires (§ Sparse fieldsets). The rest of an argument's doc comment is at most one
  source sentence, opt-in per service, and never its type or requiredness (§ Argument
  descriptions).
- **Untyped beats unreachable, but typed beats untyped.** Emit a `<Prefix>_JSON` scalar
  only when the shape cannot be typed honestly (any `oneOf` at `connect/v0.3`; at v0.4
  one whose members no wire value tells apart, or that is nested where no connector of
  its own can re-fetch it; free-form objects; `additionalProperties` maps) and say why
  in a doc comment. At v0.4 a discriminated `oneOf` is a union or interface, mapped as
  `... kind->match([wire, { __typename: "Member", … }], …, [@, null])`
  (mapping-language.md § Abstract types). Never a typed guess that drops payload data.
- **An error's message path comes from the inventory's documented shape, never a guessed
  convention.** Read `errors[].shape_ref` for the operations a source's or connector's
  `errors` block covers before writing the expression (schema-authoring.md § Errors);
  `lint`'s `error-path-unresolved` checks it.
- **Every included operation gets executed evidence**: a case plus a scoped fixture, a
  unit entry when its arguments are scalars, and a conformance check against the spec or
  the inferred schema. A skipped layer is reported as skipped, never as a pass.
- **Fixtures are truth.** Never edit a recorded fixture to make a test pass — fix the
  schema, the case, or the expectation. Scrub before commit; a committed file names a
  credential's environment variable, never its value.
- **A `.factory/` file is a regular file, or nothing.** Every instrument reads and
  writes `.factory/*` through one custody module: a symlink at any component
  of the path — `.factory` itself, `sources/`, the file — is refused, on read and on
  write alike, and the message names the workspace-relative path, never the link's
  target. `refused — a symlink, not a regular file` means the *workspace* is wrong, not
  the tool: restore the real file (`git checkout --` it, or copy it in) and re-run.
  Never work around it by reading or writing the target yourself.
- **Account for everything.** Every operation the API has is `selected`,
  `excluded` (with a reason), `unsupported` (with a reason), or
  `unresolved`. "What was left on the table" is the question the user is
  actually asking.
- **Write it down — one test decides where:** *could a reasonable engineer
  have gone the other way, and would the service still be valid?* (the
  shapes are in workspace-contract.md)
  - Yes → `graphos-factory-core decisions add`, with the question and every
    alternative, resolved by the user or by you with `--note` saying why you
    were confident enough not to ask.
  - No, because a reference or the wire settles it →
    `graphos-factory-core findings add --cites …`, and only when an instrument
    needs its `omits` or `affects` or the next session needs the fact.
  - A vendor quirk, a dead endpoint, an auth detail → `memory.md`. Also
    `memory.md`, under `## Tried and rejected`: a negative result, an
    accepted residual no instrument can waive, a standing correction the
    user gave — none is derivable from current state, and the next session
    reads `memory.md`, not `git log`.
  - A measurement, a correction to an earlier record, a stash, "found and
    fixed" → the commit message, or an edit to the record it corrects.
  - Something the *next service* would want → `graphos-factory-core/references/lessons.md`.

  A spec correction is none of these: edit the working copy, then
  `graphos-factory-core codify --source` records it as `patches[]` in
  `sources.lock.yaml` with the reason; add the live evidence as `verified`.
<!-- core:end -->

- **Without the user's key the subgraph is checked alone.** Compose,
  unit, e2e, conformance and live prove the subgraph by itself; whether it
  composes with the user's other subgraphs is unverified until `supergraph_check`
  passes or they run `rover subgraph check` (references/verification.md). Say so in every report,
  and record any entity or `@shareable` choice as a decision (references/federation-subgraph.md).

<!-- core:begin -->
## Discover, then select, then apply

`discover` never edits the schema or selection. It rebuilds the inventory,
reports added / removed / changed operations, and assesses customer context.
It may persist requirements and authorized metadata snapshots; unresolved
inputs remain visible in `context.yaml`. The user changes `selection.yaml`
(by hand, through a host UI, or by asking you); only then does `apply` touch
the schema, and only for the operations the delta names.

## Hand edits: detect, codify, keep editable

`.factory/applied.lock.yaml` is the schema as you last wrote it, one hash
per span (header, each type, each root field by operation key), plus one for
each pinned document and one for `inventory.json`. Anything
that hashes differently is a **hand edit** — the engineer's or a host UI's —
and `graphos-factory-core reconcile`, `lock --check` and `lint` all name it. An
edited `inventory.json` has nothing to codify: it is built, never edited, so
rebuild it and put the correction where it belongs (the pinned document, or
`selection.yaml`). Nor is a root field whose path several operations match
equally (`unattributed-span`): declare its operation in `selection.yaml`;
`lock` and `codify` refuse it (schema-authoring.md).
**Never start an `apply` while one exists**: you could not tell it from
your own delta, and "correcting" it back toward the selection is the exact
failure this skill exists to prevent.

When you find one, codify it before anything else:

1. **Learn why.** Read the `git log` of the file and the diff of the span;
   ask the engineer if the reason is not obvious. Never invent one.
2. **Prefer the selection.** If the edit is something `selection.yaml` can
   say — a tag, a rename, an exclusion, a root, a name — put it there, check
   `graphos-factory-core reconcile` shows no drift for the operation, then
   `graphos-factory-core codify --key K --reason R --expressed`. The next apply
   reproduces the edit from the selection; nothing is frozen.
3. **Otherwise assert the intent.** `graphos-factory-core codify --key K --reason R
   --assert contains=… --assert tag=…` records an override: what must stay
   true of the span, not its bytes. Write assertions for the *point* of the
   edit (the comment that explains it, the ordering, the extra argument),
   not for incidental text. `--until` says when to revisit; `--expires`
   makes reconcile say so. `--pin` (no assertions) freezes the span and is
   a last resort — lint warns on it.
4. **Commit `decide:`.** codify wrote the why onto the override (`reason`,
   and `context` from `--context TEXT` for what the diff cannot show) and
   refreshed the lock; it records no decision, and `--decision D-id`
   only attaches the entry to a real one. Add a `memory.md` line when
   the reason is a vendor fact rather than a local preference.

An override does not lock an operation. When a later selection or inventory
change names an overridden span, edit it like any other, keep every
assertion true (reconcile checks them), say in the `apply:` commit which
intents you carried forward, and re-run `graphos-factory-core lock`. If a change
would make an assertion impossible, stop and ask — do not pick a side.
Read the override's `reason` and `context` before touching the span; that
is where the why lives.

**The same rules govern a pinned spec.** `graphos-factory-core sources pin
--path openapi.json` keeps the vendor's bytes untouched as
`.factory/sources/openapi.upstream.json` and acknowledges the working copy
in `applied.lock.yaml`; from then on `openapi.json` is editable exactly like
the schema. When the spec is wrong (a field the API sends as null, a missing
response, a wrong type), edit the working copy — never the upstream — and
codify it: `graphos-factory-core codify --source openapi.json --reason R`
computes the structural difference from the upstream (formatting never
counts) and records it as `patches[]` on the entry, each operation with the
reason (and `--context`, when given). `lock --check`, `reconcile` and `lint` name an
uncodified spec edit (`unacknowledged-source-edit`) and refuse an `apply`
until it is codified; a modified upstream is an error to restore, never to
codify. A newly fetched vendor document is refreshed in with
`sources refresh --path openapi.json --from FILE --reason R` (the patches
are replayed and each reported re-applied, obsolete or in conflict; a
finding records both shas and each patch's fate; the inventory is rebuilt and diffed; see
spec-intake.md), never codified as patches and never copied over the
working copy; exit 3 means a conflict whose intent you must re-apply by hand
and codify, exit 4 an interrupted write to restore with the `git checkout`
it names. Every `discover` reads the working copy, so the inventory marks the
operations a patch touches. Add `verified:` (the sample or page that proves
the vendor wrong) to a patch by hand; a patch without it is a guess.

## Finishing an `apply`

Report context readiness and any unresolved live requirements separately from
connector test results. Then report, in this order:

1. `graphos-factory-core lock --check` before you started (no hand edits);
2. operations added, changed, removed (the `graphos-factory-core reconcile` report
   before you edited, and its `clean` line after, with `changed since HEAD`
   naming only spans the delta covers);
3. every override: its assertions `ok`, its drift from the selection (the
   engineer's, reported not fixed), and whether you changed it and why;
4. the validation table from `evidence/latest.json`, naming every skipped
   or not-run layer and its reason;
5. the `graphos-factory-core lock` result, including the recorded skill revision,
   dirty state and commit hash.

The provenance record describes the authored state. The model value is
self-reported. It does not prove the model identity or the full session
history. It does not claim bit-for-bit replay.

Quote the passing tool output rather than describing it. If any selected
operation lacks executed evidence, the workspace is **not** validated — say
so plainly instead of listing the layers that did run.
<!-- core:end -->

When the user asks how the subgraph reaches their graph, answer from
references/export-graphos.md: `export`, then rover, which the user runs.

## References

- [`first-subgraph.md`](references/first-subgraph.md) — **the first subgraph in a new workspace**: the linear path from `init` to `export`, the expected non-zero exits, and the refusals a first run meets most
- [`customer-context.md`](graphos-factory-core/references/customer-context.md) — **read only when the intake is specialized or unclear** (step 3 gates it): the specialized workflow, missing inputs, discovery, questions, and the `context.yaml` requirements contract
- [`workspace-contract.md`](graphos-factory-core/references/workspace-contract.md) — files, shapes, git conventions
- [`connectors-language.md`](graphos-factory-core/references/connectors-language.md) — `@source`/`@connect`, expression variables, relationship fields, entities, errors, v0.3 vs v0.4
- [`mapping-language.md`](graphos-factory-core/references/mapping-language.md) — `selection`/`body`/`queryParams`: shapes, the methods the router runs, literals, absence, troubleshooting
- [`naming.md`](graphos-factory-core/references/naming.md) — prefixes, snake_case, the semantic root, aliasing
- [`schema-authoring.md`](graphos-factory-core/references/schema-authoring.md) — envelopes, pagination, argument constraints, scalar choice, enums, nullability, depth, the JSON policy
- [`spec-intake.md`](graphos-factory-core/references/spec-intake.md) — reading a description document (OpenAPI 3.x or Swagger 2.0); what `securitySchemes` and `security` become in the inventory; spec pathology classes; pinned specs and `patches[]`
- [`api-discovery.md`](graphos-factory-core/references/api-discovery.md) — the no-spec playbook: docs, probes, provenance, confidence; recording an OAuth flow from the docs
- [`testing.md`](graphos-factory-core/references/testing.md) — the eight layers, what each is blind to, and the traps
- [`selection-review.md`](graphos-factory-core/references/selection-review.md) — the `selection review` contract a UI or a headless agent uses to propose a selection change
- [`lessons.md`](graphos-factory-core/references/lessons.md) — cross-subgraph memory; append when you learn something vendor-independent
- [`federation-subgraph.md`](references/federation-subgraph.md) — versions from the user's graph, the directives a connector subgraph may carry and may not, entities another subgraph owns, `@tag` and contracts, what is still open
- [`export-graphos.md`](references/export-graphos.md) — when to export, the command and its gate, what the user runs (rover, the router), and what an export does not verify
- [`verification.md`](references/verification.md) — what the layers prove, `supergraph_check` (what it runs, the two variables, reading pass, fail and not_run), and the hand-off
