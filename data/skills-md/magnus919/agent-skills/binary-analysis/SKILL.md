---
name: binary-analysis
description: >-
  Analyze unknown binary files through a deterministic CLI that wraps Ghidra's
  static-analysis engine. Use when you need to inspect a PE, ELF, or Mach-O
  file — triage suspicious binaries, map imported APIs, decompile functions,
  trace call paths, or produce structured evidence reports. Do not use for
  runtime analysis (debugging, dynamic tracing, sandbox execution), for
  modifying or patching binaries, or for binaries you already know everything
  about. The skill owns planning, hypothesis formation, and evidence synthesis;
  the CLI owns all deterministic operations.
license: MIT
compatibility: Requires Python 3.12+, Java JDK 21+, Ghidra 12.1+, PyGhidra 3.1+
metadata:
  tags: binary-analysis, reverse-engineering, security, malware-analysis, static-analysis, ghidra
  skill_version: "1.0.0"
  cli_entrypoint: scripts/binary
  required_skill: none
  uses: scripts/binary_analysis/
---

# Binary Analysis — Agent Skill

Analyze unknown binary files with a deterministic, non-interactive CLI backed by
Ghidra's static-analysis engine. The skill teaches you how to reason about
binaries: when to triage versus deep-dive, how to interpret canonical evidence,
and how to produce auditable reports. All observable operations happen through
the `binary` CLI — you never call Ghidra APIs directly.

## When to Use

Load this skill when any of the following conditions match:

- A user provides a binary file (PE, ELF, Mach-O, firmware image) and asks what
  it does, what APIs it imports, or whether it is suspicious.
- A user asks for decompilation, disassembly, call-graph exploration, or
  cross-reference analysis of a specific function or address.
- A user wants a structured triage report, suspicious-API analysis, or
  capability map for an unknown binary.
- A user asks to compare two binaries, verify export tables, or extract strings
  matching a pattern.
- A user wants to set up the analysis toolchain (`binary doctor`, `binary
  bootstrap`) or manage analysis projects.

## When Not to Use

Do **not** load this skill for:

- **Runtime or dynamic analysis** — debugging, strace/dtrace, sandbox
  execution, process monitoring. This skill is static-analysis only (V1).
- **Binary patching or modification** — hex-editing, resource editing,
  repackaging. The analysis harness is read-only by design.
- **Binaries you already fully understand** — if the user is asking for
  documentation or explanation of known code, use a general-purpose skill.
- **Source-code analysis** — C, C++, Rust, or assembly source files. Use a
  language-specific or general code-analysis skill instead.
- **Network forensics or packet capture** — PCAP analysis, protocol reverse
  engineering at the wire level. Use a network-focused skill.
- **Live memory forensics** — process memory dumps, heap analysis. Static
  analysis of memory-mapped regions from files is in scope; live-process
  introspection is not.

## What the Agent Owns vs What the CLI Owns

This boundary is the most important concept in the skill. Crossing it produces
unreliable evidence, wasted context, or both.

| Layer | Responsibility | Must NOT |
|-------|---------------|----------|
| **Agent (you)** | Form hypotheses about binary behavior. Choose which analyses to run and in what order. Synthesize CLI evidence into conclusions. Explain findings to the user in plain language. Write evidence-backed reports. | Invent facts not present in CLI output. Claim certainty where the CLI reports partial results or low confidence. Skip diagnostic warnings. |
| **CLI** | Parse arguments, manage project lifecycle, run Ghidra analysis, serialize canonical entities, emit JSON envelopes, enforce safety limits. | Interpret results, draw conclusions, or produce narrative prose. |

**Rule of thumb:** If a fact appears in a CLI JSON response under `data`, it is
deterministic evidence you can cite. If you are tempted to infer something not
directly supported by that evidence, flag it as an agent inference and note the
confidence gap.

## Core Workflow

Every analysis session follows this sequence. Do not skip phases — each one
produces evidence the next phase depends on.

### Phase 1: Environment Check

```bash
binary doctor --json
```

If any component reports `severity: "ERROR"`, run the bootstrap plan:

```bash
binary bootstrap --plan --json
```

Review the plan. If the user authorizes installation, run:

```bash
binary bootstrap --apply --json
```

Verify with `binary version --json`.

### Phase 2: Project Setup

Create a project for every binary you analyze. Projects isolate analysis state
and provide an audit trail.

```bash
binary project create <project-name> --json
binary import <path-to-binary> --project <project-name> --json
```

