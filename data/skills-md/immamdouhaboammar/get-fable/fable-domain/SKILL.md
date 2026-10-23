---
name: fable-domain
description: Discuss a domain with the user, research it from real sources, then generate a trusted skill bundle for it - a step-by-step workflow with a flowchart, a domain adapter, a trap fixture, and a smoke eval. Use when the user says "/fable-domain <sector>", "make a skill for <domain>", "add a domain to the fable method", or "give a lesser model Fable's workflow for <domain>". The bundle is the deliverable; a workflow without its flowchart, sources, and trap is not done.
version: 1.0.0
pack: creator
inputs:
  - sector_name
  - user_requirements
requires:
  - web_search_access
  - template_reference
produces:
  - domain_bundle
  - flowchart
  - trap_fixture
gates:
  - no_redline_violations
  - trap_verified
fallback: fable-skill-creator
mutatesWorkspace: true
parallelSafe: false
neural_links:
  precursors:
    - get-fable
  continuations:
    - fable-judge
    - fable-verify
  lateral_peers:
    - fable-skill-creator
  recovery: fable-recover
---

# Fable Domain

The fable-method ships domain adapters that translate its loop into a sector's nouns. This skill creates a new adapter and delivers a usable, step-by-step workflow with a flowchart for the domain.

## Purpose

Generate validated, source-backed domain adapters and trap fixtures for new professional sectors (finance, marketing, legal compliance, devops, etc.). Translate general agent lifecycle discipline into domain-specific evidence standards and failure fraud tables.

## When to Use

- When the user asks to add or generate a domain adapter (`/fable-domain <sector>`).
- When expanding Fable's methodology to non-coding professional sectors.
- When creating a domain-specific trap fixture and evaluation suite.

## When NOT to Use

- When the requested domain requires professional human licensure or presents high-harm risks (medical diagnosis, formal legal advice, investment advice) — refuse and route to a qualified human.
- When the domain does not differ fundamentally from standard software engineering (use `fable-execute` or `fable-plan`).
- Generic skill authoring without domain-specific adapters (use `fable-skill-creator`).

## Inputs

- `sector_name`: The industry or functional discipline requested (e.g. `finance`, `marketing`, `data-analysis`).
- `user_requirements`: Real-world use cases, trusted authorities, and non-negotiable boundaries provided by the user.

## Expected Outputs

1. **Domain Workflow with Flowchart**: Step-by-step approach distilled from research, plus a mermaid flowchart.
2. **Domain Adapter**: Conforming to `references/domains/TEMPLATE.md` with cited primary sources.
3. **Trap Fixture**: Evaluation scenario in `eval/scenarios/` with `GROUND-TRUTH.md` defining the sector's central fraud.
4. **Smoke Eval**: Initial control-vs-adapter validation runs.

## Procedure

1. **Stage 1: Discuss**: Adaptively clarify the use case, practitioner standards, trusted authorities, and forbidden actions. Enforce Red-lines (refusal for medical/legal/financial advice) and Scope stops (refusal if domain is standard software engineering).
2. **Stage 2: Research**: Perform bounded web research against authoritative sources. Extract regulations, platform policies, practitioner evidence standards, and documented failure modes.
3. **Stage 3: Generate the Bundle**:
   - Read all existing adapters in `references/domains/` and the governing template.
   - Define exact sector scope boundaries.
   - Author the ordered workflow and mermaid flowchart.
   - Write the adapter according to `references/domains/TEMPLATE.md`.
   - Wire all routing surfaces (registry, catalog, docs).
   - Build the trap fixture with objective violation markers.
4. **Stage 4: Verify & Smoke-Eval**:
   - Run repo checks to ensure structural integrity.
   - Run smoke eval comparing bare model behavior vs adapter-directed behavior.
   - Run `fable-judge` adversarial audit over the bundle's claims and sources.
   - Deliver outcome-first completion report.

## Decision Rules

- Red-Line Refusal: If a domain involves clinical medicine, formal legal counsel, or financial trading advice, refuse generation immediately.
- Scope Gate: If a requested sector's evidence consists merely of files and stack traces, stop and declare that core coding skills already cover it.
- Primary Source Mandate: Every regulatory threshold, compliance statute, or industry rule must cite a verified web source with access date.

## Tool Policy

- Use web search to fetch authoritative primary documents and regulatory texts.
- Do not invent fictional regulatory citations or synthetic policy numbers.
- Generate standard Mermaid diagrams for all workflow visualizations.

## Evidence Requirements

- Primary source URLs and verification dates in the adapter's Sources section.
- Verifiable trap fixture with reproducible failing/passing test runs.
- Passing `fable-judge` evaluation report.

## Failure Handling

- If web access is unavailable to verify real-world regulations, stop generation rather than hallucinating standards.
- If the smoke eval indicates no behavioral difference on the trap fixture, report the adapter as unproven.

## Completion Criteria

- All four bundle deliverables created and verified: workflow flowchart, adapter, trap fixture, and smoke eval.
- Zero red-line safety violations.
- Registry and documentation references cleanly synchronized.
