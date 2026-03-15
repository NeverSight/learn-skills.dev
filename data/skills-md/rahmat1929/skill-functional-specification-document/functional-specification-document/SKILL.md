---
name: functional-specification-document
description: Generate a comprehensive Business Requirements Document (BRD) or Functional Specification Document (FSD) from project requirements, PRDs, briefs, or interactive interviews. Use this skill whenever the user mentions BRD, business requirements, functional specs, FSD, software specification, feature specification, system specification, functional requirements document, or wants to document business needs or how a system should behave. Also trigger when users ask to "spec out" a feature, write up requirements, or create a detailed plan for stakeholders or developers — even if they don't use the exact terms explicitly.
---

# Requirements & Functional Specification Document Generator

This skill produces structured Business Requirements Documents (BRDs) and implementation-ready Functional Specification Documents (FSDs). A BRD defines the business problem, goals, stakeholders, and high-level business rules. An FSD bridges the gap between what stakeholders want and what engineers need to build. It answers "what does the system do and how should it behave" without dictating internal architecture.

## Content Rules

These rules govern every document this skill produces. Follow them strictly:

- **Distinguish Document Types** — Know whether you are writing a BRD or an FSD. The BRD focuses on business priorities (the "why" and "what"), stricly avoiding technical constraints and implementation details. The FSD focuses on system behavior (the "how it behaves") translating those constraints to actionable scopes that developers understand.
- **NO CODE SAMPLES** — Provide only explanations, conceptual descriptions, and structured information. Never include source code, pseudo-code, or implementation snippets.
- **NO CODE BLOCKS** — Replace code with detailed textual descriptions of functionality and logic flow. The only permitted fenced blocks are Mermaid diagrams.
- **"What" and "why", not "how"** — Use clear, developer-friendly language that focuses on system behavior and business rationale, not implementation mechanics.
- **Architectural understanding first** — Prioritize system relationships, module interactions, and data flow over technical details.
- **Mermaid exclusively for visuals** — Use Mermaid format for all diagrams: flowcharts, sequence diagrams, state diagrams, entity relationships, and architecture overviews. No ASCII art, no plaintext diagrams, no embedded images.
- **Exclude API & Database** — The FSD does not cover API endpoint specifications or database schema design. Those belong in separate API Specification and Database Design documents respectively. The FSD references them but does not define them.

## When to use this skill

- A user wants to define the business goals and high-level requirements for an initiative (BRD)
- A user wants to create a functional specification for a new product, feature, or system (FSD)
- A user has a PRD, project brief, or set of requirements and needs them turned into a detailed BRD or FSD
- A user asks to "spec out" or "write up" how something should work or what it should achieve
- A user needs to document business goals, functional requirements, use cases, or acceptance criteria

## Workflow

### Phase 1: Gather Context

Before writing anything, understand what you're specifying. There are two paths depending on what the user provides:

**Path A — User provides a source document (PRD, brief, requirements list, etc.):**
Read the document thoroughly. Extract the core requirements, identify gaps, and list clarifying questions. Present the questions to the user before proceeding. Don't guess at ambiguous requirements — ask.

**Path B — No source document (interactive interview):**
Walk through these questions to build a mental model of the system:

1. What is the product/feature? (one-sentence elevator pitch)
2. Who are the users? (roles, personas, access levels)
3. What are the core workflows? (the 3-5 things users will actually do)
4. What external systems does this interact with? (third-party services, other internal modules)
5. Are there constraints? (regulatory, platform, timeline, tech stack)
6. What does success look like? (KPIs, acceptance criteria)

Don't ask all questions at once — use the first couple of answers to tailor follow-ups. The goal is to get enough information to write a solid first draft, not to exhaustively document everything upfront.

### Phase 2: Write the Document

Determine if the user needs a BRD (business focus) or an FSD (system behavior focus). Read `references/brd-template.md` (for BRDs) or `references/fsd-template.md` (for FSDs) for the full document template and section-by-section guidance. Follow that template structure, but adapt it to the project — skip sections that genuinely don't apply and expand sections that need more depth.

