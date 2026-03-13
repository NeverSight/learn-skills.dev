---
name: code-audit-readonly
description: Execute a complete, deterministic, read-only repository audit and produce a single `improvements.md` action plan with traceable findings (file + lines), severity, category, impact, and high-level fixes. Use when users ask for full code audits, security/performance/architecture reviews, file-by-file analysis, or technical debt mapping without modifying project files.
---

# Code Audit Readonly

Run a full technical repository audit in read-only mode and record everything in `improvements.md`.

## Mandatory rules

1. Operate in read-only mode for the audited project.
2. Do not edit source code, configs, or tests in the audited project.
3. Do not run automatic refactors, formatters that write to disk, or destructive commands.
4. Allow only the creation/update of `improvements.md` as the final audit output.
5. Do not ask for confirmation to proceed with the audit; execute the plan end to end.
6. Record every validated finding; do not impose arbitrary limits.
7. If multiple locations share the same issue pattern, still register every location with explicit file and line references.
8. This audit is intentionally slow: prioritize depth, evidence quality, and completeness over speed.
9. Do not optimize for fast turnaround if that reduces analysis coverage or confidence.
10. Never reproduce secrets or raw credential material in `improvements.md`, tool output, or final responses.
11. For secret-related findings, record only the file path, line range, secret class, and sanitized context needed to explain the risk.
12. Do not quote full offending lines when they contain tokens, keys, passwords, cookies, connection strings, private keys, or other sensitive values.

## Sensitive data handling

Apply these rules whenever the audit touches credentials, secrets, or other sensitive material:

1. Treat any suspected secret as high-risk content that must stay redacted.
2. Confirm the issue via read-only inspection, but never echo the literal value back to the user.
3. Describe the finding with neutral placeholders such as `<redacted-api-key>` or `<redacted-private-key>` only when a placeholder is necessary.
4. Prefer descriptions like `hardcoded API credential in config bootstrap` over copying the surrounding source line.
5. If a log, error, or telemetry path leaks sensitive data, describe the leaked data class and exposure path without reproducing payload contents.
6. Keep traceability through file paths and line ranges, not through verbatim secret material.

## Mandatory analysis scope

1. Correctness and logic
   1. Detect obvious and subtle bugs.
   2. Check for race conditions, inconsistent states, and incorrect async/concurrency usage.
   3. Evaluate error/exception handling, nullability, typing, and unsafe conversions.
   4. Cover edge flows and extreme scenarios.
2. Performance
   1. Find unnecessary allocations, expensive loops, N+1 patterns, excessive I/O, and repeated work.
   2. Check for caching opportunities and inappropriate data structures.
   3. Correlate bottlenecks across modules.
3. Duplication and maintainability
   1. Detect literal duplication and logical duplication.
   2. Identify long functions, mixed responsibilities, and excessive coupling.
   3. Flag confusing internal APIs, ambiguous names, and outdated comments.
4. Security (mandatory, thorough)
   1. Hardcoded secrets (tokens, keys, passwords, sensitive endpoints), reported with redacted descriptions only.
   2. Injection vectors (SQL/NoSQL/command/template).
   3. XSS, CSRF, SSRF, open redirect, path traversal.
   4. Insecure uploads (insufficient type/size/validation checks).
   5. Authentication/authorization issues (bypass, missing checks, privilege escalation).
   6. Insufficient validation/sanitization.
   7. Weak cryptography and inadequate hashing.
   8. Insecure configurations (overly broad CORS, missing headers, debug in production).
   9. Vulnerable dependencies and problematic versions.
   10. Sensitive data leakage in logs, errors, and telemetry.
5. Observability and reliability
   1. Validate log quality without exposing secrets.
   2. Verify metrics/tracing where applicable.
   3. Evaluate consistency and actionability of error messages.
6. Tests and quality
   1. Identify coverage gaps in critical areas.
   2. Detect brittle tests and missing integration coverage.
   3. Map untested edge cases.

## Execution method

1. Map the repository tree and list all relevant files:
   1. Application code, internal libraries, configs, scripts, CI, Docker, IaC, migrations, and tests.
2. Initialize `improvements.md` with:
   1. A short system summary inferred from the structure.
   2. A "Progress Tracking" section with all relevant files marked as `pending`.
   3. Severity and category conventions.
3. Review each file sequentially and deterministically:
   1. Read the entire file.
   2. Record specific findings and correlate with related imports/calls/contracts.
   3. Update progress tracking.
   4. Explicitly record: `File fully reviewed: <path/to/file>`.
   5. Before moving to the next file, run a quick self-check for missed edge cases, security vectors, and cross-file impacts.
4. Run read-only auxiliary checks when useful:
   1. Static analysis, linter, and typecheck in read-only mode.
   2. Run tests without writing to disk.
   3. Dependency/CVE audit.
