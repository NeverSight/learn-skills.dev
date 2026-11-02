---
name: scout
description: "Investigate real-system best practices, production archetypes, and failure modes before architectural commitment."
---

# scout — Real-System Best Practices & Production Archetype Engine

## Domain Rubric

### 1. Source Authority Hierarchy

Triangulate technical inquiries against authoritative production evidence:

- **Tier 1 (Canonical Standards & Official Specs)**: RFCs, language specifications, cloud vendor reference architectures, and formal technical papers.
- **Tier 2 (High-Scale Production Engineering)**: Tech blogs and architecture disclosures from proven high-scale engineering organizations (e.g., Stripe, Netflix, Cloudflare, Discord, Uber, Meta).
- **Tier 3 (Battle Scars & Postmortems)**: Documented production outages, postmortems, and root-cause analyses revealing edge cases, operational bottlenecks, and failure modes.
- **Exclusion Filter**: Exclude SEO-optimized content farms, unverified personal blog posts, vendor marketing collateral, and unvetted AI summaries.

### 2. Search & Inclusion Budget

- **Exploration Ceiling**: Maximum 8 search queries and 10 fetched pages per scouting run.
- **Inclusion Budget**: Synthesize from 3 to 5 premier, high-signal sources.
- **Short-Circuit Stop**: Terminate search as soon as the canonical pattern and known failure modes are triangulated with primary evidence.

## Canonical Output Contract

```markdown
# Scout Report: <Topic / Inquiry>

## 1. Executive Summary
- **Canonical Production Archetype**: <Boring, battle-tested standard approach adopted by industry leaders>
- **Operational Reality**: <Key complexity, maintenance overhead, or scaling bottleneck in practice>

## 2. Industry Precedents & Battle Scars
| Source / Organization | Pattern Deployed | Production Scale / Context | Known Failure Mode / Trade-off |
| :--- | :--- | :--- | :--- |
| <Org / Paper> | <Architecture / Tool> | <Traffic, Data Volume, SLA> | <Failure point, latency spike, cost trap> |

## 3. Recommended Baseline vs. Traps
- **Recommended Baseline**: <Simplest robust architecture meeting requirements without premature optimization>
- **Premature Traps to Avoid**: <Over-engineered patterns or hype-driven tools that introduce unnecessary failure modes>

## 4. Primary Citations
- [<Source Title>](<Verified URL>) — <Core insight or concrete data point extracted>
```

### Routing

- Deliberate trade-offs or evaluate architectural fit for the project → (via /clarify).
- Baseline is accepted, adequately supported, and the caller requests change planning → (via /changeset).

## Execution Protocol

1. **Query Triangulation & Dispatch**:
   - Formulate 2 to 3 targeted search queries crossing: canonical standards/RFCs, high-scale engineering cases, and failure postmortems.
   - Launch `research` subagent(s) dynamically scaled to inquiry complexity or caller-declared budget (Role: `Real-System Research Scout`) supplying:
     - The triangulated queries and Search Budget (max 8 queries, 10 fetched pages).
     - The **Canonical Output Contract** above as the required output contract (offload deep comparative dossiers to `.agents/scratch/scout-dossier.md` when extensive).
   - Mandate the subagent to inspect full page bodies via URL tools before synthesizing; cite strictly verified URLs and never synthesize from search snippets alone.

2. **Synthesis & Halt**:
   - Emit the completed report into the conversation stream (with pointers to any offloaded dossiers) and halt turn immediately.

