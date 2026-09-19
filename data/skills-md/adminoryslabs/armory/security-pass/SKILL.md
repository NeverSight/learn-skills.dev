---
name: security-pass
description: Runs a context-aware security review of a software project — first understands what the system does and who could attack it, then adapts the analysis instead of running a static checklist. Produces a ranked, evidence-backed findings report and triages each finding by what kind of action it needs (code fix, spec change, design/ADR change, product decision, or accepted risk). Never edits the project — analysis only. Use when the user asks for a security review, security pass, security audit, or to find vulnerabilities in their project.
---

# Security Pass

## Goal

Run a **Security Pass**: a full security review of an existing project that adapts to whatever
that project actually is — its domain, stack, architecture, and the documents it happens to have.
This is not a fixed checklist run blindly against every project. It is a capability (the **Security
Harness**) that, each time it executes, first builds a real model of the system and only then hunts
for risk inside that model.

The flow this skill implements, every time:

```
PROJECT → DISCOVER → UNDERSTAND → ANALYZE → CORRELATE → DEDUPLICATE → TRIAGE → REPORT
```

## Non-negotiable rule

This skill only **analyzes, detects, explains, and proposes**. It never modifies code, specs,
configuration, or architecture during a Security Pass. Product decisions, architecture changes,
and risk acceptance stay with the human — this skill's job ends at a clear report they can act on.

## Reusability — do not assume the project

Do not assume language, framework, database, architecture style, cloud provider, auth model, or
type of application. All of that gets discovered in step 1, not guessed from the skill's own
priors. A project with no documents beyond source code is a valid target — scope the pass to what
exists and say explicitly what layers were skipped for lack of material.

## Required Input

None is mandatory in isolation. The skill discovers what the project actually has:

- Product docs (PRD, requirements)
- Architecture / technical design / ADRs
- Specs and tasks (SDD artifacts, if the project uses that workflow)
- Source code
- Tests
- Configuration and environment files
- Dependency manifests
- CI/CD pipelines
- `CLAUDE.md` and other agent-context files
- Any other relevant documentation

If a category doesn't exist, skip it and say so in the report — do not invent content to fill a
gap.

## Workflow

### 1. Discover the project