Use copy mode (default) for reproducibility. Use `--reference` only when the
binary is large, read-only, or shared across projects, and explain the
staleness risk to the user.

### Phase 3: Initial Analysis

Run the standard analysis profile first. It covers the structural queries most
triage workflows need.

```bash
binary analyze --project <project-name> --json
```

Check the response:
- `success: true, partial: false` — proceed to Phase 4.
- `success: true, partial: true` — review `diagnostics` for gaps. Proceed with
  bounded results, noting limitations.
- `success: false, partial: true` — timeout. Extract what completed, report
  what did not.
- `success: false, partial: false` — hard failure. Check `diagnostics` for the
  failure reason. The project is now FAILED; run `binary project clean` to
  reset.

### Phase 4: Evidence Collection

Choose analyses based on the user's question. Run these in order, building
evidence from broad to specific.

**For triage (broad survey):**
```bash
binary triage --project <project-name> --json
binary suspicious-apis --project <project-name> --json
binary capability-map --project <project-name> --json
```

**For structural understanding:**
```bash
binary metadata --project <project-name> --json
binary sections --project <project-name> --json
binary entrypoints --project <project-name> --json
binary imports --project <project-name> --json
binary exports --project <project-name> --json
binary strings --project <project-name> --contains "<pattern>" --json
```

**For function-level deep-dive:**
```bash
binary functions --project <project-name> --json
binary decompile --project <project-name> <function-selector> --json
binary disassemble --project <project-name> <target> --json
binary xrefs --project <project-name> <entity-selector> --json
binary callers --project <project-name> <function-selector> --json
binary callees --project <project-name> <function-selector> --json
binary callgraph --project <project-name> <function-selector> --depth 3 --json
```

**For path analysis:**
```bash
binary trace --project <project-name> --from <source> --to <target> --json
```

### Phase 5: Report and Handoff

Generate a durable report before explaining results to the user:

```bash
binary export-report --project <project-name> --type triage --format markdown --json
```

Read the report. Synthesize findings into a clear explanation. Always mark
agent inferences separately from CLI evidence. Example:

```
## CLI Evidence (deterministic)
- The binary imports VirtualAlloc, WriteProcessMemory, and CreateRemoteThread
  (suspicious-apis, risk_score 8, rule_id: process-injection)
- Entry point at 0x401000, 3 sections (.text, .rdata, .data)

## Agent Assessment (inference)
- The API combination suggests process injection capability. This is a
  heuristic, not a confirmed behavior. The binary would need to be executed
  (out of scope for static analysis) to confirm.
```

## Safety Boundaries

The CLI enforces these boundaries automatically. You must never attempt to
bypass them, even if a user asks.

| Boundary | Enforcement | Why |
|----------|-------------|-----|
| **Never execute the target** | CLI refuses; no execution path exists | Static analysis only |
| **Never load target as a library** | Not implemented; no dlopen/LoadLibrary path | Prevents unintended code execution |
| **Never expose a network listener** | No HTTP, MCP, or socket servers | The CLI is a local tool |
| **Never upload hashes or samples** | No telemetry, no outbound calls | Privacy and security |
| **Path containment** | All project paths validated for traversal | Prevents workspace escape |
| **Output size limits** | Default 64 MB, max 256 MB JSON | Prevents context exhaustion |
| **Memory limits** | Configurable per-operation ceiling | Prevents OOM during large analyses |
| **Timeout enforcement** | Default 300s, configurable per-command | Bounded operations |
| **Result count limits** | Paginated with default 100, max 1000 | Prevents unbounded output |
| **Graph depth limits** | Callgraph capped at depth 10 | Prevents infinite recursion |

## Evidence Standards

All CLI evidence follows a confidence hierarchy. Use these standards when
citing evidence in reports or explanations.

### Evidence Categories (triage output)

| Category | Definition | Example |
|----------|-----------|---------|
| **Observation** | Direct deterministic fact from the backend. No `confidence` field. | "Section .text is executable, size 4096 bytes" |
| **Heuristic** | Rule-derived interpretation with explicit `confidence`. | "Suspicious API: VirtualAlloc (risk_score: 8, confidence: HIGH)" |
| **Unknown** | Explicit unresolved question at a specific address. | "Indirect call target at 0x402080 could not be resolved" |

### Confidence Levels

| Level | Meaning | When to cite |
|-------|---------|--------------|
| `HIGH` | Backend is certain about this result | Cite as fact |
| `MEDIUM` | Backend has reasonable confidence | Cite with qualification ("likely") |
| `LOW` | Backend made a best-guess | Cite only with explicit caveat |
| `UNKNOWN` | Backend could not determine | Present as an open question |

