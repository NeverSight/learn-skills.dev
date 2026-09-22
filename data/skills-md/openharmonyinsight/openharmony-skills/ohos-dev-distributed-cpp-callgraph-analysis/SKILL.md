---
name: ohos-dev-distributed-cpp-callgraph-analysis
description: Use when an OpenHarmony C++ change must be checked for call-chain completeness, especially for data propagation, IPC/proxy/stub paths, virtual overrides, callbacks, or dlopen/dlsym boundaries. Produces evidence tables and modification coverage matrices; the helper script only discovers candidate edges.
metadata:
  author: openharmony
  scope: distributed
  stage: development
  domain: cpp
  capability: callgraph-analysis
  version: 0.2.0
  status: draft
---

# OpenHarmony Call-Chain Completeness Analysis

This skill has one decision layer plus optional tool support:

1. **Agent workflow**: the only layer that can judge call-chain completeness. It uses LSP/source evidence, edge classification, and a coverage matrix.
2. **Optional artifact fallback**: `ohos_callgraph.py` discovers candidate direct call edges and best-effort vtable/dlopen hints from build artifacts when LSP/source evidence leaves gaps or LSP is unavailable.

Do not claim a call chain is complete from script output alone.

## Bootstrap Repository-Scoped LSP

Before analysis, check whether a working LSP/MCP tool is already backed by the correct OpenHarmony
product compile context. Use it when available.

If LSP is missing or resolves the repository incorrectly, read
[`references/lsp-bootstrap.md`](references/lsp-bootstrap.md) and follow it before analysis. The
bootstrap is optional support, not a prerequisite: if setup or smoke testing fails, record LSP as
unavailable/incomplete and continue with source, build, symbol, helper, and runtime evidence.

If clangd is extremely slow on a specific file (minutes of 100% CPU), the file is likely missing from
the filtered `compile_commands.json`. For Claude clients, pass `--install-hook` during setup to
install a Claude PreToolUse auto-fix hook. For Codex or other clients, use the manual fix in the
"File Not in compile_commands.json" section in
[`references/lsp-bootstrap.md`](references/lsp-bootstrap.md).

## Required Workflow

### 1. Define the Analysis Target

Before using tools, state:

- Entry point or event path, such as `OnRemoteRequest`, `HandleEvent`, or a subsystem-specific entry function.
- Target data or behavior, such as a propagated field, routing decision, or state transition.
- Scope boundaries to include: client/server, IPC, callbacks, virtual interfaces, dlopen/dlsym implementations, generated code, and tests.
- Scope boundaries intentionally excluded, with reasons.

If any of these are unknown, inspect code first and make a bounded assumption. Do not skip this step.

### 2. Discover Candidate Edges

Use evidence sources in this order:

1. **LSP / clangd**: preferred static source for definitions, declarations, references, call hierarchy, override candidates, and macro-aware symbol locations.
2. **Source search**: use `rg` to find framework patterns that LSP does not model well, such as transaction codes, listener registration, `LoadLibrary<>`, `dlsym`, and generated-file names.
3. **Build graph and symbol tools**: use GN/Ninja, `llvm-nm`, `llvm-readelf`, `llvm-objdump`, and `llvm-cxxfilt` for libraries, exports, link edges, and generated artifacts.
4. **Helper script, only if needed**: use `ohos_callgraph.py` to discover IR-level candidate direct edges and best-effort vtable/dlopen hints when LSP/source/build evidence still has unexplained edges, when artifact-level confirmation is useful, or when LSP is unavailable/incomplete.
5. **Runtime trace**: use logs, instrumentation, or symbolized traces when static evidence cannot uniquely resolve virtual, callback, IPC, or dlopen/dlsym edges.

LSP is the first choice for language-level C++ facts, but it is not enough for runtime binding or OpenHarmony framework protocols.

When LSP/clangd is available, use it as the primary path for:

- `definition` / `declaration`
- `references`
- `call hierarchy` incoming/outgoing calls
- override and implementation candidates
- macro-expanded symbol locations

Do not run the helper script just to duplicate LSP direct-call results. Run it only when it can answer a different question, such as "does this compiled artifact contain a candidate edge?" or "what candidates exist when LSP cannot resolve this path?".