**Key principles while writing:**

- **Be specific.** "The system should be fast" is not a requirement. "Search results return within 200ms for up to 10,000 records" is.
- **Use consistent language.** "SHALL" = mandatory, "SHOULD" = recommended, "MAY" = optional. Define this in the Document Conventions section and stick to it.
- **Every feature gets acceptance criteria.** If you can't write a test for it, the requirement isn't clear enough.
- **Describe behavior, not implementation.** State what the system does and why, never how it does it internally.
- **Assign priority to each requirement.** Use MoSCoW: Must / Should / Could / Won't. This prevents scope creep and helps teams negotiate tradeoffs.
- **Number every requirement.** Use a hierarchical ID scheme (e.g., FR-3.2.1) so requirements are traceable from spec to test to implementation.
- **Use Mermaid for all diagrams.** State machines, user flows, system context, sequence diagrams — all in Mermaid format.

### Phase 3: Output

Save the document as a Markdown file. Use the naming convention: `BRD-[Project-Name].md` or `FSD-[Project-Name].md`.

After generating the document, run the validation script to check structural completeness. The script validates required sections, requirement ID format, acceptance criteria presence, MoSCoW labels, Mermaid diagram presence, and flags any code blocks that shouldn't be there.

If validation reports issues, fix them before presenting the final document to the user. Show the user the validation summary alongside the finished document so they know it's been checked.

### Phase 4: Review & Iterate

Present the draft to the user. Highlight:
- Sections where you made assumptions (flag these explicitly)
- Areas that need more detail from stakeholders
- Requirements you marked as "Could" or "Won't" that the user might want to reconsider

Incorporate feedback and regenerate. Each revision should re-run validation.

## Document Structure Summary

### Business Requirements Document (BRD)
The BRD follows this top-level structure (see `references/brd-template.md` for details):
1. **Executive Summary** — Purpose, background, and problem statement
2. **Business Goals & Objectives** — Project goals and success metrics (KPIs)
3. **Project Scope** — In scope and out of scope
4. **Stakeholders** — Roles, influence, and responsibilities
5. **Business Requirements** — High-level requirements mapped to MoSCoW priorities and business rules
6. **Assumptions, Constraints & Dependencies**
7. **Glossary of Terms**

### Functional Specification Document (FSD)
The FSD follows this top-level structure (see `references/fsd-template.md` for details):

1. **Introduction** — Purpose, scope, definitions, references, conventions
2. **Product Overview** — Context, high-level functions, users, environment, constraints, assumptions
3. **Functional Requirements** — Feature breakdown with IDs, descriptions, acceptance criteria, priority, business rules; use cases with main/alternative/exception flows
4. **User Interface Requirements** — Screen descriptions, interaction behavior, navigation, accessibility
5. **Non-Functional Requirements** — Performance, security, reliability, scalability, maintainability, accessibility
6. **System Behavior & Error Handling** — State transitions (Mermaid), error matrix, edge cases
7. **Approval & Sign-Off** — Stakeholder table, revision history
8. **Appendices** — Mermaid diagrams, supplementary material

## Output Quality Checklist

Before delivering the final FSD, mentally verify:

- [ ] Every requirement has a unique ID and priority (MoSCoW)
- [ ] (FSD only) Every feature has testable acceptance criteria
- [ ] (FSD only) Use cases cover main flow + at least one alternative/error flow
- [ ] (FSD only) Error handling is specified for user-facing operations
- [ ] (FSD only) Non-functional requirements have measurable targets
- [ ] No section is left as a placeholder or TODO
- [ ] Cross-references between sections are consistent
- [ ] All diagrams use Mermaid format (no code blocks, no ASCII art)
- [ ] No code samples or code blocks appear anywhere in the document
- [ ] No API endpoint definitions or database schemas are included
- [ ] The document serves its audience correctly (BRD for business stakeholders, FSD for developers/QA).
