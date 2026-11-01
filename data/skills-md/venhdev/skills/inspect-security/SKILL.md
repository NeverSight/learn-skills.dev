---
name: inspect-security
description: "Audit source code for threat exposure, authentication flaws, injection sinks, SSRF, concurrency races, and security debt."
disable-model-invocation: true
---

# inspect-security — Software Security & Threat Exposure Auditor

## Domain Rubric

### 1. Scope & Tolerability Guardrails (What to Ignore)

- **Mandatory Target Scope**: The user MUST specify an explicit target path (`file`, `directory`, or `subsystem`). If no target scope is provided, halt turn immediately and prompt user: `"Vui lòng chỉ định rõ phạm vi kiểm tra (file, thư mục hoặc subsystem) khi sử dụng /inspect-security."`; forbid speculative full-repository scans.
- **Vulnerability Debt vs. Linter Nits**: Confine analysis strictly to actionable threat exposure, broken authorization, cryptographic flaws, taint sinks, and concurrency races; defer basic AST formatting, syntax stylistic preferences, and whitespace entirely to native linters.
- **Governing Reference**: Evaluate security patterns strictly against `references/security-rubric.md`.

### 2. Decision Bifurcation: [LOCAL-FIX] vs. [ARCHITECTURAL-REFACTOR]

- `[LOCAL-FIX]` (Localized In-Function Patch): Parameterizing raw ORM queries, replacing `Math.random()` with CSPRNG, adding constant-time `timingSafeEqual` with pre-hashing, strict DTO schema whitelisting, wrapping streams in `io.LimitReader`, or pinning JWT algorithms. Route behavior-changing remediation to `/changeset`; use `/forge` only with a supported, authorized changeset.
- `[ARCHITECTURAL-REFACTOR]` (Systemic Structural Hardening): Introducing PostgreSQL Row-Level Security (RLS) for tenant isolation, deploying dedicated Egress Proxies (Smokescreen/Envoy) for SSRF mitigation, implementing Token Family refresh rotation with breach cascades, transitioning balance mutations to atomic conditional SQL / ledgers, or introducing distributed sliding-window rate limiting. Route remediation to `/changeset`.

## Canonical Output Contract

```markdown
# Security Audit Dossier: <Target Scope>

## 1. Executive Summary
- **Target Inspected**: `<directory_or_file_path>`
- **Security Posture**: <HARDENED | LOCALIZED_RISKS | CRITICAL_EXPOSURE>
- **Primary Threat Vector**: <Single-sentence summary of highest-severity exploit scenario or systemic hazard>

## 2. Load-Bearing Defect Catalog
### [<CRITICAL | HIGH | MEDIUM>] [<LOCAL-FIX | ARCHITECTURAL-REFACTOR>] <Dimension>: `<Target Symbol / Route>`
- **Offending Code**: [<file>#L<N>](file:///path/to/file#L<N>)
- **Violated Rubric**: [<spec_or_dimension>](references/security-rubric.md#anchor)
- **Threat & Exploit Scenario**: <Observable attack vector, failure mode, or privilege escalation scenario>
- **Action**: <[LOCAL-FIX] Local patch OR [ARCHITECTURAL-REFACTOR] Systemic architecture hardening>

*(Emit 'No load-bearing security defects observed across rubric dimensions' if clean)*
```

### Routing

- A supported changeset already authorizes the security fix and required verification → (via /forge).
- Local or systemic security patches requiring scope staging, including authorization, crypto, or data-contract changes → (via /changeset).

## Execution Protocol

1. **Intake & Scope Gate**:
   - Ingest target scope (`file`, `directory`, or `subsystem`).
   - **Enforce Scope Gate**: If no explicit scope is provided, halt turn immediately and prompt user: `"Vui lòng chỉ định rõ phạm vi kiểm tra (file, thư mục hoặc subsystem) khi sử dụng /inspect-security."`
   - Read and ground in `references/security-rubric.md`.

2. **Scale-Adaptive Pragmatic Audit**:
   - In-Turn Execution (< 10 files or cohesive module): Audit code directly in-turn against rubric dimensions.
   - Subagent Fan-Out (broad multi-package subsystem): Launch concurrent `research` subagents dynamically scaled to partitioned slices or caller-declared budget (Role: `Security Inspector (<Slice>)`) seeded with slice coordinates, discovered anchors, Domain Rubric, and Output Contract (offload extensive proof traces or PoCs to `.agents/scratch/security-<slice>-dossier.md`).
   - Enforce Section 1 Guardrails: ignore stylistic noise; classify every finding explicitly as `[LOCAL-FIX]` or `[ARCHITECTURAL-REFACTOR]`.

3. **Synthesis & Turn-Halt Gate**:
   - Consolidate findings into the Canonical Output Contract with pointers to any offloaded dossiers.
   - Assign definitive Security Posture (`HARDENED`, `LOCALIZED_RISKS`, `CRITICAL_EXPOSURE`).
   - Present completed dossier into conversation stream and halt turn immediately.
