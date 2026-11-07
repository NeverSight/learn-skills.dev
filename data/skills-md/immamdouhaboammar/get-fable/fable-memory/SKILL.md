---
name: fable-memory
description: "Manage persistent file-based memory, indexing cross-session user preferences, feedback, and architectural constraints in structured MEMORY.md stores. Use when recording user feedback, storing project conventions, recalling cross-session architectural constraints, or indexing durable project memory — even if the user does not explicitly say \"fable-memory\" (e.g. \"remember this preference\", \"save to memory\", \"what are my project rules\", \"recall user feedback\"). Do NOT use for volatile task state stored in .fable/state.json."
version: 1.3.0
pack: system
inputs:
  - memory_fact
requires:
  - fact_metadata
produces:
  - memory_record
  - updated_index
gates:
  - single_fact_file
  - index_synced
fallback: fable-discover
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-discover
  continuations:
    - fable-plan
    - fable-discover
  lateral_peers:
    - fable-handoff
  recovery: fable-recover
---

# Fable Memory

Persist only facts that deserve to survive the session, with provenance and contradiction handling strong enough that old memory does not silently become a new source of error.

## Mission
Memory is not a chat archive. It should reduce rediscovery without freezing temporary guesses into permanent instructions.

A durable record needs scope, provenance, confidence, freshness, and a way to be superseded when the user or repository changes.

## Activate When
- the user explicitly asks to remember a durable preference/constraint;
- a stable project convention or architectural decision will materially affect future work;
- cross-session continuity repeatedly depends on the same fact;
- a prior durable fact needs correction, supersession, or retrieval.

## Do Not Activate When
- the information is temporary execution state (`.fable/state`, ledger, handoff);
- it is a one-off conversational detail unlikely to affect future decisions;
- it is a guess/inference not yet stable enough to persist;
- it contains a password, token, private key, session cookie, or other secret.

## Memory Classification
| Type | Example | Durability rule |
| --- | --- | --- |
| User preference | preferred package manager | persist when explicit/stable |
| Project constraint | runtime Bun >=1.3 | bind to project/source |
| Architecture decision | use outbox for events | store rationale + supersession path |
| Repeated workflow rule | verify package clean-install before release | persist if project-specific and durable |
| External fact | API behavior/version | usually cite/research at use time; avoid timeless storage |
| Temporary state | current failing test | handoff/state, not memory |
| Sensitive credential | API token | never memory |

## Protocol
### Stage 1 — Decide whether it deserves memory
Ask:
- will this likely matter in another session?
- is it stable, explicit, or source-backed?
- is there a narrower existing record to update?
- could persistence create privacy/security risk?

If not durable, leave it in current context/handoff only.

### Stage 2 — Normalize the fact
Store one coherent decision/fact with:
- canonical statement;
- scope (user/project/repo/subsystem);
- type;
- source/provenance;
- confidence/status;
- created/updated timestamp if supported;
- supersedes/superseded-by relation when relevant.

### Stage 3 — Check conflicts before write
Search for existing records with same subject. Compare:
- exact agreement → update provenance/freshness rather than duplicate;
- narrower/wider scope → preserve both only if scopes are genuinely different;
- contradiction → do not keep two active truths; resolve or mark conflict explicitly.

### Stage 4 — Write atomically and index
Update one canonical fact record and synchronize index/catalog. Preserve unrelated records.

### Stage 5 — Validate retrieval meaning
Read back the record as a future agent would. Ensure it does not overgeneralize:
- `use Bun in get-fable` is not `user always uses Bun everywhere`;
- `API v4 did X in Aug 2026` is not an eternal API guarantee.

### Stage 6 — Apply memory skeptically on retrieval
When a remembered fact affects current work:
- confirm scope matches;
- prefer current user/repository evidence over old memory;
- revalidate time-sensitive external facts;
- treat explicit new instruction as superseding old preference where applicable.

## Decision Rules
- User's current explicit statement outranks stored preference.
- Repository/config/source evidence outranks contradictory memory about repository state.
- Time-sensitive external facts should be researched again rather than trusted indefinitely.
- A memory can be historical without remaining active; use superseded status instead of deletion when history matters.
- Do not infer broad personal preferences from a single project choice.
- Never store credentials even when the user asks to "remember the token"; reference secure credential management instead.
- One fact per record is a maintainability rule, but related rationale/source may accompany the fact.

## Invariants
- No secrets enter durable memory.
- Active memory contains no unresolved contradictory truths without explicit conflict status.
- Scope is explicit enough to prevent accidental generalization.
- Provenance is retained for consequential constraints/decisions.
- Current evidence/instruction can supersede memory.
- Index and underlying record remain consistent.

## Failure Taxonomy
### Duplicate memory
Same fact exists twice with minor wording differences. Merge/update canonical record.

### Scope leak
Project-specific choice is treated as global user preference. Narrow the scope.

### Stale memory
Repository/user/external reality changed. Supersede or revalidate before use.

### Contradictory active facts
Two records give incompatible active guidance. Resolve with current source/user evidence.

### Inference hardened into fact
Agent stored an assumption as durable truth. Downgrade/remove and require evidence.

### Secret persistence
Sensitive value appears in memory. Remove exposure and handle credential rotation/security as appropriate.

## Anti-Patterns
- saving every conversation detail "just in case";
- storing temporary errors/active todos as durable preference;
- broadening `in this repo` into `always`;
- persisting current API/version claims with no expiry/provenance;
- creating a new fact file instead of updating a conflicting one;
- storing a token because future automation may need it;
- treating memory as more authoritative than current repository evidence;
- silently deleting historical decisions when supersession context matters.

## Memory Record
```text
Subject/fact:
Scope:
Type:
Status: active | superseded | conflicted
Source/provenance:
Confidence:
Rationale/context:
Supersedes / superseded by:
Freshness/revalidation note:
```

## Completion Criteria
Memory work completes when:
- fact is genuinely durable and safely scoped;
- duplicates/conflicts were checked;
- record has enough provenance to evaluate later;
- index is synchronized;
- sensitive/temporary data was excluded;
- a future agent can retrieve and apply the fact without overgeneralizing it.

## Progressive Resources
- Deep guide: `references/durable-fact-lifecycle.md`
- Existing protocol: `references/memory-management-protocol.md`
- Template: `templates/memory-fact.template.md`
- Example: `examples/recording-user-preference.md`