When LSP is unavailable or incomplete, say so in the evidence table and fall back to source search plus build/symbol evidence.

#### Helper Script

**Resource check**: before running the helper, estimate the bitcode file count with `find <obj_dir> -name '*.o' | grep <repo-filter> | wc -l`. If the count exceeds ~200 files, narrow the `--repo` filter or use LSP/source evidence instead. Each file requires two LLVM tool invocations (~1-2s each), so 200 files can take 5-10 minutes.

Required helper invocation shape. The agent must resolve the source tree and repository filter before calling the script, then pass them explicitly:

```bash
SCRIPT=/path/to/skills/ohos-dev-distributed-cpp-callgraph-analysis/ohos_callgraph.py
python3 "$SCRIPT" <entry-function> \
  --oh-root <openharmony-source-root> \
  --product <product-name> \
  --repo <repo-filter> \
  --depth 4 \
  --skip-prefix "Subsystem::LogHelper" --skip-prefix "Subsystem::TimeUtil"
```

Omit `--skip-prefix` to use the built-in defaults (HiLog, std::__h::, etc.). Pass one or more `--skip-prefix` to override them entirely with subsystem-specific prefixes.

Reverse direct callers:

```bash
python3 "$SCRIPT" <target-function> \
  --oh-root <openharmony-source-root> \
  --product <product-name> \
  --repo <repo-filter> \
  --reverse \
  --depth 3
```

The helper script output is a candidate list. Every important edge still needs source evidence.
In reverse mode, the helper script only reverses direct call edges. It does not reverse vtable or dlopen/dlsym hint edges.

### 3. Classify Every Edge

Each call-chain edge must be classified:

| Type | Evidence Required |
|------|-------------------|
| `direct` | Prefer LSP call hierarchy/references; include caller line and callee definition or declaration |
| `virtual` | Prefer LSP override candidates; include interface call site, candidate overrides, and dispatch reason if known |
| `callback` | Registration site and invocation site; LSP can locate symbols but usually cannot prove registration-to-invocation flow |
| `ipc` | Proxy write, stub read, transaction code, and service handler |
| `dlopen/dlsym` | Load site, library/symbol name, factory or function pointer use; confirm with symbols or trace when needed |
| `macro/generated` | Prefer LSP macro-aware locations; include generated source or expanded target that proves the edge |
| `unknown` | Evidence gap; cannot support a completeness claim |

For virtual, callback, IPC, and dlopen/dlsym edges, list all relevant candidates or explicitly justify why only one candidate applies.

### 4. Build the Evidence Table

Output a table with these columns:

| Caller | Callee / Candidate | Edge Type | Evidence Source | Evidence | Confidence | Needs Change | Change Status |
|--------|--------------------|-----------|-----------------|----------|------------|--------------|---------------|

Rules:

- `Evidence Source` is one or more of `lsp`, `source`, `build`, `symbol`, `script`, `runtime`, or `manual`.
- `Evidence` must include file paths and line numbers.
- `Confidence` is `confirmed`, `candidate`, or `unknown`.
- `Needs Change` explains why the target data or behavior must pass through this edge.
- `Change Status` is `done`, `missing`, `not needed`, or `unknown`.
- `script` evidence alone cannot make a non-direct edge `confirmed`.

Do not collapse multiple edge types into one row.

### 5. Build the Modification Coverage Matrix

For data propagation changes (e.g. a field that must be carried through multiple layers), check each applicable surface:

| Surface | What to Check | Static Evidence | Runtime Evidence | Status |
|---------|---------------|-----------------|------------------|--------|
| Function signature | Parameter or object carries the target data | LSP definition/declaration or source line | Optional | |
| Call arguments | Caller passes the correct value, not a default or stale value | LSP call hierarchy/references or source line | Optional | |
| Event/object fields | Field is set, copied, cloned, and reset correctly | Source/LSP field references | Optional | |
| IPC proxy/stub | Parcel write/read order and transaction compatibility | Source transaction and Parcel evidence | Trace/log if ambiguous | |
| Service dispatch | Server side receives and uses the value | Source/LSP handler path | Trace/log if ambiguous | |
| Virtual overrides | All reachable overrides accept or derive the value | LSP override candidates and source evidence | Required if static dispatch is not unique | |
| Callback flow | Registration and invocation both preserve the value | Source registration/invocation evidence | Required if registration-to-call flow is ambiguous | |
| dlopen/dlsym implementation | Loaded implementation handles the value | Source + symbol/build evidence | Required if loaded target is runtime-dependent | |
| Generated code | Generated wrappers and ABI layers preserve the value | Generated source or build artifact evidence | Optional | |
| Tests | Unit/system tests exercise at least one representative path and boundary | Test source evidence | Test execution result when available | |