### Agent Inferences

When you synthesize multiple CLI observations into a conclusion, label it
explicitly as an agent inference. Never present an inference as a CLI fact. Use
language like:

- "Based on the combination of X and Y, the agent assesses that..."
- "The CLI reports Z as a heuristic (confidence: MEDIUM). The agent interprets
  this as consistent with..."
- "The CLI could not determine W. The agent notes this is an open question."

## Reference Routing

References are loaded on demand — do not read them all at startup. Use this
table to route your current task to the right reference file.

| Reference | When to Load |
|-----------|-------------|
| [references/installation.md](references/installation.md) | Setting up Ghidra, Java, or PyGhidra. Running `binary doctor` or `binary bootstrap`. Dependency troubleshooting. |
| [references/cli-reference.md](references/cli-reference.md) | Need the complete command reference with flags, exit codes, and examples. Unfamiliar with a specific command or flag. |
| [references/triage-workflow.md](references/triage-workflow.md) | Performing a triage on an unknown binary. Need the step-by-step triage methodology and interpretation guide. |
| [references/function-analysis.md](references/function-analysis.md) | Decompiling, disassembling, or tracing a function. Understanding decompiler output or call-graph analysis. |
| [references/binary-formats.md](references/binary-formats.md) | Identifying or interpreting PE, ELF, or Mach-O format characteristics. Understanding section flags, entry point conventions, or format-specific quirks. |
| [references/security.md](references/security.md) | Interpreting suspicious-API results, capability maps, or security rule matches. Understanding risk scoring and rule priorities. |
| [references/evidence-and-confidence.md](references/evidence-and-confidence.md) | Writing reports that distinguish CLI evidence from agent inferences. Building an evidence-backed argument. |
| [references/packed-and-obfuscated.md](references/packed-and-obfuscated.md) | Suspicious that a binary is packed, compressed, or obfuscated. High entropy sections, missing imports, or small import tables. |
| [references/firmware.md](references/firmware.md) | Analyzing firmware images. Need firmware-specific load address conventions, filesystem extraction patterns, or boot-loader analysis. |
| [references/troubleshooting.md](references/troubleshooting.md) | CLI returns unexpected errors, timeouts, or partial results. Ghidra fails to start. Project state is stuck. |
| [references/reporting.md](references/reporting.md) | Generating reports with `binary export-report`. Choosing report types and formats. Interpreting report structure. |

## Reporting Expectations

Every analysis session must produce at least one of these outputs before the
agent considers the task complete:

1. **Triage report** — for unknown binaries. Covers observations, heuristics,
   unknowns, and an agent assessment section clearly separated from CLI
   evidence.
2. **Focused analysis** — for targeted questions about a specific function,
   import, or behavior. Answers the user's question with CLI evidence first,
   agent interpretation second.
3. **Capability summary** — for "what does this binary do" questions. Maps
   functional areas with evidence sources and confidence levels.

Reports must:
- Separate CLI evidence (deterministic) from agent assessment (interpretation).
- Cite confidence levels for every heuristic claim.
- Include provenance: project ID, binary SHA-256, adapter and backend versions.
- Note partial results, timeouts, or diagnostic warnings — do not hide
  limitations.

## Verification Matrix

Before presenting results to the user, verify:

| Check | How |
|-------|-----|
| CLI commands all returned `success: true` or documented `partial: true` | Check `success` and `partial` in each response envelope |
| No diagnostic warnings were silently ignored | Review `diagnostics` array in every response |
| Evidence citations are traceable to CLI output | Every factual claim matches a field in a `data` block |
| Agent inferences are explicitly labeled | Search your output for unqualified claims |
| Project state is clean | Run `binary project status --project <name> --json` |
| Report was generated and reviewed | Report file exists in project `reports/` directory |

## Exit Criteria

Stop and report results when:

- A triage report has been generated and the user's question is answered with
  evidence-backed findings.
- A focused analysis has produced the specific information requested (decompiled
  function, call path, import list) with provenance.
- Three non-converging diagnostic passes have been attempted for the same issue.
  Report the evidence gathered and the blocker.
- The binary format is unsupported (exit code 5). Report the format limitation.
- A hard dependency is missing and the user declines to install it. Report the
  gap.

Do not stop after a single structural query unless it fully answers the user's
question. Static analysis is iterative — broad survey, then deep-dive.