Before analyzing security, build a mental model of the system. Read whatever exists from the list
above (glob/grep first, don't assume file layout). From it, work out:

- What the system does and who uses it
- What components exist and how they talk to each other
- What data it handles, and which of that data is sensitive
- What resources it protects
- Its inputs and outputs
- What actors exist — including which of them could plausibly be malicious
- Where the trust boundaries actually are
- What external integrations exist
- Which operations are especially sensitive (money, auth, PII, admin actions, destructive actions)

This model is what step 2 gets pointed at. Skipping this and jumping straight to code is the
single biggest way this skill degrades into a generic linter.

### 2. Analyze layer by layer — only the layers that exist

For each layer actually present in the project, ask its guiding question and hunt for real,
evidence-backed problems. Use `assets/finding-categories.md` as **vocabulary to recognize a
problem when you see one** — not as a box-ticking checklist to march through mechanically. A
category with nothing wrong in this project produces no finding; it does not need to be reported
as "checked."

- **Product / requirements** — guiding question: *"What could an attacker do with the capabilities
  this system offers?"* Look for unconsidered malicious actors, sensitive data, critical
  operations, missing security requirements, dangerous assumptions, ambiguous requirements,
  privacy/integrity/availability gaps.
- **Architecture / design** — attack surface, trust boundaries, authn/authz, privilege boundaries,
  data exposure, secrets handling, cryptography, isolation between components, failure modes. For
  every issue: state what decision exists, what risk it introduces, under what concrete scenario
  it's exploitable, and what mitigations exist or are missing. Do not flag a decision as insecure
  merely because an alternative exists — justify it against this specific system.
- **Specs / tasks** — guiding question: *"Does this spec allow the behavior to be implemented
  securely?"* Look for missing authz/authn, missing validation, missing limits, unhandled error
  states, unprotected sensitive data, missing negative/abuse cases, ownership and permission gaps,
  invalid-state handling, absent security acceptance criteria. Propose concrete acceptance
  criteria for gaps found — do not edit the spec.
- **Code** — adapt to the real stack in front of you. Typical categories: authentication bypass,
  broken access control, privilege escalation, insecure direct object/resource access, injection,
  unsafe input handling, path traversal, command execution, sensitive data exposure, secrets in
  code, weak cryptography, insecure session/token handling, business-logic abuse, meaningful race
  conditions, replay attacks, resource exhaustion, insecure error handling, insecure defaults,
  dependency/supply-chain risk, unsafe file handling, misconfiguration, sensitive data in logs,
  missing controls a system like this one needs. Every finding needs concrete evidence from the
  project — "this could theoretically be improved" is not a finding.
- **Tests** — what security properties are already verified, what negative/abuse scenarios are
  covered, what important controls have no test at all, and which security invariants deserve a
  test. Propose concrete tests where useful.

### 3. Correlate and deduplicate

If the same root problem shows up in more than one layer (e.g. a missing authorization check
visible in both the spec and the code), merge it into a single finding that names every affected
layer — don't report it three times.

### 4. Write findings using this exact structure

```
ID
Title
Severity        (CRITICAL | HIGH | MEDIUM | LOW | INFO)
Confidence       (HIGH | MEDIUM | LOW)
Category
Affected artifact
Location
Description
Evidence
Attack scenario
Potential impact
Existing mitigation
Recommended remediation
Suggested verification
Required change type
```

Discipline:

- Never raise severity without a stated justification tied to this project's actual context.
- Never write a purely hypothetical finding with no evidence in the project.
- If there isn't enough information to confirm a real vulnerability, set `Confidence: LOW` and
  state exactly what information is missing — don't inflate confidence to sound thorough, and
  don't drop the finding either.

### 5. Triage — assign `Required change type`

Every finding gets exactly one:

- `CODE FIX`
- `TEST FIX`
- `SPEC CHANGE`
- `DESIGN / ADR CHANGE`
- `PRODUCT / REQUIREMENT CHANGE`
- `PROCESS / HARNESS CHANGE`
- `ACCEPT RISK`

This skill has no authority to change product scope, architecture, ADRs, business decisions, or
to accept a risk on the user's behalf. Any finding tagged `DESIGN / ADR CHANGE`,
`PRODUCT / REQUIREMENT CHANGE`, or `ACCEPT RISK` must be explicitly called out in the report's
**Governance / Decision Required** section as needing a human decision — never silently resolved.

### 6. Avoid false positives — quality over quantity

Do not report: style preferences dressed up as vulnerabilities, purely theoretical issues with no
project evidence, duplicates, issues already mitigated elsewhere in the project, controls that are
irrelevant to this specific system. A short report of real findings beats a long report padded
with noise — padding is what makes teams stop reading security reports.

### 7. Write the report

Write `SECURITY-REPORT.md` at the project root, following `assets/report-template.md`:

- Executive Summary
- Security Strengths
- Findings
- Priority
- Governance / Decision Required

## Output

`SECURITY-REPORT.md` — nothing else in the project changes. This skill never touches code, specs,
config, or documentation other than writing this one report file.

## Quality Gate

Before returning, silently check:

- Discovery actually happened first — the analysis in step 2 is grounded in the model built in
  step 1, not a generic pass over the code.
- Every layer that genuinely exists in the project was reviewed; any layer skipped for lack of
  material is stated explicitly, not silently omitted.
- Every finding traces to concrete evidence (a file, a line, a spec, a requirement) — nothing
  invented "because it could theoretically happen."
- No `CRITICAL`/`HIGH` severity without a stated justification.
- Findings requiring a human decision are explicitly flagged in Governance / Decision Required —
  none were resolved as if this skill had that authority.
- The project itself is untouched — this was a report-only pass.

## What this skill deliberately does not do yet

It runs on-demand, invoked directly. It's built so its pieces (discovery, per-layer analysis,
finding structure, triage) could later plug into code review, PR checks, CI/CD, or new-spec
workflows — but that wiring isn't part of this skill. Don't build it speculatively; add it when
there's a real need to run this automatically instead of on demand.
