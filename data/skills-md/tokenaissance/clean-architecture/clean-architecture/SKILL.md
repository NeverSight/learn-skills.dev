---
name: clean-architecture
description: |
  Clean Architecture practitioner's guide. Trigger when users ask about four-layer architecture, dependency direction & inversion (DIP), an entity directly depending on external SDKs, ORM/data access layer (Repository pattern) design, microservice decomposition, technology selection, over-engineering, or architecture refactoring. Covers business logic organization in Express/Next.js/Go/Spring projects, MongoDB→PostgreSQL migrate, REST→GraphQL migrate, third-party integration (Stripe/PayPal), Redis caching, and Kafka message queue evaluation. Evaluates architecture against Robert C. Martin's Clean Architecture, SOLID principles, and the Dependency Rule; uses Musk's five-step algorithm as an anti-over-engineering gate. Do NOT trigger on: pure code quality, DDD, system design interviews, single-DTO micro-decisions, cache library selection, DI framework debugging, diagram drawing, translation, or formatting requests — answer directly without invoking this skill.
metadata:
  author: Tokenaissance
  version: "1.2.2"
  upstream_inspiration: wondelai/skills:clean-architecture; affaan-m/everything-claude-code; giuseppe-trisciuoglio/developer-kit; pproenca/dot-skills
---

# Clean Architecture

Practical layering, DIP enforcement, and anti-over-engineering — grounded in Robert C. Martin's Clean Architecture, SOLID (SRP/OCP/LSP/ISP/DIP), component principles (CCP/CRP/ADP/SDP/SAP), and Musk's five-step algorithm.

## Router Rules

- Description-based routing: trigger on architecture-significant scenarios — four-layer decomposition, DIP violation, Repository/Adapter boundary design, technology evaluation, over-engineering detection.
- Once triggered, follow Workflow. This is an architecture governance entrypoint, not a debugging or code-review tool.
- Hard-exclusion list (answer directly, do NOT invoke): pure code quality, DDD, system design interviews, single-DTO micro-decisions, cache library selection, DI framework debugging, diagram drawing, translation, formatting.
- Stack-agnostic: explain in canonical four-layer terms (Entities / Use Cases / Interface Adapters / Frameworks & Drivers), then map to the user's actual framework (Express/Next.js/Go/Spring). Service/Repository/Controller are implementation-pattern mappings, not primary layer names. Adopt the user's existing conventions where established.
- Read-only audit requests: zero file modifications.

## Use when

- Monolithic controller/route bloat → SRP decomposition + DIP-driven refactoring into four layers
- Entity/Use Case directly importing external SDK (Stripe/PayPal) or DB driver → Dependency Rule audit
- Technology evaluation: microservices / Kafka / Redis / caching → bounded-context fitness and CCP alignment
- Storage or API migration (MongoDB→PostgreSQL, REST→GraphQL) → Repository boundary design, Ports & Adapters impact
- Multi-vendor integration → Adapter layer design, swappability via interface contracts

## Do NOT use when

- Diagramming, translation, formatting, title-writing, document summarization
- Framework debugging: DI wiring failures, HTTP 500, slow SQL, index optimization
- Micro-decisions: React component splitting, single DTO addition, naming
- System design interview problems (Twitter-scale, bit.ly, Saga pattern, multi-tenancy)
- User explicitly opts out ("don't talk about architecture," "just explain")

## Workflow

1. **Diagnose — probe before prescribe**: Elicit scale, team size, concurrency, change frequency. CCP: same change reason + same change cadence → co-locate. SRP: different actors → separate. Invest boundaries only on proven variation axes (3+ historical changes at the same seam); YAGNI on unproven axes.
2. **Principle evaluation**: Assess against the four-layer concentric model + Dependency Rule (∀ dep → inward; Entities ⊥ Use Cases ⊥ Interface Adapters ⊥ Frameworks & Drivers), SOLID (SRP/OCP/LSP/ISP/DIP), component cohesion (REP/CCP/CRP) + coupling (ADP/SDP/SAP), Musk's five-step algorithm, and engineering dialectics (unity of opposites, quantitative→qualitative change, negation of negation). See Reference Map.
3. **Structured answer** (architecture scenario confirmed):
   - **Four-layer map**: Entities / Use Cases / Interface Adapters / Frameworks & Drivers — each layer named with contents
   - **Dependency Rule**: source-code dependencies point inward only — concrete direction arrows drawn
   - **Stack mapping**: canonical layers projected onto user's actual framework + directory structure
   - **Code example**: minimal before/after with layer labels, ≤ 50 lines
4. **Anti-over-engineering gate**: Every "adopt complex solution" recommendation must survive Musk's five steps — Question → Delete → Simplify → Accelerate → Automate, order invariant. Monolith suffices → do NOT propose microservices. Single implementation → do NOT propose interface abstraction.
5. **Documentation isomorphism** (as needed): Architecture decisions must persist as discoverable artifacts for downstream Agents and developers. Code change without documentation update = incomplete. Granularity matches impact radius: cross-layer refactor → L3→L2→L1 full loop; single import change → one L3 line. See Reference Map → Documentation Isomorphism.

## Output Contract

- **Hit**: diagnosis + four-layer map + Dependency Rule explication + stack mapping + ≤50-line code example + anti-over-engineering verdict. Major architecture decisions → append L2/L3 documentation skeletons.
- **Miss**: answer directly; suppress this skill's template.
- **Scaffold restraint**: full directory scaffold (> 5 directories or named files) only on explicit request. Default: layer-level directory suggestions (≤ 5 directory names, no specific files).

## Reference Map

- Theory & Principles: `references/clean-architecture.md`
- Anti-Over-Engineering: `references/musk-algorithm.md`
- Engineering Philosophy: `references/engineering-philosophy.md`
- Documentation Isomorphism: `references/geb-fractal-docs.md`