5. Close `improvements.md` with:
   1. A complete finding inventory (all findings captured during the audit).
   2. A prioritized backlog that references finding IDs and contains no artificial cap.
   3. A detailed phased remediation plan (see "Detailed planning requirements").
   4. A brief completeness checkpoint describing what was verified to ensure no relevant area was rushed or skipped.

## Progress tracking

Apply these rules to keep progress tracking clear and stable:

1. Build a canonical file list once:
   1. Normalize paths (`./` removed, no trailing slash, consistent case as seen on disk).
   2. Sort the list before writing "Progress Tracking".
2. Keep exactly one progress row per canonical file path.
3. Update progress in-place:
   1. Change the existing row status (`pending` -> `in_progress` -> `reviewed`).
   2. Never append a second row for the same file.
4. Write `File fully reviewed: <path/to/file>` exactly once per file.
5. If a file is revisited, add notes under the same file entry; do not create a new checklist row or a second `File fully reviewed` line.
6. Before finishing, validate:
   1. Number of `reviewed` rows == number of unique relevant files.
   2. "Progress Tracking" appears exactly once in the report.
   3. Every finding location appears in at least one reviewed file entry.

## Example report structure

Use this high-level structure to keep the report consistent and to ensure a single "Progress Tracking" section:

```markdown
# improvements.md

## 1. System summary
- Inferred architecture and main modules.
- Main risk surfaces.

## 2. Conventions
- Categories and severity scale used in the audit.
- Finding ID convention (`A001`, `A002`, ...).

## 3. Progress Tracking
- [ ] path/to/file-a.ext
- [ ] path/to/file-b.ext
- [ ] path/to/file-c.ext

## 4. Complete finding inventory
### A001
Category: ...
Severity: ...
Location: ...
Problem: ...
Impact: ...
Suggestion: ...
Correlation notes: ...
Security (if applicable): ...

### A002
...

## 5. Prioritized backlog (all findings)
- Priority 1: A00X, A00Y...
- Priority 2: A00Z...

## 6. Detailed phased remediation plan
### Phase 1
- Objective
- Findings included
- Dependencies
- Validation gates
- Exit criteria

### Phase 2
...

### Phase 3
...
```

## Categories and severity

Use only these categories:
- `Bug`
- `Performance`
- `Security`
- `Duplication`
- `Code Quality`
- `Architecture`
- `Maintainability`
- `Observability`
- `Tests`
- `Dependencies`

Use only these severity levels:
- `Critical`
- `High`
- `Medium`
- `Low`

## Mandatory format for each finding

Use unique sequential IDs (`A001`, `A002`, ...).

```text
A0XX
Category: <...>
Severity: <Critical|High|Medium|Low>
Location: <file>:<start line>-<end line>
Problem: <objective description>
Impact: <real or potential impact>
Suggestion: <high-level fix, without editing code>
Correlation notes: <related files/flows>
Security (if applicable): <plausible abuse scenario + mitigation>
```

For secret-related findings, keep the same structure but never include the raw secret value or paste the full source line. Use file and line references plus sanitized descriptions only.

## Detailed planning requirements

The planning phase in `improvements.md` must be explicit and implementation-oriented. Use this structure:

1. Planning assumptions and constraints:
   1. Confirm read-only audit boundaries.
   2. List unknowns that may affect remediation sequencing.
2. Prioritized backlog (complete):
   1. Include all findings (`A001...A0XX`) with:
      1. Priority order.
      2. Estimated effort (`S`, `M`, `L`) with a short rationale.
      3. Primary risk type (`Correctness`, `Security`, `Performance`, `Reliability`, `Maintainability`).
3. Phase plan with objective and controls:
   1. For each phase, include:
      1. Objective.
      2. Findings included (explicit ID list).
      3. Dependencies and ordering constraints.
      4. Validation gates (tests/checks/evidence expected after fixes).
      5. Exit criteria (what must be true to close the phase).
4. Sequencing rules:
   1. Resolve `Critical` and exploitable `High` security/correctness findings first.
   2. Schedule performance and maintainability work after risk containment unless blocking.
   3. Call out parallelizable workstreams and non-parallelizable bottlenecks.
5. Delivery roadmap:
   1. Provide a suggested execution order by batch/wave.
   2. For each batch, list expected risk reduction and verification focus.

## Traceability requirements

1. Make every finding traceable to file and line/section.
2. Avoid generic recommendations without evidence.
3. Register all validated findings found during the audit, including low-severity and repeated-location findings.
4. Explicitly record uncertainties when evidence is partial.
5. For sensitive findings, preserve traceability with file and line references while keeping all credential material redacted.

## Completion criteria

Finish only when:
1. All relevant files are marked as reviewed in Progress Tracking.
2. Each reviewed file has the line `File fully reviewed: ...`.
3. `improvements.md` contains the complete finding inventory, a prioritized backlog, and a detailed phased plan.
4. The audited project remains intact, with only `improvements.md` as the audit output artifact.
