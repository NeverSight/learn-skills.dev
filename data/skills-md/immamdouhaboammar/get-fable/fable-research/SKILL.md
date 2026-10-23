---
name: fable-research
description: "Resolve current external facts, official documentation, library behaviors, and API contracts against primary sources before implementation. Use when consulting library documentation, checking breaking changes, investigating external APIs, or verifying framework versions — even if the user does not explicitly say \"fable-research\" (e.g. \"check the latest docs\", \"what is the API for X in version Y\", \"look up SDK specs\", \"verify library support\"). Do NOT use for repository-local code exploration (use fable-discover) or for writing implementation code directly (use fable-tdd or fable-execute)."
version: 1.3.0
pack: intelligence
inputs:
  - research_query
requires:
  - primary_sources
produces:
  - research_evidence
  - source_backed_facts
gates:
  - primary_source_grounding
fallback: fable-discover
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - fable-discover
  continuations:
    - fable-plan
    - fable-tdd
    - fable-execute
  lateral_peers:
    - fable-discover
  recovery: fable-recover
---

# Fable Research

Resolve external facts that can change the implementation, using current primary evidence instead of model memory.

## Mission
Research is not link collection. The output must be a decision-ready statement tied to the exact version, environment, or contract the repository will use.

## Activate When
- SDK/API signatures, limits, defaults, lifecycle semantics, or compatibility may have changed;
- a design depends on current cloud/provider behavior;
- the repository pins a version that may differ from current docs;
- multiple official sources appear to disagree;
- an error may come from a documented breaking change or deprecation;
- a standard/RFC/security requirement must be interpreted precisely.

## Do Not Activate When
- the fact is repository-local (`fable-discover`);
- the implementation is already grounded and only needs execution (`fable-execute`/`fable-tdd`);
- the task is general brainstorming where no external claim changes the decision.

## Research Classification
Classify the question first.

| Question type | Best primary evidence | Extra risk |
| --- | --- | --- |
| API signature | versioned official docs + source/types | docs may show latest, repo pins older |
| Runtime behavior | official docs + upstream implementation/tests | marketing docs may omit edge behavior |
| Compatibility | release notes/changelog + version matrix | transitive dependency constraints |
| Standard/protocol | normative spec/RFC | examples may be non-normative |
| Cloud/product limit | current vendor docs | region/tier/account differences |
| Security guidance | official security docs/advisories | stale blog summaries |
| Deprecation/migration | migration guide + release notes | old and new APIs coexist |

## Protocol

### Stage 1 — Turn the task into answerable claims
Break a broad request into the smallest external claims that can affect design.

Bad: "Research the new SDK."

Good:
- Does version 4.2 expose streaming tool-call deltas?
- Which parameter enables them?
- Is the callback ordered?
- What minimum runtime version is required?

### Stage 2 — Bind to repository reality
Before accepting current docs as applicable, record:
- package/version actually used;
- runtime/language version;
- relevant feature flags/tier/region if applicable;
- whether the repository uses generated types or a wrapper that changes the public contract.

### Stage 3 — Use a source hierarchy
Prefer, in order when available:
1. normative specification or official versioned reference;
2. official upstream source/types/tests;
3. official release notes/migration guides/advisories;
4. vendor examples authored for the relevant version;
5. secondary sources only as leads.

Never use an unsourced search snippet as final evidence.

### Stage 4 — Reconcile version and source conflicts
If latest docs disagree with the pinned package:
- inspect versioned docs/release notes/source for the pinned version;
- state the delta explicitly;
- do not silently recommend latest syntax to an older lockfile.

If two official sources disagree, prefer the one closest to executable truth for the exact version, and report the conflict.

### Stage 5 — Separate fact from interpretation
Record:
- **Fact**: what the source establishes;
- **Applicability**: why it applies to this repo/version;
- **Interpretation**: what it means for the design;
- **Confidence**: measured / strongly supported / unresolved.

### Stage 6 — Stop when the decision is grounded
Do not continue reading once all load-bearing external claims are resolved and the next action is safe.

## Decision Rules
- If a fact could have changed since model training, verify it rather than recall it.
- If docs are unversioned and the repo pins an older version, inspect source/types/changelog for that exact version.
- If an official quickstart conflicts with a normative reference, do not flatten the disagreement; determine which governs the target behavior.
- If behavior depends on account/tier/region, label that dependency and avoid universal claims.
- If no primary source is available, report the evidence gap and use upstream code/types/tests as the next-best source; never invent missing parameters.
- If the answer changes architecture, hand off to `fable-plan`; if it simply confirms a bounded implementation contract, hand off to `fable-tdd` or `fable-execute`.

## Invariants
- Every load-bearing external claim has a source.
- Source applicability includes version/context, not just URL authority.
- Quotes/signatures are kept short and exact; conclusions are written in the agent's own words.
- Secondary sources do not override accessible primary sources.
- Conflicting evidence remains visible until resolved.

## Failure Taxonomy
### Freshness failure
The source is official but stale/deprecated. Find versioned/current material and release history.

### Version mismatch
The repo and docs describe different versions. Reconcile against the lockfile/package metadata.

### Authority mismatch
A blog/example contradicts normative docs or upstream source. Demote the weaker source.

### Context mismatch
The claim differs by region, tier, runtime, platform, or feature flag. Scope the conclusion.

### Interpretation ambiguity
The source is clear but its implication for the repository is not. Hand the unresolved design question to `fable-plan` rather than pretending the research answered it.

## Anti-Patterns
- asking a search engine for a signature and copying the snippet;
- citing the latest docs without checking the pinned version;
- collecting many links without a decision-ready conclusion;
- using model memory because the API "probably hasn't changed";
- quoting a source without saying why it applies;
- hiding official-source disagreement;
- continuing research after every load-bearing claim is resolved.

## Research Packet / Handoff

```text
Question:
Repository version/context:
Source-backed facts:
- fact → primary source → applicability
Conflicts/version deltas:
Interpretation for implementation:
Confidence / unresolved:
Recommended next Skill:
```

## Completion Criteria
Research is complete when:
- the exact external claim is answered for the repository's actual context;
- evidence is primary or the absence of primary evidence is explicit;
- version conflicts are reconciled;
- the implementation/design implication is stated without overclaiming;
- no load-bearing parameter or semantic remains ambiguous.

## Progressive Resources
- Deep guide: `references/source-reconciliation-playbook.md`
- Existing hierarchy: `references/primary-source-hierarchy.md`
- Example: `examples/research-api-specs.md`