The final answer must say which rows are complete, missing, or unknown.

### 6. Decide Completeness

Use these labels:

- **Complete**: all relevant confirmed and candidate edges have `done` or `not needed`, and unknowns are either resolved or explicitly out of scope.
- **Incomplete**: at least one required edge or surface is `missing`.
- **Not provable**: important edges remain `unknown`, or static-only evidence cannot resolve a runtime-bound edge that affects the conclusion.

## Helper Script Scope

`ohos_callgraph.py` is an optional artifact fallback after LSP/source inspection:

- Direct IR call edges from `opt --print-callgraph`
- Best-effort vtable interface hints from LLVM IR metadata
- Best-effort dlopen hints from common `LoadLibrary<>` / `CreateInstance` patterns
- Reverse direct callers only; reverse mode does not include vtable or dlopen/dlsym hint edges

Limitations:

- It does not prove all possible C++ calls.
- It does not resolve runtime virtual dispatch to a unique override.
- It does not prove callback, function pointer, or `std::function` targets.
- It does not prove IPC parameter propagation.
- It does not prove field propagation. `--name-keyword` only checks demangled function names and direct child function names as a rough hint; it does not inspect C++ parameter names, call arguments, member access, local variables, or IPC serialization.
- It may miss edges when build artifacts are stale, missing bitcode, optimized differently, or external tools fail.

Use the helper script only as a candidate discovery aid for the evidence workflow. Skip it when LSP/source evidence already covers the relevant direct calls and no artifact-level confirmation is needed.

## LSP Guidance

Use LSP/clangd as evidence when it is backed by the correct compile context for the OpenHarmony product under review. If the repository lacks `compile_commands.json` or clangd cannot resolve includes/macros, mark LSP evidence as incomplete and rely on source/build evidence instead.

When LSP is unavailable and the environment permits setup, follow **Bootstrap Repository-Scoped
LSP** before falling back. Do not use a product-wide compilation database directly when a
repository-scoped database can be generated; the product database can be several gigabytes and
causes unnecessary indexing cost.

Recommended LSP-backed checks:

- For a direct function call, use outgoing call hierarchy or go-to-definition from the call site, then record the caller and callee file lines.
- For reverse analysis, use incoming call hierarchy and references, then validate the call site manually.
- For virtual calls, use implementation/override queries to list candidates. Keep candidates as `candidate` unless construction/registration/source rules or runtime trace proves the actual target.
- For macros, use the resolved symbol location from LSP, then record the macro or generated expansion source when relevant.

Do not use LSP alone to confirm callback flow, IPC dispatch, or dlopen/dlsym targets.

## Required Final Response Shape

When using this skill, end with:

1. **Scope**: entry point, target data/behavior, included boundaries.
2. **Evidence Table**: edge-by-edge evidence source, evidence, confidence, and status.
3. **Coverage Matrix**: modification surfaces with static evidence, runtime evidence, and status.
4. **Conclusion**: `Complete`, `Incomplete`, or `Not provable`, with the exact missing or unknown items.

If you cannot inspect a required boundary, say so and mark it `unknown`.

## Example: MMI Subsystem

When analyzing the multimodal input (MMI) subsystem, common analysis targets include:

- **Entry points**: `HandleMouseEvent`, `UpdateMouseTarget`, `OnRemoteRequest`
- **Propagated fields**: `groupId`, `displayId`, pointer target routing, device binding
- **Skip prefixes**: `OHOS::MMI::FormatLog`, `OHOS::MMI::GetSysClockTime`, `OHOS::MMI::InnerFunction` (pass via `--skip-prefix`)
- **Key boundaries**: client/server IPC via `MultimodalInputConnectStub`, `EventDispatchHandler` callback chains, `InputDeviceManager` dlopen loading
