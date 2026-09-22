---
name: baselinedocs-adopt
description: Adopt an existing document, proposal, specification, wiki, export, or other non-baseline format into an adaptive baseline documentation pack. Use when the source material must be distributed into a durable, resumable baselinedocs structure without losing its information, decisions, assumptions, risks, provenance, or open questions.
---

# Baselinedocs Adopt

Adopt source material into a baseline pack that is collectively equivalent in information, but easier to navigate, update, audit, and resume. Do not reconstruct the source as a replacement god document.

## Inputs

Determine or confirm:

- the source artifact or source set
- the target baseline root and pack prefix
- whether a suitable pack already exists
- the source-retention decision: retain, archive separately, or remove after validation
- the source's authority and the meaning of its claims

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Workflow

1. Inspect the complete source before editing. Record its scope, headings, decisions, requirements, workflows, assumptions, risks, open questions, and explicit exclusions.
2. Inspect the repository, canonical documentation, existing baseline pack, and worktree state. Do not treat source-document claims as implementation evidence.
3. Choose the target layout: extend a suitable existing domain pack; create one bounded-domain pack; or create an initiative index with linked domain packs for independent or dependent domains.
4. Create or update the pack documents so their combined content preserves the source information. Distribute material by purpose; do not add a replacement catch-all document.
5. Preserve provenance for every adopted claim, including the source artifact, direct relative links, and the point-in-time interpretation. Explicitly record the adoption stage: declare that foundational material was adopted at the initial project stage ("giai đoạn đầu" / initial baseline inception) with the source document date and adoption date, so downstream agents do not mistake the starting proposal baseline for recent in-flight changes.
6. Mark each claim accurately as `implemented`, `planned`, `decided`, `unverified`, or historical. Resolve contradictions only with repository evidence or an explicit decision.
7. Write a coverage ledger mapping every source section or requirement to its destination baseline document. Include exclusions and intentionally consolidated material.
8. Validate the adopted pack against the three evaluation criteria: Coverage, Purity, and Readiness. When dual-subagent cross-verification is available, launch one subagent to read the adopted pack and one to read the source artifact, cross-checking knowledge inventories against these three criteria.
9. If source removal was authorized, remove it only after coverage validation succeeds. If retention was required, follow the agreed retention method. Never infer either choice.
10. Report changed paths, coverage result, unresolved gaps, source-retention result, evaluation criteria verdicts (Coverage, Purity, Readiness), and the next executable action.

## Distribution

Distribute the source by the document roles in `references/pack-contract.md`, using the smallest applicable set. Add `*.index.md` for initiative navigation and cross-domain relationships when multiple packs are necessary.

A source document usually mixes decisions and open questions into its narrative. Both belong in `hallucination`, not in `introduction` alongside scope: a decision filed under scope loses its reasoning and its rejected alternatives, which is what makes it reversible later by someone who cannot see what it protected.

Do not force content into a file whose role does not fit. Add a narrowly scoped domain pack when separation improves discoverability without duplicating truth.

## Coverage Rules

- Preserve information, not paragraph shape or source-file structure.
- Keep exact requirements, constraints, names, state transitions, ownership boundaries, and negative requirements traceable.
- Preserve open questions as open; do not silently decide them during conversion.
- Preserve explicit unknowns and unsupported claims as unverified.
- Distinguish proposal intent from code, test, deployment, and runtime evidence. When adopting a proposal, RFC, or draft under review, mark the pack status as `draft` and its claims as `proposed` or `unverified`. Never invent an implementation roadmap or execution phases that presume acceptance - downstream agents will mistake fictitious phases for approved work.
- Explicitly declare the adoption stage in provenance. When adopting a foundational architecture proposal or starting specification, declare that adoption occurred at the initial project stage ("giai đoạn đầu" / initial baseline inception) along with the source document date and adoption date. Downstream agents reading the pack must understand that the pack represents the starting project baseline, not a recent or mid-flight operational change.
- Reference the source document directly using relative markdown links across all destination baseline documents where the blueprint or rationale is declared, ensuring clear and verifiable document lineage.
- Never borrow concrete parameters (port numbers, IP addresses, commit hashes, container UIDs, environment account IDs) from another environment or codebase to fill in abstract mentions in the source. Preserve the source's exact level of abstraction; fabricated details cause design conflicts when the proposal changes.
- Respect repository and role boundaries. Tasks outside this repository's remit (such as application surveys, licensing negotiations, or legal assessments) belong in `hallucination` as external dependencies gating the work, not as tasks on the repository's `roadmap`.
- Never create conditional documents (such as `useguide`) for proposals or unbuilt systems without active consumers or operators. Inventing CLI commands or runbooks to populate an unneeded document produces false operational memory.
- Do not claim builds, formatting, static inspection, or documentation review prove live behavior.
- Do not delete, archive, commit, or otherwise alter the source artifact unless the user explicitly authorizes that action.
- If lossless retention is required, verify raw-byte identity; a normalized hash or matching headings is insufficient.

## Evaluation Criteria

Score and verify the adopted pack against three strict criteria before completing adoption:

- **Coverage (Độ bao phủ)**: 100% of the source material's scope, requirements, constraints, architectural decisions, rejected alternatives with reasons, risks, open questions, and comparative reference tables must be traceable in the destination documents. Nothing from the source is dropped, softened, or smoothed away.
- **Purity (Tính thuần khiết)**: Zero hallucination and zero context pollution. The pack must not import concrete values (port numbers, IP addresses, commit hashes, container UIDs, environment account IDs) from other environments or existing code to fill in abstract concepts. It must not invent fictitious implementation phases or CLI runbooks. The source's exact level of abstraction is preserved intact.
- **Readiness (Tính sẵn sàng)**: Downstream agents reading the pack must be able to act without ambiguity. The lifecycle state must accurately reflect reality (`draft`/`proposed` for proposals, `blocked` when gating inputs are missing). Foundational material adopted at inception must be clearly declared as adopted at the initial project stage ("giai đoạn đầu") with point-in-time timestamps so readers do not mistake starting baselines for recent changes. Scope and role boundaries must be respected: upstream prerequisites and cross-domain dependencies belong in `hallucination` as external dependencies, keeping the repository's `roadmap` strictly focused on actionable phases within its remit.

## Output

Produce a baseline pack that is collectively equivalent in information to the adopted source while being easier to navigate, update, audit, and resume, verified clean across Coverage, Purity, and Readiness.
